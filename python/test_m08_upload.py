# Datei-Version: 1.02 (2026-11-24) - test_m08_upload.py
# Name: test_m08_upload.py
# Path: test_m08_upload.py
# Version: 1.02
# Last Update: 2026-11-24
# Author: Harold Linke
# Licence: LGPL V2.1
# History of Change:
#   1.02 2026-11-24 M08-Upload auf Original 5.12 aktualisiert, Pico-Identifikation und Firmware-Signatur erhalten.
#   1.01 2026-11-23 nobuild darf beim Protokollwechsel keine fertige Firmware bereinigen.
#   1.00 2026-11-23 Gemeinsame Befehle, Prozessausfuehrung, Nano/Pico/ESP32 und M08-Verdrahtung.
import no_tk  # v1.00  # v1.02
no_tk.install(force=True)  # v1.00  # v1.02
import ast  # v1.00  # v1.02
import io  # v1.00  # v1.02
import os  # v1.00  # v1.02
import subprocess  # v1.00  # v1.02
import sys  # v1.00  # v1.02
import tempfile  # v1.00  # v1.02
import unittest  # v1.00  # v1.02
from pathlib import Path  # v1.00  # v1.02
from types import SimpleNamespace  # v1.00  # v1.02
from unittest.mock import MagicMock, patch  # v1.00  # v1.02
from headless import headless_upload as shared  # v1.00  # v1.02


class CommandTests(unittest.TestCase):  # v1.00  # v1.02
    def test_all_original_board_environments(self):  # v1.00  # v1.02
        for board in ("nano_old", "nano_new", "nano_full", "uno", "pico", "esp32"):  # v1.00  # v1.02
            for port in ("COM17", "/dev/ttyUSB0", "/dev/ttyACM0", "/dev/cu.usbmodem101", "/dev/serial/by-id/usb-device"):  # v1.00  # v1.02
                with self.subTest(board=board, port=port):  # v1.00  # v1.02
                    job = shared.PlatformIOJob("/tools with spaces/pio", "project ü", board, port=port)  # v1.00  # v1.02
                    self.assertEqual(job.argv[0], "/tools with spaces/pio")  # v1.00  # v1.02
                    self.assertEqual(job.argv[job.argv.index("-e")+1], board)  # v1.00  # v1.02
                    self.assertEqual(job.argv[-1], port)  # v1.00  # v1.02
                    self.assertNotIn("cd ", str(job))  # v1.00  # v1.02

    def test_compile_only_and_precompiled_nano(self):  # v1.00  # v1.02
        job = shared.PlatformIOJob("pio", ".", "pico", upload=False, port="COM1")  # v1.00  # v1.02
        self.assertNotIn("upload", job.argv)  # v1.00  # v1.02
        self.assertNotIn("--upload-port", job.argv)  # v1.00  # v1.02
        precompiled = shared.PlatformIOJob("pio", ".", "nano_old", port="COM1", nobuild=True)  # v1.00  # v1.02
        self.assertEqual(precompiled.argv.count("upload"), 1)  # v1.00  # v1.02
        self.assertIn("nobuild", precompiled.argv)  # v1.02
        self.assertIn("--disable-auto-clean", precompiled.argv)  # v1.01  # v1.00  # v1.02

    def test_wlan_password_never_in_command_or_argv(self):  # v1.00  # v1.02
        previous_protocol = os.environ.get("PLATFORMIO_UPLOAD_PROTOCOL")  # v1.00  # v1.02
        job = shared.PlatformIOJob("pio", ".", "esp32", port="mobaledlib.local", transport="wlan", password="secret-test")  # v1.00  # v1.02
        self.assertNotIn("secret-test", str(job))  # v1.00  # v1.02
        self.assertNotIn("secret-test", " ".join(job.argv))  # v1.00  # v1.02
        self.assertEqual(job.transport, "wlan")  # v1.00  # v1.02
        self.assertIn("--auth=secret-test", job.environment_vars["PLATFORMIO_UPLOAD_FLAGS"])  # v1.00  # v1.02
        self.assertEqual(os.environ.get("PLATFORMIO_UPLOAD_PROTOCOL"), previous_protocol)  # v1.00  # v1.02
        for board in ("nano_old", "nano_full", "pico"):  # v1.00  # v1.02
            with self.assertRaises(ValueError):  # v1.00  # v1.02
                shared.PlatformIOJob("pio", ".", board, transport="wlan")  # v1.00  # v1.02

    def test_protocol_overlay_is_private_temporary_and_does_not_change_project(self):  # v1.00  # v1.02
        with tempfile.TemporaryDirectory() as folder:  # v1.00  # v1.02
            ini = Path(folder) / "platformio.ini"  # v1.00  # v1.02
            original = "[env:esp32]\nplatform = espressif32\n"  # v1.00  # v1.02
            ini.write_text(original, encoding="utf-8")  # v1.00  # v1.02
            job = shared.PlatformIOJob("pio", folder, "esp32", port="host.lan", transport="wlan", password="secret-test")  # v1.00  # v1.02
            with shared.upload_configuration(job):  # v1.00  # v1.02
                path = Path(job.argv[-1])  # v1.00  # v1.02
                self.assertTrue(path.is_file())  # v1.00  # v1.02
                self.assertIn("upload_protocol = espota", path.read_text(encoding="utf-8"))  # v1.00  # v1.02
                self.assertNotIn("secret-test", path.read_text(encoding="utf-8"))  # v1.00  # v1.02
            self.assertFalse(path.exists())  # v1.00  # v1.02
            self.assertEqual(ini.read_text(encoding="utf-8"), original)  # v1.00  # v1.02
            self.assertNotIn("--project-conf", job.argv)  # v1.00  # v1.02

    def test_usb_cannot_inherit_ota_protocol(self):  # v1.00  # v1.02
        with patch.dict(os.environ, {"PLATFORMIO_UPLOAD_PROTOCOL":"espota", "PLATFORMIO_UPLOAD_FLAGS":"--auth=old"}):  # v1.00  # v1.02
            job = shared.PlatformIOJob("pio", ".", "esp32", port="COM1")  # v1.00  # v1.02
        self.assertNotIn("PLATFORMIO_UPLOAD_PROTOCOL", job.environment_vars)  # v1.00  # v1.02
        self.assertEqual(job.environment_vars["PLATFORMIO_UPLOAD_FLAGS"], "")  # v1.00  # v1.02


