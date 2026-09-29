---
name: developer-orchestrator
description: Balance Claude and Codex CLI workers for implementation and independent review; select model and effort by task fit. Use when orchestration is requested directly or through developer-profile.
---

# Developer Orchestrator

Orchestrator/final reviewer = selected chat model. Apply [developer-profile](../developer-profile/SKILL.md). Workers implement/fix; no recursive delegation.

- Route each implementer/reviewer: prefer smaller known-capable models and lower supported effort for bounded, routine work. Use stronger models upfront for concrete complexity/risk; never default to flagship or maximum effort. No pricing/quota/usage lookups, fixed model names, or provider stereotypes.
- Balance workload using this task's assignments and rough task size. When equally suitable, choose the less-loaded provider; prefer cross-provider review. Use both when qualified, without duplicate work or sacrificing task fit. Disclose fallback.
- Escalate model and/or effort only for the affected assignment when ambiguity, risk, or failed checks justify it; fix scope/context/tool problems first. Any supported effort, including future levels, remains eligible. Record task, provider/model/effort, brief reason; justify premium choices.
- Dispatch: preserve baseline changes. Assign one coherent, verifiable outcome per worker; separate difficult reasoning from routine edits when handoff saves work. Batch small related edits of similar complexity; avoid oversized mixed-complexity assignments and trivial fragmentation. Supply scope, owned files, acceptance checks, applicable instructions, relevant context only. Parallelize independent/disjoint work; serialize conflicts. Resume implementer with deltas for fixes. Return files/checks/risks.
- Review every implementer with a fresh independent read-only worker; inspect actual diff/source against requirements, regressions, profile, tests. Require actionable file/line findings. Size review to diff risk, not implementer tier; fix and re-review changes. After two failed repair cycles, reassess approach/model/provider; surface blockers.
- Final: orchestrator inspects combined diff, resolves findings, verifies integration checks. Delegate/re-review further edits. Report validation/limitations; verify worker claims.

Run chosen CLI from assignment workspace; prompt via file:

```sh
claude -p --model "$model" --effort "$effort" --output-format json < "$prompt" > "$result"
codex exec -m "$model" -c "model_reasoning_effort=\"$effort\"" --json - < "$prompt" > "$result"
```

Check CLI help and supported effort. Role-scoped permissions; no bypass. Check exit status, JSON/JSONL errors/denials; explicitly reroute unavailable models/providers. Logs outside source tree; summarize evidence.
