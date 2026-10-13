#!/bin/bash
# Datei-Version: 1.03 (2026-10-13) - install_mac.command
# Installiert die Web-Oberflaeche von pyMobaLedLib unter macOS: Python-Umgebung, Pakete, Programmsymbol und ein Programm
# "pyMobaLedLib" auf dem Schreibtisch (Doppelklick startet die Oberflaeche und oeffnet den Browser).
#
# Aufruf: im Finder doppelklicken, oder im Terminal:   bash install_mac.command [--nocheck] [--with-arduino-libs]
#   --with-arduino-ide    ARDUINO IDE 1.8.19 von arduino.cc laden und in Programme kopieren (die IDE 2.x wird NICHT unterstuetzt), dazu --with-arduino-libs
#   --with-arduino-libs   Bibliothek MobaLedLib (und FastLED in der geforderten Version) mit der ARDUINO IDE installieren
#   --nocheck             ohne den Test der Installation am Ende
# (Ist die Datei nicht ausfuehrbar:  chmod +x install_mac.command)
set -u
cd "$(dirname "$0")" || exit 1
HERE="$(pwd)"
APPDIR="$(cd .. && pwd)"
VENV="$APPDIR/venv_web"
APP="${MLL_APP_DIR:-$HOME/Desktop}/pyMobaLedLib.app"
CHECK=1
WITH_LIBS=0
WITH_IDE=0
IDE_URL="${MLL_IDE_URL:-https://downloads.arduino.cc/arduino-1.8.19-macosx.zip}"
FASTLED_VERSION="${MLL_FASTLED_VERSION:-3.9.12}"
for a in "$@"; do
  [ "$a" = "--nocheck" ] && CHECK=0
  [ "$a" = "--with-arduino-libs" ] && WITH_LIBS=1
  [ "$a" = "--with-arduino-ide" ] && { WITH_IDE=1; WITH_LIBS=1; }
done

echo
echo "============================================================"
echo " pyMobaLedLib - Installation der Web-Oberflaeche (macOS)"
echo "============================================================"
echo " Projektordner: $APPDIR"
echo

if [ "$(uname)" != "Darwin" ] && [ "${MLL_FORCE:-0}" != "1" ]; then
  echo "Dieses Skript ist fuer macOS. Unter Linux/Raspberry Pi: pi/install_pi.sh"; exit 1
fi
if [ ! -f "$APPDIR/headless_web.py" ]; then
  echo "FEHLER: headless_web.py nicht gefunden in $APPDIR"
  echo "Der Ordner install muss im Projektordner neben headless_web.py liegen."; exit 1
fi
fail() { echo; echo "Die Installation wurde nicht abgeschlossen."; read -r -p "Zum Beenden Enter druecken ..." _; exit 1; }

# --- 1. Python 3.10 oder neuer suchen
find_python() {
  local c
  for c in python3.13 python3.12 python3.11 python3.10 /opt/homebrew/bin/python3.13 /opt/homebrew/bin/python3.12 \
           /usr/local/bin/python3.13 /usr/local/bin/python3.12 /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 python3; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
      command -v "$c"; return 0
    fi
  done
  return 1
}
PY="$(find_python || true)"
if [ -z "$PY" ]; then
  echo "Python 3.10 oder neuer wurde nicht gefunden (das mit macOS gelieferte Python ist zu alt)."
  BREW="$(command -v brew || ls /opt/homebrew/bin/brew /usr/local/bin/brew 2>/dev/null | head -1 || true)"
  if [ -n "$BREW" ]; then
    read -r -p "Python 3.12 jetzt mit Homebrew installieren? [j/N] " ans
    if [ "$ans" = "j" ] || [ "$ans" = "J" ]; then
      "$BREW" install python@3.12 || fail
      PY="$(find_python || true)"
    fi
  fi
fi
if [ -z "$PY" ]; then
  echo "Bitte Python 3.12 installieren: https://www.python.org/downloads/macos/  (oder: brew install python@3.12)"
  echo "und dieses Skript danach noch einmal starten."
  fail
fi
echo "Gefunden: $PY ($("$PY" --version 2>&1))"
echo

# --- 2. Python-Umgebung und Pakete
echo "[1/4] Python-Umgebung anlegen: $VENV"
if [ ! -x "$VENV/bin/python" ]; then
  "$PY" -m venv "$VENV" || fail
fi
echo "[2/4] Pakete installieren (das dauert einige Minuten) ..."
if [ "${MLL_SKIP_PIP:-0}" != "1" ]; then
  "$VENV/bin/python" -m pip install --upgrade pip || fail
  "$VENV/bin/python" -m pip install -r "$HERE/requirements-web.txt" || fail
fi

# --- 3. Programmsymbol
echo "[3/4] Programmsymbol erzeugen"
"$VENV/bin/python" "$HERE/make_icons.py" "$HERE" || echo "Symbol nicht erzeugt (das Programm funktioniert trotzdem)."

# --- 4. Programm auf dem Schreibtisch: pyMobaLedLib.app (startet die Oberflaeche ohne Terminalfenster)
echo "[4/4] Programm anlegen: $APP"
rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources" || fail
cat > "$APP/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>pyMobaLedLib</string>
  <key>CFBundleDisplayName</key><string>pyMobaLedLib</string>
  <key>CFBundleIdentifier</key><string>de.mobaledlib.web</string>
  <key>CFBundleVersion</key><string>1.0</string>
  <key>CFBundleShortVersionString</key><string>1.0</string>
  <key>CFBundleExecutable</key><string>pyMobaLedLib</string>
  <key>CFBundleIconFile</key><string>mobaledlib</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>LSMinimumSystemVersion</key><string>10.13</string>
  <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
