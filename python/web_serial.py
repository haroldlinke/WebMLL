"""Serielle Verbindung zum Arduino/Pico ohne Tk (Mixin fuer HeadlessAppController).

Entspricht dem, was im Tk-Programm pyMobaLedLib.py (connect, connectIP, disconnect, send_to_ARDUINO,
send_ledcolor_to_ARDUINO, determine_ARDUINO_Properties_from_Startmessage) und SerialMonitorPage.py
(SerialThread/ReadLine) zusammen machen, aber:

  * ohne Tk: Senden und Empfangen laufen in eigenen Threads (statt mit Tk-"after" und einer Queue, die die
    Seite alle 100 ms leert),
  * Empfangene Zeilen landen in RxLog (statt in einer Queue mit maxsize=100, die den Empfangsthread blockiert,
    wenn niemand sie leert),
  * Telnet (WLAN-Pico) laeuft ueber einen einfachen TCP-Port, weil telnetlib ab Python 3.13 fehlt.

Die Methoden und Attribute haben dieselben Namen wie im Original, damit der uebersetzte Code
(M06, M07, M08 ... und die Testtasten) unveraendert darauf zugreifen kann.
"""
from __future__ import annotations

import logging
import queue
import re
import select
import socket
import threading
import time
from collections import deque

logger = logging.getLogger(__name__)


def _const(name: str, default):
    try:
        import mlpyproggen.DefaultConstants as DF
        return getattr(DF, name, default)
    except Exception:                                     # noqa: BLE001
        return default


# ------------------------------------------------------------------------------------------ Empfangspuffer
class RxLog:
    """Ersatz fuer die Queue des Tk-Programms: nimmt Zeilen auf und blockiert nie.

    Die Web-Seite "Serial Monitor" liest mit lines_since(seq) alles, was neu ist."""

    def __init__(self, on_line=None, maxlen: int = 3000):
        self._lines: deque = deque(maxlen=maxlen)
        self._seq = 0
        self._lock = threading.Lock()
        self.on_line = on_line

    def put(self, text, *args, **kwargs):
        text = str(text)
        with self._lock:
            self._seq += 1
            self._lines.append((self._seq, time.time(), text))
        if self.on_line:
            try:
                self.on_line(text)
            except Exception:                             # noqa: BLE001
                logger.debug("on_line fehlgeschlagen", exc_info=True)

    def lines_since(self, seq: int):
        """-> (neue Folgenummer, [(Zeit, Text), ...])"""
        with self._lock:
            new = [(t, s) for (n, t, s) in self._lines if n > seq]
            return self._seq, new

    def qsize(self) -> int:
        return 0

    def clear(self):
        with self._lock:
            self._lines.clear()


# ------------------------------------------------------------------------------------------ TCP statt telnetlib
class TcpPort:
    """Minimaler Ersatz fuer telnetlib.Telnet / serial.Serial bei einer IP-Verbindung (WLAN-Pico)."""

    def __init__(self, host: str, port: int = 23, timeout: float = 5.0):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(2.0)
        self.is_open = True
        self.portstr = host
        self._buf = b""

    @property
    def in_waiting(self) -> int:
        if self._buf:
            return len(self._buf)
        try:
            r, _, _ = select.select([self.sock], [], [], 0)
            return 1 if r else 0
        except Exception:                                 # noqa: BLE001
            return 0

    def write(self, data: bytes):
        self.sock.sendall(data)

    def read(self, n: int = 1) -> bytes:
        if len(self._buf) < n:
            try:
                chunk = self.sock.recv(max(n, 4096))
                if chunk == b"":
                    self.is_open = False
                    raise ConnectionError("Verbindung vom Gegenueber geschlossen")
                self._buf += chunk
            except socket.timeout:
                pass
        data, self._buf = self._buf[:n], self._buf[n:]
        return data

    def read_until(self, expected: bytes = b"\n", timeout: float = 5.0) -> bytes:
        end = time.time() + timeout
        while expected not in self._buf and time.time() < end:
            try:
                chunk = self.sock.recv(4096)
                if chunk == b"":
                    break
                self._buf += chunk
            except socket.timeout:
                continue
        i = self._buf.find(expected)
        if i < 0:
            data, self._buf = self._buf, b""
        else:
            data, self._buf = self._buf[:i + len(expected)], self._buf[i + len(expected):]
        return data

    def flush(self):
        pass

    def close(self):
        self.is_open = False
        try:
            self.sock.close()
        except OSError:
            pass


