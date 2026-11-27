# Datei-Version: 1.00 (2026-11-26) - test_pico_device_dialog.py
# ----------------------------------------------------------------------------------------------
# Name:           test_pico_device_dialog.py
# Path:           test_pico_device_dialog.py
# Version:        1.00
# Last Update:    2026-11-26
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-26  Neu: Geraeteauswahl fuer die Firmware-Installation des Pico (web_form_comport 1.45, _fw_mode): nur Pico-Geraete, auch unbekannte und andere MobaLedLib Geraete
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_pico_device_dialog.py

Prueft die Regeln der Geraeteauswahl im Firmware-Modus ohne Browser: Liste (nur Pico-Geraete, Servo-Module waehlbar), Blatt und Build Optionen bleiben unveraendert.
Die Anschlussliste des Rechners wird ersetzt, es wird kein Anschluss geoeffnet."""
import os
import sys
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


PORTS = [port("COM3", 0x1A86, "USB-SERIAL CH340 (COM3)", 0x7523),                 # Nano
         port("COM4", 0x10C4, "Silicon Labs CP210x USB to UART Bridge (COM4)", 0xEA60),  # ESP32
         port("COM5", 0x2E8A, "USB Serial Device (COM5)", 0x000A, "E661"),         # Pico
         port("COM6", 0x2E8A, "USB Serial Device (COM6)", 0x000A, "E662"),         # Pico, spaeter als Servo-Modul erkannt
         port("COM7", 0x0403, "FTDI Geraet (COM7)", 0x6001),                        # FTDI: gilt als Nano
         port("COM8", 0x1234, "Mystery Device (COM8)", 0x0001)]                    # keinem Typ zuzuordnen


class FirmwareDeviceTests(unittest.TestCase):
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
        import proggen.M07_COM_Port as M07
        import proggen.M07_COM_Port_New as M07New
        cls.F00, cls.M07, cls.M07New = F00, M07, M07New

    def setUp(self):
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
        self.form._fw_mode = True

    def tearDown(self):
        self.form._fw_mode = False
        self.M07.portlist.comports = self.original
        self.M07New.Ident_Send_Keepalive, self.M07New._Ident_Post = self.saved
        self.M07.SERVO_PORTS.pop("COM6", None)

    def test_only_pico_devices_are_listed(self):
        self.form._compute_new()
        self.assertEqual([r["dev"] for r in self.form._rows], ["COM5", "COM6"])        # Nano, ESP32 und das unbekannte Geraet fehlen
        self.assertEqual({r["typ"] for r in self.form._rows}, {"Pico"})

    def test_unknown_ports_with_checkbox(self):
        self.form._show_unknown = True                                                 # Kontrollkaestchen eingeschaltet
        self.form._compute_new()
        rows = {r["dev"]: r["typ"] for r in self.form._rows}
        self.assertEqual(rows, {"COM5": "Pico", "COM6": "Pico", "COM8": "unbekannt"})  # Nano und ESP32 bleiben ausgeschlossen
        self.assertTrue(all(self.form._is_selectable(r) for r in self.form._rows))

    def test_no_image_for_other_mobaledlib_devices(self):
        self.M07.SERVO_PORTS["COM6"] = "Servo"
        self.form._compute_new()
        self.form._sel_dev = "COM5"
        self.assertTrue(self.form._board_view()["image"])                              # Pico: Bild
        self.form._sel_dev = "COM6"
        self.assertEqual(self.form._board_view()["image"], "")                         # Andere MobaLedLib Geraete: kein Bild

    def test_device_with_same_platform_as_firmware_is_preferred(self):
        self.form._fw_platform = "MLL512V1"
        self.form._info["COM6"] = (0, {"kind": "servo", "type": "PICOSERVO", "ver": "1.0", "platform": "MLL512V1"}, 1)
        self.form._info["COM5"] = (0, {"platform": "PICO", "ver": "1.0"}, 1)
        self.form._compute_new()
        self.assertEqual(self.form._sel_dev, "COM6")                                   # COM5 waere sonst die erste Zeile
        self.form._sel_dev, self.form._sel_user = "COM5", True                         # eigene Wahl des Anwenders bleibt
        self.form._compute_new()
        self.assertEqual(self.form._sel_dev, "COM5")

    def test_without_platform_the_first_device_is_selected(self):
        self.form._fw_platform = ""
        self.form._info["COM6"] = (0, {"kind": "servo", "type": "PICOSERVO", "ver": "1.0", "platform": "MLL512V1"}, 1)
        self.form._compute_new()
        self.assertEqual(self.form._sel_dev, "COM5")

    def test_identity_string_is_parsed_tolerantly(self):
        kv = self.M07New._Kv
        for typ in ("PICOSERVO", "PICOSOUND", "PICO2X3"):                              # die Zeilen der Geraete
            self.assertEqual(kv("~MLLINFO type=%s platform=MLL512V1 ver=1.1\r\n" % typ, "~MLLINFO "),
                             {"type": typ, "platform": "MLL512V1", "ver": "1.1"})
        base = {"type": "PICOSERVO", "platform": "MLL512V1", "ver": "1.1"}
        cases = [
            "~MLLINFO type=PICOSERVO platform=MLL512V1 ver=1.1 neu=abc",               # unbekannter Schluessel wird ignoriert
            "~MLLINFO neu=abc type=PICOSERVO platform=MLL512V1 ver=1.1 nochmehr=1=2",
            "~MLLINFO type=PICOSERVO platform=MLL512V1 ver=1.1 allein",                # Eintrag ohne =
            "~MLLINFO TYPE=picoservo Platform=MLL512V1 VER=1.1",                       # Gross-/Kleinschreibung
            "~MLLINFO type=\"PICOSERVO\" platform='MLL512V1' ver=1.1",                  # Anfuehrungszeichen
            "~MLLINFO type=PICOSERVO,platform=MLL512V1;ver=1.1",                       # Komma und Semikolon
            "rst:0x1 (POWERON) ~MLLINFO   type=PICOSERVO   platform=MLL512V1\tver=1.1\x00",   # Zeichen davor, mehrere Trenner, Steuerzeichen
            "~MLLINFO type = PICOSERVO platform = MLL512V1 ver = 1.1",                 # Leerzeichen um das =
        ]
        for line in cases:
            got = kv(line, "~MLLINFO ")
            for key, value in base.items():
                self.assertEqual(got.get(key), value, line)
        self.assertIsNone(kv("~MLLINFO", "~MLLINFO "))                                  # Echo des Befehls ohne Angaben
        self.assertEqual(kv("~MLLINFO ", "~MLLINFO "), {})
        self.assertEqual(self.M07New.Parse_Kv("a=1 a=2"), {"a": "1"})                  # doppelter Schluessel: der erste gilt
        self.assertEqual(self.M07New.Parse_Kv(None), {})

    def test_allowed_protocols_come_from_the_machine_list(self):
        from _web import web_startpage as SP
        self.assertEqual(SP.protocols_for_platform("PICO"), ["DCC"])                     # PicoZero und MoLLi: nur DCC
        self.assertEqual(SP.protocols_for_platform("ESP32"), ["DCC", "LNet", "CAN", "Selectrix"])
        self.assertEqual(SP.protocols_for_platform("AM328"), ["DCC", "LNet", "CAN", "Selectrix"])   # Classic: alle (Mini nur DCC), Vereinigung
        self.assertIsNone(SP.protocols_for_platform("MLL512V1"))                         # kein Lichtmaschinen-Eintrag (isCentral aus)
        self.assertIsNone(SP.protocols_for_platform(None))

    def test_missing_or_empty_image_is_detected(self):
        from _web import web_startpage as SP
        self.assertTrue(SP.image_exists(ROOT, "LED_image.png"))
        self.assertFalse(SP.image_exists(ROOT, ""))                                     # leer: leeres Bild
        self.assertFalse(SP.image_exists(ROOT, None))
        self.assertFalse(SP.image_exists(ROOT, "gibt_es_nicht.png"))                   # Datei fehlt: leeres Bild
        self.assertFalse(SP.image_exists(ROOT, "../csv/Lichtmaschinen_prop.json"))     # nur Dateien aus dem Ordner images

    def test_devices_and_platforms_are_separate_lists(self):
        from _web import web_startpage as SP
        machines = SP.load_machines(ROOT)
        self.assertEqual([m["key"] for m in machines], ["Classic", "Mini", "Pro", "PicoZero", "MoLLi"])   # nur Lichtmaschinen
        self.assertTrue(all("isCentral" not in m for m in machines))
        platforms = {m["platform"]: m for m in SP.load_platforms(ROOT)}
        self.assertEqual(set(platforms), {"MLL512V1", "MLLS88GWV1"})
        for entry in platforms.values():
            self.assertEqual(set(entry), {"platform", "name", "text", "image"})
        self.assertIn("Selectrix", SP.supported_protocols("Classic"))                    # Feld protocols (frueher centrals)
        self.assertNotIn("Selectrix", SP.supported_protocols("PicoZero"))
        self.assertEqual(SP.machine_for_port_type("Pico"), "PicoZero")

    def test_platform_name_and_image(self):
        import json
        import tempfile
        from _web import web_startpage as SP
        with tempfile.TemporaryDirectory() as base:
            os.makedirs(os.path.join(base, "csv"))
            os.makedirs(os.path.join(base, "images"))
            open(os.path.join(base, "images", "mit.png"), "wb").write(b"x")
            data = {"devices": [{"key": "A", "name": "Lichtmaschine A", "platform": "PICO", "board": "Pico", "protocols": ["DCC"]}],
                    "platforms": [{"platform": "P1", "name": "Mit Bild", "image": "mit.png"}, {"platform": "P2", "name": "Ohne Bild", "image": ""},
                                  {"platform": "P3", "name": "Datei fehlt", "image": "fehlt.png"}]}
            with open(os.path.join(base, "csv", "Lichtmaschinen_prop.json"), "w", encoding="utf-8") as fh:
                json.dump(data, fh)
            self.assertEqual(SP.platform_name("P1", base), "Mit Bild")
            self.assertEqual(SP.platform_name("p2", base), "Ohne Bild")                  # Gross-/Kleinschreibung egal
            self.assertEqual(SP.platform_name("PICO", base), "Lichtmaschine A")          # nicht in platforms: die devices
            self.assertIsNone(SP.platform_name("UNBEKANNT", base))
            self.assertEqual(SP.platform_image("P1", base), "mit.png")
            self.assertIsNone(SP.platform_image("P2", base))                             # kein Bild eingetragen
            self.assertIsNone(SP.platform_image("P3", base))                             # Datei nicht gefunden
            self.assertIsNone(SP.platform_image("PICO", base))                           # devices haben hier kein Plattform-Bild
            self.assertIsNone(SP.platform_image("", base))

    def test_dialog_image_comes_from_platforms_when_available(self):
        from _web import web_startpage as SP
        original = SP.platform_image
        SP.platform_image = lambda plat, base_dir=None: "PICO_image.png" if plat == "MLL512V1" else None
        try:
            self.form._compute_new()
            self.form._info["COM6"] = (0, {"kind": "servo", "type": "PICOSERVO", "ver": "1.0", "platform": "MLL512V1"}, 1)
            self.M07.SERVO_PORTS["COM6"] = "1.0"
            self.form._compute_new()
            self.form._sel_dev = "COM6"
            self.assertEqual(self.form._board_view()["image"], "/mll_images/PICO_image.png")       # Bild der Plattform, auch bei 'Andere MobaLedLib Geraete'
            self.form._info["COM6"] = (0, {"kind": "servo", "type": "PICOSERVO", "ver": "1.0", "platform": "UNBEKANNT"}, 1)
            self.assertEqual(self.form._board_view()["image"], "")                                  # kein Bild bekannt: wie bisher keines
            self.form._sel_dev = "COM5"
            self.assertTrue(self.form._board_view()["image"])                                       # Pico: Bild des Boards
        finally:
            SP.platform_image = original

    def test_other_mobaledlib_devices_are_selectable(self):
        self.M07.SERVO_PORTS["COM6"] = "Servo"                                         # als Servo-Modul erkannt
        self.form._compute_new()
        rows = {r["dev"]: r for r in self.form._rows}
        self.assertEqual(rows["COM6"]["typ"], "Servo")
        self.assertTrue(self.form._is_selectable(rows["COM6"]))
        self.form._fw_mode = False
        self.assertFalse(self.form._is_selectable(rows["COM6"]))                       # als Lichtmaschine bleibt es gesperrt

    def test_stored_port_that_is_gone_is_not_listed(self):
        self.form._stored_port = "COM9"
        self.form._compute_new()
        self.assertNotIn("COM9", [r["dev"] for r in self.form._rows])

    def test_sheet_is_not_touched(self):
        self.assertEqual(self.form._sheet_group(), "Pico")
        self.assertFalse(self.form._apply_group("Classic"))
        self.assertFalse(self.form._apply_group("Pro"))

    def test_placeholder_port_is_no_device(self):
        for value in ("COM?", "NO DEVICE", "999", "-3", "", None):
            self.assertEqual(self.form._norm_port(value), "", value)
        self.assertEqual(self.form._norm_port("COM3"), "COM3")
        self.form._fw_mode = False
        self.M07.portlist.comports = lambda include_links=False: []           # kein Geraet angeschlossen
        self.form._stored_port = self.form._norm_port("COM?")
        self.form._compute_new()
        self.assertEqual(self.form._rows, [])                                 # keine Zeile COM?
        self.assertIsNone(self.form._sel_dev)                                 # nichts gewaehlt

    def test_normal_mode_is_unchanged(self):
        self.form._fw_mode = False
        self.form._compute_new()
        devs = [r["dev"] for r in self.form._rows]
        self.assertIn("COM3", devs)
        self.assertIn("COM4", devs)
        self.assertIn("COM5", devs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
