---
name: developer-orchestrator
description: Orchestrate token-efficient Claude and Codex workers with cavecrew delegation, caveman-compressed handoffs, small implementation chunks, and independent review. Use when orchestration is requested directly or through developer-profile.
---

# Developer Orchestrator

The selected chat model is lead and final integrator. Apply [developer-profile](../developer-profile/SKILL.md), then load the available `cavecrew` and `caveman` skills. Use caveman `ultra` for orchestration prompts, worker results, progress, and final reporting unless its Auto-Clarity rules apply. Workers never delegate or redesign orchestration.

Optimize for verified completion with minimum total tokens, then elapsed time. Do work inline when delegation plus handoff costs more than the task. No persistent tracking, benchmarks, duplicated investigation, or repeated summaries.

## Routing

Prefer cavecrew whenever its bounded contract fits:

- `cavecrew-investigator`: locate definitions, callers, tests, conventions, or failure evidence.
- `cavecrew-builder`: surgical edit in one or two known files after decisions are fixed.
- `cavecrew-reviewer`: findings-only review of a diff, branch, or file.

Use an ordinary specialist for architecture decisions or unfamiliar causal analysis, an ordinary builder for cross-cutting or three-plus-file changes, and an ordinary reviewer when rationale or alternatives matter. Require caveman `ultra` output from each. If named cavecrew presets are unavailable, give an ordinary worker the same scope and output contract.

Use only needed roles. No scout when lead already knows sites. No builder when lead can make a trivial edit cheaper. No duplicate assignments. Parallelize only independent work whose saved time exceeds added prompt and merge cost.

Use smallest known-capable model and lowest safe effort. Start reasoning-heavy work at initiating chat effort; lower only for decided mechanical work, raise only for ambiguity or risk. Fix weak scope or context before escalating. Prefer cross-provider review when equally suitable; never query live price, quota, or usage.

## Work packets

Resolve design before implementation. Send only context worker cannot cheaply read from workspace. Prefer paths, symbols, and line ranges over pasted source. Never repeat skill bodies, full diffs, prior discussion, or unchanged requirements.

Use this minimal packet, omitting empty fields:

```text
outcome: <one observable result>
not: <explicit non-goals>
own: <files or narrow area; no overlapping writer>
decisions: <fixed behavior/interface choices>
read: <only relevant paths, symbols, evidence>
checks: <exact acceptance commands/behavior>
return: <required compact contract>
```

Ordinary implementers and test workers return at most:

```text
changed: <path:line — fact>
checks: <command — pass|fail>
risk: <none|fact>
```

Specialists return `decision`, `evidence` with `path:line`, and `risk`. Cavecrew workers use their native contracts. No preamble, process narration, assignment restatement, or long logs. Exact errors only when decisive.

## Execution

1. Lead inspects minimum full feature flow needed to fix decisions, reuse existing code, and split ownership.
2. Use `cavecrew-investigator` only for unresolved bounded locations. Convert findings directly into decided packets; do not resummarize them.
3. Dispatch disjoint packets together. Serialize overlapping files or dependent behavior. Resume same worker for repairs with deltas only.
4. Run targeted checks once per stable chunk. Reuse valid evidence; rerun only for changed code, failures, gaps, or integration risk.
5. Independently review every change. Prefer `cavecrew-reviewer`; batch related stable diffs. Use a stronger ordinary reviewer only for cross-cutting behavior, security, migrations, or architectural risk.
6. Consolidate findings into one repair pass. Re-review only material behavior changes or unresolved risk. After two failed repairs, reassess packet, model, or provider.
7. Lead inspects combined diff and integration, then reports only outcome, validation, and limitations.

If user-visible dispatch disclosure is required, batch it into one line per worker: `<role> | <provider/model> | <effort> | <reason>`. Do not narrate tool calls or repeat worker results.

Run external workers from assignment workspace with prompt and result files:

```sh
claude -p --model "$model" --effort "$effort" --output-format json < "$prompt" > "$result"
codex exec -m "$model" -c "model_reasoning_effort=\"$effort\"" --json - < "$prompt" > "$result"
```

Use known supported options; consult help only after uncertainty or error. Grant role-scoped permissions without bypasses. Check exit status plus JSON/JSONL errors or denials. Keep logs outside source tree and retain only decisive evidence.
