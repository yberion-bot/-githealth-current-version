import os
import sys
import subprocess
import json
import datetime
import tkinter as tk
from tkinter import messagebox

# --- BASE DIR ---
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

# --- PATHS ---
NEXUS_EXE = os.path.join(BASE_DIR, "Yberion_Nexus.exe")
CONTROLLER_SCRIPT = os.path.join(BASE_DIR, "yberion_controller.py")
LAUNCHER_EXE = os.path.join(BASE_DIR, "Yberion_Nexus.exe")  # Can also point to this GUI
DASHBOARD_JSON = os.path.join(BASE_DIR, "githealth_dashboard.json")

PYTHON_EXE = sys.executable

# --- LOAD DASHBOARD ---
if os.path.exists(DASHBOARD_JSON):
    with open(DASHBOARD_JSON, 'r') as f:
        dashboard = json.load(f)
else:
    dashboard = {
        "Nexus": {},
        "Controller": {},
        "Launcher": {}
    }

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
    if exe_path and file_exists(exe_path):
        if is_process_running(os.path.basename(exe_path)):
            messagebox.showinfo("Info", f"{name} is already running.")
        else:
            subprocess.Popen(exe_path, shell=True)
            messagebox.showinfo("Success", f"{name} launched successfully.")
    elif script_path and file_exists(script_path):
        subprocess.Popen([PYTHON_EXE, script_path], shell=True)
        messagebox.showinfo("Success", f"{name} script launched successfully.")
    else:
        messagebox.showerror("Error", f"{name} executable or script not found!")
    update_entry(name, exe_path, script_path)

# --- AUTO LAUNCH ON GUI START ---
launch_process('Nexus', NEXUS_EXE)
launch_process('Controller', None, CONTROLLER_SCRIPT)
launch_process('Launcher', LAUNCHER_EXE)

# --- GUI SETUP ---
root = tk.Tk()
root.title("Yberion Nexus Launcher")
root.geometry("400x250")
root.resizable(False, False)

components = [
    ("Nexus", NEXUS_EXE, None),
    ("Controller", None, CONTROLLER_SCRIPT),
    ("Launcher", LAUNCHER_EXE, None)
]

for i, (name, exe_path, script_path) in enumerate(components):
    tk.Label(root, text=name, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=10, sticky='w')
    tk.Button(root, text="Launch", command=lambda n=name, e=exe_path, s=script_path: launch_process(n, e, s)).grid(row=i, column=1, padx=10)

def refresh_status():
    for name, exe_path, script_path in components:
        update_entry(name, exe_path, script_path)
    root.after(5000, refresh_status)  # Refresh every 5 seconds

refresh_status()
root.mainloop()