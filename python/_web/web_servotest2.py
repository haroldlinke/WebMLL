# Datei-Version: 1.00 (2026-10-20) - web_servotest2.py
# ----------------------------------------------------------------------------------------------
# Name:           web_servotest2.py
# Path:           _web/web_servotest2.py
# Version:        1.00
# Last Update:    2026-10-20
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-20  Neu: Seite Servo Test 2 (ServoTestPage2.py ohne Tk), Teil A: direkte Steuerung von Direct Mode Servos (Betriebsarten 1 bis 10, ENTER, Regler 0 bis 255, Zeitgeber mit CRC4). Ohne Programmieren des ATtiny (Teil B und C)
# ----------------------------------------------------------------------------------------------
"""Web-Version der Seite "Servo Test 2" (mlpyproggen/ServoTestPage2.py, Klasse ServoTestPage2, ohne Tk): Servos im Direct Mode (Variante von Eckhart, ein ATtiny
statt des WS2811-Chips, Kommandos mit CRC4-Pruefsumme).

Teil A (diese Datei): direkte Steuerung. Noch nicht dabei: "Attiny Direkt Programmieren" (Hex-Datei ueber den Bus laden) und "Servo-Attiny Programmieren" (Formular fuer
den Programmieradapter).

Die Seite schickt in einem Zeitgeber (50 ms, mit Fast Refresh 40 ms) laufend ein Kommando an die LED des Servos. Die LED-Farbe besteht aus drei Bytes:
  #L <LED Nummer> <High> <Control mit CRC4> <Low> <Anzahl 1>
Je nach Betriebsart (servo_update_status des Originals):
  1 Normal: Position (High), Control 1                        6 Servo zuruecksetzen: High 0xE9, Low 0x8A, Control 5 (mit ENTER 13)
  2 Training standard, 3 Training weit: Control 2 oder 3         7 Werkseinstellung: High 0x16, Low 0x75, Control 5 (mit ENTER 13)
    (mit ENTER Control + 8)                                      8 Letzte Position zuruecksetzen: High 0x5A, Low 0x9E, Control 5 (mit ENTER 13)
  4 Max Speed: Control 4 (mit ENTER 12), Low 0x9A                9 Oszillator trimmen: High = Position * 35 / 255, Control 4 (mit ENTER 12), Low 0x9C
  5 Invers umschalten: High 1, Low 0x15, Control 4 (ENTER 12)   10 Speed (Legacy): Control 4 (mit ENTER 12), Low 0x65
Nach ENTER in den Betriebsarten 4 bis 8 und 10 (und nach dem zweiten Schritt in 2 und 3) wird die Betriebsart beim Loslassen von ENTER auf 0 gesetzt: Dann wird nichts
mehr gesendet (wie im Original).

Unterschiede zum Tk-Original (siehe HOC_intern.md, Version 1.91):
  * Der Zeitgeber sendet nur, wenn die Sendewarteschlange leer ist (ein Kommando wird bei der naechsten Runde ohnehin wiederholt), damit sich bei einer langsamen Verbindung
    nichts staut.
  * Die Betriebsart wird nicht gemerkt, die Seite beginnt immer mit 1 (Normal). Adresse, LED Kanal und Fast Refresh werden gemerkt (eigene Werte, nicht die von Servo Test 1).
  * Wird die Betriebsart geaendert, beginnt die Abfolge der ENTER-Taste (2nd Step) wieder von vorn.
  * ENTER ist beim Beruehren gedrueckt; rutscht der Finger ab (pointerleave, pointercancel), wird losgelassen.
  * Beim Verlassen des Reiters, beim Schliessen oder Neuladen der Seite und beim Beenden des Programms wird nur der Direktmodus beendet (wie im Original).
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

SERVO_SCALE_MIN = 0                   # Servo_Scale_Min
SERVO_SCALE_MAX = 255                 # Servo_Scale_Max
SERVO_RATE = 0.05                     # Sekunden: hoechstens 20 Positionen je Sekunde vom Regler (gesendet wird im Zeitgeber)
DELAY = 0.05                          # Servo_delay 50 ms
DELAY_FAST = 0.04                     # mit Fast Refresh (ServoCRCold) 40 ms
POS_ZERO_BUTTON = 1                   # die Taste "Pos 0" setzt im Original die Position 1 (nicht 0)

ENTER_TEXT, STEP2_TEXT, ENTER_BACK_TEXT = "ENTER", "2nd Step", "Enter"
MODES = {
    0: "0 = aus (es wird nichts gesendet)",
    1: "1 = Normal",
    2: "2 = Training (Standard)",
    3: "3 = Training (weit)",
    4: "4 = Max Speed programmieren",
    5: "5 = Invers umschalten",
    6: "6 = Servo zurücksetzen",
    7: "7 = Werkseinstellung",
    8: "8 = Letzte Position zurücksetzen",
    9: "9 = Oszillator trimmen (OSCCAL)",
    10: "10 = Speed programmieren (Legacy)",
}
PARAM_DEFAULTS = {                    # (Text, Min, Max, Vorgabe, Hinweis) falls MacroParamDef fehlt; Schluessel wie in MacroParamDef
    "ServoAddress": ("Servo Modul Adresse", 0, 32767, 1, "Moduladresse des Servos (LED-Nummer des Anschlusses)"),
    "ServoLEDChannel": ("LED Kanal", 0, 99, 0, "LED Kanal an dem die Servoplatine angeschlossen ist"),
    "ServoControl": ("Servo Betriebsart", 0, 10, 1, "Betriebsart des Servos"),
    "ServoCRCold": ("Fast Refresh (40 ms)", 0, 1, 0, "Refresh auf 40ms setzen (nur für Experten)"),
}
CONFIG_KEYS = {"ServoAddress": "Servo2Address", "ServoLEDChannel": "Servo2LEDChannel", "ServoCRCold": "Servo2FastRefresh"}     # eigene Werte dieser Seite

TEXT_FALLBACK = "Testen und Konfigurieren von Servos basierend auf der Direct Mode Variante von Eckhart"

CSS = """
.mll-servo2 { max-width: 760px; margin: 0 auto; padding: 8px; }
.mll-servo2-desc { cursor: pointer; }
.mll-servo2-fields { flex-wrap: wrap; }
.mll-servo2-field { flex: 1 1 130px; min-width: 110px; }
.mll-servo2-btn { min-height: 72px; touch-action: none; user-select: none; -webkit-user-select: none; -webkit-touch-callout: none; }
.mll-servo2-pos { flex: 1 1 0; min-width: 0; }
.mll-servo2-enter { flex: 2 1 0; min-width: 0; font-size: 18px; }
.mll-servo2-actions { flex-wrap: nowrap; }
"""

ACTIVE_MODELS: dict = {}              # Modelle der Seiten mit offenem Reiter -> laufende Nummer ihres Betretens
_SEQ = [0]


def _to_int(value, default=0):
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def stop_all(wait=False):
    """Fuer alle Seiten, die den Servo bedienen: Direktmodus beenden (Programm wird beendet oder neu gestartet)"""
    models = sorted(ACTIVE_MODELS, key=lambda m: ACTIVE_MODELS[m], reverse=True)          # die zuletzt betretene Seite zuerst
    for index, model in enumerate(models):
        ctrl = model.ctrl
        model.leave(quiet=index > 0)
        if wait:
            try:
                ctrl._wait_sent(1.0)
            except Exception:                                      # noqa: BLE001
                pass


class Servo2Model:
    """Logik der Seite. Die Anzeige liest mode, position, enter_text und ruft die Methoden auf. Ohne Browser testbar."""

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.address = self._clamp("ServoAddress", self._stored("ServoAddress"))
        self.channel = self._clamp("ServoLEDChannel", self._stored("ServoLEDChannel"))
        self.fast = bool(self._clamp("ServoCRCold", self._stored("ServoCRCold")))
        self.mode = 1                                   # ServoControl: beginnt immer mit Normal
        self.position = SERVO_SCALE_MIN                 # servo_position
        self.enter_pressed = False
        self.step_1 = False                             # servo_programm_step_1
        self.set_mode_normal = False                    # servo_set_mode_normal
        self.enter_text = ENTER_TEXT

    # ---- Parameter
    def definition(self, key):
        """(Text, Min, Max, Vorgabe, Hinweis) aus MacroParamDef (Min, Max, Vorgabe, Hinweis), sonst die eingebauten Werte"""
        d = {}
        try:
            d = self.ctrl.MacroParamDef.data.get(key, {}) or {}
        except AttributeError:
            pass
        text, lo, hi, default, hint = PARAM_DEFAULTS[key]
        if key in ("ServoAddress", "ServoLEDChannel", "ServoControl"):
            text = d.get("Input Text") or text
        return (text, lo if key in ("ServoControl", "ServoCRCold") else _to_int(d.get("Min"), lo), hi if key in ("ServoControl", "ServoCRCold") else _to_int(d.get("Max"), hi),
                default if key in ("ServoControl", "ServoCRCold") else _to_int(d.get("Default"), default), d.get("Hint") or hint)

    def _stored(self, key):
        try:
            value = self.ctrl.getConfigData(CONFIG_KEYS[key])
        except Exception:                                          # noqa: BLE001
            value = ""
        return value if value not in ("", None) else self.definition(key)[3]

    def _clamp(self, key, value):
        _, lo, hi, default, _ = self.definition(key)
        return max(lo, min(hi, _to_int(value, default)))

    def _persist(self, key, value):
        try:
            self.ctrl.setConfigData(CONFIG_KEYS[key], value)
            self.ctrl.SaveConfigData()
        except Exception:                                          # noqa: BLE001
            logger.debug("Wert %s nicht gesichert", key, exc_info=True)

    def leds_per_channel(self):
        """LEDs je Kanal aus der Startmeldung des Arduinos, sonst leer"""
        try:
            return [int(x) for x in (self.ctrl.max_ledcnt_list or [])]
        except (TypeError, ValueError, AttributeError):
            return []

    def channel_max(self):
        leds = self.leds_per_channel()
        return max(0, len(leds) - 1) if leds else self.definition("ServoLEDChannel")[2]

    def set_address(self, value):
        self.address = self._clamp("ServoAddress", value)
        self._persist("ServoAddress", self.address)
        return self.address

    def set_channel(self, value):
        self.channel = max(0, min(self.channel_max(), _to_int(value, self.channel)))
        self._persist("ServoLEDChannel", self.channel)
        return self.channel

    def set_fast(self, value):
        self.fast = bool(value)
        self._persist("ServoCRCold", 1 if self.fast else 0)
        return self.fast

    def interval(self):
        """Abstand des Zeitgebers in Sekunden (Servo_delay: 40 ms mit Fast Refresh, sonst 50 ms)"""
        return DELAY_FAST if self.fast else DELAY

    def set_mode(self, mode):
        """Betriebsart waehlen (0 bis 10); die Abfolge der ENTER-Taste beginnt von vorn"""
        self.mode = max(0, min(10, _to_int(mode, self.mode)))
        self.step_1 = False
        self.set_mode_normal = False
        self.enter_text = ENTER_TEXT
        return self.mode

    def set_position(self, position):
        self.position = max(SERVO_SCALE_MIN, min(SERVO_SCALE_MAX, _to_int(position, self.position)))
        return self.position

    def servo_address(self):
        """LED-Nummer des Servos: Servo Modul Adresse plus Versatz des LED-Kanals"""
        return self.address + int(self.ctrl.get_lednum_offset_for_channel(self.channel))

    # ---- ENTER (servo_prog_label_pressed, servo_prog_label_released)
    def enter_press(self):
        if self.enter_pressed:                          # schon gedrueckt: nicht noch einmal (sonst wuerde "2nd Step" doppelt weitergeschaltet)
            return False
        self.enter_pressed = True
        if self.mode in (2, 3):                         # Programmieren laeuft: zwei Schritte
            if self.step_1:
                self.enter_text = ENTER_BACK_TEXT
                self.step_1 = False
                self.set_mode_normal = True
            else:
                self.enter_text = STEP2_TEXT
                self.step_1 = True
        return True

    def enter_release(self):
        """Rueckgabe: True, wenn sich die Betriebsart geaendert hat (auf 0: danach wird nichts mehr gesendet)"""
        if not self.enter_pressed:
            return False
        self.enter_pressed = False
        if self.set_mode_normal:
            self.set_mode_normal = False
            self.mode = 0
            return True
        return False

    # ---- Kommandos (servo_update_status, _update_servos)
    def message(self, lednum, high, control, low, start_crc4=0, gen_crc4=True):
        """Nachricht #L ...: High, Control (mit CRC4 im oberen Halbbyte), Low als die drei Farbwerte der LED (wie _update_servos im Original)"""
        if gen_crc4:
            from tools.CRCalgorithms import CalculateControlValuewithChecksum
            control = CalculateControlValuewithChecksum(control, high, low, start_CRC4=start_crc4)
        if self.ctrl.mobaledlib_version == 1:
            return "#L" + "{:02x}".format(lednum) + " " + "{:02x}".format(high) + " " + "{:02x}".format(control) + " " + "{:02x}".format(low) + " " + "{:02x}".format(1) + "\n"
        return "#L " + "{:02x}".format(lednum) + " " + "{:02x}".format(high) + " " + "{:02x}".format(control) + " " + "{:02x}".format(low) + " " + "{:04x}".format(1) + "\n"

    def command(self):
        """Das Kommando dieser Runde als (High, Control, Low) oder None (Betriebsart 0): Port von servo_update_status. Setzt auch set_mode_normal."""
        control, position, enter = self.mode, self.position, self.enter_pressed
        if control == 1:                                # normale Position
            return position, control, 0
        if control in (2, 3):                           # Training: Endpositionen
            if enter:
                control += 8                            # ENTER-Bit
            return position, control, 0
        if control == 4:                                # max Speed programmieren
            if enter:
                control += 8
                self.set_mode_normal = True
            return position, control, 0x9A
        if control == 5:                                # Invers umschalten
            if enter:
                self.set_mode_normal = True
                return 1, 12, 0x15
            return 1, 4, 0x15
        if control == 6:                                # Servo zuruecksetzen
            if enter:
                self.set_mode_normal = True
                return 0xE9, 13, 0x8A
            return 0xE9, 5, 0x8A
        if control == 7:                                # alles auf Werkseinstellung
            if enter:
                self.set_mode_normal = True
                return 0x16, 13, 0x75
            return 0x16, 5, 0x75
        if control == 8:                                # letzte Position zuruecksetzen
            if enter:
                self.set_mode_normal = True
                return 0x5A, 13, 0x9E
            return 0x5A, 5, 0x9E
        if control == 9:                                # Oszillator trimmen
            tune_val = int(position * 35 / 255.0)
            control = 4
            if enter:
                control += 8
            return tune_val, control, 0x9C
        if control == 10:                               # Speed programmieren, Legacy
            control = 4
            if enter:
                control += 8
                self.set_mode_normal = True
            return position, control, 0x65
        return None

    def on_timer(self):
        """Eine Runde des Zeitgebers (servo_status_loop): Kommando bilden und senden. Rueckgabe: die gesendete Nachricht oder None."""
        command = self.command()
        if command is None:
            return None
        message = self.message(self.servo_address(), *command)
        idle = getattr(self.ctrl, "tx_idle", None)
        if idle is not None and not idle():              # die letzte Nachricht ist noch nicht gesendet: diese Runde auslassen (die naechste wiederholt es)
            return None
        self.ctrl.send_to_ARDUINO(message)
        return message

    # ---- Reiter betreten und verlassen
    def tab_selected(self):
        _SEQ[0] += 1
        ACTIVE_MODELS[self] = _SEQ[0]
        self.enter_pressed = False
        self.step_1 = False
        self.set_mode_normal = False
        self.enter_text = ENTER_TEXT
        try:
            self.ctrl.ARDUINO_begin_direct_mode()
        except Exception:                                          # noqa: BLE001
            logger.warning("Direktmodus konnte nicht gestartet werden", exc_info=True)

    def leave(self, quiet=False):
        """Reiter oder Seite verlassen: ENTER loslassen, Direktmodus beenden (nur einmal; hat eine NEUERE Seite den Servo uebernommen, zum Beispiel nach dem Neuladen im
        Browser, wird der Direktmodus nicht beendet). quiet: nur aufraeumen."""
        mine = ACTIVE_MODELS.pop(self, None)
        self.enter_pressed = False
        self.set_mode_normal = False
        try:
            newer = mine is not None and any(number > mine for number in ACTIVE_MODELS.values())
            if mine is not None and not newer and not quiet:
                self.ctrl.ARDUINO_end_direct_mode()
        except Exception:                                          # noqa: BLE001
            logger.warning("Servo Test 2 beim Verlassen nicht sauber beendet", exc_info=True)

    tab_unselected = leave


