# Datei-Version: 1.05 (2026-10-17) - headless_pattgen.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_pattgen.py
# Path:           headless/headless_pattgen.py
# Version:        1.05
# Last Update:    2026-10-17
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-17  neu: Tk-freie Seite des Patterngenerators (Arbeitsmappe PatternWorkbook ohne Tk oeffnen, Formulare als Platzhalter, activated())
#   1.01  2026-10-17  Aktionen fuer den Browser (select_cell, set_value, update_grafik, Spalten, new_sheet, set_rgb_led), Haken RGB LED, protected_columns, info_text
#   1.02  2026-10-17  Spaltenbreiten fuer den Browser (D 200, E 240, ab F 60), right_aligned_columns
#   1.03  2026-10-17  Auswahlereignis mit Datenindizes (Selection.Row war bei ausgeblendeten Zeilen verschoben), Balken nach Spalte hinzufuegen/entfernen neu zeichnen
#   1.04  2026-10-17  Muster-Spalten gleich breit (56), NormColWidth 56; clear_cell und paste_text (Entf, Ausschneiden, Einfuegen)
#   1.05  2026-10-17  export_to_proggen (mit Pruefung vor dem Export) und import_from_proggen
# ----------------------------------------------------------------------------------------------
"""Tk-freier Ersatz fuer Pattern_GeneratorPage: baut die Arbeitsmappe "PatternWorkbook" des Patterngenerators.

Entspricht dem Teil von Pattern_GeneratorPage.__init__, der die Arbeitsmappe anlegt (ohne Frames und Knoepfe). Die Beschreibung der
Arbeitsmappe kommt aus Pattern_Generator.build_workbook_dict (gemeinsame Quelle mit der Tk-Seite). Voraussetzung: MLL_HEADLESS=1 und
die Headless-Variante von ExcelAPI/XLA_Application.py (wie beim Programmgenerator, siehe headless_proggen.py).

Die Seite macht den Programmgenerator NICHT zum inaktiven Arbeitsbuch: Nach dem Oeffnen bleibt das zuvor aktive Arbeitsbuch aktiv. Fuer alle
Aktionen des Patterngenerators (Zelle aendern, Knoepfe) gibt es activated(): es schaltet fuer die Dauer des Aufrufs auf PatternWorkbook um
und danach zurueck. Die Excel-Schicht (X02.ActiveSheet, X02.ThisWorkbook) kennt immer nur ein aktives Arbeitsbuch.

Die Tk-Formulare (Auswahl, Optionen, Beispiele ...) werden nicht angelegt; HeadlessForm ersetzt sie und protokolliert die Aufrufe.
"""
from __future__ import annotations

import contextlib
import logging
import os
import re  # v1.01
import types  # v1.01

import userdata                                    # Datenordner ausserhalb des Projektordners

from ExcelAPI.headless_sheet import Selected  # v1.03

import ExcelAPI.XLA_Application as X02
import mlpyproggen.Pattern_Generator as PGP        # importiert tkinter, instanziiert aber keine GUI
import pattgen.D00_Forms as D00
import pattgen.DieseArbeitsmappe as AM
import pattgen.M01_Public_Constants_a_Var as M01  # v1.04
import pattgen.M03_Analog_Trend as M03  # v1.01
import pattgen.M11_To_Prog_Gen as M11  # v1.05
import pattgen.Tabelle9 as T09  # v1.01
import pgcommon.G00_common as G00  # v1.01
from headless.headless_proggen import HeadlessStatusForm

logger = logging.getLogger(__name__)


class HeadlessForm:
    """Platzhalter fuer ein Tk-Formular des Patterngenerators, das es im Web noch nicht gibt: Aufrufe werden protokolliert (INFO) und liefern None."""

    def __init__(self, name):
        self._name = name
        self.UserForm_res = None

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)

        def _call(*args, **kwargs):
            logger.info("Patterngenerator: Formular %s.%s%r gibt es im Web noch nicht", self._name, name, args)
            return None
        return _call


