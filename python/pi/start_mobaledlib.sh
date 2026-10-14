#!/usr/bin/env bash
# Datei-Version: 1.00 (2026-10-12) - start_mobaledlib.sh
# Startet pyMobaLedLib auf dem Raspberry Pi mit einem Klick (Desktop-Symbol):
#   1. den Dienst mobaledlib-web starten, falls er nicht laeuft
#   2. warten, bis die Oberflaeche antwortet (das Laden der Blaetter dauert 20 bis 60 Sekunden)
#   3. die Oberflaeche in einem eigenen Browserfenster oeffnen
# Umgebung: MLL_BROWSER=<Programm>  waehlt einen anderen Browser.
APPDIR="$(cd "$(dirname "$(realpath "$0")")/.." && pwd)"
PORT=8080
if [ -r "$APPDIR/pi/launcher.conf" ]; then
  P="$(grep -E '^PORT=[0-9]+$' "$APPDIR/pi/launcher.conf" | tail -1 | cut -d= -f2)"
  [ -n "$P" ] && PORT="$P"
fi
URL="http://localhost:$PORT"

say() { command -v notify-send >/dev/null 2>&1 && notify-send -a pyMobaLedLib "$1" "${2:-}"; echo "$1 ${2:-}"; }
up()  { (exec 3<>"/dev/tcp/127.0.0.1/$PORT") 2>/dev/null; }

if ! up; then
  say "pyMobaLedLib wird gestartet" "Das dauert etwa eine halbe Minute."
  if ! sudo -n systemctl start mobaledlib-web 2>/dev/null; then
    say "Der Dienst konnte nicht gestartet werden" "Bitte im Terminal:  sudo systemctl start mobaledlib-web"
    exit 1
  fi
  for _ in $(seq 1 150); do up && break; sleep 1; done
fi
if ! up; then
  say "pyMobaLedLib antwortet nicht" "Siehe:  journalctl -u mobaledlib-web -e"
  exit 1
fi

if [ -n "${MLL_BROWSER:-}" ] && command -v "$MLL_BROWSER" >/dev/null 2>&1; then
  exec "$MLL_BROWSER" "$URL"
fi
for b in chromium chromium-browser; do
  if command -v "$b" >/dev/null 2>&1; then exec "$b" --app="$URL" --window-size=1400,900; fi
done
command -v firefox >/dev/null 2>&1 && exec firefox "$URL"
exec xdg-open "$URL"
