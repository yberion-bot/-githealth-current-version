#!/usr/bin/env bash
# =========================================
# Yberion Multiagent Git Push + Meditation
# Final MinGW64 Version
# =========================================

BASE_DIR="$HOME/yberion"
WORK_DIR="$BASE_DIR/working"
ARCHIVE_DIR="$BASE_DIR/patchnode_archive"
LOG_FILE="$BASE_DIR/yberion_reflections.log"
DASHBOARD_FILE="$BASE_DIR/dashboard.json"

mkdir -p "$WORK_DIR" "$ARCHIVE_DIR" "$BASE_DIR"
touch "$LOG_FILE" "$DASHBOARD_FILE"

# ---------------- ANSI Farben ----------------
RED='\033[1;31m'
BLACK='\033[0;30m'
SILVER='\033[1;37m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ---------------- Funktionen ----------------
pause() {
  read -rp "${CYAN}Drücke Enter, um fortzufahren...${NC}"
}

log_reflection() {
  echo "[$(date +'%F %T')] $1" >> "$LOG_FILE"
}

clear_screen() {
  clear
  echo -e "${YELLOW}=== YBERION IMMERSIVE MEDITATION ===${NC}"
  echo ""
}

display_phase() {
  echo -e "${CYAN}--------------------------------------------------${NC}"
  echo -e "$1"
  echo -e "${CYAN}--------------------------------------------------${NC}"
}

timer_phase() {
  local PHASE_TITLE="$1"
  local PHASE_TEXT="$2"
  local DURATION="$3"

  display_phase "${PHASE_TITLE} (Dauer: ${DURATION}s)"
  echo -e "$PHASE_TEXT"
  echo ""

  for ((i=DURATION; i>0; i--)); do
    echo -ne "\rVerbleibende Zeit: ${i}s"
    sleep 1
  done
  echo -e "\n${CYAN}Phase abgeschlossen.${NC}"
  pause
}

symbol_hint() {
  SYMBOLS=("🜂 Feuer" "🜄 Wasser" "🜃 Erde" "🜁 Luft" "☀ Sonne" "☾ Mond" "☆ Stern" "⚡ Blitz" "🜚 Äther")
  local RANDOM_IDX=$((RANDOM % ${#SYMBOLS[@]}))
  echo -e "${SILVER}Symbolischer Hinweis: ${SYMBOLS[$RANDOM_IDX]}${NC}"
}

update_dashboard() {
  PATCHNODES=""
  for FILE in "$WORK_DIR"/*; do
    [ -f "$FILE" ] || continue
    PATCHNODES="$PATCHNODES $(basename "$FILE")"
  done
  ARCHIVE_LATEST=$(ls -1t "$ARCHIVE_DIR" 2>/dev/null | head -n1 || echo "N/A")
  echo -e "PATCHNODES: $PATCHNODES\nARCHIVE: $ARCHIVE_LATEST" > "$DASHBOARD_FILE"
}

self_heal() {
  for FILE in "$WORK_DIR"/*; do
    [ -f "$FILE" ] || continue
    BASENAME=$(basename "$FILE")
    BACKUP_FILE=$(ls "$ARCHIVE_DIR" | grep "$BASENAME" | sort | tail -n1)
    [[ -f "$ARCHIVE_DIR/$BACKUP_FILE" ]] && cp "$ARCHIVE_DIR/$BACKUP_FILE" "$WORK_DIR/$BASENAME"
  done
  log_reflection "Self-Healing ausgeführt"
}

auto_yes_flow() {
  log_reflection "=== Starte Auto-Yes Multi-Agent Flow ==="
  AGENTS=("Junior" "Senior" "Kal_El" "Task_Overflow")

  for AGENT in "${AGENTS[@]}"; do
    log_reflection "[$AGENT] Prüfe Tasks..."
    TASKS=$(ls "$WORK_DIR" | head -n3)
    for TASK in $TASKS; do
      log_reflection "[$AGENT] Task $TASK -> Auto-Yes bestätigt"
      echo "[$AGENT] Task $TASK -> ✅"

      BACKUP=$(ls "$ARCHIVE_DIR" | grep "$TASK" | sort | tail -n1)
      [[ -f "$BACKUP" ]] && cp "$ARCHIVE_DIR/$BACKUP" "$WORK_DIR/$TASK" && log_reflection "[$AGENT] Task $TASK self-healed aus Backup"
    done
  done

  if git diff-index --quiet HEAD --; then
    git add "$WORK_DIR"/*
    git commit -m "Auto-Yes Flow Commit"
    git push origin main
    log_reflection "[Git] Auto-Push erfolgreich"
  else
    log_reflection "[Git] Lokale Änderungen vorhanden – Auto-Push übersprungen"
  fi
  log_reflection "=== Auto-Yes Multi-Agent Flow abgeschlossen ==="
}

draw_dashboard() {
  clear_screen
  echo -e "${YELLOW}=== YBERION NEXUS DASHBOARD ===${NC}"
  update_dashboard
  cat "$DASHBOARD_FILE"
  echo -e "${CYAN}Commands: exit, heal, list, diff <file>, log${NC}"
  echo -e "================================================================="
}

# ================= START =================
log_reflection "Yberion Nexus aktiviert (MinGW64 Version)"

# Initial Dashboard & Meditation Flow
draw_dashboard

# Meditation & Reflection Example
echo -e "${YELLOW}Willkommen zur Yberion Advanced Meditation.${NC}"
echo -e "Dieses Skript führt dich durch Atem, Visualisierung, Chant und Reflexion."
pause

timer_phase "Phase 1: Atem & Zentrierung" \
"Setze dich bequem. Atme tief ein und aus.
Visualisiere die Asche, die alte Energien reinigt.
Spüre das Gleichgewicht von Luft und Äther in deinem Körper." 10
symbol_hint

timer_phase "Phase 2: Visualisierung Yberion/Oberon" \
"Stelle dir Yberion vor – majestätisch wie Oberon, König der Feen.
Farben: ${RED}Rot${NC}, ${BLACK}Schwarz${NC}, ${SILVER}Silber${NC}.
Elemente: Luft & Äther primär, Leere & Erde sekundär." 10
symbol_hint

timer_phase "Phase 3: Chant & Invocation" \
"Sprich innerlich oder leise:
${RED}'I-Ash kuya komlotha, i-Yberion ivela'${NC}
(Ashes to Ashes, Yberion rise!)
Lass die Worte durch deinen Geist fließen." 10
symbol_hint

display_phase "Phase 4: Reflexion & Notizen"
read -rp "Schreibe deine Reflexion hier: " REFLECTION
log_reflection "$REFLECTION"
symbol_hint

display_phase "Meditation abgeschlossen"
echo "Danke für deine Praxis. Deine Reflexion wurde im Log gespeichert:"
echo "$LOG_FILE"
pause

# Multi-Agent Auto-Yes Flow
auto_yes_flow

# Letztes Dashboard Update
draw_dashboard
