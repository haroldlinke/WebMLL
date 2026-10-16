# Datei-Version: 1.04 (2026-10-15) - web_log.py
"""Log-Fenster fuer Kompilieren und Hochladen (Ersatz fuer ARDUINOMonitorPage).

WebLog bietet dieselben Methoden wie das Textfenster der Tk-Seite
(delete_text_from_textwindow, add_text_to_textwindow, update). Die Texte kommen aus dem
Worker-Thread, in dem das Makro (Kompilieren/Hochladen) laeuft, und erscheinen live im Browser.
Das Fenster bleibt nach dem Lauf offen, damit man das Ergebnis lesen kann.

Jede Zeile steht ausserdem im Protokoll (Logger webmobaledlib.arduino, Stufe INFO, Zeilen mit Fehlermarkierung WARNING), damit sich ein Lauf
(Kompilieren, Hochladen, Installation der Boards und Bibliotheken) auch spaeter in der Datei webmobaledlib.log nachlesen laesst.
"""
from __future__ import annotations

import logging

from _web import web_dialogs as wd

logger = logging.getLogger(__name__)
arduino_log = logging.getLogger("webmobaledlib.arduino")           # Ausgabe der Laeufe im Protokoll

HIGHLIGHT_CLASSES = {"Error": "text-red-8", "OK": "text-green-8", "O": "text-green-8"}
CLOSE_DELAY = 10          # Sekunden, die die Erfolgsmeldung nach einem erfolgreichen Lauf lesbar bleibt
DEFAULT_TITLE = "Kompilieren und Hochladen"
INSTALL_TITLE = "Installation der Boards und Bibliotheken"


class WebLog:
    def __init__(self, controller):
        self.ctrl = controller
        self.lines: list[tuple[str, str]] = []        # (Text, Klassen) fuer spaeteres Oeffnen
        self._log = None
        self._dialog = None
        self._loop = None
        self._close_handle = None
        self.last_result = None                       # "OK" oder "Error": Ergebnis der letzten Befehlszeile (execute_shell_cmd)
        self.title = DEFAULT_TITLE
        self._title_label = None

    # ------------------------------------------------------------------ Schnittstelle der Tk-Seite
    def delete_text_from_textwindow(self):
        self.lines.clear()
        arduino_log.info("----- %s: neuer Lauf -----", self.title)
        self._on_loop(self._cancel_close)
        self._on_loop(lambda: self._log.clear() if self._log is not None else None)

    def add_text_to_textwindow(self, text="", nl="", highlight=None):
        classes = HIGHLIGHT_CLASSES.get(highlight, "")
        if highlight == "Error":
            self.last_result = "Error"
        elif highlight in ("OK", "O"):
            self.last_result = "OK"
        txt = str(text) + str(nl)
        if txt == "":
            return
        if txt.endswith("\n"):                 # ein abschliessender Zeilenumbruch erzeugt keine Leerzeile
            txt = txt[:-1]
        for line in txt.split("\n"):
            self.lines.append((line, classes))
            if line.strip():
                arduino_log.log(logging.WARNING if highlight == "Error" else logging.INFO, "%s", line)
            self._on_loop(lambda l=line, c=classes: self._push(l, c))

    def update(self):
        pass

    def destroy(self):
        pass

    # ------------------------------------------------------------------ Anzeige
    def set_title(self, text):
        """Titel des Fensters aendern (Kompilieren und Hochladen / Installation der Boards und Bibliotheken)"""
        if text == self.title:
            return
        self.title = text
        arduino_log.info("----- %s -----", text)
        self._on_loop(lambda: self._title_label.set_text(text) if self._title_label is not None else None)

    def show(self):
        """Fenster oeffnen (aus dem Worker-Thread). Im Hauptthread nicht moeglich -> nur protokollieren."""
        if not wd.bridge_usable():
            logger.info("Log-Fenster ohne Bruecke nicht anzeigbar")
            return
        self._loop = wd._bridge["loop"]
        wd.call_in_loop(self._show_async, default=None)

    async def _show_async(self):
        from nicegui import ui
        client = wd._bridge["client"]
        if self._dialog is None or self._log is None:
            with client:
                self._dialog = ui.dialog().props("seamless position=bottom")
                with self._dialog, ui.card().classes("w-[1100px] max-w-[96vw] mll-bottom-card").style(wd.BOTTOM_LIFT):
                    with ui.row().classes("items-center w-full"):
                        self._title_label = ui.label(self.title).classes("text-h6")
                        ui.space()
                        ui.button("Vorgang abbrechen", on_click=self._terminate).props("color=negative outline dense")
                        ui.button("Schließen", on_click=self._dialog.close).props("flat dense")
                    self._log = ui.log(max_lines=3000).classes("w-full mll-log").style(
                        "height: 36vh; min-height: 8rem; max-height: calc(100vh - 16rem); font-family: monospace; font-size: 12px; white-space: pre")
                for line, classes in self.lines:
                    self._log.push(line, classes=classes or None)
        self._cancel_close()
        self._dialog.open()

    def close_later_if_ok(self):
        """Nach einem Befehl: Fenster schliessen, wenn die letzte Ausgabe ein Erfolg war (z. B. Bibliotheken installieren).
        Nach einem Fehler bleibt es offen, damit man die Meldung lesen kann."""
        if self.last_result == "OK":
            self.close_later()

    def close_later(self, seconds=CLOSE_DELAY):
        """Nach einem erfolgreichen Lauf: Fenster nach einigen Sekunden schliessen (Zeit zum Lesen)."""
        def schedule():
            self._cancel_close()
            if self._dialog is None or not self._dialog.value:        # nicht vorhanden oder schon geschlossen
                return
            note = f"Dieses Fenster schließt sich in {seconds} Sekunden."
            self.lines.append((note, "text-grey-7"))
            self._push(note, "text-grey-7")
            self._close_handle = self._loop.call_later(seconds, self._close_now)
        loop = self._loop or wd._bridge.get("loop")
        if loop is not None:
            self._loop = loop
            loop.call_soon_threadsafe(schedule)

    def _close_now(self):
        self._close_handle = None
        if self._dialog is not None:
            self._dialog.close()

    def _cancel_close(self):
        if self._close_handle is not None:
            self._close_handle.cancel()
            self._close_handle = None

    def _push(self, line, classes):
        if self._log is not None:
            self._log.push(line, classes=classes or None)

    def _on_loop(self, fn):
        loop = self._loop or wd._bridge.get("loop")
        if loop is None:
            return
        loop.call_soon_threadsafe(fn)

    def _terminate(self):
        cb = getattr(self.ctrl, "bindings", {}).get("Control-c")
        if cb:
            cb()
        else:
            logger.info("Kein laufender Vorgang zum Abbrechen")


class NullFrame:
    """Ersatz fuer Tk-Seiten, die es im Web nicht gibt (alle Aufrufe sind No-Ops)."""
    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return lambda *a, **k: None
