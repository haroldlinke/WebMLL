# Datei-Version: 1.00 (2026-11-28) - test_usb_list.py
# ----------------------------------------------------------------------------------------------
# Name:           test_usb_list.py
# Path:           test_usb_list.py
# Version:        1.00
# Last Update:    2026-11-28
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-28  Neu: Liste der USB Geraete (_web/web_usb_list.py): Zeilen, Vorgabe nur serielle USB-Anschluesse, 'Alle Geräte' ohne Doppelte, Linux-Einlesen,
#                     Text fuer die Zwischenablage, Uebersetzungen
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_usb_list.py

Prueft die reinen Funktionen von _web/web_usb_list.py mit Ersatzobjekten fuer die Anschluesse und einem Ersatz-Ordner fuer /sys/bus/usb/devices. Die Regeln kommen aus der
echten csv/Lichtmaschinen_prop.json. Nicht geprueft: das Fenster (NiceGUI), die Abfrage unter Windows (CIM) und macOS (system_profiler) an echten Geraeten."""
import os
import shutil
import sys
import tempfile
import unittest
from types import SimpleNamespace

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from _web import web_usb_list as U  # noqa: E402


def port(device, vid, pid, desc, serial="", manufacturer="", product=""):
    hwid = ("USB VID:PID=%04X:%04X SER=%s" % (vid, pid, serial)) if vid is not None else "BTHENUM\\X"
    return SimpleNamespace(device=device, vid=vid, pid=pid, description=desc, hwid=hwid, serial_number=serial, manufacturer=manufacturer, product=product)


PORTS = [port("COM16", 0x1A86, 0x7523, "USB-SERIAL CH340 (COM16)"),
         port("COM3", 0x10C4, 0xEA60, "Silicon Labs CP210x USB to UART Bridge (COM3)", "0001"),
         port("COM7", 0x2E8A, 0x000A, "Serielles USB-Gerät (COM7)", "E661"),
         port("COM11", None, None, "Standardmäßige Seriell-über-Bluetooth-Verbindung (COM11)")]


class RowTests(unittest.TestCase):
    def test_default_only_serial_usb_sorted(self):
        rows = U.collect_rows(PORTS)
        self.assertEqual([r["device"] for r in rows], ["COM3", "COM7", "COM16"])    # kein Bluetooth, nach Nummer sortiert
        r = rows[2]
        self.assertEqual((r["vid"], r["pid"]), ("1A86", "7523"))
        self.assertIn("AM328", r["rule_sets"])
        self.assertIn("Classic", r["devices"])
        self.assertEqual(rows[1]["rule_sets"], "PICO")

    def test_all_devices_without_duplicates(self):
        usb = [U._usb(0x2E8A, 0x000A, "Pico", serial_number="E661"),                # derselbe Pico wie COM7: nicht doppelt
               U._usb(0x046D, 0xC52B, "Logitech USB Input Device"),
               U._usb(0x045B, 0x0209, "Generischer USB-Hub")]
        rows = U.collect_rows(PORTS, all_devices=True, usb_devices_=usb)
        self.assertEqual([r["device"] for r in rows[:4]], ["COM3", "COM7", "COM11", "COM16"])   # mit Bluetooth
        self.assertEqual([(r["vid"], r["pid"]) for r in rows[4:]], [("045B", "0209"), ("046D", "C52B")])
        self.assertEqual(rows[4]["device"], "")

    def test_weak_match_is_marked(self):
        rows = U.collect_rows([port("COM9", 0x1234, 0x0001, "Serielles USB-Gerät (COM9)")])
        self.assertTrue(rows[0]["rule_sets"].endswith(U.tr("(schwach)")))

    def test_text(self):
        text = U.rows_as_text(U.collect_rows(PORTS))
        lines = text.split("\n")
        self.assertEqual(len(lines), 4)
        self.assertEqual(len(lines[0].split("\t")), len(U.FIELDS))
        self.assertIn("1A86\t7523", lines[3])


class LinuxTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="mll_usb_")
        for name, files in {"1-1": {"idVendor": "2341\n", "idProduct": "0043\n", "manufacturer": "Arduino (www.arduino.cc)\n", "product": "Arduino Uno\n", "serial": "95730\n"},
                            "1-1_1.0": {"bInterfaceClass": "02\n"},                       # Schnittstelle (unter Linux 1-1:1.0; der Doppelpunkt geht unter Windows nicht)
                            "usb1": {"idVendor": "1d6b\n", "idProduct": "0002\n", "product": "xHCI Host Controller\n"}}.items():
            os.makedirs(os.path.join(self.root, name))
            for f, v in files.items():
                with open(os.path.join(self.root, name, f), "w", encoding="utf-8") as fh:
                    fh.write(v)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_read_sysfs(self):
        devs = U._linux_usb(self.root)
        self.assertEqual([(d.vid, d.pid) for d in devs], [(0x2341, 0x0043), (0x1D6B, 0x0002)])   # Schnittstelle ohne idVendor fehlt
        uno = devs[0]
        self.assertEqual((uno.manufacturer, uno.product, uno.serial_number), ("Arduino (www.arduino.cc)", "Arduino Uno", "95730"))
        self.assertIn("VID:PID=2341:0043", uno.hwid)
        row = U._row(uno)
        self.assertIn("AM328", row["rule_sets"])
        from test_usb_detect import uno_set_exists
        if uno_set_exists():
            self.assertIn("Uno", row["devices"])                                    # Regel-Set des Uno passt (2341:0043)


class TranslationTests(unittest.TestCase):
    TEXTS = ["Liste der USB Geräte …", "Liste der USB Geräte", "Keine seriellen USB-Geräte gefunden.", "Neu einlesen", "Als Text kopieren", "Alle Geräte",
             "In die Zwischenablage kopiert", "Hersteller", "Produkt", "Seriennummer", "Hardware-Kennung", "Regel-Sets", "Lichtmaschinen", "(schwach)",
             "Auch USB-Geräte ohne seriellen Anschluss anzeigen (Spalte Anschluss leer)",
             "Serielle USB-Anschlüsse mit den Daten, nach denen die Regeln detectionRules in csv/Lichtmaschinen_prop.json filtern (vid, pid, text = Beschreibung, Hersteller oder Produkt, hwid = Hardware-Kennung), und die passenden Regel-Sets und Lichtmaschinen."]

    def test_all_languages(self):
        from _web import web_i18n as I
        for n in range(1, 7):
            with I.use_language(n):
                for t in self.TEXTS:
                    if t == "Produkt" and n == 6:                                    # Daenisch: gleiches Wort
                        continue
                    self.assertNotEqual(I.tr(t), t, "Sprache %d: %s" % (n, t))
        with I.use_language(0):
            for t in self.TEXTS:
                self.assertEqual(I.tr(t), t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
