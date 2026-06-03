---
name: developer-profile
description: "Enforces my preferred coding style: project-native, simple, modular, decoupled, strongly typed, readable, and consistent with existing code."
---

# Developer Profile

Use this skill whenever implementing, refactoring, fixing, reviewing, or extending code.

Use it especially when:
- adding a new feature
- changing existing behavior
- refactoring code
- fixing bugs
- creating components, services, utilities, types, or tests
- working in an unfamiliar part of the project

## Instructions

1. First inspect the existing codebase before making changes.
   - Check the current folder structure.
   - Look for similar existing features.
   - Identify naming conventions.
   - Identify state/data patterns.
   - Identify shared components, services, utilities, types, and styles.
   - Identify existing error handling and testing patterns.

2. Reuse what already exists.
   - Do not duplicate logic, components, services, types, utilities, styles, or architecture.
   - Prefer existing project patterns over generic external patterns.
   - Extend existing abstractions only when it clearly fits.
   - Avoid creating new helpers or layers if existing ones already solve the problem.

3. Implement the smallest clean solution.
   - Keep changes focused and easy to review.
   - Do not rewrite unrelated code.
   - Do not introduce new architecture unless necessary.
   - Do not add new dependencies unless clearly justified.
   - Prefer simple, explicit code over clever code.

4. Keep code modular and decoupled.
   - Use clear separation of concerns.
   - Keep files, functions, components, and services small.
   - Avoid mixing UI, business logic, data access, and formatting concerns.
   - Avoid hidden side effects.

5. Keep code readable and strongly typed.
   - Use clear names that match the project language.
   - Prefer explicit types where they improve clarity.
   - Avoid `any` unless there is a strong reason.
   - Avoid magic values; use named constants when useful.
   - Handle errors explicitly where relevant.

6. Follow the project structure exactly.
   - Place new code where this project would naturally place it.
   - Match existing file naming.
   - Match existing import style.
   - Match existing formatting and conventions.
   - Match existing test structure when adding tests.

7. After coding, provide a brief summary.
   - What changed.
   - What existing code was reused.
   - Why the structure fits the project.
   - Any tradeoffs or follow-ups.