PLIST
{
  echo '#!/bin/bash'
  echo "APPDIR=\"$APPDIR\""
  echo 'cd "$APPDIR" || exit 1'
  echo 'export MLL_HEADLESS=1'
  echo 'exec "$APPDIR/venv_web/bin/python" "$APPDIR/headless_web.py" --open-if-running >> "$APPDIR/headless-console.log" 2>&1'
} > "$APP/Contents/MacOS/pyMobaLedLib"
chmod +x "$APP/Contents/MacOS/pyMobaLedLib"
[ -f "$HERE/mobaledlib.icns" ] && cp "$HERE/mobaledlib.icns" "$APP/Contents/Resources/mobaledlib.icns"
touch "$APP"

# --- ARDUINO IDE 1.8.19 (nur mit --with-arduino-ide)
find_ide() {
  local c
  for c in "${MLL_IDE_TARGET:-/Applications}/Arduino.app/Contents/MacOS/Arduino" /Applications/Arduino.app/Contents/MacOS/Arduino \
           "$HOME/Applications/Arduino.app/Contents/MacOS/Arduino"; do
    [ -x "$c" ] && { echo "$c"; return 0; }
  done
  return 1
}
if [ "$WITH_IDE" = "1" ]; then
  echo
  if find_ide >/dev/null; then
    echo "Die ARDUINO IDE ist schon installiert: $(find_ide)"
  else
    echo "ARDUINO IDE 1.8.19 herunterladen (etwa 200 MB) ..."
    TMPD="$(mktemp -d)"
    TARGET="${MLL_IDE_TARGET:-/Applications}"
    [ -w "$TARGET" ] || TARGET="$HOME/Applications"
    mkdir -p "$TARGET"
    if curl -fL --retry 3 -o "$TMPD/ide.zip" "$IDE_URL"; then
      mkdir -p "$TMPD/x"
      if command -v ditto >/dev/null 2>&1; then ditto -x -k "$TMPD/ide.zip" "$TMPD/x"; else unzip -q "$TMPD/ide.zip" -d "$TMPD/x"; fi
      if [ -d "$TMPD/x/Arduino.app" ]; then
        rm -rf "$TARGET/Arduino.app"
        mv "$TMPD/x/Arduino.app" "$TARGET/" && echo "ARDUINO IDE installiert: $TARGET/Arduino.app"
        echo "(Auf Macs mit Apple-Chip fragt macOS beim ersten Start nach Rosetta: bitte zustimmen.)"
      else
        echo "Im Download wurde Arduino.app nicht gefunden."
      fi
    else
      echo "Der Download der ARDUINO IDE ist fehlgeschlagen. Bitte von arduino.cc laden (Legacy IDE 1.8.x, macOS) und in Programme kopieren."
    fi
    rm -rf "$TMPD"
  fi
fi

# --- Bibliothek MobaLedLib (nur mit --with-arduino-libs): die IDE 1.8.19 muss in Programme liegen
if [ "$WITH_LIBS" = "1" ]; then
  IDE="$(find_ide || true)"
  echo
  if [ -z "$IDE" ]; then
    echo "Keine ARDUINO IDE gefunden. Mit  bash install_mac.command --with-arduino-ide  wird die IDE 1.8.19 geladen,"
    echo "oder sie von arduino.cc (Legacy IDE 1.8.x) in den Ordner Programme kopieren (die IDE 2.x geht nicht)."
  else
    echo "ARDUINO IDE gefunden: $IDE"
    # Einstellungsdatei der IDE vorbereiten und eine nicht installierte Board-Auswahl zuruecksetzen (sonst stuerzt die IDE ab)
    "$VENV/bin/python" -c "import sys; sys.path.insert(0, '$APPDIR'); import arduino_prefs as a; a.ensure_arduino_prefs(); a.sanitize_arduino_prefs()" || true
    echo "Bibliotheken installieren: FastLED $FASTLED_VERSION und danach MobaLedLib (dauert einige Minuten) ..."
    "$IDE" --install-library "FastLED:$FASTLED_VERSION" || echo "(FastLED: siehe Meldungen oben)"
    "$IDE" --install-library "MobaLedLib" || echo "(MobaLedLib: siehe Meldungen oben)"
  fi
fi

# --- Test der Installation
if [ "$CHECK" = "1" ]; then
  echo
  echo "Test der Installation (dauert etwa eine Minute) ..."
  MLL_TK_ROOT=0 MLL_HEADLESS=1 "$VENV/bin/python" "$APPDIR/pi_check.py" || echo "Der Test meldet Probleme, siehe die Meldungen oben."
fi

echo
echo "============================================================"
echo " Fertig. Starten: Programm \"pyMobaLedLib\" auf dem Schreibtisch doppelklicken"
echo " (beim ersten Mal ggf. Rechtsklick > Oeffnen)  oder  $HERE/start_mac.command"
echo
if find_ide >/dev/null; then
  echo " ARDUINO IDE gefunden: $(find_ide)"
else
  echo " Hinweis: Fuer das Kompilieren und Hochladen werden die ARDUINO IDE 1.8.19 (NICHT die IDE 2.x) und die Bibliothek"
  echo " MobaLedLib benoetigt. Mit  bash install_mac.command --with-arduino-ide  werden beide installiert"
  echo " (siehe ANLEITUNG_Installation, Kapitel 2.2 und 4)."
fi
echo "============================================================"
read -r -p "Zum Beenden Enter druecken ..." _
exit 0