FORM_NAMES = ("Select_COM_Port_UserForm", "Select_GotoNr_Form", "MainMenu_Form", "Select_from_Sheet_Form", "Examples_UserForm",
              "UserForm_Attiny_direct_program")


def init_userforms_headless(controller):
    """Ersatz fuer pattgen.D00_Forms.init_UserForms: keine Tk-Fenster, sondern Platzhalter (und die Statusanzeige ueber die Statuszeile)"""
    D00.StatusMsg_UserForm = HeadlessStatusForm(controller)
    for name in FORM_NAMES:
        setattr(D00, name, HeadlessForm(name))


class HeadlessControl:  # v1.01
    """Ersatz fuer ein Steuerelement auf dem Blatt (Haken RGB LED): pattgen liest ActiveSheet.RGB_LED_CheckBox.Value und .Enabled"""  # v1.01

    def __init__(self, name, value=False):  # v1.01
        self.Name = name  # v1.01
        self.Value = value  # v1.01
        self.Enabled = True  # v1.01


# Breiten der Web-Ansicht in Pixeln (0-basierte Spalte). Die Excel-Schicht rechnet die Formen der grafischen Anzeige (Balken) mit denselben
# Spaltenbreiten wie die Tabelle im Browser; deshalb werden sie im Blatt selbst gesetzt, bevor die Grafik zum ersten Mal berechnet wird.
COLUMN_WIDTHS = {3: 200, 4: 240}                       # D: Beschriftungen, E: Eingaben und Ergebnisse  # v1.04
PATTERN_COLUMN_FIRST, PATTERN_COLUMN_WIDTH = 5, 56     # ab Spalte F: Muster. M04 passt benutzte Spalten an die Dauer an, ausgehend von NormColWidth (hier ebenfalls 56)  # v1.04


def col_index(letters):  # v1.01
    """A -> 0, Z -> 25, AA -> 26"""  # v1.01
    n = 0  # v1.01
    for ch in letters.upper():  # v1.01
        n = n * 26 + ord(ch) - 64  # v1.01
    return n - 1  # v1.01


