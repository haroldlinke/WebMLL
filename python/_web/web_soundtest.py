# Datei-Version: 1.01 (2026-10-21) - web_soundtest.py
# ----------------------------------------------------------------------------------------------
# Name:           web_soundtest.py
# Path:           _web/web_soundtest.py
# Version:        1.01
# Last Update:    2026-10-21
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-21  Neu: Reiter Sound Test (mlpyproggen/SoundCheckPage.py ohne Tk): Adresse, LED Kanal, Impulslaenge, R/G/B, Senden mit Impuls, Direktmodus
#   1.01  2026-10-21  Die Taste Verbinden entfaellt: verbunden wird mit der Taste Mit ARDUINO verbinden in der Kopfzeile fuer alle Reiter; neu SoundPage.on_connected (Direktmodus nach dem Verbinden)
# ----------------------------------------------------------------------------------------------
"""Web-Version der Seite "Sound Test" (mlpyproggen/SoundCheckPage.py, Klasse SoundCheckPage, ohne Tk).

Testet die MLL-Soundplatine (MP3-TF-16): Welcher Ton kommt, haengt von den drei Farbwerten R, G, B der LED des Soundmoduls ab. Die Seite schickt
  #L <Adresse> <R> <G> <B> 01      (Version 2: Adresse mit 4 Hex-Ziffern, Version 1: #L<Adresse mit 2 Hex-Ziffern>)
und nach der Impulslaenge (ms)
  #L <Adresse> 00 00 00 01
Adresse = Soundmodul-Adresse plus Versatz des LED-Kanals. Die Werte Adresse, Impulslaenge, R, G und B schicken beim Aendern gleich (ValueChangeEvent im Original),
der LED Kanal nicht; die Taste schickt immer.

Unterschiede zum Tk-Original (siehe HOC_intern.md, Version 1.95):
  * Beim Tippen in ein Feld wird erst 300 ms nach der letzten Eingabe gesendet (sonst ginge fuer 120 je ein Kommando fuer 1, 12 und 120 an die Platine).
  * Das Kommando zum Beenden des Impulses geht an dieselbe Adresse wie das Kommando zum Starten, auch bei Version 1 und einem LED Kanal ungleich 0 (das Original nahm
    bei Version 1 die Adresse ohne Versatz des Kanals) und nicht an die Adresse, die beim Ablauf der Zeit gerade im Feld steht.
  * Beim Verlassen des Reiters, beim Schliessen oder Neuladen der Seite und beim Beenden des Programms wird ein noch laufender Impuls sofort beendet (das Original liess ihn
    laufen: nach dem Verlassen kam das Ende nicht mehr, wenn die Seite weg war).
  * Die Tastenkuerzel Strg-R und Alt-R fuer den Rotwert gibt es nicht (Strg-R laedt im Browser die Seite neu).
  * Verbunden wird mit dem Knopf Mit ARDUINO verbinden in der Kopfzeile (fuer alle Reiter); die Tk-Seite verband nicht selbst. Danach startet die Seite den Direktmodus (SoundPage.on_connected).
"""
from __future__ import annotations

import asyncio
import logging

logger = logging.getLogger(__name__)

SEND_DELAY = 0.3                       # Sekunden Ruhe nach der letzten Eingabe, bevor gesendet wird (debounce)
PARAMS = ("Sound_Address", "SoundLEDChannel", "Sound_ImpulsLength", "Sound_RED", "Sound_GREEN", "Sound_BLUE")      # ParName / ConfigName der Werte
DEFINITION_KEYS = {"Sound_Address": "SoundAddress", "SoundLEDChannel": "SoundLEDChannel", "Sound_ImpulsLength": "SoundImpulsLength",
                   "Sound_RED": "Sound_RED", "Sound_GREEN": "Sound_GREEN", "Sound_BLUE": "Sound_BLUE"}               # ParName -> Schluessel in MacroParamDef
