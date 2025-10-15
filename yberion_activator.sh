#!/usr/bin/env bash
# ======================================================
# Yberion Activator (MinGW64 / Git Bash) - optimized single script
# ======================================================

# --- Safety / compat ---
set +H                # disable history expansion (avoids "!" problems)
shopt -s expand_aliases 2>/dev/null || true

# --- Paths & Init ---
BASE_DIR="$HOME/yberion"
LOG_FILE="$BASE_DIR/yberion_reflections.log"

mkdir -p "$BASE_DIR" 2>/dev/null || true
: > "$LOG_FILE" 2>/dev/null || true   # ensure log file exists (truncate)

# --- ANSI colors (fallback safe) ---
RED='\e[1;31m'
BLACK='\e[0;30m'
SILVER='\e[1;37m'
CYAN='\e[1;36m'
YELLOW='\e[1;33m'
NC='\e[0m'

# --- Utilities ---
pause() {
  # portable prompt for Git Bash / MinGW64
  printf "%b" "${CYAN}Drücke Enter, um fortzufahren...${NC}"
  IFS= read -r _
}

log_reflection() {
  # $1 = text
  if [ -n "$1" ]; then
    printf "[%s] %s\n" "$(date '+%F %T')" "$1" >> "$LOG_FILE"
  fi
}

clear_screen() {
  # try clear, fallback to printing newlines
  if command -v clear >/dev/null 2>&1; then
    clear
  else
    printf '\n%.0s' {1..20}
  fi
}

display_phase() {
  printf "%b\n" "${CYAN}--------------------------------------------------${NC}"
  printf "%b\n" "$1"
  printf "%b\n" "${CYAN}--------------------------------------------------${NC}"
}

# --- Timer with clean single-line refresh ---
timer_phase() {
  PHASE_TITLE="$1"
  PHASE_TEXT="$2"
  DURATION="$3"

  display_phase "${PHASE_TITLE} (Dauer: ${DURATION}s)"
  printf "%b\n\n" "$PHASE_TEXT"

  # loop with formatted, fixed-width output to avoid residue chars
  i=$DURATION
  while [ "$i" -gt 0 ]; do
    # clear line then print (use printf with \r and pad spaces)
    printf "\rVerbleibende Zeit: %3ds   " "$i"
    sleep 1
    i=$((i - 1))
  done
  # finish line and newline
  printf "\rVerbleibende Zeit:   0s   \n"
  printf "%b\n" "${CYAN}Phase abgeschlossen.${NC}"
  pause
}

# --- Random symbolic hint (no fancy emoji to be safer) ---
symbol_hint() {
  SYMBOLS=("Feuer" "Wasser" "Erde" "Luft" "Sonne" "Mond" "Stern" "Blitz" "Äther")
  # number of elements
  LEN=${#SYMBOLS[@]}
  if [ "$LEN" -gt 0 ]; then
    IDX=$((RANDOM % LEN))
    printf "%b\n" "${SILVER}Symbolischer Hinweis: ${SYMBOLS[$IDX]}${NC}"
  fi
}

# --- Main flow ---
clear_screen
printf "%b\n" "${YELLOW}=== YBERION IMMERSIVE MEDITATION (MinGW64) ===${NC}"
printf "\nDieses Skript führt dich durch Atem, Visualisierung, Chant und Reflexion.\n\n"
pause

# Phase 1
timer_phase "Phase 1: Atem & Zentrierung" \
"Setze dich bequem. Atme tief ein und aus.
Visualisiere die Asche, die alte Energien reinigt.
Spüre das Gleichgewicht von Luft und Äther in deinem Körper." 12
symbol_hint
printf "\n"

# Phase 2
timer_phase "Phase 2: Visualisierung Yberion/Oberon" \
"Stelle dir Yberion vor – majestätisch wie Oberon, König der Feen.
Farben: Rot, Schwarz, Silber.
Elemente: Luft & Äther primär, Leere & Erde sekundär." 15
symbol_hint
printf "\n"

# Phase 3 (avoid history expansion issues by disabling ! already)
timer_phase "Phase 3: Chant & Invocation" \
"Sprich innerlich oder leise: 'I-Ash kuya komlotha, i-Yberion ivela'
(Ashes to Ashes, Yberion rise!)
Lass die Worte durch deinen Geist fließen." 12
symbol_hint
printf "\n"

# Phase 4 - Reflection
display_phase "Phase 4: Reflexion & Notizen"
printf "%b\n" "Nimm dir einen Moment, um Gedanken, Visionen oder Empfindungen aufzuschreiben."
# read with a prompt
printf "%b" "${CYAN}Schreibe deine Reflexion hier: ${NC}"
IFS= read -r REFLECTION
if [ -n "$REFLECTION" ]; then
  log_reflection "$REFLECTION"
  printf "%b\n" "${SILVER}Reflexion gespeichert in: ${LOG_FILE}${NC}"
else
  printf "%b\n" "${SILVER}Keine Reflexion eingegeben.${NC}"
fi
symbol_hint
printf "\n"

# Abschluss
display_phase "Meditation abgeschlossen"
printf "%b\n" "Danke für deine Praxis. Deine Reflexion (falls vorhanden) wurde im Log gespeichert:"
printf "%s\n\n" "$LOG_FILE"
pause
clear_screen

# --- exit cleanly ---
printf "%b\n" "${YELLOW}Yberion Activator beendet. Möge die Weisheit mit dir gehen.${NC}"
exit 0
