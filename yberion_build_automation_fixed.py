# Bereinigte Version von yberion_build_automation.py
# Prüft nun direkt, ob yberion_launcher.py existiert, bevor PyInstaller ausgeführt wird

import os
import subprocess
import sys

# ---------------------------
# Variablen
base_dir = os.getcwd()
launcher_py = os.path.join(base_dir, 'yberion_launcher.py')
dist_dir = os.path.join(base_dir, 'dist')
spec_file = os.path.join(base_dir, 'yberion_launcher.spec')
python_exe = sys.executable  # aktuelles Python

# ---------------------------
# Prüfen, ob yberion_launcher.py existiert
if not os.path.exists(launcher_py):
    print(f"FEHLER: '{launcher_py}' wurde nicht gefunden. Bitte sicherstellen, dass yberion_launcher.py im Verzeichnis vorhanden ist.")
    sys.exit(1)

# ---------------------------
# Spec-Datei prüfen / erstellen
if not os.path.exists(spec_file):
    print('Spec-Datei nicht gefunden, wird erstellt...')
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

exe_name = 'Yberion_Launcher'
script_file = 'yberion_launcher.py'
base_dir = r'{base_dir}'

# Analysis
a = Analysis([
    script_file
],
    pathex=[base_dir],
    binaries=[],
    datas=[],
    hiddenimports=['psutil'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

# PYZ
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name=exe_name, debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=False)

# COLLECT
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name=exe_name)
"""
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
else:
    print(f'Spec-Datei vorhanden: {spec_file}')

# ---------------------------
# Abhängigkeiten installieren
print('Installiere Abhängigkeiten...')
subprocess.run([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
subprocess.run([python_exe, '-m', 'pip', 'install', 'pyinstaller', 'psutil'], check=True)

# ---------------------------
# EXE bauen
print('Starte PyInstaller Build...')
# Prüfen, ob Launcher-Skript existiert, bevor Build ausgeführt wird
if os.path.exists(launcher_py):
    subprocess.run([python_exe, '-m', 'PyInstaller', spec_file], check=True)
else:
    print(f"FEHLER: '{launcher_py}' fehlt, kann PyInstaller Build nicht starten.")
    sys.exit(1)

# ---------------------------
# Sandbox-Test
print('Sandbox-Test: SANDBOX_MODE=True')
with open(launcher_py, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('SANDBOX_MODE = False', 'SANDBOX_MODE = True')
with open(launcher_py, 'w', encoding='utf-8') as f:
    f.write(content)
subprocess.Popen([os.path.join(dist_dir, 'Yberion_Launcher.exe')])
print('Nur ein GUI-Fenster sollte erscheinen.')

# ---------------------------
# Live-Test
print('Live-Test: SANDBOX_MODE=False')
with open(launcher_py, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('SANDBOX_MODE = True', 'SANDBOX_MODE = False')
with open(launcher_py, 'w', encoding='utf-8') as f:
    f.write(content)
subprocess.Popen([os.path.join(dist_dir, 'Yberion_Launcher.exe')])
print('Task Manager prüfen: max. 1 Prozess pro Component')
