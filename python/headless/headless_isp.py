# Datei-Version: 1.00 (2026-11-03) - headless_isp.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_isp.py
# Path:           headless/headless_isp.py
# Version:        1.00
# Last Update:    2026-11-03
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-03  Neu: schneller Bootloader mit PlatformIO: avrdude von PlatformIO finden, Signatur des Mikrocontrollers lesen, Bootloader-Datei waehlen, die beiden avrdude-Befehle bauen
# ----------------------------------------------------------------------------------------------
"""Schneller Bootloader (Optiboot Version 108.1) mit PlatformIO auf den linken Arduino schreiben.

Der rechte Arduino bekommt das Programm ArduinoISP (fertig uebersetzt: 03.ArduinoISP.hex, Ordner libraries/MobaLedLib/firmware) und programmiert damit ueber die Jumper den linken
Arduino (stk500v1, 19200 Baud). Das Excel-Programm benutzt dafuer eine Stapeldatei mit dem avrdude der ARDUINO IDE; hier wird das avrdude von PlatformIO benutzt (Paket
tool-avrdude, kommt mit der Plattform atmelavr). Die Befehle sind dieselben wie in der Stapeldatei:

1. Signatur lesen:   avrdude -C<conf> -patmega328p -F -cstk500v1 -P<Anschluss> -b19200 -Usignature:r:<Datei>:h
2. Bootloader:       avrdude -C<conf> -v -p<cpu> -cstk500v1 -P<Anschluss> -b19200 -Uflash:w:<Bootloader>:i -Ulock:w:0x0F:m -Uhfuse:w:0xDE:m

Alle Funktionen nehmen ihre Umgebung als Parameter und sind ohne PlatformIO pruefbar.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

ISP_INO = "03.ArduinoISP.ino"                     # Name der Quelle; die fertige Datei heisst 03.ArduinoISP.hex
BAUD = 19200
BOOT_328 = "optiboot_atmega328_Ver108.1.hex"      # auch fuer den ATmega328PB, wenn er als 328P beschrieben wird (Signatur aendern)
BOOT_328PB = "optiboot_atmega328pb_16mhz.hex"
SIGNATURES = {(0x1E, 0x95, 0x0F): "atmega328p", (0x1E, 0x95, 0x16): "atmega328pb"}
LOCK = "0x0F"
HFUSE = "0xDE"


def parse_signature(text):
    """Die Signaturdatei von avrdude (-Usignature:r:...:h) lesen: '0x1e,0x95,0x0f' (auch '0x1e,0x95,0xf', mit Leerraum, Grossbuchstaben). Rueckgabe (a, b, c) oder None."""
    parts = [p.strip() for p in str(text or "").replace("\r", "").split("\n")[0].split(",")]
    try:
        values = tuple(int(p, 16) for p in parts)
    except ValueError:
        return None
    return values if len(values) == 3 and all(0 <= v <= 255 for v in values) else None


def signature_cpu(text):
    """(cpu, problem) zur Signatur: cpu 'atmega328p' oder 'atmega328pb'; problem '' | 'unreadable' (nichts gelesen, 0x0,0x0,0x0 oder kein Anschluss) | 'unsupported' (anderer Chip)"""
    sig = parse_signature(text)
    if sig is None or sig == (0, 0, 0):
        return "", "unreadable"
    cpu = SIGNATURES.get(sig)
    return (cpu, "") if cpu else ("", "unsupported")


def signature_text(text) -> str:
    """Die Signatur lesbar (0x1e,0x95,0x16) fuer Meldungen; die Rohzeile, wenn sie nicht zu lesen ist"""
    sig = parse_signature(text)
    return ",".join("0x%02x" % v for v in sig) if sig else str(text or "").strip()


def bootloader_name(cpu, flash_as_328p=True) -> str:
    """Name der Bootloader-Datei: der ATmega328P bekommt immer die Datei fuer den 328; der ATmega328PB bekommt sie, wenn er als 328P beschrieben werden soll
    (Signatur aendern, die Vorgabe des Excel-Programms), sonst die Datei fuer den 328PB"""
    if cpu == "atmega328pb" and not flash_as_328p:
        return BOOT_328PB
    return BOOT_328


def find_avrdude(core=None, windows=None, isfile=None, listdir=None):
    """avrdude von PlatformIO: (Programm, avrdude.conf) im Paket tool-avrdude des Kernordners von PlatformIO (PLATFORMIO_CORE_DIR oder ~/.platformio); ('', '') wenn es noch nicht da ist
    (es kommt mit der Plattform atmelavr beim ersten Hochladen oder Uebersetzen fuer einen Nano)"""
    isfile = isfile or os.path.isfile
    listdir = listdir or os.listdir
    windows = (os.name == "nt") if windows is None else windows
    if core is None:
        import headless.headless_pio_cache as HC
        core = HC.core_dir()
    packages = os.path.join(core, "packages")
    try:
        names = sorted(n for n in listdir(packages) if n.lower().startswith("tool-avrdude"))
    except OSError:
        return "", ""
    names.sort(key=lambda n: (n.lower() != "tool-avrdude", n))                      # der Ordner ohne Versionsangabe zuerst
    exe_name = "avrdude.exe" if windows else "avrdude"
    for name in names:
        folder = os.path.join(packages, name)
        exe = os.path.join(folder, exe_name)
        if not isfile(exe) and not windows:
            exe = os.path.join(folder, "bin", exe_name)
        for conf in (os.path.join(folder, "avrdude.conf"), os.path.join(folder, "etc", "avrdude.conf")):
            if isfile(exe) and isfile(conf):
                return exe, conf
    return "", ""


def read_signature_cmd(exe, conf, port, sigfile) -> str:
    """Befehl 1: die Signatur des linken Arduino lesen (stk500v1 ueber den ArduinoISP des rechten Arduino; -F: auch bei unbekannter Signatur)"""
    return '"%s" "-C%s" -patmega328p -F -cstk500v1 -P%s -b%d "-Usignature:r:%s:h"' % (exe, conf, port, BAUD, sigfile)


def write_cmd(exe, conf, cpu, port, bootfile) -> str:
    """Befehl 2: Bootloader schreiben, Lock-Bits 0x0F und High-Fuse 0xDE (512 Byte fuer den Bootloader reserviert)"""
    return '"%s" "-C%s" -v -p%s -cstk500v1 -P%s -b%d "-Uflash:w:%s:i" -Ulock:w:%s:m -Uhfuse:w:%s:m' % (exe, conf, cpu, port, BAUD, bootfile, LOCK, HFUSE)


def bootloader_dirs(src_dir_in_lib) -> list:
    """Ordner mit den Bootloader-Dateien: <Sketchbook>/libraries/MobaLedLib/extras/ArduinoISP (Get_SrcDirInLib + 'ArduinoISP')"""
    base = str(src_dir_in_lib or "").rstrip("/\\")
    return [os.path.join(base, "ArduinoISP")] if base else []


def find_bootloader(name, dirs) -> str:
    """Voller Pfad der Bootloader-Datei im ersten Ordner, der sie hat (Gross-/Kleinschreibung egal); '' wenn keine da ist"""
    import headless.headless_hex_upload as HX
    for folder in dirs or []:
        real = folder
        if not os.path.isdir(real):
            parent, last = os.path.split(str(folder).rstrip("/\\"))
            real = HX._ci_child(parent or ".", last)
        if not real or not os.path.isdir(real):
            continue
        path = HX._ci_child(real, name)
        if path and os.path.isfile(path):
            return path
    return ""


def read_text(path) -> str:
    """Inhalt einer kleinen Textdatei (die Signaturdatei von avrdude); '' wenn es sie nicht gibt"""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""
