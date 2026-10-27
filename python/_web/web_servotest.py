# Datei-Version: 2.06 (2026-10-26) - web_servotest.py
# ----------------------------------------------------------------------------------------------
# Name:           web_servotest.py
# Path:           _web/web_servotest.py
# Version:        2.06
# Last Update:    2026-10-26
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-20  Neu: Seite Servo Test 1 nach ServoTestPage.py (Tk): Regler, Servo STOP, Dec/Inc mit Halten, Programmieren in vier Schritten
#   2.00  2026-10-20  Umbau nach dem Excel-Dialog Servo Test und Einstellung (UserForm): Auswahl LED Nummer, Anschluss, LED Kanal; Regler mit Wackeln und Keep-Alive; Konfigurieren in drei Schritten mit gehaltenen Pfeiltasten (Zeitgeber 100 ms); Servo zuruecksetzen; Schliessen
#   2.01  2026-10-20  Layout fuer das Smartphone: Beschreibung eine Zeile und aufklappbar, Servo Modul Auswahl in der Zeile der Felder, die drei Tasten in einer Zeile (auch beim Konfigurieren)
#   2.02  2026-10-20  Die dritte Taste im Zustand Einstellen heisst Verbinden (statt Schliessen) und ruft die Funktion des Menuepunkts ARDUINO -> Verbinden auf; close entfaellt
#   2.03  2026-10-20  Verlassen von Reiter und Seite: leave() sendet Wert 0 und beendet den Direktmodus, bricht laufende Ablaeufe ab (epoch), nur einmal und ohne eine andere Seite zu stoeren; stop_all fuer Beenden und Neustart; page_closed fuer das Trennen des Browsers
#   2.04  2026-10-21  Die dritte Taste im Zustand Einstellen (Verbinden) entfaellt: verbunden wird mit der Taste Mit ARDUINO verbinden in der Kopfzeile fuer alle Reiter; neu ServoPage.on_connected (Direktmodus und Servo waehlen nach dem Verbinden)
#   2.05  2026-10-23  Texte mit eingesetzten Werten (f-Strings) mit tr("... {name}", name=...) umgestellt, damit sie uebersetzt werden
#   2.06  2026-10-26  Zusammengesetzte Meldungen (Verkettungen und f-Strings) mit tr(...) uebersetzbar gemacht
# ----------------------------------------------------------------------------------------------
"""Web-Version der Seite "Servo Test 1" nach dem Excel-Dialog "Servo Test und Einstellung" (UserForm der Excel-Fassung, Stand Oktober 2026).

Die Seite schickt Servo-Kommandos als LED-Befehl ueber dieselbe serielle Schnittstelle wie der Farb Test (web_serial):

  #L <Adresse> <s0> <s1> <s2> 01      (mobaledlib_version 2: Adresse 4 Hex-Ziffern, Version 1: #L<Adresse mit 2 Hex-Ziffern>)

Adresse = Versatz des LED-Kanals + LED Nummer; s0, s1, s2 sind die Werte der drei Anschluesse (Anschluss 0, 1, 2). Die Namen folgen dem VBA-Code (ShowDialog, SendValue,
SetMin_Button_Click, OnTimer ...).

Zwei Zustaende wie im Dialog:
  * Einstellen (prog_step 0): LED Nummer, Anschluss, LED Kanal waehlen; Schieberegler fuer die Position; nach jeder Wahl waehlt die Seite den Servo (225, 230, 235) und
    laesst ihn kurz wackeln (110 und 120 im Wechsel, 20 Schritte), damit man ihn erkennt. Der Zeitgeber (100 ms) schickt sonst ein Keep-Alive (#L 0 0 0 0 0).
  * Konfigurieren (prog_step 1 bis 3: Minimalposition, Maximalposition, Geschwindigkeit): Die Pfeiltasten << < > >> werden gehalten; der Zeitgeber schickt alle 100 ms den Wert
    (100 in der Ruhe, davon weg in Schritten von 1 oder 5, begrenzt auf 20 bis 180).

Unterschiede zum Excel-Dialog (siehe HOC_intern.md, Version 1.84):
  * Die Pausen von 200 ms zwischen den Befehlen sind asynchron (await), der Browser bleibt bedienbar; waehrenddessen ruhen Zeitgeber und Tasten (busy).
  * Das Keep-Alive geht nur, wenn die Sendewarteschlange leer ist (Servo-Nachrichten dauern pro Zeichen maxLEDcnt * 0,2 ms).
  * Die dritte Taste im Zustand Einstellen (im Excel-Dialog Schliessen) gibt es im Browser nicht: Sie ist ausgeblendet. Verbunden wird mit dem Knopf Mit ARDUINO verbinden in der
    Kopfzeile (fuer alle Reiter); danach startet die Seite den Direktmodus und waehlt den Servo (ServoPage.on_connected).
  * ResetPostition im VBA-Code ruft SendValue mit der Position statt mit dem Anschluss als Modul auf und sendet deshalb nie etwas. Das Verhalten ist uebernommen
    (reset_position tut nichts); gemeint war wohl "Wert 0 an den vorher gewaehlten Servo".
  * Tippfehler "Positition" im Text berichtigt.
"""
from __future__ import annotations

import asyncio
import logging
import time
try:  # v2.05
    from _web.web_i18n import tr  # v2.05
except ImportError:  # v2.05                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v2.05
    def tr(text, **values):  # v2.05
        return text.format(**values) if values else text  # v2.05

