#!/usr/bin/env bash
# Datei-Version: 1.02 (2026-10-15) - uninstall_linux.sh
# Entfernt Starter und Symbole des Linux-Desktops. Mit --purge wird auch die Python-Umgebung venv_web geloescht.
# Projektordner, ARDUINO IDE und Bibliotheken bleiben erhalten.
cd "$(dirname "$0")/.." || exit 1
APPDIR="$(pwd)"
rm -f "${XDG_DATA_HOME:-$HOME/.local/share}/applications/webMobaLedLib.desktop" "${XDG_DATA_HOME:-$HOME/.local/share}/applications/pyMobaLedLib.desktop"
DESK="$(xdg-user-dir DESKTOP 2>/dev/null || true)"; [ -z "$DESK" ] || [ "$DESK" = "$HOME" ] && DESK="$HOME/Desktop"
rm -f "$DESK/webMobaLedLib.desktop" "$DESK/pyMobaLedLib.desktop"
DATADIR="$("$APPDIR/venv_web/bin/python" "$APPDIR/userdata.py" 2>/dev/null || true)"
if [ "${1:-}" = "--purge" ]; then rm -rf "$APPDIR/venv_web"; echo "Python-Umgebung venv_web geloescht."; fi
echo "Starter und Symbole entfernt."
[ -n "$DATADIR" ] && echo "Deine Daten (Konfiguration, Sicherungen, Protokolle) bleiben erhalten: $DATADIR"
