---
name: muxer-refine-ticket
description: Refine a Linear backlog issue for the Muxer Swift app and move it to Todo when it is actionable. Use when the user asks to refine a Muxer ticket, backlog item, or Linear issue such as "Refine MUX-123".
---

# Muxer Refine Ticket

Use this skill to turn a rough Linear backlog item into an actionable Todo issue. Do not implement code during refinement unless the user explicitly asks.

## Inputs

- Linear issue id, usually `MUX-123`.
- Optional product context from the user.

## Workflow

1. Read the Linear issue, comments, labels, project, and current status.
2. Inspect the repo narrowly only when needed to confirm feasibility, existing patterns, likely files, or test locations.
3. Rewrite or update the issue so it is implementation-ready:
   - clear problem statement
   - expected behavior
   - acceptance criteria
   - likely implementation notes
   - focused test expectations
   - open questions or blockers
4. Move the issue to `Todo` only if it has enough detail to implement without product guessing.
5. If important information is missing, leave it in `Backlog` and add the missing questions to the issue.

## Linear Format

Prefer this structure:

```markdown
## Problem

## Expected behavior

## Acceptance criteria
- [ ]

## Implementation notes

## Test expectations

## Open questions
```

## Agent Use

Do not spawn subagents for normal refinement. If the user explicitly asks to use agents, use at most one explorer agent to inspect code paths and produce concise implementation notes.

## Output

Report:

- whether the issue was moved to `Todo`
- what changed in the issue
- any open questions or blockers
- likely files/modules, if known
