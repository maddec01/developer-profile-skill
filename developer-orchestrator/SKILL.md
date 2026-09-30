---
name: developer-orchestrator
description: Orchestrate specialist Claude and Codex CLI workers through lead-planned, small implementation chunks and independent review. Use when orchestration is requested directly or through developer-profile.
---

# Developer Orchestrator

The selected chat model is the engineering lead and final integrator. Apply [developer-profile](../developer-profile/SKILL.md). Workers never delegate or redesign the orchestration.

Optimize elapsed time to verified completion, including startup, handoffs, reviews, and retries. Keep orchestration self-contained; do not create persistent tracking or benchmarks.

## Baseline and authority

- Treat the initiating chat's effort as the user's baseline signal for task difficulty and expected quality. Preserve that quality bar throughout planning, review, and final verification.
- The lead owns decomposition, architecture, acceptance criteria, worker preset, provider, concrete model, and effort. Workers do not choose their own effort or expand their role.
- Start reasoning-heavy workers at the baseline effort. Raise model capability or effort when ambiguity, risk, or failed checks justify it. Lower effort only for a tightly specified mechanical assignment whose decisions have already been made; this must not lower review rigor or acceptance criteria.
- Fix unclear scope, missing context, or weak work packets before escalating a model. Escalate only the affected assignment and disclose any provider fallback.

## Worker presets

Resolve model classes to currently available Claude or Codex models when dispatching. `Fast` means the smallest fast model known to handle the exact assignment, `balanced` means the general coding/reasoning model, and `strong` means the most capable model warranted by the risk. Prefer cross-provider review and balance equally suitable work across providers; do not query live pricing, quota, or usage.

| Preset | Responsibility | Default model class | Effort rule |
| --- | --- | --- | --- |
| Scout | Read-only tracing of files, dependencies, conventions, or failure evidence | Fast; balanced for unfamiliar or cross-cutting code | Below baseline is allowed for bounded lookup; baseline for causal analysis |
| Domain specialist | Make a difficult decision in one domain: frontend/UX, backend/API, data/migrations, infrastructure/tooling, security/performance, or test strategy | Balanced; strong for architectural or irreversible risk | Baseline or higher |
| Builder | Implement one already-decided work packet without broad discovery or redesign | Fast, coding-capable | Lead-selected low effort when mechanical; otherwise baseline |
| Test engineer | Add focused tests or execute a defined validation plan | Fast for execution; balanced for test design or failure diagnosis | Lead-selected; baseline for non-obvious coverage decisions |
| Reviewer | Independently inspect the exact diff, relevant source, and check evidence; return only actionable findings | Balanced; strong for broad or high-risk changes | Baseline or higher, sized to change risk |

Use only the roles the task needs. The lead handles ordinary scoping; add a scout or domain specialist only when their focused expertise removes uncertainty before implementation. A worker may wear one domain label and one preset, such as `backend builder` or `migration reviewer`.

## Work packets

The lead first resolves design choices, then turns the plan into the smallest coherent implementation chunks that can be executed with little judgment. Each packet must contain:

- one observable outcome and explicit non-goals;
- owned files or a narrow allowed area, with no concurrent overlapping writer;
- exact behavior or interface decisions already made;
- relevant project instructions, existing patterns to reuse, and baseline changes to preserve;
- acceptance checks and the concise result format: files changed, checks run, and blockers or risks.

A builder must not invent architecture, broaden scope, or silently resolve ambiguity. If the packet requires a new design decision, it returns the blocker to the lead or specialist. Keep inherently coupled edits together, but split work that contains independent outcomes, unrelated domains, or multiple unresolved decisions. Avoid fragments so small that startup and handoff cost more than the edit.

## Execution and review

1. Inspect enough of the full feature flow to identify decisions, dependencies, reusable code, and independent work.
2. Use scouts or domain specialists for unresolved questions. The lead converts their conclusions into explicit builder packets.
3. Dispatch independent packets in parallel and serialize overlapping files or dependent behavior. Resume the same builder with precise deltas for fixes.
4. Run targeted checks per chunk. A test engineer can own mechanical test additions or validation, while the lead retains coverage decisions that affect the quality bar.
5. Give every change independent read-only review, batching related chunks when this improves integration coverage. Supply the exact diff, relevant source, requirements, and check evidence. Send consolidated findings back for one focused repair pass; re-review material behavior changes, failed checks, or unresolved integration risks. Reassess the packet, model, or provider after two failed repairs.
6. The lead inspects the combined diff and repaired areas, checks cross-chunk integration, and confirms the original acceptance criteria at the initiating effort's quality bar. Reuse valid check evidence; rerun checks only for changes, gaps, failures, or integration risk.

Briefly state each dispatched worker's preset, domain, provider/model, effort, and selection reason. Final reporting covers validation and limitations without repeating worker investigation.

Run the chosen CLI from the assignment workspace and pass the prompt through a file:

```sh
claude -p --model "$model" --effort "$effort" --output-format json < "$prompt" > "$result"
codex exec -m "$model" -c "model_reasoning_effort=\"$effort\"" --json - < "$prompt" > "$result"
```

Use known supported CLI options and effort levels; consult help only for uncertainty or errors. Grant role-scoped permissions without bypasses. Check exit status and JSON/JSONL errors or denials. Keep logs outside the source tree and summarize evidence.
