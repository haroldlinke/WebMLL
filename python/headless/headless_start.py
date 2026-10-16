# Datei-Version: 1.03 (2026-10-15) - headless_start.py
"""Startet den Programmgenerator ohne Tk und zeigt die geladenen Blaetter an.

Ablage: Diese Datei liegt im Ordner headless des Projektordners (neben pyMobaLedLib.py). Ausserdem muessen die angepassten Dateien
  ExcelAPI/XLA_Application.py, ExcelAPI/headless_sheet.py und mlpyproggen/Prog_Generator.py an ihrem Platz liegen.
Start aus dem Projektordner:  set MLL_HEADLESS=1   (Linux/Mac: export MLL_HEADLESS=1)   dann   python headless/headless_start.py
"""
import logging
import os
import sys

os.environ["MLL_HEADLESS"] = "1"
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # Projektordner (ueber dem Ordner headless)
if here not in sys.path:
    sys.path.insert(0, here)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

# Die Python-UserForms (Userform_*.py) legen beim Start Tk-Variablen an (tk.IntVar usw.). Standard ist der Ersatz no_tk (weder Tk noch
# ein Bildschirm noetig). Mit MLL_TK_ROOT=1 wird stattdessen ein unsichtbares echtes Tk-Wurzelfenster versucht (nur zum Vergleichen).
import no_tk                                                    # noqa: E402  (Ersatz fuer tkinter ohne Tk/Display)

_hidden_root = no_tk.real_tk_root() if os.environ.get("MLL_TK_ROOT", "0") == "1" else None
if _hidden_root is None:
    no_tk.install()                                             # Standard: Ersatz ohne Tk

from headless.headless_app_controller import HeadlessAppController     # noqa: E402

import userdata                                                                        # noqa: E402  (Datenordner)

ARGS = {"loaddatafile": "True", "logfilename": userdata.log_file()}   # wie COMMAND_LINE_ARG_DICT
ctrl = HeadlessAppController(mainfile_dir=here, command_line_args=ARGS)
if globals().get("_hidden_root") is not None:
    ctrl.attach_tk_root(_hidden_root)       # Uebergang: Tk-Formulare erwarten ein Tk-Widget als Controller
ctrl.on_status.append(lambda text, fg: print("STATUS:", text))
ctrl.create_excel_application()

from headless.headless_proggen import HeadlessProgGeneratorPage         # noqa: E402

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
