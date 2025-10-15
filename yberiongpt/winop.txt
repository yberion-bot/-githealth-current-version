@echo off
title Ultimate Windows 11 Optimizer
color 0a

echo ---- Starting Windows 11 Ultimate Optimization ----

:: 1. Set High Performance Power Plan
echo [1/7] Setting High Performance Power Plan...
powercfg -setactive SCHEME_MIN

:: 2. Clean Temporary Files
echo [2/7] Cleaning temporary files...
del /q/f/s "%TEMP%\*" >nul 2>&1
del /q/f/s "C:\Windows\Temp\*" >nul 2>&1

:: 3. Optimize C: drive (Trim SSD)
echo [3/7] Optimizing C: drive (Trim SSD)...
defrag C: /L /O >nul

:: 4. Disable Startup Items in Startup Folder
echo [4/7] Removing unnecessary startup items...
set startup="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if exist %startup% (
    for %%f in (%startup%\*) do (
        del /q "%%f" >nul 2>&1
    )
)

:: 5. Adjust Visual Effects for Best Performance
echo [5/7] Adjusting visual effects...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f >nul

:: 6. Disable Widgets
echo [6/7] Disabling Widgets...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v TaskbarDa /t REG_DWORD /d 0 /f >nul

:: 7. Disable Snap Assist / Snap Layout Animations
echo [7/7] Disabling Snap Assist animations...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v DisablePreviewDesktop /t REG_DWORD /d 1 /f >nul

:: 8. Disable safe unnecessary background services
echo Disabling unnecessary services...
sc config XblGameSave start= disabled
net stop XblGameSave
sc config OneSyncSvc start= disabled
net stop OneSyncSvc
sc config WaaSMedicSvc start= disabled
net stop WaaSMedicSvc

echo ---- Ultimate Optimization Complete! ----
echo Please restart your computer for all changes to take effect.
pause
