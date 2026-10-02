---
name: developer-orchestrator
description: Route Claude and Codex workers by task with compact cavecrew contracts, small implementation chunks, and independent review. Use for explicit orchestration or through developer-profile.
---

# Developer Orchestrator

Chat model is lead/final integrator; select workers independently by assignment, respecting user overrides. Workers never delegate or redesign orchestration. Apply [developer-profile](../developer-profile/SKILL.md), then available `cavecrew` and `caveman` skills. Use caveman `ultra` for prompts, results, progress, and final reports, subject to Auto-Clarity.

Invoking this skill authorizes Claude and Codex workers and sending necessary task/repository context to either provider. Proceed without additional user confirmation for provider selection, context sharing, or worker launches. Use configured host approval mechanisms for required escalation; enforced permissions and denials remain binding.

Minimize total tokens for verified completion, then elapsed time. Work inline when delegation/handoff costs more, including trivial edits. Avoid persistent tracking, benchmarks, duplicate assignments/investigation, and repeated summaries. Skip scouts for known sites. Parallelize only independent work whose time savings exceed prompt/merge costs.

## Model routing

Inspect native options and check both CLIs once: `command -v claude`, `command -v codex`. Resolve supported model IDs/aliases from tool metadata or local configuration/cache; installed does not mean accessible. Never query live price, quota, or usage.

Choose the smallest known-capable model meeting the chat's quality bar. Fast/balanced/strong are capability classes, not model IDs. Size effort to assignment difficulty and model support; never inherit the chat's provider, model, or effort by default.

| Assignment | Model class | Effort |
| --- | --- | --- |
| Bounded lookup, known-symbol tracing | Fast | Low |
| Decided edit, mechanical tests | Fast coding-capable; balanced for judgment | Low mechanical; medium otherwise |
| Cross-file implementation, test design, unfamiliar causal analysis | Balanced | Medium; higher for ambiguity/risk |
| Difficult architecture, security, migrations, repeated reasoning failures | Strong as needed | High+ when justified |
| Independent review | Balanced; strong for broad/high-risk changes | Match risk; preserve acceptance rigor |

Compare qualified models across both providers. Break ties by less-assigned provider, counting rough work size; prefer the other provider for qualified, available independent review. Never force a mix at task-fit/work-cost expense. Repair weak scope/context before escalating only the affected packet.

Select role/provider/model/effort **before** native preset or CLI; set supported overrides explicitly, overriding preset pins/`inherit`. If native dispatch cannot express the route, use that provider's CLI with the same packet/contract. Same-provider native availability says nothing about the other provider. Fall back only for concrete model, authentication, permission, or executable limitations; disclose why and preserve quality. Omit unsupported effort controls.

## Roles and packets

Prefer these cavecrew scopes/contracts on either provider; reproduce them if presets are missing or pin another model:

- `cavecrew-investigator`: definitions, callers, tests, conventions, failure evidence.
- `cavecrew-builder`: decided surgical edits in 1–2 known files.
- `cavecrew-reviewer`: findings-only diff/branch/file review.

Use ordinary specialists for architecture/unfamiliar causes, builders for cross-cutting or 3+ files, reviewers for rationale/alternatives. All return caveman `ultra`.

Resolve design first. Send only context workers cannot cheaply read; prefer paths/symbols/line ranges. Do not repeat skill bodies, full diffs, history, or unchanged requirements. Omit empty packet fields:

```text
outcome: <observable result>
not: <non-goals>
own: <files/area; no overlapping writers>
decisions: <fixed behavior/interfaces>
read: <relevant paths/symbols/evidence>
checks: <exact acceptance commands/behavior>
return: <compact contract>
```

Implementer/test output at most:

```text
changed: <path:line — fact>
checks: <command — pass|fail>
risk: <none|fact>
```

Specialists: `decision`, `evidence` (`path:line`), `risk`. Cavecrew: native contracts. No preamble, narration, restated assignment, or long logs; exact errors only when decisive.

## Execution

1. Inspect minimal full feature flow; reuse code, fix decisions, split ownership. Scout only unresolved bounded locations; turn findings directly into packets.
2. Route each packet; dispatch disjoint work together, serialize overlap/dependencies. Repair with deltas to the same worker; reroute for changed capability/access.
3. Check each stable chunk once. Reuse evidence; rerun for changed code, failures, gaps, or integration risk.
4. Independently review every change; batch related stable diffs, prefer `cavecrew-reviewer`. Stronger ordinary review only for cross-cutting behavior, security, migrations, or architecture risk. Consolidate repairs; re-review material behavior changes/unresolved risk. After two failed repairs, reassess packet/model/provider.
5. Inspect combined diff/integration; report outcome, validation, limitations. Batch dispatch disclosure: `<role> | <provider/model> | <effort or unsupported> | <task-fit reason>`. Do not repeat worker results or narrate calls.

## CLI execution

Check `claude auth status --json` with the resolved executable in the worker's context. Preserve `HOME`/`CLAUDE_CONFIG_DIR`; never relocate/export credentials.

macOS sandboxing can hide Claude's Keychain login. Sandboxed `loggedIn: false` or missing-authentication errors require one status retry through normal host escalation (`exec_command`, `sandbox_permissions: "require_escalated"`). If successful, launch the worker through that same approved path. If still logged out, report/fall back; if escalation is unavailable/denied, report the restriction, not a need to log in, and use a qualified provider within existing permissions. Never retry/bypass denials or disable sandboxing globally. Keep worker permissions role-scoped; host escalation grants no broader actions.

Launch from assignment workspace with prompt/result files (effort only when supported):

```sh
claude -p --model "$model" --effort "$effort" --output-format json < "$prompt" > "$result"
codex exec -m "$model" -c "model_reasoning_effort=\"$effort\"" --json - < "$prompt" > "$result"
```

Use supported options; consult help for uncertainty/errors. Authentication status proves credential visibility only: check worker exit status and JSON/JSONL for model, network, filesystem, permission errors/denials. Never bypass worker permissions. Keep logs outside source; retain decisive evidence only.
