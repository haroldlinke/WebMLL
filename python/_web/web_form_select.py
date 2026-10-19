# Datei-Version: 1.01 (2026-10-18) - web_form_select.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_select.py
# Path:           _web/web_form_select.py
# Version:        1.01
# Last Update:    2026-10-18
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-18  neu: Dialoge des Patterngenerators im Browser: Auswahl aus einer Liste (Ersatz fuer Select_from_Sheet_Form: Spezial Mode, spaeter
#   1.01  2026-10-18  params_dialog: Parameter eingeben (Goto Aktivierung: Counter, RandomTime ...)
#                     Goto Aktivierung) und Eingabe einer Nummer (Ersatz fuer Select_LED_Address: RGB Modul Nr)
# ----------------------------------------------------------------------------------------------
"""Dialoge des Patterngenerators im Browser.

Die Makros des Originals rufen Formulare auf (Select_from_Sheet_Form.Show_Form, M60.Select_LED_Address_Dialog) und warten auf die Antwort. Im
Worker-Thread uebernehmen headless_pattgen.HeadlessSelectFromSheetForm und led_address_dialog das, die Anzeige im Browser setzen
install() ueber HeadlessPresenters ein. Wie bei den anderen Dialogen (web_dialogs) wartet der Worker, bis der Anwender geantwortet hat.
"""
from __future__ import annotations

import logging

from nicegui import ui

from _web import web_dialogs

logger = logging.getLogger(__name__)


async def select_dialog(req: dict):
    """Liste mit Name und Kurzbeschreibung, darunter Beschreibung und Details des gewaehlten Eintrags. Antwort:
    {"action": "select" | "delete" | "abort", "rows": [Zeile]}"""
    entries = req.get("entries") or []
    state = {"expert": bool(req.get("expert_checked")), "sel": None, "labels": {}}
    with web_dialogs._bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[700px] max-w-full gap-2"):
            ui.label(req.get("title") or "Auswahl").classes("text-h6")
            if req.get("head"):
                ui.label(req["head"]).classes("text-subtitle2 text-bold")
            if req.get("description"):
                ui.label(req["description"]).classes("text-caption text-grey-8").style("white-space: pre-wrap")
            if req.get("expert_caption"):
                ui.checkbox(req["expert_caption"], value=state["expert"], on_change=lambda e: on_expert(bool(e.value)))
            box = ui.column().classes("w-full gap-0").style("max-height: 240px; overflow-y: auto; border: 1px solid #bbb; border-radius: 4px")
            ui.label("Beschreibung").classes("text-caption text-grey-7")
            middle = ui.label("").classes("w-full").style("white-space: pre-wrap; min-height: 3em; max-height: 160px; overflow-y: auto")
            lower = ui.label("").classes("text-caption text-grey-8 w-full").style("white-space: pre-wrap")
            with ui.row().classes("justify-between items-center w-full"):
                count = ui.label("Ausgewählt: 0").classes("text-caption")
                with ui.row().classes("gap-2"):
                    ui.button("Abbrechen", on_click=lambda: dlg.submit({"action": "abort", "rows": []})).props("flat").classes("mll-cancel")
                    if req.get("delete_button"):
                        ui.button("Löschen", on_click=lambda: dlg.submit({"action": "delete", "rows": []})).props("outline color=negative")
                    ok = ui.button("Auswahl", on_click=lambda: submit()).classes("mll-default")
                    ok.set_enabled(False)

        def submit():
            if state["sel"] is not None:
                dlg.submit({"action": "select", "rows": [state["sel"]]})

        def choose(entry, double=False):
            state["sel"] = entry["row"]
            for row, label in state["labels"].items():
                label.classes(add="bg-blue-2" if row == entry["row"] else "", remove="" if row == entry["row"] else "bg-blue-2")
            middle.set_text(entry.get("middle") or entry.get("short") or "")
            lower.set_text(entry.get("lower") or "")
            count.set_text("Ausgewählt: 1")
            ok.set_enabled(True)
            if double:
                submit()

        def fill():
            box.clear()
            state["labels"] = {}
            state["sel"] = None
            with box:
                for entry in entries:
                    if entry.get("expert") and not state["expert"]:
                        continue
                    text = entry["name"] + (" : " + entry["short"] if entry.get("short") else "")
                    label = ui.label(text).classes("w-full px-2 py-1 cursor-pointer").style("white-space: nowrap; overflow: hidden; text-overflow: ellipsis")
                    label.on("click", lambda e=entry: choose(e))
                    label.on("dblclick", lambda e=entry: choose(e, True))
                    state["labels"][entry["row"]] = label
            middle.set_text("")
            lower.set_text("")
            count.set_text("Ausgewählt: 0")
            ok.set_enabled(False)

        def on_expert(value):
            state["expert"] = value
            fill()
        fill()
        result = await dlg
        web_dialogs.safe_delete(dlg)
    return result


async def number_dialog(req: dict):
    """Eingabe einer ganzen Zahl mit - und + (Ersatz fuer Select_LED_Address ohne Modul). Antwort: die Zahl oder None"""
    low, high = int(req.get("minimum", 0)), int(req.get("maximum", 255))
    with web_dialogs._bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[420px] max-w-full gap-2"):
            ui.label(req.get("title") or "Nummer").classes("text-h6")
            if req.get("text"):
                ui.label(req["text"]).classes("text-caption text-grey-8").style("white-space: pre-wrap")
            with ui.row().classes("items-center gap-2"):
                ui.button("\u2212", on_click=lambda: step(-1)).props("outline dense")
                number = ui.number(value=int(req.get("value", low)), min=low, max=high, step=1, precision=0).props("autofocus outlined dense").classes("w-28")
                ui.button("+", on_click=lambda: step(1)).props("outline dense")
                ui.label(f"Max: {high}").classes("text-caption text-grey-7")
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen", on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
                ui.button("OK", on_click=lambda: ok()).classes("mll-default")

        def step(delta):
            value = int(number.value or 0) + delta
            number.set_value(max(low, min(high, value)))

        def ok():
            if number.value is not None:
                dlg.submit(max(low, min(high, int(number.value))))
        number.on("keydown.enter", lambda: ok())
        result = await dlg
        web_dialogs.safe_delete(dlg)
    return result


async def params_dialog(req: dict):  # v1.01
    """Parameter eines Makros eingeben (Goto Aktivierung: Counter, RandomTime ...): je Parameter ein Feld mit Beschriftung und Hinweis. Die Pruefung macht
    req["validate"](Werte), eine Liste mit Fehlertext oder None je Parameter. Antwort: Liste der Werte oder None"""
    fields = []  # v1.01
    with web_dialogs._bridge["client"]:  # v1.01
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[620px] max-w-full gap-2"):  # v1.01
            ui.label(req.get("title") or "Parameter").classes("text-h6")  # v1.01
            if req.get("description"):  # v1.01
                ui.label(req["description"]).classes("text-caption text-grey-8").style("white-space: pre-wrap")  # v1.01
            for p in req.get("params") or []:  # v1.01
                field = ui.input(label=p.get("label") or p.get("name"), value=p.get("default") or "").props("outlined dense").classes("w-full")  # v1.01
                field.on("keydown.enter", lambda: ok())  # v1.01
                fields.append(field)  # v1.01
                if p.get("hint"):  # v1.01
                    ui.label(p["hint"]).classes("text-caption text-grey-7").style("white-space: pre-wrap")  # v1.01
            error = ui.label("").classes("text-negative").style("white-space: pre-wrap")  # v1.01
            with ui.row().classes("justify-end w-full"):  # v1.01
                ui.button("Abbrechen", on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")  # v1.01
                ui.button("OK", on_click=lambda: ok()).classes("mll-default")  # v1.01

        def ok():  # v1.01
            values = [str(f.value or "").strip() for f in fields]  # v1.01
            messages = [m for m in req["validate"](values) if m]  # v1.01
            if messages:  # v1.01
                error.set_text("\n".join(messages))  # v1.01
                return  # v1.01
            dlg.submit(values)  # v1.01
        result = await dlg  # v1.01
        web_dialogs.safe_delete(dlg)  # v1.01
    return result  # v1.01


def install():
    """Die Dialoge fuer headless_pattgen einsetzen (mehrfaches Aufrufen schadet nicht)"""
    from headless import headless_pattgen as HP
    HP.HeadlessPresenters.select = lambda req: web_dialogs.call_in_loop(select_dialog, req, default=None)
    HP.HeadlessPresenters.number = lambda req: web_dialogs.call_in_loop(number_dialog, req, default=None)
    HP.HeadlessPresenters.params = lambda req: web_dialogs.call_in_loop(params_dialog, req, default=None)  # v1.01
    logger.info("Auswahldialoge des Patterngenerators installiert")
