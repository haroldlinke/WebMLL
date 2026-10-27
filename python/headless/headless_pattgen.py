# Datei-Version: 1.16 (2026-10-26) - headless_pattgen.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_pattgen.py
# Path:           headless/headless_pattgen.py
# Version:        1.16
# Last Update:    2026-10-26
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-17  neu: Tk-freie Seite des Patterngenerators (Arbeitsmappe PatternWorkbook ohne Tk oeffnen, Formulare als Platzhalter, activated())
#   1.01  2026-10-17  Aktionen fuer den Browser (select_cell, set_value, update_grafik, Spalten, new_sheet, set_rgb_led), Haken RGB LED, protected_columns, info_text
#   1.02  2026-10-17  Spaltenbreiten fuer den Browser (D 200, E 240, ab F 60), right_aligned_columns
#   1.03  2026-10-17  Auswahlereignis mit Datenindizes (Selection.Row war bei ausgeblendeten Zeilen verschoben), Balken nach Spalte hinzufuegen/entfernen neu zeichnen
#   1.04  2026-10-17  Muster-Spalten gleich breit (56), NormColWidth 56; clear_cell und paste_text (Entf, Ausschneiden, Einfuegen)
#   1.05  2026-10-17  export_to_proggen (mit Pruefung vor dem Export) und import_from_proggen
#   1.06  2026-10-18  Beispiele, Laden und Speichern, Loeschen (Optionen): load_examples, load_upload, save_for_download, delete_sheet, delete_all_data_sheets; Textfelder und Formularknoepfe der Dateien werden gemerkt und beim Speichern wieder geschrieben
#   1.07  2026-10-18  ensure_grafik: Balken beim Anzeigen zeichnen, wenn das Blatt keine hat (nach einem Neustart fehlen sie)
#   1.07  2026-10-18  Doppelklick-Dialoge Spezial Mode und RGB Modul Nr: HeadlessSelectFromSheetForm (Ersatz fuer Select_from_Sheet_Form), led_address_dialog, HeadlessPresenters, dialog_cells, run_cell_dialog
#   1.08  2026-10-18  dialog_cells: auch die Seite Main (Is_Data_Sheet des Originals fragt nur nach dem Bereich RGB_Modul_Nr), nur die Hilfsblaetter ausnehmen
#   1.09  2026-10-18  Goto Aktivierung (3c): Doppelklick, Auswahlliste mit Check_Param_Goto, HeadlessUserFormOther (Parameterdialog fuer Counter, RandomTime ...), check_param_value
#   1.10  2026-10-19  Bilder: sync_pictures und restore_pictures (nach dem Neustart), insert_picture (Bild einfuegen), remove_pictures, image_size; die Bilder bleiben, wo sie sind (nur Pfad und Lage werden gesichert)
#   1.11  2026-10-19  led_row_count: Zahl der LED-Zeilen der Tabelle (fuer die Rahmen)
#   1.12  2026-10-19  restore_dynamic_rows: nach dem Neustart Goto- und Spezial-Mode-Zeilen neu bestimmen (Hide_Show_*_If_Enabled)
#   1.13  2026-10-19  restore_dynamic_rows: auch die Zeile Goto Aktivierung (Zeile 13) neu bestimmen (Hide_Show_Check_Goto_Activation); die Vorlage versteckt sie, nach dem Neustart fehlte sie
#   1.14  2026-10-23  Dateien im Pattern-Format aus dem Excel-Programm (cp1252) werden auch von sheet_names_in_file und object_lines_in_file richtig gelesen (Blattnamen, Textfelder und Formularknoepfe), nicht nur von Load_Sheets
#   1.15  2026-10-26  Speichern im Pattern-Format: Datei wird (Programm Einstellungen, Standard an) in den Windows-Zeichensatz umgeschrieben, wenn alle Zeichen Platz haben (fuer das Excel-Programm)
#   1.16  2026-10-26  Zusammengesetzte Meldungen (Verkettungen und f-Strings) mit tr(...) uebersetzbar gemacht
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
import shutil  # v1.06
import struct  # v1.10
import tempfile  # v1.06
import types  # v1.01
import zipfile  # v1.06

import userdata                                    # Datenordner ausserhalb des Projektordners

from ExcelAPI.headless_sheet import Selected  # v1.03

import ExcelAPI.XLA_Application as X02
import mlpyproggen.Pattern_Generator as PGP        # importiert tkinter, instanziiert aber keine GUI
import pattgen.D00_Forms as D00
import pattgen.DieseArbeitsmappe as AM
import pattgen.M01_Public_Constants_a_Var as M01  # v1.04
import pattgen.M03_Analog_Trend as M03  # v1.01
import pattgen.M07_Save_Sheet_Data as M07  # v1.06
import pattgen.M02_Main as M02A  # v1.13
import pattgen.M06_Goto_Graph as M06G  # v1.12
import pattgen.M08_Load_Sheet_Data as M08  # v1.06
import pattgen.M14_Select_GotoAct as M14  # v1.09
import pattgen.M60_Select_LED as M60  # v1.07
import pattgen.M11_To_Prog_Gen as M11  # v1.05
import pattgen.Tabelle9 as T09  # v1.01
import pgcommon.G00_common as G00  # v1.01
from vb2py.vbfunctions import VBMissingArgument  # v1.07
from headless.headless_proggen import HeadlessStatusForm
try:  # v1.16
    from _web.web_i18n import tr  # v1.16
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v1.16
    def tr(text, **values):  # v1.16
        return text.format(**values) if values else text  # v1.16

