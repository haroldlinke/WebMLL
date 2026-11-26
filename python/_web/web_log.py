# Datei-Version: 1.15 (2026-11-26) - web_log.py
# ----------------------------------------------------------------------------------------------
# Name:           web_log.py
# Path:           _web/web_log.py
# Version:        1.15
# Last Update:    2026-11-26
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.15  2026-11-26  Beim Verschieben des Fensters hakte es, wenn gleichzeitig Meldungen kamen: die Zeilen werden gesammelt und alle 0,1 s auf einmal angezeigt; waehrend des Ziehens (Ereignis mll_log_drag) werden sie zurueckgehalten und nach dem Loslassen angezeigt; das Ziehen selbst ist leichter (ein Schritt je Bild, keine Layout-Abfrage je Mausbewegung, Zeiger-Ereignisse am Fenster). Test: test_log_drag.py. Zeilen mit '# v1.15'
#   1.14  2026-11-26  (Fassung mit Wiederholung, bis der Browser das Fenster aufgebaut hat) Das Fenster Kompilieren und Hochladen schwebt und laesst sich an der Titelzeile verschieben (die Seite dahinter bleibt bedienbar); die Position bleibt beim erneuten Oeffnen erhalten, Doppelklick auf die Titelzeile setzt sie zurueck. Zeilen mit '# v1.14'
#   1.13  2026-11-25  Issue 60 (Rueckmeldung zu 5.12): Knoepfe Vorgang abbrechen und Schliessen flackerten weiter beim Setup uebertragen: Zaehler der ruhigen Abfragen wird bei neuem Lauf und show() zurueckgesetzt; solange in den letzten 3 s Ausgabe kam, gilt der Vorgang als laufend
#   1.12  2026-11-23  Issue 60: Knoepfe Vorgang abbrechen und Schliessen flackerten waehrend Kompilieren/Hochladen: das Ende des Vorgangs wird erst nach 3 Abfragen (1,5 s) gemeldet
#   1.11  2026-11-20  Erfolgsfenster schliesst sich nach konfigurierbarer Verzögerung automatisch (MLL_WEBLOG_CLOSE_DELAY, 0 = sofort)
#   1.10  2026-11-19  Vorgang abbrechen beendet zuerst einen laufenden ESP32-Build oder -Upload (headless_esp32_ota.cancel_running), sonst wie bisher
#   1.09  2026-11-19  run_id: Nummer des Laufs im Fenster; Schliessen wird auch dann aktiv, wenn ein umgebendes Formular (OTA) noch als beschaeftigt gilt (Minimale Firmware per USB)
#   1.08  2026-11-19  Schliessen erst aktiv, wenn der Vorgang fertig ist; Vorgang abbrechen nur, solange er laeuft (set_running; Issue 28, Juergen)
#   1.07  2026-11-17  Kein Fehler mehr in der Ereignisschleife, wenn die Browserseite beim Kompilieren geschlossen oder neu geladen wurde (Log-Element gehoert zu einem geloeschten Client)
#   1.06  2026-11-11  Meldungen der ARDUINO IDE zum Netzwerk (JmDNS: javax.jmdns, dns[response, Hexdump, Steuerzeichen) werden weder angezeigt noch ins Protokoll geschrieben (tausende Zeilen je Minute auf einem Raspberry Pi mit verlaengertem Rechnernamen); eine Zeile im Protokoll nennt es je Lauf (fruehere Versionen ohne Eintrag)
# ----------------------------------------------------------------------------------------------
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
import os
import re  # v1.06
import time  # v1.13

from _web import web_dialogs as wd
try:  # v1.05
    from _web.web_i18n import tr  # v1.05
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v1.05
    def tr(text, **values):  # v1.05
        return text.format(**values) if values else text  # v1.05

logger = logging.getLogger(__name__)
arduino_log = logging.getLogger("webmobaledlib.arduino")           # Ausgabe der Laeufe im Protokoll

IDE_NOISE_MARKERS = ('javax.jmdns', 'dns[response', 'dns[query', 'Picked up JAVA_TOOL_OPTIONS')  # v1.06: Meldungen der Java-Bibliothek der IDE (Suche nach Boards im Netz), die mit dem Hochladen nichts zu tun haben
IDE_NOISE_HEXDUMP = re.compile(r"^\s*\d+: [0-9a-f]{16} [0-9a-f]{16}")  # v1.06: Hexdump eines DNS-Pakets


