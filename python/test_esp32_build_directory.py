# Datei-Version: 1.05 (2026-11-26) - test_esp32_build_directory.py
# Name: test_esp32_build_directory.py
# Path: test_esp32_build_directory.py
# Version: 1.05
# Last Update: 2026-11-26
# Author: Harold Linke
# Licence: LGPL V2.1
# History of Change:
#   1.05 2026-11-26 M08-Abgleich auf Original-Release 5.54; Programm-VERSION unveraendert 5.54.
#   1.04 2026-11-26 M08-Upload auf 5.41/MobaLedLib 3.6.0 aktualisiert; neue Originalkorrekturen erhalten.
#   1.03 2026-11-24 M08-Upload auf Original 5.12 aktualisiert, Pico-Identifikation und Firmware-Signatur erhalten.
#   1.02 2026-11-23 Gemeinsame Pfadermittlung und M08-Buildadapter pruefen.
#   1.01 2026-11-23 Abweichenden PlatformIO-Paketordner und USB-Aufruf pruefen.
#   1.00 2026-11-23 Externe PlatformIO-Build-Pfade nach erfolgreichem ESP32-Build pruefen.
import json  # v1.00
import tempfile  # v1.00
import unittest  # v1.00
import no_tk  # headless Teststart auch ohne installiertes tkinter  # v1.02  # v1.03  # v1.04  # v1.05
no_tk.install(force=True)  # v1.02  # v1.03  # v1.04  # v1.05
from pathlib import Path  # v1.00
from types import SimpleNamespace  # v1.00
from unittest.mock import patch  # v1.00
from headless import headless_esp32_ota as ota  # v1.00


class BuildDirectoryTests(unittest.TestCase):  # v1.00
    def config(self, options):  # v1.00
        return SimpleNamespace(returncode=0, stdout=json.dumps([["platformio", list(options.items())]]))  # v1.00

    def test_explicit_packages_directory(self):  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
        with tempfile.TemporaryDirectory() as folder, patch.object(ota, "platformio_ota_project", return_value=Path(folder)), patch("headless.headless_upload.platformio_project_options", return_value={"packages_dir": folder}):  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
            (Path(folder) / "platformio.ini").write_text("[platformio]", encoding="utf-8")  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertEqual(ota.platformio_packages("pio"), Path(folder))  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05

    def test_runtime_core_directory_instead_of_users_home(self):  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
        with tempfile.TemporaryDirectory() as folder, patch.object(ota, "platformio_ota_project", return_value=Path(folder)), patch("headless.headless_upload.platformio_project_options", return_value={}), patch.object(ota.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout=json.dumps({"core_dir": {"value": folder}}))):  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertEqual(ota.platformio_packages("pio"), Path(folder) / "packages")  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05

    def test_usb_uses_esptool_from_selected_packages(self):  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
        with tempfile.TemporaryDirectory() as folder:  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
            (Path(folder) / "platformio.ini").write_text("[platformio]", encoding="utf-8")  # v1.02  # v1.03  # v1.04  # v1.05
            packages = Path(folder) / "Werkzeuge ü"  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
            script = packages / "tool-esptoolpy/esptool.py"  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
            script.parent.mkdir(parents=True)  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
            script.touch()  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
            with patch.object(ota, "platformio_ota_project", return_value=Path(folder)), patch("headless.headless_upload.platformio_project_options", return_value={"packages_dir": str(packages)}), patch.object(ota.subprocess, "run", return_value=SimpleNamespace(returncode=1, stdout="test", stderr="")) as run:  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
                with self.assertRaisesRegex(ValueError, "Partitionstabelle"):  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
                    ota.flash_usb("COM7", b"image", b"partitions", lambda line: None, pio="pio")  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
                self.assertIn(str(script), run.call_args.args[0])  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05
                self.assertIn("read_flash", run.call_args.args[0])  # v1.01  # v1.02  # v1.03  # v1.04  # v1.05

    def test_default_relative_workspace_and_absolute_build(self):  # v1.00
        with tempfile.TemporaryDirectory() as folder, patch.dict(ota.os.environ, {"PLATFORMIO_BUILD_DIR": "", "PLATFORMIO_WORKSPACE_DIR": ""}):  # v1.00
            project = Path(folder).resolve()  # v1.00
            for options, expected in [({}, project / ".pio/build/esp32"), ({"workspace_dir": "andere Arbeitsfläche"}, project / "andere Arbeitsfläche/build/esp32"), ({"build_dir": str(project / "extern ü")}, project / "extern ü/esp32")]:  # v1.00
                with self.subTest(options=options), patch.object(ota.subprocess, "run", return_value=self.config(options)):  # v1.00
                    self.assertEqual(ota.platformio_build_directory("pio", project), expected)  # v1.00

    def test_invalid_configuration_does_not_expose_secrets(self):  # v1.00
        for result in [SimpleNamespace(returncode=1, stdout="secret-password"), SimpleNamespace(returncode=0, stdout="secret-password")]:  # v1.00
            with patch.object(ota.subprocess, "run", return_value=result):  # v1.00
                with self.assertRaises(ValueError) as error:  # v1.00
                    ota.platformio_build_directory("pio", ".")  # v1.00
                self.assertNotIn("secret-password", str(error.exception))  # v1.00

    def test_successful_build_reads_external_files_not_stale_default(self):  # v1.00
        with tempfile.TemporaryDirectory() as folder:  # v1.00
            root = Path(folder)  # v1.00
            sketch = root / "source/LEDs_AutoProg"  # v1.00
            sketch.mkdir(parents=True)  # v1.00
            (sketch.parent / "libraries").mkdir()  # v1.00
            project = root / "project"  # v1.00
            stale = project / ".pio/build/esp32"  # v1.00
            stale.mkdir(parents=True)  # v1.00
            (stale / "firmware.bin").write_bytes(b"old")  # v1.00
            build = root / "external build ü/esp32"  # v1.00
            build.mkdir(parents=True)  # v1.00
            (build / "firmware.bin").write_bytes(b"new firmware")  # v1.00
            (build / "partitions.bin").write_bytes(b"new partitions")  # v1.00
            def config(path):  # v1.00
                (Path(path).parent / "platformio.ini").write_text("[platformio]\n", encoding="utf-8")  # v1.00
                return True  # v1.00
            # with patch.object(ota, "platformio_ota_project", return_value=project), patch.object(ota, "prepare_ota_sketch", return_value="secret"), patch.object(ota, "run_streaming", return_value=0), patch.object(ota.subprocess, "run", return_value=self.config({"build_dir": str(build.parent)})):  # v1.00  # v1.03 (entfallen)
            with patch.object(ota, "platformio_ota_project", return_value=project), patch.object(ota, "prepare_ota_sketch", return_value="secret"), patch("proggen.M08_ARDUINO.Run_PlatformIO", return_value=0), patch.object(ota.subprocess, "run", return_value=self.config({"build_dir": str(build.parent)})):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                self.assertEqual(ota.build_platformio_project(sketch, "pio", "", lambda line: None, config), (b"new firmware", b"new partitions"))  # v1.00
                (build / "firmware.bin").unlink()  # v1.00
                with self.assertRaisesRegex(ValueError, "ESP32-Dateien"):  # v1.00
                    ota.build_platformio_project(sketch, "pio", "", lambda line: None, config)  # v1.00


if __name__ == "__main__":  # v1.00
    unittest.main()  # v1.00