class ExecutionTests(unittest.TestCase):  # v1.00  # v1.02
    def test_real_process_arguments_and_masking(self):  # v1.00  # v1.02
        lines = []  # v1.00  # v1.02
        value = "path with spaces ü & $ ;"  # v1.00  # v1.02
        rc = shared.run_streaming([sys.executable, "-c", "import sys; print(sys.argv[1]); print('secret-test')", value], lines.append, 10, ("secret-test",))  # v1.00  # v1.02
        self.assertEqual(rc, 0)  # v1.00  # v1.02
        self.assertEqual(lines, [value, "********"])  # v1.00  # v1.02

    def test_structured_job_uses_argv_and_no_shell(self):  # v1.00  # v1.02
        job = shared.PlatformIOJob("pio", ".", "esp32", port="host.local", transport="wlan", password="secret-test")  # v1.00  # v1.02
        proc = MagicMock()  # v1.00  # v1.02
        proc.stdout = io.StringIO("--auth=secret-test\n")  # v1.00  # v1.02
        proc.wait.return_value = 0  # v1.00  # v1.02
        proc.returncode = 0  # v1.00  # v1.02
        callback, lines = MagicMock(), []  # v1.00  # v1.02
        with patch.object(shared.subprocess, "Popen", return_value=proc) as spawn:  # v1.00  # v1.02
            self.assertEqual(shared.run_streaming(job, lines.append, on_process=callback), 0)  # v1.00  # v1.02
        self.assertEqual(spawn.call_args.args[0][:len(job.argv)], list(job.argv))  # v1.00  # v1.02
        self.assertFalse(spawn.call_args.kwargs["shell"])  # v1.00  # v1.02
        self.assertEqual(spawn.call_args.kwargs["cwd"], job.project)  # v1.00  # v1.02
        callback.assert_called_once_with(proc)  # v1.00  # v1.02
        self.assertEqual(lines, ["--auth=********"])  # v1.00  # v1.02
        if os.name == "nt":  # v1.00  # v1.02
            self.assertTrue(spawn.call_args.kwargs["creationflags"])  # v1.00  # v1.02
        else:  # v1.00  # v1.02
            self.assertTrue(spawn.call_args.kwargs["start_new_session"])  # v1.00  # v1.02

    def test_real_timeout_terminates_child_process(self):  # v1.00  # v1.02
        with self.assertRaises(shared.UploadTimeout):  # v1.00  # v1.02
            shared.run_streaming([sys.executable, "-c", "import time; time.sleep(20)"], lambda line: None, 0.2)  # v1.00  # v1.02
        self.assertIsNone(shared._current["proc"])  # v1.00  # v1.02

    def test_cancellation_reaches_current_process(self):  # v1.00  # v1.02
        proc = MagicMock()  # v1.00  # v1.02
        proc.poll.return_value = None  # v1.00  # v1.02
        with patch.dict(shared._current, {"proc":proc, "cancelled":False}), patch.object(shared, "_kill_tree") as kill:  # v1.00  # v1.02
            self.assertTrue(shared.cancel_running())  # v1.00  # v1.02
            self.assertTrue(shared._current["cancelled"])  # v1.00  # v1.02
            kill.assert_called_once_with(proc)  # v1.00  # v1.02


