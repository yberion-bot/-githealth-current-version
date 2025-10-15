#!/bin/bash
DASHBOARD_FILE="dashboard/githealth_dashboard.json"
REFRESH_INTERVAL=3

display_dashboard() {
  if [ ! -f "$DASHBOARD_FILE" ]; then
    echo "[Yberion] Dashboard file not found: $DASHBOARD_FILE"
    return
  fi

  local DASH=$(cat "$DASHBOARD_FILE")
  local ACCOUNT_WIDE=$(echo "$DASH" | jq -r '.account_wide')
  local SSH_ENABLED=$(echo "$DASH" | jq -r '.ssh_enabled')
  local GIT_PUSH_ENABLED=$(echo "$DASH" | jq -r '.git_push_enabled')
  local DIVERGENCE=$(echo "$DASH" | jq -r '.divergence')
  local UPDATE_STATUS=$(echo "$DASH" | jq -r '.update_status')
  local SELF_HEALING=$(echo "$DASH" | jq -r '.self_healing_enabled')
  local LOCAL_HASH=$(echo "$DASH" | jq -r '.local_hash')
  local REMOTE_HASH=$(echo "$DASH" | jq -r '.remote_hash')
  local LAST_BACKUP=$(echo "$DASH" | jq -r '.last_backup')

  clear
  echo "================= YBERION NEXUS DASHBOARD ================="
  echo "Account-Wide Mode : $ACCOUNT_WIDE"
  echo "SSH Enabled       : $SSH_ENABLED"
  echo "Git Push Enabled  : $GIT_PUSH_ENABLED"

  [[ "$DIVERGENCE" = true ]] && DIVERGENCE_COLOR="\e[31mDIVERGENCE DETECTED\e[0m" || DIVERGENCE_COLOR="\e[32mNo Divergence\e[0m"
  case "$UPDATE_STATUS" in
    up-to-date) STATUS_COLOR="\e[32m$UPDATE_STATUS\e[0m";;
    divergent)  STATUS_COLOR="\e[33m$UPDATE_STATUS\e[0m";;
    pushed)     STATUS_COLOR="\e[36m$UPDATE_STATUS\e[0m";;
    *)          STATUS_COLOR="$UPDATE_STATUS";;
  esac

  echo -e "Divergence        : $DIVERGENCE_COLOR"
  echo -e "Update Status     : $STATUS_COLOR"
  echo "Self-Healing      : $SELF_HEALING"
  echo "Local Hash        : $LOCAL_HASH"
  echo "Remote Hash       : $REMOTE_HASH"
  echo "Last Backup Hash  : $LAST_BACKUP"
  echo "==========================================================="
}

while true; do
  display_dashboard
  sleep $REFRESH_INTERVAL
done
