#!/usr/bin/env bash
set -euo pipefail

echo "=== Git & SSH Setup für Yberion ==="

# 1. Git User konfigurieren
git config --global user.name "yberion-bot"
git config --global user.email "schatzfrederic88@gmail.com"

# 2. SSH-Agent starten und Key laden
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_yberion || echo "⚠️ Bitte sicherstellen, dass ~/.ssh/id_yberion existiert"

# 3. Public Key anzeigen (manuell bei GitHub einfügen!)
echo "=== Kopiere diesen Key und füge ihn in GitHub unter Settings → SSH and GPG Keys ein ==="
cat ~/.ssh/id_yberion.pub || echo "⚠️ Kein Public Key gefunden!"
echo "====================================================================================="

# 4. Branch main erstellen oder wechseln
git checkout -b main 2>/dev/null || git checkout main

# 5. Alles ins Staging nehmen und committen
git add .
git commit -m "Initial commit of Yberion project" || echo "⚠️ Commit bereits vorhanden oder keine Änderungen"

# 6. Push nach GitHub
git push -u origin main || echo "⚠️ Push fehlgeschlagen – prüfe SSH-Key und Remote-URL"