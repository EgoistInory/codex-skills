---
name: macos-app-external-restart
description: Restart a macOS GUI application from Codex or another agent without relying on the current agent process staying alive. Use when the user asks to restart Codex, ChatGPT, Chrome, Electron apps, or any macOS app so new skills/plugins/config take effect, especially when nohup/background shell jobs may be killed with the agent. Provides launchd-based external restart, failure diagnosis, and cleanup verification.
---

# macOS App External Restart

Restarting the app that is hosting the agent is different from restarting a
normal child process. If the agent closes its own host app, ordinary shell
background jobs can be reaped before they finish. Use macOS `launchd` as the
external supervisor so the restart continues after the agent process is gone.

## When To Use

Use this skill when the user wants a macOS app restarted and any of these are
true:

- The app is Codex, ChatGPT, Chrome, or another GUI/Electron app.
- The restart is needed to reload newly installed skills, plugins, or config.
- The current agent is running inside the app being restarted.
- A previous `nohup ... &` or background shell restart did not complete.
- The user cares about no residual helper, test, or restart processes.

Do not use this for system reboots, login item management, or privileged daemon
changes unless the user explicitly asks and understands the risk.

## Core Rules

- Prefer a normal application quit first, then fall back to terminating only
  processes inside the target app bundle.
- Never use broad patterns like `pkill Codex`, `killall node`, or `killall
  Electron`; they can kill unrelated work.
- Submit the actual restart through `launchd`, not `nohup`, when restarting the
  app that owns the current agent session.
- Keep scripts one-shot. They must not contain keepalive loops or recurring
  jobs.
- Verify both success and cleanup: app is running, launchd job is gone, and no
  restart/test helper processes remain.
- Keep logs in `/private/tmp` until verification is complete, then remove them
  if the user asks for a clean machine state.
- Treat `Codex` and `ChatGPT` as compatible host names. The helper detects which
  host is running; if neither is running, it prefers the current
  `/Applications/ChatGPT.app` and falls back to the legacy
  `/Applications/Codex.app`.

## Recommended Script

This skill bundles a deterministic helper:

```bash
skills/macos-app-external-restart/scripts/restart-macos-app-via-launchd.sh
```

Copy or run it from the skill directory. First do a dry run:

```bash
scripts/restart-macos-app-via-launchd.sh --app Codex --delay 8 --dry-run
```

Then submit the restart:

```bash
scripts/restart-macos-app-via-launchd.sh --app Codex --delay 8
```

The command reports both `requested_app` and `effective_app`. For example,
`--app Codex` can correctly report `effective_app=ChatGPT` after the desktop
apps have been consolidated.

The command returns immediately after handing the job to `launchd`. The current
session may disconnect if it is inside the app being restarted.

## Manual Workflow

### 1. Identify The Target

Confirm the app name and app bundle path:

```bash
osascript -e 'application "Codex" is running'
osascript -e 'POSIX path of (path to application "Codex")'
```

If the app bundle cannot be resolved, stop and ask for the exact app path. Do
not guess a broad process pattern.

### 2. Avoid The `nohup` Trap

Do not rely on:

```bash
nohup ./restart.sh >/tmp/restart.log 2>&1 &
```

When the current agent host exits, the execution environment may kill or reap
that background process. A common failure signature is that the log contains
only the first line before `sleep`, then never reaches the quit/open steps.

### 3. Submit A One-Shot `launchd` Job

Use `launchctl submit` with a unique label:

```bash
launchctl submit -l "com.$USER.macos-app-external-restart.codex.$(date +%s)" -- /private/tmp/restart-worker.zsh
```

The worker should:

1. Sleep briefly to let the agent response flush.
2. Ask the app to quit with AppleScript.
3. Poll `application "<App>" is running`.
4. If still running, terminate only processes under the resolved app bundle
   path, for example `/Applications/Codex.app/Contents/`.
5. Reopen the app with `open -a "<App>"`.
6. Record final running state.
7. Remove its own launchd job with `launchctl remove "$XPC_SERVICE_NAME"`.

### 4. Verify

After reconnecting or after the expected delay, run:

```bash
tail -n 120 /private/tmp/<restart-log>.log
osascript -e 'application "Codex" is running'
launchctl print "gui/$(id -u)/<label>"
ps -axo pid,ppid,stat,etime,command | rg '<label>|restart-worker|Codex.app/Contents/MacOS/Codex'
```

Interpretation:

- A `launchctl print` "Could not find service" result is expected after the
  worker self-removes.
- The only process matches should be the current app's normal processes and the
  current `ps | rg` check itself.
- A fresh app PID or short elapsed time confirms the app restarted.

### 5. Clean Temporary Files

After success, remove one-shot workers and test logs:

```bash
rm -f /private/tmp/<restart-prefix>*
```

Then confirm:

```bash
ps -axo pid,ppid,stat,etime,command | rg '<restart-prefix>|nohup'
launchctl list | rg '<restart-prefix>'
ls -l /private/tmp/<restart-prefix>*
```

Expected cleanup result: no process matches except the current check command,
no launchd job matches, and no temporary files remain.

## Failure Patterns

### AppleScript Quit Returns `-128`

`用户已取消` / `user canceled` can happen when the app refuses or interrupts the
graceful quit request. Treat this as a failed graceful quit, not as total
failure. Continue to the scoped bundle-process termination fallback.

### `nohup` Writes Only The First Log Line

Root cause is usually host-environment cleanup of background children. Switch
to `launchd submit`; do not keep retrying `nohup`.

### `launchctl print` Still Shows The Job

Inspect `last exit code` and the stderr path. If it exited nonzero, read the
log. If it is still running beyond the expected delay, stop and inspect before
adding a second restart job.

### Multiple Old App Versions Appear

Crashpad handlers or update helpers may remain briefly. Only clean processes
that match the target app bundle and are clearly stale. Do not kill unrelated
Chrome, node, or MCP processes unless they are children of the target app's
current app-server and the user asked to stop that app.

## Success Report

Report:

- App name restarted.
- Whether graceful quit worked or fallback termination was used.
- New app running state and PID when checked.
- Whether the launchd job self-removed.
- Whether temporary files and helper processes were cleaned.
