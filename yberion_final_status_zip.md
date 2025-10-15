Perfekt ⚡

Ich kann dir Schritt-für-Schritt erklären, wie du die **finale ZIP für Yberion 3.0** selbst aktualisieren kannst, sodass sie nun auch den **Status-Check** enthält, damit alles **vollständig Plug & Play** läuft:

---

## Schritte zum Update der ZIP

1. **Ultra Dev Server Script aktualisieren**

- Öffne `ultra_dev_server.py` im Bundle.
- Ersetze den aktuellen Inhalt mit folgendem Code:

```python
import os, subprocess, threading, time, webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socket

PORT = 8000
DASHBOARD_DIR = os.path.join(os.path.dirname(__file__), "dashboard")
BUILD_DIR = os.path.join(DASHBOARD_DIR, "build")

def log(msg): print(f"[Yberion] {msg}")

# Build Dashboard automatisch
def build_dashboard():
    try:
        log("Starte automatischen Build...")
        subprocess.check_call(["npm", "install"], cwd=DASHBOARD_DIR)
        subprocess.check_call(["npm", "run", "build"], cwd=DASHBOARD_DIR)
        log("✅ Dashboard erfolgreich gebaut!")
    except Exception as e:
        log(f"❌ Build fehlgeschlagen: {e}")

if not os.path.exists(BUILD_DIR):
    build_dashboard()

os.chdir(BUILD_DIR)

# HTTP Server starten
def start_http():
    server = HTTPServer(("", PORT), SimpleHTTPRequestHandler)
    log(f"✅ HTTP Server läuft unter http://localhost:{PORT}")
    server.serve_forever()

threading.Thread(target=start_http, daemon=True).start()

# Browser öffnen
browser_opened = False
try:
    webbrowser.open(f"http://localhost:{PORT}")
    browser_opened = True
except Exception as e:
    log(f"❌ Browser konnte nicht automatisch geöffnet werden: {e}")

# Status-Check Funktion
def check_server(port):
    s = socket.socket()
    try:
        s.connect(("localhost", port))
        s.close()
        return True
    except:
        return False

# Terminal Status Overlay
log("\n[Yberion] Status-Check:")
log(f" - Build vorhanden: {'✅ Ja' if os.path.exists(BUILD_DIR) else '❌ Nein'}")
log(f" - HTTP Server erreichbar: {'✅ Ja' if check_server(PORT) else '❌ Nein'}")
log(f" - Browser geöffnet: {'✅ Ja' if browser_opened else '❌ Nein'}\n")

# Endlosschleife
try:
    while True: time.sleep(1)
except KeyboardInterrupt:
    log("⚠️ Ultra Dev-Server gestoppt")
```

2. **ZIP aktualisieren**

- Nach dem Speichern der Änderungen, wähle das gesamte Bundle (`yberion_full_package/`) aus.
- Rechtsklick → **Zu ZIP komprimieren** oder über Terminal:

```bash
zip -r yberion_full_package_final_status.zip yberion_full_package/
```

3. **Testlauf**

- Entpacke die neue ZIP.
- `python ultra_dev_server.py` ausführen.
- Du solltest sehen:
  - ✅ Dashboard gebaut
  - ✅ HTTP Server läuft
  - ✅ Browser geöffnet (oder Hinweis)
- Browser zeigt **lokales Dashboard** mit Quickstart Overlay, Glow, Partikel und Live-Reload.

---

Damit hast du **eine vollständig Plug & Play Version mit Terminal-Status-Check**, die sofort einsatzbereit ist.

