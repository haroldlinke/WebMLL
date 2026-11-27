# Datei-Version: 1.09 (2026-11-27) - test_monitor_connect.py
# ----------------------------------------------------------------------------------------------
# Name:           test_monitor_connect.py
# Path:           test_monitor_connect.py
# Version:        1.09
# Last Update:    2026-11-26
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.09  2026-11-27  Waehrend einer Konfigurationsuebertragung gehen ~MLLCFG-Zeilen an cfg_lines und nicht in den Serial Monitor (web_serial 1.31)
#   1.08  2026-11-27  Geraete, die das Schreiben blockieren, Unsinn senden oder nur halb antworten, halten das Verbinden nicht auf (web_serial 1.30)
#   1.07  2026-11-27  Serial Monitor testet zuerst schnell (hoechstens 250 ms) auf den EFFECT Mode, sonst DIRECT Mode (web_serial 1.29)
#   1.06  2026-11-27  Verlassen des Monitors auch in Richtung Farb Test, Servo, Sound, DCC, Patterngenerator (webmobaledlib 5.62)
#   1.05  2026-11-27  Der Monitor meldet DIRECT Mode, eine normale Verbindung EFFECT Mode (web_serial 1.28)
#   1.04  2026-11-27  Wechsel vom Seriellen Monitor in den Programm Generator stellt die Verbindung auf das Blatt um (webmobaledlib 5.60)
#   1.03  2026-11-27  Automatisch neu verbinden nach Verlust, nicht nach Trennen durch den Anwender (web_serial 1.27)
#   1.02  2026-11-27  Die Statusanzeige nennt nach dem Verlust Typ und Anschluss (web_serial 1.26)
#   1.01  2026-11-27  Zwei Tests zum Verbindungsverlust (USB abgezogen, web_serial 1.25)
#   1.00  2026-11-26  Neu: Serial Monitor verbindet nur zum Mitlesen (web_serial 1.22, connect_monitor): keine Abfrage am Geraet
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_monitor_connect.py

