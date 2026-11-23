# Datei-Version: 1.00 (2026-11-23) - test_m08_upload.py
# Name: test_m08_upload.py
# Path: test_m08_upload.py
# Version: 1.00
# Last Update: 2026-11-23
# Author: Harold Linke
# Licence: LGPL V2.1
# History of Change:
#   1.00 2026-11-23 Gemeinsame Befehle, Prozessausfuehrung, Nano/Pico/ESP32 und M08-Verdrahtung.
import no_tk  # v1.00
no_tk.install(force=True)  # v1.00
import ast  # v1.00
import io  # v1.00
import os  # v1.00
import subprocess  # v1.00
import sys  # v1.00
import tempfile  # v1.00
import unittest  # v1.00
from pathlib import Path  # v1.00
from types import SimpleNamespace  # v1.00
from unittest.mock import MagicMock, patch  # v1.00
from headless import headless_upload as shared  # v1.00


class CommandTests(unittest.TestCase):  # v1.00
    def test_all_original_board_environments(self):  # v1.00
        for board in ("nano_old", "nano_new", "nano_full", "uno", "pico", "esp32"):  # v1.00
            for port in ("COM17", "/dev/ttyUSB0", "/dev/ttyACM0", "/dev/cu.usbmodem101", "/dev/serial/by-id/usb-device"):  # v1.00
                with self.subTest(board=board, port=port):  # v1.00
                    job = shared.PlatformIOJob("/tools with spaces/pio", "project ü", board, port=port)  # v1.00
                    self.assertEqual(job.argv[0], "/tools with spaces/pio")  # v1.00
                    self.assertEqual(job.argv[job.argv.index("-e")+1], board)  # v1.00
                    self.assertEqual(job.argv[-1], port)  # v1.00
                    self.assertNotIn("cd ", str(job))  # v1.00

    def test_compile_only_and_precompiled_nano(self):  # v1.00
        job = shared.PlatformIOJob("pio", ".", "pico", upload=False, port="COM1")  # v1.00
        self.assertNotIn("upload", job.argv)  # v1.00
        self.assertNotIn("--upload-port", job.argv)  # v1.00
        precompiled = shared.PlatformIOJob("pio", ".", "nano_old", port="COM1", nobuild=True)  # v1.00
        self.assertEqual(precompiled.argv.count("upload"), 1)  # v1.00
        self.assertIn("nobuild", precompiled.argv)  # v1.00

    def test_wlan_password_never_in_command_or_argv(self):  # v1.00
        previous_protocol = os.environ.get("PLATFORMIO_UPLOAD_PROTOCOL")  # v1.00
        job = shared.PlatformIOJob("pio", ".", "esp32", port="mobaledlib.local", transport="wlan", password="secret-test")  # v1.00
        self.assertNotIn("secret-test", str(job))  # v1.00
        self.assertNotIn("secret-test", " ".join(job.argv))  # v1.00
        self.assertEqual(job.transport, "wlan")  # v1.00
        self.assertIn("--auth=secret-test", job.environment_vars["PLATFORMIO_UPLOAD_FLAGS"])  # v1.00
        self.assertEqual(os.environ.get("PLATFORMIO_UPLOAD_PROTOCOL"), previous_protocol)  # v1.00
        for board in ("nano_old", "nano_full", "pico"):  # v1.00
            with self.assertRaises(ValueError):  # v1.00
                shared.PlatformIOJob("pio", ".", board, transport="wlan")  # v1.00

    def test_protocol_overlay_is_private_temporary_and_does_not_change_project(self):  # v1.00
        with tempfile.TemporaryDirectory() as folder:  # v1.00
            ini = Path(folder) / "platformio.ini"  # v1.00
            original = "[env:esp32]\nplatform = espressif32\n"  # v1.00
            ini.write_text(original, encoding="utf-8")  # v1.00
            job = shared.PlatformIOJob("pio", folder, "esp32", port="host.lan", transport="wlan", password="secret-test")  # v1.00
            with shared.upload_configuration(job):  # v1.00
                path = Path(job.argv[-1])  # v1.00
                self.assertTrue(path.is_file())  # v1.00
                self.assertIn("upload_protocol = espota", path.read_text(encoding="utf-8"))  # v1.00
                self.assertNotIn("secret-test", path.read_text(encoding="utf-8"))  # v1.00
            self.assertFalse(path.exists())  # v1.00
            self.assertEqual(ini.read_text(encoding="utf-8"), original)  # v1.00
            self.assertNotIn("--project-conf", job.argv)  # v1.00

    def test_usb_cannot_inherit_ota_protocol(self):  # v1.00
        with patch.dict(os.environ, {"PLATFORMIO_UPLOAD_PROTOCOL":"espota", "PLATFORMIO_UPLOAD_FLAGS":"--auth=old"}):  # v1.00
            job = shared.PlatformIOJob("pio", ".", "esp32", port="COM1")  # v1.00
        self.assertNotIn("PLATFORMIO_UPLOAD_PROTOCOL", job.environment_vars)  # v1.00
        self.assertEqual(job.environment_vars["PLATFORMIO_UPLOAD_FLAGS"], "")  # v1.00


