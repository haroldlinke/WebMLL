#!/usr/bin/env bash
# Datei-Version: 1.00 (2026-10-12) - start_linux.sh
# Startet die Web-Oberflaeche von pyMobaLedLib und oeffnet den Browser. Laeuft sie schon, wird nur der Browser geoeffnet.
# Beenden: Knopf "Beenden" in der Oberflaeche. Meldungen: headless.log (und headless-console.log im Projektordner).
cd "$(dirname "$(realpath "$0")")/.." || exit 1
if [ ! -x venv_web/bin/python ]; then
  msg="Die Installation fehlt. Bitte zuerst install/install_linux.sh ausfuehren."
  echo "$msg"; command -v notify-send >/dev/null 2>&1 && notify-send -a pyMobaLedLib "pyMobaLedLib" "$msg"; exit 1
fi
export MLL_HEADLESS=1
if [ -t 1 ]; then                                  # im Terminal gestartet: Meldungen anzeigen
  exec venv_web/bin/python headless_web.py --open-if-running "$@"
fi
exec venv_web/bin/python headless_web.py --open-if-running "$@" >> headless-console.log 2>&1     # per Symbol gestartet
