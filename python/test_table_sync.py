# Datei-Version: 1.06 (2026-11-23) - test_table_sync.py
# Name: test_table_sync.py
# Path: test_table_sync.py
# Version: 1.06
# Last Update: 2026-11-23
# Author: Harold Linke
# Licence: LGPL V2.1
# History of Change:
#   1.06 2026-11-23 Falschen Code ueber echten HTTP-Server mit verstaendlicher Meldung pruefen.
#   1.05 2026-11-23 Aktualisierungsfunktion der aktuellen Programmseite an Dialog uebergeben.
#   1.04 2026-11-23 Kanalauswahl beim Zeilenimport pruefen.
#   1.03 2026-11-23 Feature-Branch auf Basis 4.79; Sprachen und Startvorgaben dokumentiert.
#   1.02 2026-11-23 Zeilenauswahl, Einfuegeposition, Metadaten, Konflikte, Backup und Protokollschutz.
#   1.01 2026-11-23 Originalberechnung nach Import und Wiederherstellung pruefen.
#   1.00 2026-11-22 Paketgrenzen, Backup, Wiederherstellung, Fehlerrollback und echte LAN-Protokolle.
import copy  # v1.03
import json  # v1.03
from pathlib import Path  # v1.03
import tempfile  # v1.03
import unittest  # v1.03
from unittest.mock import patch  # v1.03
from urllib.error import HTTPError  # v1.03

from headless import headless_table_sync as s  # v1.03


def workbook(value="alt"):  # v1.03
    return {"Version": "test", "DataVersion": "102", "Workbookdata": {
        "DCC": {"TKSHEET_data": [["DE", "COM-local", "local-ip"], [value, 2, 3]], "col_pos": [0, 100, 200]},
        "CAN": {"TKSHEET_data": [["DE"], ["behalten"]]},
        "Config": {"TKSHEET_data": [["geheim"]]}}, "SheetOrder": ["DCC", "CAN"],
        "Esp32Wlan": {"DCC": {"host": "target-host"}}, "Esp32Options": {"DCC": {"ldr": True}}}  # v1.03


class TablesTests(unittest.TestCase):  # v1.03
    def test_only_selected_tables_no_settings(self):  # v1.03
        data = s.validate(s.make_package(workbook(), ["DCC"], local_columns=[1, 2]))  # v1.03
        self.assertEqual(list(data["sheets"]), ["DCC"])  # v1.03
        self.assertNotIn("Esp32Wlan", data)  # v1.03
        self.assertNotIn("Esp32Options", data)  # v1.03
        self.assertEqual(data["sheets"]["DCC"]["data"]["TKSHEET_data"][0][1:], ["", ""])  # v1.03

    def test_preserves_other_tables_and_target_settings(self):  # v1.03
        before = workbook()  # v1.03
        package = s.make_package(workbook("neu"), ["DCC"], local_columns=[1, 2])  # v1.03
        result = s.merge(before, package, local_columns=[1, 2])  # v1.03
        self.assertEqual(result["Workbookdata"]["DCC"]["TKSHEET_data"][1][0], "neu")  # v1.03
        self.assertEqual(result["Workbookdata"]["DCC"]["TKSHEET_data"][0][1], "COM-local")  # v1.03
        self.assertEqual(result["Workbookdata"]["CAN"], before["Workbookdata"]["CAN"])  # v1.03
        self.assertEqual(result["Esp32Wlan"], before["Esp32Wlan"])  # v1.03
        self.assertEqual(result["Esp32Options"], before["Esp32Options"])  # v1.03
        self.assertEqual(before, workbook())  # v1.03

    def test_exactly_one_backup_is_replaced(self):  # v1.03
        with tempfile.TemporaryDirectory() as tmp:  # v1.03
            path = Path(tmp) / "mappe.json"  # v1.03
            path.write_bytes(s.encode(workbook("eins")))  # v1.03
            for value in ["zwei", "drei"]:  # v1.03
                s.import_tables(tmp, path, s.make_package(workbook(value), ["DCC"]))  # v1.03
            backup = json.loads((Path(tmp) / s.BACKUP).read_bytes())  # v1.03
            self.assertEqual(backup["Workbookdata"]["DCC"]["TKSHEET_data"][1][0], "zwei")  # v1.03
            self.assertEqual(len(list(Path(tmp).glob("*backup*"))), 1)  # v1.03
            s.restore(tmp, path)  # v1.03
            self.assertEqual(json.loads(path.read_bytes()), backup)  # v1.03

    def test_failed_import_preserves_both_files(self):  # v1.03
        with tempfile.TemporaryDirectory() as tmp:  # v1.03
            path = Path(tmp) / "mappe.json"  # v1.03
            before = s.encode(workbook())  # v1.03
            path.write_bytes(before)  # v1.03
            backup = Path(tmp) / s.BACKUP  # v1.03
            backup.write_bytes(b"older-backup")  # v1.03
            write = s.atomic_write  # v1.03
            def fail_target(name, data):  # v1.03
                if Path(name) == path:  # v1.03
                    raise OSError("disk full")  # v1.03
                write(name, data)  # v1.03
            with patch.object(s, "atomic_write", side_effect=fail_target):  # v1.03
                with self.assertRaises(OSError):  # v1.03
                    s.import_tables(tmp, path, s.make_package(workbook("neu"), ["DCC"]))  # v1.03
            self.assertEqual(path.read_bytes(), before)  # v1.03
            self.assertEqual(backup.read_bytes(), b"older-backup")  # v1.03

    def test_bad_versions_and_config_sheet_rejected(self):  # v1.03
        source = workbook()  # v1.03
        source["DataVersion"] = "999"  # v1.03
        with self.assertRaises(ValueError):  # v1.03
            s.merge(workbook(), s.make_package(source, ["DCC"]))  # v1.03
        with self.assertRaises(ValueError):  # v1.03
            s.make_package(workbook(), ["Config"])  # v1.03

    def test_malformed_package_does_not_create_backup(self):  # v1.03
        with tempfile.TemporaryDirectory() as tmp:  # v1.03
            path = Path(tmp) / "mappe.json"  # v1.03
            path.write_bytes(s.encode(workbook()))  # v1.03
            with self.assertRaises(ValueError):  # v1.03
                s.import_tables(tmp, path, b"not-json")  # v1.03
            self.assertFalse((Path(tmp) / s.BACKUP).exists())  # v1.03