# --------------------------------------------------------------------------- Oberflaeche (NiceGUI)
class Servo2Page:
    """Rueckgabe von build: tab_selected(), tab_unselected(), page_closed(), model"""

    def __init__(self, model, refresh, timer):
        self.model = model
        self._refresh = refresh
        self._timer = timer

    def tab_selected(self):
        self.model.tab_selected()
        self._timer.interval = self.model.interval()
        self._timer.active = True
        self._refresh()

    def tab_unselected(self):
        self._timer.active = False
        self.model.leave()
        self._refresh()

    def page_closed(self):
        """Der Browser hat die Seite verlassen (geschlossen, neu geladen, Verbindung weg): Direktmodus beenden, nichts mehr in die Anzeige schreiben"""
        self._timer.active = False
        self.model.leave()


def build(ctrl, is_active=None):
    """Baut die Seite "Servo Test 2" in den aktuellen Container. is_active: liefert True, solange die Seite sichtbar ist."""
    from nicegui import ui

    model = Servo2Model(ctrl)
    macro = ctrl.MacroDef.data.get("ServoTestPage2", {}) if getattr(ctrl, "MacroDef", None) else {}
    title = macro.get("Title") or "MobaLedLib LED-Servotester für Direct Mode Servos"
    description = macro.get("Ausführliche Beschreibung") or macro.get("Kurzbeschreibung") or TEXT_FALLBACK
    ui.add_head_html("<style>" + CSS + "</style>")
    refs: dict = {}
    desc = {"open": False}

    def refresh_description():
        opened = desc["open"]
        refs["description"].set_text(description if opened else description.split("\n")[0])
        shape = "white-space: pre-line; overflow: visible; text-overflow: clip" if opened else "white-space: nowrap; overflow: hidden; text-overflow: ellipsis"
        refs["description"].style(f"background: #f0f0f0; padding: 6px 10px; border: 1px solid #aaa; min-width: 0; {shape}")
        refs["desc_toggle"].props(f"icon={'expand_less' if opened else 'expand_more'}")

    def toggle_description(_=None):
        desc["open"] = not desc["open"]
        refresh_description()

    def current(key):
        return {"address": model.address, "channel": model.channel, "mode": model.mode, "fast": model.fast}[key]

    def refresh():
        refresh_description()
        refs["guard"] = True                            # Werte vom Programm gesetzt, nicht vom Anwender
        try:
            refs["address"].set_value(model.address)
            refs["channel"].set_value(model.channel)
            refs["mode"].set_value(model.mode)
            refs["fast"].set_value(model.fast)
        finally:
            refs["guard"] = False
        refs["slider"].set_value(model.position)
        refs["position"].set_text(str(model.position))
        refs["enter"].set_text(model.enter_text)

    def tick():
        if is_active is not None and not is_active():
            return
        model.on_timer()

    def changed(key, value, apply):
        if value is None or refs.get("guard") or value == current(key) or (key in ("address", "channel", "mode") and _to_int(value, current(key)) == current(key)):
            return
        refs["guard"] = True
        try:
            apply(value)
            if key == "fast":
                refs["timer"].interval = model.interval()
        finally:
            refs["guard"] = False
        refresh()

    def on_slide(e):
        args = e.args
        value = args[0] if isinstance(args, (list, tuple)) and args else args
        model.set_position(value)
        refs["position"].set_text(str(model.position))

    def set_pos(value):
        model.set_position(value)
        refs["slider"].set_value(model.position)
        refs["position"].set_text(str(model.position))

    def enter_down(_=None):
        if model.enter_press():
            refs["enter"].set_text(model.enter_text)

    def enter_up(_=None):
        if model.enter_release():
            refresh()                                   # die Betriebsart wurde auf 0 gesetzt
        refs["enter"].set_text(model.enter_text)

    with ui.column().classes("w-full items-stretch gap-3 mll-servo2"):
        ui.label(title).classes("text-h6")
        with ui.row().classes("w-full items-center no-wrap gap-1 mll-servo2-desc"):
            refs["description"] = ui.label(description).classes("grow").tooltip("Antippen zum Auf- und Zuklappen")
            refs["description"].on("click", toggle_description)
            refs["desc_toggle"] = ui.button(icon="expand_more", on_click=toggle_description).props("flat dense round")
        with ui.card().props("flat bordered").classes("w-full"):
            with ui.row().classes("w-full items-end gap-2 mll-servo2-fields"):
                text, lo, hi, _, hint = model.definition("ServoAddress")
                refs["address"] = ui.number(label=text, value=model.address, min=lo, max=hi, step=1, precision=0,
                                            on_change=lambda e: changed("address", e.value, model.set_address)).props("dense outlined").classes("mll-servo2-field")
                refs["address"].tooltip(hint)
                text, lo, hi, _, hint = model.definition("ServoLEDChannel")
                refs["channel"] = ui.number(label=text, value=model.channel, min=lo, max=hi, step=1, precision=0,
                                            on_change=lambda e: changed("channel", e.value, model.set_channel)).props("dense outlined").classes("mll-servo2-field")
                refs["channel"].tooltip(hint)
            text, _, _, _, hint = model.definition("ServoControl")
            refs["mode"] = ui.select(MODES, value=model.mode, label=text, on_change=lambda e: changed("mode", e.value, model.set_mode)).props("dense outlined").classes("w-full")
            refs["mode"].tooltip("Betriebsart des Servos: 1 Normal, 2 und 3 Training, 4 Max Speed, 5 Invers, 6 Servo zurücksetzen, 7 Werkseinstellung, 8 letzte Position zurücksetzen, 9 Oszillator trimmen")
            text, _, _, _, hint = model.definition("ServoCRCold")
            refs["fast"] = ui.checkbox(text, value=model.fast, on_change=lambda e: changed("fast", e.value, model.set_fast))
            refs["fast"].tooltip(hint)
        with ui.row().classes("w-full items-center no-wrap gap-2"):
            left = ui.button(icon="chevron_left", on_click=lambda: set_pos(model.position - 1)).props("outline")
            left.tooltip("Position um 1 verringern")
            refs["slider"] = ui.slider(min=SERVO_SCALE_MIN, max=SERVO_SCALE_MAX, step=1, value=model.position).props("label markers=51").classes("grow")
            refs["slider"].tooltip("Position des Servos 0..255. Mit den Pfeiltasten Schritt für Schritt, Pos1 und Ende springen an den Anfang und das Ende.")
            refs["slider"].on("update:model-value", on_slide, throttle=SERVO_RATE)
            right = ui.button(icon="chevron_right", on_click=lambda: set_pos(model.position + 1)).props("outline")
            right.tooltip("Position um 1 erhöhen")
            refs["position"] = ui.label(str(model.position)).style("min-width: 3em; text-align: right")
        with ui.row().classes("w-full items-stretch gap-2 mll-servo2-actions"):
            zero = ui.button("Pos 0", on_click=lambda: set_pos(POS_ZERO_BUTTON)).props("outline no-caps").classes("mll-servo2-btn mll-servo2-pos")
            zero.tooltip("Position 1 (wie im Original)")
            refs["enter"] = ui.button(model.enter_text).props("outline no-caps").classes("mll-servo2-btn mll-servo2-enter")
            refs["enter"].tooltip("ENTER: gedrückt halten. In den Betriebsarten 2 und 3 zweimal drücken (2nd Step)")
            refs["enter"].on("pointerdown", enter_down)
            for event in ("pointerup", "pointercancel", "pointerleave"):       # auch wenn der Finger abrutscht: immer loslassen
                refs["enter"].on(event, enter_up)
            full = ui.button("Pos 255", on_click=lambda: set_pos(255)).props("outline no-caps").classes("mll-servo2-btn mll-servo2-pos")
    timer = ui.timer(DELAY, tick)
    timer.active = False
    refs["timer"] = timer
    refresh()
    return Servo2Page(model, refresh, timer)
