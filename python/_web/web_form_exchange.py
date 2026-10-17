# Datei-Version: 1.00 (2026-10-17) - web_form_exchange.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_exchange.py
# Path:           _web/web_form_exchange.py
# Version:        1.00
# Last Update:    2026-10-17
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-17  Neu: Zeilenauswahl fuer Export zu ProgGen und Import von ProgGen als Hinweisband im Reiter Programm Generator
# ----------------------------------------------------------------------------------------------
"""Web-Ersatz fuer proggen/Select_ProgGen_Dest_Form.py und Select_ProgGen_Src_Form.py.

Der Patterngenerator traegt sein Makro in eine Zeile des Programm Generators ein (Export) oder liest ein Makro aus einer Zeile (Import).
Dazu zeigte die Tk-Version ein Fenster, in dem man die Zeile anklickt und mit OK bestaetigt. Hier erscheint stattdessen ein Hinweisband
ueber der Tabelle des Programm Generators (ExchangeBanner).

WebSelectDestForm und WebSelectSrcForm erben von den Originalklassen: Die Pruefungen und die Rueckrufe (Copy_Pattern_Macro_Callback,
Import_From_Prog_Gen_Callback) bleiben unveraendert, ersetzt werden nur Show und Hide. Die Rueckrufe aktivieren das Arbeitsbuch des
Patterngenerators (PG.ThisWorkbook.Activate()); nach OK und Abbrechen wird deshalb der Programm Generator wieder zum aktiven Arbeitsbuch gemacht.
Die Beschriftungen werden aus dem Quelltext der Originale gelesen.
"""
from __future__ import annotations

import asyncio
import inspect
import json
import logging
import re

from nicegui import ui

import ExcelAPI.XLA_Application as X02
import proggen.Select_ProgGen_Dest_Form as D13
import proggen.Select_ProgGen_Src_Form as D12

logger = logging.getLogger(__name__)


class _Check:
    """Ersatz fuer ein Haeckchen des Tk-Formulars (die Originale lesen die Eigenschaft Value)"""
    def __init__(self, value=False):
        self.Value = value


class _WebFormMixin:
    kind = ""

    def Show(self):
        """Statt des Tk-Fensters das Hinweisband im Browser zeigen (der Browser wechselt zum Programm Generator)"""
        self.IsActive = True
        hook = getattr(self.controller, "web_select_row", None)
        if hook is None:                                # keine Oberflaeche: wie Abbrechen
            logger.warning("Zeilenauswahl: kein Browser verbunden, abgebrochen")
            self.IsActive = False
            if self.Callback_Proc:
                self.Callback_Proc(*self._abort_args())
            return
        hook(self)

    def Hide(self):
        self.IsActive = False
        hook = getattr(self.controller, "web_select_row_done", None)
        if hook is not None:
            hook(self)


class WebSelectDestForm(_WebFormMixin, D13.CSelect_ProgGen_Dest_Form):
    kind = "dest"

    def __init__(self, controller):
        D13.CSelect_ProgGen_Dest_Form.__init__(self, controller)
        self.SendToArduino_CheckBox = _Check(False)
        self.GoBack_CheckBox = _Check(True)

    def _abort_args(self):
        return (False, False, False)


class WebSelectSrcForm(_WebFormMixin, D12.CSelect_ProgGen_Src_Form):
    kind = "src"

    def _abort_args(self):
        return (False, "", "", 0)


def install_forms(F00, controller):
    """Ersetzt die Tk-Formulare in proggen.F00_mainbuttons (wird nach F00.init_UserForms() aufgerufen)"""
    if not isinstance(getattr(F00, "Select_ProgGen_Dest_Form", None), WebSelectDestForm):
        F00.Select_ProgGen_Dest_Form = WebSelectDestForm(controller)
    if not isinstance(getattr(F00, "Select_ProgGen_Src_Form", None), WebSelectSrcForm):
        F00.Select_ProgGen_Src_Form = WebSelectSrcForm(controller)
    logger.info("Web-Formulare installiert (Select_ProgGen_Dest_Form, Select_ProgGen_Src_Form)")


def _captions(cls) -> dict:
    """Beschriftungen der Komponenten aus dem Quelltext des Originals: Name -> Caption"""
    out = {}
    try:
        src = inspect.getsource(cls)
    except (OSError, TypeError):
        return out
    for name, cap in re.findall(r'"Name":"(\w+)"[^}]*?"Caption":"((?:[^"\\]|\\.)*)"', src):
        try:
            out[name] = json.loads('"' + cap + '"')
        except ValueError:
            out[name] = cap
    return out


def _clean(text: str) -> str:
    """Namen der Web-Oberflaeche einsetzen; der Hinweis auf die Enter-Taste (Tk-Dialog) entfaellt"""
    lines = [l for l in text.split("\n") if "'Enter'" not in l]
    text = "\n".join(lines).strip()
    return text.replace("Prog_Generator", "Programm Generator").replace("Pattern_Configurator", "Patterngenerator")


