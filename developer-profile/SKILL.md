---
name: developer-profile
description: "Enforces my preferred coding style: project-native, simple, modular, decoupled, strongly typed, readable, and consistent with existing code."
---

# Developer Profile

Use whenever implementing, refactoring, fixing, reviewing, or extending code; especially new features, behavior changes, refactors, bugs, components/services/utilities/types/tests, or unfamiliar project areas.

Instructions:
1. Inspect codebase first: folder structure; similar features; naming; state/data patterns; shared components/services/utilities/types/styles; error handling; tests.
2. Reuse existing code/patterns: no duplicate logic, components, services, types, utilities, styles, or architecture; prefer project-native patterns over generic external ones; extend abstractions only when clearly fitting; avoid new helpers/layers if existing ones solve it.
3. Implement smallest clean solution: focused, reviewable diff; no unrelated rewrites; no new architecture unless necessary; no new dependencies unless justified; simple explicit code over clever code.
4. Keep modular/decoupled: clear separation of concerns; small files/functions/components/services; do not mix UI, business logic, data access, and formatting; avoid hidden side effects.
5. Keep readable/typed: clear names matching project language; explicit types when clearer; avoid `any` without strong reason; avoid magic values via named constants when useful; handle relevant errors explicitly.
6. Follow project structure exactly: natural location; existing file naming, import style, formatting, conventions, and test structure.
7. After coding, briefly summarize: what changed; what existing code was reused; why structure fits; tradeoffs/follow-ups.
