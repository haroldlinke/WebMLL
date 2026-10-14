#!/usr/bin/env bash
# Datei-Version: 1.00 (2026-10-12) - uninstall_pi.sh
# Entfernt Dienst, Einstellungen, sudo-Regel und Desktop-Symbol. Projektordner, venv und ARDUINO IDE bleiben erhalten.
set -euo pipefail
if [ "$(id -u)" -ne 0 ]; then exec sudo -E bash "$0" "$@"; fi
SERVICE_USER="${SUDO_USER:-}"
USER_HOME="$(getent passwd "${SERVICE_USER:-root}" | cut -d: -f6)"
systemctl disable --now mobaledlib-web 2>/dev/null || true
rm -f /etc/systemd/system/mobaledlib-web.service /etc/mobaledlib-web.env /etc/sudoers.d/mobaledlib-web
systemctl daemon-reload
rm -f "$USER_HOME/.local/share/applications/pyMobaLedLib.desktop"
for d in "$USER_HOME/Desktop" "$(sudo -u "$SERVICE_USER" env HOME="$USER_HOME" xdg-user-dir DESKTOP 2>/dev/null || true)"; do
  [ -n "$d" ] && rm -f "$d/pyMobaLedLib.desktop"
done
echo "Entfernt. Der Projektordner, die Python-Umgebung (venv) und die ARDUINO IDE (/opt/arduino-1.8.19) wurden nicht geloescht."
