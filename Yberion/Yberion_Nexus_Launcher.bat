@echo off
title Yberion Nexus Autoupdater
color 0A
echo ============================================
echo        YBERION NEXUS AUTORUN INITIALIZED
echo ============================================
echo.

:: Change to the Yberion Nexus directory
cd /d "%~dp0"

:: Verify Git installation
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git not found. Please install Git for Windows:
    echo https://git-scm.com/download/win
    pause
    exit /b
)

:: Run the Nexus health check
echo [Yberion] Checking git health and synchronizing...
bash scripts/githealth_nexus.sh

:: Launch the live dashboard (in new window)
echo [Yberion] Launching live dashboard...
start bash scripts/githealth_dashboard.sh

echo.
echo [Yberion] Nexus initialized successfully.
echo Press any key to exit this launcher window.
pause >nul
exit
