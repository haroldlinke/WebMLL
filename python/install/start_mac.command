#!/bin/bash
# Datei-Version: 1.01 (2026-10-13) - start_mac.command
# Startet die Web-Oberflaeche von pyMobaLedLib im Terminalfenster und oeffnet den Browser. Laeuft sie schon, wird nur der
# Browser geoeffnet. Beenden: Knopf "Beenden" in der Oberflaeche.
cd "$(dirname "$0")/.." || exit 1
if [ ! -x venv_web/bin/python ]; then
  echo "Die Installation fehlt. Bitte zuerst install/install_mac.command ausfuehren."; read -r -p "Enter ..." _; exit 1
fi
export MLL_HEADLESS=1
exec venv_web/bin/python webmobaledlib.py --open-if-running "$@"
