---
name: frontend-acceptance-workflow
description: End-to-end workflow for improving an existing frontend project from product intent and UI design through implementation, code validation, browser regression testing, bug triage, and final acceptance. Use when Codex is asked to beautify or redesign a frontend, add generated visual assets, verify local web app behavior, debug user-reported UI regressions, or prepare a project for acceptance after frontend changes.
---

# Frontend Acceptance Workflow

Use this skill to run frontend work as a closed loop: understand intent, inspect the repo, implement in the existing style, validate with builds/tests, verify in browser, respond to user testing, and finish with acceptance notes.

## Operating Principles

- Preserve core product behavior while improving presentation and ergonomics.
- Read the existing code and design system before choosing a visual direction.
- Prefer scoped UI changes over broad rewrites unless the app is already a single-file MVP.
- Treat browser-visible behavior as the acceptance source of truth.
- When the user reports a regression, reproduce the exact user path before assuming the cause.
- Do not let new UI state machines block an existing working business flow.

## Workflow

1. Ground the project.
   - Inspect `package.json`, app entrypoints, main components, global styles, assets, and utilities.
   - Run a build or typecheck early if it is available and not destructive.
   - Note existing dirty files and do not revert unrelated user changes.

2. Lock product intent.
   - Identify audience, main workflow, success criteria, in/out of scope, and visual direction.
   - For frontend polish, choose a concrete aesthetic tied to the product domain.
   - If generated images are useful, define where they will be used and save project-bound assets inside the workspace.

3. Implement conservatively.
   - Keep business logic and public interfaces stable unless the request explicitly changes them.
   - Keep asset/file-processing semantics intact when changing UI.
   - For existing upload/crop/export flows, preserve the original happy path first; add feedback around it without blocking it.
   - Avoid hidden state that can strand users in `loading`, `selecting`, or `processing`.

4. Validate code.
   - Run the repo’s build/typecheck command.
   - If changing utilities, add or run focused checks for the transformed outputs.
   - Inspect diffs for accidental text corruption, stale labels, oversized assets, and unrelated churn.

5. Verify in browser.
   - Start the local dev server and open the known localhost URL with the in-app browser when available.
   - Check desktop and narrow/mobile viewports when layout changed.
   - Exercise primary workflows: initial render, key buttons, modals, upload paths, preview generation, error states, export/download.
   - Read browser console warnings/errors after interactions.

6. Handle user testing feedback.
   - Restate the exact observed behavior and expected behavior.
   - Determine whether the issue occurs before, during, or after the business operation.
   - Compare against the pre-change implementation when the user suspects a regression.
   - Fix the smallest layer that restores the intended behavior, then rebuild and refresh the browser.

7. Finish acceptance.
   - Summarize changed files and behavior.
   - Report verification commands and browser checks.
   - Call out any untested paths, environmental limitations, or manual test steps still needed.

## Regression Triage Pattern

For UI regressions, classify the failure point:

- **Event not triggered**: click/input handler or hidden input problem.
- **State stuck**: UI status changed but no business operation ran.
- **Business operation failed**: processing/export function threw or returned invalid output.
- **Preview/display failed**: output exists but is not rendered or is hidden by CSS.
- **User expectation mismatch**: UI wording implies automation but implementation requires manual confirmation.

When in doubt, restore the original working flow and layer feedback on top.

## Generated Asset Guidance

- Use generated bitmap assets only when they improve product communication or empty states.
- Save final project-bound assets under the repo, not only under Codex generated image storage.
- Verify generated assets load in the browser and do not block the primary workflow.

## Acceptance Checklist

Read `references/acceptance-checklist.md` when preparing a final verification pass or a handoff summary.
