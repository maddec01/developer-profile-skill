---
name: muxer-work-ticket
description: Implement a refined Linear Todo issue for the Muxer Swift app using repo conventions, focused tests, caveman full communication, developer-profile implementation standards, and cavecrew subagents when explicitly requested. Use when the user asks to work a Muxer ticket such as "Work MUX-123" or "Work MUX-123 using agents".
---

# Muxer Work Ticket

## Required Skill Modes

- Use `caveman` at `full` intensity 
- Use `developer-profile` for implementation.
- Use `cavecrew` only when the user explicitly asks for agents, delegation, subagents, or parallel work.

## Preconditions

- Read `AGENTS.md` in the repo root first.
- Read the Linear issue, comments, acceptance criteria, and status. If the issue is part of a Linear Project, also read the project description for context. Prefer `Todo`; refine vague or `Backlog` issues first, or report the blocker.
- Solo workflow by default: use the current git state, do not change checkout, and do not open a PR unless asked.

## Workflow

1. Confirm the ticket contract: behavior, acceptance criteria, likely files/modules, and test expectations.
2. If Linear tools are available and the issue is ready, move it to `In Progress`.
3. Check git state, worktree, and index; protect unrelated user changes.
4. Find any relevant skills in the project skills and use them to guide implementation.
5. Inspect the smallest relevant code paths, then implement the smallest change that matches existing Muxer patterns.
6. Add/update focused tests where behavior can be tested directly.
7. Run targeted validation when practical.
8. Review the diff for acceptance coverage, Swift style, broad rewrites, edge cases, and weak/missing tests.
9. If Linear tools are available, add a concise implementation note and move the issue to `In Review`.

Do not commit, push, or move the issue to `Done` until the user explicitly says they are happy with the change or otherwise approves finalization.

## Git And Review

- The user's code review feedback is expected in the same Zed agent chat where the ticket is being worked.
- Use Linear comments for concise implementation/status notes, not line-by-line code review.
- Every Muxer commit, including ad-hoc staged-file commits, must use Conventional Commits. Use the issue key in scope when useful, e.g. `fix(MUX-18): preserve cached audio extensions`; avoid sentence-style messages. Prefer `feat`, `fix`, `refactor`, `test`, `chore`, or `docs`.

## Final Approval Mode

When the user approves, says they are happy, or asks to finalize:

1. Review the final diff and ensure only ticket-related changes are included.
2. Check staged/unstaged changes. Unstage unrelated files without reverting them; stage only ticket-related files.
3. Create a Conventional Commit for the ticket.
4. Push current `HEAD`; if no upstream exists, set upstream tracking for the existing checkout.
5. If Linear tools are available, add a concise completion note and move the issue to `Done`.

## Chat Review Mode

When the user gives review feedback or requested changes in the same chat:

1. Read the feedback and Linear issue; review the local diff and recent ticket commits.
2. Keep the checkout, make only requested follow-up changes, and update tests only for changed behavior or newly exposed gaps.
3. Run targeted validation.
4. Keep Linear in `In Review`; do not commit or move to `Done` until finalization approval, unless already finalized or explicitly asked to commit.

## Post-Finalization Follow-Up

When the same chat finds a missed change after commit, push, and `Done`:

1. If Linear tools are available, move the issue back to `In Review`.
2. Make only the requested follow-up in the current git state and run targeted validation.
3. Amend the existing ticket commit instead of creating a second commit.
4. Force-push with lease after amending.
5. If Linear tools are available, add a concise update note and move the issue back to `Done`.

## Agent Use

Skills do not automatically create agents. Only spawn subagents when the user explicitly asks for agents, delegation, or parallel work.

When agents are allowed:

- Use `cavecrew-investigator` for bounded code mapping, call-site searches, and ambiguity checks.
- Use `cavecrew-builder` only for surgical edits with obvious scope and no more than two owned files.
- Use `cavecrew-reviewer` for independent diff review before handoff.
- Do not assign overlapping write scopes. Main agent owns planning, integration, validation, and final summary.
- Close out agent findings: address them, explain why out of scope, or note residual risk.

## Output

Report:

- changed files
- git status
- tests or validation run
- Linear issue updates
- remaining risks or follow-up items
