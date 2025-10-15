@echo off
REM ======================================================
REM Yberion Activator Starter (Git Bash)
REM ======================================================

REM --- Pfad zu Git Bash (anpassen, falls anders installiert) ---
SET GIT_BASH="C:\Program Files\Git\bin\bash.exe"

REM --- Pfad zu Yberion-Skript ---
SET SCRIPT_PATH="%USERPROFILE%\yberion\yberion_activator.sh"

REM --- Prüfen, ob Git Bash existiert ---
IF NOT EXIST %GIT_BASH% (
    echo Git Bash wurde nicht gefunden. Bitte installiere Git for Windows.
    pause
    exit /b 1
)

REM --- Prüfen, ob Skript existiert ---
IF NOT EXIST %SCRIPT_PATH% (
    echo Yberion-Skript wurde nicht gefunden: %SCRIPT_PATH%
    pause
    exit /b 1
)

REM --- Git Bash mit Skript starten ---
echo Starte Yberion Activator in Git Bash...
"%GIT_BASH%" --login -i "%SCRIPT_PATH%"

REM --- Ende ---
exit /b 0
