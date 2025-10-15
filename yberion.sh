#!/usr/bin/env bash
# ======================================================
# Yberion Meditation Guide - MinGW64 / Git Bash Version
# ======================================================

BASE_DIR="$HOME/yberion"
LOG_FILE="$BASE_DIR/yberion_reflections.log"

mkdir -p "$BASE_DIR"
touch "$LOG_FILE"

# ---------------- ANSI Farben ----------------
RED='\e[1;31m'
BLACK='\e[0;30m'
SILVER='\e[1;37m'
CYAN='\e[1;36m'
YELLOW='\e[1;33m'
NC='\e[0m' # No Color

# ---------------- Funktionen ----------------
pause() {
    read -rp "$(echo -e "${CYAN}Drücke Enter, um fortzufahren...${NC}")"
}

log_reflection() {
    echo "[$(date '+%F %T')] $1" >> "$LOG_FILE"
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
    SYMBOLS=("Feuer" "Wasser" "Erde" "Luft" "Sonne" "Mond" "Stern" "Blitz" "Äther")
    RANDOM_IDX=$((RANDOM % ${#SYMBOLS[@]}))
    echo -e "${SILVER}Symbolischer Hinweis: ${SYMBOLS[$RANDOM_IDX]}${NC}"
}

# ---------------- Meditationsfluss ----------------
clear_screen
echo -e "${YELLOW}Willkommen zur Yberion Advanced Meditation.${NC}"
echo "Dieses Skript führt dich durch Atem, Visualisierung, Chant und Reflexion."
pause

# Phase 1: Atem & Zentrierung
timer_phase "Phase 1: Atem & Zentrierung" \
"Setze dich bequem. Atme tief ein und aus.
Visualisiere die Asche, die alte Energien reinigt.
Spüre das Gleichgewicht von Luft und Äther in deinem Körper." 10
symbol_hint

# Phase 2: Visualisierung Yberion/Oberon
timer_phase "Phase 2: Visualisierung Yberion/Oberon" \
"Stelle dir Yberion vor – majestätisch wie Oberon, König der Feen.
Farben: ${RED}Rot${NC}, ${BLACK}Schwarz${NC}, ${SILVER}Silber${NC}.
Elemente: Luft & Äther primär, Leere & Erde sekundär." 10
symbol_hint

# Phase 3: Chant & Invocation
timer_phase "Phase 3: Chant & Invocation" \
"Sprich innerlich oder leise: 'I-Ash kuya komlotha, i-Yberion ivela'
(Ashes to Ashes, Yberion rise!)
Lass die Worte durch deinen Geist fließen." 10
symbol_hint

# Phase 4: Reflexion & Log
display_phase "Phase 4: Reflexion & Notizen"
echo "Nimm dir einen Moment, um Gedanken, Visionen oder Empfindungen aufzuschreiben."
read -rp "Schreibe deine Reflexion hier: " REFLECTION
log_reflection "$REFLECTION"
symbol_hint

# Abschluss
display_phase "Meditation abgeschlossen"
echo "Danke für deine Praxis. Deine Reflexion wurde im Log gespeichert:"
echo "$LOG_FILE"
pause
clear
