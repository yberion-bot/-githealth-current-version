import os
import zipfile
import datetime
import shutil

# ==== EINSTELLUNGEN ====
SOURCE_DIR = "yberion_full_package"   # Quellordner
OUTPUT_NAME_BASE = "yberion_full_package_final_status"  # Basisname für ZIP
OUTPUT_DIR = "."                       # Zielverzeichnis (aktuelles Verzeichnis)
BACKUP_OLD = True                      # Alte ZIPs sichern statt überschreiben
DELETE_TEMP = False                    # Temporäre Dateien nach Update löschen

def log(msg):
    print(f"[Yberion] {msg}")

def zip_directory(source_dir, output_path):
    """Erstellt ZIP-Datei aus Verzeichnis"""
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_dir))
                zipf.write(file_path, arcname)
    log(f"✅ ZIP erstellt: {output_path}")

def main():
    log("Starte Auto-ZIP-Update für Yberion 3.0 ...")

    if not os.path.exists(SOURCE_DIR):
        log(f"❌ Quellverzeichnis '{SOURCE_DIR}' nicht gefunden!")
        return

    # Erzeuge Dateiname mit Zeitstempel
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_zip = os.path.join(OUTPUT_DIR, f"{OUTPUT_NAME_BASE}_v3.0_{timestamp}.zip")

    # Alte ZIP sichern oder löschen
    existing_zips = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(OUTPUT_NAME_BASE) and f.endswith(".zip")]
    for old_zip in existing_zips:
        old_path = os.path.join(OUTPUT_DIR, old_zip)
        if BACKUP_OLD:
            backup_path = old_path.replace(".zip", "_backup.zip")
            shutil.move(old_path, backup_path)
            log(f"📦 Alte ZIP gesichert: {backup_path}")
        else:
            os.remove(old_path)
            log(f"🗑️ Alte ZIP gelöscht: {old_path}")

    # Neue ZIP erstellen
    zip_directory(SOURCE_DIR, output_zip)

    # Abschluss-Check
    size_mb = os.path.getsize(output_zip) / (1024 * 1024)
    log(f"📏 Neue ZIP-Größe: {size_mb:.2f} MB")
    log("✅ Auto-ZIP-Update erfolgreich abgeschlossen!")

    if DELETE_TEMP:
        log("🧹 Temporäre Dateien entfernt (Option aktiviert)")

if __name__ == "__main__":
    main()
