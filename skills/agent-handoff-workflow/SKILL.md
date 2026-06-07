---
name: agent-handoff-workflow
description: Create and maintain portable project handoff context for agent-to-agent continuity. Use when a user mentions agent handoff, context limits, quota limits, switching agents or models, 接手项目, 交接, 上下文到顶, 额度用完, 项目背景断层, or asks Codex to preserve project understanding across sessions by creating or updating AGENTS.md, PROJECT_BRIEF.md, CURRENT_STATUS.md, TASKS.md, DECISIONS.md, HANDOFF.md, ACCEPTANCE.md, or CHANGELOG.md.
---

# Agent Handoff Workflow

Keep project memory in project files, not in the previous chat. The goal is to
make a new agent able to resume work from a small, current context packet
without reading old conversation history.

## Core Rules

- Do not frame handoff as bypassing quota, plan, or usage limits. Frame it as
  preserving project state and reducing context loss.
- Prefer a small context packet over a large knowledge base. Create only the
  files that will be read and maintained.
- Never overwrite existing project context files blindly. Read them first,
  preserve useful content, and patch only stale or missing sections.
- Treat `AGENTS.md` and `HANDOFF.md` as higher priority than chat history when
  they conflict with older conversation context.
- Keep handoff files specific, current, and operational. Avoid generic advice
  that the next agent cannot act on.

## Context Packet

Use this default packet for a project that needs durable handoff:

```text
AGENTS.md
PROJECT_BRIEF.md
CURRENT_STATUS.md
TASKS.md
DECISIONS.md
HANDOFF.md
ACCEPTANCE.md
CHANGELOG.md
```

Create fewer files when the project is small. The minimum useful packet is:

```text
AGENTS.md
PROJECT_BRIEF.md
CURRENT_STATUS.md
HANDOFF.md
```

## Start Or Refresh A Handoff Packet

1. Inspect the repository root and any existing project instructions.
2. Read existing context files before editing: `AGENTS.md`, `PROJECT_BRIEF.md`,
   `CURRENT_STATUS.md`, `TASKS.md`, `DECISIONS.md`, `HANDOFF.md`,
   `ACCEPTANCE.md`, and `CHANGELOG.md` when present.
3. Decide whether the project needs the full packet or the minimum packet.
4. Create missing files with concrete project facts gathered from the repo,
   current user request, recent diffs, and explicit user preferences.
5. Update stale files instead of duplicating content in new files.
6. Run the smallest useful verification: list the files, check markdown renders
   as plain text, and inspect the final diff.

## File Responsibilities

### AGENTS.md

Put durable agent behavior rules here: safety constraints, command rules,
validation expectations, style, repo-specific workflow, and which handoff files
must be read before work starts.

Include this resume rule when appropriate:

```md
Before continuing project work, read:
1. PROJECT_BRIEF.md
2. CURRENT_STATUS.md
3. HANDOFF.md
4. DECISIONS.md
5. ACCEPTANCE.md

If these files conflict with old chat context, follow AGENTS.md and HANDOFF.md.
```

### PROJECT_BRIEF.md

Record stable context:

- Project name and purpose
- User goal and non-goals
- Target users or audience
- Important constraints
- Long-term user preferences
- Domain terms, canonical formats, or naming rules

### CURRENT_STATUS.md

Record the current state:

- What works now
- What was completed recently
- What is in progress
- What is blocked
- Current branch, relevant commands, or environment notes when useful

### TASKS.md

Record actionable work, not broad wishes:

- Priority
- Task
- Status
- Owner or agent role when relevant
- Verification needed

### DECISIONS.md

Record decisions that should not be reopened without cause:

- Date
- Decision
- Reason
- Alternatives rejected
- Impact on future work

### HANDOFF.md

Make this the most current resume document. It should be short enough for a new
agent to read first and precise enough to continue immediately.

Use this structure:

```md
# HANDOFF.md

## Current Objective

## User Preferences To Preserve

## Completed

## In Progress

## Not Done

## Key Decisions

## Required Format Or Contracts

## Next Agent First Step

## Risks And Traps

## Verification Already Run
```

### ACCEPTANCE.md

Record how done will be judged:

- Functional acceptance criteria
- Required tests or checks
- Quality bar
- Known exclusions
- Manual verification steps when needed

### CHANGELOG.md

Record concise project changes in reverse chronological order. Do not turn it
into a full transcript.

## Before A Limit Or Session End

When the user asks for a handoff, or when work should pause before a context
limit, stop expanding scope and update `HANDOFF.md` plus any stale status files.

Capture:

1. Current project goal
2. User preferences that affect future outputs
3. Current task status
4. Completed work
5. Unfinished work
6. Recent key decisions
7. Required output or code contracts
8. First step for the next agent
9. Known pitfalls
10. Verification already run and remaining risk

## When Resuming A Project

Read in this order:

1. `AGENTS.md`
2. `PROJECT_BRIEF.md`
3. `CURRENT_STATUS.md`
4. `HANDOFF.md`
5. `DECISIONS.md`
6. `ACCEPTANCE.md`
7. `TASKS.md`
8. `CHANGELOG.md`

Then respond briefly with:

1. The understood project goal
2. Current task state
3. The next action

After that, continue the task. Do not restate the whole project history unless
the user asks.

## Multi-Agent Role Split

Use specialized roles only when they reduce confusion:

- Main agent: preserve user intent, scope, and durable decisions.
- Execution agent: implement the next concrete task.
- QA agent: verify acceptance criteria, risks, and regressions.
- Archivist agent: update context files and changelog.

All roles must share the same context packet. Do not let each agent maintain a
separate private version of the project state.
