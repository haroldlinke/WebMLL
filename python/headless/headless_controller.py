# Datei-Version: 1.01 (2026-10-12) - headless_controller.py
"""HeadlessController: Tk-freier Ersatz für den Hauptcontroller (nur die Teilmenge, die
XLA_Application.py, XLF_FormGenerator.py und die Python-Module tatsächlich aufrufen).

Gefunden per Suche nach `controller.` / `global_controller.` in XLA_Application.py:
  set_statusmessage, update, bind, after, winfo_width/height/x/y, blinking_on_off,
  show_hiddentables, loaddatafile, getConfigData/setConfigData, defaultfontnormal,
  activeworkbook, ProgVersion, DataVersion, ProgGenMinDataVersion, PattGenMinDataVersion, ToolTip.

Statusmeldungen gehen an registrierte Callbacks (`on_status`). Ein Web-Frontend hängt dort
seine Statuszeile ein, z. B.:  controller.on_status.append(lambda text, fg: bridge.post(label.set_text, text))
"""
from __future__ import annotations

import logging
import threading
import time
from typing import Callable

logger = logging.getLogger(__name__)


class HeadlessController:
    def __init__(self, prog_version: str = "0.0.0", data_version: str = "1",
                 prog_gen_min_data_version: str = "0", patt_gen_min_data_version: str = "0"):
        # --- Versionsangaben (werden mit int(...) verglichen, daher numerische Strings)
        self.ProgVersion = prog_version
        self.DataVersion = data_version
        self.ProgGenMinDataVersion = prog_gen_min_data_version
        self.PattGenMinDataVersion = patt_gen_min_data_version
        # --- Zustand, den die Excel-Schicht liest
        self.defaultfontnormal = ("Arial", 9)
        self.defaultfontsmall = ("Arial", 8)
        self.smallscreen = False
        self.IPUploadTimeout = 30           # Platzhalter, bitte an den Originalwert anpassen
        self.tempworkbookFilname = "tempworkbook"   # Platzhalter
        self.bindings: dict = {}
        self.ExcelApplication = None        # nach CApplication(...) setzen
        self.MacroDef = None                # Makrodefinitionen (Toolbar), noch nicht umgesetzt
        self.show_hiddentables = False
        self.loaddatafile = ""          # Pfad der beim Start zu ladenden Datei oder ""
        self.activeworkbook = None
        self._config: dict[str, str] = {}
        # --- Beobachter für die Oberfläche
        self.on_status: list[Callable[[str, str], None]] = []
        self.on_update: list[Callable[[], None]] = []
        self.on_blink: list[Callable[..., None]] = []
        self.statusmessage_text = ""
        self.statusmessage_fg = "black"
        self.statusmessage_time = time.monotonic()      # wann die Meldung gesetzt wurde (die Oberflaeche blendet alte Meldungen aus)

    # ------------------------------------------------------------------ Status / Update
    def set_statusmessage(self, status_text, fg="black", monitor_message=False):
        logger.debug("set_statusmessage: %s", status_text)
        self.statusmessage_text = str(status_text)
        self.statusmessage_fg = fg
        self.statusmessage_time = time.monotonic()
        for cb in list(self.on_status):
            cb(self.statusmessage_text, fg)

    def update(self):
        for cb in list(self.on_update):
            cb()

    # ------------------------------------------------------------------ Tk-Aufrufe ohne Wirkung
    def bind(self, *args, **kwargs):
        """Tk-Tastenbindungen: nur merken (z. B. 'Control-c' -> Abbrechen im Log-Fenster)."""
        if len(args) >= 2 and callable(args[1]):
            self.bindings[args[0]] = args[1]
        return None

    def winfo_width(self):
        return 1920

    def winfo_height(self):
        return 1080

    def winfo_x(self):
        return 0

    def winfo_y(self):
        return 0

    def ToolTip(self, widget=None, text="", button_1=False):
        return None

    def get_font(self, name):
        return {"FontText": ("Arial", 10), "FontTitle": ("Arial", 14, "bold")}.get(name, self.defaultfontnormal)

    # ------------------------------------------------------------------ Zeit
    def after(self, ms, func=None, *args):
        """Tk: after(ms) ohne Funktion = Warten, mit Funktion = später aufrufen."""
        if func is None:
            time.sleep(ms / 1000)
            return None
        t = threading.Timer(ms / 1000, func, args)
        t.daemon = True
        t.start()
        return t

    # ------------------------------------------------------------------ Konfiguration / Hardware
    def getConfigData(self, key, default=""):
        return self._config.get(key, default)

    def setConfigData(self, key, value):
        self._config[key] = value

    def blinking_on_off(self, lednum, ledcount, seq=False):
        for cb in list(self.on_blink):
            cb(lednum, ledcount, seq)