class ExecutionTests(unittest.TestCase):  # v1.00
    def test_real_process_arguments_and_masking(self):  # v1.00
        lines = []  # v1.00
        value = "path with spaces ü & $ ;"  # v1.00
        rc = shared.run_streaming([sys.executable, "-c", "import sys; print(sys.argv[1]); print('secret-test')", value], lines.append, 10, ("secret-test",))  # v1.00
        self.assertEqual(rc, 0)  # v1.00
        self.assertEqual(lines, [value, "********"])  # v1.00

    def test_structured_job_uses_argv_and_no_shell(self):  # v1.00
        job = shared.PlatformIOJob("pio", ".", "esp32", port="host.local", transport="wlan", password="secret-test")  # v1.00
        proc = MagicMock()  # v1.00
        proc.stdout = io.StringIO("--auth=secret-test\n")  # v1.00
        proc.wait.return_value = 0  # v1.00
        proc.returncode = 0  # v1.00
        callback, lines = MagicMock(), []  # v1.00
        with patch.object(shared.subprocess, "Popen", return_value=proc) as spawn:  # v1.00
            self.assertEqual(shared.run_streaming(job, lines.append, on_process=callback), 0)  # v1.00
        self.assertEqual(spawn.call_args.args[0][:len(job.argv)], list(job.argv))  # v1.00
        self.assertFalse(spawn.call_args.kwargs["shell"])  # v1.00
        self.assertEqual(spawn.call_args.kwargs["cwd"], job.project)  # v1.00
        callback.assert_called_once_with(proc)  # v1.00
        self.assertEqual(lines, ["--auth=********"])  # v1.00
        if os.name == "nt":  # v1.00
            self.assertTrue(spawn.call_args.kwargs["creationflags"])  # v1.00
        else:  # v1.00
            self.assertTrue(spawn.call_args.kwargs["start_new_session"])  # v1.00

    def test_real_timeout_terminates_child_process(self):  # v1.00
        with self.assertRaises(shared.UploadTimeout):  # v1.00
            shared.run_streaming([sys.executable, "-c", "import time; time.sleep(20)"], lambda line: None, 0.2)  # v1.00
        self.assertIsNone(shared._current["proc"])  # v1.00

    def test_cancellation_reaches_current_process(self):  # v1.00
        proc = MagicMock()  # v1.00
        proc.poll.return_value = None  # v1.00
        with patch.dict(shared._current, {"proc":proc, "cancelled":False}), patch.object(shared, "_kill_tree") as kill:  # v1.00
            self.assertTrue(shared.cancel_running())  # v1.00
            self.assertTrue(shared._current["cancelled"])  # v1.00
            kill.assert_called_once_with(proc)  # v1.00


