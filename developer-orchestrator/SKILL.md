---
name: developer-orchestrator
description: Balance Claude and Codex CLI workers for implementation and independent review; select model and effort by task fit. Use when orchestration is requested directly or through developer-profile.
---

# Developer Orchestrator

Orchestrator/final reviewer = selected chat model. Apply [developer-profile](../developer-profile/SKILL.md). Workers implement/fix; no recursive delegation.

Optimize elapsed time to verified completion, including startup, handoffs, reviews, and retries. Self-contained; no persistent tracking, benchmarks, or user reporting.

- Route each implementer/reviewer: prefer fast, smaller capable models and lower effort for routine work. Start stronger for concrete complexity/risk that would otherwise cause retries. No default flagship/maximum effort, fixed model names, provider stereotypes, or live pricing/quota/usage queries.
- Balance workload using this task's assignments and rough task size. When equally suitable, choose the less-loaded provider; prefer cross-provider review. Use both when qualified, without duplicate work or sacrificing task fit. Disclose fallback.
- Escalate model and/or effort only for the affected assignment when ambiguity, risk, or failed checks justify it; fix scope/context/tool problems first. Any supported effort, including future levels, remains eligible. Briefly state provider/model/effort and selection reason.
- Dispatch independent/disjoint assignments in parallel after minimal scoping; keep coupled work together. A single-track task needs one implementer, not a separate planning worker. Pass baseline, scope, owned files, acceptance checks, instructions, and relevant context. Resume workers for fixes; return concise files/checks/risks.
- Give every change independent read-only review, batching related changes in one pass. Start reviewing stable completed changes while other workers run. Supply exact diff, source, and check evidence. Send consolidated actionable findings to the relevant implementers in parallel for one focused repair pass. Re-review only material behavior changes, failed checks, or unresolved integration risks; avoid routine back-and-forth. Reassess approach/model/provider if repairs fail twice.
- Final: orchestrator inspects combined diff and repaired areas, resolves findings, and checks integration. Reuse test evidence; rerun only for changed code, gaps, failures, or integration risk. Report validation/limitations without repeating worker investigation.

Run chosen CLI from assignment workspace; prompt via file:

```sh
claude -p --model "$model" --effort "$effort" --output-format json < "$prompt" > "$result"
codex exec -m "$model" -c "model_reasoning_effort=\"$effort\"" --json - < "$prompt" > "$result"
```

Use known supported CLI options/effort; consult help only for uncertainty or errors. Role-scoped permissions; no bypass. Check exit status and JSON/JSONL errors/denials; disclose fallback. Logs outside source tree; summarize evidence.