class RowInsertTests(unittest.TestCase):  # v1.03
    def data(self, value="alt", address="10"):  # v1.03
        d = workbook(value)  # v1.03
        sheet = d["Workbookdata"]["DCC"]  # v1.03
        sheet["TKSHEET_data"] = [["", "DCC", "", "", "COM-local"], ["", "Aktiv", "", "Adresse", "Typ"], ["", "*", "", address, value]]  # v1.03
        return d  # v1.03

    def test_selected_channel_changes_only_inserted_rows(self):  # v1.04
        current, source = self.data(), self.data("neu", "20")  # v1.04
        for data in (current, source):  # v1.04
            data["Workbookdata"]["DCC"]["TKSHEET_data"][1].extend(["", "LED Kanal"])  # v1.04
            data["Workbookdata"]["DCC"]["TKSHEET_data"][2].extend(["", 7])  # v1.04
        before = copy.deepcopy(current)  # v1.04
        source_before = copy.deepcopy(source)  # v1.04
        raw = s.make_package(source, ["DCC"])  # v1.04
        for channel in (0, 1, 9):  # v1.04
            result, _, _ = s.plan_row_insert(current, raw, "DCC", "3", "DCC", led_channel=channel, channel_column=6)  # v1.04
            self.assertEqual(result["Workbookdata"]["DCC"]["TKSHEET_data"][3][6], channel)  # v1.04
            self.assertEqual(result["Workbookdata"]["DCC"]["TKSHEET_data"][:3], before["Workbookdata"]["DCC"]["TKSHEET_data"])  # v1.04
        kept, _, _ = s.plan_row_insert(current, raw, "DCC", "3", "DCC")  # v1.04
        self.assertEqual(kept["Workbookdata"]["DCC"]["TKSHEET_data"][3][6], 7)  # v1.04
        self.assertEqual(current, before)  # v1.04
        self.assertEqual(source, source_before)  # v1.04
        for channel in (-1, 10, 1.5, "x"):  # v1.04
            with self.assertRaises(ValueError):  # v1.04
                s.plan_row_insert(current, raw, "DCC", "3", "DCC", led_channel=channel, channel_column=6)  # v1.04
        with self.assertRaises(ValueError):  # v1.04
            s.plan_row_insert(current, raw, "DCC", "3", "DCC", led_channel=1, channel_column=99)  # v1.04

    def test_range_selection(self):  # v1.03
        self.assertEqual(s.row_selection("3-5, 7, 4", 8), [2, 3, 4, 6])  # v1.03
        for value in ["1", "2-4", "4-3", "3-9", "x", ""]:  # v1.03
            with self.assertRaises(ValueError): s.row_selection(value, 8)  # v1.03

    def test_before_keeps_existing_rows_and_settings(self):  # v1.03
        before = self.data()  # v1.03
        source = self.data("neu", "20")  # v1.03
        result, warnings, summary = s.plan_row_insert(before, s.make_package(source,["DCC"]), "DCC", "3", "DCC", "before", 3)  # v1.03
        rows = result["Workbookdata"]["DCC"]["TKSHEET_data"]  # v1.03
        self.assertEqual([r[4] for r in rows[2:]], ["neu", "alt"])  # v1.03
        self.assertEqual(rows[:2], before["Workbookdata"]["DCC"]["TKSHEET_data"][:2])  # v1.03
        self.assertEqual(result["Esp32Wlan"], before["Esp32Wlan"])  # v1.03
        self.assertEqual(result["Workbookdata"]["CAN"], before["Workbookdata"]["CAN"])  # v1.03
        self.assertEqual(warnings, [])  # v1.03
        self.assertEqual(summary["at"],3)  # v1.03
        self.assertEqual(before, self.data())  # v1.03

    def test_after_and_end(self):  # v1.03
        for where in ["after", "end"]:  # v1.03
            result, _, _ = s.plan_row_insert(self.data(), s.make_package(self.data("neu","20"),["DCC"]), "DCC","3","DCC",where,3)  # v1.03
            self.assertEqual([r[4] for r in result["Workbookdata"]["DCC"]["TKSHEET_data"][2:]], ["alt","neu"])  # v1.03

    def test_metadata_is_shifted_and_copied(self):  # v1.03
        target = self.data()  # v1.03
        target["Workbookdata"]["DCC"].update(TKSHEET_highlighted_cells={"2,4":"red"}, row_heights={"2":30}, hidden_rows=[2], shapelist=[{"Row":3,"TopLeftCell_Row":3,"Top_val":40}])  # v1.03
        source = self.data("neu","20")  # v1.03
        source["Workbookdata"]["DCC"].update(TKSHEET_highlighted_cells={"2,4":"green"},row_heights={"2":25},TKSHEET_manual_cells=["2,4"])  # v1.03
        result,_,_=s.plan_row_insert(target,s.make_package(source,["DCC"]),"DCC","3","DCC","before",3)  # v1.03
        sheet=result["Workbookdata"]["DCC"]  # v1.03
        self.assertEqual(sheet["TKSHEET_highlighted_cells"],{"3,4":"red","2,4":"green"})  # v1.03
        self.assertEqual(sheet["row_heights"],{"3":30,"2":25})  # v1.03
        self.assertEqual(sheet["hidden_rows"],[3])  # v1.03
        self.assertEqual(sheet["TKSHEET_manual_cells"],["2,4"])  # v1.03
        self.assertEqual(sheet["shapelist"][0]["Row"],4)  # v1.03

    def test_address_range_and_names_warn(self):  # v1.03
        target=self.data(address="10-12")  # v1.03
        target["Workbookdata"]["DCC"]["TKSHEET_data"][2].append("#define SIGNAL(x) foo")  # v1.03
        source=self.data("neu","12-14")  # v1.03
        source["Workbookdata"]["DCC"]["TKSHEET_data"][2].append("#define SIGNAL(x) bar")  # v1.03
        _,warnings,_=s.plan_row_insert(target,s.make_package(source,["DCC"]),"DCC","3","DCC")  # v1.03
        self.assertEqual({w["kind"] for w in warnings},{"address","name"})  # v1.03

    def test_backup_and_undo_insertion(self):  # v1.03
        with tempfile.TemporaryDirectory() as tmp:  # v1.03
            path=Path(tmp)/"mappe.json"  # v1.03
            before=s.encode(self.data())  # v1.03
            path.write_bytes(before)  # v1.03
            raw=s.make_package(self.data("neu","10"),["DCC"])  # v1.03
            options=dict(source_name="DCC",rows="3",target_name="DCC",where="end")  # v1.03
            with self.assertRaises(ValueError):s.import_rows(tmp,path,raw,**options)  # v1.03
            self.assertEqual(path.read_bytes(),before)  # v1.03
            self.assertFalse((Path(tmp)/s.BACKUP).exists())  # v1.03
            s.import_rows(tmp,path,raw,allow_conflicts=True,**options)  # v1.03
            self.assertEqual(len(json.loads(path.read_bytes())["Workbookdata"]["DCC"]["TKSHEET_data"]),4)  # v1.03
            s.restore(tmp,path)  # v1.03
            self.assertEqual(path.read_bytes(),before)  # v1.03

    def test_missing_include_reference_warns(self):  # v1.03
        source=self.data("neu","20")  # v1.03
        source["Workbookdata"]["DCC"]["TKSHEET_data"][2].append('include(Missing_Sheet, 0)')  # v1.03
        _,warnings,_=s.plan_row_insert(self.data(),s.make_package(source,["DCC"]),"DCC","3","DCC")  # v1.03
        self.assertTrue(any(w["kind"]=="reference" and w["value"]=="Missing_Sheet" for w in warnings))  # v1.03

    def test_wrong_protocol_rejected(self):  # v1.03
        source=self.data()  # v1.03
        source["Workbookdata"]["DCC"]["TKSHEET_data"][0][1]="Selectrix"  # v1.03
        with self.assertRaises(ValueError):s.plan_row_insert(self.data(),s.make_package(source,["DCC"]),"DCC","3","DCC")  # v1.03