class TranslationTests(unittest.TestCase):  # v1.00  # v1.02
    def test_new_messages_in_all_seven_languages(self):  # v1.00  # v1.02
        from _web.web_i18n import use_language, tr  # v1.00  # v1.02
        keys = ["Gerät und Verbindung", "WLAN-Upload wird für dieses Board nicht unterstützt.", "Das Build-Ergebnis wurde zwischenzeitlich geändert. Bitte erneut übertragen.", "Die PlatformIO-Werkzeugpfade konnten nicht ermittelt werden.", "Es wird nur kompiliert, nicht hochgeladen."]  # v1.00  # v1.02
        for key in keys:  # v1.00  # v1.02
            for language in range(7):  # v1.00  # v1.02
                with self.subTest(key=key, language=language), use_language(language):  # v1.00  # v1.02
                    if language == 0:  # v1.00  # v1.02
                        self.assertEqual(tr(key), key)  # v1.00  # v1.02
                    else:  # v1.00  # v1.02
                        self.assertTrue(tr(key))  # v1.00  # v1.02
                        self.assertNotEqual(tr(key), key)  # v1.00  # v1.02


class Upstream512Tests(unittest.TestCase):  # v1.02
    def test_pico_identity_reaches_port_rediscovery(self):  # v1.02
        from proggen import M42_Dyn_Config as dyn  # v1.02
        original = dict(dyn._state)  # v1.02
        try:  # v1.02
            dyn._state.update(blob=b"config", pico=True)  # v1.02
            with patch.object(dyn, "_out"), patch.object(dyn.DC, "wait_for_port", return_value=None) as wait:  # v1.02
                self.assertFalse(dyn.After_Full_Flash("COM7", expected_serial="pico-123", expected_location="usb-2"))  # v1.02
                wait.assert_called_once_with("COM7", True, 25.0, "pico-123", "usb-2")  # v1.02
        finally:  # v1.02
            dyn._state.clear()  # v1.02
            dyn._state.update(original)  # v1.02

    def test_current_program_version_is_available_for_firmware_signature(self):  # v1.02
        from proggen import M42_Dyn_Config as dyn  # v1.02
        self.assertEqual(dyn._program_version(), "5.12 (2026-11-24)")  # v1.02

    def test_minimal_firmware_keeps_static_network_settings_and_restores_header(self):  # v1.02
        from proggen import M08_ARDUINO as m08  # v1.02
        from headless import headless_esp32_ota as ota  # v1.02
        with tempfile.TemporaryDirectory() as folder:  # v1.02
            sketch = Path(folder) / m08.M02.Ino_Dir_LED  # v1.02
            sketch.mkdir(parents=True)  # v1.02
            header = sketch / "LEDs_AutoProg.h"  # v1.02
            header.write_bytes(b"original configuration")  # v1.02
            network = dict(ip="192.0.2.20", gateway="192.0.2.1", mask="255.255.255.0", dns1="192.0.2.1", dns2="192.0.2.1")  # v1.02
            ctrl = MagicMock()  # v1.02
            ctrl.is_connection_open.return_value = False  # v1.02
            with patch.object(m08.M07, "Ensure_Existing_USB_Port", return_value="COM7"), patch.object(m08.M07, "Check_USB_Port_with_Dialog", return_value=True), patch.object(m08.P01, "Cells", return_value="COM7"), patch.object(m08, "GetWorkbookPath", return_value=folder), patch.object(m08.M28, "Is_PlatformIO", return_value=True), patch.object(m08, "Find_PIO", return_value="pio"), patch.object(m08, "Ensure_Git", return_value=True) as git, patch.object(ota, "validate_network", return_value=network), patch.object(m08, "Build_ESP32_Project", return_value=(b"image", b"partitions")) as build, patch.object(m08, "Upload_ESP32_Project", return_value=0) as upload:  # v1.02
                m08.Compile_and_Upload_Minimal_ESP32(ctrl, "esp32", "COM7", "secret", {"hostname": "mobaledlib"})  # v1.02
                self.assertEqual(build.call_args.kwargs["network"], network)  # v1.02
                git.assert_called_once_with("esp32")  # v1.02
                upload.assert_called_once()  # v1.02
            self.assertEqual(header.read_bytes(), b"original configuration")  # v1.02


