# Datei-Version: 1.06 (2026-11-19) - test_web_devices.py
# Name:           test_web_devices.py
# Path:           test_web_devices.py
# Version:        1.06
# Last Update:    2026-11-19
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.06  2026-11-19  Loeschen verbundener und anderer Geraeteeintraege testen
#   1.05  2026-11-19  USB-Unterdialog und automatische Verbindungen bei offenen Befehlen pruefen
#   1.04  2026-11-19  Gewuenschte Baudrate nach Treiber-Wiederherstellung pruefen
#   1.03  2026-11-19  Baudraten-Fallback der Blinkpruefung testen
#   1.02  2026-11-19  Busy-Port-Migration und Freigabe fuer die Port-Pruefung pruefen
#   1.01  2026-11-19  Umbenennen mit erhaltener Passwortzuordnung pruefen
#   1.00  2026-11-19  Regressionen fuer Geraeteverwaltung und automatische Verbindung
import json  # v1.00
from pathlib import Path  # v1.00
import tempfile  # v1.00
import threading  # v1.00
import unittest  # v1.00
from types import SimpleNamespace  # v1.00
from unittest.mock import patch  # v1.00

from _web.web_devices import DeviceManager  # v1.00


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
        self.good = {"COM3"}  # v1.00

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
        self.device_manager.observe()  # v1.00


