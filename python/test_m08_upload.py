# Datei-Version: 1.05 (2026-11-27) - test_m08_upload.py
# Name: test_m08_upload.py
# Path: test_m08_upload.py
# Version: 1.05
# Last Update: 2026-11-27
# Author: Harold Linke, moosbewohner
# Licence: LGPL V2.1
# History of Change:
#   1.05 2026-11-27 moosbewohner: M08-Beitrag auf Original 5.60; vorhandene EFFECT-Verbindung und Abbruchpfade erhalten.
#   1.04 2026-11-26 M08-Abgleich auf Original-Release 5.54; Programm-VERSION unveraendert 5.54.
#   1.03 2026-11-26 M08-Upload auf 5.41/MobaLedLib 3.6.0 aktualisiert; neue Originalkorrekturen erhalten.
#   1.02 2026-11-24 M08-Upload auf Original 5.12 aktualisiert, Pico-Identifikation und Firmware-Signatur erhalten.
#   1.01 2026-11-23 nobuild darf beim Protokollwechsel keine fertige Firmware bereinigen.
#   1.00 2026-11-23 Gemeinsame Befehle, Prozessausfuehrung, Nano/Pico/ESP32 und M08-Verdrahtung.
import no_tk  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
no_tk.install(force=True)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
import ast  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
import io  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
import os  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
import subprocess  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
import sys  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
import tempfile  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
import unittest  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
from pathlib import Path  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
from types import SimpleNamespace  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
from unittest.mock import MagicMock, patch  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
from headless import headless_upload as shared  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05


