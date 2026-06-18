@echo off
title Utah-Vid-ia Gaming Unlock
echo.
echo  Utah-Vid-ia Gaming Unlock (requires Python 3.10+)
echo  No Git required - installs from this folder via pip
echo.

where py >nul 2>&1
if %ERRORLEVEL%==0 (
    set PY=py
) else (
    set PY=python
)

%PY% --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found. Install Python from https://python.org
    echo Or download UtahVidia-Gaming.exe from GitHub Releases instead.
    pause
    exit /b 1
)

cd /d "%~dp0.."
echo Installing Utah-Vid-ia from local folder...
%PY% -m pip install -e ".[dev]" -q
if %ERRORLEVEL% neq 0 (
    echo pip install failed.
    pause
    exit /b 1
)

echo.
%PY% -m utahvidia.gaming_launcher
pause
