# Datei-Version: 1.10 (2026-11-26) - test_dyn_config_wlan.py
# Name: test_dyn_config_wlan.py
# Path: test_dyn_config_wlan.py
# Version: 1.10
# Last Update: 2026-11-26
# Author: Harold Linke
# Licence: LGPL V2.1
# History of Change:
#   1.10 2026-11-26 M08-Abgleich auf Original-Release 5.54; Programm-VERSION unveraendert 5.54.
#   1.09 2026-11-26 M08-Upload auf 5.41/MobaLedLib 3.6.0 aktualisiert; neue Originalkorrekturen erhalten.
#   1.08 2026-11-24 M08-Upload auf Original 5.12 aktualisiert, Pico-Identifikation und Firmware-Signatur erhalten.
#   1.06 2026-11-23 M08-Transportadapter in den Konfigurations-Regressionstests verwenden.
#   1.05 2026-11-22 Drei WLAN-Versuche, Erfolg im dritten Versuch, Abbruch nach drei Fehlern.
#   1.04 2026-11-22 Verzoegerten Firmware-Neustart absichern; insgesamt 14 Tests.
#   1.03 2026-11-22 Abschlusspruefung bei verlorener END-Antwort.
#   1.02 2026-11-22 PlatformIO-Werkzeugsuche ohne IDE und isolierte Uploadtests.
#   1.01 2026-11-22 Header-Parameteruebergabe bis zur inneren Generatorfunktion pruefen.
#   1.00 2026-11-22 TCP-Protokoll mit echtem lokalen Socket, HMAC und fragmentierten Antworten.
import no_tk  # headless Teststart auch ohne installiertes tkinter  # v1.06  # v1.08  # v1.09  # v1.10
no_tk.install(force=True)  # v1.06  # v1.08  # v1.09  # v1.10
from pathlib import Path
import hashlib
import hmac
import socket
import threading
import unittest
from unittest.mock import patch
from headless import headless_dyn_config as DC
from _web.web_serial import TcpPort
from test_dyn_config import FakeDevice, SIG


class WlanTests(unittest.TestCase):
    def session(self, password="secret", corrupt=False, disconnect=False):
        server = socket.socket()
        server.bind(("127.0.0.1", 0))
        server.listen()
        port = server.getsockname()[1]
        device = FakeDevice(SIG)
        errors = []
        def run():
            try:
                with server.accept()[0] as conn:
                    conn.settimeout(3)
                    nonce = b"0123456789abcdef0123456789abcdef"
                    conn.sendall(nonce[:12])
                    conn.sendall(nonce[12:] + b"\n")
                    f = conn.makefile("rb")
                    digest = f.readline().strip()
                    expected = hmac.digest(b"secret", nonce, "sha256").hex().encode()
                    if digest != expected:
                        conn.sendall(b"DENIED\n")
                        return
                    conn.sendall(b"OK\n")
                    if disconnect:
                        return
                    device.out = b""
                    while True:
                        line = f.readline()
                        if not line:
                            break
                        device.write(line)
                        answer, device.out = device.out, b""
                        if corrupt and b" ACK " in answer:
                            answer = b"~MLLCFG ACK 99999\n"
                        conn.sendall(answer[:5])
                        conn.sendall(answer[5:])
            except (ConnectionError, OSError):
                pass
            except BaseException as e:
                errors.append(e)
            finally:
                server.close()
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        factory = lambda host, ignored, timeout: TcpPort(host, port, timeout)
        return thread, device, errors, patch("_web.web_serial.TcpPort", side_effect=factory)

    def test_roundtrip(self):
        thread, dev, errors, patched = self.session()
        blob = DC.pack_blob(bytes(range(256)) * 3, b"", b"", b"", b"", 0, SIG)
        with patched:
            link = DC.TcpLink("127.0.0.1", "secret")
            try:
                self.assertEqual(DC.query_info(link)["sig"], SIG)
                progress = []
                DC.send_blob(link, blob, lambda a, b: progress.append((a, b)))
                self.assertEqual(dev.file, blob)
                self.assertEqual(progress[-1], (len(blob), len(blob)))
                self.assertEqual(DC.query_info(link)["valid"], "1")
            finally:
                link.close()
        thread.join(4)
        self.assertFalse(thread.is_alive())
        self.assertEqual(errors, [])

    def test_bad_password(self):
        thread, dev, errors, patched = self.session()
        with patched, self.assertRaises(DC.DynConfigError):
            DC.TcpLink("127.0.0.1", "wrong")
        thread.join(4)
        self.assertIsNone(dev.file)

    def test_bad_ack(self):
        thread, dev, errors, patched = self.session(corrupt=True)
        with patched:
            link = DC.TcpLink("127.0.0.1", "secret")
            try:
                blob = DC.pack_blob(b"123", b"", b"", b"", b"", 0, SIG)
                with self.assertRaisesRegex(DC.DynConfigError, "Bestaetigung"):
                    DC.send_blob(link, blob)
            finally:
                link.close()
        thread.join(4)
        self.assertIsNone(dev.file)

    def test_disconnect(self):
        thread, dev, errors, patched = self.session(disconnect=True)
        with patched:
            link = DC.TcpLink("127.0.0.1", "secret")
            try:
                with self.assertRaises(DC.DynConfigError):
                    DC.query_info(link, 1)
            finally:
                link.close()
        thread.join(4)


