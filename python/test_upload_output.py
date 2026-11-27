# Datei-Version: 1.02 (2026-11-27) - test_upload_output.py
# ----------------------------------------------------------------------------------------------
# Name:           test_upload_output.py
# Path:           test_upload_output.py
# Version:        1.02
# Last Update:    2026-11-27
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.02  2026-11-27  _open_output (M42 1.15) leert das Fenster nicht mehr
#   1.01  2026-11-27  Nach einem Rueckfall wird das Fenster nicht mehr geleert (M08 1.43, Prog_Generator 1.13: preface entfaellt)
#   1.00  2026-11-27  Neu: Log-Fenster bei Setup uebertragen: der Starttext ist uebersetzt (Prog_Generator 1.12), der Grund fuer den Rueckfall vom schnellen Upload auf das ganze Programm
#                     bleibt sichtbar, auch wenn das Fenster geleert wird (M42 1.14 Fallback_Text, M08 1.42, start_ARDUINO_program_cmd preface)
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_upload_output.py

Holt die Funktionen mit ast aus M42_Dyn_Config.py und Prog_Generator.py und fuehrt sie mit Ersatzobjekten (Ausgabefenster, Controller) aus.
Der Starttext wird mit dem echten Uebersetzer in allen Sprachen geprueft.
Nicht geprueft: das echte Ausgabefenster im Browser, ein ganzer Upload mit Hardware."""
import ast
import builtins
import logging
import os
import sys
import textwrap
import types
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def function_source(rel, name, source=None):
    source = source if source is not None else read(rel)
    found = [n for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    assert len(found) == 1, "%s: %d Funktionen %s" % (rel, len(found), name)
    return textwrap.dedent(ast.get_source_segment(source, found[0])), found[0]


class FakePage:
    def __init__(self):
        self.events = []

    def set_title(self, text):
        self.events.append(("title", text))

    def delete_text_from_textwindow(self):
        self.events.append(("delete",))

    def add_text_to_textwindow(self, text="", nl="", highlight=None):
        self.events.append(("text", text + nl))


class M42Tests(unittest.TestCase):
    NAMES = ("_t", "_page", "_out", "_open_output", "_restore_title", "_fallback", "Fallback_Text")

    def setUp(self):
        self.page = FakePage()
        controller = types.SimpleNamespace(getFramebyName=lambda name: self.page, showFramebyName=lambda name: self.page.events.append(("show", name)))
        self.ns = {"log": logging.getLogger("test_upload_output"), "PG": types.SimpleNamespace(global_controller=controller),
                   "_state": {"active": False, "off": False, "output": False, "lines": [], "fallback": False}}
        for name in self.NAMES:
            exec(compile(function_source("proggen/M42_Dyn_Config.py", name)[0], name, "exec"), self.ns)

    def test_reason_is_kept_for_m08(self):
        ns = self.ns
        ns["_open_output"]()
        ns["_out"]("Die Firmware im Gerät (COM7) wird geprüft ...")
        self.assertFalse(ns["_fallback"]("Die Firmware im Gerät passt nicht zu dieser Konfiguration. Es wird das ganze Programm hochgeladen."))
        text = ns["Fallback_Text"]()
        self.assertEqual(text.split(chr(10)), ["Die Firmware im Gerät (COM7) wird geprüft ...", "Die Firmware im Gerät passt nicht zu dieser Konfiguration. Es wird das ganze Programm hochgeladen."])
        self.assertEqual(ns["Fallback_Text"](), "", "der Text wird nur einmal geliefert")

    def test_open_output_keeps_the_start_text(self):  # 1.02
        self.ns["_open_output"]()
        self.assertNotIn(("delete",), self.page.events)
        self.assertIn(("show", "ARDUINOMonitorPage"), self.page.events)

    def test_without_fallback_nothing_is_returned(self):
        ns = self.ns
        ns["_open_output"]()
        ns["_out"]("Fertig: Die Konfiguration wurde übertragen.")
        self.assertEqual(ns["Fallback_Text"](), "")

    def test_new_attempt_forgets_the_old_lines(self):
        ns = self.ns
        ns["_open_output"]()
        ns["_out"]("alt")
        ns["_fallback"]("Grund alt")
        ns["_open_output"]()
        ns["_out"]("neu")
        ns["_fallback"]("Grund neu")
        self.assertEqual(ns["Fallback_Text"](), "neu" + chr(10) + "Grund neu")

    def test_reason_survives_a_state_reset_of_output(self):
        """Create_HeaderFile (Simulator) ruft Decide() auf und setzt output zurueck: der Grund darf dabei nicht verloren gehen"""
        ns = self.ns
        ns["_open_output"]()
        ns["_fallback"]("Grund")
        ns["_state"]["output"] = False
        self.assertEqual(ns["Fallback_Text"](), "Grund")

    def test_m08_does_not_clear_the_window_after_a_fallback(self):
        source = read("proggen/M08_ARDUINO.py")
        calls = [l for l in source.splitlines() if "start_ARDUINO_program_cmd(CommandStr" in l and not l.lstrip().startswith("#")]
        self.assertEqual(len(calls), 2)
        for line in calls:
            self.assertIn('empty_text=(FastReason == "")', line)
            self.assertNotIn("preface", line)
        self.assertEqual(len([l for l in source.splitlines() if l.strip().startswith("FastReason = M42.Fallback_Text()")]), 1)


class WindowTests(unittest.TestCase):
    def run_start(self, **kw):
        source, node = function_source("mlpyproggen/Prog_Generator.py", "start_ARDUINO_program_cmd")
        ns = {}
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name) and not hasattr(builtins, sub.id):
                ns.setdefault(sub.id, mock.MagicMock())
        ns["logging"] = mock.MagicMock()
        exec(compile(source, "start_ARDUINO_program_cmd", "exec"), ns)
        page = FakePage()
        self_ = mock.MagicMock()
        self_.controller.getFramebyName.return_value = page
        self_.controller.showFramebyName.side_effect = lambda name: page.events.append(("show", name))
        self_.execute_shell_cmd.return_value = 0
        ns["start_ARDUINO_program_cmd"](self_, "pio run", arduino_type="Left", show_intro=False, **kw)
        return page.events

    def test_empty_text_false_keeps_the_lines(self):
        events = self.run_start(empty_text=False)
        self.assertNotIn(("delete",), events)
        self.assertTrue([e for e in events if e[0] == "text"][0][1].lstrip().startswith("*"))

    def test_empty_text_true_clears_first(self):
        events = self.run_start(empty_text=True)
        self.assertEqual(events[0], ("delete",))

    def test_no_preface_parameter_any_more(self):
        _source, node = function_source("mlpyproggen/Prog_Generator.py", "start_ARDUINO_program_cmd")
        self.assertNotIn("preface", [a.arg for a in node.args.args])


class StartTextTests(unittest.TestCase):
    TEXT = "Vorbereitung des Programms gestartet"

    def test_no_english_literal_left_in_the_code(self):
        tree = ast.parse(read("mlpyproggen/Prog_Generator.py"))
        literals = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        self.assertNotIn("Preparation of Program Started", literals)
        self.assertIn(self.TEXT, literals)

    def test_translated_in_all_languages(self):
        from _web import web_i18n
        web_i18n.load_catalog(force=True)
        seen = set()
        for language in range(0, 7):
            with web_i18n.use_language(language):
                out = web_i18n.tr(self.TEXT)
            if language == 0:
                self.assertEqual(out, self.TEXT)
            else:
                self.assertNotEqual(out, self.TEXT, "Sprache %d nicht uebersetzt" % language)
            seen.add(out)
        self.assertEqual(len(seen), 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
