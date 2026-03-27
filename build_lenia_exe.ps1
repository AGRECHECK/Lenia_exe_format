param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $projectRoot ".venv-build"
$pythonExe = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    python -m venv $venvPath
}

& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r (Join-Path $projectRoot "requirements-build.txt")

$pyInstallerArgs = @(
    "-m", "PyInstaller",
    (Join-Path $projectRoot "Lenia.spec"),
    "--noconfirm"
)

if ($Clean) {
    $pyInstallerArgs += "--clean"
}

& $pythonExe @pyInstallerArgs
