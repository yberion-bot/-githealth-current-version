#!/bin/bash
# --- CONFIG ---
AUTHORIZED_ACCOUNT="YOUR_PRIMARY_ACCOUNT"
CURRENT_ACCOUNT=$(whoami)
LOGFILE="logs/githealth.log"
DASHBOARD_FILE="dashboard/githealth_dashboard.json"
UPDATE_STATUS="pending"
SELF_HEALING_ENABLED=true

ACCOUNT_WIDE=false
SSH_ENABLED=false
GIT_PUSH_ENABLED=false

# --- ACCOUNT CHECK ---
if [ "$CURRENT_ACCOUNT" = "$AUTHORIZED_ACCOUNT" ]; then
    echo "[Yberion] Full Account-Wide Mode enabled" | tee -a $LOGFILE
    ACCOUNT_WIDE=true; SSH_ENABLED=true; GIT_PUSH_ENABLED=true
else
    echo "[Yberion] Restricted Mode: Single-Window only" | tee -a $LOGFILE
fi

# --- FETCH AND CHECK DIVERGENCE ---
git fetch origin main
LOCAL_HASH=$(git rev-parse HEAD)
REMOTE_HASH=$(git rev-parse origin/main)

if [ "$LOCAL_HASH" != "$REMOTE_HASH" ]; then
    echo "[Yberion] Divergence detected. Auto backup/stash engaged." | tee -a $LOGFILE
    git stash push -m "Yberion auto backup $(date +'%F %T')"
    BACKUP_HASH=$(git rev-parse HEAD)
    UPDATE_STATUS="divergent"
else
    BACKUP_HASH=$LOCAL_HASH
    UPDATE_STATUS="up-to-date"
fi

# --- SELF-HEALING ---
if $SELF_HEALING_ENABLED && [ "$UPDATE_STATUS" = "divergent" ]; then
    echo "[Yberion] Performing self-healing operations..." | tee -a $LOGFILE
    git pull --rebase origin main || git merge origin/main
    echo "[Yberion] Self-healing complete" | tee -a $LOGFILE
fi

# --- DASHBOARD UPDATE ---
mkdir -p dashboard
cat <<EOF > $DASHBOARD_FILE
{
  "local_hash": "$LOCAL_HASH",
  "remote_hash": "$REMOTE_HASH",
  "account_wide": "$ACCOUNT_WIDE",
  "ssh_enabled": "$SSH_ENABLED",
  "git_push_enabled": "$GIT_PUSH_ENABLED",
  "divergence": "$([ "$LOCAL_HASH" != "$REMOTE_HASH" ] && echo true || echo false)",
  "last_backup": "$BACKUP_HASH",
  "update_status": "$UPDATE_STATUS",
  "self_healing_enabled": "$SELF_HEALING_ENABLED"
}
EOF

echo "[Yberion] Dashboard updated at $DASHBOARD_FILE" | tee -a $LOGFILE

# --- COMMIT / PUSH ---
if $GIT_PUSH_ENABLED; then
    git add .
    COMMIT_MSG="Yberion auto-update $(date +'%F %T')"
    git commit -m "$COMMIT_MSG"
    git push origin main && UPDATE_STATUS="pushed"
    echo "[Yberion] Push complete" | tee -a $LOGFILE
else
    echo "[Yberion] Push blocked for unauthorized account" | tee -a $LOGFILE
fi

echo "[Yberion] Nexus Autoupdater finished. Status: $UPDATE_STATUS" | tee -a $LOGFILE