Prueft mit einer gefaelschten seriellen Schnittstelle, dass der Serial Monitor das Geraet nicht abfragt: es wird nichts gesendet ('#?', '#X'), der Fehlerdialog
'Falsche oder keine Antwort vom Geraet' kommt nicht, auch wenn das Geraet nie antwortet; connect() (zentraler Knopf) fragt dagegen weiter ab."""
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
os.environ["MLL_HEADLESS"] = "1"
os.environ["MLL_DATA_DIR"] = tempfile.mkdtemp(prefix="mll_test_")
sys.path.insert(0, ROOT)
os.chdir(ROOT)


class FakeSerial:
    """Ein Geraet, das nie antwortet (reply leer) oder auf '#?' mit reply antwortet; merkt sich, was ihm gesendet wurde"""
    def __init__(self, reply=b""):
        self.written, self.closed = [], False
        self.reply, self.pending = reply, b""
        self.is_open = True

    @property
    def in_waiting(self):
        return len(self.pending)

    def write(self, data):
        self.written.append(bytes(data))
        if b"#?" in bytes(data):
            self.pending += self.reply
        return len(data)

    def flush(self):
        pass

    def read(self, n=1):
        data, self.pending = self.pending[:n], self.pending[n:]
        return data

    def close(self):
        self.closed = True

    def reset_input_buffer(self):
        pass

    def readline(self):
        return b""


class MonitorConnectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import no_tk
        no_tk.install()
        from headless.headless_app_controller import HeadlessAppController
        import userdata
        cls.ctrl = HeadlessAppController(mainfile_dir=ROOT, command_line_args={"loaddatafile": "True", "logfilename": userdata.log_file()})
        cls.ctrl.create_excel_application()

    def setUp(self):
        c = self.ctrl
        self.fake = FakeSerial()
        self.messages = []
        self.saved = (c._open_serial, c._start_reader, c._msg, c.send_to_ARDUINO, c.send_to_ARDUINO_init_buffer, c._wait_sent)
        c._open_serial = lambda serial, port: self.fake
        c._start_reader = lambda: None
        c._msg = lambda text, title="", *a, **k: self.messages.append((title, text)) or 6
        self.sent = []
        c.send_to_ARDUINO = lambda text, *a, **k: self.sent.append(text)
        c.send_to_ARDUINO_init_buffer = lambda *a, **k: None
        c._wait_sent = lambda *a, **k: None
        c.arduino = None
        c.ARDUINO_current_portname = ""
        self.saved_watch = (c.reconnect_max_wait, c.reconnect_interval, c.reconnect_settle)
        c.reconnect_max_wait = 0                                                 # kein Warten im Hintergrund, ausser ein Test will es
        c.lost_port = ""

    def tearDown(self):
        c = self.ctrl
        (c._open_serial, c._start_reader, c._msg, c.send_to_ARDUINO, c.send_to_ARDUINO_init_buffer, c._wait_sent) = self.saved
        c.arduino = None
        c.ARDUINO_current_portname = ""
        c.reconnect_max_wait, c.reconnect_interval, c.reconnect_settle = self.saved_watch
        c.lost_port = ""

    def test_monitor_connect_without_answer_falls_back_to_direct_mode_quickly(self):
        import time
        start = time.time()
        self.assertTrue(self.ctrl.connect_monitor("COM77"))
        self.assertLess(time.time() - start, 0.6)                                # der Test auf den EFFECT Mode dauert hoechstens 250 ms
        self.assertEqual(self.sent, [])                                          # kein '#X' (nichts erkannt)
        self.assertEqual(self.fake.written, [b"#?\r\n"])                         # nur die eine schnelle Abfrage, keine Wiederholung
        self.assertEqual(self.messages, [])                                      # kein Dialog 'Falsche oder keine Antwort'
        self.assertIn("DIRECT Mode", self.ctrl.connect_status[0])               # Monitor = Direktmodus, nicht EFFECT Mode
        self.assertNotIn("EFFECT Mode", self.ctrl.connect_status[0])
        self.assertTrue(self.ctrl.monitor_connected)                             # fuer das Umstellen beim Verlassen des Monitors
        self.assertEqual(self.ctrl.ARDUINO_current_portname, "COM77")
        text, fg = self.ctrl.connect_status
        self.assertIn("COM77", text)
        self.assertEqual(fg, "green")
        self.assertFalse(getattr(self.ctrl, "monitor_only", False))             # gilt nur fuer diesen Aufruf

    def test_monitor_connect_can_open_error_gives_message(self):
        def fail(serial, port):
            raise OSError("Zugriff verweigert")
        self.ctrl._open_serial = fail
        self.assertFalse(self.ctrl.connect_monitor("COM78"))
        self.assertEqual(len(self.messages), 1)
        self.assertIn("COM78", self.messages[0][1])

    def test_dtr_follows_the_device_at_the_port_not_the_board_of_the_sheet(self):
        from types import SimpleNamespace
        from serial.tools import list_ports
        ports = [SimpleNamespace(device="COM81", vid=0x2E8A, pid=0x000A, description="USB Serial Device", hwid="USB VID:PID=2E8A:000A"),     # Pico
                 SimpleNamespace(device="COM82", vid=0x10C4, pid=0xEA60, description="CP210x", hwid="USB VID:PID=10C4:EA60"),                 # ESP32
                 SimpleNamespace(device="COM83", vid=0x1A86, pid=0x7523, description="USB-SERIAL CH340", hwid="USB VID:PID=1A86:7523"),      # Nano
                 SimpleNamespace(device="COM84", vid=0x9999, pid=0x0001, description="Mystery", hwid="USB VID:PID=9999:0001")]               # unbekannt
        seen = {}

        def open_serial(serial, port):
            seen[port] = self.ctrl._board_needs_dtr()
            return self.fake
        self.ctrl._open_serial = open_serial
        orig = list_ports.comports
        list_ports.comports = lambda *a, **k: ports
        orig_board = self.ctrl.dtr_override
        try:
            for port in ("COM81", "COM82", "COM83", "COM84"):
                self.ctrl.arduino = None
                self.ctrl.ARDUINO_current_portname = ""
                self.assertTrue(self.ctrl.connect_monitor(port))
            self.assertTrue(seen["COM81"])                                       # Pico: DTR an, auch wenn im Blatt ein anderes Board steht
            self.assertFalse(seen["COM82"])                                      # ESP32: DTR aus
            self.assertFalse(seen["COM83"])                                      # Nano: DTR aus
            self.assertEqual(seen["COM84"], self.ctrl._board_needs_dtr())        # unbekannt: Board im Blatt
            self.assertEqual(self.ctrl.dtr_override, orig_board)                 # gilt nur fuer diesen Aufruf
        finally:
            list_ports.comports = orig

    def test_lost_connection_is_detected_when_usb_is_unplugged(self):
        import threading
        self.assertTrue(self.ctrl.connect_monitor("COM76"))
        port = self.fake

        def broken_read(n=1):
            raise OSError("ClearCommError failed: Das Geraet erkennt den Befehl nicht")
        port.read = broken_read
        port.is_open = True
        self.assertTrue(self.ctrl.is_connection_open())
        before = self.ctrl.queue.lines_since(0)[0]
        self.ctrl._reader_loop(port, threading.Event())                         # der Empfangsthread bekommt den Lesefehler
        self.assertFalse(self.ctrl.is_connection_open())                        # Verbindung geschlossen
        self.assertTrue(port.closed)
        self.assertEqual(self.ctrl.connect_status[1], "red")
        self.assertIn("verloren", self.ctrl.connect_status[0].lower())
        import webmobaledlib as W
        label = W.connect_device_label(self.ctrl, False, "COM3")                # Anschluss des Blatts: COM3, verloren ging COM76
        self.assertTrue(label.endswith("COM76"), label)
        shown = W.translate_connect_status(self.ctrl.connectstatus_text, label)
        self.assertTrue(shown.startswith("Verbindung verloren - ") and shown.endswith("COM76"), shown)   # wie 'Nicht verbunden - Pro/COM3'
        seq, lines = self.ctrl.queue.lines_since(before)
        self.assertTrue(any("COM76" in text and "verloren" in text for _t, text in lines), lines)   # Zeile im Serial Monitor

    def test_own_disconnect_is_not_reported_as_lost(self):
        import threading
        self.assertTrue(self.ctrl.connect_monitor("COM75"))
        port = self.fake

        def broken_read(n=1):
            raise OSError("closed")
        port.read = broken_read
        stop = threading.Event()
        stop.set()                                                              # Trennen durch den Anwender setzt zuerst das Stoppzeichen
        self.ctrl._reader_loop(port, stop)
        self.assertTrue(self.ctrl.is_connection_open() or self.ctrl.arduino is port)   # nicht vom Empfangsthread geschlossen
        self.assertNotIn("verloren", str(self.ctrl.connect_status[0]).lower())

    def _lose_connection(self, port_name):
        import threading
        self.assertTrue(self.ctrl.connect_monitor(port_name))
        port = self.fake

        def broken_read(n=1):
            raise OSError("ClearCommError failed")
        port.read = broken_read
        port.is_open = True
        return port

    def test_reconnects_automatically_when_the_port_comes_back(self):
        import threading
        import time
        from types import SimpleNamespace
        from serial.tools import list_ports
        c = self.ctrl
        present = []
        orig = list_ports.comports
        list_ports.comports = lambda *a, **k: [SimpleNamespace(device=d, vid=None, pid=None, description="x", hwid="") for d in present]
        try:
            old = self._lose_connection("COM74")
            c.reconnect_max_wait, c.reconnect_interval, c.reconnect_settle = 10, 0.05, 0.05
            self.fake = FakeSerial()                                             # das neue Geraet nach dem Anstecken
            c._reader_loop(old, threading.Event())                               # Verlust: startet das Warten
            self.assertFalse(c.is_connection_open())
            time.sleep(0.3)
            self.assertFalse(c.is_connection_open())                             # Anschluss fehlt noch: keine Neuverbindung
            present.append("COM74")                                              # USB wieder angesteckt
            for _ in range(60):
                if c.is_connection_open() and c.ARDUINO_current_portname == "COM74":   # der schnelle Test auf den EFFECT Mode dauert bis 250 ms
                    break
                time.sleep(0.1)
            self.assertTrue(c.is_connection_open())
            self.assertEqual(c.ARDUINO_current_portname, "COM74")
            self.assertEqual(c.lost_port, "")
            self.assertEqual(self.sent, [])                                      # Serial Monitor: weiterhin nur mitlesen
            self.assertEqual(self.messages, [])                                  # keine Dialoge im Hintergrund
        finally:
            list_ports.comports = orig
            c.reconnect_max_wait = 0

    def test_no_automatic_reconnect_after_disconnect_by_the_user(self):
        import threading
        import time
        from types import SimpleNamespace
        from serial.tools import list_ports
        c = self.ctrl
        orig = list_ports.comports
        list_ports.comports = lambda *a, **k: [SimpleNamespace(device="COM73", vid=None, pid=None, description="x", hwid="")]
        try:
            old = self._lose_connection("COM73")
            c.reconnect_max_wait, c.reconnect_interval, c.reconnect_settle = 10, 0.3, 0.05
            c._reader_loop(old, threading.Event())
            c.disconnect()                                                       # der Anwender trennt (Knopf Trennen)
            self.assertEqual(c.lost_port, "")
            time.sleep(1.0)
            self.assertFalse(c.is_connection_open())                             # kein Neuverbinden gegen den Willen des Anwenders
        finally:
            list_ports.comports = orig
            c.reconnect_max_wait = 0

    def _assert_direct_quickly(self, port, fake):
        import time
        self.fake = fake
        start = time.time()
        self.assertTrue(self.ctrl.connect_monitor(port))
        took = time.time() - start
        self.assertLess(took, 0.6, "Verbinden dauerte %.2f s" % took)         # spaetestens nach 250 ms im Direktmodus
        self.assertTrue(self.ctrl.monitor_connected)
        self.assertIn("DIRECT Mode", self.ctrl.connect_status[0])
        self.assertEqual(self.ctrl.ARDUINO_current_portname, port)

    def test_device_that_blocks_writing_does_not_hold_up_connecting(self):
        import time

        class Blocking(FakeSerial):
            def write(self, data):
                time.sleep(3)                                                 # das Geraet nimmt nichts an
                return super().write(data)
        self._assert_direct_quickly("COM71", Blocking())

    def test_device_that_floods_garbage_does_not_hold_up_connecting(self):
        class Flood(FakeSerial):
            @property
            def in_waiting(self):
                return 4096                                                   # sendet ununterbrochen Unsinn ohne Zeilenende

            def read(self, n=1):
                return b"x" * n
        self._assert_direct_quickly("COM70", Flood())

    def test_device_with_half_an_answer_does_not_hold_up_connecting(self):
        self._assert_direct_quickly("COM69", FakeSerial(reply=b"#?LEDs_AutoProg V3.5 ohne Zeilenende"))

    def test_device_raising_errors_falls_back_to_direct_mode(self):
        class Raising(FakeSerial):
            @property
            def in_waiting(self):
                raise OSError("Geraet meldet Unsinn")
        self._assert_direct_quickly("COM68", Raising())

    def test_config_lines_go_to_the_transfer_not_to_the_monitor(self):
        import queue
        import threading
        stop = threading.Event()
        data = bytearray(b"Programmmeldung" + bytes([13, 10]) + b"~MLLCFG ACK 100" + bytes([13, 10]) + b"~MLLERR Test" + bytes([13, 10]) + b"danach" + bytes([13, 10]))

        class Port:
            is_open = True
            in_waiting = 0

            def read(self, n=1):
                if not data:
                    stop.set()
                    return b""
                d = bytes(data[:n])
                del data[:n]
                return d
        c = self.ctrl
        c.cfg_lines = queue.Queue()
        before = c.queue.lines_since(0)[0]
        try:
            c._reader_loop(Port(), stop)
            got = []
            while not c.cfg_lines.empty():
                got.append(c.cfg_lines.get_nowait())
        finally:
            c.cfg_lines = None
        self.assertEqual([g.strip() for g in got], ["~MLLCFG ACK 100", "~MLLERR Test"])   # an die Uebertragung
        shown = [text.strip() for _t, text in c.queue.lines_since(before)[1]]
        self.assertIn("Programmmeldung", shown)                                  # alles andere bleibt im Serial Monitor
        self.assertIn("danach", shown)
        self.assertFalse(any("~MLL" in s for s in shown), shown)

    def test_monitor_connect_uses_effect_mode_when_the_device_answers(self):
        self.fake = FakeSerial(reply=b"#?LEDs_AutoProg V3.5 Nano\r\n")
        self.assertTrue(self.ctrl.connect_monitor("COM72"))
        self.assertFalse(self.ctrl.monitor_connected)                            # normale Verbindung
        self.assertIn("EFFECT Mode", self.ctrl.connect_status[0])
        self.assertNotIn("DIRECT Mode", self.ctrl.connect_status[0])
        self.assertIn("#X\r\n", self.sent)                                        # wie beim normalen Verbinden
        self.assertEqual(self.messages, [])
        self.assertEqual(self.ctrl.ARDUINO_current_portname, "COM72")

    def test_leaving_the_monitor_for_a_sheet_resyncs_the_connection(self):
        import webmobaledlib as W
        self.assertTrue(W.monitor_left_for_sheet("mon", "pg"))
        self.assertFalse(W.monitor_left_for_sheet("pg", "mon"))
        for tab in ("farb", "servo1", "servo2", "sound", "dcc", "patt"):
            self.assertTrue(W.monitor_left_for_sheet("mon", tab), tab)
        self.assertFalse(W.monitor_left_for_sheet("mon", "mon"))
        self.assertFalse(W.monitor_left_for_sheet("mon", "z21"))                  # kein serieller Reiter
        self.assertFalse(W.monitor_left_for_sheet("farb", "servo1"))
        self.assertFalse(W.monitor_left_for_sheet("pg", "pg"))

    def test_normal_connect_still_queries_the_device(self):
        import time
        orig_sleep = time.sleep
        time.sleep = lambda s: orig_sleep(min(s, 0.001))                          # den Handshake nicht in Echtzeit abwarten
        try:
            start = time.time()
            ok = self.ctrl.connect("COM79")
        finally:
            time.sleep = orig_sleep
        self.assertFalse(ok)                                                     # das Geraet antwortet nie
        self.assertIn("#?\r\n", self.sent)                                       # der zentrale Weg fragt ab
        self.assertTrue(any("Falsche oder keine Antwort" in m[1] for m in self.messages))


if __name__ == "__main__":
    unittest.main(verbosity=2)
