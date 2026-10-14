#!/usr/bin/env bash
# Datei-Version: 1.03 (2026-10-14) - start_linux.sh
# Startet die Web-Oberflaeche von pyMobaLedLib und oeffnet den Browser. Laeuft sie schon, wird nur der Browser geoeffnet.
# Beenden: Knopf "Beenden" in der Oberflaeche. Meldungen: webmobaledlib.log und webmobaledlib-console.log im Datenordner (Ort: venv_web/bin/python userdata.py).
cd "$(dirname "$(realpath "$0")")/.." || exit 1
if [ ! -x venv_web/bin/python ]; then
  msg="Die Installation fehlt. Bitte zuerst install/install_linux.sh ausfuehren."
  echo "$msg"; command -v notify-send >/dev/null 2>&1 && notify-send -a pyMobaLedLib "pyMobaLedLib" "$msg"; exit 1
fi
export MLL_HEADLESS=1
if [ -t 1 ]; then                                  # im Terminal gestartet: Meldungen anzeigen
  exec venv_web/bin/python webmobaledlib.py --open-if-running "$@"
fi
DATA="$(venv_web/bin/python userdata.py 2>/dev/null || echo "$HOME")"      # Datenordner ausserhalb des Projektordners
exec venv_web/bin/python webmobaledlib.py --open-if-running "$@" >> "$DATA/webmobaledlib-console.log" 2>&1     # per Symbol gestartet
