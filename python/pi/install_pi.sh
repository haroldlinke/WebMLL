#!/usr/bin/env bash
# Datei-Version: 1.08 (2026-10-15) - install_pi.sh
# Installiert die Web-Oberflaeche von pyMobaLedLib als Dienst (systemd) auf einem Raspberry Pi (Raspberry Pi OS Bookworm/Trixie)
# oder einem anderen Debian/Ubuntu und legt ein Desktop-Symbol zum Starten an.
#
# Aufruf im Ordner "pi" des Projekts:   sudo bash install_pi.sh [Optionen]
#   --port N            Port der Oberflaeche (Standard 8080)
#   --hostname NAME     Rechnername des Pi aendern (zum Beispiel webMLLraspi): erreichbar als http://NAME.local:8080
#                       (spaeter auch im Programm aenderbar: Programm Einstellungen, Name des Raspberry Pi im Netz)
#   --local-only        nur auf dem Pi selbst erreichbar (127.0.0.1), kein Passwort noetig
#   --password PW       Passwort fuer den Zugriff aus dem Netz (Voreinstellung: mobaledlib; spaeter im Programm aenderbar:
#                       Programm Einstellungen, Zugriff ueber das Netz)
#   --with-arduino-ide  ARDUINO IDE 1.8.19 herunterladen und nach /opt/arduino-1.8.19 installieren
#                       (installiert danach auch die Bibliothek MobaLedLib samt Abhaengigkeiten)
#   --with-arduino-libs nur die Bibliothek MobaLedLib samt Abhaengigkeiten installieren (IDE ist schon da)
#   --desktop-icon      Desktop-Symbol auch ohne erkannten Desktop anlegen
#   --no-desktop-icon   kein Desktop-Symbol
#   --no-check          den Test der Installation (pi_check.py) ueberspringen
set -euo pipefail

PORT=8080
LOCAL_ONLY=0
PASSWORD=""
NEWHOST=""
RUN_CHECK=1
WITH_IDE=0
WITH_LIBS=0
DESKTOP_ICON=auto
while [ $# -gt 0 ]; do
  case "$1" in
    --port) PORT="$2"; shift 2 ;;
    --local-only) LOCAL_ONLY=1; shift ;;
    --password) PASSWORD="$2"; shift 2 ;;
    --hostname) NEWHOST="$2"; shift 2 ;;
    --with-arduino-ide) WITH_IDE=1; WITH_LIBS=1; shift ;;
    --with-arduino-libs) WITH_LIBS=1; shift ;;
    --desktop-icon) DESKTOP_ICON=1; shift ;;
    --no-desktop-icon) DESKTOP_ICON=0; shift ;;
    --no-check) RUN_CHECK=0; shift ;;
    -h|--help) sed -n '3,19p' "$0"; exit 0 ;;
    *) echo "Unbekannte Option: $1"; exit 1 ;;
  esac
done

if [ "$(id -u)" -ne 0 ]; then exec sudo -E bash "$0" "$@"; fi
SERVICE_USER="${SUDO_USER:-}"
if [ -z "$SERVICE_USER" ] || [ "$SERVICE_USER" = "root" ]; then
  echo "Bitte als normaler Benutzer mit  sudo bash install_pi.sh  starten (der Dienst laeuft unter diesem Benutzer)."; exit 1
fi
USER_HOME="$(getent passwd "$SERVICE_USER" | cut -d: -f6)"
APPDIR="$(cd "$(dirname "$(realpath "$0")")/.." && pwd)"
if [ ! -f "$APPDIR/webmobaledlib.py" ]; then
  echo "webmobaledlib.py nicht gefunden in $APPDIR - liegt der Ordner pi im Projektordner (neben webmobaledlib.py)?"; exit 1
