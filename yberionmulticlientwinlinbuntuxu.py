# ultra_dev_server.py
import os, sys, subprocess, threading, time, asyncio, webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path
import websockets

# ---------------- Konfiguration ----------------
PORT = 8000
WS_PORT = 8765
DASHBOARD_DIR = r"C:\Users\<DeinUser>\yberion_full_package\dashboard"  # anpassen
SRC_DIR = os.path.join(DASHBOARD_DIR, "src")
BUILD_DIR = os.path.join(DASHBOARD_DIR, "build")
POLL_INTERVAL = 1  # Sekunden
AUTO_OPEN_BROWSER = True
# -----------------------------------------------

# ---------------- Logging ----------------
def log_info(msg): print(f"\033[94m[Yberion] {msg}\033[0m")
def log_success(msg): print(f"\033[92m[Yberion] {msg}\033[0m")
def log_warn(msg): print(f"\033[93m[Yberion] {msg}\033[0m")
def log_error(msg): print(f"\033[91m[Yberion] {msg}\033[0m")

# ---------------- Build ----------------
build_error_msg = ""

def build_dashboard():
    global build_error_msg
    log_info("Starte Build...")
    try:
        subprocess.check_call(["npm", "install"], cwd=DASHBOARD_DIR)
        subprocess.check_call(["npm", "run", "build"], cwd=DASHBOARD_DIR)
        log_success("Dashboard erfolgreich gebaut!")
        build_error_msg = ""
    except FileNotFoundError:
        build_error_msg = "npm nicht gefunden. Bitte Node.js installieren."
        log_error(build_error_msg)
    except subprocess.CalledProcessError as e:
        build_error_msg = f"Build fehlgeschlagen: {e}"
        log_error(build_error_msg)

# Initial Build
if not os.path.exists(BUILD_DIR):
    build_dashboard()

os.chdir(BUILD_DIR)

# ---------------- HTTP Server ----------------
def start_http():
    server = HTTPServer(("", PORT), SimpleHTTPRequestHandler)
    log_info(f"HTTP Server läuft unter http://localhost:{PORT}")
    server.serve_forever()

threading.Thread(target=start_http, daemon=True).start()

# ---------------- Browser ----------------
if AUTO_OPEN_BROWSER:
    webbrowser.open(f"http://localhost:{PORT}")

# ---------------- WebSocket Live-Reload ----------------
connected_clients = set()
last_build_mtime = {}
last_src_mtime = {}

async def ws_handler(websocket, path):
    connected_clients.add(websocket)
    # Sende initiale Fehler (falls Build fehlgeschlagen)
    if build_error_msg:
        await websocket.send(f"error:{build_error_msg}")
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def watch_files():
    while True:
        rebuild_needed = False
        # src Änderungen prüfen
        for path in Path(SRC_DIR).rglob("*.*"):
            try:
                mtime = path.stat().st_mtime
            except FileNotFoundError:
                continue
            if path not in last_src_mtime or last_src_mtime[path] != mtime:
                last_src_mtime[path] = mtime
                rebuild_needed = True

        if rebuild_needed:
            log_warn("Änderungen in src erkannt – führe Build aus")
            build_dashboard()

        # build Änderungen prüfen
        reload_needed = False
        for path in Path(BUILD_DIR).rglob("*.*"):
            try:
                mtime = path.stat().st_mtime
            except FileNotFoundError:
                continue
            if path not in last_build_mtime or last_build_mtime[path] != mtime:
                last_build_mtime[path] = mtime
                reload_needed = True

        if reload_needed and connected_clients:
            # Fehler oder Reload
            for client in connected_clients:
                if build_error_msg:
                    await client.send(f"error:{build_error_msg}")
                else:
                    ext = path.suffix.lower()
                    if ext == ".css":
                        await client.send(f"hmr:{path.name}")
                    else:
                        await client.send("reload")
            log_info("Browser aktualisiert (reload/hmr)")

        await asyncio.sleep(POLL_INTERVAL)

async def main():
    ws_server = await websockets.serve(ws_handler, "localhost", WS_PORT)
    log_info(f"WebSocket Live-Reload Server läuft auf ws://localhost:{WS_PORT}")
    await watch_files()

def start_ws():
    asyncio.run(main())

threading.Thread(target=start_ws, daemon=True).start()

# ---------------- HTML Hinweis ----------------
log_info(f"""
Füge in deine index.html kurz vor </body> folgenden Code ein:

<script>
const ws = new WebSocket("ws://localhost:{WS_PORT}");
ws.onmessage = event => {{
    if(event.data.startsWith("reload")) window.location.reload();
    else if(event.data.startsWith("hmr:")) {{
        const file = event.data.split(":")[1];
        const links = document.querySelectorAll("link[rel=stylesheet]");
        links.forEach(link => {{
            if(link.href.includes(file)) {{
                const href = link.href.split("?")[0] + "?t=" + Date.now();
                link.href = href;
            }}
        }});
    }}
    else if(event.data.startsWith("error:")) {{
        let overlay = document.getElementById("yberion-error-overlay");
        if(!overlay) {{
            overlay = document.createElement("div");
            overlay.id = "yberion-error-overlay";
            overlay.style.position = "fixed";
            overlay.style.top = "0"; overlay.style.left = "0";
            overlay.style.width = "100%"; overlay.style.height = "100%";
            overlay.style.backgroundColor = "rgba(255,0,0,0.9)";
            overlay.style.color = "white"; overlay.style.fontSize = "18px";
            overlay.style.padding = "20px"; overlay.style.zIndex = "9999";
            document.body.appendChild(overlay);
        }}
        overlay.innerText = event.data.substring(6);
    }}
}};
</script>
""")

# ---------------- Hauptschleife ----------------
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    log_warn("Ultra Dev-Server gestoppt")