logger = logging.getLogger(__name__)

ACTIVE_MODELS: dict = {}              # Modelle der Seiten, die den Servo gerade bedienen (Reiter offen) -> laufende Nummer ihres Betretens  # v2.03
_SEQ = [0]  # v2.03


class _Aborted(Exception):  # v2.03
    """Ein Ablauf mit Pausen wurde durch das Verlassen des Reiters oder der Seite abgebrochen"""  # v2.03


def stop_all(wait=False):  # v2.03
    """Fuer alle Seiten, die den Servo bedienen: Ablaeufe abbrechen, Wert 0 senden, Direktmodus beenden (Programm wird beendet oder neu gestartet).
    wait: kurz warten, bis die Nachrichten gesendet sind (der Sendethread ist ein Hintergrundthread)."""
    models = sorted(ACTIVE_MODELS, key=lambda m: ACTIVE_MODELS[m], reverse=True)          # die zuletzt betretene Seite zuerst: sie sendet, die aelteren schweigen  # v2.03
    for index, model in enumerate(models):  # v2.03
        ctrl = model.ctrl  # v2.03
        model.leave(quiet=index > 0)  # v2.03
        if wait:  # v2.03
            try:  # v2.03
                ctrl._wait_sent(1.0)  # v2.03
            except Exception:                                      # noqa: BLE001  # v2.03
                pass  # v2.03

SERVO_SCALE_MIN = 10                  # Bereich des Schiebereglers (wie ServoTestPage.py: Servo_Scale_Min, Servo_Scale_Max)
SERVO_SCALE_MAX = 210
SERVO_RATE = 0.1                      # Sekunden: hoechstens zehn Positionen je Sekunde beim Ziehen des Reglers
TICK = 0.1                            # Zeitgeber (StartTimer Me, 100)

SRV_WAIT_TIME_CMD = 0.2               # Pause zwischen den Befehlen (Sleep 200)
SRV_POS_DEFAULT = 100                 # Ruhewert beim Konfigurieren
SRV_WIGG_MIN, SRV_WIGG_MAX = 110, 120
SRV_WIGG_TIME = 0.5                   # Sekunden zwischen den Wackel-Schritten
SRV_WIGG_FIRST = 0.2                  # Sekunden bis zum ersten Wackel-Schritt
SRV_WIGG_COUNT = 20
SRV_DEFAULT_MIN_POS = 55              # Grundeinstellung (Servo zuruecksetzen)
SRV_DEFAULT_MAX_POS = 110
SRV_DEFAULT_SPEED = 58
SRV_BUTTON1 = 205
SRV_SEL_LED = {0: 225, 1: 230, 2: 235}
SRV_MIN_MAX = 240
SRV_SPEED = 245
SRV_SPECIAL = 250
SRV_FINISH = 254
LIMIT_LOW, LIMIT_HIGH = 20, 180       # Begrenzung des Werts beim Konfigurieren

# gehaltene Pfeiltasten: (Startwert bei MouseDown, Schritt je Zeitgeber)
ARROWS = {"minus2": (90, -5), "minus1": (96, -1), "plus1": (104, 1), "plus2": (110, 5)}
ARROW_LABELS = {"minus2": "<<", "minus1": "<", "plus1": ">", "plus2": ">>"}

PARAMS = ("ServoAddress", "ServoLEDChannel", "ServoChannel")          # Namen der gemerkten Werte (wie in der Tk-Fassung)
PARAM_DEFAULTS = {                    # (Text im Excel-Dialog, Min, Max, Vorgabe, Hinweis)
    "ServoAddress": ("LED Nummer", 0, 32767, 1, "Moduladresse des Servos (LED-Nummer des Anschlusses)"),
    "ServoLEDChannel": ("LED Kanal", 0, 99, 0, "LED Kanal an dem die Servoplatine angeschlossen ist"),
    "ServoChannel": ("Anschluss", 0, 2, 0, "Anschluss des Servos (RGB-Nummer des Anschlusses)"),
}

TEXT_DEFAULT = ("Wählen sie zuerst die Adresse des Servos.\nMit dem Schieberegler wird die Position eingestellt.\n\n"
                "Mit den Knöpfen unten wird der aktuelle Servo konfiguriert.")
TEXT_POSITION = "Mit den Pfeiltasten wird die Position eingestellt. Durch Halten der Tasten wird die Position schneller verändert"
# TEXT_MIN = "Konfiguration der Minimalposition\n\n" + TEXT_POSITION  # v2.06 (entfallen)
# TEXT_MAX = "Konfiguration der Maximalposition\n\n" + TEXT_POSITION  # v2.06 (entfallen)
TEXT_MIN = "Konfiguration der Minimalposition\n\n" + TEXT_POSITION  # v2.06 (wieder wie vorher; uebersetzt wird beim Aufruf mit text_min(), nicht beim Import)
TEXT_MAX = "Konfiguration der Maximalposition\n\n" + TEXT_POSITION  # v2.06


def text_min():  # v2.06
    return tr("Konfiguration der Minimalposition\n\n") + tr(TEXT_POSITION)  # v2.06


def text_max():  # v2.06
    return tr("Konfiguration der Maximalposition\n\n") + tr(TEXT_POSITION)  # v2.06
TEXT_SPEED = ("Konfiguration der Geschwindigkeit\n\nMit den Pfeiltasten wird die Geschwindigkeit eingestellt. "
              "Durch Halten der Tasten wird die Geschwindigkeit schneller verändert")
