# Datei-Version: 1.08 (2026-11-19) - test_web_devices.py
# Name:           test_web_devices.py
# Path:           test_web_devices.py
# Version:        1.08
# Last Update:    2026-11-19
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.08  2026-11-19  NiceGUI-Kontext nach Porterkennung und Fehlerfreigabe des Workers testen
#   1.07  2026-11-19  Passive Geraeteliste und originale Start-/Upload-Rueckverbindung testen
import ast
import asyncio
import json
import logging
from pathlib import Path
import tempfile
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, AsyncMock, patch

from _web.web_devices import DeviceManager
from _web import web_tabs


def original_async(name, namespace):
    source = Path(__file__).parent / "webmobaledlib.py"
    tree = ast.parse(source.read_text(encoding="utf8"))
    function = next(n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), "exec"), namespace)
    return namespace[name]


class Controller:  # v1.00
    def __init__(self):  # v1.00
        self._conn_lock = threading.RLock()  # v1.00
        self._connection_context = threading.local()  # v1.00
        self.ARDUINO_status = ""  # v1.00
        self.ARDUINO_current_portname = ""  # v1.00
        self.ARDUINO_boardtype = ""  # v1.00
        self.ARDUINO_IP = False  # v1.00
        self._esp32_session = False  # v1.00
        self.calls = []  # v1.00
        self.good = {"COM3"}
        self.config = {}  # v1.00

    def getConfigData(self, key):
        return self.config.get(key)

    def setConfigData(self, key, value):
        self.config[key] = value

    def is_connection_open(self):  # v1.00
        return self.ARDUINO_status == "Connected"  # v1.00

    def connect(self, port, wlan=False):  # v1.00
        self.calls.append((port, wlan))  # v1.00
        self.ARDUINO_status = "Connected" if port in self.good else ""  # v1.00
        self.ARDUINO_current_portname = port if self.is_connection_open() else ""  # v1.00
        self.ARDUINO_IP = False  # v1.00
        self._esp32_session = False  # v1.00
        self.device_manager.observe()  # v1.00
        return self.is_connection_open()  # v1.00

    def connect_esp32(self, host, password):  # v1.00
        self.calls.append((host, password))  # v1.00
        self.ARDUINO_status = "Connected"  # v1.00
        self.ARDUINO_current_portname = host  # v1.00
        self.ARDUINO_IP = True  # v1.00
        self._esp32_session = True  # v1.00
        self.device_manager.observe()  # v1.00
        return True  # v1.00

    def disconnect(self):  # v1.00
        self.ARDUINO_status = ""  # v1.00
        self.ARDUINO_current_portname = ""  # v1.00
        self.device_manager.observe()

class DeviceTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.ctrl = Controller()
        self.manager = DeviceManager(self.ctrl, self.folder.name)
        self.ctrl.device_manager = self.manager
        self.manager.connector = lambda device: self.ctrl.connect_esp32(device["address"], self.manager._password(device)) if device["kind"] == "wlan" else self.ctrl.connect(device["address"], wlan=False)

    def tearDown(self):
        self.manager.shutdown()
        self.folder.cleanup()

    def test_last_connection_survives_shutdown_disconnect(self):  # v1.00
        key = self.manager.add("usb", "COM3")  # v1.00
        self.assertTrue(self.manager.connect(key))  # v1.00
        self.manager.shutdown()  # v1.00
        self.ctrl.disconnect()  # v1.00
        saved = json.loads(self.manager.path.read_text(encoding="utf8"))  # v1.00
        self.assertEqual(saved["last"], key)  # v1.00
        self.assertTrue(saved["active"])

    def test_manual_disconnect_is_saved(self):  # v1.00
        key = self.manager.add("usb", "COM3")  # v1.00
        self.manager.connect(key)  # v1.00
        self.manager.disconnect()  # v1.00
        self.assertFalse(json.loads(self.manager.path.read_text(encoding="utf8"))["active"])

    def test_wlan_password_does_not_enter_device_file(self):  # v1.00
        key = self.manager.add("wlan", "192.168.1.2", "mobaledlib", "secret-test")  # v1.00
        self.manager.connect(key)  # v1.00
        self.assertEqual(self.ctrl.calls[-1], ("192.168.1.2", "secret-test"))  # v1.00
        self.assertNotIn("secret-test", self.manager.path.read_text(encoding="utf8"))  # v1.00
        self.assertEqual(self.manager.rows()[0]["board"], "ESP32")  # v1.00
        restarted = DeviceManager(Controller(), self.folder.name)  # v1.00
        self.assertEqual(restarted._password(restarted.devices[key]), "secret-test")

    def test_scan_filters_bluetooth_and_keeps_all_usb_candidates(self):  # v1.00
        ports = [SimpleNamespace(device="COM3", vid=123, description="USB Serial"),  # v1.00
                 SimpleNamespace(device="COM4", vid=None, description="Bluetooth")]  # v1.00
        with patch("serial.tools.list_ports.comports", return_value=ports), patch.object(self.manager, "register_wlan"):  # v1.00
            devices = self.manager.scan()  # v1.00
        self.assertEqual([d["address"] for d in devices], ["COM3"])

    def test_custom_name_survives_discovery_and_password_reload(self):  # v1.01
        key = self.manager.add("wlan", "192.168.1.2", "mobaledlib", "rename-secret")  # v1.01
        self.manager.rename(key, "Bahnhof Nord")  # v1.01
        self.manager.add("wlan", "192.168.1.2", "mobaledlib")  # v1.01
        restarted = DeviceManager(Controller(), self.folder.name)  # v1.01
        self.assertEqual(restarted.devices[key]["name"], "Bahnhof Nord")  # v1.01
        self.assertEqual(restarted._password(restarted.devices[key]), "rename-secret")  # v1.01
        with self.assertRaises(ValueError):  # v1.01
            restarted.rename(key, " ")

    def test_serial_recovery_restores_requested_baudrate(self):  # v1.04
        import serial  # v1.04
        from unittest.mock import Mock  # v1.04
        from headless.headless_serial_port import open_serial_port  # v1.04
        connection = Mock(baudrate=115200)  # v1.04
        connection.open.side_effect = [serial.SerialException("Cannot configure port"), None]  # v1.04
        with patch("headless.headless_serial_port.time.sleep"):  # v1.04
            open_serial_port(connection)  # v1.04
        self.assertEqual(connection.open.call_count, 2)  # v1.04
        self.assertEqual(connection.baudrate, 115200)  # v1.04
        connection.close.assert_called_once()

    def test_remove_connected_device_clears_saved_choices(self):  # v1.06
        key = self.manager.add("usb", "COM3")  # v1.06
        other = self.manager.add("usb", "COM8")  # v1.06
        self.manager.connect(key)  # v1.06
        self.manager.set_automatic(key, True)  # v1.06
        self.manager.remove(key)  # v1.06
        self.assertFalse(self.ctrl.is_connection_open())  # v1.06
        restarted = DeviceManager(self.ctrl, self.folder.name)  # v1.06
        self.assertNotIn(key, restarted.devices)  # v1.06
        self.assertIsNone(restarted.add("usb", "COM3"))  # v1.06
        self.assertEqual(restarted.add("usb", "COM3", rediscover=True), key)  # v1.06
        self.assertIn(other, restarted.devices)  # v1.06
        self.assertEqual(restarted.last, "")  # v1.06
        self.assertEqual(restarted.automatic, "")

    def test_remove_other_device_keeps_current_connection(self):  # v1.06
        active = self.manager.add("usb", "COM3")  # v1.06
        other = self.manager.add("usb", "COM8")  # v1.06
        self.manager.connect(active)  # v1.06
        self.manager.remove(other)  # v1.06
        self.assertTrue(self.ctrl.is_connection_open())  # v1.06
        self.assertEqual(self.manager.last, active)


    def test_start_preference_respects_last_connected_flag(self):
        first = self.manager.add("usb", "COM3")
        second = self.manager.add("usb", "COM8")
        self.manager.last = first
        self.assertIsNone(self.manager.start_device(False))
        self.assertEqual(self.manager.start_device(True), first)
        self.manager.set_automatic(second, True)
        self.assertEqual(self.manager.start_device(False), second)
        self.assertEqual(self.ctrl.getConfigData("AutoConnect"), "1")

    def test_original_startup_uses_preferred_device(self):
        key = self.manager.add("usb", "COM3")
        self.manager.set_automatic(key, True)
        async def io_bound(function, *args):
            return function(*args)
        environment = {
            "ctrl": self.ctrl, "state": {"busy": False}, "_web_tabs": web_tabs,
            "asyncio": SimpleNamespace(sleep=AsyncMock()), "run": SimpleNamespace(io_bound=io_bound),
            "_stored_ports": lambda: ("COM8", ""), "wifi_target": lambda: None,
            "_port_present": lambda port: True, "logger": logging.getLogger(__name__),
            "_silent_connect": Mock(return_value=False), "_search_lichtmaschine": Mock(return_value=None),
            "after_connect": Mock(), "ui": SimpleNamespace(notify=Mock()), "tr": lambda text, **kw: text.format(**kw)}
        asyncio.run(original_async("startup_autoconnect", environment)())
        self.assertEqual(self.ctrl.ARDUINO_current_portname, "COM3")
        environment["_silent_connect"].assert_not_called()
        environment["_search_lichtmaschine"].assert_not_called()

    def test_original_autoconnect_off_prevents_preferred_connection(self):
        key = self.manager.add("usb", "COM3")
        self.manager.set_automatic(key, True)
        self.ctrl.setConfigData("AutoConnect", "0")
        environment = {"ctrl": self.ctrl, "_web_tabs": web_tabs}
        asyncio.run(original_async("startup_autoconnect", environment)())
        self.assertEqual(self.ctrl.calls, [])

    def test_original_upload_reconnect_uses_actual_usb_target(self):
        self.ctrl.setConfigData("AutoConnect", "1")
        self.ctrl.setConfigData("serportname", "COM8")
        silent = Mock(return_value=True)
        async def io_bound(function, *args):
            return function(*args)
        upload = {"ok": True, "host": "", "port": "COM3"}
        environment = {
            "ctrl": self.ctrl, "state": {"busy": False}, "_web_tabs": web_tabs,
            "ota_arduino": SimpleNamespace(Last_Upload=upload), "asyncio": SimpleNamespace(sleep=AsyncMock()),
            "run": SimpleNamespace(io_bound=io_bound), "_silent_connect": silent,
            "after_connect": Mock(), "ui": SimpleNamespace(notify=Mock()), "tr": lambda text, **kw: text.format(**kw)}
        asyncio.run(original_async("connect_after_upload", environment)())
        silent.assert_called_once_with("COM3", False, None)
        self.assertFalse(upload["ok"])

    def test_original_upload_reconnect_uses_wlan_transport(self):
        self.ctrl.setConfigData("AutoConnect", "1")
        silent = Mock(return_value=True)
        async def io_bound(function, *args):
            return function(*args)
        environment = {
            "ctrl": self.ctrl, "state": {"busy": False}, "_web_tabs": web_tabs,
            "ota_arduino": SimpleNamespace(Last_Upload={"ok": True, "host": "192.168.1.20"}),
            "headless_esp32_ota": SimpleNamespace(load_settings=lambda: {"password": "test-password"}),
            "asyncio": SimpleNamespace(sleep=AsyncMock()), "run": SimpleNamespace(io_bound=io_bound),
            "_silent_connect": silent, "after_connect": Mock(), "ui": SimpleNamespace(notify=Mock()),
            "tr": lambda text, **kw: text.format(**kw)}
        asyncio.run(original_async("connect_after_upload", environment)())
        silent.assert_called_once_with(None, None, None, ("192.168.1.20", "test-password"))

    def test_auto_detect_callback_restores_real_nicegui_context(self):
        from nicegui import ui, context
        with ui.column() as container:
            client = container.client
        observed = []
        async def connect():
            observed.append(context.client)
        callback = original_async("auto_connect_in_page", {"page_client": client, "auto_connect_after_detect": connect})
        asyncio.run(callback())
        self.assertEqual(observed, [client])

    def test_worker_uses_captured_client_and_releases_busy_after_bridge_error(self):
        state = {"busy": False}
        client = object()
        bridge = SimpleNamespace(set_bridge=Mock(side_effect=RuntimeError("bridge error")), clear_bridge=Mock())
        flush = Mock()
        environment = {"state": state, "page_client": client, "asyncio": asyncio, "web_dialogs": bridge, "flush_downloads": flush}
        worker = original_async("run_in_worker", environment)
        with self.assertRaises(RuntimeError):
            asyncio.run(worker(lambda: None))
        self.assertFalse(state["busy"])
        self.assertIs(bridge.set_bridge.call_args.args[1], client)
        bridge.clear_bridge.assert_called_once()


if __name__ == "__main__":
    unittest.main()
