# Datei-Version: 1.00 (2026-10-21) - web_dcckeyboard.py
# ----------------------------------------------------------------------------------------------
# Name:           web_dcckeyboard.py
# Path:           _web/web_dcckeyboard.py
# Version:        1.00
# Last Update:    2026-10-21
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-21  Neu: Reiter DCC Keyboard (mlpyproggen/DCC_KeyboardPage.py ohne Tk): 32 Schalter mit rotem und gruenem Knopf, Basisadresse, Kommando @ AAA CC 01
# ----------------------------------------------------------------------------------------------
"""Web-Version der Seite "DCC Keyboard" (mlpyproggen/DCC_KeyboardPage.py, Klasse DCCKeyboardPage, ohne Tk).

Der DCC-Keyboard-Simulator schickt dem ARDUINO direkt die Kommandos, die sonst der DCC-ARDUINO an den LED-ARDUINO schicken wuerde, damit man die Funktion der
DCC-Schalter ausprobieren kann:  @ AAA CC 01  (AAA: Adresse mit mindestens drei Stellen, CC: Kanal 00 = rot, 01 = gruen, danach ein Zeilenende).
32 Adressen (Basisadresse + 0 bis 31), je ein roter und ein gruener Knopf, in vier Gruppen zu acht.

Unterschiede zum Tk-Original (siehe HOC_intern.md, Version 1.95):
  * Das Kommando geht in einem Stueck an die serielle Schicht (sie sendet ohnehin Zeichen fuer Zeichen); das Original rief send_to_ARDUINO je Zeichen auf.
  * Wie im Original verbindet die Seite beim ersten Tastendruck selbst (connect_if_not_connected), im Hintergrund, damit die Oberflaeche nicht haengt. Gelingt das nicht,
    kommt eine Meldung; das Original schwieg.
  * Die Beschriftung der roten Knoepfe folgt der Basisadresse sofort (im Original erst nach dem naechsten Tastendruck).
"""
from __future__ import annotations

import asyncio
import logging

logger = logging.getLogger(__name__)

BASE_KEY = "DCC_BaseAddress"           # ConfigName der Basisadresse (wie im Original, Persistent)
BASE_MIN, BASE_MAX, BASE_DEFAULT = 1, 9999, 200
GROUPS, PER_GROUP = 4, 8               # vier Gruppen zu acht Schaltern

CSS = """
.mll-dcc { max-width: 760px; margin: 0 auto; padding: 8px; }
.mll-dcc-desc { cursor: pointer; }
.mll-dcc-group { display: grid; grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 4px; width: 100%; margin-bottom: 8px; }
.mll-dcc-btn { min-width: 0 !important; min-height: 44px; padding: 0 !important; font-size: 14px; }
"""


def _to_int(value, default=0):
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


class DCCModel:
    """Logik der Seite, ohne Browser testbar."""

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.base = self._clamp(self._stored())

    def definition(self):
        """(Text, Min, Max, Vorgabe, Hinweis) aus MacroParamDef, sonst die eingebauten Werte"""
        d = {}
        try:
            d = self.ctrl.MacroParamDef.data.get("DCC BaseAddress", {}) or {}
        except AttributeError:
            pass
        return (d.get("Input Text") or "DCC-Basisadresse", _to_int(d.get("Min"), BASE_MIN), _to_int(d.get("Max"), BASE_MAX), _to_int(d.get("Default"), BASE_DEFAULT),
                d.get("Hint") or "Basisadresse des DCC-Keyboards")

    def _stored(self):
        try:
            value = self.ctrl.getConfigData(BASE_KEY)
        except Exception:                                          # noqa: BLE001
            value = ""
        return value if value not in ("", None) else self.definition()[3]

    def _clamp(self, value):
        _, lo, hi, default, _ = self.definition()
        return max(lo, min(hi, _to_int(value, default)))

    def set_base(self, value):
        self.base = self._clamp(value)
        try:
            self.ctrl.setConfigData(BASE_KEY, self.base)
            self.ctrl.SaveConfigData()
        except Exception:                                          # noqa: BLE001
            logger.debug("Basisadresse nicht gesichert", exc_info=True)
        return self.base

    def address(self, index):
        """DCC-Adresse des Schalters index (0 bis 31)"""
        return self.base + index

    def command(self, index, channel):
        """Kommando @ AAA CC 01 (ohne Zeilenende), wie _button_cmd im Original"""
        return "@ {:03} {:02} 01".format(self.address(index), channel)

    def ensure_connected(self):
        """Mit dem ARDUINO verbinden, wenn noch nicht geschehen (blockiert bis zu einigen Sekunden: nicht im Event-Loop aufrufen). Rueckgabe: verbunden?"""
        try:
            return bool(self.ctrl.connect_if_not_connected())
        except Exception:                                          # noqa: BLE001
            logger.warning("Verbinden fehlgeschlagen", exc_info=True)
            return False

    def send(self, index, channel):
        """Kommando senden (die Verbindung muss stehen). Rueckgabe: die gesendete Zeile"""
        line = self.command(index, channel) + "\n"
        self.ctrl.send_to_ARDUINO(line)
        return line


