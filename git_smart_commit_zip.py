import os
import zipfile
from git import Repo, GitCommandError

# Liste der Dateitypen, die wir committen wollen
INCLUDE_EXTENSIONS = ['.py', '.md', '.sh', '.bat', '.txt']
EXCLUDE_DIRS = ['yberionrepositry_local', 'Yberion_Download', 'AutoGPT-master']

# Gehe durch den Arbeitsordner und füge nur passende Dateien hinzu
def smart_add(repo_path):
    repo = Repo(repo_path)
    files_to_add = []

    for root, dirs, files in os.walk(repo_path):
        # Verzeichnisse ausschließen
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if any(file.endswith(ext) for ext in INCLUDE_EXTENSIONS):
                file_path = os.path.relpath(os.path.join(root, file), repo_path)
                files_to_add.append(file_path)

    if files_to_add:
        repo.index.add(files_to_add)
    return files_to_add

# ZIP export der Dateien
def export_files_zip(repo_path, files, zip_name='smart_commit_export.zip'):
    zip_path = os.path.join(repo_path, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            full_path = os.path.join(repo_path, file)
            zf.write(full_path, arcname=file)
    return zip_path

# Commit durchführen und optional pushen
def smart_commit_push(repo_path, message='smart commit', push=False):
    repo = Repo(repo_path)
    files_added = smart_add(repo_path)

    if not files_added:
        print('Keine Dateien zum Committen gefunden.')
        return

    try:
        repo.index.commit(message)
        print(f'Commit erfolgreich: {files_added}')

        zip_file = export_files_zip(repo_path, files_added)
        print(f'Exportiert als ZIP: {zip_file}')

        if push:
            origin = repo.remote(name='origin')
            origin.push()
            print('Push erfolgreich.')

    except GitCommandError as e:
        print(f'Fehler beim Commit oder Push: {e}')

if __name__ == '__main__':
    REPO_PATH = r'C:\Users\schat\yberion'
    smart_commit_push(REPO_PATH, 'Add selected files using smart commit filter', push=False)