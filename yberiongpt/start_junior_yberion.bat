@echo off
REM ==============================
REM Junior Yberion Auto-Start Batch
REM ==============================

REM Path to Python executable (adjust if needed)
set PYTHON_EXE=C:\Users\schat\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe

REM Path to your Python script
set SCRIPT=junior_yberion_backloop.py

echo Starting Junior Yberion...
"%PYTHON_EXE%" "%SCRIPT%"

echo.
echo Done! Press any key to exit...
pause >nul