logger = logging.getLogger(__name__)

# Beispielsammlungen (Dateien im Ordner Pattern_Config_Examples) in der Reihenfolge und mit den Namen des Formulars Examples_UserForm
EXAMPLE_COLLECTIONS = (("Basic", "Allgemein"), ("Traffic_Lights", "Ampeln"), ("ConstrWarnLight", "Baustellenlichter"), ("Signals", "Signale"),  # v1.06
                       ("Signals_3D", "Signale 3D Druck RGB LEDs"), ("Sounds", "Sounds"), ("Status_Buttons", "Taster mit Status Anzeige"),  # v1.06
                       ("Charlieplexing", "Charlieplexing"), ("Illuminations", "Illuminations"))  # v1.06
# Blaetter, die keine Datenblaetter sind (M08.Is_Normal_Data_Sheet kennt PG-Temp nicht und wuerde danach fragen)
NON_DATA_SHEETS = (M01.MAIN_SH, M01.LANGUAGES_SH, M01.GOTO_ACTIVATION_SH, M01.PAR_DESCRIPTION_SH, M01.SPECIAL_MODEDLG_SH, "Named_Ranges", "PG-Temp")  # v1.06


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

# Zellen, auf die ein Doppelklick einen Dialog oeffnet (M02_Main.Proc_DoubleClick): Art und Name des benannten Bereichs
DOUBLECLICK_CELLS = (("special_mode", "Special_Mode"), ("rgb_modul_nr", "RGB_Modul_Nr"), ("goto_act", "Goto_Aktivierung"))  # v1.09


class HeadlessPresenters:  # v1.07
    """Hier setzt die Web-Oberflaeche die Funktionen, die Auswahldialoge im Browser zeigen (Aufruf aus dem Worker-Thread, sie warten auf die Antwort)"""  # v1.07
    select = None          # Funktion(Anforderung: dict) -> {"action": "select" | "delete" | "abort", "rows": [Zeilen]} oder None  # v1.07
    number = None          # Funktion(Anforderung: dict) -> int oder None  # v1.07
    params = None          # Funktion(Anforderung: dict) -> Liste der Werte (Texte) oder None  # v1.09


class HeadlessSelectFromSheetForm:  # v1.07
    """Ersatz fuer Select_from_Sheet_Form: eine Liste aus einem Blatt der Arbeitsmappe zur Auswahl anbieten (Spezial Mode, Goto Aktivierung).
    Rueckgabe wie im Original: '' (abgebrochen), 'DELETE' oder 'Name,Zeile' (mehrere durch Leerzeichen getrennt). Das Tk-Formular lieferte den ganzen
    Listeneintrag 'Name : Kurzbeschreibung' als Namen, hier ist es wie in VBA nur der Name."""

    def Show_Form(self, ListDataSh, Dialog_Titel, Head_Label_Txt, Description_Label_Txt, oCheck_Param_Func=VBMissingArgument,  # v1.07
                  oExpert_CheckBox=VBMissingArgument, oExpert_CheckBox_Checked=VBMissingArgument, oDelete_Button=VBMissingArgument,  # v1.07
                  oExp_Mode_COL=0, oLowerWin_COL=0, oName_Dat_COL=4, oShortDescCOL=5, oMiddleWinCOL=0, oDialog_Dat_ROW1=4):  # v1.07
        present = HeadlessPresenters.select  # v1.07
        if present is None:  # v1.07
            logger.info("Patterngenerator: Auswahlliste %s: keine Anzeige verfuegbar", ListDataSh)  # v1.07
            return ""  # v1.07

        def given(value):  # v1.07
            return value is not VBMissingArgument and value not in ("", None, False)  # v1.07
        check = getattr(M14, str(oCheck_Param_Func), None) if given(oCheck_Param_Func) else None      # zum Beispiel Check_Param_Goto  # v1.09
        sheet = X02.Sheets(ListDataSh)  # v1.07
        last = sheet.get_LastUsedRow()  # v1.07
        entries = []  # v1.07
        for r in range(int(oDialog_Dat_ROW1), last + 1):  # v1.07
            name = str(sheet.Cells(r, oName_Dat_COL)).strip()  # v1.07
            if name == "" and str(sheet.Cells(r + 1, oName_Dat_COL)).strip() == "" and str(sheet.Cells(r + 2, oName_Dat_COL)).strip() == "":  # v1.07
                break                                                                   # wie Add_Filtered: drei leere Namen beenden die Liste  # v1.07
            if name == "":  # v1.07
                continue  # v1.07
            if check is not None:  # v1.09
                try:  # v1.09
                    if not check(r):  # v1.09
                        continue  # v1.09
                except TypeError:                                   # Optionales Argument (zum Beispiel ExpOutCnt) ohne Wert: alle Eintraege zeigen  # v1.09
                    pass  # v1.09
            entries.append({  # v1.07
                "row": r, "name": name,  # v1.07
                "short": str(sheet.Cells(r, oShortDescCOL)).strip(),  # v1.07
                "middle": str(sheet.Cells(r, oMiddleWinCOL)).replace("|", "\n").strip() if oMiddleWinCOL > 0 else "",  # v1.07
                "lower": " ".join(str(sheet.Cells(r, oLowerWin_COL)).split()) if oLowerWin_COL > 0 else "",  # v1.07
                "expert": oExp_Mode_COL > 0 and str(sheet.Cells(r, oExp_Mode_COL)).strip() != ""})  # v1.07
        request = {"title": str(Dialog_Titel), "head": str(Head_Label_Txt), "description": str(Description_Label_Txt), "entries": entries,  # v1.07
                   "expert_caption": str(oExpert_CheckBox) if given(oExpert_CheckBox) else "", "expert_checked": bool(given(oExpert_CheckBox_Checked)),  # v1.07
                   "delete_button": bool(given(oDelete_Button))}  # v1.07
        result = present(request)  # v1.07
        if not result or result.get("action") == "abort":  # v1.07
            return ""  # v1.07
        if result.get("action") == "delete":  # v1.07
            return "DELETE"  # v1.07
        names = {e["row"]: e["name"] for e in entries}  # v1.07
        return " ".join(f"{names[row]},{row}" for row in result.get("rows", []) if row in names)  # v1.07