BUTTON_START, BUTTON_NEXT = "Servo Konfigurieren", "Weiter"
BUTTON2_RESET, BUTTON2_SAVE = "Servo zurücksetzen", "Einstellungen speichern"
# BUTTON_CONNECT, BUTTON_NO_SAVE = "Verbinden", "nicht speichern"  # v2.04 (entfallen)
BUTTON_CONNECT, BUTTON_NO_SAVE = "", "nicht speichern"          # die dritte Taste ist im Zustand Einstellen ausgeblendet (verbunden wird in der Kopfzeile)  # v2.04
CONFIRM_RESET_TITLE = "Servo zurücksetzen"
CONFIRM_RESET_TEXT = "Sollen der Servo auf die Grundeinstellungen (Limits, Geschwindigkeit) zurückgesetzt werden?"
COLOR_DEFAULT, COLOR_STEP = "#f0f0f0", "#c0ffc0"

CSS = """
.mll-servo { max-width: 760px; margin: 0 auto; padding: 8px; }
.mll-servo-btn { min-height: 52px; min-width: 64px; touch-action: none; user-select: none; -webkit-user-select: none; -webkit-touch-callout: none; }
.mll-servo-wide { min-height: 52px; }
@media (max-width: 600px) { .mll-servo-arrow { flex: 1 1 20%; min-width: 0; } }
.mll-servo-desc { cursor: pointer; }
.mll-servo-fields { flex-wrap: nowrap; }
.mll-servo-caption { flex: 0 1 auto; align-self: center; max-width: 7em; line-height: 1.15; }
.mll-servo-field { flex: 1 1 0; min-width: 64px; max-width: 150px; }
.mll-servo-actions { flex-wrap: nowrap; }
.mll-servo-action { flex: 1 1 0; min-width: 0; min-height: 52px; padding: 4px 6px; font-size: 13px; line-height: 1.15; }
.mll-servo-action .q-btn__content { white-space: normal; text-align: center; }
"""


def _to_int(value, default=0):
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


