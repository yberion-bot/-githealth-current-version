# Robust Push-Skript für die finale Yberion ZIP ohne Input(), für sandboxed Umgebungen
import subprocess
import os
import shutil
import sys

# Pfade werden nur als Argumente oder fest kodiert verwendet, keine input() Abfragen
# Beispiel: python push_yberion_zip.py /path/to/repo /path/to/yberion.zip
if len(sys.argv) >= 3:
    REPO_DIR = sys.argv[1]
    ZIP_PATH = sys.argv[2]
else:
    # TODO: Auf deinem System anpassen
    REPO_DIR = '/Pfad/zu/deinem/yberion-repo'
    ZIP_PATH = '/Pfad/zur/yberion_full_package_final_status.zip'

# Optionaler Testmodus (prüft nur Pfade, keine Änderungen)
TEST_MODE = False

def log(msg):
    print(f"[Yberion-Push] {msg}")

try:
    log(f"Verwende Repository: {REPO_DIR}")
    log(f"Verwende ZIP-Datei: {ZIP_PATH}")

    # Prüfen, ob die angegebenen Pfade existieren
    if not os.path.isdir(REPO_DIR):
        raise FileNotFoundError(f"Repository-Verzeichnis existiert nicht: {REPO_DIR}")
    if not os.path.isfile(ZIP_PATH):
        raise FileNotFoundError(f"ZIP-Datei existiert nicht: {ZIP_PATH}")

    if TEST_MODE:
        log("✅ Testmodus aktiv: Pfade geprüft, keine Änderungen werden vorgenommen.")
        sys.exit(0)

    # In das Repository wechseln
    os.chdir(REPO_DIR)

    # ZIP-Datei kopieren (überschreibt, falls vorhanden)
    dest_zip = os.path.join(REPO_DIR, os.path.basename(ZIP_PATH))
    shutil.copy2(ZIP_PATH, dest_zip)
    log(f"✅ ZIP-Datei kopiert nach {dest_zip}")

    # Git-Befehle ausführen
    log("Füge ZIP-Datei zu Git hinzu...")
    subprocess.run(['git', 'add', os.path.basename(ZIP_PATH)], check=True)

    log("Commit vorbereiten...")
    subprocess.run(['git', 'commit', '-m', 'Add final Yberion 3.0 ZIP with status-check'], check=True)

    log("Push zu GitHub...")
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)

    log("✅ ZIP erfolgreich gepusht!")

except FileNotFoundError as e:
    log(f"❌ Fehler: {e}")
except subprocess.CalledProcessError as e:
    log(f"❌ Git-Befehl fehlgeschlagen: {e}")
except Exception as e:
    log(f"❌ Unerwarteter Fehler: {e}")

log("💡 Hinweis: Pfade können als Argumente übergeben werden:")
log("python push_yberion_zip.py <Repo-Pfad> <ZIP-Pfad>")
