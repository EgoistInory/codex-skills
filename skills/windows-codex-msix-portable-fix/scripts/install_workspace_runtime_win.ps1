param(
    [string]$ArchivePath = "E:\tmp\codex-primary-runtime-win32-x64-26.601.10930.tar.xz",
    [string]$InstallParent = "C:\Users\admin\.cache\codex-runtimes"
)

$ErrorActionPreference = "Stop"

$ArchiveUrl = "https://persistent.oaistatic.com/codex-primary-runtime/26.601.10930/codex-primary-runtime-win32-x64-26.601.10930.tar.xz"
$ExpectedSha256 = "e8fa1db179a2d2e62e372f81b4dac25117680491fc2b819bce81d4910578ef1c"
$RuntimeDirName = "codex-primary-runtime"
$BundleVersion = "26.601.10930"

function Get-FileSha256([string]$Path) {
    (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Assert-UnderDirectory([string]$Path, [string]$Root) {
    $resolvedPath = [System.IO.Path]::GetFullPath($Path)
    $resolvedRoot = [System.IO.Path]::GetFullPath($Root)
    if (-not $resolvedPath.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to operate outside expected root. Path=$resolvedPath Root=$resolvedRoot"
    }
}

$archiveDir = Split-Path -Parent $ArchivePath
New-Item -ItemType Directory -Force -Path $archiveDir | Out-Null

if (-not (Test-Path -LiteralPath $ArchivePath) -or (Get-FileSha256 $ArchivePath) -ne $ExpectedSha256) {
    Write-Host "Downloading Codex workspace runtime $BundleVersion..."
    Invoke-WebRequest -UseBasicParsing -Uri $ArchiveUrl -OutFile $ArchivePath
}

$actualSha256 = Get-FileSha256 $ArchivePath
if ($actualSha256 -ne $ExpectedSha256) {
    throw "SHA256 mismatch. Expected $ExpectedSha256 but got $actualSha256"
}

$shortId = [guid]::NewGuid().ToString("N").Substring(0, 8)
$tempRoot = Join-Path "E:\tmp\r" $shortId
$payloadDir = Join-Path $tempRoot "payload"
New-Item -ItemType Directory -Force -Path $payloadDir | Out-Null

$completed = $false
try {
    Write-Host "Extracting runtime archive..."
    $extractScript = Join-Path $tempRoot "extract_runtime.py"
    @'
import os
import shutil
import sys
import tarfile

archive_path, extract_dir = sys.argv[1], sys.argv[2]
root = os.path.abspath(extract_dir)

def safe_join(base, *parts):
    target = os.path.abspath(os.path.join(base, *parts))
    if target != base and not target.startswith(base + os.sep):
        raise RuntimeError(f"Refusing to extract outside target: {parts}")
    return target

def fs_path(path):
    path = os.path.abspath(path)
    if os.name != "nt":
        return path
    if path.startswith("\\\\?\\"):
        return path
    if path.startswith("\\\\"):
        return "\\\\?\\UNC\\" + path[2:]
    return "\\\\?\\" + path

def link_source(member, target_path):
    link_name = member.linkname.replace("/", os.sep)
    if os.path.isabs(link_name):
        return safe_join(root, link_name.lstrip("\\/"))
    return safe_join(os.path.dirname(target_path), link_name)

def copy_or_link_file(source, target):
    os.makedirs(fs_path(os.path.dirname(target)), exist_ok=True)
    if os.path.exists(fs_path(target)):
        os.unlink(fs_path(target))
    try:
        os.link(fs_path(source), fs_path(target))
    except OSError:
        shutil.copy2(fs_path(source), fs_path(target))

with tarfile.open(archive_path, "r:xz") as archive:
    members = archive.getmembers()
    for member in members:
        safe_join(root, member.name)
        if member.islnk() or member.issym():
            link_source(member, safe_join(root, member.name))

    for member in members:
        if member.islnk() or member.issym():
            continue
        if member.isdev():
            continue
        target = safe_join(root, member.name)
        if member.isdir():
            os.makedirs(fs_path(target), exist_ok=True)
        elif member.isfile():
            os.makedirs(fs_path(os.path.dirname(target)), exist_ok=True)
            source_file = archive.extractfile(member)
            if source_file is None:
                raise RuntimeError(f"Failed to read archive member: {member.name}")
            with source_file, open(fs_path(target), "wb") as target_file:
                shutil.copyfileobj(source_file, target_file)

    for member in members:
        if not member.issym():
            continue
        target = safe_join(root, member.name)
        source = link_source(member, target)
        os.makedirs(fs_path(os.path.dirname(target)), exist_ok=True)
        if os.path.exists(fs_path(target)):
            continue
        try:
            os.symlink(member.linkname, fs_path(target), target_is_directory=os.path.isdir(fs_path(source)))
        except OSError:
            if os.path.isdir(fs_path(source)):
                shutil.copytree(fs_path(source), fs_path(target), dirs_exist_ok=True)
            elif os.path.exists(fs_path(source)):
                shutil.copy2(fs_path(source), fs_path(target))

    for member in members:
        if not member.islnk():
            continue
        target = safe_join(root, member.name)
        source = safe_join(root, member.linkname.replace("/", os.sep))
        if os.path.isdir(fs_path(source)):
            shutil.copytree(fs_path(source), fs_path(target), dirs_exist_ok=True)
        else:
            copy_or_link_file(source, target)
'@ | Set-Content -LiteralPath $extractScript -Encoding ASCII

    py -3 $extractScript $ArchivePath $payloadDir
    if ($LASTEXITCODE -ne 0) {
        throw "Python tar.xz extraction failed with exit code $LASTEXITCODE"
    }

    $extractedRoot = Join-Path $payloadDir $RuntimeDirName
    $runtimeJson = Join-Path $extractedRoot "runtime.json"
    $nodeExe = Join-Path $extractedRoot "dependencies\node\bin\node.exe"
    $pythonExe = Join-Path $extractedRoot "dependencies\python\python.exe"

    foreach ($required in @($runtimeJson, $nodeExe, $pythonExe)) {
        if (-not (Test-Path -LiteralPath $required)) {
            throw "Extracted runtime is incomplete. Missing: $required"
        }
    }

    New-Item -ItemType Directory -Force -Path $InstallParent | Out-Null
    $target = Join-Path $InstallParent $RuntimeDirName
    Assert-UnderDirectory $target $InstallParent

    if (Test-Path -LiteralPath $target) {
        $backup = Join-Path $InstallParent ($RuntimeDirName + ".previous-manual-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
        Assert-UnderDirectory $backup $InstallParent
        Rename-Item -LiteralPath $target -NewName (Split-Path -Leaf $backup)
        Write-Host "Previous runtime backed up to: $backup"
    }

    $copyScript = Join-Path $tempRoot "copy_runtime.py"
    @'
import os
import shutil
import sys

source, target = sys.argv[1], sys.argv[2]

def fs_path(path):
    path = os.path.abspath(path)
    if os.name != "nt":
        return path
    if path.startswith("\\\\?\\"):
        return path
    if path.startswith("\\\\"):
        return "\\\\?\\UNC\\" + path[2:]
    return "\\\\?\\" + path

if os.path.exists(fs_path(target)):
    raise RuntimeError(f"Target already exists: {target}")

shutil.copytree(fs_path(source), fs_path(target), symlinks=True)
'@ | Set-Content -LiteralPath $copyScript -Encoding ASCII

    py -3 $copyScript $extractedRoot $target
    if ($LASTEXITCODE -ne 0) {
        throw "Python runtime copy failed with exit code $LASTEXITCODE"
    }

    & (Join-Path $target "dependencies\node\bin\node.exe") --version
    & (Join-Path $target "dependencies\python\python.exe") --version
    Write-Host "Installed Codex workspace runtime $BundleVersion to: $target"
    $completed = $true
}
finally {
    if (Test-Path -LiteralPath $tempRoot) {
        Assert-UnderDirectory $tempRoot "E:\tmp"
        if ($completed) {
            py -3 -c "import os, shutil, stat, sys; p=os.path.abspath(sys.argv[1]); p='\\\\?\\' + p if os.name == 'nt' and not p.startswith('\\\\?\\') else p; exec('def onerror(func, path, exc_info):\n    os.chmod(path, stat.S_IWRITE)\n    func(path)'); shutil.rmtree(p, onerror=onerror)" $tempRoot
        } else {
            Write-Host "Preserving failed temp directory for inspection: $tempRoot"
        }
    }
}