class DeviceTests(unittest.TestCase):  # v1.00
    def setUp(self):  # v1.00
        self.folder = tempfile.TemporaryDirectory()  # v1.00
        self.ctrl = Controller()  # v1.00
        self.manager = DeviceManager(self.ctrl, self.folder.name)  # v1.00
        self.ctrl.device_manager = self.manager  # v1.00

    def tearDown(self):  # v1.00
        self.manager.shutdown()  # v1.00
        if self.manager.thread.is_alive():  # v1.00
            self.manager.thread.join(2)  # v1.00
        self.folder.cleanup()  # v1.00

    def test_last_connection_survives_shutdown_disconnect(self):  # v1.00
        key = self.manager.add("usb", "COM3")  # v1.00
        self.assertTrue(self.manager.connect(key))  # v1.00
        self.manager.shutdown()  # v1.00
        self.ctrl.disconnect()  # v1.00
        saved = json.loads(self.manager.path.read_text(encoding="utf8"))  # v1.00
        self.assertEqual(saved["last"], key)  # v1.00
        self.assertTrue(saved["active"])  # v1.00

    def test_manual_disconnect_is_saved(self):  # v1.00
        key = self.manager.add("usb", "COM3")  # v1.00
        self.manager.connect(key)  # v1.00
        self.manager.disconnect()  # v1.00
        self.assertFalse(json.loads(self.manager.path.read_text(encoding="utf8"))["active"])  # v1.00

    def test_wlan_password_does_not_enter_device_file(self):  # v1.00
        key = self.manager.add("wlan", "192.168.1.2", "mobaledlib", "secret-test")  # v1.00
        self.manager.connect(key)  # v1.00
        self.assertEqual(self.ctrl.calls[-1], ("192.168.1.2", "secret-test"))  # v1.00
        self.assertNotIn("secret-test", self.manager.path.read_text(encoding="utf8"))  # v1.00
        self.assertEqual(self.manager.rows()[0]["board"], "ESP32")  # v1.00
        restarted = DeviceManager(Controller(), self.folder.name)  # v1.00
        self.assertEqual(restarted._password(restarted.devices[key]), "secret-test")  # v1.00

    def test_scan_filters_bluetooth_and_keeps_all_usb_candidates(self):  # v1.00
        ports = [SimpleNamespace(device="COM3", vid=123, description="USB Serial"),  # v1.00
                 SimpleNamespace(device="COM4", vid=None, description="Bluetooth")]  # v1.00
        with patch("serial.tools.list_ports.comports", return_value=ports), patch.object(self.manager, "register_wlan"):  # v1.00
            devices = self.manager.scan()  # v1.00
        self.assertEqual([d["address"] for d in devices], ["COM3"])  # v1.00

    def test_upload_restores_the_exact_target_and_preserves_last_active(self):  # v1.00
        key = self.manager.add("usb", "COM3")  # v1.00
        self.manager.connect(key)  # v1.00
        @self.manager.upload_guard  # v1.00
        def upload():  # v1.00
            self.ctrl.disconnect()  # v1.00
            self.assertTrue(self.manager.active_at_exit)  # v1.00
            self.manager.after_upload("COM8")  # v1.00
        upload()  # v1.00
        generation, target = self.manager.tasks.get_nowait()  # v1.00
        self.assertEqual(target, "usb:COM8")  # v1.00
        self.assertEqual(generation, self.manager.generation)  # v1.00
        self.assertEqual(self.manager.uploads, 0)  # v1.00

    def test_startup_does_not_block_and_restores_saved_target(self):  # v1.00
        key = self.manager.add("usb", "COM3")  # v1.00
        self.manager.last, self.manager.active_at_exit = key, True  # v1.00
        finished = threading.Event()  # v1.00
        original = self.manager.connect  # v1.00
        def connect(target, generation=None):  # v1.00
            result = original(target, generation)  # v1.00
            finished.set()  # v1.00
            return result  # v1.00
        with patch.object(self.manager, "scan", return_value=[]), patch.object(self.manager, "connect", side_effect=connect):  # v1.00
            self.manager.start()  # v1.00
            self.assertFalse(finished.is_set())  # v1.00
            self.manager.ready.set()  # v1.00
            self.assertTrue(finished.wait(2))  # v1.00
        self.assertEqual(self.ctrl.calls, [("COM3", False)])  # v1.00

    def test_automatic_choice_and_cancel(self):  # v1.00
        key = self.manager.add("usb", "COM3")  # v1.00
        self.manager.set_automatic(key, True)  # v1.00
        other = DeviceManager(Controller(), self.folder.name)  # v1.00
        self.assertEqual(other.automatic, key)  # v1.00
        self.manager.after_upload("COM8")  # v1.00
        generation, target = self.manager.tasks.get_nowait()  # v1.00
        self.manager.cancel_pending()  # v1.00
        self.assertNotEqual(generation, self.manager.generation)  # v1.00

    def test_search_skips_nonresponding_port(self):  # v1.00
        first = self.manager.add("usb", "COM2")  # v1.00
        second = self.manager.add("usb", "COM3")  # v1.00
        self.manager.present = {"COM2", "COM3"}  # v1.00
        devices = [self.manager.devices[first], self.manager.devices[second]]  # v1.00
        finished = threading.Event()  # v1.00
        original = self.manager.connect  # v1.00
        def connect(key, generation=None):  # v1.00
            ok = original(key, generation)  # v1.00
            if ok:  # v1.00
                finished.set()  # v1.00
            return ok  # v1.00
        with patch.object(self.manager, "scan", return_value=devices), patch.object(self.manager, "connect", side_effect=connect):  # v1.00
            self.manager.start()  # v1.00
            self.manager.ready.set()  # v1.00
            self.assertTrue(finished.wait(2))  # v1.00
        self.assertEqual(self.ctrl.calls, [("COM2", False), ("COM3", False)])  # v1.00

    def test_cancelled_connection_is_not_opened(self):  # v1.00
        key = self.manager.add("usb", "COM3")  # v1.00
        generation = self.manager.generation  # v1.00
        self.manager.cancel_pending()  # v1.00
        self.assertFalse(self.manager.connect(key, generation))  # v1.00
        self.assertEqual(self.ctrl.calls, [])  # v1.00

    def test_custom_name_survives_discovery_and_password_reload(self):  # v1.01
        key = self.manager.add("wlan", "192.168.1.2", "mobaledlib", "rename-secret")  # v1.01
        self.manager.rename(key, "Bahnhof Nord")  # v1.01
        self.manager.add("wlan", "192.168.1.2", "mobaledlib")  # v1.01
        restarted = DeviceManager(Controller(), self.folder.name)  # v1.01
        self.assertEqual(restarted.devices[key]["name"], "Bahnhof Nord")  # v1.01
        self.assertEqual(restarted._password(restarted.devices[key]), "rename-secret")  # v1.01
        with self.assertRaises(ValueError):  # v1.01
            restarted.rename(key, " ")  # v1.01

    def test_busy_marker_does_not_create_another_device(self):  # v1.02
        key = self.manager.add("usb", "COM8")  # v1.02
        self.manager.rename(key, "Lima 1")  # v1.02
        self.assertEqual(self.manager.add("usb", "*COM8"), key)  # v1.02
        self.assertEqual(self.manager.add("usb", "8"), key)  # v1.02
        self.assertEqual(len(self.manager.devices), 1)  # v1.02
        self.assertEqual(self.manager.devices[key]["name"], "Lima 1")  # v1.02

    def test_existing_busy_duplicate_is_merged(self):  # v1.02
        data = {"devices": [  # v1.02
            {"id": "usb:COM8", "kind": "usb", "address": "COM8", "name": "Lima", "custom_name": True, "verified": True},  # v1.02
            {"id": "usb:*COM8", "kind": "usb", "address": "*COM8", "name": "*COM8"}],  # v1.02
            "last": "usb:*COM8", "automatic": "usb:*COM8"}  # v1.02
        self.manager.path.write_text(json.dumps(data), encoding="utf8")  # v1.02
        restarted = DeviceManager(self.ctrl, self.folder.name)  # v1.02
        self.assertEqual(list(restarted.devices), ["usb:COM8"])  # v1.02
        self.assertEqual(restarted.devices["usb:COM8"]["name"], "Lima")  # v1.02
        self.assertTrue(restarted.devices["usb:COM8"]["verified"])  # v1.02
        self.assertEqual(restarted.last, "usb:COM8")  # v1.02
        self.assertEqual(restarted.automatic, "usb:COM8")  # v1.02

    def test_port_detection_releases_own_connection_and_schedules_restore(self):  # v1.02
        key = self.manager.add("usb", "COM3")  # v1.02
        self.manager.connect(key)  # v1.02
        self.manager.pause_for_port_detection()  # v1.02
        self.assertFalse(self.ctrl.is_connection_open())  # v1.02
        self.assertTrue(self.manager.active_at_exit)  # v1.02
        self.manager.finish_port_detection()  # v1.02
        generation, target = self.manager.tasks.get_nowait()  # v1.02
        self.assertEqual(target, key)  # v1.02
        self.assertEqual(generation, self.manager.generation)  # v1.02

    def test_successful_upload_supersedes_probe_restore(self):  # v1.02
        key = self.manager.add("usb", "COM3")  # v1.02
        self.manager.connect(key)  # v1.02
        self.manager.pause_for_port_detection()  # v1.02
        self.manager.after_upload("COM8")  # v1.02
        self.manager.finish_port_detection()  # v1.02
        self.assertEqual(self.manager.tasks.get_nowait()[1], "usb:COM8")  # v1.02
        self.assertTrue(self.manager.tasks.empty())  # v1.02

    def test_blink_probe_falls_back_only_for_low_baud_configuration_error(self):  # v1.03
        import ast  # v1.03
        import logging  # v1.03
        import serial  # v1.03
        from unittest.mock import Mock  # v1.03
        source = Path(__file__).parent / "proggen/M07_COM_Port.py"  # v1.03
        function = next(n for n in ast.parse(source.read_text(encoding="utf8")).body if isinstance(n, ast.FunctionDef) and n.name == "_Open_Probe_Port")  # v1.03
        namespace = {"serial": serial, "logging": logging, "_Close_Quiet": lambda ser: ser.close()}  # v1.03
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), "exec"), namespace)  # v1.03
        probe = namespace["_Open_Probe_Port"]  # v1.03
        ser = Mock(baudrate=50)  # v1.03
        ser.open.side_effect = [serial.SerialException("Cannot configure port, something went wrong."), None]  # v1.03
        probe(ser, 50)  # v1.03
        self.assertEqual(ser.baudrate, 9600)  # v1.03
        self.assertEqual(ser.open.call_count, 2)  # v1.03
        ser = Mock(baudrate=115200)  # v1.03
        ser.open.side_effect = serial.SerialException("Access is denied")  # v1.03
        with self.assertRaises(serial.SerialException):  # v1.03
            probe(ser, 115200)  # v1.03
        self.assertEqual(ser.open.call_count, 1)  # v1.03

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
        connection.close.assert_called_once()  # v1.04

    def test_command_guard_allows_usb_subdialog_worker(self):  # v1.05
        completed = threading.Event()  # v1.05
        def operation():  # v1.05
            with self.ctrl._conn_lock:  # v1.05
                completed.set()  # v1.05
        with self.manager.command_guard():  # v1.05
            thread = threading.Thread(target=operation)  # v1.05
            thread.start()  # v1.05
            self.assertTrue(completed.wait(1))  # v1.05
            self.assertFalse(self.manager.commands_idle.is_set())  # v1.05
        thread.join(1)  # v1.05
        self.assertTrue(self.manager.commands_idle.is_set())  # v1.05

    def test_command_guard_pauses_only_background_connections(self):  # v1.05
        key = self.manager.add("usb", "COM3")  # v1.05
        with self.manager.command_guard():  # v1.05
            generation = self.manager.generation  # v1.05
            self.assertFalse(self.manager.connect(key, generation))  # v1.05
            self.assertTrue(self.manager.connect(key))  # v1.05

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
        self.assertEqual(restarted.automatic, "")  # v1.06

    def test_remove_other_device_keeps_current_connection(self):  # v1.06
        active = self.manager.add("usb", "COM3")  # v1.06
        other = self.manager.add("usb", "COM8")  # v1.06
        self.manager.connect(active)  # v1.06
        self.manager.remove(other)  # v1.06
        self.assertTrue(self.ctrl.is_connection_open())  # v1.06
        self.assertEqual(self.manager.last, active)  # v1.06


if __name__ == "__main__":  # v1.00
    unittest.main()  # v1.00