def is_ide_network_noise(line) -> bool:  # v1.06
    """True fuer Zeilen der IDE zur Netzwerksuche (JmDNS): Marker, Hexdump eines DNS-Pakets oder Zeilen mit Steuerzeichen (Paketinhalt)"""  # v1.06
    text = str(line)  # v1.06
    return any(m in text for m in IDE_NOISE_MARKERS) or bool(IDE_NOISE_HEXDUMP.match(text)) or "\x00" in text  # v1.06


HIGHLIGHT_CLASSES = {"Error": "text-red-8", "OK": "text-green-8", "O": "text-green-8"}
try:
    CLOSE_DELAY = max(0, min(300, int(os.environ.get("MLL_WEBLOG_CLOSE_DELAY", "5"))))
except ValueError:
    CLOSE_DELAY = 5
DEFAULT_TITLE = "Kompilieren und Hochladen"
INSTALL_TITLE = "Installation der Boards und Bibliotheken"


# Verschieben des schwebenden Fensters (v1.14): Titelzeile ziehen; die Verschiebung merkt sich der Browser (window.__mllLogPos), Doppelklick setzt sie zurueck
_DRAG_JS = """
(function setup(cardId, headId, tries){
  const find = id => document.getElementById('ng-' + id) || document.getElementById('c' + id);  // NiceGUI 4: ng-<Nr>, aeltere Versionen: c<Nr>
  const card = find(cardId), head = find(headId);
  if (!card || !head) {  // das Fenster wird nach dem Oeffnen erst vom Browser aufgebaut: kurz warten
    if (tries < 100) setTimeout(() => setup(cardId, headId, tries + 1), 50);
    return;
  }
  const st = window.__mllLogPos || (window.__mllLogPos = {x: 0, y: 0});
  const place = () => { card.style.transform = 'translate(' + st.x + 'px,' + st.y + 'px)'; };
  place();
  if (head.__mllDrag) return;
  head.__mllDrag = true;
  head.style.cursor = 'move';
  head.style.userSelect = 'none';
  head.style.touchAction = 'none';
  head.title = 'Zum Verschieben ziehen, Doppelklick: Ausgangsposition';
  const notify = on => { try { emitEvent('mll_log_drag', {on: on}); } catch (err) {} };  // der Server haelt waehrend des Ziehens die Meldungen zurueck
  head.addEventListener('dblclick', e => { if (e.target.closest('button')) return; st.x = 0; st.y = 0; place(); });
  head.addEventListener('pointerdown', e => {
    if (e.target.closest('button') || e.button > 0) return;
    const sx = e.clientX, sy = e.clientY, ox = st.x, oy = st.y;
    const r0 = card.getBoundingClientRect();  // einmal messen (Ausgangslage), nicht bei jeder Mausbewegung
    const W = window.innerWidth, H = window.innerHeight;
    let nx = ox, ny = oy, queued = false;
    const frame = () => { queued = false; st.x = nx; st.y = ny; place(); };
    const mv = ev => {
      let dx = ox + ev.clientX - sx, dy = oy + ev.clientY - sy;
      const top = r0.top + (dy - oy), left = r0.left + (dx - ox);
      if (top < 0) dy -= top;                                  // die Titelzeile bleibt im sichtbaren Bereich
      if (top > H - 40) dy -= top - (H - 40);
      if (left + r0.width < 80) dx += 80 - (left + r0.width);
      if (left > W - 80) dx -= left - (W - 80);
      nx = dx; ny = dy;
      if (!queued) { queued = true; requestAnimationFrame(frame); }  // hoechstens eine Aenderung je Bild
    };
    const up = () => {
      window.removeEventListener('pointermove', mv);
      window.removeEventListener('pointerup', up);
      window.removeEventListener('pointercancel', up);
      st.x = nx; st.y = ny; place();
      notify(false);
    };
    window.addEventListener('pointermove', mv);
    window.addEventListener('pointerup', up);
    window.addEventListener('pointercancel', up);
    notify(true);
  });
})(%d, %d, 0);
"""


