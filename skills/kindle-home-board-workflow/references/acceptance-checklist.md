# Acceptance Checklist

## Code Checks

- Run Python unit tests for sync and service behavior.
- Run JavaScript tests for display polling and admin form transforms.
- Run syntax checks for Python and JavaScript files.
- Validate example JSON files.
- Run `git diff --check`.

## Display Page Browser Checks

- Open the local service in a controlled browser.
- Test the target e-ink viewport when known; for Kindle Oasis-style portrait, use about `1072x1448`.
- Confirm no horizontal overflow.
- Confirm clock/date, weather, schedule, reminders, shopping, focus, note, source status, and refresh button render.
- Click the manual refresh button and verify visible status changes.
- Check browser console errors.

## Admin Browser Checks

- Open `/admin.html`.
- Confirm the ordinary form loads existing board data.
- Confirm advanced JSON mode can be opened and contains valid JSON.
- Test a narrow mobile width around `390px`.
- Confirm no horizontal overflow.
- Check browser console errors.

## Sync Checks

- Run a dry-run or direct sync with example/private config when safe.
- Confirm generated fields are merged without erasing manual sections.
- Confirm daily sync marker prevents repeated successful syncs on the same day.
- Confirm failure does not update the marker, so retry remains possible.

## Handoff Notes

- State whether the local service is running.
- State the local/LAN URL if relevant.
- State what remains private and ignored by Git.
- State whether weather/calendar/reminder data is live, mocked, or disabled.