TIME_UNITS = {"Min": 60000, "Sek": 1000, "sek": 1000, "Sec": 1000, "sec": 1000, "Ms": 1, "ms": 1}      # wie Userform_Other.Check_Time_String  # v1.09


def _number(text):  # v1.09
    try:  # v1.09
        return int(float(str(text).replace(",", ".")))  # v1.09
    except (TypeError, ValueError):  # v1.09
        return None  # v1.09


def check_param_value(meta, text):  # v1.09
    """Pruefung eines Parameterwerts wie Userform_Other.Check_Time_String und Check_Limit_to_MinMax des Programmgenerators.
    Zeit: Zahl in ms oder 'Zahl Einheit' (Min, Sek, sek, Sec, sec, Ms, ms) innerhalb Min und Max. Rueckgabe: Fehlertext oder None"""
    text = str(text).strip()  # v1.09
    if text == "":  # v1.09
        # return f"Der Parameter '{meta['name']}' darf nicht leer sein."  # v1.16 (entfallen)
        return tr("Der Parameter '{parameter}' darf nicht leer sein.", parameter=meta['name'])  # v1.16
    if meta["type"] != "Time":  # v1.09
        return None  # v1.09
    low, high = meta["min"], meta["max"]  # v1.09
    # hint = f"Der Parameter '{meta['name']}' ist ungültig.\nBitte eine Zeit zwischen {low} ms und {high} ms eingeben, zum Beispiel 30 Sek, 5 Min oder 500 ms."  # v1.16 (entfallen)
    hint = tr("Der Parameter '{parameter}' ist ungültig.\nBitte eine Zeit zwischen {low} ms und {high} ms eingeben, zum Beispiel 30 Sek, 5 Min oder 500 ms.", parameter=meta['name'], low=low, high=high)  # v1.16
    parts = text.split(" ")  # v1.09
    if len(parts) == 1 and _number(parts[0]) is not None:  # v1.09
        value = _number(parts[0])  # v1.09
    elif len(parts) == 2 and _number(parts[0]) is not None and parts[1] in TIME_UNITS:  # v1.09
        value = float(parts[0].replace(",", ".")) * TIME_UNITS[parts[1]]  # v1.09
    else:  # v1.09
        return hint  # v1.09
    if (low is not None and value < low) or (high is not None and value > high):  # v1.09
        return hint  # v1.09
    return None  # v1.09


class HeadlessUserFormOther:  # v1.09
    """Ersatz fuer UserForm_Other des Patterngenerators (Parameter eines Makros eingeben, M14_Select_GotoAct.Proc_General). Das Tk-Formular fehlt im
    Python-Port (der Aufruf endete mit einem Fehler). Die Parameter stehen in der Tabelle Par_Description; das Ergebnis steht in M14.Userform_Res."""

    def meta(self, name):  # v1.09
        sheet = X02.Sheets(M01.PAR_DESCRIPTION_SH)  # v1.09
        for r in range(2, sheet.get_LastUsedRow() + 1):  # v1.09
            if str(sheet.Cells(r, 1)).strip() == name:  # v1.09
                return {"name": name, "type": str(sheet.Cells(r, 3)).strip(), "min": _number(str(sheet.Cells(r, 4))), "max": _number(str(sheet.Cells(r, 5))),  # v1.09
                        "default": str(sheet.Cells(r, 6)).strip(), "label": str(sheet.Cells(r, 7)).strip() or name, "hint": str(sheet.Cells(r, 8)).strip()}  # v1.09
        return {"name": name, "type": "", "min": None, "max": None, "default": "", "label": name, "hint": ""}  # v1.09

    def Show_UserForm_Other(self, Par, Name, Description, *args, **kwargs):  # v1.09
        M14.Userform_Res = ""  # v1.09
        present = HeadlessPresenters.params  # v1.09
        if present is None:  # v1.09
            logger.info("Patterngenerator: Parameterdialog fuer %s: keine Anzeige verfuegbar", Name)  # v1.09
            return  # v1.09
        metas = [self.meta(p.strip()) for p in str(Par).split(",") if p.strip()]  # v1.09
        request = {"title": str(Name), "description": str(Description), "params": metas,  # v1.09
                   "validate": lambda values: [check_param_value(m, v) for m, v in zip(metas, values)]}  # v1.09
        values = present(request)  # v1.09
        if values is None:  # v1.09
            return  # v1.09
        M14.Userform_Res = str(Name) + "(" + ", ".join(str(v).strip() for v in values) + ")"  # v1.09


