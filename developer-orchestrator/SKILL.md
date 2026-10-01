---
name: developer-orchestrator
description: Select Claude and Codex worker models per task, with token-efficient cavecrew contracts, compact handoffs, small implementation chunks, and independent review. Use when orchestration is requested directly or through developer-profile.
---

# Developer Orchestrator

The selected chat model is lead and final integrator only. Select each worker's provider, model, and effort independently by its assignment; never inherit them merely because the chat started in Claude or Codex. Respect explicit user overrides. Apply [developer-profile](../developer-profile/SKILL.md), then load the available `cavecrew` and `caveman` skills. Use caveman `ultra` for orchestration prompts, worker results, progress, and final reporting unless its Auto-Clarity rules apply. Workers never delegate or redesign orchestration.

Optimize for verified completion with minimum total tokens, then elapsed time. Do work inline when delegation plus handoff costs more than the task. No persistent tracking, benchmarks, duplicated investigation, or repeated summaries.

## Model routing

Before dispatch, inspect available native worker options and check both installed CLIs once (`command -v claude`, `command -v codex`). Resolve supported model IDs or aliases from tool metadata or local model configuration/cache. A CLI's presence does not prove model access; handle actual dispatch failures. Never query live price, quota, or usage.

Choose the smallest known-capable model for the packet. `Fast`, `balanced`, and `strong` are capability classes to resolve to concrete supported models, not executable model names. Preserve the initiating chat's quality bar; choose worker effort by task difficulty and the selected model's supported settings rather than copying the chat's effort value.

| Assignment | Model class | Effort |
| --- | --- | --- |
| Bounded lookup, tracing known symbols | Fast | Low |
| Decided surgical edit, mechanical test execution | Fast coding-capable; balanced if judgment remains | Low for mechanical work; medium otherwise |
| Cross-file implementation, test design, unfamiliar causal analysis | Balanced | Medium; higher for ambiguity or risk |
| Difficult architecture, security, migrations, repeated reasoning failures | Strong when needed | High or higher when justified |
| Independent review | Balanced; strong for broad or high-risk changes | Sized to change risk; retain acceptance rigor |

Compare qualified candidates across both providers. When equally suitable, choose the less-assigned provider by rough work size in this task. Use the other provider for independent review when qualified and available. Do not manufacture extra work or sacrifice task fit to force a mix. Fix weak scope or context before escalating; escalate only the affected packet.

Select role, provider, concrete model, and supported effort **before** choosing a native preset or CLI. Set model and effort explicitly where supported. Preset pins and `inherit` defaults must not override this selection. If native dispatch cannot express the chosen route, use that provider's CLI with the same packet and contract. A same-provider native tool is not evidence the other provider is unavailable. Fall back only for a concrete model, authentication, permission, or executable limitation; disclose the reason and preserve the quality bar. Omit effort overrides for models without effort control.

## Role contracts

Prefer cavecrew scope and output contracts whenever they fit, on either provider:

- `cavecrew-investigator`: locate definitions, callers, tests, conventions, or failure evidence.
- `cavecrew-builder`: surgical edit in one or two known files after decisions are fixed.
- `cavecrew-reviewer`: findings-only review of a diff, branch, or file.

Use an ordinary specialist for architecture decisions or unfamiliar causal analysis, an ordinary builder for cross-cutting or three-plus-file changes, and an ordinary reviewer when rationale or alternatives matter. Require caveman `ultra` output from each. If named cavecrew presets are unavailable or pin a different model, give the selected worker the same scope and output contract.

Use only needed roles. No scout when lead already knows sites. No builder when lead can make a trivial edit cheaper. No duplicate assignments. Parallelize only independent work whose saved time exceeds added prompt and merge cost.

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
3. Apply model routing to each packet, then dispatch disjoint packets together. Serialize overlapping files or dependent behavior. Resume same worker for repairs with deltas only; reroute if capability or access changes.
4. Run targeted checks once per stable chunk. Reuse valid evidence; rerun only for changed code, failures, gaps, or integration risk.
5. Independently review every change. Prefer `cavecrew-reviewer`; batch related stable diffs. Use a stronger ordinary reviewer only for cross-cutting behavior, security, migrations, or architectural risk.
6. Consolidate findings into one repair pass. Re-review only material behavior changes or unresolved risk. After two failed repairs, reassess packet, model, or provider.
7. Lead inspects combined diff and integration, then reports only outcome, validation, and limitations.

Batch dispatch disclosure into one line per worker: `<role> | <provider/model> | <effort or unsupported> | <task-fit reason>`. Do not narrate tool calls or repeat worker results.

Run the selected external worker from assignment workspace with prompt and result files (include effort only when supported):

```sh
claude -p --model "$model" --effort "$effort" --output-format json < "$prompt" > "$result"
codex exec -m "$model" -c "model_reasoning_effort=\"$effort\"" --json - < "$prompt" > "$result"
```

Use known supported options; consult help only after uncertainty or error. Grant role-scoped permissions without bypasses. Check exit status plus JSON/JSONL errors or denials. Keep logs outside source tree and retain only decisive evidence.
