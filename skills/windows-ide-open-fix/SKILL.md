---
name: windows-ide-open-fix
description: Use when Codex Desktop on Windows fails to open a project or file in a configured IDE such as Antigravity, VS Code, Cursor, PyCharm, or another editor, especially when the target IDE icon is wrong, the IDE path contains spaces, the IDE CLI exits with code 1, or Codex logs show Failed to open file / exited with code errors.
---

# Windows IDE Open Fix

Use this skill to diagnose and fix Windows-only failures where Codex cannot open a workspace, folder, or file through the configured IDE from the top-right "open in IDE" control.

## Safety

- Do not modify project code for this class of issue unless logs prove the project itself is the cause.
- Do not delete IDE user data, extension directories, or app caches as a first step.
- Do not restart Explorer, kill IDE processes, reinstall the IDE, or edit global PATH without explicit user approval.
- Never print secrets from Codex, IDE, browser, or app logs. Quote only minimal error lines.
- Prefer user-level, reversible fixes such as a shim command in a user PATH directory.

## Fast Triage

1. Confirm scope:
   - Does the failure happen for one project, all projects, or individual files?
   - Does direct IDE launch work outside Codex?
   - Is the IDE icon wrong, missing, or pointing to another editor?

2. Inspect Codex configuration:

```powershell
rg -n "open-in-target|open-in-target-preferences|antigravity|visualStudio|cursor|code|pycharm" "$env:USERPROFILE\.codex\config.toml" "$env:USERPROFILE\.codex\.codex-global-state.json"
```

3. Inspect recent Codex logs:

```powershell
Get-ChildItem -LiteralPath "$env:LOCALAPPDATA\Codex\Logs" -Recurse -File |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 10 FullName,Length,LastWriteTime

rg -n "Failed to open file|exited with code|ENOENT|spawn|open.*file|antigravity|code.cmd|cursor|pycharm|auto_verification" "$env:LOCALAPPDATA\Codex\Logs" -i
```

Look for lines like:

```text
Failed to open file ... <IDE CLI>.cmd exited with code 1 (<target path>)
```

4. Identify the exact IDE command Codex is trying to use. Check both PATH and configured shortcuts:

```powershell
Get-Command antigravity,antigravity.cmd,code,code.cmd,cursor,cursor.cmd,pycharm64 -All -ErrorAction SilentlyContinue |
  Select-Object Name,Source,CommandType

cmd.exe /d /c where antigravity.cmd
cmd.exe /d /c where code.cmd
```

## Reproduce Like Codex

Codex/Electron often behaves closer to `cmd.exe` than to PowerShell. Reproduce with `cmd.exe` and a quoted target path:

```powershell
cmd.exe /d /c antigravity.cmd "D:\path\to\project"
cmd.exe /d /c code.cmd "D:\path\to\project"
```

If calling the full path manually works but Codex fails, test whether the IDE executable or `.cmd` path contains spaces:

```powershell
cmd.exe /d /c ""E:\Program Files\Antigravity\bin\antigravity.cmd" "D:\path\to\project""
```

A failure such as `'E:\Program' is not recognized` indicates quoting or command-discovery trouble around a path containing spaces.

## Common Root Causes

- IDE installed under a path with spaces, such as `E:\Program Files\...`, and Codex/Electron invokes its `.cmd` wrapper incorrectly.
- Codex cached a stale absolute IDE CLI path.
- Start menu shortcut has a valid target but invalid or empty `IconLocation`, causing the target IDE icon to look wrong.
- PATH differs between PowerShell, `cmd.exe`, and Codex because Codex shell env loading timed out.
- IDE CLI is present but the running IDE instance is unhealthy, so the CLI exits nonzero.
- Git ownership (`dubious ownership`) may break IDE SCM features but is usually not the direct cause of opening the IDE.

## Minimal Fixes

### Fix a Broken IDE Icon

Check shortcut target and icon:

```powershell
$lnk = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Antigravity\Antigravity.lnk"
$s = (New-Object -ComObject WScript.Shell).CreateShortcut($lnk)
$s | Select-Object TargetPath,Arguments,IconLocation,WorkingDirectory
```

If `IconLocation` is empty or wrong, set it to the real executable:

```powershell
$s.IconLocation = 'E:\Program Files\Antigravity\Antigravity.exe,0'
$s.Save()
ie4uinit.exe -show
```

### Add a User-Level Shim for Paths With Spaces

Use this when logs show Codex calls an IDE `.cmd` under a path with spaces and it exits with code 1, but direct quoted execution works.

Choose a user PATH directory that appears before the real IDE path in `cmd.exe /d /c echo %PATH%`. Avoid protected directories. If `C:\Users\<user>\.dotnet\tools` is already in PATH before the IDE path, it is a practical reversible location.

Example for Antigravity:

```powershell
$dir = "$env:USERPROFILE\.dotnet\tools"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$shim = Join-Path $dir 'antigravity.cmd'
@('@echo off','"E:\Program Files\Antigravity\bin\antigravity.cmd" %*') |
  Set-Content -LiteralPath $shim -Encoding ASCII

cmd.exe /d /c where antigravity.cmd
cmd.exe /d /c antigravity.cmd --version
cmd.exe /d /c antigravity.cmd "D:\path\to\project"
```

Expected:

- `where` lists the shim before the original IDE path.
- `--version` exits `0`.
- Opening the project exits `0`.

If `WindowsApps` is in PATH but `cmd.exe /d /c where` ignores or cannot access a shim there, use another user-level PATH directory instead.

### If Codex Still Uses a Stale Absolute Path

After creating the shim, restart Codex and retry. Then re-check latest Codex logs. If errors still reference the original absolute path, Codex is caching that path.

Next steps:

1. Search Codex user config/state for the stale path.
2. Prefer changing the open target from the UI if available.
3. Only edit Codex config/state after backing up non-sensitive config files and confirming the exact key.
4. Do not edit SQLite state files unless there is no safer path.

## Validation Checklist

- `cmd.exe /d /c where <ide>.cmd` resolves to the intended command first.
- `cmd.exe /d /c <ide>.cmd --version` succeeds, if the IDE supports `--version`.
- `cmd.exe /d /c <ide>.cmd "<workspace>"` exits `0`.
- Codex latest log no longer contains new `Failed to open file` lines for that IDE after retry.
- The IDE opens the intended project, not a previous workspace.
- If icon was fixed, shortcut `IconLocation` points to the real executable.

## Rollback

Remove only the shim files you created:

```powershell
Remove-Item -LiteralPath "$env:USERPROFILE\.dotnet\tools\antigravity.cmd"
Remove-Item -LiteralPath "$env:LOCALAPPDATA\Microsoft\WindowsApps\antigravity.cmd"
```

Do not remove directories unless they were created solely for this fix and are empty.

## Final Report Format

Keep the final response short:

- Root cause evidence from Codex logs.
- Files or shortcuts changed.
- Commands used to validate.
- Whether Codex must be restarted.
- Any remaining risk, such as stale absolute-path cache.
