import os
import subprocess
import json
import datetime
import tkinter as tk
from tkinter import messagebox

# --- BASE DIR ---
base_dir = os.getcwd()

# --- Paths ---
nexus_exe = os.path.join(base_dir, 'dist', 'Yberion_Nexus.exe')
controller_script = os.path.join(base_dir, 'yberion_controller.py')
launcher_exe = os.path.join(base_dir, 'dist', 'yberion_launcher.exe')
dashboard_file = os.path.join(base_dir, 'githealth_dashboard.json')

# --- Load or initialize dashboard ---
if os.path.exists(dashboard_file):
    with open(dashboard_file, 'r') as f:
        dashboard = json.load(f)
else:
    dashboard = {"Nexus": {}, "Controller": {}, "Launcher": {}}

# --- Helper Functions ---
def is_process_running(process_name):
    try:
        output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}"', shell=True)
        return process_name.encode() in output
    except Exception:
        return False

def file_exists(path):
    return path is not None and os.path.exists(path)

def update_entry(name, exe_path, script_path=None):
    entry = dashboard.get(name, {})
    entry['exists'] = file_exists(exe_path)
    entry['running'] = is_process_running(os.path.basename(exe_path))
    entry['last_checked'] = datetime.datetime.now().isoformat()
    if script_path:
        entry['script_exists'] = file_exists(script_path)
    dashboard[name] = entry
    with open(dashboard_file, 'w') as f:
        json.dump(dashboard, f, indent=4)

def launch_process(name, exe_path, script_path=None):
    if not file_exists(exe_path) and not (script_path and file_exists(script_path)):
        messagebox.showerror("Error", f"{name} executable or script not found!")
        return
    if exe_path and is_process_running(os.path.basename(exe_path)):
        messagebox.showinfo("Info", f"{name} is already running.")
        return
    try:
        if exe_path and file_exists(exe_path):
            subprocess.Popen(exe_path)
        elif script_path and file_exists(script_path):
            subprocess.Popen(['python', script_path])
        messagebox.showinfo("Success", f"{name} launched successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    update_entry(name, exe_path, script_path)

# --- GUI Setup ---
root = tk.Tk()
root.title("Yberion Launcher")
root.geometry("400x250")
root.resizable(False, False)

components = [
    ("Nexus", nexus_exe, None),
    ("Controller", launcher_exe, controller_script),
    ("Launcher", launcher_exe, None)
]

for i, (name, exe_path, script_path) in enumerate(components):
    tk.Label(root, text=name, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=10, sticky='w')
    tk.Button(root, text="Launch", command=lambda n=name, e=exe_path, s=script_path: launch_process(n, e, s)).grid(row=i, column=1, padx=10)

# --- Auto-launch all on GUI start ---
for name, exe_path, script_path in components:
    launch_process(name, exe_path, script_path)

# --- Auto-refresh dashboard status ---
def refresh_status():
    for name, exe_path, script_path in components:
        update_entry(name, exe_path, script_path)
    root.after(5000, refresh_status)

refresh_status()
root.mainloop()