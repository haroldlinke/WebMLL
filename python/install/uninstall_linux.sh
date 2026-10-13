#!/usr/bin/env bash
# Datei-Version: 1.00 (2026-10-12) - uninstall_linux.sh
# Entfernt Starter und Symbole des Linux-Desktops. Mit --purge wird auch die Python-Umgebung venv_web geloescht.
# Projektordner, ARDUINO IDE und Bibliotheken bleiben erhalten.
cd "$(dirname "$0")/.." || exit 1
APPDIR="$(pwd)"
rm -f "${XDG_DATA_HOME:-$HOME/.local/share}/applications/pyMobaLedLib.desktop"
DESK="$(xdg-user-dir DESKTOP 2>/dev/null || true)"; [ -z "$DESK" ] || [ "$DESK" = "$HOME" ] && DESK="$HOME/Desktop"
rm -f "$DESK/pyMobaLedLib.desktop"
if [ "${1:-}" = "--purge" ]; then rm -rf "$APPDIR/venv_web"; echo "Python-Umgebung venv_web geloescht."; fi
echo "Starter und Symbole entfernt."