class WebLog:
    def __init__(self, controller):
        self.ctrl = controller
        self.lines: list[tuple[str, str]] = []        # (Text, Klassen) fuer spaeteres Oeffnen
        self._log = None
        self._dialog = None
        self._loop = None
        self._close_handle = None
        self._close_note = None                       # verhindert doppelte Meldungen beim mehrfachen Aufruf
        self.last_result = None                       # "OK" oder "Error": Ergebnis der letzten Befehlszeile (execute_shell_cmd)
        self.close_delay = CLOSE_DELAY                # v1.11: konfigurierbar per ENV MLL_WEBLOG_CLOSE_DELAY (0 = sofort schliessen)
        self.title = DEFAULT_TITLE
        self._title_label = None
        self._running = False                         # v1.08: laeuft gerade ein Vorgang? (steuert Schliessen und Vorgang abbrechen)
        self._btn_cancel = None  # v1.08
        self._btn_close = None  # v1.08
        self.run_id = 0  # v1.09: wird mit jedem neuen Lauf (delete_text_from_textwindow) hochgezaehlt
        self._pending = []  # v1.15: Zeilen, die noch nicht im Fenster stehen (nur im Ereignis-Thread benutzt)
        self._flush_scheduled = False  # v1.15
        self._dragging = False  # v1.15: der Anwender verschiebt gerade das Fenster
        self._drag_since = 0.0  # v1.15

    # ------------------------------------------------------------------ Schnittstelle der Tk-Seite
    def delete_text_from_textwindow(self):
        self.lines.clear()
        self._noise_count = 0  # v1.06
        arduino_log.info("----- %s: neuer Lauf -----", self.title)
        self._running = True  # v1.08: neuer Lauf
        self._idle_polls = 0  # v1.13: Zaehler der ruhigen Abfragen neu beginnen
        self._last_activity = time.monotonic()  # v1.13
        self.run_id += 1  # v1.09
        self._on_loop(self._apply_running)  # v1.08
        self._on_loop(self._cancel_close)
        self._on_loop(self._pending.clear)  # v1.15
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
            if is_ide_network_noise(line):                          # v1.06: Netzwerkmeldungen der IDE nicht anzeigen
                self._noise_count = getattr(self, "_noise_count", 0) + 1  # v1.06
                if self._noise_count == 1:  # v1.06
                    arduino_log.info("Meldungen der ARDUINO IDE zum Netzwerk (JmDNS) werden nicht angezeigt und nicht protokolliert")  # v1.06
                continue  # v1.06
            self.lines.append((line, classes))
            self._last_activity = time.monotonic()  # v1.13: Ausgabe im Gang = Vorgang laeuft
            if line.strip():
                arduino_log.log(logging.WARNING if highlight == "Error" else logging.INFO, "%s", line)
            # self._on_loop(lambda l=line, c=classes: self._push(l, c))  # v1.15 (entfallen: eine Aenderung je Zeile belastete den Browser)
            self._on_loop(lambda l=line, c=classes: self._enqueue(l, c))  # v1.15

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
        self._running = True  # v1.08: show() kommt aus dem Worker-Thread eines laufenden Vorgangs
        self._idle_polls = 0  # v1.13
        self._last_activity = time.monotonic()  # v1.13
        wd.call_in_loop(self._show_async, default=None)

    async def _show_async(self):
        from nicegui import ui
        client = wd._bridge["client"]
        if self._dialog is None or self._log is None:
            with client:
                self._dialog = ui.dialog().props("seamless position=bottom")
                ui.on("mll_log_drag", self._on_drag)  # v1.15
                with self._dialog, ui.card().classes("w-[1100px] max-w-[96vw] mll-bottom-card").style(wd.BOTTOM_LIFT) as self._card:  # v1.14
                    with ui.row().classes("items-center w-full") as self._head:  # v1.14: Titelzeile = Griff zum Verschieben
                        self._title_label = ui.label(self.title).classes("text-h6")
                        ui.space()
                        # ui.button("Vorgang abbrechen", on_click=self._terminate).props("color=negative outline dense")  # v1.08 (entfallen)
                        # ui.button("Schließen", on_click=self._dialog.close).props("flat dense")  # v1.08 (entfallen)
                        self._btn_cancel = ui.button("Vorgang abbrechen", on_click=self._terminate).props("color=negative outline dense")  # v1.08
                        self._btn_close = ui.button("Schließen", on_click=self._dialog.close).props("flat dense")  # v1.08
                    self._log = ui.log(max_lines=3000).classes("w-full mll-log").style(
                        "height: 36vh; min-height: 8rem; max-height: calc(100vh - 16rem); font-family: monospace; font-size: 12px; white-space: pre")
                for line, classes in self.lines:
                    self._log.push(line, classes=classes or None)
                self._pending.clear()  # v1.15: alles Bisherige steht jetzt im Fenster
        self._apply_running()  # v1.08
        self._cancel_close()
        self._dialog.open()
        try:  # v1.14: schwebend und verschiebbar
            client.run_javascript(_DRAG_JS % (self._card.id, self._head.id))  # v1.14
        except Exception:                              # noqa: BLE001  # v1.14
            logger.debug("Log-Fenster nicht verschiebbar", exc_info=True)  # v1.14

    def set_running(self, running):  # v1.08
        """Laeuft ein Vorgang? Dann ist nur Vorgang abbrechen aktiv, sonst nur Schliessen (Aufruf aus dem Zeitgeber der Seite, im Ereignis-Thread)."""
        running = bool(running)
        if not running and time.monotonic() - getattr(self, "_last_activity", 0.0) < 3.0:  # v1.13: in den letzten 3 s kam Ausgabe: der Vorgang laeuft noch (auch wenn busy kurz zurueckgesetzt war)
            running = True  # v1.13
        if running:  # v1.12
            self._idle_polls = 0  # v1.12
        elif self._running:  # v1.12: Ende des Vorgangs erst melden, wenn es 3 Abfragen (1,5 s) hintereinander so ist: kein Flackern der Knoepfe, wenn ein kurzer Befehl den Zustand kurz zuruecksetzt (Issue 60)
            self._idle_polls = getattr(self, "_idle_polls", 0) + 1  # v1.12
            if self._idle_polls < 3:  # v1.12
                return  # v1.12
        # if running == self._running:  # v1.12 (entfallen: gleiche Pruefung folgt)
        if running == self._running:
            return
        self._running = running
        self._apply_running()

    def _apply_running(self):  # v1.08
        try:
            if self._btn_cancel is not None:
                self._btn_cancel.set_enabled(self._running)
            if self._btn_close is not None:
                self._btn_close.set_enabled(not self._running)
        except RuntimeError:                           # Browserseite wurde geschlossen/neu geladen
            self._btn_cancel = self._btn_close = None

    def _close_delay_for(self, setting_name, fallback=None):
        """Wert der Auto-Close-Option aus den Programm Einstellungen: 'sofort', '5 Sekunden', ..., 'nie' -> None."""
        if self.ctrl is None:
            return fallback
        try:
            raw = self.ctrl.getConfigData(setting_name)
            if raw is None or raw == "":
                raw = self.ctrl.getConfigData(setting_name + "Idx")
        except Exception:                                  # noqa: BLE001
            raw = None
        if raw is None or raw == "":
            return fallback
        if isinstance(raw, str):
            text = raw.strip()
            if text.lower() in ("sofort", "0"):
                return 0
            if text.lower() in ("5 sekunden", "5"):
                return 5
            if text.lower() in ("10 sekunden", "10"):
                return 10
            if text.lower() in ("30 sekunden", "30"):
                return 30
            if text.lower() in ("nie", "never", "no"):
                return None
            try:
                return max(0, int(float(text)))
            except ValueError:
                return fallback
        try:
            value = int(raw)
        except (TypeError, ValueError):
            return fallback
        if value == 0:
            return 0
        if value == 1:
            return 5
        if value == 2:
            return 10
        if value == 3:
            return 30
        if value == 4:
            return None
        return fallback

    def close_later_if_ok(self, *, on_error=False):
        """Nach einem Befehl: Fenster schliessen, wenn die letzte Ausgabe ein Erfolg war (z. B. Bibliotheken installieren).
        Bei Fehler wird nur dann automatisch geschlossen, wenn in den Einstellungen eine Zeit gesetzt wurde."""
        if self.last_result == "OK":
            self.close_later(self._close_delay_for("SetupCloseOnSuccess", self.close_delay))
        elif on_error:
            delay = self._close_delay_for("SetupCloseOnError", 30)
            if delay is not None:
                self.close_later(delay)

    def close_later(self, seconds=None):
        """Nach einem erfolgreichen Lauf: Fenster nach einigen Sekunden schliessen (Zeit zum Lesen)."""
        if seconds is None:
            seconds = self.close_delay
        else:
            seconds = max(0, seconds)
        if seconds is None:
            return
        note = tr('Dieses Fenster schließt sich in {seconds} Sekunden.', seconds=seconds) if seconds > 0 else None
        if note is not None and self._close_note == note and self._close_handle is not None:
            return
        def schedule():
            self._cancel_close()
            if self._dialog is None or not self._dialog.value:        # nicht vorhanden oder schon geschlossen
                return
            if note is not None:
                if not self.lines or self.lines[-1][0] != note:
                    self.lines.append((note, "text-grey-7"))
                    self._push(note, "text-grey-7")
                self._close_note = note
            else:
                self._close_note = None
            self._close_handle = self._loop.call_later(seconds, self._close_now)
        loop = self._loop or wd._bridge.get("loop")
        if loop is not None:
            self._loop = loop
            loop.call_soon_threadsafe(schedule)

    def _close_now(self):
        self._close_handle = None
        self._close_note = None
        if self._dialog is not None:
            self._dialog.close()

    def _cancel_close(self):
        if self._close_handle is not None:
            self._close_handle.cancel()
            self._close_handle = None
        self._close_note = None

    FLUSH_INTERVAL = 0.1  # v1.15: Sekunden zwischen zwei Aktualisierungen des Fensters
    DRAG_HOLD_MAX = 8.0  # v1.15: laenger werden Meldungen beim Ziehen nicht zurueckgehalten (falls das Loslassen nie ankommt)

    def _enqueue(self, line, classes):  # v1.15: im Ereignis-Thread
        self._pending.append((line, classes))
        if not self._flush_scheduled:
            self._flush_scheduled = True
            loop = self._loop or wd._bridge.get("loop")
            if loop is None:
                self._flush_scheduled = False
                return
            loop.call_later(self.FLUSH_INTERVAL, self._flush)

    def _flush(self):  # v1.15: alle gesammelten Zeilen auf einmal anzeigen, nicht waehrend das Fenster gezogen wird
        self._flush_scheduled = False
        if self._dragging:
            if time.monotonic() - self._drag_since < self.DRAG_HOLD_MAX:
                return                                  # nach dem Loslassen (_on_drag) wird nachgeholt
            self._dragging = False
        pending, self._pending = self._pending, []
        for line, classes in pending:
            self._push(line, classes)

    def _on_drag(self, e):  # v1.15: Ereignis mll_log_drag des Browsers: Ziehen beginnt (on) oder endet
        try:
            on = bool((e.args or {}).get("on"))
        except Exception:                              # noqa: BLE001
            on = False
        self._dragging = on
        self._drag_since = time.monotonic()
        if not on:
            self._flush()

    def _push(self, line, classes):
        if self._log is not None:
            try:  # v1.07
                self._log.push(line, classes=classes or None)
            except RuntimeError:                           # v1.07: Browserseite wurde geschlossen/neu geladen ("client has been deleted")
                self._log = None  # v1.07

    def _on_loop(self, fn):
        loop = self._loop or wd._bridge.get("loop")
        if loop is None:
            return
        loop.call_soon_threadsafe(fn)

    def _terminate(self):
        try:  # v1.10: laufender ESP32-Build oder -Upload?
            from headless import headless_esp32_ota as _ota  # v1.10
            if _ota.cancel_running():  # v1.10
                logger.info("ESP32-Build/Upload wird abgebrochen")  # v1.10
                return  # v1.10
        except Exception:  # noqa: BLE001  # v1.10
            logger.debug("cancel_running nicht verfuegbar", exc_info=True)  # v1.10
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
