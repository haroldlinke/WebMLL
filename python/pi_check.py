# Datei-Version: 1.03 (2026-10-14) - pi_check.py
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
    prefs = os.path.expanduser("~/.arduino15/preferences.txt")
    report("OK" if os.path.isfile(prefs) else "HINWEIS",
           f"Einstellungsdatei der ARDUINO IDE vorhanden: {prefs}" if os.path.isfile(prefs) else
           f"{prefs} fehlt (das Programm legt sie beim Start an; sonst: bash pi/install_arduino_libs.sh)")
    startcmd = str(ctrl.getConfigData("startcmd_filename") or "")
    if os.path.isfile(startcmd):
        report("OK", f"ARDUINO IDE gefunden: {startcmd}")
    else:
        report("HINWEIS", "Pfad der ARDUINO IDE nicht gesetzt oder falsch (" + (startcmd or "leer") + "). Unter Linux muss er in "
                          "'ARDUINO Einstellungen' eingetragen werden (Startdatei 'arduino' der IDE 1.8.19).")
except Exception:                                      # noqa: BLE001
    report("FEHLT", "Programm konnte nicht gestartet werden:")
    traceback.print_exc()

print()
if problems:
    print(f"{len(problems)} Problem(e) gefunden. Bitte die Zeilen mit FEHLT beheben und den Test wiederholen.")
    sys.exit(1)
print("Keine Fehler gefunden.")