class RetryTests(unittest.TestCase):
    def run_attempts(self, outcomes, after_flash=False):
        import ast
        from unittest.mock import MagicMock
        source = Path(__file__).with_name("proggen") / "M42_Dyn_Config.py"
        node = next(n for n in ast.parse(source.read_text(encoding="utf-8")).body if isinstance(n, ast.FunctionDef) and n.name == "_wlan_attempts")
        operation = MagicMock(side_effect=outcomes)
        fallback = MagicMock(return_value=False)
        clock = MagicMock()
        env = dict(DC=DC, _out=MagicMock(), _t=lambda text, **kw: text.format(**kw), time=clock, _fallback=fallback)
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), env)
        result = env["_wlan_attempts"](operation, after_flash=after_flash)
        return result, operation, fallback, clock

    def test_third_attempt_succeeds(self):
        result, op, fallback, clock = self.run_attempts([DC.DynConfigError("DATA"), OSError("TCP"), True])
        self.assertTrue(result)
        self.assertEqual(op.call_count, 3)
        fallback.assert_not_called()
        self.assertEqual(clock.sleep.call_count, 2)

    def test_three_failures_fallback_once(self):
        result, op, fallback, clock = self.run_attempts([OSError("TCP")] * 3)
        self.assertFalse(result)
        self.assertEqual(op.call_count, 3)
        fallback.assert_called_once()

    def test_mismatch_not_retried(self):
        result, op, fallback, clock = self.run_attempts([False])
        self.assertFalse(result)
        op.assert_called_once()
        clock.sleep.assert_not_called()

    def test_after_flash_failure_does_not_flash_again(self):
        result, op, fallback, clock = self.run_attempts([OSError("TCP")] * 3, after_flash=True)
        self.assertFalse(result)
        self.assertEqual(op.call_count, 3)
        fallback.assert_not_called()


class FirmwareRestartTests(unittest.TestCase):
    def test_saved_wifi_retries_without_erasing_credentials(self):  # v1.08  # v1.09  # v1.10
        source = (Path(__file__).parent / "LEDs_AutoProg" / "ESP32Extensions.h").read_text(encoding="utf-8")  # v1.08  # v1.09  # v1.10
        loop = source.split("void loopESP32Extensions() {", 1)[1]  # v1.08  # v1.09  # v1.10
        retry = loop.split("#ifdef MLL_OTA_SAVED_WIFI", 1)[1].split("#endif", 1)[0]  # v1.08  # v1.09  # v1.10
        self.assertIn("15000UL", retry)  # v1.08  # v1.09  # v1.10
        self.assertIn("WiFi.reconnect()", retry)  # v1.08  # v1.09  # v1.10
        self.assertNotIn("WiFi.disconnect", retry)  # v1.08  # v1.09  # v1.10

    def test_restart_is_deferred_to_main_loop(self):
        root = Path(__file__).parent / "LEDs_AutoProg"
        firmware = (root / "MLLDynConfig.h").read_text(encoding="utf-8")
        restart = firmware.split("static void MllRestart(Stream &port)", 1)[1].split("//-------------------------------------------", 1)[0]
        active = "\n".join(line for line in restart.splitlines() if not line.lstrip().startswith("//"))
        self.assertNotIn("ESP.restart()", active)
        self.assertIn("mllCfgRestartPending = true", active)
        ino = (root / "LEDs_AutoProg.ino").read_text(encoding="utf-8")
        main_loop = ino.split("void loop(){", 1)[1]
        self.assertIn("MllCfgPollRestart();", main_loop[:180])


