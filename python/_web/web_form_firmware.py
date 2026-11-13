# Datei-Version: 1.02 (2026-11-12) - web_form_firmware.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_firmware.py
# Path:           _web/web_form_firmware.py
# Version:        1.02
# Last Update:    2026-11-12
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-28  Neu: Firmware-Dialog fuer den Raspberry Pi Pico (Select_Firmware_Form der Version K)
#   1.01  2026-11-12  Excel-Programm 3.5.0L3: Knopf Firmware laden (Download aus dem Internet, danach wird die neue Firmware vorgewaehlt); der Dialog oeffnet auch ohne Firmware-Dateien (mit Hinweis, Installieren gesperrt)
#   1.02  2026-11-12  Knopf: 'Firmware herunterladen' (vorher 'Firmware laden')
# ----------------------------------------------------------------------------------------------

"""Firmware-Dialog fuer den Raspberry Pi Pico (Select_Firmware_Form des Excel-Programms 3.5.0-K) im Browser.

Links die Firmware-Namen (je Name die hoechste Version mit Kurztext), rechts die Auswahl der Version und der Langtext. Rueckgabe: der volle Pfad der
gewaehlten UF2-Datei oder None (Abbrechen). Die Dateien und Beschreibungen liest headless_pico.scan_firmware."""
import logging
import os

from _web import web_dialogs as wd
from _web.web_i18n import tr

logger = logging.getLogger(__name__)


async def firmware_async(groups: list, folder: str, download=None, rescan=None, texts=None):  # v1.01
    """Dialog zur Auswahl von Firmware und Version; Rueckgabe Pfad der UF2-Datei oder None.
    download: async-Funktion, die den Dialog Firmware Herunterladen zeigt und den Eintrag der heruntergeladenen Firmware (oder None) liefert (Knopf Firmware herunterladen, wie
    btnDownload im Excel-Programm); rescan: Funktion, die den Ordner neu einliest (Liste der Gruppen); texts: {"download": Beschriftung des Knopfes}.
    Ohne Firmware-Dateien zeigt der Dialog einen Hinweis; Installieren geht erst, wenn es eine gibt."""  # v1.01
    from nicegui import ui
    texts = texts or {}  # v1.01
    state = {"i": 0, "j": 0}
    ref = {}  # v1.01

    def line(g):
        top = g["versions"][0]
        return f"{g['base']}    {top['version']}    {top['short']}"

    with wd._bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[820px] max-w-full"):
            ui.label(tr("Firmware für den Raspberry Pi Pico auswählen")).classes("text-h6")
            ui.label(tr("Ordner: {ordner}", ordner=folder)).classes("text-caption text-grey-7")
            holder = ui.column().classes("w-full")  # v1.01: Auswahl, wird nach dem Herunterladen neu aufgebaut

            def build():  # v1.01
                holder.clear()
                if state["i"] >= len(groups):  # v1.01
                    state["i"], state["j"] = 0, 0  # v1.01
                with holder:
                    if not groups:  # v1.01: keine Firmware-Dateien im Ordner
                        ui.label(tr("Im Ordner {ordner} gibt es keine Firmware-Dateien (*.uf2). Die fertigen Firmware-Dateien gehören in diesen Ordner (Unterordner MobaLedLib/firmware des Sketchbook-Ordners).", ordner=folder)).style("white-space: pre-wrap")  # v1.01
                        return  # v1.01
                    with ui.row().classes("w-full no-wrap items-start"):
                        with ui.scroll_area().classes("w-1/2").style("height: 280px; border: 1px solid #e0e0e0"):
                            radio = ui.radio({i: line(g) for i, g in enumerate(groups)}, value=state["i"])  # v1.01 (vorher value=0)
                        with ui.column().classes("w-1/2"):
                            version = ui.select({j: v["version"] for j, v in enumerate(groups[state["i"]]["versions"])}, value=state["j"], label=tr("Version")).classes("w-64")  # v1.01
                            current = groups[state["i"]]["versions"][state["j"]]  # v1.01
                            short = ui.label(current["short"]).classes("text-subtitle1")  # v1.01
                            detail = ui.label(current["detail"]).style("white-space: pre-wrap")  # v1.01

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

            build()  # v1.01

            def select(entry):  # v1.01: die heruntergeladene Firmware vorwaehlen (Name und Version, sonst die erste)
                i = next((n for n, g in enumerate(groups) if g["base"].lower() == str(entry.get("name", "")).lower()), 0)
                j = next((n for n, v in enumerate(groups[i]["versions"]) if str(v["version"]) == str(entry.get("version", ""))), 0) if groups else 0
                state["i"], state["j"] = i, j

            async def on_download():  # v1.01
                entry = await download()
                if not entry:
                    return
                if rescan:
                    groups[:] = rescan()
                if groups:
                    select(entry)
                build()
                ref["ok"].set_enabled(bool(groups))

            def ok():
                v = groups[state["i"]]["versions"][state["j"]]
                dlg.submit(os.path.join(folder, v["file"]))
            with ui.row().classes("justify-between w-full"):  # v1.01 (vorher justify-end)
                if download is not None:  # v1.01
                    ui.button(texts.get("download") or tr("Firmware herunterladen"), on_click=on_download).props("outline no-caps")  # v1.01
                else:  # v1.01
                    ui.label("")  # v1.01
                with ui.row():  # v1.01
                    ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(None)).props("flat")
                    ref["ok"] = ui.button(tr("Installieren"), on_click=ok).props("color=primary")  # v1.01
                    ref["ok"].set_enabled(bool(groups))  # v1.01
    dlg.open()
    answer = await dlg
    wd.safe_delete(dlg)
    return answer


