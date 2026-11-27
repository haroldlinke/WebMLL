# Datei-Version: 1.02 (2026-11-27) - test_macro_edit.py  # v1.02
# Name: test_macro_edit.py
# Path: test_macro_edit.py
# Version: 1.02  # v1.02
# Last Update: 2026-11-27
# Author: Harold Linke, Jürgen Winkler
# Licence: LGPL V2.1
# History of Change:
#   1.00  2026-11-19  Tests der Makro-Syntaxpruefung
#   1.01  2026-11-19  Tests fuer das Neufuellen von LEDs, InCnt und LocInCh nach dem Aendern des Makros
#   1.02  2026-11-27  Test fuer Makronamen mit Punkt (EX.IRReceiverNEC)
"""Tests for the syntax checks used by the configuration cell editor."""
import ast
import csv
import logging
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from headless import headless_macro_edit as macro_edit
from headless.headless_macro_edit import MacroSyntaxError, expected_argument_count, parse_call


class MacroEditTests(unittest.TestCase):
    def test_nested_expressions_and_strings(self):
        self.assertEqual(parse_call('Const(#LED, C1, f(1, 2), "a,b)", {1, 2})'),
                         ('Const', ['#LED', 'C1', 'f(1, 2)', '"a,b)"', '{1, 2}']))
        self.assertEqual(parse_call('RGB_Heartbeat()'), ('RGB_Heartbeat', []))

    def test_extension_macro_names_with_dot(self):  # v1.02
        self.assertEqual(parse_call('EX.IRReceiverNEC(2, 0)'), ('EX.IRReceiverNEC', ['2', '0']))
        self.assertEqual(parse_call('EX.P_ScheduleExtension(Test1, Test1, SI_1, 13)')[0], 'EX.P_ScheduleExtension')
        for text in ('EX.(1)', '.EX(1)', 'EX..A(1)', 'EX.1A(1)'):
            with self.subTest(text=text), self.assertRaises(MacroSyntaxError):
                parse_call(text)

    def test_invalid_calls(self):
        for text in ('Const', 'Const(', 'Const(1,)', 'Const(,1)', 'Const(1,,2)',
                     'Const([1),2)', 'Const("abc)', 'Const(1) trailing'):
            with self.subTest(text=text), self.assertRaises(MacroSyntaxError):
                parse_call(text)

    def test_non_call_configurations(self):
        for text in ('', '#define READ_LDR', '// Activation: Binary\nPattern(...)'):
            with self.subTest(text=text):
                self.assertIsNone(parse_call(text))

    def test_parameter_counts(self):
        types = {'Val0': '', 'Val1': '', 'Color': 'RGB', 'Colors': 'RGB2'}
        self.assertEqual(expected_argument_count('Const(LED, Cx, InCh, Val0, Val1)', types), 5)
        self.assertEqual(expected_argument_count('Example(#LED, Color, Colors)', types), 10)
        self.assertIsNone(expected_argument_count('House(LED, InCh, ...)', types))
        self.assertIsNone(expected_argument_count('Example(unknown)', types))
        self.assertIsNone(expected_argument_count('#define READ_LDR', types))

    def test_real_library_templates(self):
        root = Path(__file__).parent
        with (root / 'csv' / 'Lib_Macros.csv').open(encoding='utf-8-sig', newline='') as f:
            rows = list(csv.reader(f, delimiter=';'))
        with (root / 'csv' / 'Par_Description.csv').open(encoding='utf-8-sig', newline='') as f:
            types = {row[0].strip(): row[2].strip() for row in csv.reader(f, delimiter=';') if len(row) > 2}
        templates = {row[15]: row[14] for row in rows if len(row) > 16 and row[15]}
        self.assertEqual(expected_argument_count(templates['Const('], types), 5)
        self.assertEqual(expected_argument_count(templates['RGB_Heartbeat('], types), 1)
        self.assertIsNone(expected_argument_count(templates['Logic('], types))

    def test_translations(self):
        from _web.web_i18n import load_catalog, tr, use_language
        keys = ['Ungültiger Makrotext', 'Makrotext', 'Ursprünglichen Makrotext wiederherstellen',
                'Änderung prüfen', 'Ein Makroparameter ist leer.',
                'Ein Makroaufruf muss mit einem Namen und einer öffnenden Klammer beginnen.',
                'Die Klammern im Makrotext stimmen nicht überein.',
                'Nach dem Makroaufruf steht zusätzlicher Text.',
                'Der Makroaufruf hat eine nicht geschlossene Klammer oder Zeichenkette.',
                'Das Makro erwartet {expected} Parameter, angegeben wurden {actual}.',
                # 'Fehler beim Prüfen des Makrotexts: {ex}']  # v1.02 (entfallen)
                'Fehler beim Prüfen des Makrotexts: {ex}',
                "Der Parameter '{parameter}' muss eine ganze Zahl sein.",
                "Der Parameter '{parameter}' hat den Wert {value}, zulässig ist der Bereich {range}.",
                "Der Parameter '{parameter}' muss eine Zeitangabe sein, zum Beispiel 3 Sec (Einheiten: Min, Sec, ms).",
                "Der Parameter '{parameter}' muss einen gültigen Variablennamen enthalten.",
                "Die Farbwerte des Parameters '{parameter}' müssen ganze Zahlen von 0 bis 255 sein."]  # v1.02
        catalog = load_catalog(force=True)
        for key in keys:
            self.assertTrue(all(catalog[key][:7]), key)
            for language in range(7):
                with use_language(language):
                    # result = tr(key, expected=5, actual=3, ex='test')  # v1.02 (entfallen)
                    result = tr(key, expected=5, actual=3, ex='test', parameter='P', value='9', range='0 – 5')  # v1.02
                # self.assertEqual(result, catalog[key][language].format(expected=5, actual=3, ex='test'))  # v1.02 (entfallen)
                self.assertEqual(result, catalog[key][language].format(expected=5, actual=3, ex='test', parameter='P', value='9', range='0 – 5'))  # v1.02

    def test_library_count_validation(self):
        root = Path(__file__).parent
        source = (root / 'webmobaledlib.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        function = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'validate_macro_text')
        module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
        with (root / 'csv' / 'Lib_Macros.csv').open(encoding='utf-8-sig', newline='') as f:
            rows = list(csv.reader(f, delimiter=';'))
        with (root / 'csv' / 'Par_Description.csv').open(encoding='utf-8-sig', newline='') as f:
            parameters = list(csv.reader(f, delimiter=';'))
        # Konstruktor einer Extension (wie M38_Extensions.Load_Extensions ihn in Lib_Macros und Par_Description einträgt)  # v1.02
        extension_row = [''] * 17
        extension_row[0], extension_row[14], extension_row[15] = 'EX.Constructor', 'EX.IRReceiverNEC(EX.InfraredMLX.Pin, EX.InfraredMLX.Wait, EX.InfraredMLX.Name)', 'EX.IRReceiverNEC('
        rows.append(extension_row)
        parameters += [['EX.InfraredMLX.Pin', '', '', '0', '40', '2', '', 'Pin'],
                       ['EX.InfraredMLX.Wait', '', 'Time', '0', '1000', '0', '', 'Wartezeit'],
                       ['EX.InfraredMLX.Name', '', 'Var', '', '', '', '', 'Name']]
        by_name = {r[15]: i for i, r in enumerate(rows) if len(r) > 16 and r[15]}
        lib = SimpleNamespace(Cells=lambda row, col: rows[row][col - 1])
        param_sheet = SimpleNamespace(tksheet=SimpleNamespace(data=parameters))
        env = {'macro_edit': macro_edit, 'M09SM': SimpleNamespace(Find_Macro_in_Lib_Macros_Sheet=lambda s: by_name.get(s, 0)),
               'M02': SimpleNamespace(LIBMACROS_SH='lib', PAR_DESCR_SH='params', SM_Typ___COL=1,
                                      # SM_Mode__COL=2, SM_Macro_COL=15),  # v1.02 (entfallen)
                                      SM_Mode__COL=2, SM_Macro_COL=15, PAT_LEDVariableName=r'^[A-Za-z][A-Za-z0-9_]*$'),  # v1.02
               'wb': SimpleNamespace(Sheets=lambda name: lib if name == 'lib' else param_sheet),
               'tr': lambda text, **kw: text.format(**kw)}
        exec(compile(module, 'webmobaledlib.py', 'exec'), env)
        validate = env['validate_macro_text']
        ws = SimpleNamespace(Activate=Mock())
        validate(ws, 'Const(#LED, C1, #InCh, 0, 255)')
        with self.assertRaises(MacroSyntaxError):
            validate(ws, 'Const(#LED)')
        validate(ws, 'House(#LED, #InCh, 1, 2, ROOM_DARK)')
        validate(ws, 'CustomMacro(1)')
        validate(ws, 'EX.IRReceiverNEC(2, 0, Taste)')  # v1.02
        validate(ws, 'EX.IRReceiverNEC(2, 0.5 Sec, _Taste)')  # v1.02
        for text in ('EX.IRReceiverNEC(2, 0)', 'EX.IRReceiverNEC(41, 0, Taste)', 'EX.IRReceiverNEC(a, 0, Taste)',
                     'EX.IRReceiverNEC(2, 2 Sec, Taste)', 'EX.IRReceiverNEC(2, 5 Tage, Taste)', 'EX.IRReceiverNEC(2, 0, 1Taste)'):  # v1.02
            with self.subTest(text=text), self.assertRaises(MacroSyntaxError):
                validate(ws, text)


class RowFieldTests(unittest.TestCase):  # v1.01
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).parent
        with (root / 'csv' / 'Lib_Macros.csv').open(encoding='utf-8-sig', newline='') as f:
            rows = list(csv.reader(f, delimiter=';'))
        with (root / 'csv' / 'Par_Description.csv').open(encoding='utf-8-sig', newline='') as f:
            cls.types = {row[0].strip(): row[2].strip() for row in csv.reader(f, delimiter=';') if len(row) > 2}
        cls.by_name = {r[15]: r for r in rows if len(r) > 16 and r[15]}

    def fields(self, text):
        r = self.by_name[text.split('(')[0] + '(']
        lib = {'typ': r[0], 'leds': r[2], 'incnt': r[3], 'locinch': r[5], 'sngled': r[7], 'template': r[14]}
        return macro_edit.macro_row_fields(lib, text, self.types, lambda statement, mode: 3)

    def test_led_count_follows_macro(self):
        self.assertEqual(self.fields('ConstrWarnLightRGB6(#LED, #InCh, 5, 255, 100 ms, 0 ms, 500 ms)'),
                         {'leds': '6', 'incnt': 1, 'locinch': 0})
        self.assertEqual(self.fields('ConstRGB(#LED, #InCh, 0, 0, 0, 127, 127, 127)'),
                         {'leds': '1', 'incnt': 1, 'locinch': 0})

    def test_channel_selection(self):
        self.assertEqual(self.fields('Const(#LED, C2, #InCh, 0, 255)')['leds'], 'C2-2')
        self.assertEqual(self.fields('Const(#LED, C12, #InCh, 0, 255)')['leds'], 'C1-2')
        self.assertEqual(self.fields('Const(#LED, C_ALL, #InCh, 0, 255)')['leds'], '1')

    def test_input_count_modes(self):
        self.assertEqual(self.fields('InCh_to_TmpVar(#InCh, 4)')['incnt'], 4)
        self.assertEqual(self.fields('Charlie_Buttons(#LED, #InCh, 6)')['incnt'], 6)
        self.assertEqual(self.fields('Charlie_Binary(#LED, #InCh, 5)')['incnt'], 3)
        self.assertEqual(self.fields('Logic(Var, #InCh OR #InCh+2)')['incnt'], 3)
        self.assertEqual(self.fields('RS_FlipFlop(Var, #InCh, #InCh+1)')['incnt'], 3)

    def test_own_dialog_macros_are_not_filled(self):
        self.assertIsNone(macro_edit.macro_row_fields({'typ': 'House', 'leds': 'C_ALL'}, 'House(#LED, #InCh)', {}, None))
        self.assertIsNone(macro_edit.macro_row_fields({'typ': '', 'leds': '1'}, '#define X', {}, None))

    def test_apply_macro_fields(self):
        source = (Path(__file__).parent / 'webmobaledlib.py').read_text(encoding='utf-8')
        function = next(n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.FunctionDef) and n.name == 'apply_macro_fields')
        module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
        data = {(5, 4): '^ C1-2'}

        class Cell:
            def __init__(cell, row, col):
                cell.key = (row, col)
            @property
            def Value(cell):
                return data.get(cell.key, '')
            @Value.setter
            def Value(cell, value):
                data[cell.key] = value
        calls = []
        m20 = SimpleNamespace(Check_IsSingleChannelCmd=lambda leds: 'C' in leds,
                              Complete_Addr_Column_with_InCnt=lambda row: calls.append(('addr', row)),
                              Update_TestButtons=lambda row: calls.append(('buttons', row)),
                              Update_Start_LedNr=lambda: calls.append(('start',)))
        env = {'X02': SimpleNamespace(CRange=lambda row, col, ws: Cell(row, col), Application=SimpleNamespace(EnableEvents=True)),
               'M25': SimpleNamespace(LEDs____Col=4, InCnt___Col=5, LocInCh_Col=6), 'M20': m20}
        exec(compile(module, 'webmobaledlib.py', 'exec'), env)
        env['apply_macro_fields'](None, 5, {'leds': 'C1-1', 'incnt': 2, 'locinch': 0})
        self.assertEqual((data[(5, 4)], data[(5, 5)], data[(5, 6)]), ('^ C1-1', 2, 0))
        self.assertEqual(calls, [('addr', 5), ('buttons', 5), ('start',)])
        env['apply_macro_fields'](None, 5, {'leds': '1', 'incnt': None, 'locinch': 0})
        self.assertEqual((data[(5, 4)], data[(5, 5)]), ('1', 2))
        self.assertTrue(env['X02'].Application.EnableEvents)


class GridEditTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        source = (Path(__file__).parent / 'webmobaledlib.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        function = next(n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef) and n.name == 'on_cell_changed')
        module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
        self.data = [[''] * 12 for _ in range(3)]
        self.data[2][11] = 'Const(1)'
        self.data[2][10] = 'Eigener Name'
        self.ws = SimpleNamespace(Name='DCC', tksheet=SimpleNamespace(data=self.data), Activate=Mock())
        self.icons = []
        self.records = []
        self.restored = []
        self.corrected = None
        self.field_result = (0, None)  # v1.01
        self.applied = []  # v1.01

        class Cell:
            def __init__(cell, row, col):
                cell.row, cell.col = row, col
            @property
            def Value(cell):
                return self.data[cell.row - 1][cell.col - 1]
            @Value.setter
            def Value(cell, value):
                self.data[cell.row - 1][cell.col - 1] = value

        def find(text):
            return 1 if text.startswith('Const(') else (2 if text.startswith('Fire(') else 0)
        def add_icon(lib, row, ws):
            self.icons.append(('add', lib))
            self.data[row - 1][10] = 'Feuer' if lib == 2 else 'Konstant'
        async def worker(fn):
            return fn()
        async def correct(ws, text, error):
            self.restored.append(('dialog', text))
            return self.corrected
        def undo_record(ws, before, label, rows, **kwargs):
            self.records.append((before, kwargs))
        self.env = {
            'state': {'ws': self.ws, 'busy': False}, 'ui': SimpleNamespace(notify=Mock()),
            'show': Mock(), 'first_data_row0': lambda: 2, 'readonly_columns': lambda ws: set(),
            'event_col_id': lambda a: 'c11', 'M09': SimpleNamespace(CANONICAL_TOKENS=False),
            'typ_column': lambda ws: 4, 'undo_cell': lambda ws, r, c: self.data[r][c],
            'undo_row_count': lambda ws: len(self.data), 'M28': SimpleNamespace(Is_Data_Sheet=lambda ws: True),
            'M25': SimpleNamespace(Config__Col=12, LanName_Col=11, Make_sure_that_Col_Variables_match=Mock(), LEDs____Col=4,
                                   InCnt___Col=5, LocInCh_Col=6, DCC_or_CAN_Add_Col=7, SX_Channel_Col=0, SX_Bitposi_Col=0, Inp_Typ_Col=3),  # v1.01
            'macro_field_values': lambda ws, text: self.field_result, 'apply_macro_fields': lambda ws, row, fields: self.applied.append((row, fields)),  # v1.01
            'macro_edit': macro_edit, 'run_in_worker': worker, 'validate_macro_text': lambda ws, text: parse_call(text),
            'correct_macro_text': correct, 'restore_grid_row': lambda ws, row: self.restored.append(('restore', row)),
            'X02': SimpleNamespace(CRange=lambda row, col, ws: Cell(row, col)),
            'M09SM': SimpleNamespace(Find_Macro_in_Lib_Macros_Sheet=find, Add_Icon_and_Name=add_icon),
            'M27': SimpleNamespace(Del_one_Icon_in_IconCol=lambda row, ws: self.icons.append(('delete', row)),
                                   FindMacro_and_Add_Icon_and_Name=Mock()),
            'SHAPES_DEBUG': False, 'auto_color_rows': Mock(), 'logger': logging.getLogger(__name__),
            'tr': lambda text, **kw: text.format(**kw), 'undo_record': undo_record,
        }
        exec(compile(module, 'webmobaledlib.py', 'exec'), self.env)

    async def change(self, value):
        await self.env['on_cell_changed'](SimpleNamespace(args={'data': {'_r': 2}, 'newValue': value}))

    async def test_invalid_can_restore(self):
        await self.change('Fire(')
        self.assertEqual(self.data[2][11], 'Const(1)')
        self.assertEqual(self.restored, [('restore', 3), ('dialog', 'Fire(')])
        self.assertEqual(self.records, [])

    async def test_invalid_can_be_corrected_and_changes_metadata(self):
        self.corrected = 'Fire(1)'
        await self.change('Fire(')
        self.assertEqual(self.data[2][11], 'Fire(1)')
        self.assertEqual(self.data[2][10], 'Feuer')
        self.assertEqual(self.icons, [('delete', 3), ('add', 2)])
        # Zusaetzlich werden die mit dem Makro neu gefuellten Felder fuer das Rueckgaengig gemerkt  # v1.01
        self.assertEqual(self.records[0][0][:2], [((2, 11), 'Const(1)'), ((2, 10), 'Eigener Name')])
        self.assertEqual({pos for pos, _ in self.records[0][0][2:]}, {(2, 3), (2, 4), (2, 5), (2, 2), (2, 6)})  # v1.01
        self.assertTrue(self.records[0][1]['include_unchanged'])

    async def test_parameter_change_keeps_name_and_icon(self):
        await self.change('Const(2)')
        self.assertEqual(self.data[2][10], 'Eigener Name')
        self.assertEqual(self.icons, [])
        self.assertTrue(self.records[0][1]['include_unchanged'])

    async def test_fields_are_refilled_after_macro_change(self):  # v1.01
        fields = {'leds': '1', 'incnt': 1, 'locinch': 0}
        self.field_result = (1, fields)
        await self.change('Const(2)')
        self.assertEqual(self.applied, [(3, fields)])

    async def test_no_refill_for_unknown_macro(self):  # v1.01
        await self.change('Custom(2)')
        self.assertEqual(self.applied, [])


if __name__ == '__main__':
    unittest.main()