class TranslationTests(unittest.TestCase):  # v1.00
    def test_new_messages_in_all_seven_languages(self):  # v1.00
        from _web.web_i18n import use_language, tr  # v1.00
        keys = ["Gerät und Verbindung", "WLAN-Upload wird für dieses Board nicht unterstützt.", "Das Build-Ergebnis wurde zwischenzeitlich geändert. Bitte erneut übertragen.", "Die PlatformIO-Werkzeugpfade konnten nicht ermittelt werden.", "Es wird nur kompiliert, nicht hochgeladen."]  # v1.00
        for key in keys:  # v1.00
            for language in range(7):  # v1.00
                with self.subTest(key=key, language=language), use_language(language):  # v1.00
                    if language == 0:  # v1.00
                        self.assertEqual(tr(key), key)  # v1.00
                    else:  # v1.00
                        self.assertTrue(tr(key))  # v1.00
                        self.assertNotEqual(tr(key), key)  # v1.00


class WiringTests(unittest.TestCase):  # v1.00
    def test_m08_target_list_reuses_original_port_enumeration(self):  # v1.00
        from proggen import M08_ARDUINO as m08  # v1.00
        with patch.object(m08.M07, "EnumComPorts", return_value=(["COM7"], ["Testboard"])) as ports:  # v1.00
            choices = m08.Upload_Targets(wlan_host="device.local", board=m08.M02.HT_ESP32)  # v1.00
            self.assertIn("COM7", choices["usb:COM7"])  # v1.00
            self.assertIn("device.local", choices["wlan"])  # v1.00
            self.assertEqual(ports.call_args.kwargs["Transport"], "usb")  # v1.00
            choices = m08.Upload_Targets(wlan_host="device.local", board=m08.M02.HT_PICO)  # v1.00
            self.assertNotIn("wlan", choices)  # v1.00

    def test_original_m08_environment_mapping(self):  # v1.00
        source = Path(__file__).parent / "proggen/M08_ARDUINO.py"  # v1.00
        tree = ast.parse(source.read_text(encoding="utf-8"))  # v1.00
        methods = {n.name:n for n in tree.body if isinstance(n, ast.FunctionDef)}  # v1.00
        for name in ("Run_PlatformIO", "PIO_Command", "Upload_ESP32_Project", "Compile_and_Upload_Minimal_ESP32", "Compile_and_Upload_ESP32_Setup"):  # v1.00
            self.assertIn(name, methods)  # v1.00
        # Original board-specific detection and Pico udev checks remain in the shared path.
        text = ast.get_source_segment(source.read_text(encoding="utf-8"), methods["Create_PIO_Build_cmd"])  # v1.00
        self.assertIn("BOARD_NANO_OLD", text)  # v1.00
        self.assertIn("BOARD_NANO_FULL", text)  # v1.00
        self.assertIn("BOARD_PICO", text)  # v1.00
        self.assertIn("Pico_Udev_Ok", text)  # v1.00

    def test_structured_job_is_one_command_in_original_upload_dispatch(self):  # v1.00
        source = (Path(__file__).parent / "proggen/M08_ARDUINO.py").read_text(encoding="utf-8")  # v1.00
        tree = ast.parse(source)  # v1.00
        method = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "Compile_and_Upload_Prog_to_Arduino")  # v1.00
        condition = next(n.test for n in ast.walk(method) if isinstance(n, ast.If) and isinstance(n.test, ast.Call) and isinstance(n.test.func, ast.Name) and n.test.func.id == "isinstance" and any(isinstance(a, ast.Name) and a.id == "CommandStr" for a in n.test.args))  # v1.00
        job = shared.PlatformIOJob("pio", ".", "nano_old", port="COM1")  # v1.00
        self.assertTrue(eval(compile(ast.Expression(condition), "dispatch", "eval"), {"CommandStr": job}))  # v1.00

    def test_main_minimal_upload_has_no_own_build_or_flash(self):  # v1.00
        source = (Path(__file__).parent / "webmobaledlib.py").read_text(encoding="utf-8")  # v1.00
        tree = ast.parse(source)  # v1.00
        minimal = next(n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef) and n.name == "minimal_firmware")  # v1.00
        calls = [n.func.attr for n in ast.walk(minimal) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)]  # v1.00
        self.assertIn("Compile_and_Upload_Minimal_ESP32", calls)  # v1.00
        self.assertNotIn("build_platformio_project", calls)  # v1.00
        self.assertNotIn("flash_usb", calls)  # v1.00


if __name__ == "__main__":  # v1.00
    unittest.main()  # v1.00
