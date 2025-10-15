# Yberion Launcher EXE sicher mit PyInstaller bauen

## Schritt-für-Schritt Anleitung für stabile EXE

### 1. Virtuelle Umgebung vorbereiten
```bash
python -m venv yberion_venv
# Linux/macOS
source yberion_venv/bin/activate
# Windows
yberion_venv\Scripts\activate
```

### 2. Abhängigkeiten installieren
```bash
pip install pyinstaller psutil
```

### 3. Launcher Script vorbereiten
- Nutze die letzte Version des Launchers (Live Mode) `yberion_launcher.py`
- Stelle sicher, dass alle Pfade korrekt sind

### 4. PyInstaller Build
```bash
pyinstaller --onefile --noconsole --name Yberion_Launcher yberion_launcher.py
```
- `--onefile` → alle Dateien in einer EXE
- `--noconsole` → keine zusätzliche Konsole öffnen
- `--name` → EXE Name

### 5. Optional: Hidden Imports
Falls Module nicht automatisch gefunden werden:
```bash
pyinstaller --onefile --noconsole --hidden-import=psutil yberion_launcher.py
```

### 6. Test in Sandbox
- Zunächst `SANDBOX_MODE=True` um zu prüfen, dass **kein Prozess übermäßig startet**
- Prüfen, dass **nur ein GUI-Fenster** sich öffnet und Status-Updates funktionieren

### 7. Live Test
- Setze `SANDBOX_MODE=False` und teste die EXE
- Prüfe im Task Manager → nur 1 Prozess pro Component wird gestartet

### 8. Fehlerbehandlung
- Bei Crash: logs aus `githealth_dashboard.json` prüfen
- Bei fehlgeschlagenen Starts → überprüfe Pfade oder Rechte

### 9. Optional: Auto-Update
- Dashboard kann Pfade und Versionen aktualisieren
- GUI informiert über neue Versionen und Status

**Vorteile dieser Vorgehensweise:**
- Nie mehr als 1 GUI geöffnet
- Subprocesses nur kontrolliert gestartet
- Windows bleibt stabil (kein WinError 1450)
- Produktionstaugliche EXE entsteht

