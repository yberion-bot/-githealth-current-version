import os
import json
import subprocess
import tkinter as tk
from tkinter import messagebox

# Lade githealth_dashboard.json
dashboard_file = os.path.join(os.getcwd(), 'githealth_dashboard.json')
with open(dashboard_file, 'r') as f:
    dashboard = json.load(f)

# Funktion, um einen Eintrag zu starten
def launch_component(name):
    entry = dashboard.get(name)
    if not entry:
        messagebox.showerror("Error", f"Component {name} not found in dashboard")
        return

    exe_path = entry.get('exists') and entry.get('running') is False and os.path.join('dist', f'Yberion_{name}.exe')
    if exe_path and os.path.exists(exe_path):
        try:
            subprocess.Popen(exe_path)
            messagebox.showinfo("Launched", f"{name} launched successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch {name}: {str(e)}")
    else:
        messagebox.showwarning("Warning", f"{name} does not exist or is already running.")

# Tkinter GUI
root = tk.Tk()
root.title("Yberion Launcher")
root.geometry("400x200")

row = 0
for component in dashboard.keys():
    label = tk.Label(root, text=component)
    label.grid(row=row, column=0, padx=10, pady=5)

    btn = tk.Button(root, text="Launch", command=lambda c=component: launch_component(c))
    btn.grid(row=row, column=1, padx=10, pady=5)
    row += 1

root.mainloop()