import os
import subprocess
import ctypes
import shutil
import winreg

# ---- Check for admin rights ----
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("Please run this script as Administrator!")
    exit()

print("---- Starting Windows 11 Ultimate Optimization ----")

# 1. Set High Performance Power Plan
print("[1/7] Setting High Performance Power Plan...")
subprocess.run("powercfg -setactive SCHEME_MIN", shell=True)

# 2. Clean Temporary Files
print("[2/7] Cleaning temporary files...")
temp_dirs = [os.environ['TEMP'], r"C:\Windows\Temp"]
for d in temp_dirs:
    for root, dirs, files in os.walk(d):
        for f in files:
            try:
                os.remove(os.path.join(root, f))
            except:
                pass
        for folder in dirs:
            try:
                shutil.rmtree(os.path.join(root, folder))
            except:
                pass

# 3. Optimize SSD (Trim)
print("[3/7] Optimizing C: drive (Trim)...")
subprocess.run("defrag C: /L /O", shell=True)

# 4. Disable unnecessary startup apps
print("[4/7] Disabling unnecessary startup apps...")
startup_path = os.path.join(os.environ['APPDATA'], r"Microsoft\Windows\Start Menu\Programs\Startup")
if os.path.exists(startup_path):
    for item in os.listdir(startup_path):
        item_path = os.path.join(startup_path, item)
        try:
            os.remove(item_path)
            print(f"Removed startup item: {item}")
        except:
            pass

# 5. Adjust Visual Effects for Best Performance
print("[5/7] Adjusting visual effects for best performance...")
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
    winreg.CloseKey(key)
except:
    print("Failed to adjust visual effects.")

# 6. Disable Widgets
print("[6/7] Disabling Windows Widgets...")
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "TaskbarDa", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)
except:
    print("Failed to disable widgets.")

# 7. Disable Snap Layouts/Assist Animations
print("[7/7] Disabling Snap Assist Animations...")
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "DisablePreviewDesktop", 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)
except:
    print("Failed to disable Snap animations.")

# 8. Disable unnecessary background services (safe ones)
print("[8/7] Disabling some unnecessary background services...")
services_to_disable = [
    "XblGameSave",    # Xbox Game Save
    "WaaSMedicSvc",   # Windows Update Medic Service (won't stop updates)
    "OneSyncSvc"      # OneDrive Sync
]

for svc in services_to_disable:
    subprocess.run(f"sc config {svc} start= disabled", shell=True)
    subprocess.run(f"net stop {svc}", shell=True)

print("---- Ultimate Optimization Complete! ----")
print("Please restart your computer for all changes to take effect.")
