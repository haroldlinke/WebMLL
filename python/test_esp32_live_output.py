# Datei-Version: 1.00 (2026-11-19) - test_esp32_live_output.py
# Name:           test_esp32_live_output.py
# Path:           test_esp32_live_output.py
# Version:        1.00
# Last Update:    2026-11-19
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-19  Live-Ausgabe mit echten Prozessen, Maskierung, Fehler und Timeout pruefen
import subprocess  # v1.00
import sys  # v1.00
import tempfile  # v1.00
from pathlib import Path  # v1.00
import unittest  # v1.00

from headless.headless_esp32_ota import _run_live  # v1.00


class LiveOutputTests(unittest.TestCase):  # v1.00
    def test_first_output_arrives_before_process_finishes(self):  # v1.00
        with tempfile.TemporaryDirectory() as folder:  # v1.00
            marker = Path(folder) / "reported"  # v1.00
            def report(text):  # v1.00
                if "first" in text:  # v1.00
                    marker.write_text("ok")  # v1.00
            script = ("import pathlib,sys,time\np=pathlib.Path(sys.argv[1])\nprint('first',flush=True)\n"  # v1.00
                      "end=time.monotonic()+5\n"  # v1.00
                      "while not p.exists() and time.monotonic()<end: time.sleep(.01)\n"  # v1.00
                      "assert p.exists(), 'live callback missing'\nprint('second',flush=True)")  # v1.00
            result = _run_live([sys.executable, "-u", "-c", script, str(marker)], report, timeout=10)  # v1.00
            self.assertEqual(result.returncode, 0)  # v1.00
            self.assertIn("second", result.stdout)  # v1.00

    def test_progress_without_newline_and_fragmented_secret_are_masked(self):  # v1.00
        chunks = []  # v1.00
        script = ("import sys,time\nsys.stdout.write('phase abc');sys.stdout.flush();time.sleep(.7)\n"  # v1.00
                  "sys.stdout.write('def progress');sys.stdout.flush();time.sleep(.7)\n"  # v1.00
                  "sys.stderr.write('\\nerror detail\\n');sys.stderr.flush()")  # v1.00
        result = _run_live([sys.executable, "-u", "-c", script], chunks.append, timeout=10, secrets=("abcdef",))  # v1.00
        self.assertNotIn("abcdef", result.stdout)  # v1.00
        self.assertNotIn("abcdef", "".join(chunks))  # v1.00
        self.assertIn("********", result.stdout)  # v1.00
        self.assertIn("error detail", result.stdout)  # v1.00
        self.assertGreaterEqual(len(chunks), 2)  # v1.00

    def test_nonzero_exit_and_no_callback_keep_complete_output(self):  # v1.00
        result = _run_live([sys.executable, "-u", "-c", "import sys;print('failed');sys.exit(3)"], timeout=5)  # v1.00
        self.assertEqual(result.returncode, 3)  # v1.00
        self.assertEqual(result.stdout.strip(), "failed")  # v1.00

    def test_silent_process_timeout(self):  # v1.00
        with self.assertRaises(subprocess.TimeoutExpired):  # v1.00
            _run_live([sys.executable, "-c", "import time;time.sleep(20)"], timeout=.2)  # v1.00

    def test_abort_uses_and_restores_existing_log_binding(self):  # v1.00
        from types import SimpleNamespace  # v1.00
        previous = lambda: None  # v1.00
        bindings = {"Control-c": previous}  # v1.00
        controller = SimpleNamespace(bindings=bindings, bind=lambda key, callback: bindings.__setitem__(key, callback))  # v1.00
        class Log:  # v1.00
            ctrl = controller  # v1.00
            def report(self, text):  # v1.00
                if "ready" in text:  # v1.00
                    self.ctrl.bindings["Control-c"]()  # v1.00
        result = _run_live([sys.executable, "-u", "-c", "import time;print('ready',flush=True);time.sleep(20)"], Log().report, timeout=10)  # v1.00
        self.assertNotEqual(result.returncode, 0)  # v1.00
        self.assertIs(bindings["Control-c"], previous)  # v1.00
        self.assertNotIn("c", bindings)  # v1.00

    def test_upload_api_streams_and_keeps_masked_return_value(self):  # v1.00
        from unittest.mock import patch  # v1.00
        from headless.headless_esp32_ota import upload  # v1.00
        chunks = []  # v1.00
        with tempfile.TemporaryDirectory() as folder:  # v1.00
            script = Path(folder) / "uploader.py"  # v1.00
            script.write_text("import sys,time\nprint('Authenticating test-secret',flush=True)\ntime.sleep(.1)\nprint('Uploading...',flush=True)\n")  # v1.00
            with patch("headless.headless_esp32_ota.find_uploader", return_value=[sys.executable, str(script)]), patch("headless.headless_esp32_ota.socket.gethostbyname", return_value="127.0.0.1"):  # v1.00
                code, output = upload("esp.local", "test-secret", "firmware.bin", bytes([0xE9]) + bytes(23), report=chunks.append)  # v1.00
        self.assertEqual(code, 0)  # v1.00
        self.assertIn("Uploading...", output)  # v1.00
        self.assertNotIn("test-secret", output)  # v1.00
        self.assertNotIn("test-secret", "".join(chunks))  # v1.00
        self.assertIn("********", output)  # v1.00


if __name__ == "__main__":  # v1.00
    unittest.main()  # v1.00
