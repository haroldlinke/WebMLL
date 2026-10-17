# Datei-Version: 1.08 (2026-10-17) - headless_proggen.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_proggen.py
# Path:           headless/headless_proggen.py
# Version:        1.08
# Last Update:    2026-10-17
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.08  2026-10-17  Web-Formulare Select_ProgGen_Dest_Form und Select_ProgGen_Src_Form (Export/Import des Patterngenerators) installieren; davor bis 1.07 (2026-10-15), nicht erfasst
# ----------------------------------------------------------------------------------------------
"""Tk-freier Ersatz fuer Prog_GeneratorPage: baut die Arbeitsmappe "ProgGenerator".

Entspricht dem Teil von Prog_GeneratorPage.__init__, der das Workbook anlegt (ohne Frames,
Buttonleiste und Infolabel). Das workbook_dict kommt aus Prog_Generator.build_workbook_dict
(gemeinsame Quelle mit der Tk-Seite). Voraussetzung: MLL_HEADLESS=1 und die Headless-Variante
von ExcelAPI/XLA_Application.py.

Nicht enthalten: create_button_list (Toolbar), Statusleiste, Upload/Compile-Methoden der Seite.
Fehlende Attribute der Seite zeigen sich als AttributeError, sobald andere Module sie ueber
ThisWorkbook.macro_caller benutzen.
"""
from __future__ import annotations

import logging
import os

import userdata                               # Datenordner ausserhalb des Projektordners

import mlpyproggen.Prog_Generator as PG        # importiert tkinter, instanziiert aber keine GUI
import proggen.F00_mainbuttons as F00

logger = logging.getLogger(__name__)


class HeadlessStatusForm:
    """Ersatz fuer proggen.StatusMsg_Userform.StatusMsg_UserForm (Tk-Toplevel mit Statusanzeige).

    ShowDialog(...) und set-/update-artige Aufrufe leiten Texte an controller.set_statusmessage.
    Alle anderen Aufrufe werden nur protokolliert (INFO), damit sichtbar wird, welche Methoden
    der Originaldialog hat und benutzt wird."""

    def __init__(self, controller):
        self._c = controller
        self._main = ""                 # Haupttext ("Programmiere PICO ...")

    def ShowDialog(self, *args, **kwargs):
        text = " ".join(a for a in args if isinstance(a, str) and a)
        logger.info("StatusMsg.ShowDialog%r", args)
        if text:
            self._main = " ".join(text.split())
            self._c.set_statusmessage(self._main)

    def Set_ActSheet_Label(self, text="", *args, **kwargs):
        """Die Laufzeit-Anzeige ersetzt den Haupttext nicht mehr, sondern wird angehaengt."""
        main = self._main
        self._c.set_statusmessage(f"{main}  [{text}]" if main else str(text))

    def destroy(self, *args, **kwargs):
        self._main = ""

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)

        def _call(*args, **kwargs):
            logger.info("StatusMsg.%s%r", name, args)
            texts = [a for a in args if isinstance(a, str) and a]
            if texts and name.lower().startswith(("set", "update", "show", "text")):
                self._c.set_statusmessage(" ".join(texts))
            return None
        return _call


