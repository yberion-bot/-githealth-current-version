# This is your working Yberion Nexus GUI Launcher
# All components (Nexus, Controller, Launcher) are launched automatically and via GUI buttons

import os
import sys
import subprocess
import datetime
import json
import tkinter as tk
from tkinter import messagebox

# --- BASE DIR ---
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

# --- PATHS ---
NEXUS_EXE = os.path.join(BASE_DIR, 'dist', 'Yberion_Nexus.exe')
CONTROLLER = os.path.join(BASE_DIR, 'yberion_controller.py')
LAUNCHER_EXE = os.path.join(BASE_DIR, 'dist', 'yberion_launcher.exe')
DASHBOARD_JSON = os.path.join(BASE_DIR, 'githealth_dashboard.json')
PYTHON_EXE = sys.executable

# --- INIT DASHBOARD JSON IF MISSING ---
if not os.path.isfile(DASHBOARD_JSON):
    initial_dashboard = {
        "Nexus": {},
        "Controller": {},
        "Launcher": {}
    }
    with open(DASHBOARD_JSON, 'w') as f:
        json.dump(initial_dashboard, f, indent=4)

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
        dashboard = {}
    else:
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


def launch_process(name, exe_path):
    if not file_exists(exe_path):
        messagebox.showerror('Error', f'{name} executable not found!')
        return
    if is_process_running(os.path.basename(exe_path)):
        messagebox.showinfo('Info', f'{name} is already running.')
        return
    try:
        subprocess.Popen([exe_path], shell=True)
        messagebox.showinfo('Success', f'{name} launched successfully.')
    except Exception as e:
        messagebox.showerror('Error', str(e))
    update_entry(name, exe_path)

# --- GUI SETUP ---
root = tk.Tk()
root.title('Yberion Launcher')
root.geometry('400x250')
root.resizable(False, False)

components = [
    ('Nexus', NEXUS_EXE),
    ('Controller', CONTROLLER),
    ('Launcher', LAUNCHER_EXE)
]

# Create labels and buttons for each component
for i, (name, path) in enumerate(components):
    tk.Label(root, text=name, font=('Arial', 12)).grid(row=i, column=0, padx=10, pady=10, sticky='w')
    tk.Button(root, text='Launch', command=lambda n=name, p=path: launch_process(n, p)).grid(row=i, column=1, padx=10)

# --- AUTO LAUNCH EVERYTHING ON STARTUP ---
for name, path in components:
    launch_process(name, path)

# --- STATUS REFRESH ---
def refresh_status():
    for name, path in components:
        update_entry(name, path)
    root.after(5000, refresh_status)  # Refresh every 5 seconds

refresh_status()
root.mainloop()