DEFAULTS = {                           # (Text, Min, Max, Vorgabe, Hinweis) falls MacroParamDef fehlt
    "Sound_Address": ("Soundmodul-Adresse", 0, 32767, 0, "Adresse des Soundmoduls"),
    "SoundLEDChannel": ("LED Kanal", 0, 99, 0, "LED Kanal an dem die Soundplatine angeschlossen ist"),
    "Sound_ImpulsLength": ("Impulslänge", 0, 1200, 0, "Länge des Impulses"),
    "Sound_RED": ("Sound Anschluss R", 0, 255, 0, "Sound Anschluss R"),
    "Sound_GREEN": ("Sound Anschluss G", 0, 255, 0, "Sound Anschluss G"),
    "Sound_BLUE": ("Sound Anschluss B", 0, 255, 0, "Sound Anschluss B"),
}
SEND_ON_CHANGE = ("Sound_Address", "Sound_ImpulsLength", "Sound_RED", "Sound_GREEN", "Sound_BLUE")          # ValueChangeEvent im Original

CSS = """
.mll-sound { max-width: 760px; margin: 0 auto; padding: 8px; }
.mll-sound-desc { cursor: pointer; }
.mll-sound-field { flex: 1 1 0; min-width: 84px; }
.mll-sound-send { min-height: 72px; flex: 1 1 0; }
"""

ACTIVE_MODELS: dict = {}               # Modelle der Seiten mit offenem Reiter -> laufende Nummer ihres Betretens
_SEQ = [0]


def _to_int(value, default=0):
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def stop_all(wait=False):
    """Fuer alle Seiten mit offenem Reiter: laufende Impulse beenden, Direktmodus beenden (Programm wird beendet oder neu gestartet)"""
    models = sorted(ACTIVE_MODELS, key=lambda m: ACTIVE_MODELS[m], reverse=True)
    for index, model in enumerate(models):
        ctrl = model.ctrl
        model.leave(quiet=index > 0)
        if wait:
            try:
                ctrl._wait_sent(1.0)
            except Exception:                                      # noqa: BLE001
                pass


