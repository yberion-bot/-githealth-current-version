import subprocess
import os

# Liste der Dateitypen, die wir committen wollen
INCLUDE_EXTENSIONS = ['.py', '.md', '.sh', '.bat', '.txt']
EXCLUDE_DIRS = ['yberionrepositry_local', 'Yberion_Download', 'AutoGPT-master']

# Gehe durch den Arbeitsordner und füge nur passende Dateien hinzu
def smart_add(repo_path):
    for root, dirs, files in os.walk(repo_path):
        # Verzeichnisse ausschließen
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if any(file.endswith(ext) for ext in INCLUDE_EXTENSIONS):
                file_path = os.path.relpath(os.path.join(root, file), repo_path)
                subprocess.run(['git', 'add', file_path], cwd=repo_path)

# Commit und Push durchführen
def smart_commit_push(repo_path, message='smart commit'):
    smart_add(repo_path)
    subprocess.run(['git', 'commit', '-m', message], cwd=repo_path)
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_path)

if __name__ == '__main__':
    REPO_PATH = r'C:\Users\schat\yberion'
    smart_commit_push(REPO_PATH, 'Add selected files using smart commit filter')
