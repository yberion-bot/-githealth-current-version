import os
import zipfile
from github import Github

# --- CONFIGURATION ---
ZIP_PATH = r'C:\Users\schat\Desktop\Yberion.zip'
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN_HERE'  # Personal Access Token
REPO_NAME = 'yberion-bot/yberion'

# --- EXTRACT ZIP FILE CONTENTS ---
zip_files = set()
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_files.update(zip_ref.namelist())

# --- CONNECT TO GITHUB ---
gh = Github(GITHUB_TOKEN)
repo = gh.get_repo(REPO_NAME)

# --- GET GITHUB FILES ---
git_files = set()
def get_files_recursive(contents, path_prefix=''):
    for content in contents:
        if content.type == 'dir':
            get_files_recursive(repo.get_contents(content.path), path_prefix)
        else:
            git_files.add(content.path)

contents = repo.get_contents("")
get_files_recursive(contents)

# --- COMPARE ---
only_in_zip = zip_files - git_files
only_in_git = git_files - zip_files

print('Files only in ZIP:', only_in_zip)
print('Files only in GitHub:', only_in_git)