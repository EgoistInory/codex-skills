---
name: kindle-home-board-workflow
description: Workflow for building, improving, and accepting Kindle or low-capability browser home dashboards, e-ink information boards, family boards, and local JSON-driven display pages. Use this skill whenever the user mentions Kindle browsers, e-ink dashboards, old browsers, local family information boards, weather/calendar/reminder integrations for a display page, or making a constrained reading-device page genuinely useful.
---

# Kindle Home Board Workflow

Use this skill to keep constrained-device dashboard projects practical: old-browser friendly, low refresh, local-data first, privacy-aware, and easy for non-technical household users to maintain.

## Core Principles

- Treat the display device as weak and unreliable. Keep the client dependency-free and avoid modern browser assumptions.
- Put external integrations on the local computer or server side. The Kindle/e-ink browser should read one simple local data file.
- Optimize for usefulness over novelty: readable layout, reliable refresh, manual fallback, and simple admin workflows matter more than high-frequency data.
- Do not ask family users to edit raw JSON unless it is explicitly an advanced mode.
- Keep private source config out of Git. Calendar URLs, tokens, and local device addresses are sensitive enough to avoid commits.

## Default Architecture

Use this shape unless the existing project clearly already has a better one:

- Static display page: `index.html`, `app.js`, `styles.css`.
- Local service: a small standard-library server or existing local backend.
- Single display data source: `data/board.json`.
- Private integration config: `data/sources.json`, ignored by Git.
- Public example config: `data/sources.example.json`.
- Admin page: form-first editing, with advanced JSON mode as fallback.

## Browser Compatibility Rules

- Prefer `XMLHttpRequest` over `fetch` for old Kindle browsers.
- Prefer `var` and ordinary functions over modern JavaScript syntax.
- Use conservative DOM APIs: `createElement`, `appendChild`, text nodes, `setInterval`.
- Keep CSS conservative: high contrast, stable dimensions, restrained layout, no framework dependency.
- Verify real viewport sizes for the target device. For Kindle Oasis-style portrait testing, check around `1072x1448` when applicable.

## Refresh Model

Use a layered pull model:

- Clock/date: update locally every minute.
- Board data: poll `data/board.json` every few minutes and update only when content changed.
- Page fallback: keep a slower full-page refresh, such as 15 minutes, for old-browser recovery.
- Manual fallback: keep a visible refresh button.

Avoid push/WebSocket-first designs for Kindle browsers. They are not reliable enough for the device class.

## External Data Integrations

Prefer this flow:

1. Local sync script or server task fetches external sources.
2. It merges external data into `data/board.json`.
3. The display page sees only the changed JSON file.

Recommended handling:

- Weather: daily sync is usually enough for an e-ink home board.
- Calendar: consume `.ics` or `webcal` feeds on the server side.
- Reminders/tasks: read from local OS or trusted local automation when possible.
- Feishu or cloud work tools: reserve configuration until credentials, permissions, and token storage are designed.

## Admin UX

Default to a household-friendly form:

- Title
- Message/note
- Schedule
- Reminders
- Shopping/restock
- Focus items

Weather and generated fields should be displayed but not hand-edited by default, because manual edits can overwrite automatic sync output. Keep an advanced JSON mode for recovery and fields not yet covered by forms.

## Security Boundaries

- Local write tokens protect writes, not necessarily reads, unless the project explicitly implements read auth.
- Do not commit real `data/sources.json`, calendar feed URLs, API tokens, local passwords, or generated private tokens.
- Warn when URL query tokens are used: they can appear in browser history and server logs.
- Avoid putting sensitive household data on the board: precise addresses, lock codes, ID numbers, children’s schools, or complete travel plans.

## Implementation Workflow

1. Inspect the existing repo and dirty state.
2. Identify the target device and real constraints.
3. Add or update focused tests before behavior changes when practical.
4. Implement the smallest compatible change.
5. Run syntax, unit, and data-format checks.
6. Start the local service and verify in browser at device and mobile/admin widths.
7. Report exact behavior, commands run, and remaining limitations.

## Verification Checklist

Read `references/acceptance-checklist.md` before final acceptance or handoff.

Read `references/project-experience.md` when the user asks to continue or adapt a Kindle Home Board-style project.
