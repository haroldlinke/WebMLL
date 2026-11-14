# Datei-Version: 1.00 (2026-11-04) - web_pattern_test.py
# ----------------------------------------------------------------------------------------------
# Name:           web_pattern_test.py
# Path:           _web/web_pattern_test.py
# Version:        1.00
# Last Update:    2026-11-04
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-04  Neu: Fenster "Test Pattern" des Patterngenerators im Browser: die LEDs des Musters als Kreise, die mit den Zeiten des Musters die Farbe wechseln (wie das Excel-Programm
#                     auf dem Bildschirm); Wiederholen, PingPong, Goto-Muster mit Auswahl des Starts. Daten und Ablauf: headless_pattern_test.py
# ----------------------------------------------------------------------------------------------
"""Fenster "Test Pattern" des Patterngenerators.

Das Excel-Programm spielt das Muster auf dem Bildschirm ab (Kreise als LEDs), es sendet nichts an einen ARDUINO; das Senden an ein Modul (ATtiny) ist ein eigener Knopf und noch nicht
umgesetzt. Hier: ein Fenster mit einem Kreis je LED (bei RGB-Mustern je drei Kanaele), der mit den Zeiten des Musters die Farbe wechselt, darunter Start/Stop und bei Goto-Mustern die
Knoepfe fuer den Start. Die Farben werden direkt an den NiceGUI-Elementen gesetzt.
"""
from __future__ import annotations

import asyncio
import logging

from headless.headless_pattern_test import PatternPlayer
try:
    from _web.web_i18n import tr
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch
    def tr(text, **values):
        return text.format(**values) if values else text

logger = logging.getLogger(__name__)

def colors_at(data, step) -> list:
    """[R, G, B] je LED fuer das Muster step (1 bis steps)"""
    return [list(led["colors"][step - 1]) for led in data["leds"]]


async def show_pattern_test(data: dict, client):
    """Das Fenster oeffnen und das Muster abspielen; kehrt zurueck, wenn das Fenster geschlossen wird"""
    from nicegui import ui
    player = PatternPlayer(data["steps"], data["durations"], pingpong=data["pingpong"], goto=data["goto"], goto_list=data["goto_list"])
    st = {"task": None}
    dots = []
    with client:
        with ui.dialog().props("persistent") as dlg, ui.card().style("min-width: 340px; max-width: 96vw; max-height: 94vh; overflow: auto"):
            ui.label("%s: %s" % (tr("Test Pattern"), data["name"])).classes("text-h6")
            step_lbl = ui.label("").classes("text-body2")
            with ui.row().classes("w-full").style("gap: 10px; flex-wrap: wrap"):
                for led in data["leds"]:
                    with ui.column().classes("items-center").style("gap: 2px; width: 60px"):
                        dot = ui.element("div").style("width: 34px; height: 34px; border-radius: 50%; background: rgb(0,0,0); border: 2px solid #90a4ae")
                        dots.append(dot)
                        ui.label(led["label"]).classes("text-caption").style("font-size: 10px; max-width: 60px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis").tooltip(led["label"])
            note = ui.label("").classes("text-caption text-grey-8")
            if data["goto"]:
                with ui.row().classes("items-center").style("gap: 6px; flex-wrap: wrap"):
                    ui.label(tr("Start bei:")).classes("text-caption")
                    ui.button(tr("Anfang"), on_click=lambda: restart(0)).props("dense outline no-caps")
                    for k in range(1, player.start_count() + 1):
                        ui.button(tr("Start {n}", n=k), on_click=lambda k=k: restart(k)).props("dense outline no-caps")
            with ui.row().classes("justify-end w-full").style("gap: 8px"):
                run_btn = ui.button(tr("Stop"), on_click=lambda: toggle()).props("outline no-caps")
                ui.button(tr("Schließen"), on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")

        def show(step):
            with client:
                step_lbl.set_text(tr("Muster {n} von {total}", n=step, total=data["steps"]))
                for dot, (red, green, blue) in zip(dots, colors_at(data, step)):
                    dot.style(f"background: rgb({red},{green},{blue})")

        async def play():
            me = asyncio.current_task()
            try:
                with client:
                    run_btn.set_text(tr("Stop"))
                    note.set_text("")
                while True:
                    show(player.current)
                    await asyncio.sleep(player.duration_ms() / 1000.0)
                    if not player.advance():
                        with client:
                            note.set_text(tr("Das Muster ist zu Ende. Mit einem Start geht es weiter."))
                        break
            except asyncio.CancelledError:
                raise
            finally:
                if st.get("task") is me:                                              # ein beendeter alter Ablauf darf den neuen (nach Neustart) nicht ueberschreiben
                    st["task"] = None
                    with client:
                        run_btn.set_text(tr("Start"))

        def start_task():
            stop_task()
            st["task"] = asyncio.ensure_future(play())

        def stop_task():
            task = st.get("task")
            if task is not None and not task.done():
                task.cancel()
            st["task"] = None

        def restart(start_nr):
            player.start(start_nr)
            start_task()

        def toggle():
            task = st.get("task")
            if task is not None and not task.done():
                stop_task()
                with client:
                    run_btn.set_text(tr("Start"))
            else:
                if player.finished:
                    player.start(0)
                start_task()

        player.start(0)
        show(player.current)
        start_task()
        try:
            await dlg
        finally:
            stop_task()
            try:
                dlg.delete()
            except Exception:                                                     # noqa: BLE001
                logger.debug("Fenster Test Pattern nicht geloescht", exc_info=True)
