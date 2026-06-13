# Kindle Home Board Project Experience

## Goal

Turn a Kindle or similar e-ink reading device into a low-maintenance household information board. The main constraints are old browser support, slow e-ink refresh, non-technical household users, local-network reliability, and privacy.

## Proven Shape

- `index.html` + `app.js` + `styles.css`: dependency-free display page using old-browser-friendly JavaScript.
- Local server: static files plus JSON read/write endpoints.
- `admin.html` + `admin.js`: household form editor with advanced JSON fallback.
- `board_sync.py` or equivalent: local sync script that writes external data into `data/board.json`.
- `data/board.json`: the only file the display page reads.
- `data/sources.json`: local private source configuration, ignored by Git.

## Useful Behaviors

- Update local clock every minute.
- Poll `data/board.json` every 5 minutes.
- Keep a 15-minute full-page refresh fallback.
- Provide a manual refresh button.
- Sync weather, calendar, and reminders on the local computer or server.
- Run weather sync once per day by default.
- Use a daily marker so service restarts do not repeatedly call external APIs.
- Keep weather generated and read-only in the family admin form.

## Design Decisions

- The display device reads local JSON only. It does not call external APIs directly.
- External credentials stay on the local machine or hosting backend.
- Weather does not need high-frequency refresh on an e-ink board.
- Family admin pages should be form-first. Raw JSON belongs behind an advanced mode.
- Avoid frameworks and build chains for small local boards when standard HTML/CSS/JS and Python are sufficient.

## Risk Notes

- If the host computer sleeps or the local service stops, background sync stops too.
- Old Kindle browsers may suspend timers while sleeping.
- Python certificate stores may fail on some macOS installs; a system `curl` fallback can be pragmatic for HTTPS fetches.
- Query-string tokens are convenient but leave traces in history and logs.

## Good Next Features

- One-click preview from Admin to the display page.
- Startup logging for sync enabled/disabled and last sync date.
- Home Assistant or NAS status as another server-side JSON source.
- Stronger auth only if exposing beyond trusted LAN.