class RecalculationTests(unittest.TestCase):  # v1.03
    def test_recalculates_tables_and_restores_active_sheet(self):  # v1.03
        from types import SimpleNamespace  # v1.03
        from unittest.mock import MagicMock  # v1.03
        from _web.web_table_sync import recalculate_workbook  # v1.03
        a = MagicMock(Name="DCC", Datasheet=True)  # v1.03
        b = MagicMock(Name="DCC_1", Datasheet=True)  # v1.03
        config = MagicMock(Name="Config", Datasheet=False)  # v1.03
        wb = SimpleNamespace(sheets=[a, b, config], ActiveSheet=a)  # v1.03
        logic, columns = MagicMock(), MagicMock()  # v1.03
        recalculate_workbook(wb, logic=logic, columns=columns)  # v1.03
        logic.Update_All_Start_LedNr.assert_called_once()  # v1.03
        a.refreshicons.assert_called_once()  # v1.03
        b.refreshicons.assert_called_once()  # v1.03
        config.refreshicons.assert_not_called()  # v1.03
        self.assertEqual(logic.ResetTestButtons.call_count, 2)  # v1.03
        self.assertEqual(a.Select.call_count, 2)  # v1.03

    def test_active_sheet_restored_when_recalculation_fails(self):  # v1.03
        from types import SimpleNamespace  # v1.03
        from unittest.mock import MagicMock  # v1.03
        from _web.web_table_sync import recalculate_workbook  # v1.03
        active = MagicMock(Name="DCC", Datasheet=True)  # v1.03
        logic = MagicMock()  # v1.03
        logic.Update_All_Start_LedNr.side_effect = ValueError("invalid macro")  # v1.03
        with self.assertRaises(ValueError):  # v1.03
            recalculate_workbook(SimpleNamespace(sheets=[active], ActiveSheet=active), logic=logic, columns=MagicMock())  # v1.03
        active.Select.assert_called_once()  # v1.03


