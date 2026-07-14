---
name: openspec-lite-workflow
description: Route clear low-to-medium complexity software work through a token-efficient OpenSpec workflow with conditional planning, selective TDD, systematic debugging, completion verification, and focused code review. Use full Superpowers instead for broad, highly uncertain, or deeply coupled projects when token cost is not a concern.
---

# OpenSpec Lite Workflow

Use the smallest process that gives reliable evidence.

## Route

Start with the planning threshold in [references/planning.md](references/planning.md).

- **Simple and localized:** read context, edit directly, then run the completion verification module. Do not create planning artifacts.
- **Bounded medium complexity:** use the OpenSpec flow below.
- **High complexity or high uncertainty:** hand off to the full Superpowers workflow when broad discovery, architecture, parallel work, or extensive planning is justified.

Treat a project as high complexity when it spans multiple systems or teams, has unclear architecture or requirements, carries difficult migration or rollback risk, or needs substantial research before implementation.

## OpenSpec Flow

1. Use `openspec-explore` only when a bounded question still needs clarification.
2. Use `openspec-propose` to create the proposal, design, specs, and short task list.
3. Review scope and acceptance criteria before implementation.
4. Use `openspec-apply-change` to implement the tasks.
5. Run the completion gate, then the focused review.
6. Fix material findings and repeat affected checks.
7. Use `openspec-archive-change` only after implementation and verification are complete.

## Conditional Modules

- Read [references/tdd.md](references/tdd.md) only for core logic, complex state, algorithms, important fixes, or regression-prone behavior.
- Read [references/debugging.md](references/debugging.md) whenever a test, build, runtime, or integration check fails unexpectedly.
- Read [references/verification.md](references/verification.md) before every completion claim.
- Read [references/review.md](references/review.md) after a material change; skip review for truly trivial edits unless risk warrants it.

Do not load every reference up front. Read a module only when its trigger is reached.

Keep changes narrow, preserve existing work, and avoid unrelated refactors.
