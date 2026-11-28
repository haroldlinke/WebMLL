# Datei-Version: 1.03 (2026-11-28) - test_servo_slider.py
# ----------------------------------------------------------------------------------------------
# Name:           test_servo_slider.py
# Path:           test_servo_slider.py
# Version:        1.03
# Last Update:    2026-11-28
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-28  Neu: Regler der Seite Servo Einstellungen sendet nur die neueste Position, mit der normalen Pause, ohne Stau (web_servotest 2.12)
#   1.01  2026-11-28  Anschluss ueber 2 / unter 0 geht zur naechsten / vorigen LED Nummer (web_servotest 2.13)
#   1.02  2026-11-28  Mit echtem NiceGUI (Client, ui.number): nach dem Weiterschalten geht der neue Anschluss (0 bzw. 2) an den Browser, nicht 3 oder -1 (web_servotest 2.14)
#   1.03  2026-11-28  Tasten < und > gedrueckt halten: weiterlaufen, Stufen, Endpunkt, Loslassen; Knopf-Ereignisse mit echtem NiceGUI (web_servotest 2.15)
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_servo_slider.py

Prueft mit dem echten ServoModel (web_servotest.py) und einem Ersatz-Controller mit Sendewarteschlange:
  * eine Reglerbewegung bei leerer Warteschlange geht sofort hinaus, mit send_to_ARDUINO (normale Pause), nicht mit send_to_ARDUINO_servo,
  * viele Bewegungen, waehrend die vorige Nachricht unterwegs ist, ergeben genau eine Nachricht mit der neuesten Position (kein Stau),
  * die Befehle zum Konfigurieren und das Waehlen des Servos gehen weiter mit send_to_ARDUINO_servo,
  * Verlassen der Seite verwirft eine wartende Position; beim Konfigurieren (min_max_active) wird keine Reglerposition gesendet,
  * die Zeitgeber der Seite werden gemeinsam ein- und ausgeschaltet (build mit MagicMock statt nicegui)."""
import os
import sys
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from _web import web_servotest as S1  # noqa: E402


class FakeCtrl:
    """Sendewarteschlange: busy = die vorige Nachricht ist noch unterwegs"""

    def __init__(self):
        self.max_ledcnt_list = ["20"]
        self.config = {}
        self.normal, self.servo = [], []
        self.busy = False
        self.mobaledlib_version = 2

    def getConfigData(self, key):
        return self.config.get(key, "")

    def setConfigData(self, key, value):
        self.config[key] = value

    def SaveConfigData(self):
        pass

    def get_lednum_offset_for_channel(self, channel):
        return 0

    def tx_idle(self):
        return not self.busy

    def send_to_ARDUINO(self, message):
        self.normal.append(message)

    def send_to_ARDUINO_servo(self, message):
        self.servo.append(message)

    def ARDUINO_begin_direct_mode(self):
        pass

    def ARDUINO_end_direct_mode(self):
        pass

    def is_connection_open(self):
        return True


def position_of(message):
    return int(message.split()[2], 16)                    # '#L 0001 7c 00 00 01' -> Anschluss 0


class SliderTests(unittest.TestCase):
    def setUp(self):
        self.ctrl = FakeCtrl()
        self.m = S1.ServoModel(self.ctrl)

    def test_idle_sends_at_once_with_normal_pause(self):
        msg = self.m.set_position(150)
        self.assertIsNotNone(msg)
        self.assertEqual(self.ctrl.normal, [msg])
        self.assertEqual(self.ctrl.servo, [])
        self.assertEqual(position_of(msg), 150)

    def test_busy_only_latest_position(self):
        self.ctrl.busy = True
        for p in range(100, 160, 5):
            self.assertIsNone(self.m.set_position(p))
        self.assertEqual(self.ctrl.normal, [])
        self.assertIsNone(self.m.send_pending_position())        # noch unterwegs: nichts
        self.ctrl.busy = False
        msg = self.m.send_pending_position()
        self.assertEqual(position_of(msg), 155)
        self.assertEqual(len(self.ctrl.normal), 1)
        self.assertIsNone(self.m.send_pending_position())        # schon gesendet: nichts mehr

    def test_slider_stops_wiggle(self):
        self.m.start_wig()
        self.assertGreater(self.m.wig_count, 0)
        self.m.set_position(130)
        self.assertEqual(self.m.wig_count, 0)

    def test_select_and_config_keep_servo_pause(self):
        self.m.send_select_current_module()
        self.m.send_value_to_current(S1.SRV_MIN_MAX)
        self.assertEqual(len(self.ctrl.servo), 2)
        self.assertEqual(self.ctrl.normal, [])

    def test_leave_drops_pending(self):
        self.ctrl.busy = True
        self.m.set_position(140)
        self.m.leave(quiet=True)
        self.ctrl.busy = False
        self.assertIsNone(self.m.send_pending_position())

    def test_no_slider_during_config(self):
        self.ctrl.busy = True
        self.m.set_position(140)
        self.m.min_max_active = True
        self.ctrl.busy = False
        self.assertIsNone(self.m.send_pending_position())

    def test_constants(self):
        self.assertEqual(S1.SERVO_RATE, 0.05)
        self.assertEqual(S1.POSITION_TICK, 0.05)
        self.assertEqual(S1.TICK, 0.1)                           # Pfeiltasten und Wackeln unveraendert


class ModuleWrapTests(unittest.TestCase):
    """Anschluss: Pfeil hoch bei 2 -> naechste LED Nummer, Anschluss 0; Pfeil runter bei 0 -> vorige LED Nummer, Anschluss 2 (20 LEDs: 0 bis 19)"""

    def setUp(self):
        self.ctrl = FakeCtrl()
        self.m = S1.ServoModel(self.ctrl)

    def test_up_from_2(self):
        self.m.address, self.m.module = 5, 2
        self.m.module_changed(3)
        self.assertEqual((self.m.address, self.m.module), (6, 0))
        self.assertEqual((self.ctrl.config["ServoAddress"], self.ctrl.config["ServoChannel"]), (6, 0))
        self.assertTrue(self.ctrl.servo[0].startswith("#L 0006 "))                # neuer Servo gewaehlt

    def test_up_at_last_led(self):
        self.m.address, self.m.module = 19, 2
        self.m.module_changed(3)
        self.assertEqual((self.m.address, self.m.module), (19, 2))

    def test_down_from_0(self):
        self.m.address, self.m.module = 5, 0
        self.m.module_changed(-1)
        self.assertEqual((self.m.address, self.m.module), (4, 2))

    def test_down_at_led_0(self):
        self.m.address, self.m.module = 0, 0
        self.m.module_changed(-1)
        self.assertEqual((self.m.address, self.m.module), (0, 0))

    def test_normal_steps(self):
        self.m.address, self.m.module = 5, 0
        self.m.module_changed(1)
        self.assertEqual((self.m.address, self.m.module), (5, 1))

    def test_field_allows_minus1_and_3(self):
        fake = mock.MagicMock()
        with mock.patch.dict(sys.modules, {"nicegui": fake}):
            S1.build(FakeCtrl())
        channel = [c for c in fake.ui.number.call_args_list if c.kwargs.get("label") == "Anschluss"][0]
        self.assertEqual((channel.kwargs["min"], channel.kwargs["max"]), (-1, 3))

    def test_translation(self):
        from _web import web_i18n as I
        for n in range(1, 7):
            with I.use_language(n):
                self.assertNotEqual(I.tr(S1.TEXT_MODULE_WRAP), S1.TEXT_MODULE_WRAP, "Sprache %d" % n)


class Clock:
    def __init__(self):
        self.t = 100.0

    def __call__(self):
        return self.t


class HoldTests(unittest.TestCase):
    """Tasten < und > neben dem Regler gedrueckt halten (HOLD_STAGES: ab 0,4 s 1, ab 1,5 s 2, ab 3 s 5 Schritte je Takt)"""

    def setUp(self):
        self.ctrl = FakeCtrl()
        self.clock = Clock()
        self.m = S1.ServoModel(self.ctrl, now=self.clock)
        self.m.position = 100

    def ticks(self, seconds):
        n = int(round(seconds / S1.POSITION_TICK))
        for _ in range(n):
            self.clock.t += S1.POSITION_TICK
            self.m.hold_tick()

    def test_click_is_one_step(self):
        self.m.hold_press(1)
        self.m.hold_release(1)
        self.ticks(1.0)
        self.assertEqual(self.m.position, 101)

    def test_first_pause(self):
        self.m.hold_press(1)
        self.ticks(0.35)
        self.assertEqual(self.m.position, 101)

    def test_stages(self):
        self.assertEqual(S1.HOLD_STAGES, ((0.4, 1), (1.5, 2), (3.0, 5)))
        self.m.hold_press(-1)
        self.clock.t += 0.5
        self.assertEqual(self.m.hold_step_size(), 1)
        self.clock.t += 1.1
        self.assertEqual(self.m.hold_step_size(), 2)
        self.clock.t += 1.5
        self.assertEqual(self.m.hold_step_size(), 5)

    def test_runs_and_stops_on_release(self):
        self.m.hold_press(1)
        self.ticks(1.0)
        moved = self.m.position
        self.assertGreater(moved, 105)
        self.m.hold_release(1)
        self.ticks(1.0)
        self.assertEqual(self.m.position, moved)

    def test_stops_at_end(self):
        self.m.hold_press(1)
        self.ticks(10.0)
        self.assertEqual(self.m.position, S1.SERVO_SCALE_MAX)
        self.assertEqual(self.m.hold_direction, 0)
        self.m.position = S1.SERVO_SCALE_MIN + 3
        self.m.hold_press(-1)
        self.ticks(10.0)
        self.assertEqual(self.m.position, S1.SERVO_SCALE_MIN)

    def test_release_of_other_key_ignored(self):
        self.m.hold_press(1)
        self.m.hold_release(-1)
        self.assertEqual(self.m.hold_direction, 1)

    def test_not_during_config_and_leave_stops(self):
        self.m.min_max_active = True
        self.assertIsNone(self.m.hold_press(1))
        self.assertEqual(self.m.position, 100)
        self.m.min_max_active = False
        self.m.hold_press(1)
        self.m.leave(quiet=True)
        self.assertEqual(self.m.hold_direction, 0)

    def test_sends_latest_without_backlog(self):
        self.ctrl.busy = True
        self.m.hold_press(1)
        self.ticks(2.0)
        self.assertEqual(self.ctrl.normal, [])
        self.ctrl.busy = False
        msg = self.m.send_pending_position()
        self.assertEqual(position_of(msg), self.m.position)

    def test_translation(self):
        from _web import web_i18n as I
        for n in range(1, 7):
            with I.use_language(n):
                self.assertNotEqual(I.tr(S1.TEXT_HOLD), S1.TEXT_HOLD, "Sprache %d" % n)


class RealNiceGuiTests(unittest.TestCase):
    """Seite mit echten NiceGUI-Elementen (ohne Server): das Ereignis des Browsers (Anschluss 3 bzw. -1) wird eingespielt, geprueft wird, was an den Browser zurueckgeht.
    Ursache des Fehlers in 2.13: ui.number hat LOOPBACK = False; ein im eigenen Aenderungsereignis gesetzter Wert wurde nicht gesendet, im Feld blieb 3 oder -1 stehen."""

    def _run(self, address, module, browser_value):
        import warnings
        from nicegui import Client
        from nicegui.page import page
        from nicegui.elements.number import Number
        client = Client(page("/"))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)                  # run_javascript ohne verbundenen Browser
            with client:
                pg = S1.build(FakeCtrl())
        pg.model.address, pg.model.module = address, module
        fields = {e.props.get("label"): e for e in client.elements.values() if isinstance(e, Number)}
        sent = {}
        for f in fields.values():
            f._is_safe_to_interact = lambda: True
        client.outbox.enqueue_update = lambda el: sent.__setitem__(el.props.get("label"), el)
        field = fields["Anschluss"]
        listener = [k for k, l in field._event_listeners.items() if l.type == "update:modelValue"][0]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            field._handle_event({"listener_id": listener, "args": browser_value})
        out = {label: el._to_dict()["props"].get("model-value") for label, el in sent.items()}
        return pg.model, out

    def test_hold_buttons_events(self):
        import warnings
        from nicegui import Client
        from nicegui.page import page
        from nicegui.elements.button import Button
        client = Client(page("/"))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            with client:
                pg = S1.build(FakeCtrl())
        buttons = {e.props.get("icon"): e for e in client.elements.values() if isinstance(e, Button)}
        right = buttons["chevron_right"]
        types_ = sorted(l.type for l in right._event_listeners.values())
        self.assertEqual(types_, ["pointercancel", "pointerdown", "pointerleave", "pointerup"])        # kein click mehr (sonst doppelter Schritt)
        listeners = {l.type: k for k, l in right._event_listeners.items()}
        start = pg.model.position
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            right._handle_event({"listener_id": listeners["pointerdown"], "args": {}})
        self.assertEqual((pg.model.position, pg.model.hold_direction), (start + 1, 1))
        right._handle_event({"listener_id": listeners["pointerleave"], "args": {}})
        self.assertEqual(pg.model.hold_direction, 0)

    def test_up_sends_0(self):
        model, out = self._run(5, 2, 3)
        self.assertEqual((model.address, model.module), (6, 0))
        self.assertEqual(out.get("Anschluss"), "0")
        self.assertEqual(out.get("LED Nummer"), "6")

    def test_down_sends_2(self):
        model, out = self._run(5, 0, -1)
        self.assertEqual((model.address, model.module), (4, 2))
        self.assertEqual(out.get("Anschluss"), "2")
        self.assertEqual(out.get("LED Nummer"), "4")

    def test_up_at_last_led_sends_2(self):
        model, out = self._run(19, 2, 3)
        self.assertEqual((model.address, model.module), (19, 2))
        self.assertEqual(out.get("Anschluss"), "2")


class BuildTests(unittest.TestCase):
    def test_timers_switch_together(self):
        fake = mock.MagicMock()
        timers = []

        def make_timer(interval, fn):
            t = mock.Mock(interval=interval, callback=fn, active=True)
            timers.append(t)
            return t
        fake.ui.timer.side_effect = make_timer
        ctrl = FakeCtrl()
        with mock.patch.dict(sys.modules, {"nicegui": fake}):
            page = S1.build(ctrl)
        self.assertEqual(sorted(t.interval for t in timers), [0.05, 0.1])
        self.assertTrue(all(t.active is False for t in timers))
        page.tab_selected()
        self.assertTrue(all(t.active is True for t in timers))
        page.tab_unselected()
        self.assertTrue(all(t.active is False for t in timers))
        slider_on = [c for c in fake.ui.slider.return_value.props.return_value.classes.return_value.on.call_args_list]
        self.assertEqual(slider_on[0].kwargs.get("throttle"), 0.05)


if __name__ == "__main__":
    unittest.main(verbosity=2)