class SoundModel:
    """Logik der Seite, ohne Browser testbar. later(Sekunden, Funktion) plant einen Aufruf und liefert ein Objekt mit cancel()."""

    def __init__(self, ctrl, later=None):
        self.ctrl = ctrl
        self.later = later or (lambda delay, fn: asyncio.get_running_loop().call_later(delay, fn))
        self.values = {key: self._clamp(key, self._stored(key)) for key in PARAMS}
        self.values["SoundLEDChannel"] = min(self.values["SoundLEDChannel"], self.channel_max())
        self.pending: dict = {}          # laufende Impulse: Adresse der LED -> Haltepunkt zum Abbrechen des geplanten Endes (Liste, mehrere moegliche)

    # ---- Parameter
    def definition(self, key):
        d = {}
        try:
            d = self.ctrl.MacroParamDef.data.get(DEFINITION_KEYS[key], {}) or {}
        except AttributeError:
            pass
        text, lo, hi, default, hint = DEFAULTS[key]
        return (d.get("Input Text") or text, _to_int(d.get("Min"), lo), _to_int(d.get("Max"), hi), _to_int(d.get("Default"), default), d.get("Hint") or hint)

    def _stored(self, key):
        try:
            value = self.ctrl.getConfigData(key)
        except Exception:                                          # noqa: BLE001
            value = ""
        return value if value not in ("", None) else self.definition(key)[3]

    def _clamp(self, key, value):
        _, lo, hi, default, _ = self.definition(key)
        return max(lo, min(hi, _to_int(value, default)))

    def leds_per_channel(self):
        try:
            return [int(x) for x in (self.ctrl.max_ledcnt_list or [])]
        except (TypeError, ValueError, AttributeError):
            return []

    def channel_max(self):
        leds = self.leds_per_channel()
        return max(0, len(leds) - 1) if leds else self.definition("SoundLEDChannel")[2]

    def set_value(self, key, value):
        """Wert uebernehmen (begrenzt) und merken"""
        if key == "SoundLEDChannel":
            self.values[key] = max(0, min(self.channel_max(), _to_int(value, self.values[key])))
        else:
            self.values[key] = self._clamp(key, value)
        try:
            self.ctrl.setConfigData(key, self.values[key])
            self.ctrl.SaveConfigData()
        except Exception:                                          # noqa: BLE001
            logger.debug("Wert %s nicht gesichert", key, exc_info=True)
        return self.values[key]

    def sound_address(self):
        """LED-Nummer: Soundmodul-Adresse plus Versatz des LED-Kanals"""
        return self.values["Sound_Address"] + int(self.ctrl.get_lednum_offset_for_channel(self.values["SoundLEDChannel"]))

    # ---- Nachrichten
    def message(self, address, red, green, blue):
        if self.ctrl.mobaledlib_version == 1:
            return "#L" + "{:02x}".format(address) + " " + "{:02x}".format(red) + " " + "{:02x}".format(green) + " " + "{:02x}".format(blue) + " " + "{:02x}".format(1) + "\n"
        return "#L " + "{:04x}".format(address) + " " + "{:02x}".format(red) + " " + "{:02x}".format(green) + " " + "{:02x}".format(blue) + " " + "{:02x}".format(1) + "\n"

    def send_sound(self):
        """Sound an den ARDUINO schicken und das Ende des Impulses planen (_send_sound_to_ARDUINO). Rueckgabe: die gesendete Zeile"""
        address = self.sound_address()
        line = self.message(address, self.values["Sound_RED"], self.values["Sound_GREEN"], self.values["Sound_BLUE"])
        self.ctrl.send_to_ARDUINO(line)
        handle_box = []

        def stop():
            self._forget(address, handle_box)
            self.stop_impulse(address)
        handle = self.later(self.values["Sound_ImpulsLength"] / 1000.0, stop)
        handle_box.append(handle)
        self.pending.setdefault(address, []).append(handle_box)
        return line

    def _forget(self, address, handle_box):
        boxes = self.pending.get(address, [])
        if handle_box in boxes:
            boxes.remove(handle_box)
        if not boxes:
            self.pending.pop(address, None)

    def stop_impulse(self, address):
        """Ende des Impulses (onstopImpuls): alle drei Werte 0"""
        line = self.message(address, 0, 0, 0)
        self.ctrl.send_to_ARDUINO(line)
        return line

    def changed(self, key, value):
        """Ein Feld wurde vom Anwender geaendert: uebernehmen, bei den Feldern mit ValueChangeEvent senden. Rueckgabe: die gesendete Zeile oder None."""
        before = self.values[key]
        self.set_value(key, value)
        if key in SEND_ON_CHANGE and self.values[key] != before:
            return self.send_sound()
        return None

    # ---- Seite betreten und verlassen
    def tab_selected(self):
        _SEQ[0] += 1
        ACTIVE_MODELS[self] = _SEQ[0]
        try:
            self.ctrl.ARDUINO_begin_direct_mode()
        except Exception:                                          # noqa: BLE001
            logger.warning("Direktmodus konnte nicht gestartet werden", exc_info=True)

    def connected(self):
        try:
            return bool(self.ctrl.is_connection_open())
        except Exception:                                          # noqa: BLE001
            return False

    def end_pending(self):
        """Noch laufende Impulse sofort beenden (geplante Enden abbrechen, je Adresse einmal Wert 0 senden)"""
        addresses = list(self.pending)
        for address in addresses:
            for box in self.pending.pop(address, []):
                for handle in box:
                    try:
                        handle.cancel()
                    except Exception:                              # noqa: BLE001
                        pass
            try:
                self.stop_impulse(address)
            except Exception:                                      # noqa: BLE001
                logger.warning("Ende des Impulses nicht gesendet", exc_info=True)

    def leave(self, quiet=False):
        """Reiter oder Seite verlassen: laufende Impulse beenden, Direktmodus beenden (nur einmal; hat eine NEUERE Seite uebernommen, bleibt der Direktmodus).
        quiet: nur aufraeumen, nichts senden."""
        mine = ACTIVE_MODELS.pop(self, None)
        if quiet:
            for boxes in self.pending.values():
                for box in boxes:
                    for handle in box:
                        try:
                            handle.cancel()
                        except Exception:                          # noqa: BLE001
                            pass
            self.pending.clear()
            return
        self.end_pending()
        try:
            newer = mine is not None and any(number > mine for number in ACTIVE_MODELS.values())
            if mine is not None and not newer:
                self.ctrl.ARDUINO_end_direct_mode()
        except Exception:                                          # noqa: BLE001
            logger.warning("Sound Test beim Verlassen nicht sauber beendet", exc_info=True)

    tab_unselected = leave


