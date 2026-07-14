---
name: plan-lite
description: "Decide whether a coding task needs planning. Use for low-to-medium complexity work with OpenSpec: execute simple localized changes directly, and create a short plan only for coupled, risky, multi-file, or unclear work."
---

# Plan Lite

Choose the lightest workflow that preserves correctness.

## Decision

Execute directly when the change is localized, acceptance criteria are clear, and verification is obvious. Read the relevant context, make the smallest change, and verify it.

Create a short plan when any of these apply:

- Three or more dependent implementation steps
- Coupled changes across modules or services
- Data migration, compatibility, permissions, or rollback risk
- Important behavior with unclear acceptance criteria
- Multiple valid approaches with meaningful tradeoffs

## Short Plan

Keep the plan to 3-5 outcome-oriented steps. Mark at most one step in progress. Update it only when execution materially changes.

For an OpenSpec project, use `openspec-propose` when a plan is warranted, then `openspec-apply-change` after the proposal is ready. Simple fixes do not need OpenSpec artifacts.

Do not expand a small task into architecture work, speculative requirements, or unrelated cleanup.
