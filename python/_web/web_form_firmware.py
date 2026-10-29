# Datei-Version: 1.00 (2026-10-28) - web_form_firmware.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_firmware.py
# Path:           _web/web_form_firmware.py
# Version:        1.00
# Last Update:    2026-10-28
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-28  Neu: Firmware-Dialog fuer den Raspberry Pi Pico (Select_Firmware_Form der Version K)
# ----------------------------------------------------------------------------------------------

"""Firmware-Dialog fuer den Raspberry Pi Pico (Select_Firmware_Form des Excel-Programms 3.5.0-K) im Browser.

Links die Firmware-Namen (je Name die hoechste Version mit Kurztext), rechts die Auswahl der Version und der Langtext. Rueckgabe: der volle Pfad der
gewaehlten UF2-Datei oder None (Abbrechen). Die Dateien und Beschreibungen liest headless_pico.scan_firmware."""
import logging
import os

from _web import web_dialogs as wd
from _web.web_i18n import tr

logger = logging.getLogger(__name__)


async def firmware_async(groups: list, folder: str):
    """Dialog zur Auswahl von Firmware und Version; Rueckgabe Pfad der UF2-Datei oder None"""
    from nicegui import ui
    state = {"i": 0, "j": 0}

    def line(g):
        top = g["versions"][0]
        return f"{g['base']}    {top['version']}    {top['short']}"

    with wd._bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[820px] max-w-full"):
            ui.label(tr("Firmware für den Raspberry Pi Pico auswählen")).classes("text-h6")
            ui.label(tr("Ordner: {ordner}", ordner=folder)).classes("text-caption text-grey-7")
            with ui.row().classes("w-full no-wrap items-start"):
                with ui.scroll_area().classes("w-1/2").style("height: 280px; border: 1px solid #e0e0e0"):
                    radio = ui.radio({i: line(g) for i, g in enumerate(groups)}, value=0)
                with ui.column().classes("w-1/2"):
                    version = ui.select({j: v["version"] for j, v in enumerate(groups[0]["versions"])}, value=0, label=tr("Version")).classes("w-64")
                    short = ui.label(groups[0]["versions"][0]["short"]).classes("text-subtitle1")
                    detail = ui.label(groups[0]["versions"][0]["detail"]).style("white-space: pre-wrap")

            def refresh():
                v = groups[state["i"]]["versions"][state["j"]]
                short.set_text(v["short"])
                detail.set_text(v["detail"])

            def pick_group(e):
                if e.value is None:
                    return
                state["i"], state["j"] = int(e.value), 0                                 # eine andere Firmware: ihre hoechste Version
                version.set_options({j: v["version"] for j, v in enumerate(groups[state["i"]]["versions"])}, value=0)
                refresh()

            def pick_version(e):
                if e.value is None:
                    return
                state["j"] = int(e.value)
                refresh()
            radio.on_value_change(pick_group)
            version.on_value_change(pick_version)

            def ok():
                v = groups[state["i"]]["versions"][state["j"]]
                dlg.submit(os.path.join(folder, v["file"]))
            with ui.row().classes("justify-end w-full"):
                ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(None)).props("flat")
                ui.button(tr("Installieren"), on_click=ok).props("color=primary")
    dlg.open()
    answer = await dlg
    wd.safe_delete(dlg)
    return answer