# async def firmware_async(groups: list, folder: str):  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#     """Dialog zur Auswahl von Firmware und Version; Rueckgabe Pfad der UF2-Datei oder None"""  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#     from nicegui import ui  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#     state = {"i": 0, "j": 0}  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#     def line(g):  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#         top = g["versions"][0]  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#         return f"{g['base']}    {top['version']}    {top['short']}"  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#     with wd._bridge["client"]:  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#         with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[820px] max-w-full"):  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#             ui.label(tr("Firmware für den Raspberry Pi Pico auswählen")).classes("text-h6")  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#             ui.label(tr("Ordner: {ordner}", ordner=folder)).classes("text-caption text-grey-7")  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#             with ui.row().classes("w-full no-wrap items-start"):  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 with ui.scroll_area().classes("w-1/2").style("height: 280px; border: 1px solid #e0e0e0"):  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                     radio = ui.radio({i: line(g) for i, g in enumerate(groups)}, value=0)  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 with ui.column().classes("w-1/2"):  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                     version = ui.select({j: v["version"] for j, v in enumerate(groups[0]["versions"])}, value=0, label=tr("Version")).classes("w-64")  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                     short = ui.label(groups[0]["versions"][0]["short"]).classes("text-subtitle1")  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                     detail = ui.label(groups[0]["versions"][0]["detail"]).style("white-space: pre-wrap")  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#             def refresh():  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 v = groups[state["i"]]["versions"][state["j"]]  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 short.set_text(v["short"])  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 detail.set_text(v["detail"])  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#             def pick_group(e):  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 if e.value is None:  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                     return  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 state["i"], state["j"] = int(e.value), 0                                 # eine andere Firmware: ihre hoechste Version  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 version.set_options({j: v["version"] for j, v in enumerate(groups[state["i"]]["versions"])}, value=0)  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 refresh()  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#             def pick_version(e):  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 if e.value is None:  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                     return  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 state["j"] = int(e.value)  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 refresh()  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#             radio.on_value_change(pick_group)  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#             version.on_value_change(pick_version)  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#             def ok():  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 v = groups[state["i"]]["versions"][state["j"]]  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 dlg.submit(os.path.join(folder, v["file"]))  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#             with ui.row().classes("justify-end w-full"):  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(None)).props("flat")  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#                 ui.button(tr("Installieren"), on_click=ok).props("color=primary")  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#     dlg.open()  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#     answer = await dlg  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#     wd.safe_delete(dlg)  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
#     return answer  # v1.01 (entfallen: ersetzt durch die Fassung mit Download und Hinweis ohne Firmware)
