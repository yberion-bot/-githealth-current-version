@echo off
setlocal

set APP_NAME=Yberion
set VERSION=2.1
set ENTRY=yberion.py
set BUILD_DIR=build
set DIST_DIR=dist

echo [Yberion] Cleaning old builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q %APP_NAME%_installer_%VERSION%.exe 2>nul

echo [Yberion] Installing PyInstaller (if missing)...
pip install pyinstaller

echo [Yberion] Building standalone exe...
pyinstaller --noconfirm --onefile --name "%APP_NAME%" "%ENTRY%"

if %errorlevel% neq 0 (
  echo Build failed.
  exit /b 1
)

echo [Yberion] Preparing installer folder...
mkdir "%BUILD_DIR%"
copy "%DIST_DIR%\%APP_NAME%.exe" "%BUILD_DIR%\" /y
if exist LICENSE copy LICENSE "%BUILD_DIR%\" /y
if exist README.md copy README.md "%BUILD_DIR%\" /y

echo [Yberion] Compiling Inno Setup installer...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "yberion_installer.iss"

if %errorlevel% neq 0 (
  echo Inno Setup failed.
  exit /b 1
)

echo [Yberion] Done. Installer created: %APP_NAME%_installer_%VERSION%.exe
endlocal
pause
