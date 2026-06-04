# Frontend Acceptance Checklist

Use this checklist after implementing frontend changes.

## Build And Static Checks

- Run the repo’s build/typecheck command.
- Confirm no new TypeScript/template errors.
- Inspect changed files for unrelated rewrites or stale generated artifacts.
- Confirm new assets are referenced from workspace paths.

## Visual Checks

- First screen renders without blank media.
- Text does not overflow buttons, cards, or panels.
- Main CTA and secondary controls are visible at narrow and desktop widths.
- Empty states are informative and do not hide upload/action targets.
- Modals fit the viewport and can be closed.

## Workflow Checks

- Primary input/upload path works.
- Canceling a file picker resets transient state.
- Processing states resolve to success or error.
- Error states explain the next action.
- Preview reflects processed output, not just source input.
- Existing export/download behavior still works.

## Browser Checks

- Open the local app in the in-app browser when possible.
- Capture or inspect the relevant viewport after major UI changes.
- Check console errors/warnings after interactions.
- Reload after code changes and repeat the failing user path.

## Final Handoff

- List changed behavior and key files.
- Include commands run and their results.
- Mention any manual steps not automatable, such as native file picker selection.
- Note unrelated dirty files without reverting them.