class ServoModel:
    """Logik des Dialogs. Die Anzeige liest die Felder unter "Anzeige" und ruft die Methoden auf. sleep und now lassen sich fuer Tests ersetzen."""

    def __init__(self, ctrl, sleep=None, now=None):
        self.ctrl = ctrl
        self.sleep = sleep or asyncio.sleep
        self.now = now or time.monotonic
        self.address = self._clamp_param("ServoAddress", self._stored("ServoAddress"))
        self.channel = self._clamp_param("ServoLEDChannel", self._stored("ServoLEDChannel"))
        self.module = self._clamp_param("ServoChannel", self._stored("ServoChannel"))
        self.position = SERVO_SCALE_MIN + (SERVO_SCALE_MAX - SERVO_SCALE_MIN) // 2        # 110
        self.pressed = None                 # Name der gehaltenen Pfeiltaste
        self.busy = False                   # laeuft ein Ablauf mit Pausen: Zeitgeber und Tasten ruhen
        self._epoch = 0                     # wird beim Verlassen erhoeht: ein laufender Ablauf bricht dann beim naechsten Schritt ab  # v2.03
        self.min_max_active = False         # MinMaxActive
        self.active_button = 0
        self.min_max_value = SRV_POS_DEFAULT
        self.last_value = 0
        self.ticks_since_press = 0
        self.release_pending = False
        self.wig_count = 0
        self.wig_time = 0.0
        self.reset_buttons()

    # ---- Parameter und Grenzen
    def definition(self, key):
        """(Text, Min, Max, Vorgabe, Hinweis) aus MacroParamDef (Min, Max, Vorgabe, Hinweis) und dem Excel-Dialog (Text)"""
        d = {}
        try:
            d = self.ctrl.MacroParamDef.data.get(key, {}) or {}
        except AttributeError:
            pass
        text, lo, hi, default, hint = PARAM_DEFAULTS[key]
        return (text, _to_int(d.get("Min"), lo), _to_int(d.get("Max"), hi), _to_int(d.get("Default"), default), d.get("Hint") or hint)

    def _stored(self, key):
        try:
            value = self.ctrl.getConfigData(key)
        except Exception:                                          # noqa: BLE001
            value = ""
        return value if value not in ("", None) else self.definition(key)[3]

    def _clamp_param(self, key, value):
        _, lo, hi, default, _ = self.definition(key)
        return max(lo, min(hi, _to_int(value, default)))

    def leds_per_channel(self):
        """LEDs je Kanal (LEDsPerChannel im Dialog): aus der Startmeldung des Arduinos, sonst leer"""
        try:
            return [int(x) for x in (self.ctrl.max_ledcnt_list or [])]
        except (TypeError, ValueError, AttributeError):
            return []

    def channel_max(self):
        leds = self.leds_per_channel()
        return max(0, len(leds) - 1) if leds else self.definition("ServoLEDChannel")[2]

    def address_max(self, channel=None):
        leds = self.leds_per_channel()
        channel = self.channel if channel is None else channel
        return leds[channel] if leds and 0 <= channel < len(leds) else self.definition("ServoAddress")[2]

    def _persist(self, key, value):
        try:
            self.ctrl.setConfigData(key, value)
            self.ctrl.SaveConfigData()
        except Exception:                                          # noqa: BLE001
            logger.debug("Wert %s nicht gesichert", key, exc_info=True)

    # ---- Anzeige (ResetButtons, SetLabelText, EnableControl_Buttons ...)
    def reset_buttons(self):
        """ResetButtons: zurueck in den Zustand Einstellen"""
        self.min_max_active = False
        self.prog_step = 0
        self.description = TEXT_DEFAULT
        self.description_color = COLOR_DEFAULT
        self.arrows_visible = False                 # VisibilityControl_Buttons False: Regler statt Pfeiltasten
        self.control_mode = ""                      # TxtControlMode (Minimalposition ...), nur bei aktiven Pfeiltasten sichtbar
        self.action_text, self.action_visible = BUTTON_START, True
        self.action2_text = BUTTON2_RESET
        self.cancel_text = BUTTON_CONNECT  # v2.02
        self.fields_enabled = True                  # EnableAdressSelection True
        self.active_button = 0
        self.release_pending = False

    def _enter_step(self, step, text, mode, action_text=None):
        self.prog_step = step
        self.description, self.description_color = text, COLOR_STEP
        self.control_mode = mode
        if action_text is not None:
            self.action_text = action_text

    # ---- Senden (SendValue, SendValueToCurrent, SendSelectCurrentModule)
    def get_current_address(self):
        return int(self.ctrl.get_lednum_offset_for_channel(self.channel)) + self.address

    def send_value(self, address, module, value):
        """SendValue: Wert an einen der drei Anschluesse (0, 1, 2); sonst nichts"""
        if module not in (0, 1, 2):
            return None
        values = [0, 0, 0]
        values[module] = value
        if self.ctrl.mobaledlib_version == 1:
            message = "#L" + "{:02x}".format(address)
        else:
            message = "#L " + "{:04x}".format(address)
        message += " " + " ".join("{:02x}".format(v) for v in values) + " " + "{:02x}".format(1) + "\n"
        self.ctrl.send_to_ARDUINO_servo(message)
        return message

    def send_value_to_current(self, value):
        return self.send_value(self.get_current_address(), self.module, value)

    def send_select_current_module(self):
        return self.send_value_to_current(SRV_SEL_LED.get(self.module, SRV_SEL_LED[0]))

    def send_keep_alive(self):
        """SendKeepAlive: LED 0 mit Farbe 0 und Anzahl 0 (haelt den Direktmodus), nur wenn nichts anderes gesendet wird"""
        idle = getattr(self.ctrl, "tx_idle", None)
        if idle is not None and not idle():
            return None
        message = "#L 0 0 0 0 0\n" if self.ctrl.mobaledlib_version != 1 else "#L00 00 00 00 00\n"
        self.ctrl.send_to_ARDUINO(message)
        return message

    # ---- Wackeln (StartWig, StopWig)
    def start_wig(self):
        if self.position != SRV_WIGG_MIN:               # ScrollBarPosition.value = SRV_WIGG_MIN loest Change aus (Position senden)
            self.position = SRV_WIGG_MIN
            self.position_changed()
        self.wig_time = self.now() + SRV_WIGG_FIRST
        self.wig_count = SRV_WIGG_COUNT

    def stop_wig(self):
        self.wig_count = 0

    # ---- Wahl von LED Nummer, Anschluss, LED Kanal (AddressChanged, ModuleChanged, ChannelChanged)
    def reset_position(self):
        """ResetPostition: im VBA-Code ohne Wirkung (SendValue bekommt die Position als Anschluss und sendet dann nichts)"""
        return None

    def _check_end_settings(self):
        if self.min_max_active:                         # CheckEndSettings
            self.reset_buttons()

    def address_changed(self, address):
        self.reset_position()
        self.address = max(0, min(self.address_max(), _to_int(address, self.address)))
        self._persist("ServoAddress", self.address)
        self._check_end_settings()
        self.send_select_current_module()
        self.start_wig()
        return self.address

    def module_changed(self, module):
        self.reset_position()
        self.module = max(0, min(2, _to_int(module, self.module)))
        self._persist("ServoChannel", self.module)
        self._check_end_settings()
        self.send_select_current_module()
        self.start_wig()
        return self.module

    def channel_changed(self, channel):
        self.reset_position()
        self.channel = max(0, min(self.channel_max(), _to_int(channel, self.channel)))
        self._persist("ServoLEDChannel", self.channel)
        return self.address_changed(min(self.address, self.address_max()))              # LED Nummer in den neuen Kanal einpassen

    # ---- Regler (ScrollBarPosition_Change)
    def position_changed(self):
        """Die Position hat sich geaendert (Regler, Pfeile am Regler, Wackeln): Wackeln beenden und den Wert senden"""
        self.stop_wig()
        return self.send_value(self.get_current_address(), self.module, self.position)

    def set_position(self, position):
        self.position = max(SERVO_SCALE_MIN, min(SERVO_SCALE_MAX, _to_int(position, self.position)))
        return self.position_changed()

    # ---- Pfeiltasten beim Konfigurieren (Minus_Button_MouseDown ... Plus2_Button_MouseUp)
    def arrow_press(self, name):
        if self.busy or not self.min_max_active or name not in ARROWS:
            return
        start, step = ARROWS[name]
        self.pressed = name
        self.min_max_value, self.active_button = start, step
        self.ticks_since_press = 0
        self.release_pending = False

    def arrow_release(self, name):
        if self.pressed != name:                        # nicht gedrueckt oder schon losgelassen: nicht noch einmal
            return
        self.pressed = None
        if self.ticks_since_press == 0:                 # WaitTimerTriggered: mindestens einen Zeitgeber-Schritt abwarten
            self.release_pending = True
        else:
            self.active_button = 0

    # ---- Zeitgeber (OnTimer), alle 100 ms
    def on_timer(self):
        if self.busy:
            return None
        if not self.min_max_active:
            if self.wig_count > 0 and self.now() >= self.wig_time:
                self.wig_count -= 1
                if self.wig_count == 0:                 # ResetPostition: ohne Wirkung
                    return None
                value = SRV_WIGG_MIN if self.wig_count % 2 == 0 else SRV_WIGG_MAX
                self.wig_time = self.now() + SRV_WIGG_TIME
                return self.send_value(self.get_current_address(), self.module, value)
            return self.send_keep_alive()
        if self.active_button == 0:
            self.min_max_value = SRV_POS_DEFAULT
        else:
            self.min_max_value += self.active_button
            if self.min_max_value < LIMIT_LOW:
                self.min_max_value = LIMIT_LOW
                if self.last_value == self.min_max_value:
                    self.min_max_value += 1
            if self.min_max_value > LIMIT_HIGH:
                self.min_max_value = LIMIT_HIGH
                if self.last_value == self.min_max_value:
                    self.min_max_value -= 1
        message = self.send_value_to_current(self.min_max_value)
        self.last_value = self.min_max_value
        self.ticks_since_press += 1
        if self.release_pending:
            self.active_button = 0
            self.release_pending = False
        return message

    # ---- Ablaeufe mit Pausen
    def _begin(self):  # v2.03
        """Sperre fuer einen Ablauf mit Pausen. Rueckgabe: seine Kennung (epoch) oder None, wenn schon einer laeuft"""  # v2.03
        if self.busy:  # v2.03
            return None  # v2.03
        self.busy = True  # v2.03
        return self._epoch  # v2.03

    def _end(self, epoch):  # v2.03
        if epoch == self._epoch:                       # nach einem Abbruch hat leave() die Sperre schon aufgehoben (und evtl. laeuft ein neuer Ablauf)  # v2.03
            self.busy = False  # v2.03

    async def _pause(self, epoch):  # v2.03
        await self.sleep(SRV_WAIT_TIME_CMD)
        if epoch != self._epoch:                       # der Reiter oder die Seite wurde verlassen: nichts mehr senden  # v2.03
            raise _Aborted()  # v2.03

    async def _send_pause(self, value, epoch):  # v2.03
        self.send_value_to_current(value)
        await self._pause(epoch)  # v2.03

    async def action(self):
        """Taste Servo Konfigurieren / Weiter (Action_Button_Click)"""
        if self.prog_step == 0:
            return await self.set_min()
        if self.prog_step == 1:
            return await self.set_max()
        if self.prog_step == 2:
            return await self.set_speed()

    async def set_min(self):
        epoch = self._begin()  # v2.03
        if epoch is None:  # v2.03
            return False
        try:
            self.stop_wig()
            self.arrows_visible = True
            self.fields_enabled = False
            self.action2_text = BUTTON2_SAVE
            self._enter_step(1, text_min(), "Minimalposition", BUTTON_NEXT)  # v2.06
            self.cancel_text = BUTTON_NO_SAVE
            self.min_max_active = True                  # EnableControl_Buttons True
            self.send_select_current_module()
            await self._pause(epoch)  # v2.03
            await self._send_pause(SRV_MIN_MAX, epoch)  # v2.03
            await self._send_pause(SRV_SPECIAL, epoch)  # v2.03
            self.min_max_value = SRV_POS_DEFAULT
            return True
        except _Aborted:  # v2.03
            return False  # v2.03
        finally:
            self._end(epoch)  # v2.03

    async def set_max(self):
        epoch = self._begin()  # v2.03
        if epoch is None:  # v2.03
            return False
        try:
            self._enter_step(2, text_max(), "Maximalposition")  # v2.06
            await self._send_pause(SRV_BUTTON1, epoch)  # v2.03
            return True
        except _Aborted:  # v2.03
            return False  # v2.03
        finally:
            self._end(epoch)  # v2.03

    async def set_speed(self):
        epoch = self._begin()  # v2.03
        if epoch is None:  # v2.03
            return False
        try:
            self._enter_step(3, TEXT_SPEED, "Geschwindigkeit")
            self.action_visible = False
            await self._send_pause(SRV_BUTTON1, epoch)  # v2.03
            await self._send_pause(SRV_SPEED, epoch)  # v2.03
            await self._send_pause(SRV_SPECIAL, epoch)  # v2.03
            self.min_max_active = True
            return True
        except _Aborted:  # v2.03
            return False  # v2.03
        finally:
            self._end(epoch)  # v2.03

    async def _save_steps(self, epoch):  # v2.03
        """Save_Button_Click (ohne die Sperre): die Befehle zum Speichern, dann zurueck in den Zustand Einstellen"""
        if self.prog_step == 1:
            await self._send_pause(SRV_BUTTON1, epoch)  # v2.03
            await self._send_pause(SRV_POS_DEFAULT, epoch)  # v2.03
        if self.prog_step in (1, 2):
            await self._send_pause(SRV_BUTTON1, epoch)  # v2.03
        if self.prog_step == 3:
            await self._send_pause(SRV_BUTTON1, epoch)  # v2.03
        self.reset_buttons()
        await self._send_pause(SRV_SPECIAL, epoch)  # v2.03
        await self._send_pause(SRV_FINISH, epoch)  # v2.03
        self.send_value_to_current(0)
        self.position_changed()                         # ScrollBarPosition_Change: die Position des Reglers senden
        self.start_wig()

    async def save(self):
        """Taste Einstellungen speichern (in jedem Schritt moeglich)"""
        epoch = self._begin()  # v2.03
        if epoch is None:  # v2.03
            return False
        try:
            self.pressed = None
            await self._save_steps(epoch)  # v2.03
            return True
        except _Aborted:  # v2.03
            return False  # v2.03
        finally:
            self._end(epoch)  # v2.03

    async def reset_servo(self):
        """Servo zurücksetzen (die Rueckfrage stellt die Anzeige): Grundeinstellungen senden (Limits 55 und 110, Geschwindigkeit 58), dann speichern"""
        epoch = self._begin()  # v2.03
        if epoch is None:  # v2.03
            return False
        try:
            self.stop_wig()
            self.send_select_current_module()
            await self._pause(epoch)  # v2.03
            await self._send_pause(SRV_MIN_MAX, epoch)  # v2.03
            await self._send_pause(SRV_DEFAULT_MIN_POS, epoch)  # v2.03
            await self._send_pause(SRV_DEFAULT_MAX_POS, epoch)  # v2.03
            await self._send_pause(SRV_SPEED, epoch)  # v2.03
            await self._send_pause(SRV_DEFAULT_SPEED, epoch)  # v2.03
            await self._save_steps(epoch)  # v2.03
            self.start_wig()
            return True
        except _Aborted:  # v2.03
            return False  # v2.03
        finally:
            self._end(epoch)  # v2.03

    async def cancel_config(self):
        """nicht speichern: das Konfigurieren beenden (Cancel_Button_Click bei prog_step <> 0)"""
        epoch = self._begin()  # v2.03
        if epoch is None:  # v2.03
            return False
        try:
            self.pressed = None
            self.reset_buttons()
            self.send_value_to_current(0)
            await self._pause(epoch)  # v2.03
            self.position_changed()
            self.start_wig()
            return True
        except _Aborted:  # v2.03
            return False  # v2.03
        finally:
            self._end(epoch)  # v2.03

    # ---- Seite betreten und verlassen
    def connected(self):  # v2.02
        """Ist die Verbindung zum Arduino offen?"""  # v2.02
        try:  # v2.02
            return bool(self.ctrl.is_connection_open())  # v2.02
        except Exception:                                          # noqa: BLE001  # v2.02
            return False

    def tab_selected(self):
        """ShowDialog: Direktmodus starten, den Zustand Einstellen herstellen, den Servo waehlen und wackeln lassen"""
        _SEQ[0] += 1  # v2.03
        ACTIVE_MODELS[self] = _SEQ[0]  # v2.03
        try:
            self.ctrl.ARDUINO_begin_direct_mode()
        except Exception:                                          # noqa: BLE001
            logger.warning("Direktmodus konnte nicht gestartet werden", exc_info=True)
        self.busy = False
        self.pressed = None
        self.reset_buttons()
        if self.address == 0 and (self.leds_per_channel() or [0])[0] > 1:          # die Heartbeat-LED ueberspringen
            self.address = 1
        self.channel_changed(self.channel)

    def leave(self, quiet=False):  # v2.03
        """Reiter oder Seite verlassen (Reiter gewechselt, Browser geschlossen oder neu geladen, Verbindung weg, Programm beendet): laufende Ablaeufe abbrechen,
        Pfeiltaste loslassen, Wert 0 an den Servo senden (wie Abort_Button_Click im Excel-Dialog), Direktmodus beenden. So bleibt nichts haengen.
        Nur einmal: ein zweiter Aufruf (Reiter verlassen, danach Seite geschlossen) sendet nichts mehr. Hat inzwischen eine NEUERE Seite den Servo uebernommen
        (zum Beispiel nach dem Neuladen im Browser, das alte Fenster meldet sich erst spaeter ab), wird nichts gesendet, um sie nicht zu stoeren.
        quiet: nur aufraeumen, nichts senden."""
        self._epoch += 1  # v2.03
        self.busy = False  # v2.03
        mine = ACTIVE_MODELS.pop(self, None)  # v2.03
        self.stop_wig()  # v2.03
        self.pressed = None  # v2.03
        self.active_button = 0  # v2.03
        self.release_pending = False  # v2.03
        try:
            newer = mine is not None and any(number > mine for number in ACTIVE_MODELS.values())  # v2.03
            if mine is not None and not newer and not quiet:  # v2.03
                self.send_value_to_current(0)  # v2.03
                self.ctrl.ARDUINO_end_direct_mode()  # v2.03
        except Exception:                                          # noqa: BLE001
            logger.warning("Servo Test beim Verlassen nicht sauber beendet", exc_info=True)
        self.reset_buttons()  # v2.03

    tab_unselected = leave  # v2.03


