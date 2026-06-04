# Win10 Runtime Notes

## Observed Case

- Host OS: Windows 10 IoT Enterprise LTSC 2021, `10.0.19044`.
- Codex app path: `E:\Program Files\Codex\app\Codex.exe`.
- Codex CLI path: `E:\Program Files\Codex\app\resources\codex.exe`.
- Portable CLI version after MSIX unpack: `codex-cli 0.135.0-alpha.1`.
- Official MSIX identity observed: `OpenAI.Codex`, version `26.527.3686.0`, x64.
- `codex doctor` in the real `admin` context can be healthy while Workspace Dependencies are still missing.
- Running `codex doctor` in a sandbox user can falsely report missing auth/state because `CODEX_HOME` points at `C:\Users\CodexSandboxOffline\.codex`.

## Important Evidence Strings

Search `app.asar` or logs for:

```text
workspace_dependencies
settings.agent.dependencies
codex_primary_runtime_dependencies_diagnose
Codex Workspace dependencies are not supported on Windows 10.
codex-primary-runtime
```

Runtime installer behavior observed in bundled app code:

```text
Windows build threshold: 22621
Win10 below 22621: allow zip or tar.gz, reject tar.xz
Default runtime root: %USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime
```

Current runtime manifest observed on June 3, 2026:

```text
https://persistent.oaistatic.com/codex-primary-runtime/latest/win32-x64/LATEST.json
bundleVersion: 26.601.10930
archiveName: codex-primary-runtime-win32-x64-26.601.10930.tar.xz
format: tar.xz
nodeVersion: v24.14.0
pythonVersion: 3.12.13
```

## Failure Modes

### Win10 tar stalls

The built-in Win10 `tar.exe` may hang or produce no useful output on the runtime `.tar.xz`. Prefer Python `tarfile` with `r:xz`.

### Python tarfile hardlink failure

Naive `archive.extractall()` can fail on pnpm hardlinks:

```text
FileNotFoundError: ... .pnpm-workspace-state-v1.json
```

Use a two-phase extraction:

1. Write real directories and regular files.
2. Preserve existing real paths when symlink entries overlap them.
3. Process symlink entries.
4. Process hardlink entries.

### MAX_PATH failure

The pnpm layout can exceed 260 characters. Example:

```text
...\node_modules\.pnpm\@oai+artifact-tool@file+loc_...\node_modules\@oai\artifact-tool\node_modules\@oai\walnut\wasm\System.Runtime.InteropServices.JavaScript.o7o22a72it.wasm
```

Use short temp paths such as `E:\tmp\r\<8chars>` and `\\?\` path prefixes for Python file operations.

If `HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled` is locked at `0`, runtime discovery can still work after manual install, but deep package access should be smoke-tested.

## Validation Evidence

Healthy `load_workspace_dependencies` output includes:

```text
Workspace dependencies are available for this local desktop thread.
Bundle version: 26.601.10930
Node.js executable: C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe
Python executable: C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

Useful smoke tests:

```powershell
$env:NODE_PATH='C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' `
  -e "console.log(require.resolve('@oai/artifact-tool'))"

& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  -c "import openpyxl, docx, PIL; print('PY_IMPORTS_OK')"
```

Do not treat `require.resolve('@oai/artifact-tool/package.json')` failure as missing package; the package can intentionally block that subpath through `exports`.
