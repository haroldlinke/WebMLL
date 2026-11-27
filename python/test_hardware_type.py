# Datei-Version: 1.00 (2026-11-27) - test_hardware_type.py
# ----------------------------------------------------------------------------------------------
# Name:           test_hardware_type.py
# Path:           test_hardware_type.py
# Version:        1.00
# Last Update:    2026-11-27
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-27  Neu: Haupttyp der Lichtmaschine in den Hardware Optionen (web_form_options 1.80) und Geraeteauswahl nur mit Geraeten des eingestellten Typs (web_form_comport 1.52)
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_hardware_type.py

Benutzt die echte Arbeitsmappe (HeadlessAppController, wie test_pico_device_dialog.py) und die echten Formulare F00.Select_COM_Port_UserForm und F00.UserForm_Options.
Ersetzt werden nur die Anschlussliste des Rechners, die Ident-Befehle, die Abfragen ueber die Anschluesse und die Rueckfrage (MsgBox). Es wird kein Anschluss geoeffnet.
Nicht geprueft: Oberflaeche (NiceGUI, Auswahlfeld), echte Hardware."""
import os
import sys
import json
import tempfile
import unittest
from types import SimpleNamespace

ROOT = os.path.dirname(os.path.abspath(__file__))
os.environ["MLL_HEADLESS"] = "1"
os.environ["MLL_DATA_DIR"] = tempfile.mkdtemp(prefix="mll_test_")
sys.path.insert(0, ROOT)
os.chdir(ROOT)


def port(device, vid, desc, pid=0x0001, serial=""):
    return SimpleNamespace(device=device, description=desc, hwid="USB VID:PID=%04X:%04X" % (vid, pid), vid=vid, pid=pid, serial_number=serial)


PORTS = [port("COM3", 0x1A86, "USB-SERIAL CH340 (COM3)", 0x7523),                 # Nano oder Uno (CH340)
         port("COM4", 0x10C4, "Silicon Labs CP210x USB to UART Bridge (COM4)", 0xEA60),  # ESP32
         port("COM5", 0x2E8A, "USB Serial Device (COM5)", 0x000A, "E661"),         # Pico
         port("COM6", 0x2E8A, "USB Serial Device (COM6)", 0x000A, "E662"),         # Pico, im Test als Servo-Modul erkannt
         port("COM7", 0x2341, "Arduino Uno (COM7)", 0x0043),                        # Uno mit 16U2 (gilt auch als Nano-artig)
         port("COM8", 0x1234, "Mystery Device (COM8)", 0x0001)]                    # keinem Typ zuzuordnen


class Base(unittest.TestCase):
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
        import proggen.F00_mainbuttons as F00
        import proggen.M02_Public as M02
        import proggen.M25_Columns as M25
        import proggen.M07_COM_Port as M07
        import proggen.M07_COM_Port_New as M07New
        import ExcelAPI.XLA_Application as P01
        cls.F00, cls.M02, cls.M25, cls.M07, cls.M07New, cls.P01 = F00, M02, M25, M07, M07New, P01
        M25.Make_sure_that_Col_Variables_match()

    def set_buildopt(self, text):
        self.P01.CellDict[self.M02.SH_VARS_ROW, self.M25.BUILDOP_COL] = text

    def buildopt(self):
        return str(self.P01.Cells(self.M02.SH_VARS_ROW, self.M25.BUILDOP_COL).Value or "")


class DeviceListTests(Base):
    def setUp(self):
        self.saved_buildopt = self.buildopt()
        self.form = self.F00.Select_COM_Port_UserForm
        self.original = self.M07.portlist.comports
        self.M07.portlist.comports = lambda include_links=False: list(PORTS)
        self.saved = (self.M07New.Ident_Send_Keepalive, self.M07New._Ident_Post)
        self.M07New.Ident_Send_Keepalive = lambda *a, **k: None
        self.M07New._Ident_Post = lambda *a, **k: None
        self.form._info_refresh = lambda *a, **k: None                        # keine Abfrage ueber die Anschluesse
        self.form._info, self.form._boot, self.form._boot_busy = {}, {}, set()
        self.form._rows, self.form._sel_dev, self.form._prev_devs, self.form._old_comport = [], None, None, None
        self.form._stored_port = ""
        self.form._show_unknown = False
        self.form._fw_platform, self.form._sel_user = "", False
        self.form._fw_mode = False

    def tearDown(self):
        self.M07.portlist.comports = self.original
        self.M07New.Ident_Send_Keepalive, self.M07New._Ident_Post = self.saved
        self.M07.SERVO_PORTS.pop("COM6", None)
        del self.form._info_refresh
        self.set_buildopt(self.saved_buildopt)

    def devs(self):
        self.form._compute_new()
        return [(r["typ"], r["dev"]) for r in self.form._rows]

    def test_classic_shows_only_nano_like_ports(self):
        self.set_buildopt(self.M02.BOARD_NANO_NEW)
        self.assertEqual(self.devs(), [("Classic", "COM3"), ("Classic", "COM7")])   # kein ESP32, kein Pico, keine andere Gruppe

    def test_pro_shows_only_esp32(self):
        self.set_buildopt(self.M02.BOARD_ESP32)
        self.assertEqual(self.devs(), [("Pro", "COM4")])

    def test_pico_shows_other_mobaledlib_devices_in_own_group(self):
        self.set_buildopt(self.M02.BOARD_PICO)
        self.M07.SERVO_PORTS["COM6"] = "Servo"
        self.assertEqual(self.devs(), [("Pico", "COM5"), ("Servo", "COM6")])         # 'Andere MobaLedLib Geraete' als eigene Gruppe nach den Pico-Geraeten
        self.assertTrue(self.form._is_selectable(self.form._row("COM6")))           # waehlbar (5.66) ...
        self.assertTrue(self.form._needs_confirm(self.form._row("COM6")))           # ... mit Sicherheitsabfrage bei OK
        self.assertFalse(self.form._needs_confirm(self.form._row("COM5")))
        self.assertEqual(self.form._sel_dev, "COM5")                                 # vorgewaehlt bleibt der Pico

    def test_other_device_is_never_selected_automatically(self):
        self.set_buildopt(self.M02.BOARD_PICO)
        self.M07.SERVO_PORTS["COM6"] = "Servo"
        ports = list(PORTS)
        self.M07.portlist.comports = lambda include_links=False: [p for p in ports if p.device not in ("COM5", "COM6")]
        self.devs()
        self.M07.portlist.comports = lambda include_links=False: [p for p in ports if p.device != "COM5"]   # Servo-Modul neu angesteckt
        self.devs()
        self.assertIsNone(self.form._sel_dev)                                        # nicht von selbst gewaehlt
        self.form._sel_dev = "COM6"                                                  # Klick des Anwenders
        self.devs()
        self.assertEqual(self.form._sel_dev, "COM6")

    def test_other_mobaledlib_devices_not_for_classic_and_pro(self):
        self.M07.SERVO_PORTS["COM6"] = "Servo"
        for board in (self.M02.BOARD_NANO_NEW, self.M02.BOARD_ESP32):
            self.set_buildopt(board)
            self.assertNotIn("Servo", [t for t, _d in self.devs()])

    def test_uno_lists_classic_ports_shown_as_uno(self):
        self.set_buildopt(self.M02.BOARD_UNO_NORM)
        self.assertTrue(self.form._sheet_is_uno())
        self.form._info["COM3"] = (0, {"kind": "nano"}, 1)                            # LEDs_AutoProg hat geantwortet
        self.form._boot["COM3"] = self.M02.BOARD_NANO_NEW                             # der Bootloader eines Uno sieht aus wie Nano neu
        self.assertEqual(self.devs(), [("Classic", "COM3"), ("Classic", "COM7")])
        self.assertEqual(self.form._row("COM3")["shown"], "Uno")

    def test_uno_uses_uno_rules(self):
        ftdi = port("COM9", 0x0403, "USB Serial Port (COM9)", 0x6001)                # Nano Original (FTDI): nur Set AM328
        self.M07.portlist.comports = lambda include_links=False: list(PORTS) + [ftdi]
        self.set_buildopt(self.M02.BOARD_UNO_NORM)
        from test_usb_detect import uno_set_exists
        if uno_set_exists():
            self.assertEqual([d for _t, d in self.devs()], ["COM3", "COM7"])       # Uno: CH340 und 16U2 (Set Uno), kein FTDI-Nano
        else:
            self.assertEqual([d for _t, d in self.devs()], ["COM3", "COM7", "COM9"])   # Set des Uno fehlt in der Datei: keine Einschraenkung
        self.set_buildopt(self.M02.BOARD_NANO_NEW)
        self.assertEqual([d for _t, d in self.devs()], ["COM3", "COM7", "COM9"])   # Classic: Set AM328
        self.set_buildopt(self.M02.BOARD_UNO_NORM)
        self.form._stored_port = "COM9"                                              # im Blatt gespeicherter Anschluss bleibt sichtbar
        self.assertIn("COM9", [d for _t, d in self.devs()])

    def test_uno_keeps_board_on_ok(self):
        self.set_buildopt(self.M02.BOARD_UNO_NORM)
        self.devs()
        self.form._sel_dev = "COM3"
        self.form._boot["COM3"] = self.M02.BOARD_NANO_NEW
        self.form._apply_nano_bootloader()
        self.assertIn(self.M02.BOARD_UNO_NORM, self.buildopt())                       # bleibt Uno
        self.assertNotIn(self.M02.BOARD_NANO_NEW, self.buildopt())

    def test_nano_bootloader_still_applied_for_classic(self):
        self.set_buildopt(self.M02.BOARD_NANO_NEW)
        self.assertFalse(self.form._sheet_is_uno())
        self.devs()
        self.form._sel_dev = "COM3"
        self.form._boot["COM3"] = self.M02.BOARD_NANO_OLD
        self.form._apply_nano_bootloader()
        self.assertIn(self.M02.BOARD_NANO_OLD, self.buildopt())

    def test_image_follows_sheet_device(self):
        opts = dict(getattr(self.P01.ActiveSheet, "esp32_options", None) or {})
        try:
            self.set_buildopt(self.M02.BOARD_UNO_NORM)
            self.P01.ActiveSheet.esp32_options = {}
            self.devs()
            self.assertEqual(self.form._board_view()["image"], "")                    # Uno ohne eigenes Bild: leere Flaeche (nicht das Bild der Classic)
            self.set_buildopt(self.M02.BOARD_NANO_NEW)
            self.assertTrue(self.form._board_view()["image"].lower().endswith("led_image.png"))
            self.set_buildopt(self.M02.BOARD_PICO)
            self.P01.ActiveSheet.esp32_options = {"device": "MoLLi"}
            self.devs()
            self.form._sel_dev = "COM5"
            self.assertTrue(self.form._board_view()["image"].lower().endswith("molli_image.png"))
            self.M07.SERVO_PORTS["COM6"] = "Servo"
            self.devs()
            self.form._sel_dev = "COM6"
            self.assertEqual(self.form._board_view()["image"], "")                    # anderes Geraet ohne Plattformbild (noch keine Antwort auf ~MLLINFO)
        finally:
            self.P01.ActiveSheet.esp32_options = opts

    def test_unknown_ports_with_checkbox(self):
        self.set_buildopt(self.M02.BOARD_ESP32)
        self.form._show_unknown = True
        self.assertEqual(self.devs(), [("Pro", "COM4"), ("unbekannt", "COM8")])

    def test_stored_unknown_port_counts_as_sheet_type(self):
        self.set_buildopt(self.M02.BOARD_PICO)
        self.form._stored_port = "COM8"
        self.assertIn(("Pico", "COM8"), self.devs())
        self.assertEqual(self.form._sel_dev, "COM8")

    def test_firmware_mode_unchanged(self):
        self.set_buildopt(self.M02.BOARD_NANO_NEW)
        self.form._fw_mode = True
        try:
            self.M07.SERVO_PORTS["COM6"] = "Servo"
            self.assertEqual([d for _t, d in self.devs()], ["COM5", "COM6"])          # Firmware-Auswahl: Pico-Geraete und Servo-Module wie bisher
        finally:
            self.form._fw_mode = False


class MainTypeTests(Base):
    def setUp(self):
        self.saved_buildopt = self.buildopt()
        self.saved_port = self.P01.Cells(self.M02.SH_VARS_ROW, self.M25.COMPort_COL).Value
        self.saved_opts = dict(getattr(self.P01.ActiveSheet, "esp32_options", None) or {})
        self.P01.ActiveSheet.esp32_options = {}
        from _web import web_form_options as WO
        self.WO = WO
        WO._LAST_NANO.clear()
        self.opt = self.F00.UserForm_Options
        self.opt._web_prepare(True)
        self.questions = []
        self.detects = []
        self.saved_msgbox = self.P01.MsgBox
        self.P01.MsgBox = lambda text, *a, **k: (self.questions.append(text), self.answer)[1]
        self.answer = 7                                                              # vbNo
        name = "_" + type(self.opt).__name__ + "__Detect_LED_Port_Button_Click"
        self.detect_name = name
        setattr(self.opt, name, lambda: self.detects.append(self.buildopt()))

    def tearDown(self):
        self.P01.MsgBox = self.saved_msgbox
        delattr(self.opt, self.detect_name)
        self.set_buildopt(self.saved_buildopt)
        self.P01.CellDict[self.M02.SH_VARS_ROW, self.M25.COMPort_COL] = self.saved_port
        self.P01.ActiveSheet.esp32_options = self.saved_opts

    def port_cell(self):
        return str(self.P01.Cells(self.M02.SH_VARS_ROW, self.M25.COMPort_COL).Value).strip()

    def test_device_groups_from_json(self):
        groups = self.WO.device_groups()
        import json
        with open(os.path.join(ROOT, "csv", "Lichtmaschinen_prop.json"), encoding="utf-8") as fh:
            data = json.load(fh)
        plat_names = {p["platform"]: p["name"] for p in data["platforms"]}
        plat_prio = {plat_names.get(p["platform"], p["platform"]): p.get("sortPriority", 0) for p in data["platforms"]}
        dev_prio = {d["key"]: d.get("sortPriority", 0) for d in data["devices"]}
        names = [g for g, _items in groups]
        self.assertEqual(names, sorted(names, key=lambda n: (-plat_prio.get(n, 0), n.lower())))   # Gruppen: hoechste sortPriority zuerst, dann Name
        for _g, items in groups:
            self.assertEqual(items, sorted(items, key=lambda d: (-dev_prio.get(d[0], 0), d[1].lower())))   # Eintraege ebenso
        for d in data["devices"]:                                                     # jedes Geraet steht unter dem Namen seiner Plattform
            group = plat_names.get(d["platform"], d["platform"])
            self.assertIn(d["key"], [k for g, items in groups if g == group for k, _n, _m in items])
        unos = [d for d in data["devices"] if str(d.get("board", "")).lower() == "uno"]
        if unos:                                                                      # Uno steht in devices: kein zusaetzlicher Eintrag
            self.assertNotIn(self.WO.UNO_DEVICE, [d for _g, items in groups for d in items])
            self.assertEqual(self.WO.device_entry(groups, unos[0]["key"])[2], "Uno")
        else:
            am328 = plat_names.get("AM328", "AM328")
            self.assertIn(self.WO.UNO_DEVICE, dict(groups)[am328])                    # kein Uno in devices: Eintrag Arduino Uno

    def test_sort_priority(self):
        tmp = tempfile.mkdtemp(prefix="mll_sort_")
        os.makedirs(os.path.join(tmp, "csv"))
        data = {"devices": [{"key": "A", "name": "Alpha", "platform": "AM328", "board": "Nano"},
                            {"key": "B", "name": "Beta", "platform": "AM328", "board": "Nano", "sortPriority": 20},
                            {"key": "C", "name": "Gamma", "platform": "AM328", "board": "Uno", "sortPriority": 20},
                            {"key": "P", "name": "Pro", "platform": "ESP32", "board": "ESP32"},
                            {"key": "Z", "name": "Zero", "platform": "PICO", "board": "Pico"}],
                "platforms": [{"platform": "ESP32", "name": "ESP32", "sortPriority": 50}, {"platform": "PICO", "name": "Raspberry Pico", "sortPriority": 40},
                              {"platform": "AM328", "name": "ATMega", "sortPriority": 30}]}
        with open(os.path.join(tmp, "csv", "Lichtmaschinen_prop.json"), "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        try:
            groups = self.WO.device_groups(tmp)
        finally:
            from _web import web_startpage as SP
            SP.load_machines(ROOT)                                                   # globale Liste wieder aus der echten Datei
        self.assertEqual([g for g, _i in groups], ["ESP32", "Raspberry Pico", "ATMega"])   # 50, 40, 30
        self.assertEqual([k for k, _n, _m in dict(groups)["ATMega"]], ["B", "C", "A"])     # 20 Beta, 20 Gamma (Name), 0 Alpha

    def test_sheet_device(self):
        groups = [("ATMega", [("Classic", "Lichtmaschine Classic", "Classic"), ("Mini", "Lichtmaschine Mini", "Classic"), ("Uno", "Arduino Uno", "Uno")]),
                  ("ESP32", [("Pro", "Lichtmaschine Pro", "Pro")])]
        self.assertEqual(self.WO.sheet_device(groups, "Classic", None)[0], "Classic")
        self.assertEqual(self.WO.sheet_device(groups, "Classic", "Mini")[0], "Mini")  # gespeicherter key passt zum Haupttyp
        self.assertEqual(self.WO.sheet_device(groups, "Pro", "Mini")[0], "Pro")       # passt nicht: erster Eintrag des Haupttyps
        self.assertIsNone(self.WO.sheet_device(groups, "Pico", None))

    def test_default_device_per_platform(self):
        groups = [("ATMega", [("Classic", "Lichtmaschine Classic", "Classic"), ("Mini", "Lichtmaschine Mini", "Classic"), ("Uno", "Arduino Uno", "Uno")]),
                  ("Raspberry Pico", [("MoLLi", "Lichtmaschine MoLLi", "Pico"), ("PicoZero", "Lichtmaschine Pico Zero", "Pico")])]
        defaults = ["Classic", "PicoZero"]
        self.assertEqual(self.WO.sheet_device(groups, "Pico", None)[0], "MoLLi")             # ohne Vorgabe: erster Eintrag
        self.assertEqual(self.WO.sheet_device(groups, "Pico", None, defaults)[0], "PicoZero")  # Vorgabe der Plattform
        self.assertEqual(self.WO.sheet_device(groups, "Pico", "MoLLi", defaults)[0], "MoLLi")  # im Blatt gespeichert: hat Vorrang
        self.assertEqual(self.WO.sheet_device(groups, "Uno", None, defaults)[0], "Uno")        # Vorgabe Classic passt nicht zum Haupttyp Uno
        self.assertEqual(self.WO.sheet_device(groups, "Classic", "PicoZero", defaults)[0], "Classic")

    def test_defaults_from_json(self):
        import json
        with open(os.path.join(ROOT, "csv", "Lichtmaschinen_prop.json"), encoding="utf-8") as fh:
            data = json.load(fh)
        wanted = [p["defaultDevice"] for p in data["platforms"] if p.get("defaultDevice")]
        self.assertEqual(self.WO.default_devices(), wanted)
        self.assertIn("PicoZero", wanted)
        self.assertIn("Classic", wanted)
        self.set_buildopt(self.M02.BOARD_PICO)                                         # Blatt ohne gespeicherte Lichtmaschine
        self.assertEqual(self.opt._web_device()[0], "PicoZero")
        self.set_buildopt(self.M02.BOARD_NANO_NEW)
        self.assertEqual(self.opt._web_device()[0], "Classic")

    def test_main_type_of(self):
        M02, f = self.M02, self.WO.main_type_of
        self.assertEqual(f(M02.HT_ESP32, M02.BOARD_ESP32, M02), "Pro")
        self.assertEqual(f(M02.HT_PICO, M02.BOARD_PICO, M02), "Pico")
        self.assertEqual(f(M02.HT_AM328, M02.BOARD_UNO_NORM, M02), "Uno")
        self.assertEqual(f(M02.HT_AM328, M02.BOARD_NANO_OLD, M02), "Classic")
        self.assertEqual(f(M02.HT_AM328, None, M02), "Classic")

    def test_change_resets_port_and_asks(self):
        self.set_buildopt(self.M02.BOARD_NANO_FULL)
        self.P01.CellDict[self.M02.SH_VARS_ROW, self.M25.COMPort_COL] = "COM3"
        self.assertEqual(self.opt._web_main_type(), "Classic")
        self.assertTrue(self.opt._web_change_main_type("Pro"))
        self.assertEqual(self.buildopt(), self.M02.BOARD_ESP32)
        self.assertEqual(self.port_cell(), "")                                        # COM Port zurueckgesetzt
        self.assertEqual(len(self.questions), 1)                                      # Rueckfrage zur Suche
        self.assertIn("Lichtmaschine Pro", self.questions[0])                          # Name aus devices
        self.assertEqual(self.detects, [])                                            # Nein: keine Suche
        self.assertEqual(self.opt.boardlist[self.opt.rb_res["_L"].get()], self.M02.BOARD_ESP32)  # Auswahl des Formulars folgt
        self.assertEqual(self.P01.ActiveSheet.esp32_options.get("device"), "Pro")    # key im Blatt

    def test_change_with_search(self):
        self.set_buildopt(self.M02.BOARD_ESP32)
        self.answer = 6                                                              # vbYes
        self.assertTrue(self.opt._web_change_main_type("MoLLi"))
        self.assertEqual(self.detects, [self.M02.BOARD_PICO])                         # Geraeteauswahl mit dem neuen Typ
        self.assertEqual(self.opt._web_device()[0], "MoLLi")                          # das Menue zeigt die gewaehlte Lichtmaschine

    def test_classic_to_uno_resets_port(self):
        self.set_buildopt(self.M02.BOARD_NANO_OLD)
        self.P01.CellDict[self.M02.SH_VARS_ROW, self.M25.COMPort_COL] = "COM3"
        self.assertTrue(self.opt._web_change_main_type("Uno"))
        self.assertIn(self.M02.BOARD_UNO_NORM, self.buildopt())
        self.assertEqual(self.port_cell(), "")
        self.assertTrue(self.opt._web_change_main_type("Classic"))                    # zurueck: die zuletzt benutzte Nano-Variante
        self.assertIn(self.M02.BOARD_NANO_OLD, self.buildopt())

    def test_same_main_type_keeps_port(self):
        self.set_buildopt(self.M02.BOARD_NANO_NEW)
        self.P01.CellDict[self.M02.SH_VARS_ROW, self.M25.COMPort_COL] = "COM3"
        self.assertFalse(self.opt._web_change_main_type("Mini"))                      # Classic -> Mini: gleiche Hardware
        self.assertEqual(self.port_cell(), "COM3")
        self.assertEqual(self.questions, [])
        self.assertEqual(self.opt._web_device()[0], "Mini")                           # trotzdem gemerkt
        self.assertFalse(self.opt._web_change_main_type("gibt es nicht"))

    def test_summary_follows_selected_device(self):
        import proggen.M02a_Public as M02a
        self.set_buildopt(self.M02.BOARD_PICO)
        self.P01.ActiveSheet.esp32_options = {"device": "PicoZero"}
        zero = self.opt._board_summary(M02a)
        self.P01.ActiveSheet.esp32_options = {"device": "MoLLi"}
        molli = self.opt._board_summary(M02a)
        self.assertTrue(zero["image"].lower().endswith("pico_image.png"), zero["image"])
        self.assertTrue(molli["image"].lower().endswith("molli_image.png"), molli["image"])   # gleiche Plattform, anderes Bild
        self.set_buildopt(self.M02.BOARD_NANO_NEW)
        self.P01.ActiveSheet.esp32_options = {"device": "Classic"}
        classic = self.opt._board_summary(M02a)
        self.P01.ActiveSheet.esp32_options = {"device": "Mini"}
        mini = self.opt._board_summary(M02a)
        self.assertIn("Selectrix", classic["protocols"])
        self.assertEqual(mini["protocols"], {})                                       # Mini: kein Protokoll -> keine Protokollauswahl
        self.assertEqual(mini["protocol_hint"], "")
        self.assertFalse(self.opt._web_has_protocol())                                # -> kein DCC/Selectrix/LNet Arduino
        self.P01.ActiveSheet.esp32_options = {"device": "Classic"}
        self.assertTrue(self.opt._web_has_protocol())
        self.assertTrue(mini["image"].lower().endswith("mini_image.png"), mini["image"])

    def test_summary_without_image_is_empty(self):
        import proggen.M02a_Public as M02a
        from _web import web_startpage as SP
        self.set_buildopt(self.M02.BOARD_PICO)
        self.P01.ActiveSheet.esp32_options = {"device": "MoLLi"}
        m = SP.machine_by_key("MoLLi")
        saved = m["image"]
        try:
            m["image"] = "gibt_es_nicht.png"                                         # Bilddatei fehlt
            SP_load = SP.load_machines
            SP.load_machines = lambda base_dir: SP.MACHINES                          # Eintrag nicht neu aus der Datei lesen
            try:
                self.assertEqual(self.opt._board_summary(M02a)["image"], "")         # leere Flaeche
            finally:
                SP.load_machines = SP_load
        finally:
            m["image"] = saved

    def test_summary_has_devices_and_no_variants(self):
        import proggen.M02a_Public as M02a
        self.set_buildopt(self.M02.BOARD_UNO_NORM)
        sm = self.opt._board_summary(M02a)
        self.assertEqual((sm["device"], sm["main_type"]), ("Uno", "Uno"))
        self.assertTrue(sm["device_groups"])
        self.assertIsNone(sm["variants"])
        self.assertEqual(sm["line"], "(keine Schnittstelle gewählt)")                 # kein Port im Blatt
        self.assertEqual(sm["hw_label"], "Gerät:")


class TranslationTests(unittest.TestCase):
    TEXTS = ["Anderes MobaLedLib Gerät verwenden?", "Ja, verwenden",
             "An %1 ist keine Lichtmaschine angeschlossen, sondern ein anderes MobaLedLib Gerät (%2).\nDiese Hardware ist für die Lichtmaschine möglicherweise ungeeignet. Das Programm der Lichtmaschine kann die Firmware des Geräts überschreiben.\n\nSoll dieses Gerät wirklich als Lichtmaschine verwendet werden?",
             "Gerät", "keine Schnittstelle gewählt", "an {port}", "Soll jetzt nach der angeschlossenen Lichtmaschine gesucht werden?",
             "Die Lichtmaschine wurde auf {typ} umgestellt. Der COM Port wurde zurückgesetzt."]

    def test_all_languages(self):
        from _web import web_i18n as I
        for n in range(1, 7):
            with I.use_language(n):                                                  # Kontextmanager des echten Uebersetzers
                for t in self.TEXTS:
                    out = I.tr(t, port="COM3", typ="Uno")
                    self.assertNotEqual(out, t.format(port="COM3", typ="Uno"), "Sprache %d: %s" % (n, t))
                    self.assertTrue(("COM3" in out) if "{port}" in t else True)
                    self.assertTrue(("Uno" in out) if "{typ}" in t else True)
        with I.use_language(0):
            self.assertEqual(I.tr("an {port}", port="COM3"), "an COM3")               # Deutsch unveraendert


if __name__ == "__main__":
    unittest.main(verbosity=2)
