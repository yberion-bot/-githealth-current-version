import os
import json
import subprocess
import datetime
import tkinter as tk
from tkinter import messagebox
import sys
import threading

# -------------------------------
# Configuration
# -------------------------------
SANDBOX_MODE = True  # True = keine echten Prozesse starten, nur loggen
MAX_PROCESSES = 1    # Max 1 Subprocess pro Component gleichzeitig
CHECK_INTERVAL = 5000  # Status Refresh Interval in ms

base_dir = os.getcwd()
dashboard_file = os.path.join(base_dir, 'githealth_dashboard.json')

if os.path.exists(dashboard_file):
    with open(dashboard_file, 'r') as f:
        dashboard = json.load(f)
else:
    dashboard = {
        "Nexus": {},
        "Controller": {},
        "Launcher": {}
    }

components = {
    "Nexus": os.path.join(base_dir, 'dist', 'Yberion_Nexus.exe'),
    "Controller": os.path.join(base_dir, 'yberion_controller.py'),
    "Launcher": os.path.join(base_dir, 'dist', 'yberion_launcher.exe')
}

# -------------------------------
# Helper Functions
# -------------------------------
try:
    import psutil
except ImportError:
    psutil = None


def is_launcher_running():
    if not psutil:
        return False
    count = 0
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if 'yberion_launcher' in ' '.join(proc.info['cmdline']):
                count += 1
        except Exception:
            continue
    return count > 1


def file_exists(path):
    return os.path.exists(path)


def is_process_running(process_name):
    try:
        output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}"', shell=True)
        return process_name.encode() in output
    except Exception:
        return False


def update_entry(name, exe_path):
    entry = dashboard.get(name, {})
    entry['exists'] = file_exists(exe_path)
    entry['running'] = is_process_running(os.path.basename(exe_path))
    entry['last_checked'] = datetime.datetime.now().isoformat()
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

    def safe_start():
        if SANDBOX_MODE:
            print(f"[SANDBOX] Would launch: {exe_path}")
            messagebox.showinfo("Sandbox", f"[SANDBOX] {name} launch simulated.")
        else:
            try:
                subprocess.Popen([exe_path], shell=False)
                messagebox.showinfo("Success", f"{name} launched successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        update_entry(name, exe_path)

    threading.Thread(target=safe_start).start()

# -------------------------------
# Single Instance Enforcement
# -------------------------------
if is_launcher_running():
    messagebox.showinfo("Info", "Yberion Launcher is already running!")
    sys.exit(0)

# -------------------------------
# Auto-Kill Safe Wrapper
# -------------------------------
def auto_check_processes():
    for name, path in components.items():
        if not SANDBOX_MODE and not is_process_running(os.path.basename(path)) and file_exists(path):
            # Optionally auto-restart or log
            print(f"[AUTO-CHECK] {name} is not running.")
    root.after(CHECK_INTERVAL, auto_check_processes)

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("Yberion Launcher (Sandbox Safe)")
root.geometry("400x250")
root.resizable(False, False)

for i, (name, path) in enumerate(components.items()):
    tk.Label(root, text=name, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=10, sticky='w')
    tk.Button(root, text="Launch", command=lambda n=name, p=path: launch_process(n, p)).grid(row=i, column=1, padx=10)

# -------------------------------
# Status Refresh
# -------------------------------
def refresh_status():
    for name, path in components.items():
        update_entry(name, path)
    root.after(CHECK_INTERVAL, refresh_status)

refresh_status()
auto_check_processes()
root.mainloop()
