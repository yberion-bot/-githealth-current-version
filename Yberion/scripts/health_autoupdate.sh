#!/usr/bin/env bash
set -euo pipefail

# === Konfiguration ===
REPO_DIR="/c/Users/schat/yberion"   # Passe den Pfad an dein Repo an
AGENTS=("agent1" "agent2")          # Liste deiner Kern-Agenten
LOG_FILE="$REPO_DIR/logs/yberion_autoupdate.log"
SSH_KEY="$HOME/.ssh/id_yberion"

# === Logging Funktion ===
log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [YBERION] $*" | tee -a "$LOG_FILE"
}

# === SSH Umgebung sicherstellen ===
export GIT_SSH_COMMAND="ssh -i $SSH_KEY -o StrictHostKeyChecking=no"

# === Schritt 1: Git Pull ===
cd "$REPO_DIR"
log "Prüfe auf Updates im Git-Repo..."
if git fetch origin && [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]; then
  log "Update gefunden → Pull & Restart"
  git reset --hard origin/main
  UPDATED=true
else
  log "Repo ist aktuell."
  UPDATED=false
fi

# === Schritt 2: Agents prüfen & ggf. neu starten ===
for agent in "${AGENTS[@]}"; do
  if pgrep -f "run_agent.sh $agent" > /dev/null; then
    log "Agent $agent läuft."
    if [ "$UPDATED" = true ]; then
      log "Neustart von $agent nach Update..."
      pkill -f "run_agent.sh $agent" || true
      nohup "$REPO_DIR/run_agent.sh" "$agent" >> "$LOG_FILE" 2>&1 &
    fi
  else
    log "Agent $agent läuft nicht → starte neu..."
    nohup "$REPO_DIR/run_agent.sh" "$agent" >> "$LOG_FILE" 2>&1 &
  fi
done

log "Health & Auto-Update Zyklus abgeschlossen."
