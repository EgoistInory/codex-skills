# Completion Verification

Match each completion claim to fresh evidence from the current state.

1. Identify the claims and the cheapest checks that prove them.
2. Run the relevant focused tests.
3. Run the applicable build, type check, lint, or syntax validation.
4. Exercise the changed critical path at its real boundary when practical:
   CLI, API, browser, export, deployment, or remote state.
5. Read exit codes and meaningful output before reporting success.

Scale verification to risk, but do not omit the only check that can prove the
requested behavior. Do not claim unrun checks passed. If a check is unavailable
or fails, report the actual state, exact blocker, and narrower evidence that did
pass.
