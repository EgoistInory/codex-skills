# Selective TDD

Use test-first development only for:

- Core business rules or public contracts
- Complex state transitions or concurrency
- Algorithms and nontrivial transformations
- Important bug fixes with a reproducible regression
- Behavior likely to regress

Skip TDD for simple text, styling, static configuration, generated files,
trivial wiring, or exploratory prototypes unless project rules require it.

Cycle:

1. Define one observable behavior.
2. Write the smallest test that expresses it.
3. Run it and confirm it fails for the intended reason.
4. Implement the minimum code needed to pass.
5. Run the focused test, then nearby regression tests.
6. Refactor only while tests remain green.

Prefer public behavior over implementation details. Preserve bug reproductions
as regression tests.
