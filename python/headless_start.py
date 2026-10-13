"""Startet den Programmgenerator ohne Tk und zeigt die geladenen Blaetter an.

Ablage: Diese Datei in den Projektordner (neben pyMobaLedLib.py) legen. Ausserdem:
  - ExcelAPI/XLA_Application.py durch XLA_Application_headless.py ersetzen,
  - ExcelAPI/headless_sheet.py, headless_controller.py, headless_app_controller.py,
    headless_proggen.py in den Projektordner (oder Pythonpfad) kopieren,
  - mlpyproggen/Prog_Generator.py durch die umgebaute Version ersetzen.
Start:  set MLL_HEADLESS=1   (Linux/Mac: export MLL_HEADLESS=1)   dann   python headless_start.py
"""
import logging
import os
import sys

os.environ["MLL_HEADLESS"] = "1"
here = os.path.dirname(os.path.abspath(__file__))
if here not in sys.path:
    sys.path.insert(0, here)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

# Uebergangsloesung: Die Python-UserForms (Userform_*.py) legen beim Start Tk-Variablen an
# (tk.IntVar usw.) und brauchen dafuer ein Tk-Wurzelfenster. Wir erzeugen ein unsichtbares.
# Spaeter werden die Formulare durch Web-Dialoge ersetzt, dann entfaellt das.
# Abschalten: set MLL_TK_ROOT=0
import no_tk                                                    # noqa: E402  (Ersatz fuer tkinter ohne Tk/Display)

_hidden_root = no_tk.real_tk_root() if os.environ.get("MLL_TK_ROOT", "1") == "1" else None
if _hidden_root is None:
    no_tk.install()                                             # Raspberry Pi ohne Bildschirm

from headless_app_controller import HeadlessAppController     # noqa: E402

ARGS = {"loaddatafile": "True", "logfilename": os.path.join(here, "headless.log")}   # wie COMMAND_LINE_ARG_DICT
ctrl = HeadlessAppController(mainfile_dir=here, command_line_args=ARGS)
if globals().get("_hidden_root") is not None:
    ctrl.attach_tk_root(_hidden_root)       # Uebergang: Tk-Formulare erwarten ein Tk-Widget als Controller
ctrl.on_status.append(lambda text, fg: print("STATUS:", text))
ctrl.create_excel_application()

from headless_proggen import HeadlessProgGeneratorPage         # noqa: E402

page = HeadlessProgGeneratorPage(ctrl)
wb = page.workbook
print("\nWorkbook:", wb.Name)
for ws in wb.sheets:
    sh = ws.tksheet
    print(f"  {ws.Name:22s} {sh.get_total_rows():6d} Zeilen x {sh.get_total_columns():3d} Spalten  ({type(sh).__name__})")

dcc = wb.sheets[0]
print("\nBlatt", dcc.Name, "- erste 5 Zeilen (bis Spalte 8):")
for row in dcc.tksheet.get_data(0, 0, 5, 8):
    print("  ", row)
