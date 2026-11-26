# Datei-Version: 1.00 (2026-11-25) - test_protocol_switch.py
# ----------------------------------------------------------------------------------------------
# Name:           test_protocol_switch.py
# Path:           test_protocol_switch.py
# Version:        1.00
# Last Update:    2026-11-25
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-25  Neu: Wechsel eines Blatts zwischen Selectrix und DCC/LNet/CAN (headless_protocol_switch 1.00), Umrechnung der Adressen, Testtasten, Pgf-Export und -Import
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_protocol_switch.py

Startet die echte Arbeitsmappe ohne Oberflaeche (wie headless/headless_start.py, mit einem leeren Datenordner im Temp-Ordner) und prueft den Wechsel zwischen Selectrix
und DCC/LNet/CAN. Nicht geprueft: Oberflaeche (Dialog der Optionen, Rueckfrage im Browser), das Excel-Programm selbst."""
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
os.environ["MLL_HEADLESS"] = "1"
os.environ["MLL_DATA_DIR"] = tempfile.mkdtemp(prefix="mll_test_")
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from headless import headless_protocol_switch as PS  # noqa: E402


class MathTests(unittest.TestCase):
    def test_roundtrip_1_to_800(self):
        for address in range(9, 801):
            channel, bit = PS.to_selectrix(address)
            self.assertTrue(0 <= channel <= 99 and 1 <= bit <= 8)
            self.assertEqual(PS.from_selectrix(channel, bit), address)

    def test_examples(self):
        self.assertEqual(PS.to_selectrix(9), (1, 1))                 # Adresse = Channel * 8 + Bitposition
        self.assertEqual(PS.to_selectrix(16), (1, 8))
        self.assertEqual(PS.to_selectrix(17), (2, 1))
        self.assertEqual(PS.to_selectrix(800), (99, 8))
        for address in (0, 1, 8, 801):                               # Channel 0 gibt es nicht: Adressen 1 bis 8 sind nicht umrechenbar
            self.assertIsNone(PS.to_selectrix(address), address)
        self.assertEqual(PS.from_selectrix(1, 1), 9)
        self.assertEqual(PS.from_selectrix(99, 8), 800)
        self.assertIsNone(PS.from_selectrix(0, 1))
        self.assertIsNone(PS.from_selectrix(100, 1))
        self.assertIsNone(PS.from_selectrix(1, 0))
        self.assertIsNone(PS.from_selectrix(1, 9))

    def test_first_number(self):
        self.assertEqual(PS._first_number("5 - 8"), 5)
        self.assertEqual(PS._first_number("17"), 17)
        self.assertIsNone(PS._first_number("SwitchD1"))
        self.assertIsNone(PS._first_number("RM 1"))
        self.assertIsNone(PS._first_number(""))

    def test_crosses(self):
        self.assertTrue(PS.crosses("DCC", "Selectrix"))
        self.assertTrue(PS.crosses("Selectrix", "CAN"))
        self.assertFalse(PS.crosses("DCC", "CAN"))
        self.assertFalse(PS.crosses("Selectrix", "Selectrix"))


class SheetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import no_tk
        no_tk.install()
        from headless.headless_app_controller import HeadlessAppController
        import userdata
        ctrl = HeadlessAppController(mainfile_dir=ROOT, command_line_args={"loaddatafile": "True", "logfilename": userdata.log_file()})
        ctrl.create_excel_application()
        from headless.headless_proggen import HeadlessProgGeneratorPage
        cls.wb = HeadlessProgGeneratorPage(ctrl).workbook
        import ExcelAPI.XLA_Application as P01
        import proggen.M02_Public as M02
        import proggen.M18_Save_Load as M18
        import proggen.M20_PageEvents_a_Functions as M20
        import proggen.M25_Columns as M25
        cls.P01, cls.M02, cls.M18, cls.M20, cls.M25 = P01, M02, M18, M20, M25
        cls.M20.Complete_Typ = lambda *a, **k: None          # kein Typ-Dialog ohne Browser

    def setUp(self):
        self.ws = next(s for s in self.wb.sheets if s.Name == "DCC")
        ts = self.ws.tksheet
        del ts.data[3:]
        if str(ts.data[0][1]) != "DCC":
            self.fail("Das Blatt DCC ist nicht im Ausgangszustand")
        self.ws.shapelist = [s for s in self.ws.shapelist if s.OnAction != "DCCSend"]
        self.ws.Activate()
        self.M25.Col_from_Sheet = ""
        self.M25.Make_sure_that_Col_Variables_match(self.ws)
        self.assertEqual(self.M25.Page_ID, "DCC")

    def tearDown(self):
        if str(self.ws.tksheet.data[0][1]) != "DCC":
            PS.convert(self.ws, "DCC")

    def fill(self, rows):
        """rows: (Adresse, Typ); DCC-Aufbau: Spalte D Adresse, E Typ, L Makro, O InCnt"""
        ts = self.ws.tksheet
        for k, (address, typ) in enumerate(rows):
            r0 = 3 + k
            while len(ts.data) <= r0:
                ts.data.append([""] * len(ts.data[0]))
            row = ts.data[r0]
            row.extend([""] * (20 - len(row)))
            row[1], row[3], row[4], row[11], row[14], row[15] = self.M02.Hook_CHAR and chr(self.M02.Hook_CHAR), address, typ, "AndreaskrRGB(#LED, #InCh)", "1", "0"
            self.M20.Update_TestButtons(r0 + 1)

    def data(self):
        return [[str(c) for c in r[:6]] for r in self.ws.tksheet.data[3:]]

    def buttons(self):
        return [(s.Name, s.TextFrame2.TextRange.Text) for s in self.ws.shapelist if s.OnAction == "DCCSend"]

    def test_analyze(self):
        self.fill([("11", "Rot"), ("17", "AnAus"), ("900", ""), ("SwitchD1", ""), ("16", "Grün")])
        info = PS.analyze(self.ws)
        self.assertEqual((info["addresses"], info["red_green"], info["on_off"], info["unconvertible"]), (4, 2, 1, 1))

    def test_analyze_addresses_below_9_cannot_be_converted(self):
        self.fill([("1", ""), ("8", ""), ("9", "")])
        self.assertEqual(PS.analyze(self.ws)["unconvertible"], 2)

    def test_no_addresses_counts_zero(self):
        self.fill([("SwitchD1", ""), ("HausA", "")])
        self.assertEqual(PS.analyze(self.ws)["addresses"], 0)

    def test_dcc_to_selectrix_and_back(self):
        self.fill([("11", "Rot"), ("17", "AnAus"), ("900", ""), ("SwitchD1", ""), ("16", "")])
        PS.convert(self.ws, "Selectrix")
        self.assertEqual(self.M25.Page_ID, "Selectrix")
        self.assertEqual((self.M25.SX_Channel_Col, self.M25.SX_Bitposi_Col, self.M25.Inp_Typ_Col), (4, 5, 6))
        sx = self.data()
        self.assertEqual(sx[0][3:6], ["1", "3", "Tast"])             # Rot -> Taster
        self.assertEqual(sx[1][3:6], ["2", "1", "AnAus"])            # An/Aus bleibt
        self.assertEqual(sx[2][3:6], ["900", "", ""])                # ausserhalb 1 bis 800: bleibt stehen
        self.assertEqual(sx[3][3:6], ["SwitchD1", "", ""])           # Variable bleibt
        self.assertEqual(sx[4][3:6], ["1", "8", "Tast"])             # ohne Typ -> Taster
        self.assertEqual(str(self.ws.tksheet.data[0][1]), "Selectrix")
        self.assertIn("Channel", str(self.ws.tksheet.data[1][3]))
        self.assertIn("Bitposition", str(self.ws.tksheet.data[1][4]))
        PS.convert(self.ws, "DCC")
        back = self.data()
        self.assertEqual([r[3] for r in back], ["11", "17", "900", "SwitchD1", "16"])
        self.assertEqual([r[4] for r in back], ["", "AnAus", "", "", ""])          # Taster -> leerer Typ
        self.assertEqual(self.M25.Page_ID, "DCC")
        self.assertIn("Adresse", str(self.ws.tksheet.data[1][3]))

    def test_selectrix_testbuttons(self):
        self.fill([("11", "Rot"), ("17", "AnAus")])
        PS.convert(self.ws, "Selectrix")
        names = dict(self.buttons())
        self.assertIn("S  10- 1- 2-3", names)                        # Taster: Adresse 1*8+3-1, gelb (2), Text = Bitposition
        self.assertIn("B  16- 1- 1-1", names)                        # An/Aus: Adresse 2*8+1-1, Text = Bitposition
        self.assertEqual(names["B  16- 1- 1-1"], "1")

    def test_first_channel_keeps_type_and_buttons(self):
        self.fill([("9", "AnAus")])
        PS.convert(self.ws, "Selectrix")
        self.assertEqual(self.data()[0][3:6], ["1", "1", "AnAus"])
        self.assertEqual(len(self.buttons()), 1)

    def header_config(self):
        """Code-Generator (M06) auf das aktive Blatt: Konfigurationszeilen und die Defines der Eingangskanaele"""
        import proggen.M06_Write_Header as M06
        from vb2py.vbfunctions import vbObjectInitialize
        self.ws.Activate()
        self.M25.Col_from_Sheet = ""
        self.M25.Make_sure_that_Col_Variables_match(self.ws)
        M06.Init_HeaderFile_Generation()
        original = self.P01.MsgBox
        self.P01.MsgBox = lambda *a, **k: 1
        try:
            ok = M06.ProcessSheet(self.ws.Name, True, 0, vbObjectInitialize((self.M02.LED_CHANNELS - 1,), int), vbObjectInitialize((self.M02.LED_CHANNELS - 1,), int))
        finally:
            self.P01.MsgBox = original
        self.assertTrue(ok)
        self.errors = M06.ErrorText
        lines = [l.split("/*")[0].strip().rstrip(")") for l in M06.ConfigTxt.splitlines() if "AndreaskrRGB" in l]
        return lines, M06.InChTxt

    def test_selectrix_generator_same_input_channels_as_dcc(self):
        """Nach dem Wechsel vergibt der Code-Generator dieselben Eingangskanaele wie beim DCC-Blatt (kein leeres #InCh)."""
        self.fill([("9", "AnAus"), ("10", "AnAus"), ("17", "AnAus")])
        dcc, _ = self.header_config()
        PS.convert(self.ws, "Selectrix")
        sx, defines = self.header_config()
        channel = lambda lines: [l.split(",")[1].strip() for l in lines]
        self.assertEqual(channel(sx), channel(dcc))                  # 0, 1, 2 wie bei DCC
        self.assertNotIn("", channel(sx))
        self.assertEqual(self.errors, "")

    def test_selectrix_same_address_in_several_rows(self):
        self.fill([("9", "AnAus")] * 3)
        PS.convert(self.ws, "Selectrix")
        sx, defines = self.header_config()
        self.assertEqual([l.split(",")[1].strip() for l in sx], ["0", "INCH_SX_1_1_ONOFF", "INCH_SX_1_1_ONOFF"])
        self.assertEqual(defines.count("#define INCH_SX_1_1_ONOFF"), 1)

    def test_generator_refuses_invalid_selectrix_entries(self):
        """Channel nicht 1 bis 99 oder Bitposition nicht 1 bis 8 (auch fehlend): Fehler, das Header file wird nicht erzeugt."""
        self.fill([("9", "AnAus")])
        PS.convert(self.ws, "Selectrix")
        row = self.ws.tksheet.data[3]
        for channel, bit, ok in (("1", "1", True), ("99", "8", True), ("0", "1", False), ("100", "1", False), ("1", "0", False), ("1", "9", False), ("1", "", False)):
            row[3], row[4] = channel, bit
            self.header_config()
            self.assertEqual(self.errors == "", ok, (channel, bit, self.errors))

    def type_address(self, text):
        """Text in die Adresszelle der ersten Datenzeile schreiben und das Aenderungsereignis ausloesen; Rueckgabe: (Zelle danach, Meldungen)"""
        self.fill([("", "")])
        messages = []
        original = self.P01.MsgBox
        self.P01.MsgBox = lambda text_, kind=0, title="": messages.append(text_) or 1
        try:
            col = self.M25.Get_Address_Col()
            self.ws.tksheet.data[3][col - 1] = text
            self.M20.Global_Worksheet_Change(self.P01.Cells(4, col))
        finally:
            self.P01.MsgBox = original
        return str(self.ws.tksheet.data[3][col - 1]), messages

    def test_address_zero_not_allowed_in_dcc(self):
        for text in ("0", "0 - 3", "-1"):
            cell, messages = self.type_address(text)
            self.assertEqual(cell, "", text)
            self.assertEqual(len(messages), 1, text)
        for text in ("1", "5 - 8", "SwitchD1", "RM 1"):
            cell, messages = self.type_address(text)
            self.assertEqual(messages, [], text)
            self.assertNotEqual(cell, "", text)

    def test_channel_zero_not_allowed_in_selectrix(self):
        PS.convert(self.ws, "Selectrix")
        cell, messages = self.type_address("0")
        self.assertEqual((cell, len(messages)), ("", 1))
        cell, messages = self.type_address("1")
        self.assertEqual((cell, messages), ("1", []))

    def test_generator_refuses_address_zero_in_dcc(self):
        self.fill([("0", "AnAus")])
        self.header_config()
        self.assertIn("0", self.errors)
        self.assertNotEqual(self.errors, "")

    def test_import_into_hidden_sheet_shows_it(self):
        """Die Startseite versteckt Blaetter anderer Zentralen: ein Import in so ein Blatt blendet es wieder ein (sonst landeten die Daten unsichtbar im versteckten Blatt)."""
        hidden = next(s for s in self.wb.sheets if s.Name == "Selectrix")
        hidden.user_hidden = True
        path = os.path.join(tempfile.mkdtemp(prefix="mll_pgf_"), "sx.MLL_pgf")
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write("Head:\tProgram_Generator configuration file\tV1.0\nSheet:\tSelectrix\tSelectrix\n"
                     "Line:\tAct" + "\t" * 9 + "RGB_Heartbeat(#LED)\t1\t1\t0\t0\t0\n"
                     "Line:\tAct\t\t22\t1\tTast" + "\t" * 5 + "Const(#LED, C_ALL, #InCh, 0, 127)\t3\t1\t1\t0\t0\n")
        try:
            self.assertTrue(self.M18.Read_PGF(path, False))
            self.assertFalse(getattr(hidden, "user_hidden", False))
            self.assertTrue(any("Const(" in str(c) for r in hidden.tksheet.data for c in r))
        finally:
            hidden.user_hidden = False
            self.ws.Activate()

    def test_widths_and_columns_shift(self):
        before = self.ws.tksheet.get_total_columns()
        PS.convert(self.ws, "Selectrix")
        self.assertEqual(self.ws.tksheet.get_total_columns(), before + 1)
        PS.convert(self.ws, "DCC")
        self.assertEqual(self.ws.tksheet.get_total_columns(), before)

    def test_row1_variables_follow_columns(self):
        before = [str(c) for c in self.ws.tksheet.data[0]]
        PS.convert(self.ws, "Selectrix")
        after = [str(c) for c in self.ws.tksheet.data[0]]
        self.assertEqual(after[5:], before[4:])                      # alles ab Spalte E ist um eine Spalte verschoben
        PS.convert(self.ws, "DCC")
        self.assertEqual([str(c) for c in self.ws.tksheet.data[0]], before)

    def test_dcc_to_can_changes_nothing(self):
        with self.assertRaises(ValueError):
            PS.convert(self.ws, "CAN")

    def test_pgf_export_selectrix_and_cross_import(self):
        self.fill([("11", "Rot"), ("17", "AnAus"), ("SwitchD1", "")])
        PS.convert(self.ws, "Selectrix")
        path = os.path.join(tempfile.mkdtemp(prefix="mll_pgf_"), "sx.MLL_pgf")
        self.assertTrue(getattr(self.M18, "__Save_SingleSheet_to_pgf")(path, self.ws, False))
        lines = open(path, encoding="utf-8").read().split("\n")
        self.assertTrue(lines[0].startswith("Head:\tProgram_Generator configuration file"))
        self.assertTrue(lines[1].startswith("Sheet:\tSelectrix\t"))
        rows = [l.split("\t") for l in lines if l.startswith("Line:") and "AndreaskrRGB" in l]
        self.assertEqual([r[3:6] for r in rows], [["1", "3", "Tast"], ["2", "1", "AnAus"], ["SwitchD1", "", ""]])
        # in das DCC-Blatt laden: Adressen werden zurueckgerechnet
        PS.convert(self.ws, "DCC")
        del self.ws.tksheet.data[3:]
        self.ws.Activate()
        self.assertTrue(self.M18.Read_PGF(path, True))
        got = [r[3] for r in self.data() if r[3]]
        self.assertEqual(got, ["11", "17", "SwitchD1"])

    def test_selectrix_pgf_from_excel_into_selectrix_sheet(self):
        """Selectrix-Block der Beispieldatei des Excel-Programms in ein Selectrix-Blatt laden und wieder speichern: die aktiven Zeilen bleiben gleich."""
        src = open(os.path.join(ROOT, "Prog_Generator_Examples", "Mainboard_Hardware_Test.MLL_pgf"), encoding="cp1252").read().split("\n")
        i = next(k for k, l in enumerate(src) if l.startswith("Sheet:\tSelectrix"))
        j = next((k for k in range(i + 1, len(src)) if src[k].startswith("Sheet:")), len(src))
        folder = tempfile.mkdtemp(prefix="mll_pgf_")
        path = os.path.join(folder, "excel_sx.MLL_pgf")
        open(path, "w", encoding="utf-8", newline="").write("\n".join([src[0]] + src[i:j]) + "\n")
        self.assertTrue(self.M18.Read_PGF(path, False))
        sheet = next(s for s in self.wb.sheets if s.Name == src[i].split("\t")[2])
        out = os.path.join(folder, "out.MLL_pgf")
        self.assertTrue(getattr(self.M18, "__Save_SingleSheet_to_pgf")(out, sheet, False))

        def active(p):
            return [l.rstrip("\t") for l in open(p, encoding="utf-8").read().split("\n") if l.startswith("Line:") and not l.startswith("Line:\t-")]
        self.assertEqual(active(path), active(out))

    def test_selectrix_typ_dialog_opens_after_channel_and_bit(self):
        """Channel und Bitposition eingegeben, Typ leer: der Dialog Taster/An-Aus oeffnet sich sofort (nicht erst beim erneuten Anklicken der Zelle Typ)."""
        PS.convert(self.ws, "Selectrix")
        self.ws.Activate()
        self.M25.Col_from_Sheet = ""
        self.M25.Make_sure_that_Col_Variables_match(self.ws)
        calls = []
        original = self.M20.Select_Typ_by_Dialog
        self.M20.Select_Typ_by_Dialog = lambda target: calls.append((target.Row, target.Column))
        try:
            ts = self.ws.tksheet
            r0 = 5
            while len(ts.data) <= r0:
                ts.data.append([""] * len(ts.data[0]))
            row = ts.data[r0]
            row[1], row[11 + 1], row[15] = chr(self.M02.Hook_CHAR), "AndreaskrRGB(#LED, #InCh)", "1"
            P01 = self.P01
            ts.data[r0][3] = "1"                                                       # Channel 1
            self.M20.Global_Worksheet_Change(P01.Cells(r0 + 1, self.M25.SX_Channel_Col))
            self.assertEqual(calls, [], "ohne Bitposition noch kein Dialog")
            ts.data[r0][4] = "3"                                                       # Bitposition
            self.M20.Global_Worksheet_Change(P01.Cells(r0 + 1, self.M25.SX_Bitposi_Col))
            self.assertEqual(calls, [(r0 + 1, self.M25.Inp_Typ_Col)])
            calls.clear()
            ts.data[r0][5] = "Tast"                                                    # Typ gesetzt: kein weiterer Dialog
            self.M20.Global_Worksheet_Change(P01.Cells(r0 + 1, self.M25.SX_Bitposi_Col))
            self.assertEqual(calls, [])
            # umgekehrte Reihenfolge: erst Bitposition, dann Channel
            ts.data[r0][5], ts.data[r0][3] = "", ""
            self.M20.Global_Worksheet_Change(P01.Cells(r0 + 1, self.M25.SX_Bitposi_Col))
            self.assertEqual(calls, [], "ohne Channel kein Dialog")
            ts.data[r0][3] = "7"
            self.M20.Global_Worksheet_Change(P01.Cells(r0 + 1, self.M25.SX_Channel_Col))
            self.assertEqual(calls, [(r0 + 1, self.M25.Inp_Typ_Col)])
        finally:
            self.M20.Select_Typ_by_Dialog = original

    def test_selectrix_input_ranges(self):
        PS.convert(self.ws, "Selectrix")
        self.ws.Activate()
        self.M25.Col_from_Sheet = ""
        self.M25.Make_sure_that_Col_Variables_match(self.ws)
        messages = []
        original = self.P01.MsgBox
        self.P01.MsgBox = lambda text, kind=0, title="": messages.append(text) or 1
        ts = self.ws.tksheet
        r0 = 5
        while len(ts.data) <= r0:
            ts.data.append([""] * len(ts.data[0]))
        try:
            def enter(col, value):
                ts.data[r0][col - 1] = value
                del messages[:]
                self.M20.Global_Worksheet_Change(self.P01.Cells(r0 + 1, col))
                return ts.data[r0][col - 1], list(messages)
            for value in ("0", "100", "-1", "1.5", "99.5", "150 - 160", "0 - 3"):
                got, msg = enter(self.M25.SX_Channel_Col, value)
                self.assertEqual((got, len(msg)), ("", 1), "Channel " + value)
            for value in ("1", "99", "SwitchD1", "1 - 2", "Haus A", "7"):
                got, msg = enter(self.M25.SX_Channel_Col, value)
                self.assertEqual((got, msg), (value, []), "Channel " + value)
            for value in ("0", "9", "1.5", "a", "-1", "10"):
                got, msg = enter(self.M25.SX_Bitposi_Col, value)
                self.assertEqual((got, len(msg)), ("", 1), "Bitposition " + value)
            for value in ("1", "8", "5"):
                got, msg = enter(self.M25.SX_Bitposi_Col, value)
                self.assertEqual((got, msg), (value, []), "Bitposition " + value)
        finally:
            self.P01.MsgBox = original

    def test_dcc_sheet_has_no_selectrix_check(self):
        ts = self.ws.tksheet
        while len(ts.data) <= 5:
            ts.data.append([""] * len(ts.data[0]))
        ts.data[5][3] = "5000"
        self.assertTrue(self.M20.SX_Check_Input(self.P01.Cells(6, self.M25.DCC_or_CAN_Add_Col)))
        self.assertEqual(ts.data[5][3], "5000")

    def test_warning_text(self):
        self.fill([("11", "Rot"), ("900", "")])
        text = PS.warning_text(PS.analyze(self.ws), "DCC", "Selectrix")
        self.assertIn("2 Zeilen", text)
        self.assertIn("Rot oder Grün", text)
        self.assertIn("außerhalb von 9 bis 800", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
