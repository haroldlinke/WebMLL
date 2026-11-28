# Datei-Version: 1.00 (2026-11-28) - test_lm_channels.py
# ----------------------------------------------------------------------------------------------
# Name:           test_lm_channels.py
# Path:           test_lm_channels.py
# Version:        1.00
# Last Update:    2026-11-28
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-28  Neu: LM-Ausgang als Auswahl der Ausgaenge aus der Startmeldung, hoechste LED Nummer = Anzahl - 1 (web_servotest 2.11, web_servotest2 1.06, web_soundtest 1.06)
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_lm_channels.py

Prueft mit den echten Modellen der Seiten Servo Test 1, Servo Test 2 und Sound Test, dass
  * der LM-Ausgang nur die Ausgaenge anbietet, die die Lichtmaschine in der Startmeldung meldet (ohne Startmeldung 0 bis 3),
  * die LED Nummer (Adresse) hoechstens Anzahl der LEDs des Ausgangs - 1 ist (20 LEDs: 0 bis 19),
  * gespeicherte, zu grosse Werte beim Betreten der Seite eingepasst und gemerkt werden,
  * die Oberflaeche eine Auswahlliste baut und Liste und Maximum bei refresh neu setzt (nicegui.ui durch MagicMock ersetzt),
  * der neue Hinweistext in allen sechs Sprachen uebersetzt ist (echter Uebersetzer).
