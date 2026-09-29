"""Offline fixtures only: no worker CLI, network, or real history access."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/feedback.py"
SPEC = importlib.util.spec_from_file_location("feedback", SCRIPT)
feedback = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(feedback)


class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.db = self.root / "history.sqlite3"
        self.result = self.root / "result.jsonl"
        self.result.write_text(json.dumps({
            "type": "turn.completed", "usage": {
                "input_tokens": 100, "cached_input_tokens": 60, "output_tokens": 20,
            },
        }))
        self.case = self.root / "case.md"
        self.case.write_text("repo@commit; bounded task; test fixture and acceptance checks v1")

    def cli(self, *args, success=True):
        result = subprocess.run([sys.executable, str(SCRIPT), "--db", str(self.db), *args],
                                text=True, capture_output=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        return result.stderr

    def record(self, task="trial", policy="adaptive", extra=(), success=True):
        return self.cli("record", "--task", task, "--worker", "edit", "--category", "bounded",
                        "--policy", policy, "--provider", "codex", "--model", "future-model",
                        "--effort", "future-effort", "--role", "implement", "--seconds", "10",
                        "--exit-code", "0", "--result", str(self.result), *extra, success=success)

    def finish(self, task="trial", outcome="pass", seconds="15", success=True):
        return self.cli("finish", "--task", task, "--outcome", outcome, "--seconds", seconds,
                        "--evidence", "acceptance tests + final review", success=success)

    def test_codex_terminal_only_and_multiple_turns(self):
        self.result.write_text('\n'.join(json.dumps(row) for row in [
            {"type": "item.completed", "usage": {"input_tokens": 999}},
            {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 2}},
            {"type": "turn.completed", "usage": {"input_tokens": 20, "output_tokens": 3}},
        ]))
        metrics = feedback.read_metrics(self.result, "codex", False)
        self.assertEqual(metrics, {"status": "completed", "tokens": {"input_tokens": 30, "output_tokens": 5}})

    def test_claude_native_cache_fields_not_double_counted(self):
        self.result.write_text(json.dumps({"type": "result", "is_error": False, "usage": {
            "input_tokens": 10, "output_tokens": 4,
            "cache_read_input_tokens": 30, "cache_creation_input_tokens": 20,
        }}))
        metrics = feedback.read_metrics(self.result, "claude", False)
        self.assertEqual(metrics["tokens"]["input_tokens"], 10)
        self.assertEqual(metrics["tokens"]["cache_read_input_tokens"], 30)
        self.assertEqual(feedback.read_metrics(self.result, "claude", True)["tokens"], {})

    def test_claude_denial_and_codex_error_are_not_passes(self):
        self.result.write_text(json.dumps({"type": "result", "permission_denials": [{"tool_name": "Edit"}]}))
        self.assertEqual(feedback.read_metrics(self.result, "claude", False)["status"], "error")
        self.result.write_text('{"type":"error","message":"failed"}\n{"type":"turn.completed"}')
        self.record(extra=("--outcome", "pass", "--evidence", "claimed success"), success=False)

    def test_unknown_or_partial_usage_stays_unknown(self):
        for text in ('not json', 'null', '[]', '{"type":"new.terminal"}'):
            self.result.write_text(text)
            self.assertEqual(feedback.read_metrics(self.result, "codex", False),
                             {"status": "unrecognized", "tokens": {}})
        self.result.write_text('{"type":"turn.completed","usage":{"input_tokens":10}}\n'
                               '{"type":"turn.completed","usage":{"output_tokens":2}}')
        self.assertEqual(feedback.read_metrics(self.result, "codex", False)["tokens"], {})

    def test_verification_is_explicit_and_unknown_usage_has_coverage(self):
        self.record()
        self.record(task="other", extra=("--resumed", "--outcome", "pass", "--evidence", "tests + review"))
        result = self.cli("summary")["groups"][0]
        self.assertEqual(result["unverified_attempts"], 1)
        self.assertEqual(result["verified_attempts"], 1)
        self.assertEqual(result["native_tokens_by_provider"]["codex"]["input_tokens"],
                         {"known_sum": 100, "reported_attempts": 1, "total_attempts": 2})

    def test_rejects_false_success_and_bad_time(self):
        self.record(extra=("--outcome", "pass"), success=False)
        self.record(extra=("--outcome", "pass", "--evidence", "tests", "--exit-code", "1"), success=False)
        for seconds in ("nan", "inf", "-1"):
            self.record(extra=("--seconds", seconds), success=False)

    def test_attempt_identity_and_task_metadata_are_consistent(self):
        self.record(extra=("--attempt", "2"), success=False)
        self.record(extra=("--case-file", str(self.case)))
        self.record(extra=("--case-file", str(self.case)), success=False)
        self.record(extra=("--attempt", "2"), success=False)
        self.record(policy="changed", extra=("--attempt", "2", "--case-file", str(self.case)), success=False)
        self.record(extra=("--attempt", "2", "--case-file", str(self.case)))
        self.assertEqual(self.cli("summary")["groups"][0]["repair_attempts"], 1)

    def test_finish_is_immutable_and_closes_recording(self):
        self.finish(success=False)
        self.record()
        self.finish()
        self.finish(success=False)
        self.record(extra=("--attempt", "2"), success=False)

    def test_compare_includes_repairs_reviews_and_failed_trials(self):
        case = ("--case-file", str(self.case))
        self.record(task="old", policy="baseline", extra=case + ("--outcome", "fail", "--evidence", "test failure", "--failure-kind", "reasoning"))
        self.record(task="old", policy="baseline", extra=case + ("--attempt", "2",))
        self.record(task="old", policy="baseline", extra=case + ("--worker", "review", "--role", "review"))
        self.finish("old", "fail", "40")
        self.record(task="new", extra=case)
        self.finish("new", "pass", "12")
        self.record(task="pending", policy="baseline", extra=case)
        self.record(task="no-case")
        self.finish("no-case")
        comparison = self.cli("compare", "--policies", "baseline", "adaptive")
        self.assertEqual(comparison["matched_cases"], 1)
        self.assertEqual(comparison["excluded_trials"], 2)
        old = comparison["cases"][0]["policies"]["baseline"]
        self.assertEqual((old["attempts"], old["repair_attempts"], old["passed_trials"]), (3, 1, 0))
        self.assertEqual((old["worker_seconds"], old["median_task_seconds"]), (30, 40))
        self.assertEqual(old["failure_kinds"], {"reasoning": 1})

    def test_case_changes_prevent_invalid_comparisons(self):
        self.record(task="old", policy="baseline", extra=("--case-file", str(self.case)))
        self.finish("old")
        self.case.write_text("different baseline or acceptance checks")
        self.record(task="new", extra=("--case-file", str(self.case)))
        self.finish("new")
        result = self.cli("compare", "--policies", "baseline", "adaptive")
        self.assertEqual((result["matched_cases"], result["excluded_trials"]), (0, 2))

    def test_empty_history_and_category_filter(self):
        self.assertEqual(self.cli("summary")["groups"], [])
        self.record()
        self.assertEqual(self.cli("summary", "--category", "unrelated")["groups"], [])
        self.cli("compare", "--policies", "adaptive", "adaptive", success=False)

    def test_database_does_not_store_worker_transcript(self):
        self.result.write_text('{"type":"item.completed","item":{"text":"SECRET_TRANSCRIPT"}}\n'
                               '{"type":"turn.completed","usage":{"input_tokens":3}}')
        self.record()
        self.assertNotIn(b"SECRET_TRANSCRIPT", self.db.read_bytes())

    def test_parallel_recording_preserves_all_workers(self):
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(self.record, extra=("--worker", f"worker-{number}"))
                       for number in range(8)]
            for future in futures:
                future.result()
        self.assertEqual(self.cli("summary")["groups"][0]["attempts"], 8)


if __name__ == "__main__":
    unittest.main()
