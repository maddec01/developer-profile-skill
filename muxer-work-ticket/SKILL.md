---
name: muxer-work-ticket
description: "Work refined Linear Todo tickets for the Muxer Swift app using repo conventions, focused tests, caveman full, developer-profile standards, and cavecrew only on explicit agent/delegation request. Triggers: 'Work MUX-123', 'Work MUX-123 using agents'."
---

# Muxer Work Ticket

Modes: `caveman` full; `developer-profile` implementation; `cavecrew` only on explicit agents/delegation/subagents/parallel request.

Before work:
- Read repo-root `AGENTS.md` first.
- Read Linear issue: comments, acceptance criteria, status; if in Linear Project, read project description. Prefer `Todo`; refine vague/`Backlog` first or report blocker.
- Solo default: current git state/checkout; protect it; no PR unless asked.

Workflow:
1. Confirm contract: behavior, acceptance criteria, likely files/modules, tests.
2. If Linear tools + ready issue: move to `In Progress`.
3. Check git status/worktree/index; protect unrelated user changes.
4. Find/use relevant project skills.
5. Inspect smallest relevant paths; make smallest change matching Muxer patterns.
6. Add/update focused tests for directly testable behavior.
7. Run targeted validation when practical.
8. Review diff: acceptance coverage, Swift style, broad rewrites, edge cases, weak/missing tests.
9. If Linear tools: add concise implementation note; move issue to `In Review`.

Stop: no commit, push, or Linear `Done` until user approves/finalizes. No PR unless asked.

Git/review:
- Review feedback expected.
- Linear comments = concise implementation/status notes, not line-by-line review.
- Every Muxer commit, including ad-hoc staged-file commits, uses Conventional Commits.

Final approval triggers: user approves, says happy, or asks to finalize.
1. Review final diff; ensure only ticket-related changes.
2. Check staged/unstaged; unstage unrelated without reverting; stage only ticket files.
3. Create Conventional Commit.
4. Push `HEAD`; if no upstream, set upstream for existing checkout.
5. If Linear tools: add completion note; move issue to `Done`.

Chat review feedback:
1. Read feedback + Linear issue; review local diff + recent ticket commits.
2. Keep checkout; make only requested follow-up changes; update tests only for changed behavior/new gaps.
3. Run targeted validation.
4. Keep Linear `In Review`; no commit/`Done` until final approval, unless already finalized or explicitly asked to commit.

Post-finalization missed change (same chat after commit+push+`Done`):
1. If Linear tools: move issue back to `In Review`.
2. Make only requested follow-up in current git state; run targeted validation.
3. Amend existing ticket commit, not second commit.
4. Force-push with lease.
5. If Linear tools: add update note; move back to `Done`.

Agents:
- Never auto-spawn; only explicit user ask for agents/delegation/subagents/parallel work.
- If allowed: `cavecrew-investigator` = bounded code maps/call-site searches/ambiguity checks; `cavecrew-builder` = surgical edits, obvious scope, max 2 owned files; `cavecrew-reviewer` = independent diff review before handoff.
- No overlapping write scopes. Main agent owns planning, integration, validation, final summary.
- Close agent findings: address, mark out-of-scope, or note residual risk.

Output: changed files; git status; validation/tests; Linear updates; risks/follow-ups.
