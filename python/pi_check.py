# Datei-Version: 1.05 (2026-11-08) - pi_check.py
# ----------------------------------------------------------------------------------------------
# Name:           pi_check.py
# Path:           pi_check.py
# Version:        1.05
# Last Update:    2026-11-08
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.05  2026-11-08  PlatformIO ist der Standard: Der Test meldet bei PlatformIO die Entwicklungsumgebung (OK oder Hinweis, wenn es fehlt) und nicht mehr 'ARDUINO IDE nicht gefunden'; die Einstellungsdatei der IDE ist dann nicht noetig (fruehere Versionen ohne Eintrag)
# ----------------------------------------------------------------------------------------------
"""Prueft die Installation der Web-Oberflaeche (Raspberry Pi, aber auch jeder andere Rechner).

Aufruf im Projektordner (neben webmobaledlib.py):
    MLL_HEADLESS=1 MLL_TK_ROOT=0 venv/bin/python pi_check.py

Es wird nichts veraendert. Das Programm meldet fuer jeden Punkt OK, HINWEIS oder FEHLT und startet am Ende die
Excel-Schicht ohne Tk, laedt alle Blaetter und prueft den Pfad der ARDUINO IDE.
"""
from __future__ import annotations

import importlib
import os
import platform
import shutil
import sys
import traceback

os.environ.setdefault("MLL_HEADLESS", "1")
os.environ["MLL_TK_ROOT"] = "0"                       # kein Tk: wie als Dienst ohne Bildschirm
here = os.path.dirname(os.path.abspath(__file__))
if here not in sys.path:
    sys.path.insert(0, here)

problems = []


def report(status: str, text: str):
    print(f"  [{status:7s}] {text}")
    if status == "FEHLT":
        problems.append(text)


def report_development_environment(report_func, startcmd: str, pio_mode: bool, pio_path: str) -> None:  # v1.05
    """Entwicklungsumgebung: PlatformIO (Standard seit 2.92) oder ARDUINO IDE. Mit PlatformIO wird die ARDUINO IDE nicht gebraucht, dann keine Meldung dazu."""  # v1.05
    if pio_mode:  # v1.05
        if pio_path:  # v1.05
            report_func("OK", "PlatformIO ist die Entwicklungsumgebung: " + pio_path)  # v1.05
        else:  # v1.05
            report_func("HINWEIS", "PlatformIO ist als Entwicklungsumgebung eingestellt, wurde aber nicht gefunden. Installieren (ohne sudo): bash install/install_platformio.sh")  # v1.05
        return  # v1.05
    if startcmd and os.path.isfile(startcmd):  # v1.05
        report_func("OK", f"ARDUINO IDE gefunden: {startcmd}")  # v1.05
    else:  # v1.05
        report_func("HINWEIS", "ARDUINO IDE nicht gefunden (Pfad: " + (startcmd or "leer") + "). Die IDE 1.8.19 nach ~/arduino-1.8.19 legen, oder in "  # v1.05
                    "'ARDUINO Einstellungen' die Schaltflaeche 'IDE suchen' benutzen bzw. den Pfad der Startdatei 'arduino' eintragen "  # v1.05
                    "(oder die Umgebungsvariable MLL_ARDUINO_EXE setzen). Siehe Anleitung, Abschnitt 2.2." + ("  Oder PlatformIO benutzen (Standard): bash install/install_platformio.sh" if not pio_path else ""))  # v1.05


print(f"Projektordner: {here}")
import userdata                                        # noqa: E402
print(f"Datenordner:    {userdata.data_dir()}   (Konfiguration, Sicherungen, Protokolle, Passwort: ausserhalb des Projektordners)")
print(f"System:        {platform.platform()}  /  Python {platform.python_version()}")

print("\nPython und Pakete")
if sys.version_info < (3, 10):
    report("FEHLT", f"Python {platform.python_version()} ist zu alt (ab 3.10 noetig)")
else:
    report("OK", f"Python {platform.python_version()}")
for module, pip_name, needed in (("nicegui", "nicegui", True), ("serial", "pyserial", True), ("openpyxl", "openpyxl", True),
                                 ("PIL", "Pillow", False)):
    try:
        importlib.import_module(module)
        report("OK", f"{pip_name}")
    except ImportError:
        report("FEHLT" if needed else "HINWEIS", f"{pip_name} nicht installiert:  venv/bin/pip install {pip_name}")