class ExchangeBanner:
    """Hinweisband ueber der Tabelle des Programm Generators; erscheint, wenn der Patterngenerator eine Zeile braucht"""

    def __init__(self, ctrl, show_tab, run_in_worker, refresh_pg, get_workbook):
        self.show_tab = show_tab                         # (name) -> Reiter umschalten ("pg" oder "patt")
        self.run_in_worker = run_in_worker               # (fn) -> Coroutine: fn im Worker-Thread, Dialoge im Browser
        self.refresh_pg = refresh_pg                     # () -> Tabelle des Programm Generators neu zeigen
        self.get_workbook = get_workbook                 # () -> Arbeitsbuch des Programm Generators
        self.form = None
        loop = asyncio.get_running_loop()
        with ui.card().classes("w-full").style("background: #fff8e1; border: 2px solid #f9a825; padding: 8px 14px; gap: 6px") as self.card:
            self.title = ui.label("").style("color: #c62828; font-weight: 600")
            self.text = ui.label("").style("white-space: pre-line")
            with ui.row().classes("items-center gap-4"):
                self.chk_arduino = ui.checkbox("gleich zum Arduino schicken")
                self.chk_back = ui.checkbox("Anschließend zurück zum Patterngenerator", value=True)
                ui.button("OK", on_click=self.on_ok).props("dense no-caps color=primary").classes("px-4")
                ui.button("Abbrechen", on_click=self.on_abort).props("dense no-caps outline").classes("px-2")
        self.card.set_visibility(False)
        # Die Formulare werden im Worker-Thread aufgerufen: in den Browser uebertragen
        ctrl.web_select_row = lambda form: loop.call_soon_threadsafe(self.show_form, form)
        ctrl.web_select_row_done = lambda form: loop.call_soon_threadsafe(self.hide_form, form)

    def show_form(self, form):
        dest = form.kind == "dest"
        caps = _captions(D13.CSelect_ProgGen_Dest_Form if dest else D12.CSelect_ProgGen_Src_Form)
        self.title.set_text(_clean(caps.get("Label2" if dest else "Head_Label", "Zeile im Programm Generator auswählen.")))
        self.text.set_text(_clean(caps.get("Label1" if dest else "Text_Label", "Klicken Sie in die Zeile und betätigen dann den 'OK' Knopf.")))
        self.chk_arduino.set_visibility(dest)
        self.chk_back.set_visibility(dest)
        self.chk_arduino.value = False
        self.chk_back.value = True
        self.form = form
        self.card.set_visibility(True)
        self.show_tab("pg")

    def hide_form(self, form):
        if self.form is form:
            self.form = None
            self.card.set_visibility(False)

    def _restore(self, prev_this):
        """Die Rueckrufe aktivieren das Arbeitsbuch des Patterngenerators: der Programm Generator bleibt das aktive"""
        X02.activate_workbook(self.get_workbook().Name)
        if prev_this is not None:
            X02.ThisWorkbook = prev_this

    async def on_ok(self):
        form = self.form
        if form is None:
            return
        if form.kind == "dest":
            form.SendToArduino_CheckBox.Value = bool(self.chk_arduino.value)
            form.GoBack_CheckBox.Value = bool(self.chk_back.value)
        prev_this = getattr(X02, "ThisWorkbook", None)

        def work():
            try:
                form.OK_Button_Click()                   # Pruefung der Zeile, Rueckruf des Patterngenerators, Symbol und Name der Zeile
            finally:
                self._restore(prev_this)
        try:
            await self.run_in_worker(work)
        except Exception as ex:                          # noqa: BLE001
            logger.exception("Zeilenauswahl: OK fehlgeschlagen")
            ui.notify(f"Fehler: {ex}", type="negative")
        self.refresh_pg()
        if not form.IsActive:                            # fertig (bei einer Fehlermeldung mit Wiederholen bleibt das Band stehen)
            if form.kind == "src" or form.GoBack_CheckBox.Value:
                self.show_tab("patt")

    async def on_abort(self):
        form = self.form
        if form is None:
            return
        prev_this = getattr(X02, "ThisWorkbook", None)

        def work():
            try:
                form.Abort_Button_Click()
            finally:
                self._restore(prev_this)
        try:
            await self.run_in_worker(work)
        except Exception:                                # noqa: BLE001
            logger.exception("Zeilenauswahl: Abbrechen fehlgeschlagen")
        self.hide_form(form)
        self.show_tab("patt")


def build_banner(ctrl, show_tab, run_in_worker, refresh_pg, get_workbook):
    """Im Behaelter des Programm Generators aufrufen (legt das Hinweisband an und meldet es am Controller an)"""
    return ExchangeBanner(ctrl, show_tab, run_in_worker, refresh_pg, get_workbook)
