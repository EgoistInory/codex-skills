---
name: code-review-lite
description: Review a low-to-medium complexity code change for material issues only. Focus on correctness, regression risk, security, and obvious maintainability problems; avoid style-only commentary.
---

# Code Review Lite

Review the diff and enough surrounding context to understand changed behavior.

## Check

- Correctness: wrong conditions, edge cases, error handling, state transitions, and contract mismatches
- Regression risk: changed defaults, compatibility, shared behavior, missing cleanup, and unintended scope
- Security: input validation, authorization, secrets, injection, unsafe file or network behavior, and sensitive logging
- Maintainability: only clear issues that make the change fragile, misleading, duplicated, or difficult to test
- Tests: missing coverage for material behavior or a fix that can regress

## Output

Lead with findings ordered by severity. For each finding, give the file and location, impact, evidence, and smallest useful correction. Do not include style preferences or generic praise.

If there are no material findings, say so clearly and note any unverified path or residual test gap.