def image_size(path):  # v1.10
    """Breite und Hoehe eines PNG- oder JPEG-Bilds in Pixeln, gelesen aus dem Dateikopf (ohne Pillow, das die Installation nicht braucht)"""  # v1.10
    with open(path, "rb") as fh:  # v1.10
        head = fh.read(32)  # v1.10
        if head[:8] == b"\x89PNG\r\n\x1a\n":  # v1.10
            width, height = struct.unpack(">II", head[16:24])  # v1.10
            return int(width), int(height)  # v1.10
        if head[:2] == b"\xff\xd8":  # v1.10
            fh.seek(2)  # v1.10
            while True:  # v1.10
                marker = fh.read(2)  # v1.10
                if len(marker) < 2 or marker[0] != 0xFF:  # v1.10
                    break  # v1.10
                while marker[1] == 0xFF:                                              # Fuellbytes vor dem Markercode  # v1.10
                    marker = b"\xff" + fh.read(1)  # v1.10
                code = marker[1]  # v1.10
                if code in (0x01, 0xD8) or 0xD0 <= code <= 0xD7:                      # Marker ohne Laenge  # v1.10
                    continue  # v1.10
                length = struct.unpack(">H", fh.read(2))[0]  # v1.10
                if 0xC0 <= code <= 0xCF and code not in (0xC4, 0xC8, 0xCC):           # SOFn: Praezision, Hoehe, Breite  # v1.10
                    _, height, width = struct.unpack(">BHH", fh.read(5))  # v1.10
                    return int(width), int(height)  # v1.10
                fh.seek(length - 2, 1)  # v1.10
    raise ValueError("Die Bildgroesse konnte nicht gelesen werden (nur PNG und JPG)")  # v1.10


def led_address_dialog():  # v1.07
    """Ersatz fuer M60.Select_LED_Address_Dialog. Das Original sucht ein Modul am USB-Anschluss und laesst zur Kontrolle die gewaehlte LED blinken.
    Hier wird nur die Nummer eingegeben (das Blinken gibt es erst mit dem Senden an das Modul). Rueckgabe: Nummer oder -1 bei Abbruch"""
    present = HeadlessPresenters.number  # v1.07
    if present is None:  # v1.07
        return -1  # v1.07
    try:  # v1.07
        start = int(float(str(X02.RangeDict["RGB_Modul_Nr"].Value) or 0))  # v1.07
    except (TypeError, ValueError):  # v1.07
        start = 0  # v1.07
    result = present({"title": "RGB Modul Nr", "text": "Nummer der RGB LED am Modul (0 ist die erste LED).", "value": start, "minimum": 0, "maximum": 255})  # v1.07
    return -1 if result is None else int(result)  # v1.07


