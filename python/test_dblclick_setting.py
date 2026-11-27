# Datei-Version: 1.00 (2026-11-27) - test_dblclick_setting.py
# ----------------------------------------------------------------------------------------------
# Name:           test_dblclick_setting.py
# Path:           test_dblclick_setting.py
# Version:        1.00
# Last Update:    2026-11-27
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-27  Neu: Doppelklick auf Name und Beleuchtung oeffnet die Makroauswahl (web_layout 1.23): Standard an, ein alter gespeicherter Wert aus wird einmal auf an gesetzt, danach gilt die Wahl des Anwenders, der Anfaenger Modus ist immer an
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_dblclick_setting.py

Prueft web_layout.get_dblclick mit einem Ersatz fuer die Konfiguration (ein Woerterbuch)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from _web import web_layout as WL  # noqa: E402


class FakeCtrl:
    def __init__(self, **values):
        self.values = dict(values)

    def getConfigData(self, key):
        return self.values.get(key)

    def setConfigData(self, key, value):
        self.values[key] = value


class DblClickSettingTests(unittest.TestCase):
    def test_default_is_on(self):
        self.assertTrue(WL.get_dblclick(FakeCtrl()))

    def test_old_stored_off_is_set_to_on_once(self):
        ctrl = FakeCtrl(WebDblClickMacro=False)                       # vor V5.27 gespeichert (Standard war aus)
        self.assertTrue(WL.get_dblclick(ctrl))
        self.assertIs(ctrl.values["WebDblClickMacro"], True)
        self.assertTrue(ctrl.values[WL.DBLCLICK_MIGRATED_KEY])

    def test_choice_of_the_user_after_the_migration_stays(self):
        ctrl = FakeCtrl(WebDblClickMacro=False)
        self.assertTrue(WL.get_dblclick(ctrl))                        # Umstellung
        ctrl.setConfigData("WebDblClickMacro", False)                 # der Anwender schaltet danach selbst aus (Programm Einstellungen)
        self.assertFalse(WL.get_dblclick(ctrl))
        self.assertFalse(WL.get_dblclick(ctrl))                       # und es bleibt aus

    def test_stored_on_sets_the_marker_so_a_later_off_stays(self):
        ctrl = FakeCtrl(WebDblClickMacro=True)
        self.assertTrue(WL.get_dblclick(ctrl))
        ctrl.setConfigData("WebDblClickMacro", False)
        self.assertFalse(WL.get_dblclick(ctrl))

    def test_beginner_mode_is_always_on(self):
        ctrl = FakeCtrl(BeginnerMode=True, WebDblClickMacro=False, **{WL.DBLCLICK_MIGRATED_KEY: True})
        self.assertTrue(WL.get_dblclick(ctrl))

    def test_unwritable_config_does_not_break(self):
        class Broken(FakeCtrl):
            def setConfigData(self, key, value):
                raise OSError("nicht schreibbar")
        self.assertFalse(WL.get_dblclick(Broken(WebDblClickMacro=False)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
