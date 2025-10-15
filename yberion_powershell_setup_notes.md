# Aktueller Stand und Vorgehensweise für Yberion Launcher unter Windows

## Aktueller Stand:
- `yberion_launcher.spec` existiert noch nicht → muss erstellt oder gespeichert werden.
- Virtuelle Umgebung (`venv`) konnte nicht erstellt werden, Python wird in PowerShell nicht erkannt.
- Pip-Pakete `pyinstaller` und `psutil` wurden erfolgreich installiert.
- Python ist über die Windows-App Installation verfügbar, daher muss der volle Pfad verwendet werden.

## Nächste Schritte:

1. **Python-Pfad prüfen**
- Finde den vollständigen Pfad zu Python:
```powershell
where python
```
- Beispieltypischer Pfad: `C:\Users\schat\AppData\Local\Microsoft\WindowsApps\python3.11.exe`

2. **Launcher-Spec-Datei erstellen**
- Öffne einen Texteditor und erstelle `yberion_launcher.spec` im Ordner `C:\Users\schat\yberion`.
- Füge die vorher erstellte Spec-Datei ein.

3. **EXE direkt bauen ohne virtuelle Umgebung**
- Nutze den vollständigen Python-Pfad:
```powershell
C:\Users\schat\AppData\Local\Microsoft\WindowsApps\python3.11.exe -m PyInstaller yberion_launcher.spec
```

4. **Sandbox-Test**
- Setze `SANDBOX_MODE=True` in `yberion_launcher.py`.
- Starte die EXE aus `dist\Yberion_Launcher.exe` → prüfe, dass nur ein Fenster erscheint.

5. **Live-Test**
- Setze `SANDBOX_MODE=False`.
- Starte EXE → Task Manager prüfen: max. 1 Prozess pro Component.

6. **Fehler-Logs prüfen**
- `githealth_dashboard.json` zeigt Status, Fehler oder fehlende Components.

## Hinweise:
- Virtuelle Umgebung ist optional, kann übersprungen werden, wenn Python direkt über den vollständigen Pfad aufgerufen wird.
- Spec-Datei muss im aktuellen Arbeitsverzeichnis liegen, sonst `PyInstaller` wirft "Spec file not found".
- EXE immer zuerst im Sandbox-Modus testen, bevor Live-Modus aktiviert wird.