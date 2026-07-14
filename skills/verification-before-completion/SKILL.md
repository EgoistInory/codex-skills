---
name: verification-before-completion
description: Use before claiming coding work is complete, fixed, passing, or ready. Require fresh evidence from the applicable tests, build or type checks, and critical-path verification.
---

# Verification Before Completion Lite

Match each completion claim to fresh evidence from the current state.

## Gate

1. Identify the claims being made and the cheapest commands or checks that prove them.
2. Run the relevant focused tests.
3. Run the applicable build, type check, lint, or syntax validation when the change can affect it.
4. Exercise the changed critical path at its real boundary when practical: CLI, API, browser, export, deployment, or remote state.
5. Read exit codes and meaningful output before reporting success.

Scale verification to risk, but do not omit the only check that can prove the requested behavior. Do not claim unrun checks passed.

If a check is unavailable or fails, report the actual state, exact blocker, and any narrower evidence that did pass.
