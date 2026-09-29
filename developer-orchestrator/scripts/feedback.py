#!/usr/bin/env python3
"""Local, offline orchestration evidence. Python standard library only."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sqlite3
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path


TOKEN_FIELDS = (
    "input_tokens", "output_tokens", "cached_input_tokens",
    "cache_read_input_tokens", "cache_creation_input_tokens",
)
OUTCOMES = ("unverified", "pass", "fail")


def read_metrics(path: Path, provider: str, resumed: bool) -> dict:
    """Only consume terminal usage; never parse worker prose as evidence."""
    raw = path.read_text()
    try:
        decoded = json.loads(raw)
        events = decoded if isinstance(decoded, list) else [decoded]
    except json.JSONDecodeError:
        try:
            events = [json.loads(line) for line in raw.splitlines() if line.strip()]
        except json.JSONDecodeError:
            return {"status": "unrecognized", "tokens": {}}
    if not events or not all(isinstance(event, dict) for event in events):
        return {"status": "unrecognized", "tokens": {}}
    if provider == "claude":
        terminal = [event for event in events if event.get("type") == "result"]
        failed = any(event.get("is_error") or event.get("permission_denials")
                     for event in terminal)
    else:
        terminal = [event for event in events if event.get("type") == "turn.completed"]
        failed = any(event.get("type") in ("error", "turn.failed") for event in events)
    status = "error" if failed else ("completed" if terminal else "unrecognized")
    tokens = {}
    if not resumed:
        for field in TOKEN_FIELDS:
            values = [event.get("usage", {}).get(field)
                      if isinstance(event.get("usage"), dict) else None
                      for event in terminal]
            if values and all(type(value) is int and value >= 0 for value in values):
                tokens[field] = sum(values)
    return {"status": status, "tokens": tokens}


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    db = sqlite3.connect(path, timeout=30)
    path.chmod(0o600)
    db.execute("CREATE TABLE IF NOT EXISTS attempts "
               "(task TEXT, worker TEXT, attempt INTEGER, data TEXT, "
               "PRIMARY KEY (task, worker, attempt))")
    db.execute("CREATE TABLE IF NOT EXISTS finishes (task TEXT PRIMARY KEY, data TEXT)")
    db.commit()
    return db


def rows(db: sqlite3.Connection, table: str) -> list[dict]:
    # Table names are internal constants, never CLI input.
    return [json.loads(row[0]) for row in db.execute(f"SELECT data FROM {table}")]


def nonnegative(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be finite and nonnegative")
    return number


def positive(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def record(db: sqlite3.Connection, args: argparse.Namespace) -> dict:
    if args.outcome != "unverified" and not args.evidence.strip():
        raise ValueError("verified outcomes require independent check evidence")
    metrics = read_metrics(args.result, args.provider, args.resumed)
    if args.outcome == "pass" and (args.exit_code != 0 or metrics["status"] != "completed"):
        raise ValueError("cannot pass a failed or unrecognized CLI run")
    case_hash = hashlib.sha256(args.case_file.read_bytes()).hexdigest() if args.case_file else None
    entry = {key: getattr(args, key) for key in (
        "task", "worker", "attempt", "category", "policy", "provider", "model", "effort",
        "role", "seconds", "exit_code", "outcome", "evidence", "failure_kind", "resumed",
    )}
    entry.update(time=time.time(), case_hash=case_hash, **metrics)
    # Lock before checking invariants so concurrent recordings cannot race.
    with db:
        db.execute("BEGIN IMMEDIATE")
        if db.execute("SELECT 1 FROM finishes WHERE task = ?", (args.task,)).fetchone():
            raise ValueError("task already finished; use a new task ID for another trial")
        prior = [json.loads(row[0]) for row in db.execute(
            "SELECT data FROM attempts WHERE task = ?", (args.task,))]
        if any(row["policy"] != args.policy or row["case_hash"] != case_hash for row in prior):
            raise ValueError("task policy and case file must remain identical across workers")
        previous_attempts = [row["attempt"] for row in prior if row["worker"] == args.worker]
        if args.attempt != max(previous_attempts, default=0) + 1:
            raise ValueError("attempts must start at 1 and increase consecutively per worker")
        db.execute("INSERT INTO attempts VALUES (?, ?, ?, ?)",
                   (args.task, args.worker, args.attempt, json.dumps(entry)))
    return {"recorded": [args.task, args.worker, args.attempt], "status": metrics["status"]}


def finish(db: sqlite3.Connection, args: argparse.Namespace) -> dict:
    if not args.evidence.strip():
        raise ValueError("final outcome requires integration/review evidence")
    with db:
        db.execute("BEGIN IMMEDIATE")
        if not db.execute("SELECT 1 FROM attempts WHERE task = ?", (args.task,)).fetchone():
            raise ValueError("record worker attempts before finishing the task")
        entry = {"task": args.task, "outcome": args.outcome, "evidence": args.evidence,
                 "seconds": args.seconds, "time": time.time()}
        db.execute("INSERT INTO finishes VALUES (?, ?)", (args.task, json.dumps(entry)))
    return {"finished": args.task, "outcome": args.outcome}


def aggregate(attempts: list[dict]) -> dict:
    verified = [row for row in attempts if row["outcome"] != "unverified"]
    passed = sum(row["outcome"] == "pass" for row in verified)
    token_sums = {}
    # Preserve native fields by provider: cache accounting/tokenizers differ.
    for provider in sorted({row["provider"] for row in attempts}):
        subset = [row for row in attempts if row["provider"] == provider]
        token_sums[provider] = {}
        for field in TOKEN_FIELDS:
            values = [row["tokens"].get(field) for row in subset]
            known = [value for value in values if value is not None]
            if known:
                token_sums[provider][field] = {
                    "known_sum": sum(known), "reported_attempts": len(known),
                    "total_attempts": len(subset),
                }
    return {
        "attempts": len(attempts), "verified_attempts": len(verified),
        "passed_attempts": passed, "unverified_attempts": len(attempts) - len(verified),
        "execution_errors": sum(row["exit_code"] != 0 or row["status"] != "completed"
                                for row in attempts),
        "repair_attempts": sum(row["attempt"] > 1 for row in attempts),
        "failure_kinds": dict(Counter(row["failure_kind"] for row in attempts
                                      if row["failure_kind"] != "none")),
        "worker_seconds": round(sum(row["seconds"] for row in attempts), 3),
        "native_tokens_by_provider": token_sums,
    }


def summary(db: sqlite3.Connection, args: argparse.Namespace) -> dict:
    cutoff = time.time() - args.days * 86400
    groups = defaultdict(list)
    for row in rows(db, "attempts"):
        if row["time"] >= cutoff and (not args.category or row["category"] == args.category):
            key = tuple(row[field] for field in ("category", "role", "provider", "model", "effort"))
            groups[key].append(row)
    ordered = sorted(groups.items(), key=lambda pair: max(row["time"] for row in pair[1]), reverse=True)
    return {"days": args.days, "total_groups": len(groups), "groups": [
        dict(zip(("category", "role", "provider", "model", "effort"), key), **aggregate(group))
        for key, group in ordered[:args.limit]
    ], "note": "Observed attempts, not a model ranking. Unknown usage is not zero; tokens are not dollars."}


def compare(db: sqlite3.Connection, args: argparse.Namespace) -> dict:
    if args.policies[0] == args.policies[1]:
        raise ValueError("choose two different policies")
    by_task = defaultdict(list)
    for row in rows(db, "attempts"):
        by_task[row["task"]].append(row)
    finishes = {row["task"]: row for row in rows(db, "finishes")}
    cases = defaultdict(lambda: defaultdict(list))
    excluded = 0
    for task, attempts in by_task.items():
        first = attempts[0]
        if first["policy"] not in args.policies:
            continue
        if not first["case_hash"] or task not in finishes:
            excluded += 1
            continue
        cases[first["case_hash"]][first["policy"]].append(task)
    matched = {case: policies for case, policies in cases.items()
               if all(policy in policies for policy in args.policies)}
    excluded += sum(len(tasks) for policies in cases.values()
                    if not all(policy in policies for policy in args.policies)
                    for tasks in policies.values())
    results = []
    for case, policies in sorted(matched.items()):
        result = {"case_hash": case, "policies": {}}
        for policy in args.policies:
            task_ids = policies[policy]
            attempts = [row for task in task_ids for row in by_task[task]]
            seconds = [finishes[task]["seconds"] for task in task_ids]
            passed = sum(finishes[task]["outcome"] == "pass" for task in task_ids)
            result["policies"][policy] = {
                "trials": len(task_ids), "passed_trials": passed,
                "median_task_seconds": round(statistics.median(seconds), 3),
                **aggregate(attempts),
            }
        results.append(result)
    return {"matched_cases": len(results), "excluded_trials": excluded, "cases": results,
            "note": "Compare quality first; include failed trials and all repairs/reviews. "
                    "Worker seconds are summed effort, not wall time. No automatic winner."}


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--db", type=Path, default=Path.home() / ".local/state/developer-orchestrator/history.sqlite3")
    commands = cli.add_subparsers(dest="command", required=True)
    rec = commands.add_parser("record", help="record one CLI invocation after independent assessment")
    for name in ("task", "worker", "category", "policy", "model", "effort"):
        rec.add_argument("--" + name, required=True)
    rec.add_argument("--provider", choices=("claude", "codex"), required=True)
    rec.add_argument("--role", choices=("implement", "review", "investigate"), required=True)
    rec.add_argument("--attempt", type=positive, default=1)
    rec.add_argument("--seconds", type=nonnegative, required=True)
    rec.add_argument("--exit-code", type=int, required=True)
    rec.add_argument("--result", type=Path, required=True)
    rec.add_argument("--resumed", action="store_true", help="omit potentially cumulative usage")
    rec.add_argument("--case-file", type=Path, help="frozen evaluation specification; contents are hashed only")
    rec.add_argument("--outcome", choices=OUTCOMES, default="unverified")
    rec.add_argument("--evidence", default="")
    rec.add_argument("--failure-kind", default="none", help="e.g. reasoning, context, tools, requirements, validation")
    done = commands.add_parser("finish", help="record orchestrator's verified final task outcome")
    done.add_argument("--task", required=True)
    done.add_argument("--outcome", choices=("pass", "fail"), required=True)
    done.add_argument("--evidence", required=True)
    done.add_argument("--seconds", type=nonnegative, required=True, help="whole-task wall time, including orchestration/review")
    recent = commands.add_parser("summary", help="bounded recent evidence for routing")
    recent.add_argument("--category")
    recent.add_argument("--days", type=positive, default=30)
    recent.add_argument("--limit", type=positive, default=8)
    comparison = commands.add_parser("compare", help="compare policies on identical, completed evaluation cases")
    comparison.add_argument("--policies", nargs=2, required=True)
    return cli


def main() -> int:
    args = parser().parse_args()
    try:
        db = connect(args.db.expanduser())
        try:
            result = {"record": record, "finish": finish, "summary": summary, "compare": compare}[args.command](db, args)
        finally:
            db.close()
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, sqlite3.Error) as error:
        print(f"feedback: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
