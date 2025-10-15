import os
import zipfile
from git import Repo, GitCommandError

# Dateitypen, die wir committen und ins ZIP aufnehmen wollen
INCLUDE_EXTENSIONS = ['.py', '.md', '.sh', '.bat', '.txt']
EXCLUDE_DIRS = ['yberionrepositry_local', 'Yberion_Download', 'AutoGPT-master']

REPO_PATH = r'C:\Users\schat\yberion'
ZIP_OUTPUT = r'C:\Users\schat\yberion_smart_commit_export.zip'

# Gehe durch den Arbeitsordner und filtere passende Dateien
def get_files_to_include(repo_path):
    files_to_add = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if any(file.endswith(ext) for ext in INCLUDE_EXTENSIONS):
                file_path = os.path.relpath(os.path.join(root, file), repo_path)
                files_to_add.append(file_path)
    return files_to_add

# Commit & Push (wie bisher)
def smart_commit_push(repo_path, message='smart commit'):
    repo = Repo(repo_path)
    files_added = get_files_to_include(repo_path)

    if not files_added:
        print('Keine Dateien zum Committen gefunden.')
        return files_added

    try:
        repo.index.add(files_added)
        repo.index.commit(message)
        origin = repo.remote(name='origin')
        origin.push()
        print(f'Erfolgreich gepusht: {files_added}')
    except GitCommandError as e:
        print(f'Fehler beim Commit oder Push: {e}')

    return files_added

# ZIP erstellen
def export_to_zip(repo_path, output_path, files_list):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in files_list:
            zipf.write(os.path.join(repo_path, f), arcname=f)
    print(f'ZIP erstellt: {output_path}')

if __name__ == '__main__':
    files_to_commit = smart_commit_push(REPO_PATH, 'Add selected files using smart commit filter')
    if files_to_commit:
        export_to_zip(REPO_PATH, ZIP_OUTPUT, files_to_commit)
