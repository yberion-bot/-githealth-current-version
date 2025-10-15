import os
import subprocess
import sys
from tkinter import messagebox, Tk

# Paths
git_exe = 'git'  # Assumes git is in PATH
repo_dir = os.getcwd()  # Adjust if your repo is elsewhere

# GUI root to show message boxes
root = Tk()
root.withdraw()  # Hide main window

try:
    # Stage all changes
    subprocess.check_call([git_exe, 'add', '.'], cwd=repo_dir)
    
    # Commit with a message
    subprocess.check_call([git_exe, 'commit', '-m', 'Update: Yberion Nexus GUI progress'], cwd=repo_dir)
    
    # Push to remote
    subprocess.check_call([git_exe, 'push'], cwd=repo_dir)
    messagebox.showinfo('Git Push', 'Git push completed successfully.')
except subprocess.CalledProcessError as e:
    messagebox.showerror('Git Push Error', f'An error occurred: {e}')
    sys.exit(1)