# Yberion — Windows-Sichere Launcher-Version (Automatische Pfaderkennung)

## Ziel
- Erzeuge eine `.exe` für Windows 11, die automatisch alle Daemons + Nexus GUI startet.
- Dynamische Pfaderkennung, keine manuellen BASE_DIR Anpassungen nötig.
- GUI bleibt immer sichtbar, Watchdog integriert.

---

## Launcher Skript: `yberion_launcher.py`
```python
import subprocess
import time
import os
import sys

# Dynamische Erkennung des Basisverzeichnisses (Verzeichnis des Launcher-Skripts)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOCKET_PATH = os.path.join(BASE_DIR, 'git-agent.sock')
DRAFT_DIR = os.path.join(BASE_DIR, 'work', 'junior')

# Starte Daemons
subprocess.Popen([sys.executable, os.path.join(BASE_DIR, 'agents', 'junior_daemon.py')])
subprocess.Popen([sys.executable, os.path.join(BASE_DIR, 'agents', 'senior_daemon.py')])
subprocess.Popen([sys.executable, os.path.join(BASE_DIR, 'agents', 'sentinel_daemon.py')])

# Starte Nexus Dashboard GUI
subprocess.Popen([sys.executable, os.path.join(BASE_DIR, 'dashboard', 'nexus_dashboard.py')])

# Watchdog Loop, falls GUI geschlossen wird
while True:
    time.sleep(10)
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        if 'nexus_dashboard.exe' not in result.stdout and 'nexus_dashboard.py' not in result.stdout:
            subprocess.Popen([sys.executable, os.path.join(BASE_DIR, 'dashboard', 'nexus_dashboard.py')])
    except Exception as e:
        # Optional: Logging hier hinzufügen
        pass
```

---

## 1️⃣ PyInstaller Build
1. Öffne `cmd` im Launcher-Ordner:
```cmd
cd C:\yberion_project\launcher
```
2. Führe aus:
```cmd
pyinstaller --onefile --windowed yberion_launcher.py --name yberion.exe
```
3. Ergebnis: `dist\yberion.exe` kann durch Doppelklick gestartet werden.

---

## 2️⃣ Vorteile
- Keine manuelle Pfadanpassung nötig.
- GUI wird automatisch gestartet und überwacht.
- Alle Daemons laufen im Hintergrund.
- Sichtbares Feedback für Nutzer, verhindert Missverständnisse über Malware.
- Einfach auf Windows 11 deploybar.

---

Jetzt kannst du die `.exe` direkt starten, Nexus + Daemons laufen automatisch, und die GUI bleibt immer sichtbar.