fi
# Windows-Zeilenenden (CRLF) in den Skripten und Vorlagen entfernen (kommen vom Kopieren/Git unter Windows)
sed -i 's/\r$//' "$APPDIR"/pi/*.sh "$APPDIR"/pi/*.service "$APPDIR"/pi/*.example "$APPDIR"/pi/*.in "$APPDIR"/pi/*.txt "$APPDIR"/pi/mobaledlib-set-hostname 2>/dev/null || true

. /etc/os-release 2>/dev/null || true
echo "System:        ${PRETTY_NAME:-unbekannt} ($(uname -m))"
echo "Projektordner: $APPDIR"
echo "Benutzer:      $SERVICE_USER      Port: $PORT"

echo; echo "== 1/8  Systempakete"
apt-get update
apt-get install -y python3 python3-venv python3-pip xvfb curl xz-utils avahi-daemon
systemctl enable --now avahi-daemon >/dev/null 2>&1 || true          # macht den Pi im Netz unter <Rechnername>.local erreichbar (mDNS)
# Hilfsprogramm zum Aendern des Rechnernamens: gehoert root und liegt ausserhalb des Projektordners, damit der Dienstbenutzer es
# nicht veraendern kann. Die Oberflaeche ruft es ueber sudo auf (Programm Einstellungen: Name des Raspberry Pi im Netz).
HOSTNAME_HELPER=/usr/local/sbin/mobaledlib-set-hostname
install -m 755 -o root -g root "$APPDIR/pi/mobaledlib-set-hostname" "$HOSTNAME_HELPER"
if [ -n "$NEWHOST" ]; then
  OLDHOST="$(hostname)"
  "$HOSTNAME_HELPER" "$NEWHOST" || { echo "Der Rechnername wurde nicht geaendert."; exit 1; }
  echo "Rechnername: $OLDHOST -> $NEWHOST"
fi
# Bibliotheken, die die Java-IDE braucht (einzeln, damit ein anderer Paketname die Installation nicht abbricht)
for pkg in libxtst6 libxrender1 libxi6 libfontconfig1; do
  apt-get install -y "$pkg" || echo "  (Paket $pkg nicht installiert: nur wichtig, falls die ARDUINO IDE fehlende Bibliotheken meldet)"
done
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' || { echo "Python 3.10 oder neuer ist noetig."; exit 1; }
echo "Python:        $(python3 --version)"

echo; echo "== 2/8  Python-Umgebung $APPDIR/venv"
sudo -u "$SERVICE_USER" python3 -m venv "$APPDIR/venv"
sudo -u "$SERVICE_USER" "$APPDIR/venv/bin/pip" install --upgrade pip
sudo -u "$SERVICE_USER" "$APPDIR/venv/bin/pip" install --prefer-binary -r "$APPDIR/pi/requirements-pi.txt"

echo; echo "== 3/8  Zugriff auf die seriellen Anschluesse (Gruppe dialout)"
usermod -aG dialout "$SERVICE_USER"

echo; echo "== 4/8  Einstellungen /etc/mobaledlib-web.env"
ENVFILE=/etc/mobaledlib-web.env
if [ -f "$ENVFILE" ]; then
  echo "Vorhanden, bleibt unveraendert. (Aendern mit: sudo nano $ENVFILE)"
  if ! grep -q '^MLL_ALLOW_SHUTDOWN=' "$ENVFILE"; then
    echo 'MLL_ALLOW_SHUTDOWN=1' >> "$ENVFILE"                       # Menue "Raspberry Pi herunterfahren" in der Oberflaeche
    echo "MLL_ALLOW_SHUTDOWN=1 ergaenzt (Menue Datei: Raspberry Pi herunterfahren)"
  fi
  PORT="$(grep -E '^MLL_PORT=[0-9]+$' "$ENVFILE" | tail -1 | cut -d= -f2 || true)"; PORT="${PORT:-8080}"
else
  if [ "$LOCAL_ONLY" = "1" ]; then
    printf 'MLL_HOST=127.0.0.1\nMLL_PORT=%s\nMLL_ALLOW_SHUTDOWN=1\n' "$PORT" > "$ENVFILE"
  else
    if [ -z "$PASSWORD" ]; then PASSWORD="mobaledlib"; PASSWORD_INFO="mobaledlib  (Standardpasswort, im Programm aenderbar: Programm Einstellungen - Zugriff ueber das Netz)"
    else PASSWORD_INFO="$PASSWORD  (aus --password; im Programm aenderbar: Programm Einstellungen - Zugriff ueber das Netz)"; fi
    printf 'MLL_HOST=0.0.0.0\nMLL_PORT=%s\nMLL_USER=mobaledlib\nMLL_PASSWORD=%s\nMLL_ALLOW_SHUTDOWN=1\n' "$PORT" "$PASSWORD" > "$ENVFILE"
  fi
  chmod 600 "$ENVFILE"
fi

echo; echo "== 5/8  Starter fuer das Desktop-Symbol"
chmod 755 "$APPDIR/pi/start_mobaledlib.sh"
printf 'PORT=%s\n' "$PORT" > "$APPDIR/pi/launcher.conf"          # der Starter darf /etc/mobaledlib-web.env (Passwort) nicht lesen
chown "$SERVICE_USER": "$APPDIR/pi/launcher.conf"
# Der Benutzer darf den Dienst ohne Passwort starten, anhalten und neu starten (sonst nichts)
SYSTEMCTL="$(command -v systemctl)"
SUDOERS_TMP="$(mktemp)"
echo "$SERVICE_USER ALL=(root) NOPASSWD: $SYSTEMCTL start mobaledlib-web, $SYSTEMCTL stop mobaledlib-web, $SYSTEMCTL restart mobaledlib-web, $SYSTEMCTL poweroff, $SYSTEMCTL reboot, $HOSTNAME_HELPER *" > "$SUDOERS_TMP"
if visudo -cf "$SUDOERS_TMP" >/dev/null 2>&1; then
  install -m 440 -o root -g root "$SUDOERS_TMP" /etc/sudoers.d/mobaledlib-web
  echo "sudo-Regel angelegt: Dienst starten/anhalten/neu starten sowie den Raspberry Pi herunterfahren/neu starten"
else
  echo "sudo-Regel ungueltig, uebersprungen (das Symbol kann den Dienst dann nicht selbst starten)"
fi
rm -f "$SUDOERS_TMP"

echo; echo "== 6/8  Desktop-Symbol"
create_desktop_icon() {
  local desktop_dir d target
  desktop_dir="$USER_HOME/Desktop"
  if command -v xdg-user-dir >/dev/null 2>&1; then
    d="$(sudo -u "$SERVICE_USER" env HOME="$USER_HOME" xdg-user-dir DESKTOP 2>/dev/null || true)"
    if [ -n "$d" ] && [ "$d" != "$USER_HOME" ]; then desktop_dir="$d"; fi
  fi
  if [ "$DESKTOP_ICON" = "0" ]; then echo "uebersprungen (--no-desktop-icon)"; return; fi
  if [ ! -d "$desktop_dir" ] && [ "$DESKTOP_ICON" != "1" ]; then
    echo "Kein Desktop-Ordner ($desktop_dir): vermutlich Raspberry Pi OS Lite, Symbol uebersprungen (erzwingen: --desktop-icon)"; return
  fi
  sudo -u "$SERVICE_USER" mkdir -p "$desktop_dir" "$USER_HOME/.local/share/applications"
  for target in "$desktop_dir/pyMobaLedLib.desktop" "$USER_HOME/.local/share/applications/pyMobaLedLib.desktop"; do
    sed "s|__APPDIR__|$APPDIR|g" "$APPDIR/pi/mobaledlib.desktop.in" > "$target"
    chown "$SERVICE_USER": "$target"
    chmod 755 "$target"
    sudo -u "$SERVICE_USER" gio set "$target" metadata::trusted true >/dev/null 2>&1 || true
  done
  echo "Symbol angelegt: $desktop_dir/pyMobaLedLib.desktop (und im Startmenue unter Entwicklung/Elektronik)"
}
create_desktop_icon

echo; echo "== 7/8  ARDUINO IDE"
install_arduino_ide() {
  local arch variant url tmp
  if [ -x /opt/arduino-1.8.19/arduino ]; then echo "Schon vorhanden: /opt/arduino-1.8.19/arduino"; return; fi
  case "$(uname -m)" in
    aarch64|arm64) variant=linuxaarch64 ;;
    armv7l|armv6l) variant=linuxarm ;;
    x86_64)        variant=linux64 ;;
    *) echo "Unbekannte Architektur $(uname -m): bitte die IDE von Hand installieren (Anleitung, Kapitel 2.2)"; return ;;
  esac
  url="https://downloads.arduino.cc/arduino-1.8.19-$variant.tar.xz"
  tmp="$(mktemp -d)"
  echo "Lade $url (etwa 150 MB) ..."
  if curl -fL --retry 3 -o "$tmp/ide.tar.xz" "$url" && tar -xf "$tmp/ide.tar.xz" -C /opt; then
    chown -R root:root /opt/arduino-1.8.19
    echo "Installiert: /opt/arduino-1.8.19/arduino"
    # als Dienstbenutzer testen: als root wuerde die IDE ihre Ordner (.arduino15) mit falschem Besitzer anlegen
    sudo -u "$SERVICE_USER" env HOME="$USER_HOME" timeout 90 xvfb-run -a /opt/arduino-1.8.19/arduino --version 2>&1 | head -2 || true
  else
    echo "Download oder Auspacken fehlgeschlagen: die IDE bitte von Hand installieren (Anleitung, Kapitel 2.2)"
  fi
  rm -rf "$tmp"
}
if [ "$WITH_IDE" = "1" ]; then
  install_arduino_ide
elif ls /opt/arduino*/arduino >/dev/null 2>&1; then
  echo "Gefunden: $(ls /opt/arduino*/arduino | head -1)"
