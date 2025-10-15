# Yberion Launcher PyInstaller Spec-Datei für stabile EXE

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os

base_dir = os.getcwd()

exe_name = 'Yberion_Launcher'
script_file = 'yberion_launcher.py'

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

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False  # Keine zusätzliche Konsole
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name=exe_name
)
