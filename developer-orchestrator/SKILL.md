---
name: developer-orchestrator
description: Coordinate Claude CLI implementation workers and independent reviewers using the selected chat model. Use when requested directly or through developer-profile.
---

# Developer Orchestrator

Keep the currently selected chat model as orchestrator and final reviewer. Load [developer-profile](../developer-profile/SKILL.md) if not already loaded. Delegate implementation and fixes to Claude CLI workers; workers must not recursively orchestrate.

1. Inspect the task and working tree. Define bounded assignments, acceptance criteria, relevant files, and required checks. Record existing changes so reviews distinguish worker edits. Parallelize only independent assignments with disjoint file ownership; serialize overlapping work.
2. Choose each worker's model and effort explicitly, including reviewers. Prefer Sonnet with low/medium effort for clear, bounded work; Opus with high effort for ambiguous, cross-cutting, or difficult work. Scale review effort to risk, independently of implementation effort. Use available model aliases and supported effort levels; increase capability when evidence warrants it. Briefly state choices.
3. Launch a fresh Claude CLI session per assignment from its workspace. Supply the task, ownership, acceptance criteria, applicable repository instructions, developer-profile, and relevant context—not the full chat. Require a concise report: changed files, checks/results, unresolved risks.
4. After each implementation worker finishes, launch a separate, fresh Claude CLI reviewer. Give it the assignment, exact diff, relevant source, and test evidence. Keep it read-only; require independent inspection for correctness, regressions, scope, and profile compliance, with actionable file/line findings. Never count self-review as this review.
5. Send valid findings to the implementation worker for fixes, then have the reviewer check the revised result. If repeated attempts stall, reassess scope/model/effort; report a blocker when progress requires user input.
6. The main orchestrator inspects the complete final diff, resolves review disagreements, and verifies acceptance criteria and appropriate integration checks. Delegate any further edits and re-review them. Report the result, validation, and remaining limitations; worker approval alone is insufficient.

CLI pattern (write each prompt to a file):

```sh
claude -p --model "$worker_model" --effort "$worker_effort" --output-format json < "$prompt_file" > "$result_file"
```

Check `claude --help` for installed capabilities. Use task-scoped permissions; never bypass permission checks. Inspect exit status and JSON errors/permission denials before accepting completion. If CLI/auth/model access is unavailable, report the blocker rather than silently changing execution strategy.
