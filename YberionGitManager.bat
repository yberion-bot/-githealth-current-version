@echo off
:: ==========================================================
::  YBERION GIT MANAGER LAUNCHER for Windows 11 (Auto HTML Open, Fixed Fetch)
:: ==========================================================

set SCRIPT_PATH=%~dp0yberion_multi_branch_manager.py
set HTML_REPORT=%~dp0yberion_githealth.html

echo ==========================================================
echo  🔹  YBERION MULTI-BRANCH MANAGER LAUNCHER
echo ==========================================================
echo.

cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo ⚠️  Python not found in PATH. Please install Python 3.
    pause
    exit /b
)

echo 🚀 Running Yberion Git Manager ...
python "%SCRIPT_PATH%" --create-pr
echo.

if exist "%HTML_REPORT%" (
    echo 🌐 Opening report in browser...
    start "" "%HTML_REPORT%"
) else (
    echo ⚠️  No HTML report found.
)

echo ==========================================================
echo ✅  YBERION WORKFLOW COMPLETED
echo ==========================================================
pause
