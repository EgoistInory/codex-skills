---
name: windows-codex-msix-portable-fix
description: Diagnose and repair Codex Desktop on restricted Windows 10 machines where Microsoft Store, App Installer, or MSIX launch is blocked, Codex is run from an unpacked portable directory, or Workspace Dependencies and dependency diagnostics fail because the primary runtime is missing or unsupported.
---

# Windows Codex MSIX Portable Fix

Use this skill for restricted Windows installs where the official Codex MSIX installs poorly, cannot launch, or the unpacked/portable Codex app works but Workspace Dependencies and dependency diagnostics do not.

## Safety

- Do not change `C:\Program Files\WindowsApps` ACLs.
- Do not delete `C:\Users\<user>\.codex`; it contains user state, auth, sessions, plugins, and config.
- Do not overwrite a running Codex install. If replacing a portable app directory, create a timestamped backup first and require Codex to be closed.
- Do not expose tokens from `auth.json`, logs, cookies, or browser state.
- Prefer user-cache runtime repair over system-wide policy edits.
- Treat registry edits, Store policy changes, and process termination as approval-required operations.

## Fast Diagnosis

1. Confirm the running user and install context:

```powershell
whoami
Get-Process | Where-Object { $_.ProcessName -like '*Codex*' -or $_.Path -like '*Codex*' } |
  Select-Object ProcessName,Id,Path
& 'E:\Program Files\Codex\app\resources\codex.exe' --version
```

2. Verify the MSIX package if available:

```powershell
Get-AuthenticodeSignature -LiteralPath 'C:\Users\admin\Downloads\codex-*.msix' |
  Select-Object Status,StatusMessage,SignerCertificate
```

3. Check whether the portable app itself is consistent:

```powershell
& 'E:\Program Files\Codex\app\resources\codex.exe' doctor --summary --ascii --no-color
```

Run this in the real user context when Codex is elevated or sandboxed; otherwise `CODEX_HOME` may point at a sandbox user and produce false auth/state failures.

4. Check Workspace Dependencies from inside Codex when available:

```text
Use the app-provided load_workspace_dependencies tool.
```

Expected healthy output includes a bundle version, Node path, Node packages path, Python path, and Python packages path.

## Root Cause Pattern

On Windows 10 LTSC / build `10.0.19044`, Codex may run as an unpacked app but fail Workspace Dependencies because the primary runtime is absent. Current runtime manifests may publish a Windows x64 archive as `tar.xz`.

Codex runtime installer logic allows Windows builds below `22621` only when the archive format is `zip` or `tar.gz`; `tar.xz` is treated as unsupported on Windows 10. The app may therefore show dependency repair/diagnose failures even though the portable Codex binary itself works.

Read [references/win10-runtime-notes.md](references/win10-runtime-notes.md) when you need implementation details, evidence strings, or validation examples.

## Repair Workflow

1. Prefer the official route first:
   - Microsoft Store / App Installer MSIX.
   - Enterprise deployment through Intune, Company Portal, SCCM, or an administrator.

2. If Store/MSIX launch is blocked but the unpacked Codex app runs:
   - Keep the portable app directory, such as `E:\Program Files\Codex`.
   - Repair the primary runtime in the user cache.
   - Do not modify `WindowsApps`.

3. Install the runtime manually with the bundled script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_workspace_runtime_win.ps1
```

The script is designed for the known Win10 `tar.xz` failure mode. It:

- Downloads the official runtime archive.
- Verifies SHA256.
- Extracts `.tar.xz` with Python instead of Win10 `tar`.
- Handles pnpm symlink/hardlink layout.
- Uses short temp paths and `\\?\` long-path prefixes.
- Installs to `C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime`.
- Backs up an existing runtime directory before replacing it.

If using a non-`admin` Windows user, pass that user's cache path:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_workspace_runtime_win.ps1 `
  -InstallParent 'C:\Users\<user>\.cache\codex-runtimes'
```

## Validation

After repair, verify:

```powershell
Get-Content -LiteralPath 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\runtime.json'
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' --version
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' --version
```

Then verify dependency discovery from Codex:

```text
load_workspace_dependencies should report:
- Bundle version
- Node.js executable
- Node.js packages
- Python executable
- Python packages
```

Optional runtime smoke tests:

```powershell
$env:NODE_PATH='C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' `
  -e "console.log(require.resolve('@oai/artifact-tool'))"

& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  -c "import openpyxl, docx, PIL; print('PY_IMPORTS_OK')"
```

## If It Still Fails

- Restart Codex after runtime installation.
- Confirm the real user, not a sandbox user, owns the cache path.
- Confirm `runtime.json` exists directly under `codex-primary-runtime`.
- Confirm `LongPathsEnabled` is not required for discovery; if deep package access still fails and registry edits are blocked, recommend Windows 11 or enterprise policy support.
- If the Settings page still fails but `load_workspace_dependencies` succeeds, report this as a UI cache/restart issue first.

## Final Report

Keep the final response short:

- Root cause: Store/MSIX policy, portable install, Win10 runtime format, or user-context mismatch.
- Files or directories changed.
- Runtime bundle version installed.
- Validation commands and results.
- Whether Codex restart is needed.
