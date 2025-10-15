import os
import json
import subprocess
import datetime
import tkinter as tk
from tkinter import messagebox

# Use current working directory instead of __file__
base_dir = os.getcwd()
dashboard_file = os.path.join(base_dir, 'githealth_dashboard.json')

# Load or create dashboard
if os.path.exists(dashboard_file):
    with open(dashboard_file, 'r') as f:
        dashboard = json.load(f)
else:
    dashboard = {
        "Nexus": {},
        "Controller": {},
        "Launcher": {}
    }

# Helper functions
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
    with open(dashboard_file, 'w') as f:
        json.dump(dashboard, f, indent=4)

def launch_process(name, exe_path):
    if not file_exists(exe_path):
        messagebox.showerror("Error", f"{name} executable not found!")
        return
    if is_process_running(os.path.basename(exe_path)):
        messagebox.showinfo("Info", f"{name} is already running.")
        return
    try:
        subprocess.Popen(exe_path, shell=True)
        messagebox.showinfo("Success", f"{name} launched successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    update_entry(name, exe_path)

# Paths
nexus_exe = os.path.join(base_dir, 'dist', 'Yberion_Nexus.exe')
controller_script = os.path.join(base_dir, 'yberion_controller.py')
launcher_exe = os.path.join(base_dir, 'dist', 'yberion_launcher.exe')

# GUI setup
root = tk.Tk()
root.title("Yberion Launcher")
root.geometry("400x250")
root.resizable(False, False)

# Labels & Buttons
components = [
    ("Nexus", nexus_exe),
    ("Controller", launcher_exe),
    ("Launcher", launcher_exe)
]

for i, (name, path) in enumerate(components):
    tk.Label(root, text=name, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=10, sticky='w')
    tk.Button(root, text="Launch", command=lambda n=name, p=path: launch_process(n, p)).grid(row=i, column=1, padx=10)

def refresh_status():
    for name, path in components:
        update_entry(name, path)
    root.after(5000, refresh_status)  # Refresh every 5 seconds

# Start auto-refresh
refresh_status()

root.mainloop()