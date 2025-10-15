#!/usr/bin/env bash
# =====================================================
# Yberion Git Repository, History, README, Patchnodes Save
# Autor: Yberion Schwellenhüter
# Zweck: Vollständiges Snapshot + Patchnode Export für Audit & Version Tracking
# =====================================================

REPO_DIR="$HOME/yberion"
OUTPUT_DIR="$REPO_DIR/git_snapshot"
LOGFILE="$OUTPUT_DIR/githistory.log"
PATCHNODE_FILE="$OUTPUT_DIR/patchnodes.json"
README_FILE="$OUTPUT_DIR/README.md"
VERSION_FILE="$OUTPUT_DIR/version.txt"

# Ordner sicherstellen
mkdir -p "$OUTPUT_DIR"

cd "$REPO_DIR" || { echo "[Yberion] Repo nicht gefunden: $REPO_DIR"; exit 1; }

# --- Git History Export ---
git log --pretty=format:'%h %ad | %s%d [%an]' --date=short > "$LOGFILE"

# --- README Copy ---
if [ -f README.md ]; then
    cp README.md "$README_FILE"
fi

# --- Patchnodes Export (Dashboard JSON) ---
DASHBOARD_FILE="$REPO_DIR/dashboard/githealth_dashboard.json"
if [ -f "$DASHBOARD_FILE" ]; then
    jq '{patchnodes}' "$DASHBOARD_FILE" > "$PATCHNODE_FILE"
else
    echo '{"patchnodes": []}' > "$PATCHNODE_FILE"
fi

# --- Version Synchronisation ---
LOCAL_HASH=$(git rev-parse HEAD)
echo "$LOCAL_HASH" > "$VERSION_FILE"

# --- Ausgabe ---
echo "[Yberion] Git History, README, Patchnodes und Version synchronisiert."
echo "Logfile      : $LOGFILE"
echo "README        : $README_FILE"
echo "Patchnodes    : $PATCHNODE_FILE"
echo "Version File  : $VERSION_FILE"