# --------------------------------------------------------------------------- Oberflaeche (NiceGUI)
class SoundPage:
    """Rueckgabe von build: tab_selected(), tab_unselected(), page_closed(), model"""

    def __init__(self, model, refresh):
        self.model = model
        self._refresh = refresh

    def tab_selected(self):
        self.model.tab_selected()
        self._refresh()

    def tab_unselected(self):
        self.model.leave()
        self._refresh()

    def on_connected(self):  # v1.01
        """Die Verbindung zum Arduino wurde hergestellt (Taste "Mit ARDUINO verbinden" oder Menue): Direktmodus starten"""  # v1.01
        if self.model.connected():  # v1.01
            self.model.tab_selected()  # v1.01
        self._refresh()  # v1.01

    def page_closed(self):
        """Der Browser hat die Seite verlassen: laufende Impulse beenden, nichts mehr in die Anzeige schreiben"""
        self.model.leave()


def build(ctrl, is_active=None, connect=None):
    """Baut die Seite "Sound Test" in den aktuellen Container. connect: die Funktion des Menuepunkts ARDUINO -> Verbinden (async, ohne Argumente)."""
    from nicegui import ui

    model = SoundModel(ctrl)
    macro = ctrl.MacroDef.data.get("SoundCheckPage", {}) if getattr(ctrl, "MacroDef", None) else {}
    title = macro.get("Title") or "Sound-Test"
    description = macro.get("Ausführliche Beschreibung") or macro.get("Kurzbeschreibung") or ""
    send_text = (macro.get("Button_1") or "Sound an ARDUINO schicken").replace("\n", " ")
    ui.add_head_html("<style>" + CSS + "</style>")
    refs: dict = {"fields": {}, "guard": False}
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

    def refresh():
        refresh_description()
        refs["guard"] = True                            # vom Programm gesetzt, nicht vom Anwender: nichts senden
        try:
            for key, field in refs["fields"].items():
                field.set_value(model.values[key])
        finally:
            refs["guard"] = False

    def field_changed(key, value):
        if value is None or refs["guard"] or _to_int(value, model.values[key]) == model.values[key]:
            return
        model.changed(key, value)
        refresh()

    def send_now():
        model.send_sound()

    # async def on_connect():  # v1.01 (entfallen)
        # if connect is not None:  # v1.01 (entfallen)
            # await connect()  # v1.01 (entfallen)
        # if model.connected():  # v1.01 (entfallen)
            # model.tab_selected()  # v1.01 (entfallen)
        # refresh()  # v1.01 (entfallen)
    def number(key):
        text, lo, hi, _, hint = model.definition(key)
        max_ = model.channel_max() if key == "SoundLEDChannel" else hi
        field = ui.number(label=text, value=model.values[key], min=lo, max=max_, step=1, precision=0,
                          on_change=lambda e, k=key: field_changed(k, e.value)).props("dense outlined debounce=300").classes("mll-sound-field")
        field.tooltip(hint)
        refs["fields"][key] = field
        return field

    with ui.column().classes("w-full items-stretch gap-3 mll-sound"):
        ui.label(title).classes("text-h6")
        with ui.row().classes("w-full items-center no-wrap gap-1 mll-sound-desc"):
            refs["description"] = ui.label(description).classes("grow").tooltip("Antippen zum Auf- und Zuklappen")
            refs["description"].on("click", toggle_description)
            refs["desc_toggle"] = ui.button(icon="expand_more", on_click=toggle_description).props("flat dense round")
        with ui.card().props("flat bordered").classes("w-full"):
            with ui.row().classes("w-full items-end no-wrap gap-2"):
                for key in ("Sound_Address", "SoundLEDChannel", "Sound_ImpulsLength"):
                    number(key)
            ui.label("Sound-Auswahl").classes("text-caption")
            with ui.row().classes("w-full items-end no-wrap gap-2"):
                for key in ("Sound_RED", "Sound_GREEN", "Sound_BLUE"):
                    number(key)
        with ui.row().classes("w-full items-stretch no-wrap gap-2"):
            # connect_button = ui.button("Verbinden", on_click=on_connect).props("outline no-caps").style("min-height: 72px; flex: 1 1 0")  # v1.01 (entfallen)
            # connect_button.tooltip("Verbinden: wie ARDUINO → Verbinden")  # v1.01 (entfallen)
            refs["send"] = ui.button(send_text, on_click=send_now).props("unelevated no-caps color=primary").classes("mll-sound-send")
    refresh()
    return SoundPage(model, refresh)
