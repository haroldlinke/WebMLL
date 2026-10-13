"""Web-Version der SerialMonitorPage (Registerkarte "Serial Monitor").

Zeigt, was der Arduino/Pico sendet (mit Uhrzeit), und schickt Eingaben dorthin. Dazu eine Zeile zum Verbinden und
Trennen (im Tk-Programm geschieht das ueber das Menue ARDUINO und die Seite ARDUINO Einstellungen).
"""
from __future__ import annotations

import logging
import time

from web_serial import list_serial_ports

logger = logging.getLogger(__name__)

FG_CLASSES = {"green": "text-green-8", "red": "text-red-8", "orange": "text-orange-8"}


def build(ctrl, run_command):
    """Baut die Seite in den aktuellen Container. run_command(func, label) ist der Befehlsrahmen aus headless_web
    (fuehrt func im Hintergrund-Thread aus und aktualisiert danach die Anzeige)."""
    from nicegui import ui

    macro = ctrl.MacroDef.data.get("SerialMonitorPage", {}) if getattr(ctrl, "MacroDef", None) else {}
    title = macro.get("Title", "Serial Monitor")
    send_text = macro.get("Button_1", "Senden")
    state = {"seq": 0}

    ui.label(title).classes("text-h6")

    # ---- Verbindung
    def port_options():
        ports = [p for p, _ in list_serial_ports()]
        cur = str(ctrl.getConfigData("serportname") or "")
        if cur and cur not in ports:
            ports.append(cur)
        return ports, cur

    options, current = port_options()
    with ui.row().classes("items-center gap-3 w-full"):
        port_sel = ui.select(options, value=current or None, label="Port (COM…, /dev/tty… oder IP:…)",
                             new_value_mode="add-unique").props("dense outlined use-input").classes("w-80")

        def refresh_ports():
            opts, cur = port_options()
            port_sel.set_options(opts, value=port_sel.value or cur or None)

        ui.button(icon="refresh", on_click=refresh_ports).props("flat round dense").tooltip("Portliste aktualisieren")
        ui.button("Verbinden", on_click=run_command(lambda: ctrl.connect(port_sel.value), "Verbinden")
                  ).props("color=primary dense no-caps")
        ui.button("Trennen", on_click=run_command(lambda: ctrl.disconnect(), "Trennen")).props("outline dense no-caps")
        status = ui.label("").classes("text-bold")

    # ---- Eingabe
    def send(_=None):
        text = inp.value or ""
        if not ctrl.is_connection_open():
            ui.notify("Nicht verbunden. Bitte zuerst verbinden.", type="warning")
            return
        ctrl.send_to_ARDUINO(text + "\r\n")
        log.push(time.strftime("%H:%M:%S") + "  > " + text, classes="text-blue-8")

    with ui.row().classes("items-center w-full gap-3"):
        inp = ui.input(label="Eingabe").props("dense outlined").classes("grow")
        inp.on("keydown.enter", send)
        ui.button(send_text, on_click=send).props("color=primary dense no-caps")
        ui.button("Anzeige leeren", on_click=lambda: log.clear()).props("flat dense no-caps")

    # ---- Anzeige
    log = ui.log(max_lines=2000).classes("w-full").style(
        "flex: 1 1 0; min-height: 200px; font-family: monospace; font-size: 13px; white-space: pre-wrap")

    def poll():
        seq, lines = ctrl.queue.lines_since(state["seq"])
        state["seq"] = seq
        for t, text in lines:
            log.push(time.strftime("%H:%M:%S", time.localtime(t)) + "  " + text.rstrip("\r\n"))
        text, fg = getattr(ctrl, "connect_status", ("", "black"))
        status.set_text(text)
        status.classes(replace="text-bold " + FG_CLASSES.get(fg, ""))

    ui.timer(0.2, poll)
