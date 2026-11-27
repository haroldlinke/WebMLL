# Datei-Version: 1.01 (2026-11-27) - test_hardware_dialog.py
# ----------------------------------------------------------------------------------------------
# Name:           test_hardware_dialog.py
# Path:           test_hardware_dialog.py
# Version:        1.01
# Last Update:    2026-11-27
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.01  2026-11-27  Port-Tests an web_form_comport 1.52 angepasst (nur Geraete des Typs des Blattes); Ersatzwerte fuer die Firmware-Info (_info, _boot), die seit 1.18/1.43 fehlten
#                     (die Port-Tests brachen vorher mit AttributeError ab). Zeilen mit '# v1.01'
#   1.00  2026-11-25  Neu: Tests fuer den neuen Dialog der Lichtmaschine (web_form_comport 1.13: Liste der Boards, offline, unbekannte Ports) und die Einstellungen des
#                     Blattes als Makrozeilen (headless_sheet_settings 1.00)
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_hardware_dialog.py

Benutzt die echten Funktionen von _web/web_form_comport.py (WebSelectComPort._compute_new) und headless/headless_sheet_settings.py. Ersetzt werden nur die serielle
Schnittstelle (Liste der Anschluesse), das Blatt (Zellen, Zeilen) und die Ident-Befehle an die Lichtmaschine.
Nicht geprueft: Oberflaeche (NiceGUI), echte Arbeitsmappe, Hardware."""
import os
import sys
import types
import unittest
from types import SimpleNamespace as NS
from unittest import mock

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
try:
    import serial  # noqa: F401
except ImportError:
    sys.modules["serial"] = mock.MagicMock()


# ---------------------------------------------------------------- Port-Dialog
class FakeM07:
    CheckCOMPort = None
    CheckCOMPort_Txt = None
    ports = []

    class portlist:
        @staticmethod
        def comports(include_links=False):
            return FakeM07.ports

    @staticmethod
    def Classify_Port(cp):
        return {0x2E8A: "Pico", 0x10C4: "ESP32", 0x1A86: "Nano"}.get(getattr(cp, "vid", None), "")


def make_form(board="AM328"):
    from _web import web_form_comport as W
    base_mod = types.ModuleType("fake_select_com_port")
    base_mod.__file__ = os.path.join(ROOT, "proggen", "fake.py")
    for name, value in dict(M07=FakeM07, M09=NS(Get_Language_Str=lambda s: s), M30=NS(isInitialised=lambda x: bool(x)),
                            M02=NS(HT_ESP32="ESP32", HT_PICO="PICO"), M25=NS(Page_ID="DCC"), P01=NS(), vbCritical=0, vbCr="\n",
                            InStr=lambda a, b: 0, PortNames=[], LocalComPorts=[], OldL_ComPorts=[], LocalPrintDebug=False).items():
        setattr(base_mod, name, value)
    sys.modules["fake_select_com_port"] = base_mod

    class Base:
        def ShowDialog(self):
            pass
    Base.__module__ = "fake_select_com_port"
    form = W.make_class(Base)()
    form._sheet_group = lambda: {"ESP32": "Pro", "PICO": "Pico"}.get(board, "Classic")
    form._sheet_is_uno = lambda: False  # v1.01
    form._info_refresh = lambda *a, **k: None  # v1.01: keine Abfrage ueber die Anschluesse
    form._info, form._boot, form._boot_busy = {}, {}, set()  # v1.01
    form._rows, form._sel_dev, form._prev_devs, form._old_comport, form._stored_port = [], None, None, None, ""  # v1.01
    form._fw_mode, form._fw_platform, form._sel_user = False, "", False  # v1.01
    return form


def port(dev, vid, desc="x"):
    # return NS(device=dev, vid=vid, description=desc, hwid="USB VID:PID=0000")  # v1.01 (entfallen)
    return NS(device=dev, vid=vid, pid=0x0001, serial_number="", description=desc, hwid="USB VID:PID=0000")  # v1.01: _scan liest seit web_form_comport 1.20/1.44 auch pid und serial_number


class PortDialogTests(unittest.TestCase):
    def setUp(self):
        import proggen.M07_COM_Port_New as N
        self.patches = [mock.patch.object(N, "Ident_Send_Keepalive", lambda p: None),
                        mock.patch.object(N, "_Ident_Send_Cmd", lambda *a: None),
                        mock.patch.object(N, "_Ident_Board", lambda: None)]
        for p in self.patches:
            p.start()
        FakeM07.ports = [port("COM3", 0x1A86), port("COM5", 0x2E8A), port("COM9", 0x10C4), port("COM12", 0x9999)]

    def tearDown(self):
        for p in self.patches:
            p.stop()

    def rows(self, form):
        return [(r["typ"], r["dev"], r["offline"]) for r in form._rows]

    def test_groups_and_offline(self):
        form = make_form()
        form._stored_port = "COM7"
        form._compute_new()
        # self.assertEqual(self.rows(form), [("Classic", "COM3", False), ("Classic", "COM7", True), ("Pro", "COM9", False), ("Pico", "COM5", False)])  # v1.01 (entfallen)
        self.assertEqual(self.rows(form), [("Classic", "COM3", False), ("Classic", "COM7", True)])  # v1.01: nur Geraete des Typs des Blattes
        # self.assertEqual(form._sel_dev, "COM7")                             # das Board des Blattes ist vorgewaehlt, auch offline  # v1.01 (entfallen)
        # self.assertEqual(FakeM07.CheckCOMPort, "999")                       # offline: nichts blinken lassen  # v1.01 (entfallen)
        self.assertEqual(form._sel_dev, "COM3")  # v1.01: seit web_form_comport 1.38 ist ein angeschlossenes Geraet des Typs vorgewaehlt, nicht der gespeicherte Anschluss offline
        FakeM07.ports = [p for p in FakeM07.ports if p.device != "COM3"]  # v1.01: ohne angeschlossenes Geraet des Typs
        form._sel_dev = None  # v1.01
        form._compute_new()  # v1.01
        self.assertEqual(form._sel_dev, "COM7")  # v1.01: dann der gespeicherte (offline)
        self.assertEqual(FakeM07.CheckCOMPort, "999")  # v1.01: offline: nichts blinken lassen

    def test_unknown_ports_only_with_checkbox(self):
        form = make_form()
        form._compute_new()
        self.assertNotIn("unbekannt", [r["typ"] for r in form._rows])
        form._show_unknown = True
        form._compute_new()
        self.assertIn(("unbekannt", "COM12", False), self.rows(form))

    def test_stored_unknown_port_counts_as_sheet_board(self):
        form = make_form("ESP32")
        form._stored_port = "COM12"
        form._compute_new()
        self.assertIn(("Pro", "COM12", False), self.rows(form))
        self.assertEqual(form._sel_dev, "COM12")

    def test_new_device_is_selected(self):
        form = make_form()
        form._compute_new()
        # FakeM07.ports = FakeM07.ports + [port("COM20", 0x10C4)]  # v1.01 (entfallen: ein ESP32 erscheint bei einem Classic-Blatt nicht mehr)
        FakeM07.ports = FakeM07.ports + [port("COM20", 0x1A86)]  # v1.01
        form._sel_dev = "gone"
        form._compute_new()
        self.assertEqual(form._sel_dev, "COM20")


# ---------------------------------------------------------------- Makrozeilen
class FakeSheet:
    Name = "DCC"

    def __init__(self, rows):
        self.rows = [dict(r) for r in rows]
        self.esp32_options = {}
        sheet = self

        class TK:
            def insert_rows(self, rows, idx):
                sheet.rows.insert(idx - 2, {})
        self.tksheet = TK()

    def _r(self, r):
        return self.rows[r - 3] if 0 <= r - 3 < len(self.rows) else {}

    def Cells(self, r, c):
        return NS(Value=self._r(r).get(c, ""))

    def Rows(self, r):
        row = self._r(r)

        class E:
            @property
            def Hidden(self_):
                return row.get("hidden", False)

            @Hidden.setter
            def Hidden(self_, v):
                row["hidden"] = v
        return NS(EntireRow=E())

    def Activate(self):
        pass


class SheetSettingsTests(unittest.TestCase):
    def setUp(self):
        import headless.headless_sheet_settings as H
        self.H = H
        self.ws = ws = FakeSheet([{2: "*", 7: "Licht", 9: "House(...)"}, {2: "", 9: "#define  ENABLE_STORE_STATUS()"}])

        class CD:
            def __setitem__(self, k, v):
                ws._r(k[0])[k[1]] = v
        P01 = NS(ActiveSheet=ws, Application=NS(EnableEvents=True), CellDict=CD(), Rows=ws.Rows)
        M02 = NS(FirstDat_Row=3, Enable_Col=2, Hook_CHAR=ord("*"))
        M25 = NS(Config__Col=9, Descrip_Col=7, Make_sure_that_Col_Variables_match=lambda ws=None: None)
        M30 = NS(LastUsedRowIn=lambda w: 2 + len(w.rows))
        go = types.ModuleType("headless.headless_graph_ops")
        go.delete_row = lambda w, r0: w.rows.pop(r0 - 2)
        import headless
        self.patches = [mock.patch.object(H, "_modules", lambda: (P01, M02, M25, M30)),
                        mock.patch.dict(sys.modules, {"headless.headless_graph_ops": go,
                                                      "proggen.M20_PageEvents_a_Functions": NS(Update_Start_LedNr=lambda: None)}),
                        mock.patch.object(headless, "headless_graph_ops", go, create=True)]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()

    def macros(self):
        return [(r.get(2), r.get(9)) for r in self.ws.rows]

    def test_disabled_row_is_not_set_and_gets_enabled(self):
        self.assertFalse(self.H.is_set("store_status"))
        self.assertTrue(self.H.apply("store_status", True))
        self.assertEqual(self.macros(), [("*", "House(...)"), ("*", "#define  ENABLE_STORE_STATUS()")])  # keine zweite Zeile, die vorhandene ist eingeschaltet
        self.assertTrue(self.H.is_set("store_status"))

    def test_insert_once_and_remove(self):
        self.assertTrue(self.H.apply("ldr", True))
        self.assertEqual(self.macros()[0], ("*", "#define READ_LDR"))
        self.assertFalse(self.H.apply("ldr", True))                        # schon gesetzt: keine doppelte Zeile
        self.assertEqual(sum(1 for _e, m in self.macros() if m == "#define READ_LDR"), 1)
        self.assertTrue(self.H.apply("ldr", False))
        self.assertNotIn("#define READ_LDR", [m for _e, m in self.macros()])

    def test_remove_deletes_disabled_rows_too(self):
        self.assertTrue(self.H.apply("store_status", False))
        self.assertEqual(self.macros(), [("*", "House(...)")])

    def test_legacy_options_are_migrated(self):
        self.ws.esp32_options = {"ldr": True, "store_status": False, "oled": 3}
        self.assertTrue(self.H.is_set("ldr"))                               # frueherer Eintrag gilt, bis er uebernommen ist
        self.assertTrue(self.H.migrate_legacy())
        self.assertEqual(self.ws.esp32_options, {"oled": 3})
        self.assertIn(("*", "#define READ_LDR"), self.macros())

    def test_norm_macro(self):
        self.assertEqual(self.H.norm_macro("  #define  ENABLE_STORE_STATUS() "), "#define ENABLE_STORE_STATUS")
        self.assertNotEqual(self.H.norm_macro("#define READ_LDR_DEBUG"), self.H.norm_macro("#define READ_LDR"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
