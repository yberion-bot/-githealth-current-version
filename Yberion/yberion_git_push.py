import subprocess
import os

# --- CONFIG ---
REPO_URL = 'git@github.com:yberion-bot/yberion.git'  # SSH URL
BRANCH = 'main'
COMMIT_MESSAGE = 'Update Yberion with latest GUI and Nexus fixes'
BASE_DIR = os.getcwd()

# --- INIT GIT REPO IF MISSING ---
if not os.path.isdir(os.path.join(BASE_DIR, '.git')):
    subprocess.run(['git', 'init'], cwd=BASE_DIR)
    subprocess.run(['git', 'remote', 'add', 'origin', REPO_URL], cwd=BASE_DIR)

# --- STAGE ALL CHANGES ---
subprocess.run(['git', 'add', '.'], cwd=BASE_DIR)

# --- COMMIT ---
subprocess.run(['git', 'commit', '-m', COMMIT_MESSAGE], cwd=BASE_DIR)

# --- PUSH TO REMOTE ---
subprocess.run(['git', 'push', '-u', 'origin', BRANCH], cwd=BASE_DIR)

print('[Yberion Git Push] Completed successfully.')