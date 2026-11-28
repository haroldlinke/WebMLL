# Datei-Version: 1.04 (2026-11-28) - test_macro_tree_dblclick.py
# ----------------------------------------------------------------------------------------------
# Name:           test_macro_tree_dblclick.py
# Path:           test_macro_tree_dblclick.py
# Version:        1.04
# Last Update:    2026-11-28
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.04  2026-11-28  Doppelklick ohne Knoten in der Naehe uebernimmt nichts (frueher: die vorher gewaehlte Zeile); Luecken zwischen Zeilen gehoeren der naechsten Zeile (JS)
#   1.03  2026-11-28  Beschreibung und Makrotext haben feste Hoehe (der Dialog waechst bei der Auswahl nicht, die Zeilen verrutschen nicht)
#   1.02  2026-11-28  Doppelklick wirkt auch auf nicht gewaehlte Knoten (on_dblclick mit data-node-id), keine Textmarkierung (user-select: none)
#   1.01  2026-11-28  Funktionstest von do_ok (aus dem Quelltext geholt): Makro uebernehmen, Gruppe auf- und zuklappen, nichts gewaehlt = Hinweis
#   1.00  2026-11-28  Neu: Doppelklick in der Makroauswahl (web_macro_tree 1.14): der Baum hat no-selection-unset, der Doppelklick ruft do_ok
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_macro_tree_dblclick.py

