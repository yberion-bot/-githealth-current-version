import os
import subprocess

# --- Configuration ---
REPO_URL = "git@github.com:yberion-bot/yberion.git"
COMMIT_MSG = "Update: progress synced from local Yberion build"

# --- Determine Base Directory ---
BASE_DIR = os.getcwd()
GIT_DIR = os.path.join(BASE_DIR, ".git")

# --- Initialize repo if missing ---
if not os.path.isdir(GIT_DIR):
    print("[Yberion] Git repo not found. Initializing...")
    subprocess.run(["git", "init"], cwd=BASE_DIR)
    subprocess.run(["git", "remote", "add", "origin", REPO_URL], cwd=BASE_DIR)
else:
    print("[Yberion] Git repo detected.")

# --- Stage all changes ---
subprocess.run(["git", "add", "--all"], cwd=BASE_DIR)

# --- Commit changes ---
subprocess.run(["git", "commit", "-m", COMMIT_MSG], cwd=BASE_DIR)

# --- Push to origin (SSH) ---
subprocess.run(["git", "push", "-u", "origin", "main"], cwd=BASE_DIR)

print("[Yberion] Git push complete.")
