# Planning Threshold

Choose the lightest workflow that preserves correctness.

Execute directly when the change is localized, acceptance criteria are clear,
and verification is obvious. Read the relevant context, make the smallest
change, and verify it.

Create a short plan when any of these apply:

- Three or more dependent implementation steps
- Coupled changes across modules or services
- Data migration, compatibility, permissions, or rollback risk
- Important behavior with unclear acceptance criteria
- Multiple valid approaches with meaningful tradeoffs

Keep the plan to 3-5 outcome-oriented steps with at most one step in progress.
For an OpenSpec project, use `openspec-propose` when a plan is warranted and
`openspec-apply-change` after the proposal is ready. Do not expand a small
task into architecture work, speculative requirements, or unrelated cleanup.
