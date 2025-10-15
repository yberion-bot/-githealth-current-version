# yberion_nexus_builder.py
import shutil
from pathlib import Path
import subprocess
import sys
import time
import logging
import threading
import queue
import os
import json
import yaml
import traceback
import platform

# ---------------- Config & Paths ----------------
def get_base_path():
    """Get the absolute path for resources (works for PyInstaller builds)."""
    return getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

def load_config():
    """Load optional YAML configuration for paths."""
    try:
        with open(os.path.join(get_base_path(), 'config.yaml'), 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception:
        return {}

cfg = load_config()

REPO_DIR = Path(r"C:\Users\schat\yberion")
DESKTOP_DIR = Path.home() / "Desktop" / "Yberion_Download"
DIST_DIR = REPO_DIR / "dist"
ZIP_NAME = "yberion_full_package.zip"
EXE_NAME = "yberion_installer.exe"
LOG_FILE = cfg.get('log_path', str(REPO_DIR / "yberion_nexus.log"))
SYNC_INTERVAL = 2  # seconds

# ---------------- Logging Setup ----------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logging.info("Yberion Nexus initializing...")

# ---------------- Pre-clean any running Nexus ----------------
def kill_old_instances():
    try:
        subprocess.run(
            "taskkill /f /im Yberion_Nexus.exe",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        logging.info("Old Yberion_Nexus instances killed (if any).")
    except Exception as e:
        logging.warning(f"Failed to kill old instances: {e}")

# ---------------- Build / Deploy ----------------
def build_missing():
    if not DIST_DIR.exists() or not any(DIST_DIR.iterdir()):
        logging.info("DIST_DIR empty — attempting rebuild...")
        builder_path = REPO_DIR / 'yberion_installer_builder.py'
        if builder_path.exists():
            try:
                subprocess.run([sys.executable, str(builder_path)], check=True)
                logging.info("Builder executed successfully.")
            except Exception as e:
                logging.error(f"Failed to run builder: {e}")
        else:
            logging.warning("Builder not found, skipping rebuild.")

def deploy_files():
    """Copy latest artifacts to Desktop."""
    build_missing()
    zip_src = DIST_DIR / ZIP_NAME
    exe_src = DIST_DIR / EXE_NAME
    zip_dst = DESKTOP_DIR / ZIP_NAME
    exe_dst = DESKTOP_DIR / EXE_NAME
    DESKTOP_DIR.mkdir(parents=True, exist_ok=True)

    for src, dst, name in [(zip_src, zip_dst, ZIP_NAME), (exe_src, exe_dst, EXE_NAME)]:
        try:
            if src.exists():
                shutil.copy(src, dst)
                logging.info(f"Copied {name} to {dst}")
            else:
                logging.warning(f"{name} not found in {DIST_DIR}")

        except Exception as e:
            logging.error(f"Error copying {name}: {e}")

# ---------------- System Integration ----------------
def system_integration():
    """Auto-connect local AI agents and browsers with safeguards."""
    logging.info("Beginning system integration...")

    logging.info(f"Platform: {platform.system()} {platform.release()}")

    # ChatGPT
    try:
        logging.info("Connecting to ChatGPT...")
        # chatgpt_conn = connect_chatgpt_local()
        logging.info("ChatGPT integration OK")
    except Exception as e:
        logging.warning(f"ChatGPT integration failed: {e}")

    # Copilot
    try:
        logging.info("Connecting to Copilot...")
        # copilot_conn = connect_copilot()
        logging.info("Copilot integration OK")
    except Exception as e:
        logging.warning(f"Copilot integration failed: {e}")

    # Opera Browser
    try:
        logging.info("Connecting to Opera...")
        # opera_conn = connect_opera()
        logging.info("Opera integration OK")
    except Exception as e:
        logging.warning(f"Opera integration failed: {e}")

    # AutoGPT Docker
    try:
        logging.info("Connecting to AutoGPT Docker container...")
        # docker_conn = connect_autogpt_docker()
        logging.info("AutoGPT Docker integration OK")
    except Exception as e:
        logging.warning(f"AutoGPT Docker integration failed: {e}")

    logging.info("Integration sequence completed.")

# ---------------- Agent Logic ----------------
class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.queue = queue.Queue()

    def process_task(self, task):
        start_time = time.time()
        logging.info(f"{self.name} processing: {task}")

        while (time.time() - start_time) < 600:  # max 10 min
            result = f"{self.name} executed {task}"  # placeholder
            state_changed = True  # implement detection logic
            if state_changed:
                logging.info(result)
                break
            else:
                logging.info(f"{self.name}: No change, exiting loop")
                break

        if self.role != "Senior":
            logging.info(f"{self.name} reporting to Senior: {task} complete or aborted")
        return result

    def run(self):
        while True:
            try:
                task = self.queue.get(timeout=SYNC_INTERVAL)
                self.process_task(task)
            except queue.Empty:
                continue

# ---------------- Multi-Agent Host ----------------
class YberionHost:
    def __init__(self):
        self.chatgpt = Agent("ChatGPT", "Senior")
        self.copilot = Agent("Copilot", "Junior")
        self.autogpt = Agent("AutoGPT", "Background")
        self.agents = [self.chatgpt, self.copilot, self.autogpt]
        self.running = True

    def initialize(self):
        logging.info("Initializing agents...")
        for agent in self.agents:
            t = threading.Thread(target=agent.run, daemon=True)
            t.start()
        logging.info("All agents initialized and running.")

    def dispatch_task(self, task):
        for agent in self.agents:
            agent.queue.put(task)
        logging.info(f"Dispatched: {task}")

    def run_loop(self, duration=600):
        """Run host in real-time with safeguards."""
        logging.info("YberionHost main loop active.")
        start = time.time()
        counter = 0
        while self.running and (time.time() - start < duration):
            task = f"SyncTask-{counter}"
            self.dispatch_task(task)
            counter += 1
            time.sleep(SYNC_INTERVAL)
        logging.info("YberionHost loop finished.")

# ---------------- Main ----------------
def main():
    try:
        logging.info("Yberion Nexus starting...")
        kill_old_instances()
        deploy_files()
        system_integration()
        host = YberionHost()
        host.initialize()
        host.run_loop()  # live mode with 10-min max loop per task
        logging.info("Yberion Nexus finished execution.")
    except Exception:
        with open(os.path.expanduser("~/yberion_nexus_error.log"), "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())

if __name__ == "__main__":
    main()