class HeadlessProgGeneratorPage:
    def __init__(self, controller):
        self.controller = controller
        self.Application = controller.ExcelApplication
        PG.set_global_controller(controller)
        PG.dialog_parent = None                       # Tk-Elternfenster fuer Dialoge gibt es nicht
        self.tabClassName = "ProgGeneratorPage"
        controller.set_statusmessage("Erstelle ProgramGenerator Seite ...", fg="green")

        self.default_font = controller.defaultfontnormal
        self.default_boldfont = (self.default_font[0], self.default_font[1], "bold")
        self.default_smallfont = controller.defaultfontsmall

        macrodata = controller.MacroDef.data.get(self.tabClassName, {})
        self.tabname = PG._T(macrodata.get("MTabName", self.tabClassName))
        self.title = PG._T(macrodata.get("Title", self.tabClassName))
        self.Start_Compile_Time = 0
        self.RowFormat_data = {}

        # Ordner wie im Original: filedir = mlpyproggen, filedir2 = Projektordner
        filedir = os.path.dirname(os.path.realpath(PG.__file__))
        filedir2 = os.path.dirname(filedir)
        filedir3 = os.path.dirname(filedir2)
        filedir4 = os.path.dirname(filedir3)
        self.filedir5 = os.path.dirname(filedir4)

        self.workbookname = "ProgGenerator"
        self.tempworkbookFilname = controller.tempworkbookFilname
        # Die Sicherung der Tabellen liegt flach im Datenordner (nicht im Projektordner filedir2), damit sie ein Update ueberlebt. Der Name
        # aus DefaultConstants enthaelt "../". Einmalig wird eine Datei der Versionen 1.17 bis 1.22 uebernommen, die irrtuemlich ausserhalb
        # des Datenordners lag (Datenordner plus "../"). Dateien der Tk-Version werden nicht uebernommen.
        rel_name = self.tempworkbookFilname + "_" + self.workbookname + ".json"
        temp_workbook_filename = os.path.join(controller.data_dir, userdata.flat(rel_name))
        userdata.copy_if_missing(os.path.normpath(os.path.join(controller.data_dir, rel_name)), temp_workbook_filename)

        workbook_dict = PG.build_workbook_dict(self.default_font, self.default_smallfont, self.default_boldfont)
        PG.IPUploadTimeout = controller.IPUploadTimeout

        # Die Tk-Formulare werden von F00.workbook_init -> init_UserForms() angelegt. Nach dem
        # Anlegen ersetzen wir die Dialoge, die im Headless-Betrieb nicht als Tk-Fenster
        # erscheinen duerfen (derzeit: Statusdialog).
        _orig_init_userforms = F00.init_UserForms

        def _init_userforms_headless():
            _orig_init_userforms()
            F00.StatusMsg_UserForm = HeadlessStatusForm(controller)
            try:
                from _web import web_dialogs
                web_dialogs.install_forms(F00)     # Web-Versionen der Formulare des gefuehrten Dialogs
                from _web import web_form_exchange  # v1.08  # v1.08
                web_form_exchange.install_forms(F00, controller)  # v1.08  Zeilenauswahl fuer Export/Import des Patterngenerators  # v1.08
            except Exception:                       # noqa: BLE001
                logger.exception("Web-Formulare konnten nicht installiert werden")
        F00.init_UserForms = _init_userforms_headless

        self.workbook = self.Application.Workbooks.Open(
            ParentFrame=None,                          # kein Tk-Frame: Headless-Betrieb
            FileName=temp_workbook_filename,
            path=filedir2,
            pyProgPath=filedir2,
            workbookName=self.workbookname,
            macro_caller=self,
            InitWorkBookFunction=F00.workbook_init,
            workbookdict=workbook_dict,
            start_sheet=PG.start_sheet,
            controller=controller)

        for sheet in self.workbook.sheets:
            sheet.SetChangedCallback(PG.wschangedcallback)
            sheet.SetSelectedCallback(PG.wsselectedcallback)
            sheet.SetCalculationCallback(PG.wscalculationcallback)
            sheet.SetInitDataFunction(F00.worksheet_init)

        self.workbook.SetInitWorkbookFunction(F00.workbook_init)
        PG.ThisWorkbook = self.workbook
        PG.dialog_parent = self                          # M08/M06 rufen die Methoden der Seite ueber dialog_parent auf
        self.workbook.activate_sheet(PG.start_sheet)

    # Workbooks.Open setzt macro_caller.ThisWorkbook; wie im Original auf das Modul-Global abbilden
    def get_ThisWorkbook(self):
        return PG.ThisWorkbook

    def set_ThisWorkbook(self, value):
        PG.ThisWorkbook = value

    ThisWorkbook = property(fget=get_ThisWorkbook, fset=set_ThisWorkbook)


# ----------------------------------------------------------------------------------------------
# Methoden der Tk-Seite (Prog_GeneratorPage), die nur auf self.controller und dem Textfenster arbeiten
# (Kompilieren/Hochladen, Statuszeile, Konfigurationszugriff). Sie werden unveraendert uebernommen, damit
# es eine einzige Quelle gibt; das Textfenster liefert controller.getFramebyName("ARDUINOMonitorPage").
_BORROWED = ("getConfigData", "readConfigData", "setConfigData", "setParamData", "get_param_config_dict",
             "Update_Compile_Time", "Stop_Compile_Time_Display", "ClearStatusbar", "Show_Status_for_a_while",
             "RowFormat_Button_click", "upload_to_ARDUINO_Button_click", "upload_to_ARDUINO_end",
             "start_ARDUINO_program_cmd", "terminate_process", "execute_shell_cmd", "start_ARDUINO_program_Run",
             "start_ARDUINO_program_Popen", "write_stdout_to_text_window", "upload_to_ARDUINO", "EndProg",
             "checkcolor")                       # checkcolor: M60.Open_MobaLedCheckColors -> Farbtest mit Farbtabelle oeffnen
for _name in _BORROWED:
    _fn = PG.Prog_GeneratorPage.__dict__.get(_name)
    if _fn is None:
        logger.warning("Methode %s in Prog_GeneratorPage nicht gefunden", _name)
    else:
        setattr(HeadlessProgGeneratorPage, _name, _fn)


def _update(self):
    pass


def _after(self, ms, func=None, *args):
    return self.controller.after(ms, func, *args)


HeadlessProgGeneratorPage.update = _update
HeadlessProgGeneratorPage.after = _after


# ------------------------------------------------------------------------------------------------ ARDUINO IDE 1.8: Einstellungen
from arduino_prefs import sanitize_arduino_prefs, ensure_arduino_prefs      # noqa: E402,F401  (siehe arduino_prefs.py)

_orig_execute_shell_cmd = HeadlessProgGeneratorPage.execute_shell_cmd


def _execute_shell_cmd(self, cmd_str, message1, empty_text=True):
    installing = "--install-" in str(cmd_str)                       # Bibliotheken und Boards installieren
    weblog = getattr(self.controller, "weblog", None)
    if weblog is not None:
        from _web import web_log
        weblog.set_title(web_log.INSTALL_TITLE if installing else web_log.DEFAULT_TITLE)
    if installing:
        sanitize_arduino_prefs()
    return _orig_execute_shell_cmd(self, cmd_str, message1, empty_text)


HeadlessProgGeneratorPage.execute_shell_cmd = _execute_shell_cmd
