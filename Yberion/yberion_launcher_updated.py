import os
import subprocess
import json

# Pfad zum githealth_dashboard.json
dashboard_file = os.path.join(os.getcwd(), 'githealth_dashboard.json')

# Lade Dashboard
with open(dashboard_file, 'r') as f:
    dashboard = json.load(f)

for name, exe_path, script_path in [
('Nexus', nexus_exe, None),
('Controller', launcher_exe, controller_script),
('Launcher', launcher_exe, None)
]:
if not is_process_running(os.path.basename(exe_path)):
if exe_path.endswith('.exe'):
subprocess.Popen(exe_path)
elif exe_path.endswith('.py'):
subprocess.Popen(['python', exe_path])

print("Current Githealth Dashboard Status:\n")
for name, entry in dashboard.items():
    print(f"{name}:")
    print(f"  Exists: {entry.get('exists')}")
    print(f"  Running: {entry.get('running')}")
    if 'script_exists' in entry:
        print(f"  Script Exists: {entry.get('script_exists')}")
    print(f"  Last Checked: {entry.get('last_checked')}\n")

# Optionally, add functionality to launch apps/scripts
for name, entry in dashboard.items():
    if entry.get('exists') and not entry.get('running'):
        exe_path = entry.get('exe_path')
        script_path = entry.get('script_path', None)
        if exe_path and os.path.exists(exe_path):
            print(f"Launching {name} from {exe_path}...")
            subprocess.Popen(exe_path)
        elif script_path and os.path.exists(script_path):
            print(f"Launching {name} script from {script_path}...")
            subprocess.Popen(['python', script_path])