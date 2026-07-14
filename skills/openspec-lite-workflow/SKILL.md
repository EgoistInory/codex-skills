---
name: openspec-lite-workflow
description: Route clear low-to-medium complexity software work through a token-efficient OpenSpec workflow with plan-lite, selective TDD, systematic debugging, completion verification, and focused code review. Use full Superpowers instead for broad, highly uncertain, or deeply coupled projects when token cost is not a concern.
---

# OpenSpec Lite Workflow

Use the smallest process that gives reliable evidence.

## Route

Start with `plan-lite`.

- **Simple and localized:** read context, edit directly, then use `verification-before-completion`. Do not create planning artifacts.
- **Bounded medium complexity:** use the OpenSpec flow below.
- **High complexity or high uncertainty:** hand off to the full Superpowers workflow when broad discovery, architecture, parallel work, or extensive planning is justified.

Treat a project as high complexity when it spans multiple systems or teams, has unclear architecture or requirements, carries difficult migration or rollback risk, or needs substantial research before implementation.

## OpenSpec Flow

1. Use `openspec-explore` only when a bounded question still needs clarification.
2. Use `openspec-propose` to create the proposal, design, specs, and short task list.
3. Review scope and acceptance criteria before implementation.
4. Use `openspec-apply-change` to implement the tasks.
5. Use `verification-before-completion`, then `code-review-lite`.
6. Fix material findings and repeat affected checks.
7. Use `openspec-archive-change` only after implementation and verification are complete.

## Conditional Skills

- Use `tdd` only for core logic, complex state, algorithms, important fixes, or regression-prone behavior.
- Use `systematic-debugging` whenever a test, build, runtime, or integration check fails unexpectedly.
- Use `verification-before-completion` for every completion claim.
- Use `code-review-lite` after a material change; skip it for truly trivial edits unless risk warrants review.

Do not load every skill body up front. Invoke each skill only when its trigger is reached.

Keep changes narrow, preserve existing work, and avoid unrelated refactors.