Die Lichtmaschine wird durch ein Ersatzobjekt ersetzt."""
import os
import sys
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from _web import web_servotest as S1  # noqa: E402
from _web import web_servotest2 as S2  # noqa: E402
from _web import web_soundtest as ST  # noqa: E402


class FakeCtrl:
    """Ersatz fuer den Controller: Startmeldung (max_ledcnt_list), gemerkte Werte, Senden"""

    def __init__(self, leds=None, config=None):
        self.max_ledcnt_list = [str(x) for x in (leds or [])]
        self.config = dict(config or {})
        self.saved = 0
        self.sent = []
        self.mobaledlib_version = 2

    def getConfigData(self, key):
        return self.config.get(key, "")

    def setConfigData(self, key, value):
        self.config[key] = value

    def SaveConfigData(self):
        self.saved += 1

    def get_lednum_offset_for_channel(self, channel):
        leds = [int(x) for x in self.max_ledcnt_list]
        return sum(leds[:channel]) if channel < len(leds) else 0

    def send_to_ARDUINO(self, message):
        self.sent.append(message)

    send_to_ARDUINO_servo = send_to_ARDUINO

    def ARDUINO_begin_direct_mode(self):
        pass

    def ARDUINO_end_direct_mode(self):
        pass

    def is_connection_open(self):
        return True


def later(delay, fn):
    return mock.Mock()


class ServoTest1Tests(unittest.TestCase):
    def test_one_channel_20_leds(self):
        m = S1.ServoModel(FakeCtrl([20]))
        self.assertEqual(m.channel_options(), [0])
        self.assertEqual(m.address_max(), 19)
        self.assertEqual(m.address_changed(25), 19)
        m.channel_changed(3)
        self.assertEqual(m.channel, 0)

    def test_without_startmessage(self):
        m = S1.ServoModel(FakeCtrl([]))
        self.assertEqual(m.channel_options(), [0, 1, 2, 3])
        self.assertEqual(m.address_max(), 32767)

    def test_stored_values_fitted(self):
        ctrl = FakeCtrl([20, 10], {"ServoLEDChannel": 5, "ServoAddress": 30})
        m = S1.ServoModel(ctrl)
        self.assertEqual((m.channel, m.address), (1, 9))
        self.assertEqual((ctrl.config["ServoLEDChannel"], ctrl.config["ServoAddress"]), (1, 9))
        self.assertEqual(m.channel_options(), [0, 1])

    def test_stored_channel_kept_without_startmessage(self):
        m = S1.ServoModel(FakeCtrl([], {"ServoLEDChannel": 5}))
        self.assertEqual(m.channel, 5)
        self.assertEqual(m.channel_options(), [0, 1, 2, 3, 4, 5])

    def test_channel_change_fits_address(self):
        m = S1.ServoModel(FakeCtrl([20, 4], {"ServoAddress": 15}))
        m.channel_changed(1)
        self.assertEqual((m.channel, m.address), (1, 3))

    def test_connect_later(self):
        ctrl = FakeCtrl([], {"ServoLEDChannel": 2, "ServoAddress": 40})
        m = S1.ServoModel(ctrl)
        ctrl.max_ledcnt_list = ["20"]                       # Startmeldung kommt nach dem Aufbau der Seite
        m.tab_selected()
        self.assertEqual((m.channel, m.address), (0, 19))
        m.leave()


class ServoTest2Tests(unittest.TestCase):
    def test_limits(self):
        ctrl = FakeCtrl([20], {"Servo2LEDChannel": 3, "Servo2Address": 50})
        m = S2.Servo2Model(ctrl)
        self.assertEqual((m.channel, m.address), (0, 19))
        self.assertEqual(m.channel_options(), [0])
        self.assertEqual(m.set_address(25), 19)
        self.assertEqual(m.set_channel(2), 0)

    def test_channel_change_fits_address(self):
        m = S2.Servo2Model(FakeCtrl([20, 4], {"Servo2Address": 15}))
        m.set_channel(1)
        self.assertEqual((m.channel, m.address), (1, 3))

    def test_connect_later(self):
        ctrl = FakeCtrl([], {"Servo2LEDChannel": 2})
        m = S2.Servo2Model(ctrl)
        self.assertEqual(m.channel_options(), [0, 1, 2, 3])
        ctrl.max_ledcnt_list = ["20"]
        m.tab_selected()
        self.assertEqual(m.channel, 0)
        m.leave()


class SoundTestTests(unittest.TestCase):
    def test_limits(self):
        ctrl = FakeCtrl([20], {"SoundLEDChannel": 3, "Sound_Address": 50})
        m = ST.SoundModel(ctrl, later=later)
        self.assertEqual((m.values["SoundLEDChannel"], m.values["Sound_Address"]), (0, 19))
        self.assertEqual(m.channel_options(), [0])
        self.assertEqual(m.set_value("Sound_Address", 25), 19)

    def test_channel_change_fits_address(self):
        m = ST.SoundModel(FakeCtrl([20, 4], {"Sound_Address": 15}), later=later)
        m.set_value("SoundLEDChannel", 1)
        self.assertEqual(m.values["Sound_Address"], 3)

    def test_connect_later(self):
        ctrl = FakeCtrl([], {"SoundLEDChannel": 2})
        m = ST.SoundModel(ctrl, later=later)
        ctrl.max_ledcnt_list = ["20"]
        m.tab_selected()
        self.assertEqual(m.values["SoundLEDChannel"], 0)
        m.leave(quiet=True)


class BuildTests(unittest.TestCase):
    """Oberflaeche mit MagicMock statt nicegui: LM-Ausgang ist eine Auswahl (ui.select), Liste und Maximum werden bei refresh gesetzt"""

    def _build(self, module, ctrl, **kw):
        fake = mock.MagicMock()
        with mock.patch.dict(sys.modules, {"nicegui": fake}):
            page = module.build(ctrl, **kw)
        return fake.ui, page

    def test_servo1(self):
        ui, page = self._build(S1, FakeCtrl([20]))
        self.assertEqual(ui.select.call_args.args[0], [0])
        maxima = [c.kwargs.get("max") for c in ui.number.call_args_list]
        self.assertIn(19, maxima)
        select = ui.select.return_value.props.return_value.classes.return_value       # field = ui.select(...).props(...).classes(...)
        select.set_options.assert_called_with([0], value=0)

    def test_servo2(self):
        ctrl = FakeCtrl([20, 10])
        ctrl.MacroDef = mock.Mock(data={})
        ui, page = self._build(S2, ctrl)
        self.assertEqual(ui.select.call_args_list[0].args[0], [0, 1])
        self.assertEqual(ui.number.call_args_list[0].kwargs["max"], 19)

    def test_sound(self):
        ctrl = FakeCtrl([20])
        ctrl.MacroDef = mock.Mock(data={})
        ui, page = self._build(ST, ctrl)
        self.assertEqual(ui.select.call_args.args[0], [0])
        self.assertEqual(ui.number.call_args_list[0].kwargs["max"], 19)


class TranslationTests(unittest.TestCase):
    TEXTS = [S1.TEXT_CHANNEL_HINT, "LM-Ausgang an dem die Servoplatine angeschlossen ist", "LM-Ausgang an dem die Soundplatine angeschlossen ist"]

    def test_same_text_everywhere(self):
        self.assertEqual(S1.TEXT_CHANNEL_HINT, S2.TEXT_CHANNEL_HINT)
        self.assertEqual(S1.TEXT_CHANNEL_HINT, ST.TEXT_CHANNEL_HINT)

    def test_all_languages(self):
        from _web import web_i18n as I
        for n in range(1, 7):
            with I.use_language(n):
                for t in self.TEXTS:
                    self.assertNotEqual(I.tr(t), t, "Sprache %d: %s" % (n, t))
        with I.use_language(0):
            for t in self.TEXTS:
                self.assertEqual(I.tr(t), t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
