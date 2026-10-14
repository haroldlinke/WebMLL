#!/usr/bin/env bash
# Datei-Version: 1.04 (2026-10-13) - install_arduino_libs.sh
# Installiert die ARDUINO-Bibliothek MobaLedLib (FastLED vorab in der geforderten Version) in den Sketchbook-Ordner des
# aktuellen Benutzers (normalerweise ~/Arduino/libraries) und auf Wunsch die Boards fuer Pico und ESP32.
# Ohne sudo als der Benutzer starten, unter dem der Dienst laeuft (also NICHT mit sudo):
#
#   bash install_arduino_libs.sh [--pico[=VERSION]] [--esp32[=VERSION]]
#
# Danach den Dienst neu starten:  sudo systemctl restart mobaledlib-web
# Beim Start prueft das Programm die weiteren Bibliotheken und Boards und installiert fehlende selbst. Kontrolle und Korrektur
# falscher Versionen: in der Oberflaeche die Tabelle "Libraries" oeffnen (Optionen, Reiter Update, Status der Bibliotheken).
set -uo pipefail

PICO=""
ESP32=""
for a in "$@"; do
  case "$a" in
    --pico)    PICO="rp2040:rp2040" ;;
    --pico=*)  PICO="rp2040:rp2040:${a#--pico=}" ;;
    --esp32)   ESP32="esp32:esp32" ;;
    --esp32=*) ESP32="esp32:esp32:${a#--esp32=}" ;;
    -h|--help) sed -n '3,10p' "$0"; exit 0 ;;
    *) echo "Unbekannte Option: $a"; exit 1 ;;
  esac
done
if [ "$(id -u)" -eq 0 ] && [ "${MLL_ALLOW_ROOT:-0}" != "1" ]; then
  echo "Bitte ohne sudo starten, sonst landen die Bibliotheken im Ordner von root."; exit 1
fi

# 1. ARDUINO IDE finden (gleiche Reihenfolge wie das Programm)
IDE="${MLL_ARDUINO_EXE:-}"
if [ -z "$IDE" ] || [ ! -x "$IDE" ]; then
  IDE=""
  for c in /opt/arduino-1.8*/arduino /opt/arduino*/arduino /usr/local/arduino*/arduino "$HOME"/arduino-1.8*/arduino "$HOME"/arduino*/arduino; do
    if [ -x "$c" ]; then IDE="$c"; break; fi
  done
fi
[ -z "$IDE" ] && IDE="$(command -v arduino || true)"
if [ -z "$IDE" ] || [ ! -x "$IDE" ]; then
  echo "Die ARDUINO IDE wurde nicht gefunden. Installieren mit:  sudo bash install_pi.sh --with-arduino-ide"
  echo "(oder den Pfad der Startdatei 'arduino' in MLL_ARDUINO_EXE angeben)"; exit 1
fi
echo "ARDUINO IDE: $IDE"

# Die IDE (Java) braucht ein Display: ohne eigenes ein virtuelles benutzen
if [ -z "${DISPLAY:-}" ] && command -v xvfb-run >/dev/null 2>&1; then
  RUN=(xvfb-run -a "$IDE")
else
  RUN=("$IDE")
fi

# 1a. Einstellungsdatei der IDE anlegen, falls sie fehlt. Die IDE legt sie erst beim ersten Start mit Oberflaeche an; das Programm
# liest daraus den Sketchbook-Ordner und meldet sonst "Fehler beim Lesen der Datei .../preferences.txt".
PREFS="$HOME/.arduino15/preferences.txt"
mkdir -p "$HOME/.arduino15" "$HOME/Arduino/libraries"
if [ ! -f "$PREFS" ]; then
  printf 'sketchbook.path=%s/Arduino\ntarget_package=arduino\ntarget_platform=avr\nboard=uno\n' "$HOME" > "$PREFS"
  echo "Einstellungsdatei der IDE angelegt: $PREFS"
elif ! grep -q '^sketchbook.path=' "$PREFS"; then
  printf 'sketchbook.path=%s/Arduino\n' "$HOME" >> "$PREFS"
fi

