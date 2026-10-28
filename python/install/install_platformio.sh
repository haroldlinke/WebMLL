#!/usr/bin/env bash
# Datei-Version: 1.01 (2026-10-27) - install_platformio.sh (gilt fuer webMobaLedLib 2.27)
# Installiert PlatformIO fuer webMobaLedLib (Linux, macOS, Raspberry Pi): in eine eigene Python-Umgebung ~/.platformio/penv,
# genau dort, wo auch der Installer von platformio.org sie anlegt und wo das Programm "pio" von selbst findet.
# Das geht auch auf Debian, Ubuntu und Raspberry Pi OS, wo "pip install platformio" ausserhalb einer Umgebung nicht erlaubt ist
# (Meldung "externally-managed-environment"); pipx ist nicht noetig.
#
# Aufruf (als normaler Benutzer, ohne sudo):    bash install_platformio.sh
# Die Installationsskripte rufen es mit der Option --with-platformio auf (install_linux.sh, install_mac.command, pi/install_pi.sh).
# Danach in der Oberflaeche die Entwicklungsumgebung einstellen: Optionen, Optionen und spezielle Funktionen, Entwicklungsumgebung.
#
# Umgebungsvariablen (nur fuer Sonderfaelle und Tests):
#   MLL_PIO_HOME      Ordner von PlatformIO (Standard ~/.platformio)
#   MLL_PYTHON        zu benutzendes Python (Standard: das neueste Python 3.10 oder neuer)
#   MLL_PIO_PIP_ARGS  zusaetzliche Optionen fuer pip install (zum Beispiel --index-url ...); pip wird dann nicht aktualisiert
set -u

PIO_HOME="${MLL_PIO_HOME:-$HOME/.platformio}"
PENV="$PIO_HOME/penv"
PIO="$PENV/bin/pio"

echo
echo "PlatformIO (Ersatz fuer die ARDUINO IDE)"

# 1. Schon vorhanden? (eigene Umgebung, pipx oder im Pfad)
for c in "$PIO" "$HOME/.local/bin/pio"; do
  if [ -x "$c" ]; then
    echo "PlatformIO ist schon installiert: $c ($("$c" --version 2>&1 | head -1))"
    exit 0
  fi
done
if command -v pio >/dev/null 2>&1; then
  echo "PlatformIO ist schon installiert: $(command -v pio) ($(pio --version 2>&1 | head -1))"
  exit 0
fi

# 2. Python 3.10 oder neuer
PY="${MLL_PYTHON:-}"
if [ -z "$PY" ]; then
  for c in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then PY="$(command -v "$c")"; break; fi
  done
fi
if [ -z "$PY" ]; then
  echo "FEHLER: Python 3.10 oder neuer wurde nicht gefunden (PlatformIO braucht ein Python mit venv und pip)."
  exit 1
fi

# 3. Eigene Python-Umgebung und PlatformIO
echo "Python:     $PY ($("$PY" --version 2>&1))"
echo "Umgebung:   $PENV"
mkdir -p "$PIO_HOME" || { echo "FEHLER: Der Ordner $PIO_HOME kann nicht angelegt werden."; exit 1; }
if [ ! -x "$PENV/bin/python" ]; then
  rm -rf "$PENV"                                           # eine unvollstaendige Umgebung eines frueheren Versuchs entfernen
  "$PY" -m venv "$PENV" || { echo "FEHLER: venv fehlgeschlagen. Debian, Ubuntu, Raspberry Pi OS: sudo apt install python3-venv"; exit 1; }
fi
echo "PlatformIO installieren (das dauert einige Minuten) ..."
if [ -z "${MLL_PIO_PIP_ARGS:-}" ]; then
  "$PENV/bin/python" -m pip install --upgrade pip || { echo "FEHLER: pip konnte nicht aktualisiert werden (kein Internet?)."; exit 1; }
fi
# shellcheck disable=SC2086
if ! "$PENV/bin/python" -m pip install --prefer-binary ${MLL_PIO_PIP_ARGS:-} platformio; then
  echo
  echo "FEHLER beim Installieren von PlatformIO (siehe oben). Ursachen: kein Internet, 32-Bit-System oder Python zu alt oder zu neu fuer ein Paket."
  echo "Diagnose, bitte mitschicken: Prozessor $(uname -m), $("$PENV/bin/python" --version 2>&1), pip $("$PENV/bin/python" -m pip --version 2>&1 | cut -d' ' -f1-2)"
  exit 1
fi
if [ ! -x "$PIO" ]; then
  echo "FEHLER: Nach der Installation fehlt $PIO."
  exit 1
fi

echo
echo "PlatformIO ist installiert: $PIO ($("$PIO" --version 2>&1 | head -1))"
echo "Als Entwicklungsumgebung einstellen: Optionen, Optionen und spezielle Funktionen, Entwicklungsumgebung (PlatformIO pruefen zeigt den Stand)."
echo "Das erste Hochladen laedt die Compiler und Bibliotheken nach (Internet noetig): etwa 5 Minuten beim Nano, etwa 10 Minuten beim Pico. Danach geht es schnell."
if [ "$(uname)" = "Linux" ]; then
  echo "Raspberry Pi Pico am USB: einmalig  sudo bash $(cd "$(dirname "$0")" && pwd)/install_pico_udev.sh  (Zugriffsrecht fuer den Bootloader)."
fi
exit 0
