@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: -------------------------------
:: Automatische Bash-Erkennung
:: -------------------------------

:: Standard MSYS2 Pfade (in Anführungszeichen, falls Leerzeichen)
SET MSYS_PATHS="C:\msys64\usr\bin" "C:\msys64\mingw64\bin" "C:\MinGW\msys\1.0\bin"

SET "FOUND_BASH="
FOR %%P IN (%MSYS_PATHS%) DO (
    IF EXIST "%%~P\bash.exe" (
        SET "FOUND_BASH=%%~P\bash.exe"
        GOTO :FOUND
    )
)

:FOUND
IF "%FOUND_BASH%"=="" (
    ECHO Fehler: Bash unter MSYS2/MinGW64 nicht gefunden!
    ECHO Stelle sicher, dass MSYS2 / MinGW64 installiert ist.
    PAUSE
    EXIT /B 1
) ELSE (
    ECHO Bash gefunden: "%FOUND_BASH%"
)

:: -------------------------------
:: Starte Yberion Bash Script
:: -------------------------------
SET "YBERION_SCRIPT=%~dp0yberion_multiactor.sh"

IF NOT EXIST "%YBERION_SCRIPT%" (
    ECHO Fehler: Yberion Script nicht gefunden!
    PAUSE
    EXIT /B 1
)

:: Starte Bash mit Skript
"%FOUND_BASH%" "%YBERION_SCRIPT%"