else
  echo "Keine ARDUINO IDE gefunden. Installieren mit:  sudo bash install_pi.sh --with-arduino-ide   (oder von Hand, Anleitung, Kapitel 2.2)"
fi

if [ "$WITH_LIBS" = "1" ]; then
  echo; echo "Bibliothek MobaLedLib und Abhaengigkeiten installieren (als Benutzer $SERVICE_USER, dauert einige Minuten) ..."
  sudo -u "$SERVICE_USER" env HOME="$USER_HOME" bash "$APPDIR/pi/install_arduino_libs.sh" || \
    echo "Die Installation der Bibliotheken meldet Probleme (siehe oben). Nachholen:  bash $APPDIR/pi/install_arduino_libs.sh"
else
  echo "Die ARDUINO-Bibliothek MobaLedLib fehlt evtl. noch:  bash $APPDIR/pi/install_arduino_libs.sh   (ohne sudo; --pico und --esp32 fuer die Boards)"
fi

echo; echo "== 8/8  Dienst mobaledlib-web"
sed -e "s|__USER__|$SERVICE_USER|g" -e "s|__APPDIR__|$APPDIR|g" "$APPDIR/pi/mobaledlib-web.service" \
    > /etc/systemd/system/mobaledlib-web.service
if ! sudo -u "$SERVICE_USER" test -w "$APPDIR"; then
  echo "ACHTUNG: $APPDIR ist fuer $SERVICE_USER nicht beschreibbar (Konfiguration, Protokoll und Zwischenspeicher liegen dort)."
  echo "         Abhilfe:  sudo chown -R $SERVICE_USER: $APPDIR"
