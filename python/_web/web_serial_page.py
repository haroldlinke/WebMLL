# Datei-Version: 1.07 (2026-11-26) - web_serial_page.py
# History of Change:
#   1.07  2026-11-26  Waehrend des Verbindungsaufbaus ist der Knopf grau, gesperrt und heisst Verbinden...
#   1.07  2026-11-26  Beim Wechsel des Anschlusses bei bestehender Verbindung zeigen Knopf und Statusanzeige jeden Schritt: erst 'Nicht verbunden' (Knopf Verbinden, rot), dann 'Verbindungsaufbau ... COMx', danach der Zustand des Anschlusses (Trennen, gruen). Zeilen mit '# v1.07'
#   1.06  2026-11-26  Besteht eine Verbindung und wird in der Portauswahl ein anderer Anschluss gewaehlt, wird getrennt und mit dem neuen Anschluss neu verbunden (nur Mitlesen). Zeilen mit '# v1.06'
#   1.05  2026-11-26  Die Ueberschrift heisst Serieller Monitor, der Knopf ohne Verbindung nur Verbinden. Zeilen mit '# v1.05'
#   1.04  2026-11-26  Der Serial Monitor liest nur mit: Verbinden oeffnet den Anschluss ohne Abfrage am Geraet (ctrl.connect_monitor, kein '#?'), auch fuer Geraete ohne das MobaLedLib-Programm LEDs_AutoProg. Zeilen mit '# v1.04'
#   1.03  2026-11-26  Verbinden und Trennen sind ein Knopf wie der zentrale Verbindungsknopf (rot: Mit Lichtmaschine verbinden, gruen: Trennen) und die Statusanzeige zeigt denselben Text wie dort ('Verbunden mit Pro/COM3 - EFFECT Mode'). Ohne Verbindung wird mit dem Anschluss der Auswahl verbunden, wenn er vom Anschluss des Blatts abweicht, sonst wie beim zentralen Knopf. Zeilen mit '# v1.03'
#   1.02  2026-11-26  Die Auswahl des Anschlusses zeigt bekannte Typen und den Untertyp nach der USB-Kennung (zum Beispiel 'COM3 – ESP32 (CP2102, 10C4:EA60)'); der Wert bleibt der Name des Anschlusses. Zeilen mit '# v1.02'
"""Web-Version der SerialMonitorPage (Registerkarte "Serial Monitor").

Zeigt, was der Arduino/Pico sendet (mit Uhrzeit), und schickt Eingaben dorthin. Dazu eine Zeile zum Verbinden und
Trennen (im Tk-Programm geschieht das ueber das Menue ARDUINO und die Seite ARDUINO Einstellungen).
"""
from __future__ import annotations

import asyncio  # v1.07
import logging
import time

from _web.web_serial import list_serial_ports_typed  # v1.02
try:  # v1.07
    from _web.web_i18n import tr  # v1.07
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v1.07
    def tr(text, **values):  # v1.07
        return text.format(**values) if values else text  # v1.07

logger = logging.getLogger(__name__)

FG_CLASSES = {"green": "text-green-8", "red": "text-red-8", "orange": "text-orange-8"}