# --------------------------------------------------------------------------- Oberflaeche (NiceGUI)
class ServoPage:
    """Rueckgabe von build: tab_selected(), tab_unselected(), model"""

    def __init__(self, model, refresh, timer):
        self.model = model
        self._refresh = refresh
        self._timer = timer

    def tab_selected(self):
        self.model.tab_selected()
        self._timer.active = True
        self._refresh()

    def tab_unselected(self):
        self._timer.active = False
        self.model.leave()  # v2.03
        self._refresh()

    def on_connected(self):  # v2.04
        """Die Verbindung zum Arduino wurde hergestellt (Taste "Mit ARDUINO verbinden" oder Menue): Direktmodus starten und den Servo waehlen"""  # v2.04
        if self.model.connected():  # v2.04
            self.model.tab_selected()  # v2.04
            self._timer.active = True  # v2.04
        self._refresh()  # v2.04

    def page_closed(self):  # v2.03
        """Der Browser hat die Seite verlassen (geschlossen, neu geladen, Verbindung weg): Wert 0 senden, nichts mehr in die Anzeige schreiben"""  # v2.03
        self._timer.active = False  # v2.03
        self.model.leave()  # v2.03


async def _confirm_dialog(title, text):
    from nicegui import ui
    with ui.dialog() as dlg, ui.card().classes("w-[460px] max-w-full"):
        ui.label(title).classes("text-h6")
        ui.label(text)
        with ui.row().classes("justify-end w-full"):
            ui.button("Nein", on_click=lambda: dlg.submit(False)).props("flat no-caps")
            ui.button("Ja", on_click=lambda: dlg.submit(True)).props("color=primary no-caps")
    answer = await dlg
    dlg.delete()
    return bool(answer)


