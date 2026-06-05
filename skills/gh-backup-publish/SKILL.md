---
name: gh-backup-publish
description: Safely back up or publish a local project to GitHub. Use when a local vibe-coding project may not be a Git repository, has no GitHub remote, or needs its current changes synchronized. Creates a private GitHub repository automatically when needed, then commits and pushes without force-pushing or exposing secrets.
---

# GitHub Backup Publish

Publish a local project to GitHub with the smallest safe workflow. Default to a
private repository and treat the whole project as backup scope only after
checking exclusions and sensitive-file risks.

## Safety Rules

- Never print, stage, or commit secrets, tokens, cookies, private keys, or
  `.env` contents.
- Default a newly created GitHub repository to private unless the user
  explicitly requests another visibility.
- Never force-push, rewrite history, delete files, or replace an existing
  remote.
- Do not connect to a same-name existing GitHub repository until confirming it
  is the intended destination.
- Preserve unrelated user changes. If backup scope is ambiguous, stage explicit
  paths instead of `git add -A`.
- Stop on authentication, permission, or remote-history conflicts and report
  the exact blocker.

## Workflow

### 1. Inspect the Local Project

Work from the requested project directory.

1. Check for more specific `AGENTS.md` instructions.
2. Run `git status -sb` when the directory is already a Git repository.
3. Inspect `.gitignore` and candidate filenames without displaying sensitive
   file contents.
4. Ensure common local-only files are excluded when relevant:
   `.env*` except deliberate examples, private keys, credentials, dependency
   directories, editor state, caches, and generated secrets.
5. Review the intended staged diff before committing.

Do not initialize Git or stage files until the project boundary and sensitive
file exclusions are understood.

### 2. Verify GitHub Prerequisites

Run:

```bash
command -v gh
gh auth status
```

If `gh` is missing or unauthenticated, stop before attempting remote creation.
Ask the user to install or authenticate GitHub CLI, then resume from this step.
Never request or handle a token in chat.

### 3. Initialize and Commit Locally

If the directory is not a Git repository:

```bash
git init -b main
```

Stage only the intended backup scope. `git add -A` is allowed only when the
entire reviewed worktree belongs in the backup. Inspect the staged diff, then
create a concise commit:

```bash
git diff --cached --stat
git diff --cached --check
git commit -m "Back up project"
```

If there are no changes to commit, continue without creating an empty commit.

### 4. Select or Create the Remote

If `origin` exists, verify it is the intended GitHub repository and continue to
the push step.

If no remote exists:

1. Use the user-supplied repository name when present; otherwise use the local
   directory name if it is a valid, unambiguous repository name.
2. Resolve the authenticated owner without exposing credentials:

```bash
gh api user --jq .login
```

3. Check whether `OWNER/REPO` already exists:

```bash
gh repo view OWNER/REPO --json nameWithOwner,isPrivate,url
```

4. If it exists, stop and confirm it is the intended destination before adding
   it as a remote.
5. If it does not exist, create a private repository from the current project
   and push the current branch:

```bash
gh repo create OWNER/REPO --private --source=. --remote=origin --push
```

Treat only a confirmed "repository not found" result as permission to create.
Do not treat authentication, network, or permission failures as absence.

### 5. Synchronize an Existing Remote

For a verified existing `origin`, push the current branch with tracking:

```bash
git push -u origin "$(git branch --show-current)"
```

If the push is rejected because remote history exists, inspect and reconcile
the histories. Never automatically force-push.

### 6. Verify

Run the smallest decisive checks:

```bash
git status -sb
git remote -v
gh repo view --json nameWithOwner,isPrivate,url,defaultBranchRef
git ls-remote --exit-code origin "$(git branch --show-current)"
```

Report the repository URL, visibility, branch, commit, verification result, and
any remaining blocker. Do not open a pull request for a simple backup unless
the user requests one.
