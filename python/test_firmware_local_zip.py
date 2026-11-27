# Datei-Version: 1.00 (2026-11-26) - test_firmware_local_zip.py
# ----------------------------------------------------------------------------------------------
# Name:           test_firmware_local_zip.py
# Path:           test_firmware_local_zip.py
# Version:        1.00
# Last Update:    2026-11-26
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-26  Neu: Firmware aus einer lokalen ZIP-Datei installieren (headless_firmware_dl 1.01, web_form_firmware_download 1.03)
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_firmware_local_zip.py

Prueft ohne Browser: die ZIP-Pruefung (kein ZIP, keine *.uf2), das sichere Entpacken in den Firmware-Ordner und den Ablauf des Dialogs (Rueckfrage beim Ueberschreiben,
Meldungen, Rueckgabe zum Vorwaehlen). Die Oberflaeche (Auswahlfeld) ist hier nicht Teil des Tests."""
import asyncio
import io
import json
import os
import sys
import tempfile
import unittest
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import headless.headless_firmware_dl as HFD  # noqa: E402
from _web import web_form_firmware_download as WFD  # noqa: E402


def make_zip(files):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, content in files.items():
            z.writestr(name, content)
    return buf.getvalue()


FW = make_zip({"PicoServo-Tiny-V1.1.uf2": b"UF2DATA", "PicoServo-Tiny-V1.1.desc": b"desc"})


class HeadlessTests(unittest.TestCase):
    def test_check_rejects_non_zip_and_non_firmware(self):
        with self.assertRaises(HFD.FirmwareError) as c:
            HFD.check_local_zip(b"das ist kein zip")
        self.assertEqual(c.exception.kind, "zip")
        with self.assertRaises(HFD.FirmwareError) as c:
            HFD.check_local_zip(make_zip({"readme.txt": b"x"}))
        self.assertEqual(c.exception.kind, "nofirmware")
        self.assertEqual(HFD.check_local_zip(FW), ["PicoServo-Tiny-V1.1.uf2", "PicoServo-Tiny-V1.1.desc"])

    def test_install_unpacks_into_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            result = HFD.install_local_zip(FW, folder)
            self.assertEqual(sorted(os.listdir(folder)), ["PicoServo-Tiny-V1.1.desc", "PicoServo-Tiny-V1.1.uf2"])   # keine ZIP-Datei bleibt liegen
            self.assertEqual(result["firmware"], ["PicoServo-Tiny-V1.1.uf2"])

    def test_install_refuses_path_outside_folder(self):
        evil = make_zip({"../boese.uf2": b"x"})
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(HFD.FirmwareError) as c:
                HFD.install_local_zip(evil, os.path.join(folder, "fw") if os.makedirs(os.path.join(folder, "fw")) is None else folder)
            self.assertEqual(c.exception.kind, "unzip")
            self.assertFalse(os.path.exists(os.path.join(folder, "boese.uf2")))

    def test_missing_folder(self):
        with self.assertRaises(HFD.FirmwareError) as c:
            HFD.install_local_zip(FW, os.path.join(tempfile.gettempdir(), "gibt_es_nicht_mll_fw"))
        self.assertEqual(c.exception.kind, "nodir")

    def test_entry_from_file(self):
        self.assertEqual(HFD.entry_from_file("PicoServo-Tiny-V1.1.uf2")["name"], "PicoServo-Tiny")
        self.assertEqual(HFD.entry_from_file("PicoServo-Tiny-V1.1.uf2")["version"], "1.1")
        self.assertEqual(HFD.entry_from_file("Ordner/Blink-V1.0.uf2")["name"], "Blink")
        self.assertEqual(HFD.entry_from_file("seltsam.uf2")["name"], "")
        self.assertTrue(HFD.entry_from_file("")["local"])                     # nie leer: der Aufrufer wertet 'leer' als Abbruch


class ScanTests(unittest.TestCase):
    def test_groups_are_sorted_by_platform(self):
        import headless.headless_pico as HP
        with tempfile.TemporaryDirectory() as folder:
            def add(name, version, platform):
                open(os.path.join(folder, "%s-V%s.uf2" % (name, version)), "wb").write(b"x")
                desc = {"name": name, "version": version, "DE": {"short": name, "detail": ""}}
                if platform:
                    desc["platform"] = platform
                with open(os.path.join(folder, "%s-V%s.desc" % (name, version)), "w", encoding="utf-8") as fh:
                    json.dump(desc, fh)
            add("Zeta", "1.0", "AAA")
            add("Alpha", "1.0", "ZZZ")
            add("Beta", "1.0", "AAA")
            add("Beta", "1.1", "AAA")
            add("Ohne", "1.0", "")
            groups = HP.scan_firmware(folder, "DE")
            self.assertEqual([(g["platform"], g["base"]) for g in groups], [("AAA", "Beta"), ("AAA", "Zeta"), ("ZZZ", "Alpha"), ("", "Ohne")])
            self.assertEqual([v["version"] for v in groups[0]["versions"]], ["1.1", "1.0"])
            self.assertEqual(groups[0]["versions"][0]["platform"], "AAA")


class PlatformTitleTests(unittest.TestCase):
    def test_title_uses_name_from_json_or_falls_back_to_platform(self):
        from _web import web_form_firmware as WFF
        with open(os.path.join(ROOT, "csv", "Lichtmaschinen_prop.json"), encoding="utf-8") as fh:
            data = json.load(fh)
        names = {}
        for entry in data["platforms"] + data["devices"]:                           # erst platforms, dann devices
            names.setdefault(entry["platform"], entry["name"])
        self.assertIn("MLL512V1", names)
        for platform, name in names.items():
            self.assertEqual(WFF.platform_title(platform), name, platform)          # Name aus Lichtmaschinen_prop.json
            self.assertEqual(WFF.platform_title(platform.lower()), name, platform)  # Gross-/Kleinschreibung egal
        self.assertEqual(WFF.platform_title("UNBEKANNT_V9"), "UNBEKANNT_V9")        # nichts gefunden: wie bisher die Plattform
        self.assertEqual(WFF.platform_title(""), "Ohne Plattform")


class FlowTests(unittest.TestCase):
    def flow(self, folder, answer=6):
        self.messages = []

        async def msgbox(text, kind, title):
            self.messages.append((text, kind))
            return answer

        async def run_blocking(func, *args):
            return func(*args)
        return WFD.DownloadFlow(folder, WFD.translated_texts(lambda k: k), msgbox, run_blocking)

    def run_(self, coro):
        return asyncio.run(coro)

    def test_install_ok_returns_entry_for_preselection(self):
        with tempfile.TemporaryDirectory() as folder:
            entry = self.run_(self.flow(folder).install_local(FW, "fw.zip"))
            self.assertEqual((entry["name"], entry["version"]), ("PicoServo-Tiny", "1.1"))
            self.assertTrue(os.path.isfile(os.path.join(folder, "PicoServo-Tiny-V1.1.uf2")))
            self.assertEqual(len(self.messages), 1)                           # nur die Erfolgsmeldung

    def test_not_a_zip_and_no_firmware_give_message_and_nothing_installed(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertIsNone(self.run_(self.flow(folder).install_local(b"kein zip", "x.zip")))
            self.assertIn("kein ZIP", self.messages[0][0])
            self.assertIsNone(self.run_(self.flow(folder).install_local(make_zip({"a.txt": b"1"}), "x.zip")))
            self.assertIn("keine Firmware", self.messages[0][0])
            self.assertEqual(os.listdir(folder), [])

    def test_overwrite_is_asked_and_can_be_declined(self):
        with tempfile.TemporaryDirectory() as folder:
            target = os.path.join(folder, "PicoServo-Tiny-V1.1.uf2")
            with open(target, "wb") as fh:
                fh.write(b"ALT")
            self.assertIsNone(self.run_(self.flow(folder, answer=7).install_local(FW, "fw.zip")))      # Nein
            self.assertEqual(open(target, "rb").read(), b"ALT")
            self.assertIn("PicoServo-Tiny-V1.1.uf2", self.messages[0][0])
            entry = self.run_(self.flow(folder, answer=6).install_local(FW, "fw.zip"))                  # Ja
            self.assertEqual(entry["name"], "PicoServo-Tiny")
            self.assertEqual(open(target, "rb").read(), b"UF2DATA")


if __name__ == "__main__":
    unittest.main(verbosity=2)
