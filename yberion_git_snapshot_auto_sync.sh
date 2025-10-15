#!/usr/bin/env bash
# =====================================================
# Yberion Git Snapshot AutoSync
# Autor: Yberion Schwellenhüter
# Zweck: Automatisches Update des Git Snapshots bei jedem Push
# =====================================================

REPO_DIR="$HOME/yberion"
SNAPSHOT_DIR="$REPO_DIR/git_snapshot"
DASHBOARD_FILE="$REPO_DIR/dashboard/githealth_dashboard.json"
VERSION_FILE="$SNAPSHOT_DIR/version.txt"

mkdir -p "$SNAPSHOT_DIR"
cd "$REPO_DIR" || { echo "[Yberion] Repo nicht gefunden: $REPO_DIR"; exit 1; }

# --- Hook prüfen ---
HOOK_FILE="$REPO_DIR/.git/hooks/post-push"
if [ ! -f "$HOOK_FILE" ]; then
    cat <<'EOF' > "$HOOK_FILE"
#!/usr/bin/env bash

SNAPSHOT_DIR="$HOME/yberion/git_snapshot"
DASHBOARD_FILE="$HOME/yberion/dashboard/githealth_dashboard.json"
VERSION_FILE="$SNAPSHOT_DIR/version.txt"

mkdir -p "$SNAPSHOT_DIR"
cd "$HOME/yberion" || exit 1

# Git History
git log --oneline --graph --decorate > "$SNAPSHOT_DIR/githistory.log"

# README
if [ -f "README.md" ]; then
    cp README.md "$SNAPSHOT_DIR/README.md"
fi

# Patchnodes
if [ -f "$DASHBOARD_FILE" ]; then
    jq '.patchnodes' "$DASHBOARD_FILE" > "$SNAPSHOT_DIR/patchnodes.json"
fi

# Version
LOCAL_HASH=$(git rev-parse HEAD)
echo "$LOCAL_HASH" > "$VERSION_FILE"

echo "[Yberion] Snapshot AutoSync abgeschlossen: $VERSION_FILE"
EOF
    chmod +x "$HOOK_FILE"
    echo "[Yberion] Post-Push Hook erstellt für AutoSync." 
else
    echo "[Yberion] Post-Push Hook bereits vorhanden, AutoSync aktiv." 
fi