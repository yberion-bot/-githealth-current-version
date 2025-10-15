import os
import zipfile


# Basisverzeichnis von Yberion
BASE_DIR = '/opt/yberion' # Passe an deinen lokalen Pfad an
ZIP_NAME = 'yberion_package.zip'


# Liste der Dateien / Ordner, die inkludiert werden
INCLUDE_DIRS = ['launcher', 'agents', 'dashboard', 'systemd', 'test']


def zip_directory(zipf, folder, base_path):
for root, dirs, files in os.walk(folder):
for file in files:
file_path = os.path.join(root, file)
arcname = os.path.relpath(file_path, base_path)
zipf.write(file_path, arcname)


with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
for d in INCLUDE_DIRS:
dir_path = os.path.join(BASE_DIR, d)
if os.path.exists(dir_path):
zip_directory(zipf, dir_path, BASE_DIR)


print(f'ZIP package created: {ZIP_NAME}')