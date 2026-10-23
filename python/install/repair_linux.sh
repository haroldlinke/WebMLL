#!/usr/bin/env bash
# Datei-Version: 1.00 (2026-10-21) - repair_linux.sh
# Prueft die Installation von webMobaLedLib und stellt fehlende oder beschaedigte Dateien aus dem Release wieder her (zum Beispiel nach einem abgebrochenen Update).
# Braucht das Programm nicht: laeuft auch, wenn webMobaLedLib nicht mehr startet. Aufruf: bash install/repair_linux.sh   (Raspberry Pi: ebenso, danach den Dienst neu starten)
# Optionen: --zip <Pfad zu webmobaledlib.zip> (ohne Internet)   --offline   --allow-older   --check-only   --yes
cd "$(dirname "$(realpath "$0")")/.." || exit 1
if [ ! -f repair.py ]; then
  echo "FEHLER: repair.py fehlt. Bitte webmobaledlib.zip von https://github.com/haroldlinke/WebMLL/releases laden und den Ordner python daraus nehmen."
  exit 1
fi
PY=""
if [ -x venv_web/bin/python ]; then PY="venv_web/bin/python"
elif [ -x venv/bin/python ]; then PY="venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
elif command -v python >/dev/null 2>&1; then PY="python"
fi
if [ -z "$PY" ]; then echo "FEHLER: Python wurde nicht gefunden. Bitte install/install_linux.sh ausfuehren oder python3 installieren."; exit 1; fi
echo "webMobaLedLib: Installation pruefen und reparieren"
echo "Das Programm sollte dabei beendet sein."
echo
"$PY" repair.py --project "$PWD" "$@"
RC=$?
echo
if [ "$RC" -eq 0 ]; then
  echo "Fertig. Bitte webMobaLedLib neu starten."
  if command -v systemctl >/dev/null 2>&1 && systemctl cat mobaledlib-web >/dev/null 2>&1; then
    echo "Raspberry Pi (Dienst):  sudo systemctl restart mobaledlib-web"
  fi
else
  echo "Die Reparatur war nicht erfolgreich. Bitte die Meldungen oben lesen."
  echo "Ohne Internet: webmobaledlib.zip von https://github.com/haroldlinke/WebMLL/releases laden und aufrufen:  bash install/repair_linux.sh --zip /Pfad/webmobaledlib.zip"
fi
exit "$RC"
