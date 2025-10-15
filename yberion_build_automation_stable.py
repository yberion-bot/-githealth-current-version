# Yberion Build Automation Script - Stable Version
# Ziel: Stabile Ausführung ohne Heredoc, keine venv nötig, nur max 1 GUI-Fenster

import os
import subprocess

# ---------------------------
# Konfiguration
python_exe = r"C:\Users\schat\AppData\Local\Programs\Python\Python314\python.exe"
yberion_dir = r"C:\Users\schat\yberion"
spec_file = os.path.join(yberion_dir, 'yberion_launcher.spec')
launcher_py = os.path.join(yberion_dir, 'yberion_launcher.py')
dist_dir = os.path.join(yberion_dir, 'dist')

# ---------------------------
# Existenzprüfung der Launcher-Datei
if not os.path.isfile(launcher_py):
    print(f"FEHLER: '{launcher_py}' wurde nicht gefunden. Bitte sicherstellen, dass yberion_launcher.py im Verzeichnis vorhanden ist.")
    exit(1)

# ---------------------------
# Spec-Datei prüfen / erstellen
if not os.path.isfile(spec_file):
    print(f"Spec-Datei nicht gefunden, wird erstellt... {spec_file}")
    spec_content = """# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

# Minimal Spec für Yberion Launcher
# Automatisch generiert, psutil als hidden import
from PyInstaller.utils.hooks import collect_submodules
"""
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
else:
    print(f"Spec-Datei vorhanden: {spec_file}")

# ---------------------------
# Abhängigkeiten installieren
print("Installiere Abhängigkeiten...")
subprocess.run([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
subprocess.run([python_exe, '-m', 'pip', 'install', 'pyinstaller', 'psutil'], check=True)

# ---------------------------
# EXE bauen
print("Starte PyInstaller Build...")
try:
    subprocess.run([python_exe, '-m', 'PyInstaller', spec_file], check=True)
except subprocess.CalledProcessError:
    print("FEHLER: PyInstaller Build fehlgeschlagen.")
    exit(1)

print("Build abgeschlossen. Sandbox- und Live-Test kann nun erfolgen.")