class NetworkTests(unittest.TestCase):  # v1.03
    def setUp(self):  # v1.03
        self.share = s.Share("Testquelle", "test-code-long-enough", s.make_package(workbook("netz"), ["DCC"]),
                             host="127.0.0.1", port=0, discovery_port=0)  # v1.03
        self.address = "http://127.0.0.1:" + str(self.share.port)  # v1.03

    def tearDown(self):  # v1.03
        self.share.close()  # v1.03

    def test_real_http_roundtrip(self):  # v1.03
        package = s.validate(s.fetch(self.address, "test-code-long-enough"))  # v1.03
        self.assertEqual(package["sheets"]["DCC"]["data"]["TKSHEET_data"][1][0], "netz")  # v1.03

    def test_wrong_code_denied(self):  # v1.03
        # with self.assertRaises(HTTPError) as error:  # v1.06 (entfallen)
        with self.assertRaisesRegex(ValueError, "Verbindungscode nicht akzeptiert") as error:  # v1.06
            s.fetch(self.address, "wrong-code")  # v1.06
        self.assertNotIn("wrong-code", str(error.exception))  # v1.06
        self.assertNotIn("403", str(error.exception))  # v1.06

    def test_real_udp_discovery(self):  # v1.03
        found = s.discover(address="127.0.0.1", port=self.share.discovery_port, timeout=0.3)  # v1.03
        self.assertEqual(found, [{"name": "Testquelle", "address": self.address}])  # v1.03

    def test_nonce_cannot_be_reused(self):  # v1.03
        from urllib.request import urlopen, Request  # v1.03
        with urlopen(self.address + "/challenge") as reply:  # v1.03
            nonce = json.load(reply)["challenge"]  # v1.03
        headers = {"X-MLL-Nonce": nonce, "X-MLL-Signature": s.mac("test-code-long-enough", nonce + " /tables")}  # v1.03
        with urlopen(Request(self.address + "/tables", headers=headers)) as reply:  # v1.03
            reply.read()  # v1.03
        with self.assertRaises(HTTPError):  # v1.03
            urlopen(Request(self.address + "/tables", headers=headers))  # v1.03