class WiringTests(unittest.TestCase):  # v1.00  # v1.02
    def test_m08_target_list_reuses_original_port_enumeration(self):  # v1.00  # v1.02
        from proggen import M08_ARDUINO as m08  # v1.00  # v1.02
        with patch.object(m08.M07, "EnumComPorts", return_value=(["COM7"], ["Testboard"])) as ports:  # v1.00  # v1.02
            choices = m08.Upload_Targets(wlan_host="device.local", board=m08.M02.HT_ESP32)  # v1.00  # v1.02
            self.assertIn("COM7", choices["usb:COM7"])  # v1.00  # v1.02
            self.assertIn("device.local", choices["wlan"])  # v1.00  # v1.02
            self.assertEqual(ports.call_args.kwargs["Transport"], "usb")  # v1.00  # v1.02
            choices = m08.Upload_Targets(wlan_host="device.local", board=m08.M02.HT_PICO)  # v1.00  # v1.02
            self.assertNotIn("wlan", choices)  # v1.00  # v1.02

    def test_original_m08_environment_mapping(self):  # v1.00  # v1.02
        source = Path(__file__).parent / "proggen/M08_ARDUINO.py"  # v1.00  # v1.02
        tree = ast.parse(source.read_text(encoding="utf-8"))  # v1.00  # v1.02
        methods = {n.name:n for n in tree.body if isinstance(n, ast.FunctionDef)}  # v1.00  # v1.02
        for name in ("Run_PlatformIO", "PIO_Command", "Upload_ESP32_Project", "Compile_and_Upload_Minimal_ESP32", "Compile_and_Upload_ESP32_Setup"):  # v1.00  # v1.02
            self.assertIn(name, methods)  # v1.00  # v1.02
        # Original board-specific detection and Pico udev checks remain in the shared path.
        text = ast.get_source_segment(source.read_text(encoding="utf-8"), methods["Create_PIO_Build_cmd"])  # v1.00  # v1.02
        self.assertIn("BOARD_NANO_OLD", text)  # v1.00  # v1.02
        self.assertIn("BOARD_NANO_FULL", text)  # v1.00  # v1.02
        self.assertIn("BOARD_PICO", text)  # v1.00  # v1.02
        self.assertIn("Pico_Udev_Ok", text)  # v1.00  # v1.02

    def test_structured_job_is_one_command_in_original_upload_dispatch(self):  # v1.00  # v1.02
        source = (Path(__file__).parent / "proggen/M08_ARDUINO.py").read_text(encoding="utf-8")  # v1.00  # v1.02
        tree = ast.parse(source)  # v1.00  # v1.02
        method = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "Compile_and_Upload_Prog_to_Arduino")  # v1.00  # v1.02
        condition = next(n.test for n in ast.walk(method) if isinstance(n, ast.If) and isinstance(n.test, ast.Call) and isinstance(n.test.func, ast.Name) and n.test.func.id == "isinstance" and any(isinstance(a, ast.Name) and a.id == "CommandStr" for a in n.test.args))  # v1.00  # v1.02
        job = shared.PlatformIOJob("pio", ".", "nano_old", port="COM1")  # v1.00  # v1.02
        self.assertTrue(eval(compile(ast.Expression(condition), "dispatch", "eval"), {"CommandStr": job}))  # v1.00  # v1.02

    def test_main_minimal_upload_has_no_own_build_or_flash(self):  # v1.00  # v1.02
        source = (Path(__file__).parent / "webmobaledlib.py").read_text(encoding="utf-8")  # v1.00  # v1.02
        tree = ast.parse(source)  # v1.00  # v1.02
        minimal = next(n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef) and n.name == "minimal_firmware")  # v1.00  # v1.02
        calls = [n.func.attr for n in ast.walk(minimal) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)]  # v1.00  # v1.02
        self.assertIn("Compile_and_Upload_Minimal_ESP32", calls)  # v1.00  # v1.02
        self.assertNotIn("build_platformio_project", calls)  # v1.00  # v1.02
        self.assertNotIn("flash_usb", calls)  # v1.00  # v1.02


if __name__ == "__main__":  # v1.00  # v1.02
    unittest.main()  # v1.00  # v1.02