def list_serial_ports() -> list[tuple[str, str]]:
    """[(Port, Beschreibung)] der angeschlossenen seriellen Geraete."""
    try:
        from serial.tools import list_ports
        return [(p.device, p.description or "") for p in list_ports.comports()]
    except Exception:                                     # noqa: BLE001
        logger.debug("Portliste nicht verfuegbar", exc_info=True)
        return []


# ------------------------------------------------------------------------------------------ Mixin
class SerialMixin:
    def _serial_init(self):
        self.arduino = None
        self.queue = RxLog(on_line=self._on_rx_line)
        self.ARDUINO_IP = False
        self.ARDUINO_current_portname = ""
        self.ARDUINO_status = ""
        self.ARDUINO_version = 0
        self.ARDUINO_boardtype = ""
        self.ARDUINO_has_readbuffer = False
        self.mobaledlib_version = 2
        self.max_ledcnt_list: list = []
        self.max_LEDchannel = 0
        self.LEDchannel = 0
        self.ledhighlight = False
        self.send_active = False
        self.send_error = False
        self.waittime_int = -1
        self.waittime_slowmode = False
        self.serial_port_dict: dict = {}
        self.direct_mode_active = False
        self.detailed_debug_on = False
        self.connection_startup = False
        self.connection_startup_answer = False
        self.connect_status = ("Nicht Verbunden", "black")
        self._tx_queue: queue.Queue = queue.Queue()
        self._tx_thread = None
        self._rx_stop = threading.Event()
        self._rx_thread = None
        self._conn_lock = threading.RLock()

    # ------------------------------------------------------------------ Empfang
    def _on_rx_line(self, text: str):
        """Wie SerialMonitorPage.process_serial: Startmeldung des Arduinos auswerten."""
        t1 = _const("SerialIF_teststring1", "#?LEDs_AutoProg")
        t3 = _const("SerialIF_teststring3", "#?LEDs_AutoProg3")
        if text.startswith(t1) or text.startswith(t3):
            try:
                self.determine_ARDUINO_Properties_from_Startmessage(text)
            except Exception:                             # noqa: BLE001
                logger.debug("Startmeldung nicht auswertbar", exc_info=True)

    def _reader_loop_lines(self, port, stop: threading.Event):
        """Wie TelnetThread: liest zeilenweise (telnetlib.Telnet hat kein read(1))."""
        logger.info("Empfangsthread (Telnet) gestartet (%s)", getattr(port, "portstr", ""))
        while not stop.is_set() and port is not None and getattr(port, "is_open", False):
            try:
                data = port.read_until(b"\n", timeout=2)
            except Exception as ex:                       # noqa: BLE001
                logger.info("Empfangsthread beendet: %s", ex)
                break
            if not data:
                continue
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = str(bytes(data))
            if not text.startswith("****"):
                self.queue.put(text)
        logger.info("Empfangsthread (Telnet) beendet")

    def _reader_loop(self, port, stop: threading.Event):
        """Wie SerialThread/ReadLine: liest Zeilen; Binaernachrichten (Byte >= 0xD0) werden zu JSON:{"RMBUS": ...}."""
        if hasattr(port, "read_until") and not hasattr(port, "in_waiting"):
            return self._reader_loop_lines(port, stop)    # telnetlib.Telnet
        buf = bytearray()
        logger.info("Empfangsthread gestartet (%s)", getattr(port, "portstr", ""))
        while not stop.is_set() and port is not None and getattr(port, "is_open", False):
            try:
                data = port.read(1)
            except Exception as ex:                       # noqa: BLE001
                logger.info("Empfangsthread beendet: %s", ex)
                break
            if not data:
                continue
            if data >= b"\xD0":
                try:
                    chk = int.from_bytes(data, "big")
                    length = int.from_bytes(port.read(1), "big")
                    chk ^= length
                    result = '{"RMBUS": "'
                    for i in range(length):
                        b = port.read(1)
                        chk ^= int.from_bytes(b, "big")
                        if i < length - 1:
                            result += b.hex()
                    result += '"}'
                    if chk != 255:
                        logger.debug("Pruefsummenfehler im Feedback: %s", result)
                    self.queue.put("JSON:" + result)
                except Exception:                         # noqa: BLE001
                    logger.debug("Binaernachricht nicht lesbar", exc_info=True)
                continue
            buf.extend(data)
            if data == b"\n":
                try:
                    text = buf.decode("utf-8")
                except UnicodeDecodeError:
                    text = str(bytes(buf))
                buf.clear()
                if not text.startswith("****"):           # Debugmeldungen des Arduinos
                    self.queue.put(text)
        logger.info("Empfangsthread beendet")

    def _start_reader(self):
        self._stop_reader()
        self._rx_stop = threading.Event()
        self._rx_thread = threading.Thread(target=self._reader_loop, args=(self.arduino, self._rx_stop),
                                           name="serial-rx", daemon=True)
        self._rx_thread.start()

    def _stop_reader(self):
        self._rx_stop.set()
        t = self._rx_thread
        if t is not None and t.is_alive() and t is not threading.current_thread():
            t.join(timeout=3.0)
        self._rx_thread = None

    # ------------------------------------------------------------------ Senden
    def _ensure_tx_thread(self):
        if self._tx_thread is None or not self._tx_thread.is_alive():
            self._tx_thread = threading.Thread(target=self._tx_loop, name="serial-tx", daemon=True)
            self._tx_thread.start()

    def _tx_loop(self):
        """Sendet Zeichen fuer Zeichen mit Pause (waittime_int ms): Waehrend die LEDs aktualisiert werden, sperrt der
        Arduino die Interrupts; es darf dann hoechstens ein Byte ankommen (siehe send_to_ARDUINO im Original)."""
        while True:
            item = self._tx_queue.get()
            if item is None:
                return
            port, message, slowmode = item
            self.send_active = True
            try:
                wait = max(self.waittime_int, 1) / 1000.0
                burst = self.ARDUINO_has_readbuffer and not (self.waittime_slowmode or slowmode)
                for i, c in enumerate(message):
                    if port is None or not getattr(port, "is_open", False):
                        break
                    port.write(c.encode())
                    if burst and c != "\n":
                        continue                          # ESP32/Pico: ganze Zeile ohne Pause
                    if i < len(message) - 1 or not self._tx_queue.empty():
                        time.sleep(wait)
            except Exception as ex:                       # noqa: BLE001
                logger.info("Schreibfehler zum Arduino: %s", ex)
                self.send_error = True
                self.close_arduino_connection_after_write_error()
            finally:
                if self._tx_queue.empty():
                    self.send_active = False

    def send_to_ARDUINO(self, message, arduino=None, comport=None, slowmode=False):
        port = arduino if arduino is not None else self.arduino
        if not port:
            return
        if self.direct_mode_active and str(message).startswith("@"):
            # DCC-Kommandos der Testtasten wirken nur im EFFECT Mode. Ist der Direktmodus (Farbtest) noch aktiv, zuerst beenden.
            logger.info("DCC-Kommando im Direktmodus: Direktmodus wird beendet (#X)")
            self.ARDUINO_end_direct_mode()
        if self.waittime_int == -1:
            self.waittime_int = max(1, round(self.get_maxLEDcnt() * 0.02))      # 20 us pro LED, mind. 1 ms
        logger.debug("send_to_ARDUINO: %r", message)
        self._ensure_tx_thread()
        self.send_active = True
        self._tx_queue.put((port, str(message), slowmode))

    def send_to_ARDUINO_init_buffer(self, immediatly=False):
        while not self._tx_queue.empty():
            try:
                self._tx_queue.get_nowait()
            except queue.Empty:
                break
        self.send_active = False
        return True

    def _wait_sent(self, timeout=3.0):
        end = time.time() + timeout
        while (not self._tx_queue.empty() or self.send_active) and time.time() < end:
            time.sleep(0.01)

    # ------------------------------------------------------------------ Meldungen
    def _msg(self, text: str, title: str, kind: int = 16):
        try:
            import ExcelAPI.XLA_Application as X02
            return X02.MsgBox(text, kind, title)
        except Exception:                                 # noqa: BLE001
            logger.info("%s: %s", title, text)
            return None

    # ------------------------------------------------------------------ Eigenschaften des Arduinos
    def determine_ARDUINO_Properties_from_Startmessage(self, startmessage):
        """Startmeldung z. B.: LEDs_AutoProg Ver 4: Type-3.3.2F5 FastLED 3.9.12 25.03.25 11:39,<LEDs je Kanal>"""
        self.ARDUINO_version = 0
        m = re.search(r"Ver (\d+):", startmessage)
        version_number = int(m.group(1)) if m else None
        self.ARDUINO_version = version_number if version_number else 2
        self.ARDUINO_boardtype = ""
        if version_number and version_number >= 3:
            t = re.search(r": (.+?) ", startmessage)
            self.ARDUINO_boardtype = t.group(1) if t else ""
        self.mobaledlib_version = self.ARDUINO_version
        self.ARDUINO_boardtype = ""                       # wie im Original (der Typ wird dort wieder geloescht)
        self.ARDUINO_has_readbuffer = self.ARDUINO_boardtype in ("ESP32", "Pico")
        parts = startmessage.split(",")
        self.max_ledcnt_list = [p.strip() for p in parts[1:]]
        self.max_LEDchannel = len(self.max_ledcnt_list)
        self.LEDchannel = 0
        total = 20
        if self.max_LEDchannel:
            try:
                total = sum(int(x) for x in self.max_ledcnt_list)
            except ValueError:
                total = 20
        self.set_maxLEDcnt(total)
        self.waittime_int = -1                            # Pause zwischen den Bytes haengt von der LED-Anzahl ab

    def set_maxLEDcnt(self, maxLEDcnt):
        self.maxLEDcnt = maxLEDcnt
        try:
            self.setConfigData("maxLEDcount", maxLEDcnt)
        except Exception:                                 # noqa: BLE001
            logger.debug("maxLEDcount nicht speicherbar", exc_info=True)

    def get_maxLEDcnt(self):
        if getattr(self, "maxLEDcnt", None):
            return int(self.maxLEDcnt)
        try:
            return int(self.getConfigData("maxLEDcount"))
        except (TypeError, ValueError):
            return 20

    def get_lednum_offset_for_channel(self, channel):
        offset = 0
        try:
            if channel < len(self.max_ledcnt_list):
                for i in range(channel):
                    offset += int(self.max_ledcnt_list[i])
        except BaseException as err:                      # noqa: BLE001
            logger.error(err, exc_info=True)
        return offset

    # ------------------------------------------------------------------ LED-Kommandos
    def led_off(self, _event=None):
        self.ledhighlight = False
        self.send_to_ARDUINO("#L00 00 00 00 FF\n" if self.mobaledlib_version == 1 else "#L 00 00 00 00 7FFF\n")

    SwitchoffallLEDs = led_off

    def send_ledcolor_to_ARDUINO(self, lednum, ledcount, ledcolor, ledchannel=0):
        lednum_int = int(lednum)
        if ledchannel != 0:
            lednum_int += self.get_lednum_offset_for_channel(ledchannel)
        message = "#L" if self.mobaledlib_version == 1 else "#L "
        message += ("{:04x}".format(lednum_int) + " " + ledcolor[1:3] + " " + ledcolor[3:5] + " " + ledcolor[5:7]
                    + " " + "{:03x}".format(ledcount) + "\n")
        self.send_to_ARDUINO(message)
        time.sleep(_const("ARDUINO_WAITTIME", 0.02))

    def send_command_to_ARDUINO(self, command):
        self.connect_if_not_connected()
        for c in command:
            self.send_to_ARDUINO(c)
        self.send_to_ARDUINO(chr(10))

    # ------------------------------------------------------------------ Direktmodus (Farbtest, Servo-Test ...)
    def ARDUINO_begin_direct_mode(self):
        logger.info("Direktmodus starten (verbunden: %s)", self.is_connection_open())
        self.direct_mode_active = True
        if self.is_connection_open():
            self.send_active = False
            self._set_connect_status("Verbunden " + self.ARDUINO_current_portname + " - DIRECT Mode", "green")
            self.send_to_ARDUINO("#BEGIN\n" if self.mobaledlib_version == 1 else "#?\n")
            time.sleep(_const("ARDUINO_WAITTIME", 0.02))
            self.led_off()

    def ARDUINO_end_direct_mode(self):
        logger.info("Direktmodus beenden (verbunden: %s)", self.is_connection_open())
        self.direct_mode_active = False
        if self.is_connection_open():
            self.send_active = False
            self.led_off()
            self._set_connect_status("Verbunden " + self.ARDUINO_current_portname + " - EFFECT Mode", "green")
            self.send_to_ARDUINO("#END\n" if self.mobaledlib_version == 1 else "#X\n")

    # ------------------------------------------------------------------ Verbinden
    def is_connection_open(self):
        return bool(self.arduino and getattr(self.arduino, "is_open", False))

    def connect_if_not_connected(self, port=None):
        if self.is_connection_open():
            return True
        return self.connect(port=port)

    def _set_connect_status(self, text, fg="black"):
        self.connect_status = (text, fg)
        self.set_connectstatusmessage(text, fg=fg)

    def _fail_connect(self):
        self.arduino = None
        self.ARDUINO_status = ""
        self.ARDUINO_current_portname = ""
        self._set_connect_status("Nicht Verbunden", "black")
        return False

    def connect(self, port=None):
        with self._conn_lock:
            return self._connect(port)

    def _connect(self, port=None):
        self.ARDUINO_IP = False
        if port is None:
            port = self.getConfigData("serportname")
        port = str(port or "")                         # kann eine Zelle (CRange) sein
        if port.isdigit():
            port = "COM" + port                        # wie F00.port_check_format
        if port.startswith("IP:"):
            return self.connectIP(IPAdresse=port[3:])
        logger.info("connect %s", port)
        if self.is_connection_open():
            self.disconnect()
        if port == "" or port.upper() == "NO DEVICE":
            self._msg("Es ist kein Port ausgewählt.", "Verbinden")
            return self._fail_connect()
        self._set_connect_status("Versuch sich mit dem ARDUINO am Port " + port + " zu verbinden ...", "red")
        try:
            import serial
            self.ARDUINO_status = "Connecting"
            self.arduino = serial.Serial(port, baudrate=115200, timeout=2, parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        except BaseException as e:                        # noqa: BLE001
            logger.info("Port %s nicht zu oeffnen: %s", port, e)
            macro = self.MacroDef.data.get("StartPage", {}) if getattr(self, "MacroDef", None) else {}
            title = macro.get("connect_open_error_title", "Fehler beim Öffnen des Ports")
            text = macro.get("msg_connect_open_error", "Der Port {} konnte nicht geöffnet werden.").format(port)
            answer = self._msg(text, title, 3 + 32)       # vbYesNoCancel + vbQuestion
            self._fail_connect()
            if answer == 6:                               # Ja: anderen Port waehlen
                try:
                    import proggen.M07_COM_Port_New as M07New
                    import proggen.M25_Columns as M25
                    res, new_port = M07New.Show_USB_Port_Dialog(M25.COMPort_COL, " ")
                    if res:
                        return self._connect(new_port)
                except Exception:                         # noqa: BLE001
                    logger.info("Portauswahl nicht moeglich", exc_info=True)
            return False

        time.sleep(1)
        self.send_to_ARDUINO_init_buffer(immediatly=True)
        try:
            self.arduino.flush()
        except Exception:                                 # noqa: BLE001
            pass
        self.send_to_ARDUINO("#?\r\n")
        self._wait_sent(2.0)
        txt, read_error = "", False
        t1 = _const("SerialIF_teststring1", "#?LEDs_AutoProg")
        trials, start = 0, time.time()
        while True:                                       # wie im Original: bis zu 3 neue Anfragen im Sekundentakt
            if self.arduino.in_waiting > 0:
                while "\n" in txt:
                    txt = txt.split("\n")[-1]
                txt += self.arduino.read(self.arduino.in_waiting).decode(errors="ignore")
                pos = txt.find(t1)
                if pos != -1:
                    pos2 = txt.find("\r\n", pos)
                    if pos2 != -1:
                        txt = txt[pos + 2:pos2]
                        self.queue.put(txt)
                        self.determine_ARDUINO_Properties_from_Startmessage(txt)
                        break
            if time.time() - start >= 1:
                trials += 1
                if trials > 3:
                    read_error = True
                    break
                start = time.time()
                self.arduino.write(b"#?\n")
            time.sleep(0.01)
        self.send_to_ARDUINO("#X\r\n")
        if read_error:
            self._msg("Falsche oder keine Antwort vom ARDUINO.\n\nPrüfe, ob das richtige MobaLedLib-Programm auf den "
                      "Arduino geladen ist. Es muss mit dem Compilerschalter\n  #define RECEIVE_LED_COLOR_PER_RS232\n"
                      "übersetzt sein. Das Programm kann mit dem Knopf 'Z. Arduino schicken' geladen werden.",
                      "Fehler beim Lesen der Antwort des ARDUINO")
            try:
                self.arduino.close()
            except Exception:                             # noqa: BLE001
                pass
            return self._fail_connect()
        self.ARDUINO_current_portname = port
        self.ARDUINO_status = "Connected"
        self._set_connect_status("Verbunden mit " + port + " - EFFECT Mode", "green")
        self._start_reader()
        return True

    def connectIP(self, IPAdresse=None):
        """Verbindung zu einem WLAN-Pico (Telnet-Port 23)."""
        if not IPAdresse:
            return False
        self._set_connect_status("Versuch sich mit dem PICO- IP: " + IPAdresse + " zu verbinden ...", "red")
        t1 = _const("SerialIF_teststring1", "#?LEDs_AutoProg")
        t3 = _const("SerialIF_teststring3", "#?LEDs_AutoProg3")
        try:
            try:                                           # telnetlib (bis Python 3.12, danach als Paket telnetlib-313-and-up)
                import telnetlib
                self.arduino = telnetlib.Telnet(IPAdresse, 23, timeout=5)
                self.arduino.is_open = True
                self.arduino.portstr = IPAdresse
            except ImportError:
                self.arduino = TcpPort(IPAdresse, 23, timeout=5)   # einfacher Ersatz ohne Telnet-Aushandlung
            self.arduino.write(b"#?\n")
            txt = self.arduino.read_until(b"\n", 5).decode(errors="ignore")
            pos = txt.find(t1)
            pos = pos + 2 if pos != -1 else txt.find(t3)
            pos2 = txt.find("\n", pos) if pos != -1 else -1
            if pos == -1 or pos2 == -1:
                raise ConnectionError("keine gueltige Antwort: " + txt[:60])
            txt = txt[pos:pos2]
            self.ARDUINO_IP = True
            self.queue.put(txt)
            self.determine_ARDUINO_Properties_from_Startmessage(txt)
            self.ARDUINO_current_portname = IPAdresse
            self.ARDUINO_status = "Connected"
            self._set_connect_status("Verbunden mit " + IPAdresse + " - EFFECT Mode", "green")
            self._start_reader()
            self.send_to_ARDUINO("#X\r\n")
            return True
        except BaseException as e:                        # noqa: BLE001
            logger.info("ConnectIP: Fehler %s", e)
            try:
                if self.arduino:
                    self.arduino.close()
            except Exception:                             # noqa: BLE001
                pass
            return self._fail_connect()

    def disconnect(self):
        with self._conn_lock:
            if self.arduino:
                try:
                    self.led_off()
                    self.send_to_ARDUINO("#X\n")
                    self._wait_sent(3.0)
                    time.sleep(10 * _const("ARDUINO_WAITTIME", 0.02))
                except Exception:                         # noqa: BLE001
                    logger.debug("Fehler beim Trennen", exc_info=True)
                self._stop_reader()
                try:
                    logger.info("close ARDUINO port %s", getattr(self.arduino, "portstr", ""))
                    self.arduino.close()
                except Exception:                         # noqa: BLE001
                    pass
                self.arduino = None
                self.ARDUINO_current_portname = ""
                self.ARDUINO_status = ""
                self.send_active = False
            self._set_connect_status("Nicht Verbunden", "black")

    def close_arduino_connection_after_write_error(self):
        self._stop_reader()
        try:
            if self.arduino:
                self.arduino.close()
        except Exception:                                 # noqa: BLE001
            pass
        self.arduino = None
        self.ARDUINO_current_portname = ""
        self.ARDUINO_status = ""
        self.send_active = False
        self._set_connect_status("Nicht Verbunden", "black")