def build(ctrl, run_command, connect_ui=None):  # v1.03: connect_ui = {toggle, status, sheet_port, texts} aus webmobaledlib (der zentrale Verbindungsknopf)
    """Baut die Seite in den aktuellen Container. run_command(func, label) ist der Befehlsrahmen aus webmobaledlib
    (fuehrt func im Hintergrund-Thread aus und aktualisiert danach die Anzeige)."""
    from nicegui import ui

    macro = ctrl.MacroDef.data.get("SerialMonitorPage", {}) if getattr(ctrl, "MacroDef", None) else {}
    title = macro.get("Title", "Serieller Monitor")  # v1.05
    send_text = macro.get("Button_1", "Senden")
    state = {"seq": 0, "connected_shown": None, "phase": False}  # v1.07: phase = der Anschluss wird gerade gewechselt (die Anzeige folgt dann den Schritten, nicht dem Zeitgeber)
    cui = connect_ui or {}  # v1.03
    text_off, text_on = cui.get("texts") or ("Verbinden", "Trennen")  # v1.03  # v1.05

    ui.label(title).classes("text-h6")

    # ---- Verbindung
    def port_options():
        ports = {p: label for p, label in list_serial_ports_typed()}  # v1.02: Anschluss -> Text mit Typ und Untertyp
        cur = str(ctrl.getConfigData("serportname") or "")
        if cur and cur not in ports:
            ports[cur] = cur
        return ports, cur

    options, current = port_options()
    with ui.row().classes("items-center gap-3 w-full"):
        port_sel = ui.select(options, value=current or None, label="Port (COM…, /dev/tty… oder IP:…)",
                             new_value_mode="add-unique").props("dense outlined use-input").classes("w-[28rem]")  # v1.02: breiter fuer den Typ

        def refresh_ports():
            opts, cur = port_options()
            port_sel.set_options(opts, value=port_sel.value or cur or None)

        ui.button(icon="refresh", on_click=refresh_ports).props("flat round dense").tooltip("Portliste aktualisieren")
        async def toggle(_=None):  # v1.03: ein Knopf wie der zentrale Verbindungsknopf: mit Verbindung trennen, ohne Verbindung verbinden
            try:
                connected = bool(ctrl.is_connection_open())
            except Exception:                                  # noqa: BLE001
                connected = False
            if connected:                                      # trennen: genau die Logik des zentralen Knopfs (trennen und merken), ohne Knopf einfach trennen
                await (cui["toggle"]() if "toggle" in cui else run_command(lambda: ctrl.disconnect(), "Trennen")())
                return
            sel = str(port_sel.value or "").strip()
            if not sel and "sheet_port" in cui:
                sel = str(cui["sheet_port"]() or "").strip()   # nichts gewaehlt: der Anschluss des Blatts
            await run_command(lambda: ctrl.connect_monitor(sel), "Verbinden")()  # v1.04: nur mitlesen, keine Abfrage am Geraet

        async def on_port_change(e):  # v1.06: Verbindung steht und ein anderer Anschluss wird gewaehlt: trennen und mit dem neuen neu verbinden
            new = str(e.value or "").strip()
            if not new:
                return
            try:
                connected = bool(ctrl.is_connection_open())
            except Exception:                                  # noqa: BLE001
                connected = False
            if not connected or getattr(ctrl, "ARDUINO_IP", False):
                return
            if new.upper() == str(getattr(ctrl, "ARDUINO_current_portname", "") or "").strip().upper():
                return                                         # derselbe Anschluss (zum Beispiel nach Aktualisieren der Liste)

            state["phase"] = True  # v1.07
            log.clear()  # v1.07: Ausgaben der vorherigen Verbindung loeschen
            try:
                await run_command(lambda: ctrl.disconnect(), "Trennen")()
                show(tr("Nicht verbunden"), "black", connected=False)  # v1.07: erst die Verbindung zum alten Anschluss ist weg ...
                await asyncio.sleep(0.3)
                show(tr("Verbindungsaufbau ...") + " " + new, "red", connected=False)
                conn_btn.set_text(tr("Verbinden..."))  # v1.07
                conn_btn.props("color=grey"); conn_btn.disable()  # v1.07  # v1.07: ... dann der Aufbau zum neuen
                await run_command(lambda: ctrl.connect_monitor(new), "Verbinden")()
            finally:
                conn_btn.enable()  # v1.07
                state["phase"] = False  # v1.07: danach zeigt der Zeitgeber wieder den Zustand der Verbindung
                state["connected_shown"] = None

        def show(text, fg, connected):  # v1.07: Statusanzeige und Knopf sofort setzen
            status.set_text(text)
            status.classes(replace="text-caption " + FG_CLASSES.get(fg, ""))
            conn_btn.set_text(text_on if connected else text_off)
            conn_btn.props("color=positive" if connected else "color=negative")
            conn_btn.enable()  # v1.07

        port_sel.on_value_change(on_port_change)  # v1.06
        conn_btn = ui.button(text_off, on_click=toggle).props("unelevated no-caps dense color=negative").classes("mll-connect")  # v1.03
        status = ui.label("").classes("text-caption").style("white-space: nowrap")  # v1.03: wie die Statusanzeige neben dem zentralen Knopf

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
        busy = bool(getattr(ctrl, "connecting", False))  # v1.07: Verbindungsaufbau laeuft: Knopf grau, gesperrt, Verbinden...
        if busy != state.get("busy_shown"):
            state["busy_shown"] = busy
            if busy:
                conn_btn.set_text(tr("Verbinden..."))
                conn_btn.props("color=grey"); conn_btn.disable()
            else:
                conn_btn.enable()
                state["connected_shown"] = None
        if busy or state["phase"]:  # v1.07: der Anschluss wird gewechselt oder aufgebaut: die Schritte setzen Status und Knopf selbst
            return
        if "status" in cui:  # v1.03: derselbe Text und dieselbe Farbe wie beim zentralen Verbindungsknopf
            text, fg = cui["status"]()
        else:
            text, fg = getattr(ctrl, "connect_status", ("", "black"))
        if status.text != text:
            status.set_text(text)
        status.classes(replace="text-caption " + FG_CLASSES.get(fg, ""))
        try:  # v1.03: Knopf rot ohne Verbindung, gruen mit Verbindung
            connected = bool(ctrl.is_connection_open())
        except Exception:                                      # noqa: BLE001
            connected = False
        if state["connected_shown"] != connected:
            state["connected_shown"] = connected
            conn_btn.set_text(text_on if connected else text_off)
            conn_btn.props("color=positive" if connected else "color=negative")

    ui.timer(0.2, poll)
