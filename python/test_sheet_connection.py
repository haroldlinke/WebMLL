# Datei-Version: 1.00 (2026-11-27) - test_sheet_connection.py
# ----------------------------------------------------------------------------------------------
# Name:           test_sheet_connection.py
# Path:           test_sheet_connection.py
# Version:        1.00
# Last Update:    2026-11-27
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-27  Neu: Blattwechsel baut die Verbindung des Blatts auf (webmobaledlib 5.70, sync_connection_to_sheet): anderer Anschluss, gleicher Anschluss, Anschluss fehlt,
#                     Blatt ohne eigene Verbindung und anderer Typ, Hinweis-Anschluss (negative Zahl), Warnung bei anderem Typ, beschaeftigt, WLAN
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_sheet_connection.py

Holt die verschachtelten Funktionen (sync_connection_to_sheet, _stored_ports, _connected_type ...) mit ast aus webmobaledlib.py und fuehrt sie mit Ersatzobjekten aus:
ein Ersatz-Controller (offen/zu, Geraete mit Startmeldung je Anschluss oder WLAN-Adresse, connect_silent wie in _web/web_serial.py mit verify), ein Ersatz-Blatt (Zellen),
eine Ersatz-Oberflaeche (Meldungen). Die Texte der Meldungen werden mit dem echten Uebersetzer in allen Sprachen geprueft.
Nicht geprueft: echte Hardware, Browser, der Ablauf in NiceGUI (activate -> Hook), die Anschlussliste des Rechners (_port_present wird ersetzt)."""
import ast
import asyncio
import logging
import os
import re
import sys
import textwrap
import threading
import types
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
SRC = open(os.path.join(ROOT, "webmobaledlib.py"), encoding="utf-8").read()

NAMES = ("_silent_connect", "_sheet_board_type", "_stored_ports", "_port_hint_flag", "_store_hint_port", "_connected_type", "_connected_type_ok",
         "_connected_type_known", "_disconnect_locked", "_switch_connection", "_switch_wifi", "sync_connection_to_sheet")

T_OTHER_TYPE = "Die Verbindung wurde getrennt, weil das Blatt für eine andere Lichtmaschine ({want}) gilt als die verbundene ({have})."
T_UNREACHABLE = "Die Verbindung zum Gerät des Blatts ({port}) ist nicht möglich. Die bisherige Verbindung wurde getrennt. Bitte „Mit Lichtmaschine verbinden“ drücken."
T_WARN_TYPE = "Achtung: Am Anschluss {port} meldet sich eine andere Lichtmaschine ({have}) als im Blatt eingestellt ({want})."

MSG = {"ESP32": "LEDs_AutoProg Ver 3: ESP32 3.6.0 27.11.26 18:34", "Pico": "LEDs_AutoProg Ver 3: PICO 3.6.0 27.11.26 18:13", "Nano": "LEDs_AutoProg Ver 3: NANO 3.6.0 27.11.26 18:13"}


def extract(names):
    """Quelltext der verschachtelten Funktionen aus webmobaledlib.py (jede genau einmal)"""
    found = {}
    for node in ast.walk(ast.parse(SRC)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names:
            assert node.name not in found, "Funktion %s mehrfach vorhanden" % node.name
            found[node.name] = textwrap.dedent(ast.get_source_segment(SRC, node))
    missing = [n for n in names if n not in found]
    assert not missing, "fehlt in webmobaledlib.py: %s" % missing
    return found


class Cell(str):
    @property
    def Value(self):
        return str(self)


class Sheet:
    """Blatt mit den Zellen der Variablenzeile: Anschluss der Lichtmaschine, Build Optionen (Typ), Anschluss LNet/DCC"""
    ROW, COL_PORT, COL_PORTR, COL_OPTS = 3, 2, 4, 8

    def __init__(self, name, port="", opts=""):
        self.Name = name
        self.CellDict = {(self.ROW, self.COL_PORT): port, (self.ROW, self.COL_OPTS): opts, (self.ROW, self.COL_PORTR): ""}

    def Cells(self, row, col):
        return Cell(self.CellDict.get((row, col), ""))


class FakeCtrl:
    """Ersatz-Controller: Geraete = {Anschluss oder ('IP', Adresse): Startmeldung}; connect_silent wie web_serial.SerialMixin.connect_silent"""

    def __init__(self, devices):
        self.devices = devices
        self._conn_lock = threading.RLock()
        self.open, self.ARDUINO_current_portname, self.ARDUINO_IP, self.ARDUINO_startmessage = False, "", False, ""
        self.cfg, self.log = {}, []

    def is_connection_open(self):
        return self.open

    def attach(self, key, ip=False):
        self.open, self.ARDUINO_current_portname, self.ARDUINO_IP = True, key if not ip else key, ip
        self.ARDUINO_startmessage = self.devices.get(("IP", key) if ip else key.upper(), "")

    def disconnect(self):
        self.log.append("disconnect")
        self.open, self.ARDUINO_current_portname, self.ARDUINO_IP, self.ARDUINO_startmessage = False, "", False, ""

    def connect_silent(self, port=None, wlan=None, dtr=None, esp32=None, verify=None):
        with self._conn_lock:
            if self.open:
                return True
            key = ("IP", esp32[0]) if esp32 else str(port).upper()
            self.log.append("connect %s" % (esp32[0] if esp32 else port))
            if key not in self.devices:
                return False
            self.open, self.ARDUINO_IP = True, bool(esp32)
            self.ARDUINO_current_portname = esp32[0] if esp32 else str(port)
            self.ARDUINO_startmessage = self.devices[key]
            if verify is not None and not verify():
                self.disconnect()
                return False
            return True

    def getConfigData(self, name):
        return self.cfg.get(name, "")

    def setConfigData(self, name, value):
        self.cfg[name] = value


class Ui:
    def __init__(self):
        self.messages = []

    def notify(self, text, type="info"):
        self.messages.append((type, text))


class Run:
    async def io_bound(self, fn, *args):
        return fn(*args)


class NoWait:
    """Ersatz fuer asyncio: schlaeft nicht (der Test 'beschaeftigt' soll keine 5 Sekunden dauern)"""
    @staticmethod
    async def sleep(_seconds):
        return None


class SheetConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = extract(NAMES)

    def build(self, ws, devices, present=(), wifi=None, busy=False):
        ctrl = FakeCtrl(devices)
        ui = Ui()
        calls = []
        state = {"ws": ws, "busy": busy}
        ns = {"os": os, "re": re, "asyncio": NoWait, "logger": logging.getLogger("test_sheet_connection"), "ctrl": ctrl, "ui": ui, "run": Run(), "state": state,
              "M02": types.SimpleNamespace(SH_VARS_ROW=Sheet.ROW), "M25": types.SimpleNamespace(BUILDOP_COL=Sheet.COL_OPTS, COMPort_COL=Sheet.COL_PORT, COMPrtR_COL=Sheet.COL_PORTR),
              "tr": lambda text, **values: text.format(**values), "wifi_target": lambda: wifi, "after_connect": lambda: calls.append("after_connect")}
        for name in NAMES:
            exec(compile(self.sources[name], name, "exec"), ns)
        upper = {str(p).upper() for p in present}
        ns["_port_present"] = lambda port: str(port).upper() in upper
        return ctrl, ui, calls, ns

    def sync(self, ns, ws, **kw):
        asyncio.run(ns["sync_connection_to_sheet"](ws, **kw))

    # ------------------------------------------------------------------ Anschluss
    def test_other_port_is_connected(self):
        ws = Sheet("ESP", port="COM7", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"], "COM7": MSG["ESP32"]}, present=["COM5", "COM7"])
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertTrue(ctrl.open)
        self.assertEqual(ctrl.ARDUINO_current_portname, "COM7")
        self.assertEqual(ctrl.log, ["disconnect", "connect COM7"])
        self.assertIn(("positive", "Mit der Lichtmaschine verbunden (COM7)."), ui.messages)
        self.assertEqual(calls, ["after_connect"])
        self.assertEqual(len(ui.messages), 1, ui.messages)

    def test_same_port_stays(self):
        ws = Sheet("ESP", port="COM7", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM7": MSG["ESP32"]}, present=["COM7"])
        ctrl.attach("COM7")
        self.sync(ns, ws)
        self.assertEqual(ctrl.log, [])
        self.assertEqual(ui.messages, [])

    def test_port_missing_leaves_no_old_connection(self):
        ws = Sheet("ESP", port="COM9", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"]}, present=["COM5"])
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertFalse(ctrl.open, "die Verbindung zum Pico darf nicht stehen bleiben")
        self.assertEqual(ui.messages, [("warning", T_UNREACHABLE.format(port="COM9"))])
        self.assertEqual(calls, [])

    def test_other_type_at_explicit_port_warns(self):
        ws = Sheet("ESP", port="COM7", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM7": MSG["Pico"]}, present=["COM7"])
        self.sync(ns, ws)  # ohne offene Verbindung geschieht nichts
        self.assertEqual((ctrl.log, ui.messages), ([], []))
        ctrl.attach("COM5")
        ctrl.devices["COM5"] = MSG["ESP32"]
        ctrl.ARDUINO_startmessage = MSG["ESP32"]
        self.sync(ns, ws)
        self.assertTrue(ctrl.open)
        self.assertEqual(ctrl.ARDUINO_current_portname, "COM7")
        self.assertIn(("warning", T_WARN_TYPE.format(port="COM7", have="Pico", want="ESP32")), ui.messages)

    # ------------------------------------------------------------------ Blatt ohne eigene Verbindung
    def test_sheet_without_connection_other_type_is_disconnected(self):
        ws = Sheet("ESP", port="COM?", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"]}, present=["COM5"])
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertFalse(ctrl.open)
        self.assertEqual(ui.messages, [("warning", T_OTHER_TYPE.format(want="ESP32", have="Pico"))])

    def test_sheet_without_connection_same_type_stays(self):
        ws = Sheet("Pico", port="", opts="rp2040")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"]}, present=["COM5"])
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertTrue(ctrl.open)
        self.assertEqual((ctrl.log, ui.messages), ([], []))

    def test_unknown_type_is_never_disconnected(self):
        ws = Sheet("ESP", port="", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": ""}, present=["COM5"])
        ctrl.attach("COM5")                                    # keine Startmeldung: Typ unbekannt
        self.sync(ns, ws)
        self.assertTrue(ctrl.open)
        self.assertEqual(ui.messages, [])

    def test_sheet_without_connection_and_type_stays(self):
        ws = Sheet("Neu", port="", opts="")                    # Typ nicht eingetragen
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"]}, present=["COM5"])
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertTrue(ctrl.open)

    # ------------------------------------------------------------------ Hinweis-Anschluss (negative Zahl)
    @unittest.skipUnless(os.name == "nt", "Hinweis COM<n> gilt nur unter Windows")
    def test_hint_with_other_device_is_disconnected_and_not_stored(self):
        ws = Sheet("ESP", port="-7", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"], "COM7": MSG["Pico"]}, present=["COM5", "COM7"])
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertFalse(ctrl.open, "am Hinweis-Anschluss meldet sich ein Pico: nicht verbunden lassen")
        self.assertEqual(ws.Cells(Sheet.ROW, Sheet.COL_PORT), "-7", "der Anschluss darf nicht ins Blatt eingetragen werden")
        self.assertEqual(ui.messages, [("warning", T_UNREACHABLE.format(port="COM7"))])

    @unittest.skipUnless(os.name == "nt", "Hinweis COM<n> gilt nur unter Windows")
    def test_hint_with_matching_device_is_stored(self):
        ws = Sheet("ESP", port="-7", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"], "COM7": MSG["ESP32"]}, present=["COM5", "COM7"])
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertTrue(ctrl.open)
        self.assertEqual(ctrl.ARDUINO_current_portname, "COM7")
        self.assertEqual(ws.Cells(Sheet.ROW, Sheet.COL_PORT), "COM7")

    # ------------------------------------------------------------------ beschaeftigt, WLAN
    def test_busy_keeps_connection_without_messages(self):
        ws = Sheet("ESP", port="COM7", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"], "COM7": MSG["ESP32"]}, present=["COM5", "COM7"], busy=True)
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertTrue(ctrl.open)
        self.assertEqual(ctrl.ARDUINO_current_portname, "COM5")
        self.assertEqual((ctrl.log, ui.messages), ([], []))

    def test_wlan_target_is_preferred(self):
        ws = Sheet("ESP", port="COM7", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"], ("IP", "10.0.0.5"): MSG["ESP32"]}, present=["COM5"], wifi=("10.0.0.5", "pw"))
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertTrue(ctrl.open and ctrl.ARDUINO_IP)
        self.assertEqual(ctrl.ARDUINO_current_portname, "10.0.0.5")
        self.assertEqual(ctrl.log, ["disconnect", "connect 10.0.0.5"])

    def test_wlan_unreachable_falls_back_to_usb(self):
        ws = Sheet("ESP", port="COM7", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"], "COM7": MSG["ESP32"]}, present=["COM5", "COM7"], wifi=("10.0.0.5", "pw"))
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertEqual(ctrl.ARDUINO_current_portname, "COM7")
        self.assertFalse(ctrl.ARDUINO_IP)

    def test_wlan_and_usb_unreachable_leave_no_connection(self):
        ws = Sheet("ESP", port="COM7", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {"COM5": MSG["Pico"]}, present=["COM5"], wifi=("10.0.0.5", "pw"))
        ctrl.attach("COM5")
        self.sync(ns, ws)
        self.assertFalse(ctrl.open)
        self.assertEqual(ui.messages, [("warning", T_UNREACHABLE.format(port="10.0.0.5"))])

    def test_wlan_connection_stays_for_the_same_target(self):
        ws = Sheet("ESP", port="COM7", opts="esp32")
        ctrl, ui, calls, ns = self.build(ws, {("IP", "10.0.0.5"): MSG["ESP32"]}, present=[], wifi=("10.0.0.5", "pw"))
        ctrl.attach("10.0.0.5", ip=True)
        self.sync(ns, ws)
        self.assertEqual((ctrl.log, ui.messages), ([], []))


class CatalogTests(unittest.TestCase):
    """Die neuen Meldungen stehen im Quelltext und sind in allen Sprachen uebersetzt (echter Uebersetzer, keine Platzhalter uebrig)"""

    def test_texts_in_source_and_all_languages(self):
        from _web import web_i18n
        web_i18n.load_catalog(force=True)
        values = {"want": "ESP32", "have": "Pico", "port": "COM7"}
        for text in (T_OTHER_TYPE, T_UNREACHABLE, T_WARN_TYPE):
            self.assertIn(text, SRC, "Text fehlt in webmobaledlib.py: %s" % text[:40])
            german = text.format(**{k: v for k, v in values.items() if "{" + k + "}" in text})
            seen = set()
            for language in range(0, 7):
                with web_i18n.use_language(language):
                    out = web_i18n.tr(text, **values)
                self.assertNotRegex(out, r"\{\w+\}", "Platzhalter nicht ersetzt (Sprache %d)" % language)
                for key, value in values.items():
                    if "{" + key + "}" in text:
                        self.assertIn(value, out, "Wert %s fehlt (Sprache %d)" % (key, language))
                if language == 0:
                    self.assertEqual(out, german)
                else:
                    self.assertNotEqual(out, german, "Sprache %d nicht uebersetzt: %s" % (language, text[:40]))
                seen.add(out)
            self.assertEqual(len(seen), 7, "zwei Sprachen haben denselben Text")


if __name__ == "__main__":
    unittest.main(verbosity=2)
