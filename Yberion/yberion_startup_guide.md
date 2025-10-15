Here’s a step-by-step guide to start everything using your new files:

---

### 1. Verify File Structure
Make sure your folder looks like this:

```
Yberion/
├─ dist/
│  ├─ yberion_launcher.exe
│  ├─ Yberion_Nexus.exe
├─ yberion_controller.py
├─ githealth_dashboard.json
├─ launcher.py  (your updated GUI launcher script)
```

### 2. Run the Launcher
Since the launcher now opens the GUI and keeps it running:

- On Windows, simply double-click:
  ```
  dist\yberion_launcher.exe
  ```

- Or run from PowerShell:
  ```powershell
cd C:\Users\schat\Desktop\Yberion\dist
.\"yberion_launcher.exe"
```

The GUI should open immediately.

### 3. Launch Components
Inside the GUI, you’ll see buttons for:

- **Nexus** → launches `Yberion_Nexus.exe`
- **Controller** → launches `yberion_controller.py` (or `.exe` if compiled)
- **Launcher** → launches the `yberion_launcher.exe` itself (optional/restart)

Click each button as needed. The GUI will show if each process is running and update every 5 seconds.

### 4. Verify Dashboard
The `githealth_dashboard.json` will automatically update with the latest status of each component:

```json
{
    "Nexus": {"exists": true, "running": true, "last_checked": "2025-10-14T15:23:12", "script_exists": false},
    "Controller": {"exists": true, "running": false, "last_checked": "2025-10-14T15:23:12", "script_exists": true},
    "Launcher": {"exists": true, "running": true, "last_checked": "2025-10-14T15:23:12"}
}
```

This helps track everything centrally.

### 5. Optional: Auto-launch All
If you want everything to start automatically when opening the launcher, you can add this snippet in `launcher.py` before the mainloop:

```python
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
```

---

Once that’s done, you just need to start the `yberion_launcher.exe`, and your GUI will stay active while managing all other components.