class DCCPage:
    """Rueckgabe von build. Die Seite braucht weder Direktmodus noch Aufraeumen: tab_selected, tab_unselected und page_closed tun nichts."""

    def __init__(self, model, refresh):
        self.model = model
        self._refresh = refresh

    def tab_selected(self):
        self._refresh()

    def tab_unselected(self):
        pass

    def page_closed(self):
        pass


def build(ctrl, is_active=None):
    """Baut die Seite "DCC Keyboard" in den aktuellen Container."""
    from nicegui import ui

    model = DCCModel(ctrl)
    macro = ctrl.MacroDef.data.get("DCCKeyboardPage", {}) if getattr(ctrl, "MacroDef", None) else {}
    title = macro.get("Title") or "DCC-Keyboard"
    description = macro.get("Ausführliche Beschreibung") or macro.get("Kurzbeschreibung") or ""
    ui.add_head_html("<style>" + CSS + "</style>")
    refs: dict = {"red": [], "guard": False}
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
        for index, button in enumerate(refs["red"]):
            button.set_text(str(model.address(index)))
        refs["guard"] = True
        try:
            refs["base"].set_value(model.base)
        finally:
            refs["guard"] = False

    def base_changed(e):
        if e.value is None or refs["guard"] or _to_int(e.value, model.base) == model.base:
            return
        model.set_base(e.value)
        refresh()

    async def pressed(index, channel):
        if not ctrl.is_connection_open():
            ok = await asyncio.get_running_loop().run_in_executor(None, model.ensure_connected)
            if not ok:
                ui.notify("Nicht mit dem ARDUINO verbunden (ARDUINO → Verbinden).", type="warning")
                return
        model.send(index, channel)

    def switch_button(index, channel):
        color = "red" if channel == 0 else "green"
        button = ui.button(str(model.address(index)) if channel == 0 else "", on_click=lambda i=index, c=channel: pressed(i, c))
        button.props(f"unelevated no-caps color={color}").classes("mll-dcc-btn")
        button.tooltip(f"Kanal {channel} ({'rot' if channel == 0 else 'grün'})")
        return button

    with ui.column().classes("w-full items-stretch gap-3 mll-dcc"):
        ui.label(title).classes("text-h6")
        with ui.row().classes("w-full items-center no-wrap gap-1 mll-dcc-desc"):
            refs["description"] = ui.label(description).classes("grow").tooltip("Antippen zum Auf- und Zuklappen")
            refs["description"].on("click", toggle_description)
            refs["desc_toggle"] = ui.button(icon="expand_more", on_click=toggle_description).props("flat dense round")
        text, lo, hi, _, hint = model.definition()
        refs["base"] = ui.number(label=text, value=model.base, min=lo, max=hi, step=1, precision=0, on_change=base_changed).props("dense outlined debounce=300").classes("w-48")
        refs["base"].tooltip(hint)
        for group in range(GROUPS):
            with ui.element("div").classes("mll-dcc-group"):
                for i in range(PER_GROUP):
                    refs["red"].append(switch_button(group * PER_GROUP + i, 0))
                for i in range(PER_GROUP):
                    switch_button(group * PER_GROUP + i, 1)
    refresh()
    return DCCPage(model, refresh)
