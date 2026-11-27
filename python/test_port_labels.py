# Datei-Version: 1.00 (2026-11-26) - test_port_labels.py
# ----------------------------------------------------------------------------------------------
# Name:           test_port_labels.py
# Path:           test_port_labels.py
# Version:        1.00
# Last Update:    2026-11-26
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-26  Neu: Auswahl des Anschlusses im Serial Monitor zeigt bekannte Typen und den Untertyp nach der USB-Kennung (web_serial 1.21)
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_port_labels.py   (ohne Oberflaeche und ohne angeschlossene Geraete)"""
import os
import sys
import unittest
from types import SimpleNamespace

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from _web import web_serial as WS  # noqa: E402


def port(device, vid, pid, desc="", hwid=None):
    return SimpleNamespace(device=device, vid=vid, pid=pid, description=desc,
                           hwid=hwid if hwid is not None else ("USB VID:PID=%04X:%04X" % (vid, pid) if vid is not None else "n/a"))


class PortLabelTests(unittest.TestCase):
    def test_known_types_with_subtype_from_usb_id(self):
        cases = [
            (port("COM3", 0x1A86, 0x7523, "USB-SERIAL CH340 (COM3)"), "COM3 – Nano/Uno (CH340, 1A86:7523)"),
            (port("COM4", 0x10C4, 0xEA60, "Silicon Labs CP210x USB to UART Bridge"), "COM4 – ESP32 (CP2102, 10C4:EA60)"),
            (port("COM5", 0x2E8A, 0x000A, "USB Serial Device"), "COM5 – Pico (Seriell, 2E8A:000A)"),
            (port("COM6", 0x0403, 0x6001, "USB Serial Port"), "COM6 – Nano/Uno (FT232R, 0403:6001)"),
            (port("/dev/ttyACM0", 0x2341, 0x0043, "Arduino Uno"), "/dev/ttyACM0 – Nano/Uno (Arduino, 2341:0043)"),
        ]
        for p, expected in cases:
            self.assertEqual(WS.describe_port(p), expected)

    def test_unknown_subtype_of_known_vendor_shows_only_the_usb_id(self):
        self.assertEqual(WS.describe_port(port("COM7", 0x1A86, 0x1234, "")), "COM7 – Nano/Uno (CH34x, 1A86:1234)")     # Hersteller bekannt
        self.assertEqual(WS.usb_subtype(0x10C4, 0x9999), "CP210x")
        self.assertEqual(WS.usb_subtype(0x1234, 0x0001), "")
        self.assertEqual(WS.usb_subtype(None, None), "")

    def test_unknown_type_keeps_the_system_description(self):
        self.assertEqual(WS.describe_port(port("COM8", 0x9999, 0x0001, "Mystery Device (COM8)")), "COM8 – Mystery Device (COM8) (9999:0001)")
        self.assertEqual(WS.describe_port(port("/dev/ttyS0", None, None, "n/a")), "/dev/ttyS0")                           # kein USB, keine Beschreibung

    def test_other_mobaledlib_device_shows_its_type(self):
        import types
        fake = types.ModuleType("proggen.M07_COM_Port_New")
        fake.OTHER_TYPES = {"COM9": "PICOSERVO"}
        saved = sys.modules.get("proggen.M07_COM_Port_New")
        sys.modules["proggen.M07_COM_Port_New"] = fake
        try:
            self.assertEqual(WS.describe_port(port("COM9", 0x2E8A, 0x000A, "USB Serial Device")), "COM9 – PICOSERVO (Seriell, 2E8A:000A)")
        finally:
            if saved is None:
                sys.modules.pop("proggen.M07_COM_Port_New", None)
            else:
                sys.modules["proggen.M07_COM_Port_New"] = saved


if __name__ == "__main__":
    unittest.main(verbosity=2)
