"""Rauchtest: Excel-Schicht ohne Tk starten.

Ablage: headless_sheet.py und XLA_Application_headless.py (statt XLA_Application.py)
in den Ordner ExcelAPI deines Projekts kopieren, headless_controller.py daneben oder
irgendwo im Pfad. Dann aus dem Projektordner starten:

    set MLL_HEADLESS=1          (Linux/Mac: export MLL_HEADLESS=1)
    python headless_smoke.py

Der Test legt eine Arbeitsmappe mit EINEM Blatt ohne Datei an. Danach liest/schreibt er
Zellen ueber Range/Cells. Fehlermeldungen (ImportError, AttributeError ...) zeigen, welche
Tk-Reste noch im Weg sind; bitte komplett an mich zurueckgeben.
"""
import logging
import os
import sys

os.environ.setdefault("MLL_HEADLESS", "1")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

from headless_controller import HeadlessController            # noqa: E402
from ExcelAPI import XLA_Application as X02                    # noqa: E402  (Datei = die Headless-Variante)

print("HEADLESS =", X02.HEADLESS)

ctrl = HeadlessController()
ctrl.on_status.append(lambda text, fg: print("STATUS:", text))

# Signatur wie im Hauptprogramm; bei Abweichung bitte die Zeile aus deinem Startcode uebernehmen
app = X02.CApplication(None, "MLL", os.getcwd(), ctrl)
ctrl.ExcelApplication = app

workbook_dict = {
    "Name": "SmokeTest",
    "Events": {},
    "SheetDict": {"DCC": {"Name": "DCC", "Fieldnames": "A;B;C", "SheetType": "Datasheet"}},
    "JumpTable": {},
}

wb = app.Workbooks.Open(ParentFrame=None, FileName="smoke.json", path=os.getcwd(), pyProgPath=os.getcwd(),
                        workbookName="SmokeTest", macro_caller=type("M", (), {})(), InitWorkBookFunction=None,
                        workbookdict=workbook_dict, start_sheet="DCC", controller=ctrl)
print("Workbook:", wb.Name, "| Blaetter:", [s.Name for s in wb.sheets])

ws = wb.sheets[0]
print("tksheet-Typ:", type(ws.tksheet).__name__)
ws.tksheet.set_sheet_data([["a", "b", "c"], ["1", "2", "3"]])
ws.update_table_properties()
print("Zellwert (2,2):", ws.Cells(2, 2).Value if hasattr(ws, "Cells") else "(kein ws.Cells)")
print("OK")
