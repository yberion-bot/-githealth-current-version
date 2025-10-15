import os
import sys
import subprocess
import json
import datetime
import tkinter as tk
from tkinter import messagebox
import time

# --- BASE DIR ---
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

# --- PATHS ---
NEXUS_EXE = os.path.join(BASE_DIR, "Yberion_Nexus.exe")
CONTROLLER = os.path.join(BASE_DIR, "yberion_controller.py")
DASHBOARD_JSON = os.path.join(BASE_DIR, "githealth_dashboard.json")

PYTHON_EXE = sys.executable

# --- INIT DASHBOARD JSON IF MISSING ---
if not os.path.isfile(DASHBOARD_JSON):
    initial_dashboard = {
        "Nexus": {},
        "Controller": {},
        "Launcher": {}
    }
    with open(DASHBOARD_JSON, "w") as f:
        json.dump(initial_dashboard, f, indent=4)
    print(f"[Yberion] Initialized dashboard JSON at {DASHBOARD_JSON}")

# --- HELPER FUNCTIONS ---

def is_process_running(process_name):
    try:
        output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}"', shell=True)
        return process_name.encode() in output
    except Exception:
        return False

def file_exists(path):
    return os.path.exists(path)

def update_entry(name, exe_path, script_path=None):
    if not os.path.exists(DASHBOARD_JSON):
        return
    with open(DASHBOARD_JSON, 'r') as f:
        dashboard = json.load(f)

    entry = dashboard.get(name, {})
    entry['exists'] = file_exists(exe_path)
    entry['running'] = is_process_running(os.path.basename(exe_path))
    entry['last_checked'] = datetime.datetime.now().isoformat()
    if script_path:
        entry['script_exists'] = file_exists(script_path)
    dashboard[name] = entry

    with open(DASHBOARD_JSON, 'w') as f:
        json.dump(dashboard, f, indent=4)


def launch_process(name, exe_path, script_path=None):
    if not file_exists(exe_path) and not (script_path and file_exists(script_path)):
        messagebox.showerror("Error", f"{name} executable or script not found!")
        return
    if exe_path and is_process_running(os.path.basename(exe_path)):
        messagebox.showinfo("Info", f"{name} is already running.")
        return
    try:
        if exe_path and os.path.exists(exe_path):
            subprocess.Popen(exe_path, shell=True)
        elif script_path and os.path.exists(script_path):
            subprocess.Popen([PYTHON_EXE, script_path], shell=True)
        messagebox.showinfo("Success", f"{name} launched successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    update_entry(name, exe_path, script_path)

# --- GUI SETUP ---
root = tk.Tk()
root.title("Yberion Launcher")
root.geometry("400x250")
root.resizable(False, False)

components = [
    ("Nexus", NEXUS_EXE, None),
    ("Controller", None, CONTROLLER),
    ("Launcher", os.path.join(BASE_DIR, "Yberion_Nexus.exe"), None)
]

for i, (name, exe_path, script_path) in enumerate(components):
    tk.Label(root, text=name, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=10, sticky='w')
    tk.Button(root, text="Launch", command=lambda n=name, e=exe_path, s=script_path: launch_process(n, e, s)).grid(row=i, column=1, padx=10)

# --- AUTO LAUNCH ALL ---
for name, exe_path, script_path in components:
    launch_process(name, exe_path, script_path)

# --- AUTO REFRESH ---
def refresh_status():
    for name, exe_path, script_path in components:
        update_entry(name, exe_path, script_path)
    root.after(5000, refresh_status)

refresh_status()

root.mainloop()
