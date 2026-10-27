#!/usr/bin/env bash
# Datei-Version: 1.00 (2026-10-27) - install_pico_udev.sh (gilt fuer webMobaLedLib 2.21)
# Linux: gibt dem angemeldeten Benutzer Zugriff auf den Raspberry Pi Pico (RP2040, RP2350) im BOOTSEL-Modus und als serielle Schnittstelle.
# Ohne diese Regel meldet PlatformIO beim Hochladen: "picotool was unable to connect. Maybe try 'sudo' or check your permissions."
# Aufruf (einmalig):   sudo bash install/install_pico_udev.sh [Benutzername]
# Das Programm ruft das Skript auch selbst auf (Optionen, Entwicklungsumgebung, "USB-Zugriff fuer den Pico einrichten"); dann fragt pkexec nach dem Passwort.
# Zum Pruefen ohne Administratorrechte: MLL_UDEV_DIR=/Pfad/zu/einem/Ordner bash install/install_pico_udev.sh  (schreibt nur die Regel, aendert keine Gruppen, laedt udev nicht neu)
set -e
TEST_DIR="${MLL_UDEV_DIR:-}"
RULE_DIR="${TEST_DIR:-/etc/udev/rules.d}"
RULE="$RULE_DIR/99-mobaledlib-pico.rules"

if [ -z "$TEST_DIR" ] && [ "$(id -u)" != "0" ]; then
  echo "Bitte mit Administratorrechten ausfuehren:  sudo bash $0"
  exit 1
fi

# Benutzer, der den Pico benutzen soll: Parameter, sonst der Benutzer, der sudo oder pkexec aufgerufen hat
TARGET="${1:-${SUDO_USER:-}}"
if [ -z "$TARGET" ] && [ -n "${PKEXEC_UID:-}" ]; then
  TARGET="$(getent passwd "$PKEXEC_UID" | cut -d: -f1)"
fi

mkdir -p "$RULE_DIR"
cat > "$RULE" << 'RULES'
# webMobaLedLib: Zugriff auf den Raspberry Pi Pico (RP2040, RP2350) fuer den angemeldeten Benutzer
# BOOTSEL-Modus (picotool, PlatformIO) und serielle Schnittstelle (ttyACM)
SUBSYSTEM=="usb", ATTRS{idVendor}=="2e8a", MODE="0660", TAG+="uaccess", GROUP="plugdev"
KERNEL=="ttyACM[0-9]*", SUBSYSTEM=="tty", ATTRS{idVendor}=="2e8a", MODE="0660", TAG+="uaccess", GROUP="dialout"
RULES
chmod 644 "$RULE"
echo "Regel geschrieben: $RULE"

if [ -z "$TEST_DIR" ]; then
  if [ -n "$TARGET" ] && id "$TARGET" > /dev/null 2>&1; then
    getent group plugdev > /dev/null || groupadd plugdev
    usermod -a -G plugdev,dialout "$TARGET"
    echo "Benutzer $TARGET ist jetzt in den Gruppen plugdev und dialout (gilt nach dem naechsten An- und Abmelden)."
  fi
  udevadm control --reload-rules
  udevadm trigger
  echo "Fertig. Bitte den Pico neu anstecken (BOOTSEL-Taste gedrueckt halten) und das Hochladen wiederholen."
fi
