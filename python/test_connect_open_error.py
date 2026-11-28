# Datei-Version: 1.00 (2026-11-28) - test_connect_open_error.py
# ----------------------------------------------------------------------------------------------
# Name:           test_connect_open_error.py
# Path:           test_connect_open_error.py
# Version:        1.00
# Last Update:    2026-11-28
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-28  Neu: Verbinden scheitert beim Oeffnen: Geraeteauswahl ohne Rueckfrage, wenn der Anschluss fehlt; Ja/Nein mit Grund, wenn er vorhanden ist (web_serial 1.34)
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_connect_open_error.py  (mit dem Python von venv_web: braucht pyserial)

Benutzt die echte Funktion SerialMixin._connect aus _web/web_serial.py. Ersetzt werden: das Oeffnen des Anschlusses (scheitert immer), die Anschlussliste des Rechners
(serial.tools.list_ports.comports), die Meldung (_msg) und die Module der Geraeteauswahl (proggen.M07_COM_Port_New, proggen.M25_Columns).
Geprueft wird:
  * Anschluss am Rechner nicht vorhanden: keine Meldung, die Geraeteauswahl oeffnet sich sofort; mit gewaehltem Anschluss wird neu verbunden,
  * stilles Verbinden (quiet) und fehlender Anschluss: weder Meldung noch Geraeteauswahl,
  * Anschluss vorhanden, aber nicht zu oeffnen: Meldung mit Ja/Nein (4 + 32) und dem Grund; Ja oeffnet die Geraeteauswahl, Nein nicht,
  * der neue Text ist in sechs Sprachen uebersetzt (echter Uebersetzer)."""
import os
import sys
import types
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from _web import web_serial  # noqa: E402

BUSY_TEXT = "Der Port ist vorhanden, lässt sich aber nicht öffnen. Wahrscheinlich benutzt ihn gerade ein anderes Programm (zum Beispiel ein Serial Monitor oder die ARDUINO IDE)."


class Ctl(web_serial.SerialMixin):
    """Kleinster Controller um den echten SerialMixin; Oeffnen scheitert immer"""

    def __init__(self, answer=None):
        self._serial_init()
        self.cfg = {"serportname": "COM3"}
        self.MacroDef = None
        self.messages = []
        self.answer = answer

    def getConfigData(self, key):
        return self.cfg.get(key, "")

    def setConfigData(self, key, value):
        self.cfg[key] = value

    def set_connectstatusmessage(self, text, fg="black"):
        pass

    def _open_serial(self, serial_module, port):
        raise OSError("could not open port '%s'" % port)

    def _msg(self, text, title, kind=16):
        self.messages.append((text, title, kind))
        return None if self.quiet else self.answer


def comports(*names):
    return lambda include_links=False: [types.SimpleNamespace(device=n) for n in names]


class OpenErrorTests(unittest.TestCase):
    def setUp(self):
        self.dialog_calls = []
        self.dialog_result = (False, " ")
        m07 = types.ModuleType("proggen.M07_COM_Port_New")
        m07.Device_Dialog_Open = False

        def show(col, port):
            self.dialog_calls.append((col, port))
            return self.dialog_result
        m07.Show_USB_Port_Dialog = show
        m25 = types.ModuleType("proggen.M25_Columns")
        m25.COMPort_COL = 7
        import proggen
        self.patches = [mock.patch.dict(sys.modules, {"proggen.M07_COM_Port_New": m07, "proggen.M25_Columns": m25}),
                        mock.patch.object(proggen, "M07_COM_Port_New", m07, create=True),
                        mock.patch.object(proggen, "M25_Columns", m25, create=True)]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()

    def test_missing_port_opens_dialog_without_question(self):
        ctl = Ctl()
        with mock.patch("serial.tools.list_ports.comports", comports("COM5")):
            self.assertFalse(ctl._connect("COM3"))
        self.assertEqual(ctl.messages, [])
        self.assertEqual(self.dialog_calls, [(7, " ")])

    def test_missing_port_dialog_choice_connects_again(self):
        ctl = Ctl()
        self.dialog_result = (True, "COM5")
        tried = []
        original = ctl._connect

        def spy(port=None):
            tried.append(port)
            if port == "COM5":
                return True
            return original(port)
        ctl._connect = spy
        with mock.patch("serial.tools.list_ports.comports", comports("COM5")):
            self.assertTrue(ctl._connect("COM3"))
        self.assertEqual(tried, ["COM3", "COM5"])

    def test_missing_port_quiet_no_dialog(self):
        ctl = Ctl()
        ctl.quiet = True
        with mock.patch("serial.tools.list_ports.comports", comports()):
            self.assertFalse(ctl._connect("COM3"))
        self.assertEqual(ctl.messages, [])
        self.assertEqual(self.dialog_calls, [])

    def test_present_port_asks_yes_no_with_reason(self):
        ctl = Ctl(answer=7)                                   # Nein
        with mock.patch("serial.tools.list_ports.comports", comports("COM3")):
            self.assertFalse(ctl._connect("COM3"))
        self.assertEqual(len(ctl.messages), 1)
        text, title, kind = ctl.messages[0]
        self.assertEqual(kind, 4 + 32)
        self.assertIn(BUSY_TEXT, text)
        self.assertIn("COM3", text)
        self.assertEqual(self.dialog_calls, [])

    def test_present_port_yes_opens_dialog(self):
        ctl = Ctl(answer=6)                                   # Ja
        with mock.patch("serial.tools.list_ports.comports", comports("com3")):          # Schreibweise egal
            self.assertFalse(ctl._connect("COM3"))
        self.assertEqual(len(ctl.messages), 1)
        self.assertEqual(self.dialog_calls, [(7, " ")])

    def test_connection_state_reset(self):
        ctl = Ctl()
        with mock.patch("serial.tools.list_ports.comports", comports()):
            ctl._connect("COM3")
        self.assertIsNone(ctl.arduino)
        self.assertEqual(ctl.ARDUINO_current_portname, "")


class TranslationTests(unittest.TestCase):
    def test_all_languages(self):
        from _web import web_i18n as I
        for n in range(1, 7):
            with I.use_language(n):
                self.assertNotEqual(I.tr(BUSY_TEXT), BUSY_TEXT, "Sprache %d" % n)
        with I.use_language(0):
            self.assertEqual(I.tr(BUSY_TEXT), BUSY_TEXT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