class HeadlessPatternGeneratorPage:
    workbookname = "PatternWorkbook"

    def __init__(self, controller):
        self.controller = controller
        self.Application = controller.ExcelApplication
        self.tabClassName = "PatternConfiguratorPage"
        self.tabname = "Patterngenerator"             # der Name wird nicht uebersetzt
        self.title = "Patterngenerator"
        controller.set_statusmessage("Erstelle Patterngenerator Seite ...", fg="green")
        PGP.set_global_controller(controller)
        PGP.dialog_parent = None                      # Tk-Elternfenster fuer Dialoge gibt es nicht

        self.default_font = controller.defaultfontnormal
        self.default_boldfont = (self.default_font[0], self.default_font[1], "bold")
        self.default_smallfont = controller.defaultfontsmall

        # Projektordner wie im Original: filedir = mlpyproggen, filedir2 = Projektordner (dort liegt csv/PA_*.csv)
        filedir = os.path.dirname(os.path.realpath(PGP.__file__))
        self.filedir2 = os.path.dirname(filedir)
        # Die Sicherung der Tabellen liegt flach im Datenordner (der Name aus DefaultConstants enthaelt "../")
        self.tempworkbookFilname = controller.tempworkbookFilname
        rel_name = self.tempworkbookFilname + "_" + self.workbookname + ".json"
        temp_workbook_filename = os.path.join(controller.data_dir, userdata.flat(rel_name))

        workbook_dict = PGP.build_workbook_dict(self.default_font, self.default_smallfont, self.default_boldfont, self.Workbook_Open)
        self.workbook_dict = workbook_dict  # v1.01
        D00.init_UserForms = lambda: init_userforms_headless(controller)       # statt der Tk-Formulare (Aufruf in Workbook_Open)
        # Erster Start: Die Tabellen stammen noch aus den CSV-Dateien (alte Ergebnisse), sie werden einmal neu berechnet
        self.fresh = not os.path.exists(temp_workbook_filename)

        X02.Application.EnableEvents = True
        previous_wb, previous_this = getattr(X02, "ActiveWorkbook", None), getattr(X02, "ThisWorkbook", None)
        self.workbook = self.Application.Workbooks.Open(
            ParentFrame=None,                          # kein Tk-Frame: Headless-Betrieb
            FileName=temp_workbook_filename,
            path=self.filedir2,
            pyProgPath=self.filedir2,
            workbookName=self.workbookname,
            InitWorkBookFunction=None,
            macro_caller=self,
            workbookdict=workbook_dict,
            start_sheet=PGP.start_sheet,
            controller=controller)

        for sheet in self.workbook.sheets:
            sheet.SetChangedCallback(PGP.wschangedcallback)
            sheet.SetSelectedCallback(PGP.wsselectedcallback)
            sheet.SetCalculationCallback(PGP.wscalculationcallback)
            sheet.SetInitDataFunction(PGP.SheetInitDataProc)

        self.workbook.SetInitWorkbookFunction(None)
        M01.NormColWidth = PATTERN_COLUMN_WIDTH          # Normalbreite der Muster-Spalten (M04.Normal_Column_With, 49 im Original)  # v1.04
        self.attach_controls()  # v1.01
        for ws in self.workbook.sheets:  # v1.02
            self.apply_column_widths(ws)  # v1.02
        PGP.ThisWorkbook = self.workbook
        PGP.dialog_parent = self
        self.workbook.activate_sheet(PGP.start_sheet)
        # Das Oeffnen macht PatternWorkbook zum aktiven Arbeitsbuch: das vorige (Programmgenerator) wieder aktivieren
        if previous_wb is not None and previous_wb is not self.workbook:
            self.Application.setActiveWorkbook(previous_wb.Name)
        if previous_this is not None:
            X02.ThisWorkbook = previous_this

    # Workbooks.Open setzt macro_caller.ThisWorkbook; wie im Original auf das Modul-Global abbilden
    def get_ThisWorkbook(self):
        return PGP.ThisWorkbook

    def set_ThisWorkbook(self, value):
        PGP.ThisWorkbook = value

    ThisWorkbook = property(fget=get_ThisWorkbook, fset=set_ThisWorkbook)

    def Workbook_Open(self):
        """Ereignis Workbook_Open (wie Pattern_GeneratorPage.Workbook_Open, aber mit den Platzhaltern statt der Tk-Formulare)"""
        D00.init_UserForms()
        AM.Workbook_Open()

    @contextlib.contextmanager
    def activated(self):
        """PatternWorkbook fuer die Dauer des Blocks zum aktiven Arbeitsbuch machen (X02.ActiveSheet, X02.ThisWorkbook), danach das vorige wieder"""
        previous_wb, previous_this = getattr(X02, "ActiveWorkbook", None), getattr(X02, "ThisWorkbook", None)
        self.Application.setActiveWorkbook(self.workbookname)
        X02.ThisWorkbook = self.workbook
        try:
            yield self
        finally:
            if previous_wb is not None and previous_wb is not self.workbook:
                self.Application.setActiveWorkbook(previous_wb.Name)
            if previous_this is not None:
                X02.ThisWorkbook = previous_this

    def recalculate(self):
        """Formeln des aktiven Blatts berechnen und das Aenderungsereignis ausloesen (Zelle E5), wie der Knopf Neu berechnen"""  # v1.01
        with self.activated():
            X02.ActiveSheet.EventWSchanged(X02.Cells(5, 5))

    # ------------------------------------------------------------------ Aktionen der Werkzeugleiste und der Tabelle
    # Sie laufen im Worker-Thread (Dialoge der Makros erscheinen im Browser) und innerhalb von activated().
    def attach_controls(self):  # v1.01
        """Haken RGB LED: pattgen liest ihn als Eigenschaft des Blatts; die Tk-Steuerelemente gibt es hier nicht"""  # v1.01
        for ws in self.workbook.sheets:  # v1.01
            if not hasattr(ws, "RGB_LED_CheckBox"):  # v1.01
                ws.RGB_LED_CheckBox = HeadlessControl("RGB_LED_CheckBox")  # v1.01

    def apply_column_widths(self, ws):  # v1.02
        """Breitere Spalten fuer Beschriftung, Eingabe und Muster (die Breiten der Blattdefinition sind fuer Excel gedacht und im Browser zu schmal)"""  # v1.02
        if ws.Name not in ("Main", "PG-Temp"):  # v1.02
            return  # v1.02
        sh = ws.tksheet  # v1.02
        for c in range(sh.get_total_columns()):  # v1.02
            width = COLUMN_WIDTHS.get(c, PATTERN_COLUMN_WIDTH if c >= PATTERN_COLUMN_FIRST else None)  # v1.04
            if width is not None:  # v1.02
                sh.column_width(c, width)  # v1.02

    def right_aligned_columns(self, sheetname):  # v1.02
        """Rechtsbuendige Spalten (Formating/ColumnAlignment, Schluessel "ex": zum Beispiel die Beschriftungen in Spalte D)"""  # v1.02
        sheets = self.workbook_dict["SheetDict"]  # v1.02
        fmt = (sheets.get(sheetname) or sheets["Main"]).get("Formating", {})  # v1.02
        entry = fmt.get("ColumnAlignment", {}).get("ex", ())  # v1.02
        return {col_index(str(x)) for x in ([entry] if isinstance(entry, str) else entry)}  # v1.02

    def use(self, ws):  # v1.01
        """Das Blatt zum aktiven Blatt der Arbeitsmappe machen (die Makros arbeiten mit X02.ActiveSheet)"""  # v1.01
        if X02.ActiveSheet is not ws:  # v1.01
            ws.Activate()  # v1.01

    def select_cell(self, ws, row, col):  # v1.01
        self.use(ws)  # v1.01
        # Datenindizes (0-basiert): HeadlessSheet rechnet auf angezeigte Zeilen um. CRange.Select() setzt die Auswahl ohne diese Umrechnung,
        # dann liegt sie bei ausgeblendeten Zeilen (Patterngenerator: 22) an der falschen Stelle.
        ws.tksheet.set_selection(cells={(row - 1, col - 1)}, current=(row - 1, col - 1))  # v1.01
        # X02.CRange(row, col, ws=ws).Select()  # v1.01 (ersetzt: falsche Zeile bei ausgeblendeten Zeilen)
        # Wie das tksheet-Ereignis: setzt die globale Selection der Excel-Schicht (Add_or_Del_Columns liest X02.Selection) und ruft
        # Worksheet_SelectionChange des Patterngenerators
        # Das Ereignis erwartet Datenindizes (selected.row + 1 ist die Zeile des Ziels); get_currently_selected() liefert angezeigte Indizes
        ws.Evt_SheetSelectionChange(types.SimpleNamespace(selected=Selected(row - 1, col - 1, "cell")))  # v1.03

    def set_value(self, ws, row, col, value):  # v1.01
        self.use(ws)  # v1.01
        X02.CRange(row, col, ws=ws).Value = value        # loest wie in Excel Worksheet_Change aus  # v1.01

    def update_grafik(self, ws):  # v1.01
        """Knopf Aktualisieren der Tk-Seite: Grafik (Balken) neu aufbauen"""  # v1.01
        self.use(ws)  # v1.01
        X02.Application.Caller = "Update"  # v1.01
        M03.Update_Grafik()  # v1.01

    def add_columns(self, ws):  # v1.01
        self.use(ws)  # v1.01
        PGP.Add_Col_Button_Click()  # v1.01
        M03.Update_Grafik()                             # die Balken zeichnet die Excel-Schicht dabei nicht neu (alte Formen blieben stehen)  # v1.03

    def del_columns(self, ws):  # v1.01
        self.use(ws)  # v1.01
        PGP.Del_Col_Button_Click()  # v1.01
        M03.Update_Grafik()  # v1.03

    def new_sheet(self, ws):  # v1.01
        """Neues Blatt (Kopie des aktuellen): der Name wird ueber G00.InputBox im Browser abgefragt"""  # v1.01
        self.use(ws)  # v1.01
        G00.New_Sheet()  # v1.01
        self.attach_controls()  # v1.01

    def export_to_proggen(self, ws):  # v1.05
        """Knopf 'Export zu ProgGen': Makro des Blatts in eine Zeile des Programm Generators eintragen.
        Vorher die Pruefungen des Excel-Originals (Makroname, LED-Tabelle, Dauer-Zeile; im Tk-Port waren sie ausgelassen).
        Die Zeilenauswahl erscheint danach im Browser (web_form_exchange), das Eintragen macht der Rueckruf des Originals."""
        self.use(ws)  # v1.05
        self.update_table_empty_flag(ws)  # v1.05
        try:  # v1.05
            ok = M11.Check_Table_before_Copy(True)  # v1.05
        except Exception:  # noqa: BLE001  # v1.05
            logger.exception("Pruefung vor dem Export nicht moeglich, es geht ohne Pruefung weiter")  # v1.05
            ok = True  # v1.05
        if ok:  # v1.05
            T09.Prog_Generator_Button_Click()  # v1.05

    def update_table_empty_flag(self, ws):  # v1.05
        """F44 (M01.TableEmptyMsgRng) ist in Excel eine Formel, die einen Text liefert, wenn in der LED-Tabelle nichts markiert ist. Die
        CSV-Datei enthaelt nur ihren Wert (leer), deshalb hier nachgerechnet, bevor M11.Check_Table_before_Copy ihn liest."""
        sheet = ws.tksheet  # v1.05
        rows = int(X02.Range(M01.LED_Cnt_Rng))  # v1.05
        def used(value):                                # in einer Zelle der Tabelle (Spalte BY) steht eine Liste leerer Texte: zaehlt nicht  # v1.05
            return isinstance(value, str) and value.strip() != ""  # v1.05
        filled = any(used(sheet.get_cell_data(r - 1, c - 1))  # v1.05
                     for r in range(M01.LEDsTAB_R, M01.LEDsTAB_R + rows) for c in range(M01.Dauer_Col1, sheet.get_total_columns() + 1))  # v1.05
        events = X02.Application.EnableEvents  # v1.05
        X02.Application.EnableEvents = False  # v1.05
        try:  # v1.05
            X02.Range(M01.TableEmptyMsgRng).Value = "" if filled else "leer"  # v1.05
        finally:  # v1.05
            X02.Application.EnableEvents = events  # v1.05

    def import_from_proggen(self, ws):  # v1.05
        """Knopf 'Import von ProgGen': Makro aus einer Zeile des Programm Generators in das Blatt einlesen"""  # v1.05
        self.use(ws)  # v1.05
        T09.Import_from_ProgGen_Button_Click()  # v1.05

    def clear_cell(self, ws, row, col):  # v1.04
        """Zelle leeren (Entf, Ausschneiden); gesperrte Spalten bleiben unveraendert"""  # v1.04
        if col - 1 in self.protected_columns(ws.Name):  # v1.04
            return  # v1.04
        self.set_value(ws, row, col, "")  # v1.04

    def paste_text(self, ws, row, col, text):  # v1.04
        """Text aus der Zwischenablage ab der Zelle einfuegen (Zeilen durch Zeilenwechsel, Spalten durch Tabulator, wie in Excel).
        Mehrere Zellen werden ohne Ereignisse geschrieben und danach einmal neu berechnet. Gesperrte Spalten werden uebersprungen."""
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")  # v1.04
        if lines and lines[-1] == "":  # v1.04
            lines.pop()  # v1.04
        grid = [line.split("\t") for line in lines]  # v1.04
        if not grid:  # v1.04
            return  # v1.04
        protected = self.protected_columns(ws.Name)  # v1.04
        if len(grid) == 1 and len(grid[0]) == 1:  # v1.04
            if col - 1 not in protected:  # v1.04
                self.set_value(ws, row, col, grid[0][0])  # v1.04
            return  # v1.04
        self.use(ws)  # v1.04
        events = X02.Application.EnableEvents  # v1.04
        X02.Application.EnableEvents = False  # v1.04
        try:  # v1.04
            for i, cells in enumerate(grid):  # v1.04
                for j, value in enumerate(cells):  # v1.04
                    if col + j - 1 not in protected:  # v1.04
                        X02.CRange(row + i, col + j, ws=ws).Value = value  # v1.04
        finally:  # v1.04
            X02.Application.EnableEvents = events  # v1.04
        ws.EventWSchanged(X02.Cells(5, 5))  # v1.04

    def set_rgb_led(self, ws, value):  # v1.01
        self.use(ws)  # v1.01
        ws.RGB_LED_CheckBox.Value = bool(value)  # v1.01
        T09.RGB_LED_CheckBox_Click()  # v1.01

    def protected_columns(self, sheetname):  # v1.01
        """Spalten, die nicht editierbar sind (Formating/ProtectedCells der Blattdefinition, zum Beispiel A:D)"""  # v1.01
        sheets = self.workbook_dict["SheetDict"]  # v1.01
        fmt = (sheets.get(sheetname) or sheets["Main"]).get("Formating", {})  # v1.01
        cols = set()  # v1.01
        for entry in fmt.get("ProtectedCells", ()):  # v1.01
            for part in ([entry] if isinstance(entry, str) else entry):  # v1.01
                m = re.fullmatch(r"([A-Za-z]+):([A-Za-z]+)", str(part).strip())  # v1.01
                if m:  # v1.01
                    cols.update(range(col_index(m.group(1)), col_index(m.group(2)) + 1))  # v1.01
        return cols  # v1.01

    def info_text(self):  # v1.01
        """Beschreibungstext des Blatts (im Original eine Textbox auf dem Blatt)"""  # v1.01
        for form in self.workbook_dict["SheetDict"]["Main"].get("Controls", {}).values():  # v1.01
            for comp in form.get("Components", []):  # v1.01
                if comp.get("Name") == "Text_Box1":  # v1.01
                    return str(comp.get("Caption", ""))  # v1.01
        return ""  # v1.01

    def sheet(self, name):
        return self.workbook.SheetsDict[name]

    def find_sheet(self, name):  # v1.01
        """Blatt mit dem Namen oder None (SheetsDict kennt kein get)"""  # v1.01
        for ws in self.workbook.sheets:  # v1.01
            if ws.Name == name:  # v1.01
                return ws  # v1.01
        return None  # v1.01

    def visible_sheets(self, show_hidden=False):
        """Blaetter, die als Reiter erscheinen (Languages, Goto_Activation_Entries ... blendet M02_Main.Init aus)"""
        result = []
        for ws in self.workbook.sheets:
            try:
                visible = ws.Visible
            except Exception:                          # noqa: BLE001
                visible = True
            if visible is not False or show_hidden:
                result.append(ws)
        return result


# ----------------------------------------------------------------------------------------------
# Methoden der Tk-Seite (Pattern_GeneratorPage), die nur auf self.controller arbeiten (Konfigurationszugriff)
_BORROWED = ("getConfigData", "readConfigData", "setConfigData", "setParamData", "get_param_config_dict")
for _name in _BORROWED:
    _fn = PGP.Pattern_GeneratorPage.__dict__.get(_name)
    if _fn is None:
        logger.warning("Methode %s in Pattern_GeneratorPage nicht gefunden", _name)
    else:
        setattr(HeadlessPatternGeneratorPage, _name, _fn)


def _update(self):
    pass


def _after(self, ms, func=None, *args):
    return self.controller.after(ms, func, *args)


HeadlessPatternGeneratorPage.update = _update
HeadlessPatternGeneratorPage.after = _after