class CommandTests(unittest.TestCase):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
    def test_all_original_board_environments(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        for board in ("nano_old", "nano_new", "nano_full", "uno", "pico", "esp32"):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            for port in ("COM17", "/dev/ttyUSB0", "/dev/ttyACM0", "/dev/cu.usbmodem101", "/dev/serial/by-id/usb-device"):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                with self.subTest(board=board, port=port):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                    job = shared.PlatformIOJob("/tools with spaces/pio", "project ü", board, port=port)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                    self.assertEqual(job.argv[0], "/tools with spaces/pio")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                    self.assertEqual(job.argv[job.argv.index("-e")+1], board)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                    self.assertEqual(job.argv[-1], port)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                    self.assertNotIn("cd ", str(job))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05

    def test_compile_only_and_precompiled_nano(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        job = shared.PlatformIOJob("pio", ".", "pico", upload=False, port="COM1")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertNotIn("upload", job.argv)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertNotIn("--upload-port", job.argv)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        precompiled = shared.PlatformIOJob("pio", ".", "nano_old", port="COM1", nobuild=True)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertEqual(precompiled.argv.count("upload"), 1)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertIn("nobuild", precompiled.argv)  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertIn("--disable-auto-clean", precompiled.argv)  # v1.01  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05

    def test_wlan_password_never_in_command_or_argv(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        previous_protocol = os.environ.get("PLATFORMIO_UPLOAD_PROTOCOL")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        job = shared.PlatformIOJob("pio", ".", "esp32", port="mobaledlib.local", transport="wlan", password="secret-test")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertNotIn("secret-test", str(job))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertNotIn("secret-test", " ".join(job.argv))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertEqual(job.transport, "wlan")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertIn("--auth=secret-test", job.environment_vars["PLATFORMIO_UPLOAD_FLAGS"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertEqual(os.environ.get("PLATFORMIO_UPLOAD_PROTOCOL"), previous_protocol)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        for board in ("nano_old", "nano_full", "pico"):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            with self.assertRaises(ValueError):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                shared.PlatformIOJob("pio", ".", board, transport="wlan")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05

    def test_protocol_overlay_is_private_temporary_and_does_not_change_project(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        with tempfile.TemporaryDirectory() as folder:  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            ini = Path(folder) / "platformio.ini"  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            original = "[env:esp32]\nplatform = espressif32\n"  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            ini.write_text(original, encoding="utf-8")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            job = shared.PlatformIOJob("pio", folder, "esp32", port="host.lan", transport="wlan", password="secret-test")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            with shared.upload_configuration(job):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                path = Path(job.argv[-1])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                self.assertTrue(path.is_file())  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                self.assertIn("upload_protocol = espota", path.read_text(encoding="utf-8"))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                self.assertNotIn("secret-test", path.read_text(encoding="utf-8"))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertFalse(path.exists())  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertEqual(ini.read_text(encoding="utf-8"), original)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertNotIn("--project-conf", job.argv)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05

    def test_usb_cannot_inherit_ota_protocol(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        with patch.dict(os.environ, {"PLATFORMIO_UPLOAD_PROTOCOL":"espota", "PLATFORMIO_UPLOAD_FLAGS":"--auth=old"}):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            job = shared.PlatformIOJob("pio", ".", "esp32", port="COM1")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertNotIn("PLATFORMIO_UPLOAD_PROTOCOL", job.environment_vars)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertEqual(job.environment_vars["PLATFORMIO_UPLOAD_FLAGS"], "")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05


class ExecutionTests(unittest.TestCase):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
    def test_real_process_arguments_and_masking(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        lines = []  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        value = "path with spaces ü & $ ;"  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        rc = shared.run_streaming([sys.executable, "-c", "import sys; print(sys.argv[1]); print('secret-test')", value], lines.append, 10, ("secret-test",))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertEqual(rc, 0)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertEqual(lines, [value, "********"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05

    def test_structured_job_uses_argv_and_no_shell(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        job = shared.PlatformIOJob("pio", ".", "esp32", port="host.local", transport="wlan", password="secret-test")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        proc = MagicMock()  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        proc.stdout = io.StringIO("--auth=secret-test\n")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        proc.wait.return_value = 0  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        proc.returncode = 0  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        callback, lines = MagicMock(), []  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        with patch.object(shared.subprocess, "Popen", return_value=proc) as spawn:  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertEqual(shared.run_streaming(job, lines.append, on_process=callback), 0)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertEqual(spawn.call_args.args[0][:len(job.argv)], list(job.argv))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertFalse(spawn.call_args.kwargs["shell"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertEqual(spawn.call_args.kwargs["cwd"], job.project)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        callback.assert_called_once_with(proc)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertEqual(lines, ["--auth=********"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        if os.name == "nt":  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertTrue(spawn.call_args.kwargs["creationflags"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        else:  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertTrue(spawn.call_args.kwargs["start_new_session"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05

    def test_real_timeout_terminates_child_process(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        with self.assertRaises(shared.UploadTimeout):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            shared.run_streaming([sys.executable, "-c", "import time; time.sleep(20)"], lambda line: None, 0.2)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertIsNone(shared._current["proc"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05

    def test_cancellation_reaches_current_process(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        proc = MagicMock()  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        proc.poll.return_value = None  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        with patch.dict(shared._current, {"proc":proc, "cancelled":False}), patch.object(shared, "_kill_tree") as kill:  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertTrue(shared.cancel_running())  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertTrue(shared._current["cancelled"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            kill.assert_called_once_with(proc)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05


class TranslationTests(unittest.TestCase):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
    def test_new_messages_in_all_seven_languages(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        from _web.web_i18n import use_language, tr  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        keys = ["Gerät und Verbindung", "WLAN-Upload wird für dieses Board nicht unterstützt.", "Das Build-Ergebnis wurde zwischenzeitlich geändert. Bitte erneut übertragen.", "Die PlatformIO-Werkzeugpfade konnten nicht ermittelt werden.", "Es wird nur kompiliert, nicht hochgeladen."]  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        for key in keys:  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            for language in range(7):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                with self.subTest(key=key, language=language), use_language(language):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                    if language == 0:  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                        self.assertEqual(tr(key), key)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                    else:  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                        self.assertTrue(tr(key))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
                        self.assertNotEqual(tr(key), key)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05


class Upstream512Tests(unittest.TestCase):  # v1.02  # v1.03  # v1.04  # v1.05
    def test_pico_identity_reaches_port_rediscovery(self):  # v1.02  # v1.03  # v1.04  # v1.05
        from proggen import M42_Dyn_Config as dyn  # v1.02  # v1.03  # v1.04  # v1.05
        original = dict(dyn._state)  # v1.02  # v1.03  # v1.04  # v1.05
        try:  # v1.02  # v1.03  # v1.04  # v1.05
            dyn._state.update(blob=b"config", pico=True)  # v1.02  # v1.03  # v1.04  # v1.05
            with patch.object(dyn, "_out"), patch.object(dyn.DC, "wait_for_port", return_value=None) as wait:  # v1.02  # v1.03  # v1.04  # v1.05
                self.assertFalse(dyn.After_Full_Flash("COM7", expected_serial="pico-123", expected_location="usb-2"))  # v1.02  # v1.03  # v1.04  # v1.05
                wait.assert_called_once_with("COM7", True, 10.0, "pico-123", "usb-2")  # v1.02  # v1.03  # v1.04  # v1.05
        finally:  # v1.02  # v1.03  # v1.04  # v1.05
            dyn._state.clear()  # v1.02  # v1.03  # v1.04  # v1.05
            dyn._state.update(original)  # v1.02  # v1.03  # v1.04  # v1.05

    def test_current_program_version_is_available_for_firmware_signature(self):  # v1.02  # v1.03  # v1.04  # v1.05
        from proggen import M42_Dyn_Config as dyn  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertEqual(dyn._program_version(), "5.60 (2026-11-27)")  # v1.02  # v1.03  # v1.04  # v1.05

    def test_minimal_firmware_keeps_static_network_settings_and_restores_header(self):  # v1.02  # v1.03  # v1.04  # v1.05
        from proggen import M08_ARDUINO as m08  # v1.02  # v1.03  # v1.04  # v1.05
        from headless import headless_esp32_ota as ota  # v1.02  # v1.03  # v1.04  # v1.05
        with tempfile.TemporaryDirectory() as folder:  # v1.02  # v1.03  # v1.04  # v1.05
            sketch = Path(folder) / m08.M02.Ino_Dir_LED  # v1.02  # v1.03  # v1.04  # v1.05
            sketch.mkdir(parents=True)  # v1.02  # v1.03  # v1.04  # v1.05
            header = sketch / "LEDs_AutoProg.h"  # v1.02  # v1.03  # v1.04  # v1.05
            header.write_bytes(b"original configuration")  # v1.02  # v1.03  # v1.04  # v1.05
            network = dict(ip="192.0.2.20", gateway="192.0.2.1", mask="255.255.255.0", dns1="192.0.2.1", dns2="192.0.2.1")  # v1.02  # v1.03  # v1.04  # v1.05
            ctrl = MagicMock()  # v1.02  # v1.03  # v1.04  # v1.05
            ctrl.is_connection_open.return_value = False  # v1.02  # v1.03  # v1.04  # v1.05
            with patch.object(m08.M07, "Ensure_Existing_USB_Port", return_value="COM7"), patch.object(m08.M07, "Check_USB_Port_with_Dialog", return_value=True), patch.object(m08.P01, "Cells", return_value="COM7"), patch.object(m08, "GetWorkbookPath", return_value=folder), patch.object(m08.M28, "Is_PlatformIO", return_value=True), patch.object(m08, "Find_PIO", return_value="pio"), patch.object(m08, "Ensure_Git", return_value=True) as git, patch.object(ota, "validate_network", return_value=network), patch.object(m08, "Build_ESP32_Project", return_value=(b"image", b"partitions")) as build, patch.object(m08, "Upload_ESP32_Project", return_value=0) as upload:  # v1.02  # v1.03  # v1.04  # v1.05
                m08.Compile_and_Upload_Minimal_ESP32(ctrl, "esp32", "COM7", "secret", {"hostname": "mobaledlib"})  # v1.02  # v1.03  # v1.04  # v1.05
                self.assertEqual(build.call_args.kwargs["network"], network)  # v1.02  # v1.03  # v1.04  # v1.05
                git.assert_called_once_with("esp32")  # v1.02  # v1.03  # v1.04  # v1.05
                upload.assert_called_once()  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertEqual(header.read_bytes(), b"original configuration")  # v1.02  # v1.03  # v1.04  # v1.05


class Cancel554Tests(unittest.TestCase):  # v1.04  # v1.05
    def test_real_process_cancel_is_not_timeout_or_success(self):  # v1.04  # v1.05
        def report(line):  # v1.04  # v1.05
            if line.strip() == "READY":  # v1.04  # v1.05
                shared.cancel_running()  # v1.04  # v1.05
        with self.assertRaises(shared.UploadCancelled):  # v1.04  # v1.05
            shared.run_streaming([sys.executable, "-u", "-c", "import time; print('READY', flush=True); time.sleep(20)"], report, timeout=5)  # v1.04  # v1.05
        self.assertIsNone(shared._current["proc"])  # v1.04  # v1.05

    def test_device_dialog_cancel_closes_setup_without_build(self):  # v1.04  # v1.05
        from proggen import M08_ARDUINO as m08  # v1.04  # v1.05
        ctrl = MagicMock()  # v1.04  # v1.05
        with patch.object(m08.M07, "Check_USB_Port_with_Dialog", return_value=False), patch.object(m08, "Build_ESP32_Project") as build:  # v1.04  # v1.05
            m08.Compile_and_Upload_ESP32_Setup(ctrl, "esp32", "", host="", upload_password="", password="", hostname="mobaledlib", ota=True, firewall_hint="")  # v1.04  # v1.05
            ctrl.weblog.close_later.assert_called_once_with(0)  # v1.04  # v1.05
            build.assert_not_called()  # v1.04  # v1.05
            self.assertFalse(m08.Last_Upload["ok"])  # v1.04  # v1.05

    def test_runner_cancel_and_timeout_do_not_return_success(self):  # v1.04  # v1.05
        from mlpyproggen import Prog_Generator as pg  # v1.04  # v1.05
        from proggen import M08_ARDUINO as m08  # v1.04  # v1.05
        for error, expected in [(shared.UploadCancelled("cancelled"), pg.M40.UserBreak), (shared.UploadTimeout("timeout"), pg.M40.Timeout)]:  # v1.04  # v1.05
            page = MagicMock()  # v1.04  # v1.05
            with patch.object(m08, "Execute_Upload_Command", side_effect=error):  # v1.04  # v1.05
                result = pg.Prog_GeneratorPage.execute_shell_cmd(page, "pio run", "test")  # v1.04  # v1.05
                self.assertEqual(result, expected)  # v1.04  # v1.05
                self.assertNotEqual(result, pg.M40.Success)  # v1.04  # v1.05


class Shared560Tests(unittest.TestCase):  # v1.05
    def test_effect_connection_reused_only_for_same_usb_device(self):  # v1.05
        from proggen import M42_Dyn_Config as dyn  # v1.05
        ctrl = SimpleNamespace(is_connection_open=lambda: True, ARDUINO_IP=False, monitor_connected=False, ARDUINO_current_portname="COM7", cfg_lines=object())  # v1.05
        with patch.object(dyn.PG, "global_controller", ctrl):  # v1.05
            self.assertTrue(dyn.Reuse_Connection("COM7"))  # v1.05
            self.assertFalse(dyn.Reuse_Connection("COM8"))  # v1.05
            ctrl.monitor_connected = True  # v1.05
            self.assertFalse(dyn.Reuse_Connection("COM7"))  # v1.05
            ctrl.monitor_connected = False  # v1.05
            ctrl.ARDUINO_IP = True  # v1.05
            self.assertFalse(dyn.Reuse_Connection("COM7"))  # v1.05

    def test_original_m08_shared_update_does_not_disconnect(self):  # v1.05
        source = (Path(__file__).parent / "proggen/M08_ARDUINO.py").read_text(encoding="utf-8")  # v1.05
        fn = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == "Compile_and_Upload_Prog_to_Arduino")  # v1.05
        node = next(n for n in ast.walk(fn) if isinstance(n, ast.If) and any(isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "Shared" for t in x.targets) for x in n.body))  # v1.05
        for shared in (True, False):  # v1.05
            dyn, ctrl = MagicMock(), MagicMock()  # v1.05
            dyn.Reuse_Connection.return_value = shared  # v1.05
            env = dict(HexFile="", M42=dyn, Mode="Left", ComPort="COM7", PG=SimpleNamespace(global_controller=ctrl))  # v1.05
            exec(compile(ast.Module(body=[node], type_ignores=[]), "shared-path", "exec"), env)  # v1.05
            dyn.Try_Config_Only.assert_called_once_with("COM7", shared=shared)  # v1.05
            self.assertEqual(ctrl.disconnect.call_count, int(not shared))  # v1.05


class WiringTests(unittest.TestCase):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
    def test_m08_target_list_reuses_original_port_enumeration(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        from proggen import M08_ARDUINO as m08  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        with patch.object(m08.M07, "EnumComPorts", return_value=(["COM7"], ["Testboard"])) as ports:  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            choices = m08.Upload_Targets(wlan_host="device.local", board=m08.M02.HT_ESP32)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertIn("COM7", choices["usb:COM7"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertIn("device.local", choices["wlan"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertEqual(ports.call_args.kwargs["Transport"], "usb")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            choices = m08.Upload_Targets(wlan_host="device.local", board=m08.M02.HT_PICO)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertNotIn("wlan", choices)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05

    def test_original_m08_environment_mapping(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        source = Path(__file__).parent / "proggen/M08_ARDUINO.py"  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        tree = ast.parse(source.read_text(encoding="utf-8"))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        methods = {n.name:n for n in tree.body if isinstance(n, ast.FunctionDef)}  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        for name in ("Run_PlatformIO", "PIO_Command", "Upload_ESP32_Project", "Compile_and_Upload_Minimal_ESP32", "Compile_and_Upload_ESP32_Setup"):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
            self.assertIn(name, methods)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        # Original board-specific detection and Pico udev checks remain in the shared path.
        text = ast.get_source_segment(source.read_text(encoding="utf-8"), methods["Create_PIO_Build_cmd"])  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertIn("BOARD_NANO_OLD", text)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertIn("BOARD_NANO_FULL", text)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertIn("BOARD_PICO", text)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertIn("Pico_Udev_Ok", text)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05

    def test_structured_job_is_one_command_in_original_upload_dispatch(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        source = (Path(__file__).parent / "proggen/M08_ARDUINO.py").read_text(encoding="utf-8")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        tree = ast.parse(source)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        method = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "Compile_and_Upload_Prog_to_Arduino")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        condition = next(n.test for n in ast.walk(method) if isinstance(n, ast.If) and isinstance(n.test, ast.Call) and isinstance(n.test.func, ast.Name) and n.test.func.id == "isinstance" and any(isinstance(a, ast.Name) and a.id == "CommandStr" for a in n.test.args))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        job = shared.PlatformIOJob("pio", ".", "nano_old", port="COM1")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertTrue(eval(compile(ast.Expression(condition), "dispatch", "eval"), {"CommandStr": job}))  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05

    def test_main_minimal_upload_has_no_own_build_or_flash(self):  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        source = (Path(__file__).parent / "webmobaledlib.py").read_text(encoding="utf-8")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        tree = ast.parse(source)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        minimal = next(n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef) and n.name == "minimal_firmware")  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        calls = [n.func.attr for n in ast.walk(minimal) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)]  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertIn("Compile_and_Upload_Minimal_ESP32", calls)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertNotIn("build_platformio_project", calls)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
        self.assertNotIn("flash_usb", calls)  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05


if __name__ == "__main__":  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
    unittest.main()  # v1.00  # v1.02  # v1.03  # v1.04  # v1.05
