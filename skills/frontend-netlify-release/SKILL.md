---
name: frontend-netlify-release
description: Verify, commit, push, and deploy frontend projects to Netlify. Use when publishing Vite/React/static frontend sites with Netlify MCP or Netlify CLI, especially after UI changes, when avoiding failed deploys caused by dirty worktrees, oversized workspaces, node_modules, .git, caches, missing site links, npm cache permissions, or Netlify MCP upload errors.
---

# Frontend Netlify Release

Use this workflow for frontend release tasks that end with a Netlify deploy. Keep the sequence strict: verify locally, commit and push, then deploy from a clean source snapshot.

## Release Workflow

1. Inspect scope before changing state:
   - `git status --short`
   - `git branch --show-current`
   - `git remote -v`
   - Read `package.json` and `netlify.toml`.

2. Run the smallest decisive local validation:
   - Prefer `npm run build` for Vite/React/static sites.
   - If a dev server is already running, use it only for focused UI checks.
   - Stop local dev servers started for validation before finishing.

3. Check deploy package risk before Netlify MCP upload:
   - `du -sh . dist node_modules .git .npm-cache 2>/dev/null`
   - `cat .netlifyignore 2>/dev/null`
   - Treat workspaces over a few hundred MB as risky for Netlify MCP upload.
   - Common failure cause: Netlify MCP uploads the source directory and may choke on `.git`, `node_modules`, `.npm-cache`, or other generated/cache directories even when the built site is small.

4. Commit and push only intended files:
   - Commit after validation passes.
   - Push the branch before deployment when the user asked to save/publish.
   - If sandbox blocks `.git/index.lock` or SSH, request escalation for the exact Git command.

5. Prefer a clean release directory for Netlify MCP deploy:
   - Use a temp directory generated from the current commit rather than the dirty working directory.
   - Example:
     ```bash
     release_dir="/private/tmp/<repo>-release-$(git rev-parse --short HEAD)"
     mkdir -p "$release_dir"
     git archive --format=tar HEAD -o "$release_dir.tar"
     tar -xf "$release_dir.tar" -C "$release_dir"
     du -sh "$release_dir"
     ```
   - Run Netlify MCP deploy from `release_dir`, not from the original repo, when the original repo contains large ignored directories.

## Netlify Checks

Use the Netlify plugin or CLI to identify the site before deploying.

- Read Netlify user/project state.
- Search projects by repository/site name.
- Never create a new site unless the user confirms it.
- Record:
  - `siteId`
  - production URL
  - current deploy id and state

If using CLI and `npx netlify status` hangs or fails:

- Use `npx --yes netlify-cli status`.
- If `~/.npm` has EACCES/root-owned cache errors, do not run `sudo chown`.
- Use a temporary cache:
  ```bash
  npm_config_cache=/private/tmp/codex-npm-cache npx --yes netlify-cli status
  ```

## Netlify MCP Deploy

When the Netlify deploy updater returns an `npx -y @netlify/mcp@latest ...` command:

1. Run it from the clean release directory.
2. Use temporary npm cache if local npm cache has permission issues:
   ```bash
   npm_config_cache=/private/tmp/codex-npm-cache npx -y @netlify/mcp@latest ...
   ```
3. Wait for final deploy state.
4. If the first MCP deploy from the original repo fails with `500 Internal Server Error`, check workspace size and retry once from a clean release directory.
5. If the clean release directory deploy also fails with the same server error, stop retrying and report Netlify-side failure.

## Post-Deploy Verification

After deploy succeeds:

- Read deploy details and confirm `state: ready`.
- Confirm production URL and deploy URL.
- Fetch the production homepage with `curl -L <site-url>` and verify it references the new built assets.
- Check `git status --short` is clean.

Report concise release evidence:

- Commit hash and message.
- Push target.
- Netlify deploy id.
- Production URL.
- Validation commands that passed.
- Any residual risk or blocked item.

## Failure Summary Pattern

When Netlify MCP upload fails:

- State exact error text, such as `500 Internal Server Error`.
- State whether Git push succeeded.
- State current Netlify deploy id if unchanged.
- State the next safe action, usually clean release directory deploy or Netlify dashboard/CLI auth.