def init_userforms_headless(controller):
    """Ersatz fuer pattgen.D00_Forms.init_UserForms: keine Tk-Fenster, sondern Platzhalter (und die Statusanzeige ueber die Statuszeile)"""
    D00.StatusMsg_UserForm = HeadlessStatusForm(controller)
    for name in FORM_NAMES:
        setattr(D00, name, HeadlessForm(name))
    D00.Select_from_Sheet_Form = HeadlessSelectFromSheetForm()                 # Auswahlliste im Browser (HeadlessPresenters.select)  # v1.07
    M14.UserForm_Other = HeadlessUserFormOther()                               # Parameter der Goto Aktivierung (Counter, RandomTime ...)  # v1.09
    M60.Select_LED_Address_Dialog = led_address_dialog                         # Eingabe der LED Adresse im Browser (HeadlessPresenters.number)  # v1.07


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
        self.restore_all_pictures()  # v1.10
        self.restore_dynamic_rows()  # v1.12
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

    def ensure_grafik(self, ws):  # v1.07
        """Balken zeichnen, wenn das Blatt keine hat. Die Formen werden nicht gesichert (LoadWorkbook laedt PatternWorkbook ohne Formen): nach einem
        Neustart haben die wiederhergestellten Blaetter keine Balken, bis jemand Aktualisieren drueckt."""
        if any(str(getattr(s, "Type", "")) == "5" for s in (getattr(ws, "shapelist", None) or [])):  # v1.07
            return  # v1.07
        self.update_grafik(ws)  # v1.07

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

    # ------------------------------------------------------------------ Beispiele, Laden, Speichern, Loeschen (Optionen)
    def example_dir(self):  # v1.06
        return os.path.join(self.filedir2, M01.ExampleDir)  # v1.06

    def example_collections(self):  # v1.06
        """Beispielsammlungen, deren Datei vorhanden ist: Liste (Dateiname ohne .MLL_pcf, Anzeigename)"""  # v1.06
        return [(name, caption) for name, caption in EXAMPLE_COLLECTIONS if os.path.exists(os.path.join(self.example_dir(), name + ".MLL_pcf"))]  # v1.06

    def is_data_sheet(self, ws):  # v1.06
        """Datenblatt (Muster), also weder Main noch ein Hilfsblatt, und sichtbar"""  # v1.06
        try:  # v1.06
            visible = ws.Visible  # v1.06
        except Exception:                              # noqa: BLE001  # v1.06
            visible = True  # v1.06
        return visible is not False and ws.Name not in NON_DATA_SHEETS  # v1.06

    def data_sheets(self):  # v1.06
        return [ws for ws in self.workbook.sheets if self.is_data_sheet(ws)]  # v1.06

    def first_sheet(self):  # v1.06
        """Blatt, das nach dem Loeschen angezeigt wird: das erste Datenblatt, sonst Main"""  # v1.06
        sheets = self.data_sheets()  # v1.06
        return sheets[0] if sheets else self.find_sheet(M01.MAIN_SH)  # v1.06

    @staticmethod  # v1.06
    def file_encoding(path):  # v1.14
        """Zeichensatz einer Datei im Pattern-Format: UTF-8 (vom Web-Programm geschrieben) oder cp1252 (aus dem Excel-Programm, Trennzeichen Chr(175)); wie VBFiles.openFile"""  # v1.14
        try:  # v1.14
            from vb2py.vbclasses import VBFiles  # v1.14
            return VBFiles._encoding_for(path, "r")  # v1.14
        except Exception:                                                  # noqa: BLE001  aeltere vbclasses.py ohne _encoding_for  # v1.14
            return "utf-8"  # v1.14

    @staticmethod  # v1.14
    def sheet_names_in_file(path):  # v1.06
        """Namen der Blaetter in einer Datei im Pattern-Format (Zeilen SheetName)"""  # v1.06
        names = []  # v1.06
        # with open(path, encoding="utf-8", errors="replace") as fh:  # v1.14 (entfallen)
        with open(path, encoding=HeadlessPatternGeneratorPage.file_encoding(path), errors="replace") as fh:  # v1.14
            for line in fh:  # v1.06
                tokens = line.rstrip("\r\n").replace("\t", chr(M01.pcfSep)).split(chr(M01.pcfSep))  # v1.06
                if tokens[0] == "SheetName" and len(tokens) > 1:  # v1.06
                    names.append(tokens[1])  # v1.06
        return names  # v1.06

    @staticmethod  # v1.06
    def object_lines_in_file(path):  # v1.06
        """Zeilen der Textfelder (msoTextBox*) und Formularknoepfe (msoFormControl*) je Blatt (jeweils das erste Blatt dieses Namens in der Datei),
        mit den Folgezeilen mehrzeiliger Texte. Die Web-Oberflaeche legt diese Objekte nicht an: Die Zeilen werden beim Laden gemerkt und beim
        Speichern wieder geschrieben, damit die Datei fuer die Excel-Version vollstaendig bleibt."""
        sep = chr(M01.pcfSep)  # v1.06
        result, seen, current, sheet = {}, set(), None, None  # v1.06
        # with open(path, encoding="utf-8", errors="replace") as fh:  # v1.14 (entfallen)
        with open(path, encoding=HeadlessPatternGeneratorPage.file_encoding(path), errors="replace") as fh:  # v1.14
            for line in fh:  # v1.06
                line = line.rstrip("\r\n")  # v1.06
                tokens = line.replace("\t", sep).split(sep)  # v1.06
                if tokens[0] == "SheetName" and len(tokens) > 1:  # v1.06
                    sheet = tokens[1] if tokens[1] not in seen else None  # v1.06
                    seen.add(tokens[1])  # v1.06
                    current = None  # v1.06
                    if sheet is not None:  # v1.06
                        result[sheet] = []  # v1.06
                elif sheet is None:  # v1.06
                    continue  # v1.06
                elif tokens[0].startswith(("msoTextBox", "msoFormControl")):  # v1.06
                    current = result[sheet]  # v1.06
                    current.append(line)  # v1.06
                elif len(tokens) == 1 and current is not None:                         # Folgezeile eines mehrzeiligen Textes  # v1.06
                    current.append(line)  # v1.06
                else:  # v1.06
                    current = None  # v1.06
        for lines in result.values():  # v1.06
            while lines and lines[-1].strip() == "":  # v1.06
                lines.pop()  # v1.06
        return {name: lines for name, lines in result.items() if lines}  # v1.06

    def load_files(self, paths):  # v1.06
        """Dateien im Pattern-Format (.MLL_pcf) nacheinander laden (wie Load_AllExamples_Sheets / Load_Sheets des Originals). Ein Blatt, das es
        schon gibt (oder das eine vorher geladene Datei mitbrachte), wird uebersprungen, damit keine Kopien mit _Copy_ im Namen entstehen.
        Rueckgabe: (Namen der neuen Blaetter, Namen der uebersprungenen)"""
        added, skipped = [], []  # v1.06
        with self.activated():  # v1.06
            loaded = "".join(ws.Name + "\t" for ws in self.workbook.sheets)          # Load_Sheets ueberspringt Namen aus Loaded_Sheets  # v1.06
            for path in paths:  # v1.06
                names = self.sheet_names_in_file(path)  # v1.06
                objects = self.object_lines_in_file(path)  # v1.06
                skipped += [n for n in names if ("\t" + loaded).find("\t" + n + "\t") >= 0]  # v1.06
                before = {ws.Name for ws in self.workbook.sheets}  # v1.06
                M08.Load_Sheets(path, loaded, "<<LASTSHEET>>")  # v1.06
                new_names = [ws.Name for ws in self.workbook.sheets if ws.Name not in before]  # v1.06
                added += new_names  # v1.06
                for name in new_names:                                                 # Textfelder und Formularknoepfe merken (werden mit dem Blatt gesichert)  # v1.06
                    if name in objects:  # v1.06
                        ws = self.find_sheet(name)  # v1.06
                        if getattr(ws, "persistent_controls_dict", None) is None:  # v1.06
                            ws.persistent_controls_dict = {}  # v1.06
                        ws.persistent_controls_dict["pcf_objects"] = objects[name]  # v1.06
                        ws.tksheet.persistent_controls_dict = ws.persistent_controls_dict     # das Sichern der Arbeitsmappe liest das Woerterbuch des tksheet  # v1.06
                loaded += "".join(n + "\t" for n in names)  # v1.06
            self.attach_controls()  # v1.06
            for name in added:                                                         # die Balken (Freiformen) werden nicht gesichert  # v1.06
                ws = self.find_sheet(name)  # v1.06
                try:  # v1.06
                    ws.Activate()  # v1.06
                    M03.Update_Grafik()  # v1.06
                except Exception:                                                      # noqa: BLE001  # v1.06
                    logger.exception("Grafik des Blatts %s nicht aufgebaut", name)  # v1.06
                self.sync_pictures(ws)  # v1.10
        return added, skipped  # v1.06

    def load_examples(self, names):  # v1.06
        """Beispielsammlungen (Namen wie in example_collections) laden"""  # v1.06
        return self.load_files([os.path.join(self.example_dir(), name + ".MLL_pcf") for name in names])  # v1.06

    def load_upload(self, path):  # v1.06
        """Hochgeladene Datei laden: .MLL_pcf oder .zip (mit der Datei und den Bildern dazu). Rueckgabe wie load_files"""  # v1.06
        if not path.lower().endswith(".zip"):  # v1.06
            return self.load_files([path])  # v1.06
        folder = tempfile.mkdtemp(prefix="mll_pcf_up_")  # v1.06
        with zipfile.ZipFile(path) as zf:  # v1.06
            for info in zf.infolist():  # v1.06
                name = os.path.basename(info.filename)                                 # nur Dateinamen: keine Pfade aus der ZIP-Datei uebernehmen  # v1.06
                if info.is_dir() or not name:  # v1.06
                    continue  # v1.06
                with zf.open(info) as src, open(os.path.join(folder, name), "wb") as dst:  # v1.06
                    shutil.copyfileobj(src, dst)  # v1.06
        files = sorted(f for f in os.listdir(folder) if f.lower().endswith(".mll_pcf"))  # v1.06
        if not files:  # v1.06
            raise ValueError("Die ZIP-Datei enthaelt keine .MLL_pcf-Datei")  # v1.06
        return self.load_files([os.path.join(folder, f) for f in files])  # v1.06

    def save_for_download(self, ws=None):  # v1.06
        """Das Blatt ws (oder alle Datenblaetter) in eine Datei im Pattern-Format schreiben (M07.Save_One_Sheet). Die Bilder der Blaetter kopiert die
        Speicherfunktion neben die Datei; gibt es welche, wird alles in eine ZIP-Datei gepackt. Rueckgabe: (Pfad, Name zum Speichern)"""
        folder = tempfile.mkdtemp(prefix="mll_pcf_")  # v1.06
        base = ws.Name if ws is not None else "AllExamples"  # v1.06
        base = re.sub(r'[\\/:*?"<>|]', "_", base)  # v1.06
        pcf = os.path.join(folder, base + ".MLL_pcf")  # v1.06
        sheets = [ws] if ws is not None else self.data_sheets()  # v1.06
        if not sheets:  # v1.06
            raise ValueError("Es gibt kein Datenblatt zum Speichern")  # v1.06
        with self.activated():  # v1.06
            for i, sh in enumerate(sheets):  # v1.06
                sh.Activate()  # v1.06
                sh.Select()  # v1.06
                M07.Save_One_Sheet(sh, pcf, i > 0)  # v1.06
                lines = (getattr(sh, "persistent_controls_dict", None) or {}).get("pcf_objects") or []  # v1.06
                if lines:                                                              # die beim Laden gemerkten Textfelder und Formularknoepfe  # v1.06
                    with open(pcf, "a", encoding="utf-8") as fh:  # v1.06
                        fh.write("\n".join(lines) + "\n")  # v1.06
        if str(self.controller.getConfigData("SaveExcelCharset")).strip().lower() in ("1", "true", "ja", "yes", "an", "ein", "on"):   # Programm Einstellungen: fuer das Excel-Programm  # v1.15
            try:  # v1.15
                from vb2py.vbclasses import VBFiles  # v1.15
                logger.info("Datei %s: %s", os.path.basename(pcf), VBFiles.to_excel_charset(pcf))  # v1.15
            except Exception:                                                  # noqa: BLE001  # v1.15
                logger.exception("Umschreiben in den Windows-Zeichensatz fehlgeschlagen")  # v1.15
        extras = [f for f in sorted(os.listdir(folder)) if f != base + ".MLL_pcf"]  # v1.06
        if not extras:  # v1.06
            return pcf, base + ".MLL_pcf"  # v1.06
        zip_path = os.path.join(tempfile.mkdtemp(prefix="mll_pcf_zip_"), base + ".zip")  # v1.06
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:  # v1.06
            for f in [base + ".MLL_pcf"] + extras:  # v1.06
                zf.write(os.path.join(folder, f), f)  # v1.06
        return zip_path, base + ".zip"  # v1.06

    def delete_sheet(self, ws):  # v1.06
        """Datenblatt loeschen; False bei Main und den Hilfsblaettern"""  # v1.06
        if not self.is_data_sheet(ws):  # v1.06
            return False  # v1.06
        with self.activated():  # v1.06
            X02.Application.DisplayAlerts = False  # v1.06
            try:  # v1.06
                X02.Sheets(ws.Name).Delete()  # v1.06
            finally:  # v1.06
                X02.Application.DisplayAlerts = True  # v1.06
        return True  # v1.06

    def delete_all_data_sheets(self):  # v1.06
        """Alle Datenblaetter loeschen (wie Del_All_Sheets_Excep_Main, ohne Rueckfrage). Rueckgabe: Zahl der geloeschten Blaetter"""  # v1.06
        count = 0  # v1.06
        for ws in self.data_sheets():                  # eine Liste: waehrend des Loeschens aendert sich die Arbeitsmappe  # v1.06
            if self.delete_sheet(ws):  # v1.06
                count += 1  # v1.06
        return count  # v1.06

    # ------------------------------------------------------------------ Doppelklick auf Zellen mit Dialog
    def dialog_cells(self, ws):  # v1.07
        """Zellen des Blatts, auf die ein Doppelklick einen Dialog oeffnet (wie M02_Main.Proc_DoubleClick): {(Zeile, Spalte): Art}"""  # v1.07
        cells = {}  # v1.07
        if ws.Name in NON_DATA_SHEETS and ws.Name != M01.MAIN_SH:                      # Main ist in der Web-Oberflaeche ein Arbeitsblatt wie die anderen (Is_Data_Sheet des Originals fragt nur nach RGB_Modul_Nr)  # v1.08
            return cells  # v1.07
        with self.activated():  # v1.07
            self.use(ws)  # v1.07
            for kind, name in DOUBLECLICK_CELLS:  # v1.07
                try:  # v1.07
                    address = X02.Range(name).Address  # v1.07
                    cells[(int(address[0]), int(address[1]))] = kind  # v1.07
                except Exception:                                                   # noqa: BLE001  # v1.07
                    logger.debug("Benannter Bereich %s im Blatt %s nicht gefunden", name, ws.Name)  # v1.07
        return cells  # v1.07

    def run_cell_dialog(self, ws, row, col):  # v1.07
        """Dialog der Zelle (row, col) zeigen und das Ergebnis eintragen. Rueckgabe: Art des Dialogs oder None, wenn die Zelle keinen hat"""  # v1.07
        kind = self.dialog_cells(ws).get((row, col))  # v1.07
        if kind is None:  # v1.07
            return None  # v1.07
        with self.activated():  # v1.07
            self.use(ws)  # v1.07
            if kind == "special_mode":  # v1.07
                M60.Select_Special_Mode()  # v1.07
            elif kind == "rgb_modul_nr":  # v1.07
                M60.Get_LED_Address_Dialog()  # v1.07
            elif kind == "goto_act":  # v1.09
                M14.Select_GotoAct()  # v1.09
        return kind  # v1.07

    # ------------------------------------------------------------------ Bilder (bleiben, wo sie sind: nur Pfad und Lage werden mit dem Blatt gesichert)
    def picture_dir(self):  # v1.10
        """Ordner fuer Bilder, die der Anwender einfuegt (hochgeladene Dateien sind nur Zwischendateien)"""  # v1.10
        folder = os.path.join(self.controller.data_dir, "pattern_pictures")  # v1.10
        os.makedirs(folder, exist_ok=True)  # v1.10
        return folder  # v1.10

    @staticmethod  # v1.10
    def pictures_of(ws):  # v1.10
        return [s for s in (getattr(ws, "shapelist", None) or []) if str(getattr(s, "Type", "")) == "13"]  # v1.10

    def sync_pictures(self, ws):  # v1.10
        """Die Bilder des Blatts (Pfad, Lage, Groesse) in persistent_controls_dict merken, damit sie mit der Arbeitsmappe gesichert werden. Die Formen selbst
        werden nicht gesichert (LoadWorkbook mit copyshapes=False): nach einem Neustart legt restore_pictures sie wieder an."""
        entries = []  # v1.10
        for shape in self.pictures_of(ws):  # v1.10
            try:  # v1.10
                entries.append({"path": str(shape.Name), "left": float(shape.Left), "top": float(shape.Top), "width": float(shape.Width), "height": float(shape.Height)})  # v1.10
            except (TypeError, ValueError):  # v1.10
                continue  # v1.10
        if getattr(ws, "persistent_controls_dict", None) is None:  # v1.10
            ws.persistent_controls_dict = {}  # v1.10
        if ws.persistent_controls_dict.get("pcf_pictures") != entries:  # v1.10
            ws.persistent_controls_dict["pcf_pictures"] = entries  # v1.10
        ws.tksheet.persistent_controls_dict = ws.persistent_controls_dict        # das Sichern der Arbeitsmappe liest das Woerterbuch des tksheet  # v1.10

    def restore_pictures(self, ws):  # v1.10
        """Bilder nach dem Neustart wieder anlegen (sofern die Datei noch da ist)"""  # v1.10
        entries = (getattr(ws, "persistent_controls_dict", None) or {}).get("pcf_pictures") or []  # v1.10
        have = {str(shape.Name) for shape in self.pictures_of(ws)}  # v1.10
        for entry in entries:  # v1.10
            path = entry.get("path")  # v1.10
            if not path or path in have:  # v1.10
                continue  # v1.10
            if not os.path.exists(path):  # v1.10
                logger.info("Bild %s fehlt (Blatt %s): nicht wiederhergestellt", path, ws.Name)  # v1.10
                continue  # v1.10
            ws.addPicture(path, entry["left"], entry["top"], entry["width"], entry["height"])  # v1.10
            have.add(path)  # v1.10

    def restore_dynamic_rows(self):  # v1.12
        """Nach dem Neustart die Goto-Zeilen und die Zeilen des Spezial Modes neu bestimmen (wie Set_Defaults_for_Sheet nach dem Laden einer Datei): Das Blatt legt die versteckten Zeilen
        der Vorlage an, dazu gehoert die Goto-Zeile 47. Sicherungen ohne gemerkte versteckte Zeilen (aeltere Fassungen) kennen den Zustand nicht. Wer ihn schon hat, aendert sich nicht."""
        for ws in self.workbook.sheets:  # v1.12
            if ws.Name in NON_DATA_SHEETS and ws.Name != M01.MAIN_SH:  # v1.12
                continue  # v1.12
            try:  # v1.12
                with self.activated():  # v1.12
                    self.use(ws)  # v1.12
                    M02A.Hide_Show_Check_Goto_Activation()                       # Zeile Goto Aktivierung (die Vorlage versteckt sie)  # v1.13
                    M06G.Hide_Show_GotoLines_If_Enabled()  # v1.12
                    M06G.Hide_Show_Special_ModeLines_If_Enabled()  # v1.12
            except Exception:                                                    # noqa: BLE001  # v1.12
                logger.exception("Zeilen des Blatts %s nicht bestimmt", ws.Name)  # v1.12

    def restore_all_pictures(self):  # v1.10
        for ws in self.workbook.sheets:  # v1.10
            try:  # v1.10
                self.restore_pictures(ws)  # v1.10
            except Exception:                                                    # noqa: BLE001  # v1.10
                logger.exception("Bilder des Blatts %s nicht wiederhergestellt", ws.Name)  # v1.10

    def insert_picture(self, ws, source):  # v1.10
        """Ein Bild (PNG oder JPG) unter der Tabelle einfuegen (wie M80.Load_New_Picture: an der Zelle B63, natuerliche Groesse). Die hochgeladene Datei ist
        nur eine Zwischendatei und wird in den Bilderordner kopiert. Rueckgabe: Dateiname"""
        extension = os.path.splitext(source)[1].lower()  # v1.10
        if extension not in (".png", ".jpg", ".jpeg"):  # v1.10
            raise ValueError("Nur PNG- und JPG-Bilder koennen eingefuegt werden")  # v1.10
        width, height = image_size(source)  # v1.10
        name = os.path.basename(source)  # v1.10
        dest = os.path.join(self.picture_dir(), name)  # v1.10
        if os.path.exists(dest):  # v1.10
            with open(dest, "rb") as a, open(source, "rb") as b:  # v1.10
                same = a.read() == b.read()  # v1.10
            if not same:                                                         # gleicher Name, anderes Bild: nicht ueberschreiben  # v1.10
                stem, ext = os.path.splitext(name)  # v1.10
                number = 2  # v1.10
                while os.path.exists(os.path.join(self.picture_dir(), f"{stem}_{number}{ext}")):  # v1.10
                    number += 1  # v1.10
                dest = os.path.join(self.picture_dir(), f"{stem}_{number}{ext}")  # v1.10
        if not os.path.exists(dest):  # v1.10
            shutil.copy2(source, dest)  # v1.10
        with self.activated():  # v1.10
            ws.Activate()  # v1.10
            cell = X02.Cells(63, 2)  # v1.10
            factor = float(X02.guifactor) * 0.75                                 # Pixel in Punkte, dann der Faktor der Oberflaeche (so legt Load_Picture sie an)  # v1.10
            ws.addPicture(dest, float(cell.Left), float(cell.Top), width * factor, height * factor)  # v1.10
        self.sync_pictures(ws)  # v1.10
        return os.path.basename(dest)  # v1.10

    def remove_pictures(self, ws):  # v1.10
        """Alle Bilder des Blatts entfernen. Rueckgabe: Zahl der Bilder"""  # v1.10
        shapes = self.pictures_of(ws)  # v1.10
        for shape in list(shapes):  # v1.10
            ws.shapelist.remove(shape)  # v1.10
        self.sync_pictures(ws)  # v1.10
        return len(shapes)  # v1.10

    def led_row_count(self, ws):  # v1.11
        """Zahl der LED-Zeilen der Tabelle (benannter Bereich LED_Cnt_Rng, E5). In Spalte D stehen die Nummern 1 bis 20 immer, die Tabelle hat aber nur so viele Zeilen."""  # v1.11
        with self.activated():  # v1.11
            self.use(ws)  # v1.11
            try:  # v1.11
                return max(1, int(float(str(X02.Range(M01.LED_Cnt_Rng).Value))))  # v1.11
            except (TypeError, ValueError):  # v1.11
                return 1  # v1.11

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