def build(ctrl, is_active=None, connect=None, confirm=None):  # v2.02
    """Baut die Seite "Servo Test 1" in den aktuellen Container.
    is_active: liefert True, solange die Seite sichtbar ist. connect: die Funktion des Menuepunkts ARDUINO -> Verbinden (async, ohne Argumente), die dritte Taste im
    Zustand Einstellen ruft sie auf. confirm: Rueckfrage (async, Titel, Text -> True/False); Voreinstellung ist ein Dialog."""
    from nicegui import ui

    model = ServoModel(ctrl)
    confirm = confirm or _confirm_dialog
    ui.add_head_html("<style>" + CSS + "</style>")
    refs: dict = {}

    def current(key):
        return {"ServoAddress": model.address, "ServoLEDChannel": model.channel, "ServoChannel": model.module}[key]

    desc = {"open": False}                              # Beschreibung aufgeklappt? (bleibt ueber die Schritte erhalten)  # v2.01

    def refresh_description():  # v2.01
        """Beschreibung: zugeklappt nur die erste Zeile (Smartphone), aufgeklappt der ganze Text"""  # v2.01
        opened = desc["open"]  # v2.01
        refs["description"].set_text(model.description if opened else model.description.split("\n")[0])  # v2.01
        shape = "white-space: pre-line; overflow: visible; text-overflow: clip" if opened else "white-space: nowrap; overflow: hidden; text-overflow: ellipsis"  # v2.01
        refs["description"].style(f"background: {model.description_color}; padding: 6px 10px; border: 1px solid #aaa; min-width: 0; {shape}")  # v2.01
        refs["desc_toggle"].props(f"icon={'expand_less' if opened else 'expand_more'}")  # v2.01

    def toggle_description(_=None):  # v2.01
        desc["open"] = not desc["open"]  # v2.01
        refresh_description()  # v2.01

    def refresh():
        refresh_description()  # v2.01
        refs["guard"] = True                            # die Felder aendern sich durch das Programm, nicht durch den Anwender: kein Servo waehlen, nicht wackeln
        try:
            for key, field in refs["fields"].items():
                field.set_value(current(key))
                field.set_enabled(model.fields_enabled)
        finally:
            refs["guard"] = False
        refs["slider_row"].set_visibility(not model.arrows_visible)
        refs["arrow_row"].set_visibility(model.arrows_visible)
        refs["slider"].set_value(model.position)
        refs["position"].set_text(str(model.position))
        refs["mode"].set_text(model.control_mode)
        refs["action"].set_text(model.action_text)
        refs["action"].style("visibility: visible" if model.action_visible else "visibility: hidden")          # der Platz bleibt (wie im Excel-Dialog)  # v2.01
        refs["action2"].set_text(model.action2_text)
        refs["cancel"].set_text(model.cancel_text)
        refs["cancel"].set_visibility(model.prog_step != 0)                  # nur beim Konfigurieren (nicht speichern); verbunden wird in der Kopfzeile  # v2.04

    def tick():
        if is_active is not None and not is_active():
            return
        model.on_timer()

    def field_changed(key, value):
        if value is None or refs.get("guard") or _to_int(value, current(key)) == current(key):          # leer, vom Programm gesetzt oder unveraendert
            return
        refs["guard"] = True
        try:
            {"ServoAddress": model.address_changed, "ServoLEDChannel": model.channel_changed, "ServoChannel": model.module_changed}[key](value)
            refresh()
        finally:
            refs["guard"] = False

    def on_slide(e):
        args = e.args
        value = args[0] if isinstance(args, (list, tuple)) and args else args
        model.set_position(value)
        refs["position"].set_text(str(model.position))

    def step_slider(delta):
        model.set_position(model.position + delta)
        refs["slider"].set_value(model.position)
        refs["position"].set_text(str(model.position))

    async def on_action():
        await model.action()
        refresh()

    async def on_action2():
        if model.prog_step == 0:
            if not await confirm(CONFIRM_RESET_TITLE, CONFIRM_RESET_TEXT):
                return
            await model.reset_servo()
        else:
            await model.save()
        refresh()

    # async def on_connect():  # v2.04 (entfallen)
        # """Verbinden: wie ARDUINO -> Verbinden; danach den Direktmodus starten und den Servo waehlen (connect meldet nur EFFECT Mode)"""  # v2.04 (entfallen)
        # if connect is not None:  # v2.04 (entfallen)
            # await connect()  # v2.04 (entfallen)
        # if model.connected():  # v2.04 (entfallen)
            # model.tab_selected()  # v2.04 (entfallen)
        # refresh()  # v2.04 (entfallen)
    async def on_cancel():
        # if model.prog_step == 0:                        # Zustand Einstellen: die Taste verbindet  # v2.04 (entfallen)
            # await on_connect()  # v2.04 (entfallen)
        if model.prog_step == 0:                        # Zustand Einstellen: die Taste ist ausgeblendet (verbunden wird mit der Taste "Mit ARDUINO verbinden" in der Kopfzeile)  # v2.04
            return  # v2.02
        await model.cancel_config()                     # nicht speichern  # v2.02
        refresh()

    def arrow_button(name):
        button = ui.button(ARROW_LABELS[name]).props("outline no-caps").classes("mll-servo-btn mll-servo-arrow").style("font-size: 20px")
        # button.tooltip(f"Wert {ARROWS[name][0]}, danach {ARROWS[name][1]:+d} je 100 ms")  # v2.05 (entfallen)
        button.tooltip(tr('Wert {pfeil}, danach {schritt:+d} je 100 ms', pfeil=ARROWS[name][0], schritt=ARROWS[name][1]))  # v2.05
        button.on("pointerdown", lambda e, n=name: model.arrow_press(n))
        for event in ("pointerup", "pointercancel", "pointerleave"):       # auch wenn der Finger abrutscht: immer loslassen
            button.on(event, lambda e, n=name: model.arrow_release(n))
        return button

    with ui.column().classes("w-full items-stretch gap-3 mll-servo"):
        ui.label("Servo Test und Einstellung").classes("text-h6")
        with ui.row().classes("w-full items-center no-wrap gap-1 mll-servo-desc"):  # v2.01
            refs["description"] = ui.label(model.description).classes("grow").tooltip("Antippen zum Auf- und Zuklappen")  # v2.01
            refs["description"].on("click", toggle_description)  # v2.01
            refs["desc_toggle"] = ui.button(icon="expand_more", on_click=toggle_description).props("flat dense round")  # v2.01
        with ui.card().props("flat bordered").classes("w-full"):
            with ui.row().classes("w-full items-end gap-2 mll-servo-fields"):  # v2.01
                ui.label("Servo Modul Auswahl").classes("text-caption mll-servo-caption")          # in der Zeile der Felder, vor LED Nummer  # v2.01
                refs["fields"] = {}
                for key in ("ServoAddress", "ServoChannel", "ServoLEDChannel"):             # Reihenfolge wie im Excel-Dialog: LED Nummer, Anschluss, LED Kanal
                    text, lo, hi, _, hint = model.definition(key)
                    field = ui.number(label=text, value=current(key), min=lo, max=hi, step=1, precision=0,
                                      on_change=lambda e, k=key: field_changed(k, e.value)).props("dense outlined").classes("mll-servo-field")  # v2.01
                    field.tooltip(hint)
                    refs["fields"][key] = field
        with ui.row().classes("w-full items-center no-wrap gap-2") as slider_row:
            left = ui.button(icon="chevron_left", on_click=lambda: step_slider(-1)).props("outline").classes("mll-servo-wide")
            left.tooltip("Position um 1 verringern")
            slider = ui.slider(min=SERVO_SCALE_MIN, max=SERVO_SCALE_MAX, step=1, value=model.position).props("label markers=20").classes("grow")
            slider.tooltip("Position des Servos 10..210. Mit den Pfeiltasten Schritt für Schritt, Pos1 und Ende springen an den Anfang und das Ende.")
            slider.on("update:model-value", on_slide, throttle=SERVO_RATE)
            right = ui.button(icon="chevron_right", on_click=lambda: step_slider(1)).props("outline").classes("mll-servo-wide")
            right.tooltip("Position um 1 erhöhen")
            refs["position"] = ui.label(str(model.position)).style("min-width: 3em; text-align: right")
        refs["slider_row"], refs["slider"] = slider_row, slider
        with ui.row().classes("w-full items-center justify-center no-wrap gap-2") as arrow_row:
            arrow_button("minus2")
            arrow_button("minus1")
            refs["mode"] = ui.label(model.control_mode).classes("text-h6 text-center").style("min-width: 9em; flex: 1 1 auto")
            arrow_button("plus1")
            arrow_button("plus2")
        refs["arrow_row"] = arrow_row
        with ui.row().classes("w-full items-stretch no-wrap gap-2 mll-servo-actions"):                  # die drei Tasten in einer Zeile (Einstellen und Konfigurieren)  # v2.01
            refs["action"] = ui.button(model.action_text, on_click=on_action).props("outline no-caps").classes("mll-servo-action")  # v2.01
            refs["action2"] = ui.button(model.action2_text, on_click=on_action2).props("outline no-caps").classes("mll-servo-action")  # v2.01
            refs["cancel"] = ui.button(model.cancel_text, on_click=on_cancel).props("outline no-caps").classes("mll-servo-action")  # v2.01
            # refs["cancel"].tooltip("Verbinden: wie ARDUINO → Verbinden. Beim Konfigurieren: nicht speichern")  # v2.04 (entfallen)
            refs["cancel"].tooltip("Nicht speichern")  # v2.04
    timer = ui.timer(TICK, tick)
    timer.active = False
    refresh()
    return ServoPage(model, refresh, timer)
