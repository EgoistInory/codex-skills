---
name: tdd
description: Use selective test-driven development for core logic, complex state, algorithms, important bug fixes, and behavior likely to regress. Do not trigger for simple copy, styling, configuration, or trivial wiring changes.
---

# TDD Lite

Use test-first development only where the behavior justifies it.

## Trigger

Use TDD for:

- Core business rules or public contracts
- Complex state transitions or concurrency
- Algorithms and nontrivial transformations
- Important bug fixes with a reproducible regression
- Behavior with a meaningful history or likelihood of regression

Skip TDD for simple text, styling, static configuration, generated files, trivial wiring, or exploratory prototypes. Existing project rules can still require tests.

## Cycle

1. Define one observable behavior.
2. Write the smallest test that expresses it.
3. Run the test and confirm it fails for the intended reason.
4. Implement the minimum code needed to pass.
5. Run the focused test, then nearby regression tests.
6. Refactor only while tests remain green.

Prefer public behavior over implementation details. For bug fixes, preserve the failing case as a regression test.