Prueft am Quelltext von web_macro_tree._tree_async (ohne Browser): Der Baum bekommt die Eigenschaft no-selection-unset VOR dem Doppelklick-Ereignis,
und der Doppelklick ruft do_ok. Ohne die Eigenschaft sendet Quasar beim zweiten Klick eines Doppelklicks auf den gewaehlten Knoten update:selected mit
null, on_select(None) loescht die Auswahl und do_ok meldet 'Bitte ein Makro auswaehlen.'. Zusaetzlich: die mitgelieferte Quasar-Version kennt die Eigenschaft."""
import ast
import glob
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

SOURCE = os.path.join(ROOT, "_web", "web_macro_tree.py")


def tree_calls():
    """Aufrufe tree.props(...) und tree.on(...) in _tree_async in der Reihenfolge des Quelltexts: [(Zeile, Name, Argumente als Quelltext)]"""
    with open(SOURCE, "r", encoding="utf-8") as fh:
        module = ast.parse(fh.read())
    func = next(n for n in ast.walk(module) if isinstance(n, ast.AsyncFunctionDef) and n.name == "_tree_async")
    out = []
    for node in ast.walk(func):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) \
                and node.func.value.id == "tree" and node.func.attr in ("props", "on"):
            out.append((node.lineno, node.func.attr, [ast.unparse(a) for a in node.args]))
    return sorted(out)


def load_nested(name, namespace):
    """Verschachtelte Funktion aus _tree_async holen und mit Ersatzobjekten im Namensraum ausfuehren"""
    with open(SOURCE, "r", encoding="utf-8") as fh:
        source = fh.read()
    module = ast.parse(source)
    func = next(n for n in ast.walk(module) if isinstance(n, ast.AsyncFunctionDef) and n.name == "_tree_async")
    node = next(n for n in ast.walk(func) if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), SOURCE, "exec"), namespace)
    return namespace[name]


def load_do_ok(ctx, toggle, dlg, ui):
    return load_nested("do_ok", {"ctx": ctx, "toggle": toggle, "dlg": dlg, "ui": ui})


class FakeEvent:
    def __init__(self, args):
        self.args = args


class FakeTree:
    def __init__(self):
        self.selected = []

    def select(self, nid):
        self.selected.append(nid)


class FakeDialog:
    def __init__(self):
        self.result = "offen"

    def submit(self, value):
        self.result = value


class FakeUi:
    def __init__(self):
        self.messages = []

    def notify(self, text, **kwargs):
        self.messages.append(text)


class DoOkTests(unittest.TestCase):
    def run_ok(self, node):
        toggled, dlg, ui = [], FakeDialog(), FakeUi()
        load_do_ok({"selected": node}, toggled.append, dlg, ui)()
        return toggled, dlg, ui

    def test_double_click_on_macro_submits_its_row(self):
        toggled, dlg, ui = self.run_ok({"id": "m1", "leaf": True, "row": 42})
        self.assertEqual(dlg.result, 42)
        self.assertEqual(toggled, [])

    def test_double_click_on_group_toggles_it(self):
        group = {"id": "g1", "leaf": False, "row": 0}
        toggled, dlg, ui = self.run_ok(group)
        self.assertEqual(toggled, [group])
        self.assertEqual(dlg.result, "offen")

    def test_nothing_selected_gives_a_hint(self):
        toggled, dlg, ui = self.run_ok(None)
        self.assertEqual(dlg.result, "offen")
        self.assertEqual(len(ui.messages), 1)


class OnDblClickTests(unittest.TestCase):
    def run_dbl(self, args):
        by_id, tree, calls = {"n1": {"id": "n1"}, "n2": {"id": "n2"}}, FakeTree(), []
        on_dblclick = load_nested("on_dblclick", {"by_id": by_id, "tree": tree, "on_select": lambda nid: calls.append(("select", nid)),
                                                  "do_ok": lambda: calls.append(("ok",))})
        on_dblclick(FakeEvent(args))
        return tree, calls

    def test_unselected_node_is_selected_then_ok(self):
        tree, calls = self.run_dbl("n2")
        self.assertEqual(tree.selected, ["n2"])
        self.assertEqual(calls, [("select", "n2"), ("ok",)])

    def test_no_node_near_the_mouse_does_nothing(self):
        """Sonst wuerde die vorher gewaehlte Zeile uebernommen, nicht die doppelt angeklickte"""
        for args in (None, "gibt_es_nicht", 5):
            tree, calls = self.run_dbl(args)
            self.assertEqual(tree.selected, [])
            self.assertEqual(calls, [])


class MacroTreeDblClickTests(unittest.TestCase):
    def test_description_areas_have_fixed_height(self):
        """Waechst der (zentrierte) Dialog bei der Auswahl, rutschen die Zeilen zwischen den beiden Klicks eines Doppelklicks: der zweite Klick trifft eine andere Zeile"""
        with open(SOURCE, "r", encoding="utf-8") as fh:
            lines = [l for l in fh.read().splitlines() if l.lstrip().startswith(("descr = ui.label", "detail = ui.label"))]
        self.assertEqual(len(lines), 2)
        for line in lines:
            self.assertIn("height: ", line)
            self.assertNotIn("min-height", line)
            self.assertNotIn("max-height", line)

    def test_tree_does_not_unselect_on_click(self):
        props = [c for c in tree_calls() if c[1] == "props" and "'no-selection-unset'" in c[2]]
        self.assertEqual(len(props), 1, "tree.props('no-selection-unset') fehlt oder steht mehrfach")

    def test_dblclick_calls_do_ok(self):
        dbl = [c for c in tree_calls() if c[1] == "on" and c[2] and c[2][0] == "'dblclick'"]
        self.assertEqual(len(dbl), 1)
        self.assertEqual(dbl[0][2][1], "on_dblclick")

    def test_node_id_is_sent_by_the_browser_and_text_selection_is_off(self):
        with open(SOURCE, "r", encoding="utf-8") as fh:
            source = fh.read()
        self.assertIn(':data-node-id="props.node.id"', source)
        self.assertIn("dataset.nodeId", source)
        self.assertIn("dist = 7", source)                 # Luecke zwischen zwei Zeilen: naechste Zeile bis 6 Pixel
        self.assertIn("user-select: none", source)

    def test_prop_is_set_before_the_event_is_bound(self):
        calls = tree_calls()
        prop_line = next(c[0] for c in calls if c[1] == "props" and "'no-selection-unset'" in c[2])
        dbl_line = next(c[0] for c in calls if c[1] == "on" and c[2] and c[2][0] == "'dblclick'")
        self.assertLess(prop_line, dbl_line)

    def test_quasar_knows_the_property(self):
        try:
            import nicegui
        except ImportError:
            self.skipTest("nicegui nicht installiert")
        files = glob.glob(os.path.join(os.path.dirname(nicegui.__file__), "static", "quasar.umd.js"))
        if not files:
            self.skipTest("quasar.umd.js nicht gefunden")
        with open(files[0], "r", encoding="utf-8", errors="replace") as fh:
            self.assertIn("noSelectionUnset", fh.read())


if __name__ == "__main__":
    unittest.main()
