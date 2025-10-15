import os
import sys
import subprocess
import time
import json

# --- BASE DIR ---
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

# --- PATHS ---
NEXUS_EXE = os.path.join(BASE_DIR, "Yberion_Nexus.exe")
CONTROLLER = os.path.join(BASE_DIR, "yberion_controller.py")
LOG_FILE = os.path.join(BASE_DIR, "yberion_nexus.log")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
GITHEALTH_SCRIPT = os.path.join(SCRIPTS_DIR, "githealth_nexus.sh")
DASHBOARD_SCRIPT = os.path.join(SCRIPTS_DIR, "githealth_dashboard.sh")
DASHBOARD_JSON = os.path.join(DASHBOARD_DIR, "githealth_dashboard.json")

PYTHON_EXE = sys.executable

# --- ENSURE DIRECTORIES EXIST ---
os.makedirs(SCRIPTS_DIR, exist_ok=True)
os.makedirs(DASHBOARD_DIR, exist_ok=True)

# --- INIT DASHBOARD JSON IF MISSING ---
if not os.path.isfile(DASHBOARD_JSON):
    initial_dashboard = {
        "local_hash": "",
        "remote_hash": "",
        "account_wide": False,
        "ssh_enabled": False,
        "git_push_enabled": False,
        "divergence": False,
        "last_backup": "",
        "update_status": "pending",
        "self_healing_enabled": True,
        "patchnodes": []
    }
    with open(DASHBOARD_JSON, "w") as f:
        json.dump(initial_dashboard, f, indent=2)
    print(f"[Yberion] Initialized dashboard JSON at {DASHBOARD_JSON}")

# --- KILL OLD NEXUS ---
subprocess.run(["taskkill", "/f", "/im", "Yberion_Nexus.exe"],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# --- LAUNCH NEXUS EXE ---
if os.path.isfile(NEXUS_EXE):
    subprocess.Popen([NEXUS_EXE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[Yberion] Nexus EXE launched: {NEXUS_EXE}")
else:
    print(f"[Yberion] ERROR: Nexus EXE not found at {NEXUS_EXE}")

# --- LAUNCH CONTROLLER ---
if os.path.isfile(CONTROLLER):
    with open(LOG_FILE, "a") as log:
        subprocess.Popen([PYTHON_EXE, CONTROLLER], stdout=log, stderr=log)
    print(f"[Yberion] Controller launched: {CONTROLLER}")
else:
    print(f"[Yberion] ERROR: Controller script not found at {CONTROLLER}")

time.sleep(2)  # wait for processes to initialize

# --- EXECUTE GITHEALTH + DASHBOARD SCRIPTS ---
for script in [GITHEALTH_SCRIPT, DASHBOARD_SCRIPT]:
    if os.path.isfile(script):
        try:
            subprocess.Popen(["bash", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[Yberion] Started script: {script}")
        except Exception as e:
            print(f"[Yberion] Failed to start script {script}: {e}")
    else:
        print(f"[Yberion] WARNING: Script not found: {script}")

# --- FINAL STATUS ---
print("[Yberion] Launcher execution finished. Nexus + Junior + Dashboard attempted start.")
print(f"[Yberion] Dashboard JSON located at: {DASHBOARD_JSON}")
