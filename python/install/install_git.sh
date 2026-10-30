#!/usr/bin/env bash
# Datei-Version: 1.00 (2026-10-30) - install_git.sh (gilt fuer webMobaLedLib 2.54)
# Linux: installiert den Git-Client (git). PlatformIO braucht ihn fuer das Board Raspberry Pi Pico: die Plattform (platform-raspberrypi) wird aus GitHub
# geklont. Ohne git meldet PlatformIO: "UserSideException: Please install Git client from https://git-scm.com/downloads".
# Aufruf (einmalig):   sudo bash install/install_git.sh
# Das Programm ruft das Skript auch selbst auf (Optionen, Entwicklungsumgebung, "Git installieren"); dann fragt pkexec nach dem Passwort.
# Erkannt werden apt (Debian, Ubuntu, Linux Mint, Raspberry Pi OS), dnf (Fedora), pacman (Arch, Manjaro) und zypper (openSUSE).
# Zum Pruefen ohne Administratorrechte und ohne etwas zu installieren: MLL_GIT_DRYRUN=1 bash install/install_git.sh  (zeigt nur die Befehle)
set -e
if [ -z "${MLL_GIT_DRYRUN:-}" ] && command -v git >/dev/null 2>&1; then
  echo "git ist schon installiert: $(git --version)"
  exit 0
fi
if [ -z "${MLL_GIT_DRYRUN:-}" ] && [ "$(id -u)" != "0" ]; then
  echo "Bitte mit Administratorrechten ausfuehren:  sudo bash $0"
  exit 1
fi
run() { if [ -n "${MLL_GIT_DRYRUN:-}" ]; then echo "WUERDE AUSFUEHREN: $*"; else "$@"; fi; }
if command -v apt-get >/dev/null 2>&1; then          # Debian, Ubuntu, Linux Mint, Raspberry Pi OS
  export DEBIAN_FRONTEND=noninteractive
  run apt-get update
  run apt-get install -y git
elif command -v dnf >/dev/null 2>&1; then            # Fedora
  run dnf install -y git
elif command -v pacman >/dev/null 2>&1; then         # Arch, Manjaro
  run pacman -S --needed --noconfirm git
elif command -v zypper >/dev/null 2>&1; then         # openSUSE
  run zypper install -y git
else
  echo "Die Paketverwaltung wurde nicht erkannt. Bitte git selbst installieren: https://git-scm.com/downloads"
  exit 2
fi
if [ -z "${MLL_GIT_DRYRUN:-}" ]; then
  if command -v git >/dev/null 2>&1; then
    echo "git ist installiert: $(git --version)"
  else
    echo "git wurde nicht gefunden, die Installation ist fehlgeschlagen."
    exit 3
  fi
fi
