# Datei-Version: 1.02 (2026-11-28) - test_usb_detect.py
# ----------------------------------------------------------------------------------------------
# Name:           test_usb_detect.py
# Path:           test_usb_detect.py
# Version:        1.02
# Last Update:    2026-11-28
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.02  2026-11-28  devices.detect verweist auf Regel-Sets (headless_usb_detect 1.02): Verweise, Geraete und Plattformen; die Datei enthaelt die eingebauten Sets
#   1.01  2026-11-27  Vergleich mit der Erkennung des Excel-Programms (EnumComPorts, Ver_3.5.0/Source/M07_COM_Port.bas) an Windows-Bezeichnungen; schwache Regel
#                     'Serielles USB-Gerät' / 'USB Serial Device' (headless_usb_detect 1.01)
#   1.00  2026-11-27  Neu: Regeln detectionRules (csv/Lichtmaschinen_prop.json) und Auswerter headless/headless_usb_detect.py
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_usb_detect.py

Prueft den echten Auswerter mit Ersatzobjekten fuer die Anschluesse (wie pyserial ListPortInfo) und vergleicht das Ergebnis mit den festen Regeln bis 5.60
(M07_COM_Port.Classify_Port, hier als old_classify nachgebildet). Nicht geprueft: echte Anschluesse, Windows-WMI-Zweig (EnumComPorts_old)."""
import json
import os
import shutil
import sys
import tempfile
import unittest
from types import SimpleNamespace

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from headless import headless_usb_detect as UD  # noqa: E402


def port(vid=None, pid=None, desc="", hwid="", manufacturer="", product="", device="COM9"):
    return SimpleNamespace(vid=vid, pid=pid, description=desc, hwid=hwid, manufacturer=manufacturer, product=product, device=device)


def uno_set_exists():
    """Gibt es in der echten Datei ein Regel-Set, auf das eine Lichtmaschine mit board Uno verweist?"""
    with open(os.path.join(ROOT, UD.RULES_FILE), encoding="utf-8") as fh:
        data = json.load(fh)
    names = {k.lower() for k in UD.normalize_rules(data.get("detectionRules"))}
    return any(str(d.get("detect", "")).lower() in names for d in data.get("devices", []) if str(d.get("board", "")).lower() == "uno" and d.get("detect"))


def old_classify(comport):
    """Classify_Port bis 5.60 (ohne Servo)"""
    desc = str(getattr(comport, 'description', '') or '')
    hwid = str(getattr(comport, 'hwid', '') or '').upper()
    vid = getattr(comport, 'vid', None)
    if vid == 0x2E8A or 'VID:PID=2E8A:' in hwid or 'VID:PID=239A:813D' in hwid:
        return 'Pico'
    if vid == 0x10C4 or 'CP210x' in desc or 'CP2102 USB to UART' in desc:
        return 'ESP32'
    if vid in (0x1A86, 0x0403, 0x2341, 0x2A03) or 'CH340' in desc or 'Arduino' in desc or 'FT232' in desc or 'USB2.0-Ser' in desc or 'VID:PID=0403:' in hwid:
        return 'Nano'
    return ''


SAMPLES = [
    port(0x1A86, 0x7523, "USB-SERIAL CH340 (COM3)", "USB VID:PID=1A86:7523 SER= LOCATION=1-1"),
    port(0x0403, 0x6001, "USB Serial Port (COM4)", "USB VID:PID=0403:6001 SER=A9"),          # Nano Original (FTDI)
    port(None, None, "FT232R USB UART", "USB VID:PID=0403:6001"),                             # nur hwid/Beschreibung
    port(0x2341, 0x0043, "Arduino Uno (COM5)", "USB VID:PID=2341:0043"),                      # Uno mit 16U2
    port(0x2A03, 0x0043, "Arduino Uno (COM6)", "USB VID:PID=2A03:0043"),
    port(None, None, "USB2.0-Serial", "n/a"),
    port(0x10C4, 0xEA60, "Silicon Labs CP210x USB to UART Bridge (COM7)", "USB VID:PID=10C4:EA60"),
    port(None, None, "CP2102 USB to UART Bridge Controller", ""),
    port(0x2E8A, 0x000A, "USB Serial Device (COM8)", "USB VID:PID=2E8A:000A SER=E661"),        # Pico
    port(0x2E8A, 0x0003, "RP2 Boot", "USB VID:PID=2E8A:0003"),                                # Pico im Bootmodus
    port(0x239A, 0x813D, "Adafruit Feather RP2040", "USB VID:PID=239A:813D"),
    port(None, None, "x", "USB VID:PID=2E8A:000A"),
    port(0x1234, 0x0001, "Mystery Device", "USB VID:PID=1234:0001"),
    port(None, None, "ttyS0", "n/a"),
    port(0x303A, 0x1001, "USB JTAG/serial debug unit", "USB VID:PID=303A:1001"),               # ESP32-S3 nativ: bisher unbekannt
]


class RuleTests(unittest.TestCase):
    def setUp(self):
        self.rules = UD.normalize_rules(UD.DEFAULT_RULES)

    def test_same_result_as_fixed_rules_until_5_60(self):
        for p in SAMPLES:
            self.assertEqual(UD.legacy_type(UD.platform_for_port(p, rules=self.rules)), old_classify(p), p)

    def test_json_rules_contain_builtin_rules(self):
        with open(os.path.join(ROOT, UD.RULES_FILE), encoding="utf-8") as fh:
            data = json.load(fh)
        rules = UD.normalize_rules(data["detectionRules"])
        for name, ent in self.rules.items():                                         # die eingebauten Sets stehen mit denselben Filtern in der Datei
            self.assertEqual(rules[name]["filters"], ent["filters"], name)

    def test_every_detect_has_rule_set(self):
        with open(os.path.join(ROOT, UD.RULES_FILE), encoding="utf-8") as fh:
            data = json.load(fh)
        names = {k.lower() for k in UD.normalize_rules(data["detectionRules"])}
        missing = ["%s -> %s" % (d["key"], d["detect"]) for d in data["devices"] if d.get("detect") and d["detect"].lower() not in names]
        self.assertEqual(missing, [], "devices.detect verweist auf ein Regel-Set, das in detectionRules fehlt")   # Pruefung der Datei

    def test_detect_links_devices_and_platforms(self):
        links = {"am328": [("Classic", "AM328"), ("Mini", "AM328")], "uno": [("Uno", "AM328")], "pico": [("PicoZero", "PICO")]}
        rules = UD.normalize_rules({"Uno": {"priority": 3, "filters": [{"vid": "2341", "pid": "0043"}, {"vid": "1A86"}]},
                                    "AM328": {"priority": 4, "filters": [{"vid": ["1A86", "0403"]}]},
                                    "PICO": {"priority": 1, "filters": [{"vid": "2E8A"}]}})
        uno = port(0x2341, 0x0043, "Arduino Uno (COM5)")
        ch340 = port(0x1A86, 0x7523, "USB-SERIAL CH340")
        ftdi = port(0x0403, 0x6001, "USB Serial Port")
        self.assertEqual(UD.rule_sets_for_port(ch340, rules=rules), ["Uno", "AM328"])
        self.assertEqual(UD.devices_for_port(ch340, rules=rules, links=links), ["Uno", "Classic", "Mini"])
        self.assertEqual(UD.devices_for_port(uno, rules=rules, links=links), ["Uno"])
        self.assertEqual(UD.devices_for_port(ftdi, rules=rules, links=links), ["Classic", "Mini"])
        self.assertEqual(UD.platforms_for_port(uno, rules=rules, links=links), ["AM328"])          # Plattform der verweisenden Geraete
        self.assertEqual(UD.platforms_for_port(port(0x2E8A, 0x000A), rules=rules, links=links), ["PICO"])   # 'Pico' verweist auf 'PICO'
        self.assertEqual(UD.platforms_for_port(port(0x2E8A, 0x000A), rules=rules, links={}), ["PICO"])      # ohne Verweis: Set-Name als Plattform

    def test_real_file_uno_rules(self):
        if not uno_set_exists():
            self.skipTest("kein Regel-Set fuer den Uno in der Datei")
        self.assertIn("Uno", UD.devices_for_port(port(0x2341, 0x0043, "Arduino Uno (COM5)", "USB VID:PID=2341:0043")))
        self.assertNotIn("Uno", UD.devices_for_port(port(0x0403, 0x6001, "USB Serial Port (COM4)", "USB VID:PID=0403:6001")))

    def test_weak_rules_only_without_other_match(self):
        orig_ftdi = port(None, None, "USB Serial Port (COM4)", "FTDIBUS\\VID_0403+PID_6001")
        self.assertEqual(UD.platforms_for_port(orig_ftdi, rules=self.rules), [])
        self.assertEqual(UD.platforms_for_port(orig_ftdi, weak=True, rules=self.rules), ["AM328"])
        pico_linux = port(0x2E8A, 0x000A, "ttyACM0", "USB VID:PID=2E8A:000A")      # 'tty' passt schwach zu AM328, der Pico gewinnt
        self.assertEqual(UD.platforms_for_port(pico_linux, weak=True, rules=self.rules), ["PICO"])

    def test_several_platforms_sorted_by_priority(self):
        rules = UD.normalize_rules({"AM328": {"priority": 3, "filters": [{"vid": "1A86"}]},
                                    "ESP32": {"priority": 2, "filters": [{"vid": "10C4"}, {"vid": "1A86"}]}})   # ESP32-Platine mit CH340
        self.assertEqual(UD.platforms_for_port(SAMPLES[0], rules=rules), ["ESP32", "AM328"])

    def test_filter_fields_are_combined_with_and(self):
        rules = UD.normalize_rules({"PICO": {"filters": [{"vid": "239A", "pid": "813D"}]}})
        self.assertEqual(UD.platforms_for_port(port(0x239A, 0x813D), rules=rules), ["PICO"])
        self.assertEqual(UD.platforms_for_port(port(0x239A, 0x0001), rules=rules), [])   # anderes Adafruit-Geraet

    def test_text_matches_manufacturer_and_product_case_insensitive(self):
        self.assertEqual(UD.platform_for_port(port(None, None, "Serial", manufacturer="wch.cn", product="ch340"), rules=self.rules), "AM328")

    def test_invalid_filters_never_match(self):
        rules = UD.normalize_rules({"X": {"filters": [{}, {"weak": True}, {"vid": "zz"}, {"vid": "1A86", "serial": "1"}]}, "_Hinweis": "Text"})
        self.assertNotIn("_Hinweis", rules)
        self.assertEqual(UD.platforms_for_port(SAMPLES[0], weak=True, rules=rules), [])

    def test_hex_values(self):
        self.assertEqual(UD._hex("0x2E8A"), 0x2E8A)
        self.assertEqual(UD._hex(11914), 11914)
        self.assertIsNone(UD._hex("xyz"))
        self.assertIsNone(UD._hex(True))


def vba_type(caption, path):
    """Erkennung des Excel-Programms (EnumComPorts, Ver_3.5.0/Source/M07_COM_Port.bas Zeilen 363-388): WMI Caption und PnP-Pfad, nur Windows"""
    is_nano = (("CH340" in caption or "Arduino" in caption or "Serielles USB-Gerät" in caption or "USB Serial Port" in caption)
               and "USB\\VID_2E8A&PID_000A\\" not in path and "USB\\VID_239A&PID_813D\\" not in path)
    is_esp = "Silicon Labs CP210x" in caption
    is_pico = "USB\\VID_2E8A&PID_000A\\" in path or "USB\\VID_239A&PID_813D" in path
    return "Nano" if is_nano else "ESP32" if is_esp else "Pico" if is_pico else ""


def win(caption, vid, pid):
    """(Caption, PnP-Pfad, Anschluss wie pyserial unter Windows)"""
    path = "USB\\VID_%04X&PID_%04X\\123" % (vid, pid) if vid is not None else "BTHENUM\\X"
    hwid = "USB VID:PID=%04X:%04X SER=123" % (vid, pid) if vid is not None else ""
    return caption, path, port(vid, pid, caption, hwid)


class ExcelComparisonTests(unittest.TestCase):
    """Gleiches Ergebnis wie das Excel-Programm (mit schwachen Regeln, wie in der Liste der Anschluesse einer Lichtmaschine); bekannte, gewollte Abweichungen einzeln"""
    SAME = [win("USB-SERIAL CH340 (COM3)", 0x1A86, 0x7523), win("USB Serial Port (COM4)", 0x0403, 0x6001),
            win("Arduino Uno (COM5)", 0x2341, 0x0043), win("Serielles USB-Gerät (COM5)", 0x2341, 0x0043),
            win("Serielles USB-Gerät (COM5)", 0x2A03, 0x0043), win("Silicon Labs CP210x USB to UART Bridge (COM7)", 0x10C4, 0xEA60),
            win("USB-SERIAL CH340 (COM7)", 0x1A86, 0x7523),                     # ESP32 mit CH340: in beiden 'Nano' (an USB nicht unterscheidbar)
            win("Serielles USB-Gerät (COM8)", 0x2E8A, 0x000A), win("USB Serial Device (COM8)", 0x2E8A, 0x000A),
            win("Serielles USB-Gerät (COM8)", 0x239A, 0x813D), win("USB Serial Port (COM13)", 0x0403, 0x6015),
            win("Serielles USB-Gerät (COM7)", 0x303A, 0x1001),                  # ESP32-S3 nativ: in beiden schwach 'Nano'
            win("Serielles USB-Gerät (COM12)", 0x1234, 0x0001),                 # unbekanntes Geraet: in beiden schwach 'Nano'
            win("Standardmäßige Seriell-über-Bluetooth-Verbindung (COM14)", None, None)]

    def test_same_as_excel(self):
        for cap, path, p in self.SAME:
            self.assertEqual(UD.legacy_type(UD.platform_for_port(p, weak=True)), vba_type(cap, path), cap)

    def test_known_differences(self):
        cap, path, p = win("Serielles USB-Gerät (COM8)", 0x2E8A, 0x0009)          # Pico mit anderer PID (zum Beispiel Pico 2)
        self.assertEqual((vba_type(cap, path), UD.platform_for_port(p, weak=True)), ("Nano", "PICO"))
        cap, path, p = win("USB Serial Device (COM5)", 0x2341, 0x0043)            # Uno ohne Treiber, englisches Windows
        self.assertEqual((vba_type(cap, path), UD.platform_for_port(p, weak=True)), ("", "AM328"))
        cap, path, p = win("USB-Enhanced-SERIAL CH9102 (COM3)", 0x1A86, 0x55D4)   # VID 1A86 ohne CH340 im Namen
        self.assertEqual((vba_type(cap, path), UD.platform_for_port(p, weak=True)), ("", "AM328"))

    def test_weak_cdc_name_only_without_other_match(self):
        unknown = port(0x1234, 0x0001, "Serielles USB-Gerät (COM12)", "USB VID:PID=1234:0001")
        self.assertEqual(UD.platforms_for_port(unknown), [])                      # Classify_Port: unbekannt
        self.assertEqual(UD.platforms_for_port(unknown, weak=True), ["AM328"])    # Liste der Anschluesse eines Classic
        pico = port(0x2E8A, 0x000A, "Serielles USB-Gerät (COM8)", "USB VID:PID=2E8A:000A")
        self.assertEqual(UD.platforms_for_port(pico, weak=True), ["PICO"])


class LoadTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="mll_usb_")
        os.makedirs(os.path.join(self.dir, "csv"))
        self.path = os.path.join(self.dir, UD.RULES_FILE)
        UD._cache.update(path=None, mtime=None, rules=None)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)
        UD._cache.update(path=None, mtime=None, rules=None)

    def write(self, text):
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.utime(self.path, None)

    def test_broken_file_uses_builtin_rules(self):
        self.write('{"devices": [ {"key": "A"} {"key": "B"} ]}')                   # fehlendes Komma
        self.assertEqual(UD.load_rules(self.dir), UD.normalize_rules(UD.DEFAULT_RULES))

    def test_missing_rules_use_builtin_rules(self):
        self.write('{"devices": []}')
        self.assertEqual(UD.load_rules(self.dir), UD.normalize_rules(UD.DEFAULT_RULES))

    def test_own_rules_and_reload_after_change(self):
        self.write(json.dumps({"detectionRules": {"ESP32": {"priority": 1, "filters": [{"vid": "303A"}]}}}))
        self.assertEqual(UD.platforms_for_port(SAMPLES[-1], base_dir=self.dir), ["ESP32"])
        self.assertEqual(UD.platforms_for_port(SAMPLES[0], base_dir=self.dir), [])     # nur die eigenen Regeln
        st = os.stat(self.path)
        self.write(json.dumps({"detectionRules": {"AM328": {"filters": [{"vid": "1A86"}]}}}))
        os.utime(self.path, (st.st_atime, st.st_mtime + 5))                           # neuere Datei
        self.assertEqual(UD.platforms_for_port(SAMPLES[0], base_dir=self.dir), ["AM328"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