print("\nSystem")
if platform.system() == "Linux":
    xvfb = shutil.which("xvfb-run")
    report("OK" if xvfb else "HINWEIS",
           "xvfb-run vorhanden (virtuelles Display fuer die ARDUINO IDE)" if xvfb else
           "xvfb-run fehlt (sudo apt install xvfb): die ARDUINO IDE 1.8 laeuft ohne Display evtl. nicht")
    try:
        import grp
        groups = {grp.getgrgid(g).gr_name for g in os.getgroups()}
        in_group = "dialout" in groups
        report("OK" if in_group else "HINWEIS",
               "Benutzer ist in der Gruppe dialout" if in_group else
               "Benutzer ist nicht in der Gruppe dialout (der Dienst bekommt sie ueber systemd, fuer diesen Test egal)")
    except Exception:                                  # noqa: BLE001
        pass
try:
    import serial.tools.list_ports as lp
    ports = [f"{p.device} ({p.description})" for p in lp.comports()]
    report("OK" if ports else "HINWEIS", "Serielle Anschluesse: " + (", ".join(ports) if ports else "keine gefunden (Arduino/Pico angeschlossen?)"))
except Exception as ex:                                # noqa: BLE001
    report("HINWEIS", f"Serielle Anschluesse nicht pruefbar: {ex}")

print("\nProgramm (Excel-Schicht ohne Tk, laedt alle Blaetter - das dauert einige Sekunden)")
if problems:
    print("  uebersprungen: erst die oben gemeldeten fehlenden Pakete installieren")
    print(f"\n{len(problems)} Problem(e) gefunden. Bitte die Zeilen mit FEHLT beheben und den Test wiederholen.")
    sys.exit(1)
try:
    import webmobaledlib                                # richtet auch den Ersatz fuer tkinter ein
    import tkinter
    report("OK" if getattr(tkinter, "__file__", "") == "<no_tk>" else "HINWEIS",
           "tkinter-Ersatz (no_tk) aktiv" if getattr(tkinter, "__file__", "") == "<no_tk>" else
           "echtes tkinter geladen (MLL_TK_ROOT=0 wirkt nicht?)")
    webmobaledlib.start_backend()
    ctrl = webmobaledlib.ctrl
    wb = webmobaledlib.page.workbook
    names = [ws.Name for ws in wb.sheets]
    report("OK", f"{len(names)} Blaetter geladen: {', '.join(names[:6])} ...")
    try:  # v1.05: PlatformIO (Standard) oder ARDUINO IDE
        import proggen.M08_ARDUINO as M08  # v1.05
        import proggen.M28_Diverse as M28  # v1.05
        pio_mode = bool(M28.Is_PlatformIO())  # v1.05
        pio_path = str(M08.Find_PIO() or "")  # v1.05
    except Exception:                                  # noqa: BLE001  # v1.05
        pio_mode, pio_path = False, ""  # v1.05
    prefs = os.path.expanduser("~/.arduino15/preferences.txt")
    if pio_mode:  # v1.05: die Einstellungsdatei der ARDUINO IDE ist mit PlatformIO nicht noetig
        pass  # v1.05
    else:  # v1.05
        report("OK" if os.path.isfile(prefs) else "HINWEIS",
               f"Einstellungsdatei der ARDUINO IDE vorhanden: {prefs}" if os.path.isfile(prefs) else
               f"{prefs} fehlt (das Programm legt sie beim Start an; sonst: bash pi/install_arduino_libs.sh)")
    startcmd = "" if pio_mode else str(ctrl.getConfigData("startcmd_filename") or "")  # v1.05: mit PlatformIO nicht nach der IDE suchen (das Suchen schreibt sonst eine Warnung ins Protokoll)
    report_development_environment(report, startcmd, pio_mode, pio_path)  # v1.05
except Exception:                                      # noqa: BLE001
    report("FEHLT", "Programm konnte nicht gestartet werden:")
    traceback.print_exc()

print()
if problems:
    print(f"{len(problems)} Problem(e) gefunden. Bitte die Zeilen mit FEHLT beheben und den Test wiederholen.")
    sys.exit(1)
print("Keine Fehler gefunden.")
