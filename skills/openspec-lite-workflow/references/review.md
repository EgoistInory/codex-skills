# Focused Code Review

Review the diff and enough surrounding context to understand changed behavior.

Check only material issues:

- Correctness: conditions, edge cases, errors, state, and contracts
- Regression risk: defaults, compatibility, shared behavior, cleanup, and scope
- Security: validation, authorization, secrets, injection, unsafe I/O, and logs
- Maintainability: clear fragility, misleading structure, duplication, or poor
  testability
- Tests: missing coverage for material behavior or a regression-prone fix

Lead with findings ordered by severity. Give the file and location, impact,
evidence, and smallest useful correction. Omit style-only preferences and
generic praise. If there are no material findings, say so and note any
unverified path or residual test gap.
