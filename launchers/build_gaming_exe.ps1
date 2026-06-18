# Build UtahVidia-Gaming.exe (Windows)
# Requires: pip install pyinstaller
# Output: dist/UtahVidia-Gaming.exe

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "Installing build dependencies..."
py -m pip install -e ".[dev]" -q
py -m pip install pyinstaller -q

Write-Host "Building UtahVidia-Gaming.exe (this may take several minutes)..."
py -m PyInstaller `
    --onefile `
    --name UtahVidia-Gaming `
    --console `
    --clean `
    --paths "$Root" `
    --hidden-import utahvidia `
    --hidden-import utahvidia.gaming_launcher `
    --hidden-import utahvidia.reality_engine `
    --hidden-import utahvidia.latency_shield `
    --hidden-import utahvidia.gaming_profiles `
    --collect-submodules utahvidia `
    "$Root\launchers\UtahVidia-Gaming.py"

Write-Host "Done: $Root\dist\UtahVidia-Gaming.exe"
Write-Host "Note: exe includes PyTorch and is large (~200MB+). Upload to GitHub Releases."