class CommitVerificationTests(unittest.TestCase):
    def run_check(self, valid=True, partial=False):
        import ast
        from unittest.mock import MagicMock
        source = Path(__file__).with_name("proggen") / "M42_Dyn_Config.py"
        node = next(n for n in ast.parse(source.read_text(encoding="utf-8")).body if isinstance(n, ast.FunctionDef) and n.name == "_send_config")
        backend = MagicMock()
        backend.DynConfigError = DC.DynConfigError
        blob = b"configuration"
        def send(link, data, progress):
            progress(len(data) - int(partial), len(data))
            raise DC.DynConfigError("Keine Antwort auf END")
        backend.send_blob.side_effect = send
        backend.blob_crc.return_value = 123
        backend.query_info.return_value = dict(sig=SIG, valid="1", cfg="0000007b" if valid else "00000000")
        clock = MagicMock()
        clock.monotonic.side_effect = [0, 0, 26]
        env = dict(DC=backend, time=clock, _progress=lambda: MagicMock(), _state={"sig": SIG}, log=MagicMock())
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), env)
        link = MagicMock()
        if valid and not partial:
            env["_send_config"](link, blob, "host", "password")
            backend.TcpLink.return_value.close.assert_called_once()
        else:
            with self.assertRaises(DC.DynConfigError):
                env["_send_config"](link, blob, "host", "password")
        if partial:
            backend.TcpLink.assert_not_called()

    def test_lost_end_verified(self):
        self.run_check()

    def test_wrong_crc_still_fails(self):
        self.run_check(valid=False)

    def test_partial_transfer_still_fails(self):
        self.run_check(partial=True)


class ToolDiscoveryTests(unittest.TestCase):
    def test_platformio_never_searches_arduino_ide(self):
        import ast
        from unittest.mock import MagicMock
        source = Path(__file__).with_name("proggen") / "M42_Dyn_Config.py"
        node = next(n for n in ast.parse(source.read_text(encoding="utf-8")).body if isinstance(n, ast.FunctionDef) and n.name == "_tools")
        backend = MagicMock()
        backend.find_avr_tools.return_value = {"bin": "pio-tools"}
        platform = MagicMock()
        platform.Is_PlatformIO.return_value = True
        env = {"_state": {"tools_checked": False}, "DC": backend, "M28": platform, "log": MagicMock()}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), env)
        # with patch("proggen.M08_ARDUINO.Find_ArduinoExe", side_effect=AssertionError("IDE must not be searched")) as ide:  # v1.08 (entfallen)
        with patch("proggen.M08_ARDUINO.Find_ArduinoExe", side_effect=AssertionError("IDE must not be searched")) as ide, patch("proggen.M08_ARDUINO.PIO_AVR_Paths", return_value=(["external/bin"], ["external/core"])):  # v1.06  # v1.08  # v1.09  # v1.10
            self.assertEqual(env["_tools"](), {"bin": "pio-tools"})
            ide.assert_not_called()
        # backend.find_avr_tools.assert_called_once_with([], [])  # v1.08 (entfallen)
        backend.find_avr_tools.assert_called_once_with(["external/bin"], ["external/core"])  # v1.06  # v1.08  # v1.09  # v1.10


class HeaderForwardingTests(unittest.TestCase):
    def test_public_header_function_forwards_dynamic_options(self):
        import ast
        from unittest.mock import MagicMock
        source = Path(__file__).with_name("proggen") / "M06_Write_Header.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        outer = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "Create_HeaderFile")
        inner = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "Write_Header_File_and_Upload_to_Arduino")
        call = next(n for n in ast.walk(outer) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == inner.name)
        target = MagicMock()
        env = {inner.name: target, "CreateFilesOnly": False, "LEDs_per_Channel": 3, "HeaderOnly": True,
               "DynamicConfig": True, "DynFirmwareKey": "firmware-key"}
        eval(compile(ast.Expression(call), str(source), "eval"), env)
        target.assert_called_once_with(False, LEDsInUse=3, HeaderOnly=True, DynamicConfig=True, DynFirmwareKey="firmware-key")
        args = ast.arguments(posonlyargs=[], args=inner.args.args, vararg=None, kwonlyargs=inner.args.kwonlyargs,
                             kw_defaults=inner.args.kw_defaults, kwarg=None, defaults=inner.args.defaults)
        probe = ast.FunctionDef(name="probe", args=args, body=[ast.Return(value=ast.Tuple(elts=[ast.Name(id="DynamicConfig", ctx=ast.Load()), ast.Name(id="DynFirmwareKey", ctx=ast.Load())], ctx=ast.Load()))], decorator_list=[])
        module = ast.fix_missing_locations(ast.Module(body=[probe], type_ignores=[]))
        exec(compile(module, str(source), "exec"), env)
        self.assertEqual(env["probe"](DynamicConfig=True, DynFirmwareKey="firmware-key"), (True, "firmware-key"))