# 1b. Board-Auswahl der IDE zuruecksetzen. Steht in ~/.arduino15/preferences.txt ein Board, das nicht (mehr) installiert ist
# (zum Beispiel rp2040:rp2040), stuerzt die IDE bei --install-boards / --install-library mit
# "NullPointerException at processing.app.BaseNoGui.onBoardOrPortChange" ab. arduino:avr:uno ist immer vorhanden.
if [ -f "$PREFS" ]; then
  if ! grep -qx 'board=uno' "$PREFS" || grep -qE '^custom_' "$PREFS" || ! grep -qx 'target_package=arduino' "$PREFS"; then
    [ -f "$PREFS.mll-backup" ] || cp "$PREFS" "$PREFS.mll-backup"
    sed -i -E '/^(target_package|target_platform|board|custom_[A-Za-z0-9_.]+)=/d' "$PREFS"
    printf 'target_package=arduino\ntarget_platform=avr\nboard=uno\n' >> "$PREFS"
    echo "Board-Auswahl der IDE auf arduino:avr:uno zurueckgesetzt (Sicherung: $PREFS.mll-backup)"
  fi
fi

# 2. Bibliothek MobaLedLib. Wichtig: Die IDE installiert fehlende Abhaengigkeiten (FastLED, ...) immer in der NEUESTEN Version,
# die Programmerzeugung verlangt aber bestimmte Versionen (Tabelle "Libraries": Spalten installierte und geforderte Version).
# Deshalb zuerst FastLED in der geforderten Version, dann MobaLedLib (vorhandene Bibliotheken fasst die IDE nicht an).
# Alle weiteren Bibliotheken installiert das Programm beim Start in der geforderten Version selbst.
FASTLED_VERSION="${MLL_FASTLED_VERSION:-3.9.12}"          # bei Bedarf anpassen: die Tabelle "Libraries" nennt die geforderte Version
echo; echo "Installiere FastLED $FASTLED_VERSION und danach MobaLedLib"
echo "(Download der Bibliotheksliste und der Pakete, das dauert einige Minuten)"
timeout 1800 "${RUN[@]}" --install-library "FastLED:$FASTLED_VERSION"
RC=$?
timeout 1800 "${RUN[@]}" --install-library "MobaLedLib"
RC2=$?
[ $RC -ne 0 ] || [ $RC2 -ne 0 ] && echo "Die IDE meldete Rueckgabewerte $RC / $RC2 (siehe Ausgabe oben)."

# 3. Boards (optional)
if [ -n "$PICO$ESP32" ]; then
  URLS=""
  [ -n "$PICO" ]  && URLS="https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json"
  [ -n "$ESP32" ] && URLS="${URLS:+$URLS,}https://espressif.github.io/arduino-esp32/package_esp32_index.json"
  echo; echo "Trage die Boardverwalter-URLs ein"
  timeout 300 "${RUN[@]}" --pref "boardsmanager.additional.urls=$URLS" --save-prefs
  for board in $PICO $ESP32; do
    echo; echo "Installiere das Board $board (gross, dauert)"
    timeout 3600 "${RUN[@]}" --install-boards "$board" || echo "Board $board: Rueckgabewert $? (siehe Ausgabe oben)"
  done
fi

# 4. Pruefen, ob die Bibliothek da ist
SKETCHBOOK="$(grep -E '^sketchbook.path=' "$HOME/.arduino15/preferences.txt" 2>/dev/null | tail -1 | cut -d= -f2-)"
SKETCHBOOK="${SKETCHBOOK:-$HOME/Arduino}"
PROP="$SKETCHBOOK/libraries/MobaLedLib/library.properties"
echo
if [ -f "$PROP" ]; then
  echo "OK: MobaLedLib $(grep -E '^version=' "$PROP" | cut -d= -f2) in $SKETCHBOOK/libraries"
  if systemctl cat mobaledlib-web >/dev/null 2>&1; then                     # nur auf einem Pi mit eingerichtetem Dienst
    echo "Dienst neu starten:  sudo systemctl restart mobaledlib-web"
  fi
else
  echo "FEHLT: $PROP nicht gefunden. Pruefe die Ausgabe oben (Internetverbindung? Speicherplatz?)."
  echo "Von Hand:  mkdir -p $SKETCHBOOK/libraries && cd $SKETCHBOOK/libraries && git clone https://github.com/Hardi-St/MobaLedLib"
  exit 1
fi
