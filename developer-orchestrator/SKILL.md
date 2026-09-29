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
- Dispatch promptly after minimal scoping. For bounded work, one implementer owns discovery, edits, and targeted checks; no separate planning/discovery worker. Split only when specialization or parallelism saves more time than startup/context/handoffs. Keep coupled work together; parallelize independent/disjoint assignments. Pass baseline, scope, owned files, acceptance checks, instructions, and relevant context. Resume workers for fixes; return concise files/checks/risks.
- Review all changes with independent read-only workers, grouping related changes. Review stable completed changesets while unrelated work continues; re-review later modifications. Supply exact diff, relevant source, and check evidence to avoid rediscovery. Report actionable findings; size effort to risk. Reuse reviewer context for follow-ups. After two failed repairs, reassess approach/model/provider.
- Final: orchestrator inspects combined diff for acceptance and integration risks; resolves findings. Verify existing check evidence; rerun only for changed code, gaps, failures, or integration risk. Delegate/re-review further edits. Report validation/limitations. Avoid duplicating worker investigation or review.

Run chosen CLI from assignment workspace; prompt via file:

```sh
claude -p --model "$model" --effort "$effort" --output-format json < "$prompt" > "$result"
codex exec -m "$model" -c "model_reasoning_effort=\"$effort\"" --json - < "$prompt" > "$result"
```

Use known supported CLI options/effort; consult help only for uncertainty or errors. Role-scoped permissions; no bypass. Check exit status and JSON/JSONL errors/denials; disclose fallback. Logs outside source tree; summarize evidence.