class UploadFlowTests(unittest.TestCase):
    # def run_upload(self, matched=True, flash_result=0, config_result=True):  # v1.08 (entfallen)
    def run_upload(self, matched=True, flash_result=0, config_result=True, compile_only=False):  # v1.06  # v1.08  # v1.09  # v1.10
        import ast
        from types import SimpleNamespace
        from unittest.mock import MagicMock
        source = Path(__file__).with_name("proggen") / "M08_ARDUINO.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "Compile_and_Upload_ESP32_Setup")
        events = []
        dyn = MagicMock()
        dyn.Active.return_value = True
        dyn.Try_Config_Only.side_effect = lambda *a, **k: events.append("config-only") or matched
        dyn.After_Full_Flash.side_effect = lambda *a, **k: events.append("after-flash") or config_result
        backend = MagicMock()
        backend.build_platformio_project.side_effect = lambda *a, **k: events.append("build") or (b"image", b"partition")
        backend.upload.side_effect = lambda *a, **k: events.append("ota") or (flash_result, "output")
        header = MagicMock()
        header.Create_HeaderFile.return_value = True
        ctrl = MagicMock()
        # ctrl.execute_upload = True  # v1.08 (entfallen)
        # env = dict(M42=dyn, Last_Upload={}, M07=MagicMock(), M25=MagicMock(), M02=SimpleNamespace(Ino_Dir_LED="LEDs_AutoProg"),  # v1.08 (entfallen)
                   # M28=MagicMock(), os=__import__("os"), GetWorkbookPath=lambda: ".", Find_PIO=lambda: "pio", Write_PIO_Project=MagicMock())  # v1.08 (entfallen)
        ctrl.execute_upload = not compile_only  # v1.06  # v1.08  # v1.09  # v1.10
        env = dict(Ensure_Git=lambda *args: True, M42=dyn, Last_Upload={}, M07=MagicMock(), M25=MagicMock(), M02=SimpleNamespace(Ino_Dir_LED="LEDs_AutoProg"),  # v1.08  # v1.09  # v1.10
                   M28=MagicMock(), os=__import__("os"), GetWorkbookPath=lambda: ".", Find_PIO=lambda: "pio", Write_PIO_Project=MagicMock(), Upload_ESP32_Project=lambda *args, **kwargs: events.append("ota") or flash_result, Upload_ESP32_File=backend.upload, Build_ESP32_Project=backend.build_platformio_project, subprocess=__import__("subprocess"))  # v1.06  # v1.08  # v1.09  # v1.10
        code = compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec")
        with patch("proggen.M06_Write_Header.Create_HeaderFile", header.Create_HeaderFile), patch("headless.headless_esp32_ota.build_platformio_project", backend.build_platformio_project), patch("headless.headless_esp32_ota.upload", backend.upload):
            exec(code, env)
            env[node.name](ctrl, "esp32", "", host="192.0.2.1", upload_password="old", password="new", hostname="mobaledlib", ota=True, firewall_hint="hint")
        return events, env, dyn, header

    def test_compile_only_never_flashes_or_sends_configuration(self):  # v1.06  # v1.08  # v1.09  # v1.10
        events, env, dyn, header = self.run_upload(matched=False, compile_only=True)  # v1.06  # v1.08  # v1.09  # v1.10
        self.assertEqual(events, ["build"])  # v1.06  # v1.08  # v1.09  # v1.10
        dyn.Try_Config_Only.assert_not_called()  # v1.06  # v1.08  # v1.09  # v1.10
        dyn.After_Full_Flash.assert_not_called()  # v1.06  # v1.08  # v1.09  # v1.10
        self.assertFalse(env["Last_Upload"]["ok"])  # v1.06  # v1.08  # v1.09  # v1.10

    def test_matching_skips_build(self):
        events, env, dyn, header = self.run_upload()
        self.assertEqual(events, ["config-only"])
        self.assertTrue(env["Last_Upload"]["ok"])
        self.assertEqual(dyn.Try_Config_Only.call_args.kwargs["password"], "old")
        self.assertTrue(header.Create_HeaderFile.call_args.kwargs["DynamicConfig"])

    def test_fallback_and_new_password(self):
        events, env, dyn, header = self.run_upload(matched=False)
        self.assertEqual(events, ["config-only", "build", "ota", "after-flash"])
        self.assertEqual(dyn.After_Full_Flash.call_args.kwargs["password"], "new")
        self.assertTrue(env["Last_Upload"]["ok"])

    def test_failed_ota_skips_config(self):
        events, env, dyn, header = self.run_upload(matched=False, flash_result=1)
        self.assertNotIn("after-flash", events)
        self.assertFalse(env["Last_Upload"]["ok"])

    def test_failed_config_not_success(self):
        events, env, dyn, header = self.run_upload(matched=False, config_result=False)
        self.assertFalse(env["Last_Upload"]["ok"])

if __name__ == "__main__":
    unittest.main()