class DialogRefreshTests(unittest.TestCase):  # v1.05
    def test_dialog_receives_current_pages_refresh_callback(self):  # v1.05
        from unittest.mock import MagicMock  # v1.05
        from _web import web_table_sync as web  # v1.05
        callback, builder = MagicMock(), MagicMock()  # v1.05
        with patch.object(web, "_open_dialog", builder):  # v1.05
            web.open_dialog(on_changed=callback)  # v1.05
        builder.assert_called_once_with(on_changed=callback)  # v1.05


class StartupTests(unittest.IsolatedAsyncioTestCase):  # v1.03
    async def test_saved_source_is_disabled_on_start(self):  # v1.03
        from types import SimpleNamespace  # v1.03
        from unittest.mock import MagicMock  # v1.03
        from _web import web_table_sync as web  # v1.03
        with tempfile.TemporaryDirectory() as folder:  # v1.03
            s.save_settings(folder, {"enabled": True, "name": "Quelle", "code": "keep-this-code", "selected": ["DCC"]})  # v1.03
            app = MagicMock()  # v1.03
            web.install(app, SimpleNamespace(data_dir=folder), lambda: None, "4.79")  # v1.03
            saved = s.read_settings(folder)  # v1.03
            self.assertFalse(saved["enabled"])  # v1.03
            self.assertEqual(saved["selected"], ["DCC"])  # v1.03
            self.assertEqual(saved["code"], "keep-this-code")  # v1.03
            def discard(coro):  # v1.03
                coro.close()  # v1.03
            with patch.object(web.asyncio, "create_task", side_effect=discard), patch.object(s, "Share") as share:  # v1.03
                await app.on_startup.call_args.args[0]()  # v1.03
                share.assert_not_called()  # v1.03


class TranslationTests(unittest.TestCase):  # v1.03
    def test_dialog_and_validation_texts_in_all_languages(self):  # v1.03
        import ast, csv, string  # v1.03
        from _web.web_i18n import use_language, tr  # v1.03
        base = Path(__file__).parent  # v1.03
        with (base / "csv/Web_Languages.csv").open(encoding="utf-8-sig", newline="") as handle:  # v1.03
            catalog = {row[0]: row for row in csv.reader(handle, delimiter=";") if row}  # v1.03
        keys = set()  # v1.03
        for rel in ("_web/web_table_sync.py", "headless/headless_table_sync.py"):  # v1.03
            tree = ast.parse((base / rel).read_text(encoding="utf-8"))  # v1.03
            for node in ast.walk(tree):  # v1.03
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("tr", "ValueError", "RuntimeError") and node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):  # v1.03
                    keys.add(node.args[0].value)  # v1.03
        keys.add("Datenübertragung")  # v1.03
        for key in keys:  # v1.03
            self.assertIn(key, catalog)  # v1.03
            values = {name: "Test" for _, name, _, _ in string.Formatter().parse(key) if name}  # v1.03
            for language in range(7):  # v1.03
                with self.subTest(key=key, language=language), use_language(language):  # v1.03
                    self.assertTrue(catalog[key][language].strip())  # v1.03
                    self.assertEqual(tr(key, **values), catalog[key][language].format(**values))  # v1.03


if __name__ == "__main__":  # v1.03
    unittest.main()  # v1.03