fi
# Ordner der ARDUINO IDE gehoeren dem Dienstbenutzer (falls frueher ein Aufruf als root sie angelegt hat)
for d in "$USER_HOME/.arduino15" "$USER_HOME/Arduino"; do
  if [ -d "$d" ]; then chown -R "$SERVICE_USER": "$d" 2>/dev/null || true; fi
done
systemctl daemon-reload
systemctl stop mobaledlib-web 2>/dev/null || true            # damit der Test den Port nicht stoert

if [ "$RUN_CHECK" = "1" ]; then
  echo; echo "Test der Installation (dauert etwas) ..."
  (cd "$APPDIR" && sudo -u "$SERVICE_USER" env MLL_HEADLESS=1 MLL_TK_ROOT=0 "$APPDIR/venv/bin/python" "$APPDIR/pi_check.py") || \
    echo "Der Test meldet Probleme (siehe oben). Der Dienst wird trotzdem eingerichtet."
fi

systemctl enable mobaledlib-web
systemctl restart mobaledlib-web

IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
echo
echo "Fertig. Der Dienst startet beim Hochfahren automatisch (die Oberflaeche ist nach 20 bis 60 Sekunden da)."
echo "  Desktop:      Symbol \"pyMobaLedLib\" doppelklicken (startet bei Bedarf den Dienst und oeffnet das Fenster)"
echo "  Status:       systemctl status mobaledlib-web"
echo "  Protokoll:    journalctl -u mobaledlib-web -f"
if [ "$LOCAL_ONLY" = "1" ]; then
  echo "  Oberflaeche:  http://localhost:$PORT   (nur auf diesem Pi)"
else
  echo "  Oberflaeche:  http://${IP:-<IP-des-Pi>}:$PORT      Benutzer: mobaledlib   (auf dem Pi selbst ohne Passwort)"
  echo "  oder mit dem Namen:  http://$(hostname).local:$PORT     (Windows 10/11, macOS, iPhone, Linux mit avahi)"
  echo "  Passwort:     ${PASSWORD_INFO:-wie bisher (steht in $ENVFILE, oder im Programm geaendert: Programm Einstellungen - Zugriff ueber das Netz)}"
fi
echo "Hinweis: Damit die Gruppe dialout im Terminal wirkt, einmal ab- und wieder anmelden (der Dienst hat sie schon)."
