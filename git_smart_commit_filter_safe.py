import os
from git import Repo, GitCommandError

# Liste der Dateitypen, die wir committen wollen
INCLUDE_EXTENSIONS = ['.py', '.md', '.sh', '.bat', '.txt']
EXCLUDE_DIRS = ['yberionrepositry_local', 'Yberion_Download', 'AutoGPT-master']

# Ziel-Repository für sichere Test-Pushes
TEST_REPO_NAME = '-githealth-current-version'

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

# Prüfe, ob SSH Zugang funktioniert
def check_ssh(repo_path):
    repo = Repo(repo_path)
    origin = repo.remote(name='origin')
    try:
        origin.fetch()  # Einfacher Test, um SSH-Verbindung zu prüfen
        return True
    except GitCommandError as e:
        print(f'SSH-Fehler: {e}')
        return False

# Commit und Push durchführen
def smart_commit_push(repo_path, message='smart commit'):
    repo = Repo(repo_path)
    files_added = smart_add(repo_path)

    if not files_added:
        print('Keine Dateien zum Committen gefunden.')
        return

    if not check_ssh(repo_path):
        print(f'SSH Zugriff auf Repository nicht möglich. Push wird übersprungen.')
        return

    try:
        repo.index.commit(message)
        origin = repo.remote(name='origin')
        # Direkt auf Test-Repo pushen, wenn konfiguriert
        if TEST_REPO_NAME in [r.name for r in repo.remotes]:
            origin_test = repo.remote(TEST_REPO_NAME)
            origin_test.push()
            print(f'Erfolgreich auf Test-Repo {TEST_REPO_NAME} gepusht: {files_added}')
        else:
            origin.push()
            print(f'Erfolgreich gepusht: {files_added}')
    except GitCommandError as e:
        print(f'Fehler beim Commit oder Push: {e}')

if __name__ == '__main__':
    REPO_PATH = r'C:\Users\schat\yberion'
    smart_commit_push(REPO_PATH, 'Add selected files using smart commit filter')