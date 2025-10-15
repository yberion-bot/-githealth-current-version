# Yberion Build Automation Script (Healed Version)
# Purpose: Build the Yberion Launcher EXE safely, with one GUI max, without venv

import os
import subprocess

# ---------------------------
# Config
python_exe = r"C:\Users\schat\AppData\Local\Programs\Python\Python314\python.exe"
yberion_dir = r"C:\Users\schat\yberion"
spec_file = os.path.join(yberion_dir, 'yberion_launcher.spec')
launcher_py = os.path.join(yberion_dir, 'yberion_launcher.py')
dist_dir = os.path.join(yberion_dir, 'dist')

# ---------------------------
# Check if launcher exists
if not os.path.isfile(launcher_py):
    print(f"FEHLER: '{launcher_py}' wurde nicht gefunden. Bitte sicherstellen, dass yberion_launcher.py im Verzeichnis vorhanden ist.")
    exit(1)

# ---------------------------
# Check / create spec file
if not os.path.isfile(spec_file):
    print(f"Spec-Datei nicht gefunden, wird erstellt... {spec_file}")
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

from PyInstaller.utils.hooks import collect_submodules

# Spec content for Yberion Launcher
# auto-generated minimal spec

# You can add additional hooks here
"""
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
else:
    print(f"Spec-Datei vorhanden: {spec_file}")

# ---------------------------
# Install dependencies
print("Installiere Abhängigkeiten...")
subprocess.run([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
subprocess.run([python_exe, '-m', 'pip', 'install', 'pyinstaller', 'psutil'], check=True)

# ---------------------------
# Build EXE
print("Starte PyInstaller Build...")
try:
    subprocess.run([python_exe, '-m', 'PyInstaller', spec_file], check=True)
except subprocess.CalledProcessError:
    print("FEHLER: PyInstaller Build fehlgeschlagen.")
    exit(1)

print("Build abgeschlossen. Sandbox- und Live-Test kann nun erfolgen.")