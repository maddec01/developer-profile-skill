# Local feedback

Use `python3 <skill-dir>/scripts/feedback.py`; set `skill` to that installed skill directory in the examples. Standard library; no services, API calls, model catalog, or price/quota polling. Default database: `~/.local/state/developer-orchestrator/history.sqlite3`; override with `--db PATH` before the subcommand. Keep logs outside repositories. Store concise check evidence without source, prompts, transcripts, secrets, or personal data.

## Routing

Once per task, request a bounded summary for a comparable category:

```sh
python3 "$skill/scripts/feedback.py" summary --category parser-bounded --days 30 --limit 8
```

Choose categories specific enough to distinguish task type, difficulty, and relevant project context. Summary groups by category, role, provider, model, and effort; shows verified/unverified attempts, errors, repair counts, worker time, failure causes, and available tokens. Favor smaller models/lower effort after repeated comparable successes; increase capability where reasoning failures recur. Context/tool/requirements failures call for better inputs or tooling. One success, sparse history, different workloads, and old model aliases do not establish superiority. Empty history requires no probing or extra benchmark calls.

## Record actual work

Keep each invocation's JSON/JSONL output and exit code; measure wall time around the process. Record each invocation once, including failed attempts, investigations, and reviewers. After its independent assessment, record `pass`/`fail` with check evidence; otherwise use `unverified`. CLI completion alone is never a quality verdict. Batch local recording commands when convenient; no extra model calls for bookkeeping.

```sh
python3 "$skill/scripts/feedback.py" record \
  --task "$task_id" --worker parser --attempt 1 \
  --category parser-bounded --policy adaptive-v1 \
  --provider codex --model "$model" --effort "$effort" --role implement \
  --seconds "$elapsed" --exit-code "$exit_code" --result "$result_file" \
  --outcome pass --evidence 'targeted tests passed; independent review accepted'
```

- `task`: unique whole-task trial ID. `worker`: logical assignment ID; increment `attempt` for repairs, even after switching provider/model. New reviewer/investigator assignments get their own IDs. `policy`: routing-policy version, constant within a task.
- Model/effort names are unrestricted strings. Prefer concrete model IDs when already known; never query a catalog just for logging.
- Use `--failure-kind reasoning|context|tools|requirements|validation` as appropriate (free-form label, default `none`). Values are evidence-based diagnoses, not automatic guesses.
- Add `--resumed` when continuing a session: omit potentially cumulative tokens rather than double-counting. Missing/malformed/future output formats retain unknown usage and an unrecognized execution status. A nonzero exit or known terminal error cannot be labeled `pass`.
- Only terminal usage fields are extracted. Claude JSON and Codex JSONL are parsed separately; native cache fields remain separate and totals include coverage counts. Tokens are resource proxies, not money, and are not comparable units across tokenizers. Raw output is never stored in the database. See [Claude output](https://code.claude.com/docs/en/headless) and [Codex JSONL](https://developers.openai.com/codex/noninteractive/).

After final integration checks and orchestrator review, close the task:

```sh
python3 "$skill/scripts/feedback.py" finish --task "$task_id" \
  --outcome pass --seconds "$whole_task_elapsed" \
  --evidence 'acceptance suite and final diff review passed'
```

Use `fail` for a completed unsuccessful trial. Finish is immutable; another trial needs another task ID. Record all workers before finishing. Whole-task elapsed time includes orchestration, handoffs, and review; summed worker time does not represent parallel wall time. Main-chat token usage is not captured; comparisons describe worker resources and measured overall latency, not total billed cost.

## Repeatable evaluation

Run evaluations only when requested; normal tasks accumulate feedback without duplicate execution.

1. Freeze representative case specifications outside the skill: exact repository/starting commit, request, fixtures/environment, acceptance tests, and independent review criteria. Include bounded edits, debugging, and interacting changes. Use non-sensitive fixtures.
2. Run each candidate policy from an equivalent clean checkout with a fresh task ID. Keep setup, tools, checks, and case file identical; vary only routing policy. Alternate policy order across repetitions. Do not reuse another trial's changes or conversation.
3. Pass the same `--case-file PATH` to **every** `record` in a trial. Only its SHA-256 is retained. Record all failed work, repairs, and reviews, then `finish` with the same acceptance criteria. CLI exit success is insufficient.
4. Compare completed trials with matching case hashes:

```sh
python3 "$skill/scripts/feedback.py" compare --policies baseline-v1 adaptive-v1
```

The offline comparison reports each matched case separately: trials/passes, median whole-task duration, all worker resources, repairs, and token coverage. Missing-case, unfinished, and unmatched trials are explicitly excluded. Inspect exclusions and unequal trial counts before concluding anything. Compare quality first, then time/resource tradeoffs; there is no fabricated combined score or automatic winner. Hash matching checks the specification, not that the agent actually reproduced the environment. Keep a policy change only when repeated results support it.
