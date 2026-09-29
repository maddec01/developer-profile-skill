---
name: developer-orchestrator
description: Route implementation and independent review across Claude and Codex CLI workers by task fit, cost, and reliability. Use when orchestration is requested directly or through developer-profile.
---

# Developer Orchestrator

Orchestrator/final reviewer = selected chat model. Apply [developer-profile](../developer-profile/SKILL.md). Workers implement/fix; no recursive delegation.

- Route each implementer/reviewer: compare available Claude/Codex model+effort by task/risk, tools/context, observed quality, latency, price/quota. Minimize total cost including retries/reviews subject to correctness. Verify availability once; do not invent prices/capabilities or assign provider stereotypes.
- Use both providers when suitable; prefer cross-provider review at comparable fit/cost. Tie-break by quota/headroom and lower usage; no 50/50 quota or duplicate execution. Disclose fallback.
- Effort: low=mechanical, medium=routine reasoning, high=ambiguity/risk; maximum only when justified. Choose sufficient capability first. Record task, provider/model/effort, brief reason.
- Dispatch: preserve baseline changes; batch related edits; minimize workers. Supply scope, owned files, acceptance checks, applicable instructions, relevant context only. Parallelize independent/disjoint work; serialize conflicts. Resume implementer with deltas for fixes. Return files/checks/risks.
- Review every implementer with a fresh independent read-only worker; inspect actual diff/source against requirements, regressions, profile, tests. Require actionable file/line findings. Match review capability to risk; fix and re-review changes. After two failed repair cycles, reassess approach/model/provider; surface blockers.
- Final: orchestrator inspects combined diff, resolves findings, verifies integration checks. Delegate/re-review further edits. Report validation/limitations; verify worker claims.

Run chosen CLI from assignment workspace; prompt via file:

```sh
claude -p --model "$model" --effort "$effort" --output-format json < "$prompt" > "$result"
codex exec -m "$model" -c "model_reasoning_effort=\"$effort\"" --json - < "$prompt" > "$result"
```

Check CLI help and supported effort. Role-scoped permissions; no bypass. Check exit status, JSON/JSONL errors/denials; explicitly reroute unavailable models/providers. Logs outside source tree; summarize evidence.
