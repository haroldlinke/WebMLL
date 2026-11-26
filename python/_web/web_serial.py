# Datei-Version: 1.20 (2026-11-26) - web_serial.py
# ----------------------------------------------------------------------------------------------
# Name:           web_serial.py
# Path:           _web/web_serial.py
# Version:        1.20
# Last Update:    2026-11-26
# Author:         Harold Linke, Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-12  Serielle Verbindung ohne Tk (Original, nicht erfasst)
#   1.01  2026-10-20  send_to_ARDUINO_servo (Seite Servo Test 1): eigene Pause je Zeichen, Sendeschleife kennt eine Pause je Nachricht
#   1.02  2026-10-20  tx_idle (Keep-Alive der Seite Servo Test nur bei leerer Sendewarteschlange)
#   1.03  2026-10-21  rx_listeners: Funktionen, die jede Zeile vom Arduino bekommen (Rueckmeldung des Z21 Simulators)
#   1.04  2026-10-26  Zusammengesetzte Meldungen (Verkettungen und f-Strings) mit tr(...) uebersetzbar gemacht
#   1.05  2026-11-09  Der Verbindungsstatus wird uebersetzt (Nicht Verbunden, Verbunden <Port> - DIRECT/EFFECT Mode)
#   1.06  2026-11-13  Mit ARDUINO verbinden: DTR und RTS werden vor dem Oeffnen ausgeschaltet (der Nano wurde beim Verbinden zurueckgesetzt: das verzoegerte den Verbindungsaufbau und unterbrach die Anlagensteuerung); der Pico behaelt DTR und RTS an (Excel: 'pico serial USB port needs DTR to be on'); _open_serial, _board_needs_dtr
#   1.07  2026-11-14  ESP32: Verbindung ueber WLAN mit Anmeldung per HMAC (Port 2323, connect_esp32); Schreibfehler schliesst nur die eigene Verbindung (Beitrag des Fork-Entwicklers)
#   1.08  2026-11-14  TcpPort: ungueltiger Hostname (UnicodeError, "label too long") wird als OSError gemeldet statt abzustuerzen
#   1.09  2026-11-14  Automatisches Verbinden (ohne Anschlussangabe): ist fuer das Blatt eine ESP32-WLAN-Verbindung eingetragen (wifi_target_provider), wird zuerst WLAN versucht, sonst USB; connect(wlan=False) erzwingt USB
#   1.10  2026-11-14  connect_if_not_connected (Testtasten, DCC-Tastatur, Z21 ...) versucht auch mit Anschlussangabe zuerst die eingetragene ESP32-WLAN-Verbindung
#   1.11  2026-11-16  Protokoll: Zeilen der Lichtmaschine (Empfang) werden mit Level DEBUG protokolliert, die Startmeldung mit der Auswertung (LEDs je Kanal, Summe, Version) mit Level INFO
#   1.12  2026-11-19  Stilles Verbinden (quiet): keine Dialoge bei Fehlern (Automatisch verbinden beim Start und nach dem Hochladen); dtr_override fuer einen gefundenen Pico (Issue 20)
#   1.14  2026-11-23  Issue 59: Verbinden ohne Anschlussangabe nimmt den Anschluss des aktiven Blatts (sheet_port_provider) vor der globalen Einstellung serportname
#   1.15  2026-11-25  Titel der Meldung beim Verbindungsfehler: 'Fehler beim Öffnen der Verbindung' (statt 'des Ports'), jetzt uebersetzt. Zeilen mit '# v1.15'
#   1.13  2026-11-21  Option LedOffOnDisconnect (Programm Einstellungen): Beim Trennen werden die LEDs nur noch ausgeschaltet, wenn die Option gesetzt ist (Vorgabe aus; vorher immer)
#   1.16  2026-11-25  Texte: Gerät statt ARDUINO (Verbindungsstatus, Meldung bei falscher oder fehlender Antwort). Zeilen mit '# v1.16'
#   1.17  2026-11-25  Stilles Verbinden waehrend des offenen Dialogs Geraeteauswahl wird uebersprungen; Trennung der Verbindung waehrend des Verbindens (self.arduino None) ergibt keinen Traceback mehr. Zeilen mit '# v1.17'
#   1.20  2026-11-26  Eine Verbindung pro Geraet: PORT_ACCESS_LOCK (Oeffnen und Handshake eines Anschlusses sind exklusiv, auch gegenueber den Abfragen der Geraeteauswahl), Reihenfolge der Sperren _conn_lock vor PORT_ACCESS_LOCK; eine offene Verbindung zum selben Anschluss oder ESP32 wird wiederverwendet (USB, WLAN, connect, connect_esp32, connectIP); connect_if_not_connected wartet auf einen laufenden Verbindungsaufbau; connect_silent (quiet und dtr_override nur unter der Sperre, eine offene Verbindung bleibt); close_arduino_connection_after_write_error unter _conn_lock. Zeilen mit '# v1.20'
#   1.19  2026-11-26  Startmeldung wird pro Verbindung nur einmal ausgewertet; die zweite Auswertung protokolliert den Aufrufer (Zeilen mit '# v1.19')
#   1.18  2026-11-25  ARDUINO_startmessage: Startmeldung ('LEDs_AutoProg Ver 3: ...') der aktiven Verbindung, die Geraeteauswahl wertet sie fuer die Versionsanzeige des Nano aus. Zeilen mit '# v1.18'
# ----------------------------------------------------------------------------------------------
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
import hmac
import threading
import time
from collections import deque
try:  # v1.04
    from _web.web_i18n import tr  # v1.04
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v1.04
    def tr(text, **values):  # v1.04
        return text.format(**values) if values else text  # v1.04

logger = logging.getLogger(__name__)

# v1.20: Ein Zugriff auf einen seriellen Anschluss gleichzeitig: Verbinden (Oeffnen und Handshake), Abfragen der Geraeteauswahl (Typ, Version, MLLIDENT, Bootloader) und die Erkennung
# (DetectArduino, Get_Arduino_Baudrate). Reihenfolge der Sperren immer: SerialMixin._conn_lock, dann PORT_ACCESS_LOCK, dann M07._DETECT_LOCK. Wiedereintrittsfaehig (RLock).
PORT_ACCESS_LOCK = threading.RLock()  # v1.20


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
        try:
            self.sock = socket.create_connection((host, port), timeout=timeout)
        except UnicodeError as error:  # v1.08: Adresse mit zu langem Namensteil ("label too long") wie ein Verbindungsfehler behandeln
            raise OSError("Ungültiger Hostname.") from error
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
        self.rx_listeners: list = []                    # Funktionen text -> None, die jede Zeile vom Arduino bekommen (zum Beispiel der Z21 Simulator fuer die Rueckmeldung)  # v1.03
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
        for listener in list(getattr(self, "rx_listeners", ())):               # Zuhoerer (Z21 Simulator: JSON:{"RMBUS": ...}); ein Fehler darin stoert den Empfang nicht  # v1.03
            try:  # v1.03
                listener(text)  # v1.03
            except Exception:                             # noqa: BLE001  # v1.03
                logger.debug("Zuhoerer der Empfangszeile fehlgeschlagen", exc_info=True)  # v1.03
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
            logger.debug("Lichtmaschine: %r", text)  # v1.11
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
                if isinstance(port, TcpPort) and not stop.is_set() and self.arduino is port:
                    self.close_arduino_connection_after_write_error(expected_port=port)
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
                logger.debug("Lichtmaschine: %r", text)  # v1.11
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
            port, message, slowmode = item[:3]  # v1.01
            wait_override = item[3] if len(item) > 3 else None                       # Servo-Nachrichten: eigene Pause (send_to_ARDUINO_servo)  # v1.01
            self.send_active = True
            try:
                wait = wait_override if wait_override is not None else max(self.waittime_int, 1) / 1000.0  # v1.01
                burst = self.ARDUINO_has_readbuffer and not (self.waittime_slowmode or slowmode)
                if isinstance(port, TcpPort) and not (self.waittime_slowmode or slowmode or wait_override is not None):
                    if port.is_open:
                        port.write(message.encode())
                    continue
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
                self.close_arduino_connection_after_write_error(expected_port=port)
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

    def send_to_ARDUINO_servo(self, message, arduino=None, comport=None):  # v1.01
        """Wie send_to_ARDUINO_servo im Original (pyMobaLedLib.py): Zeichen fuer Zeichen mit der Pause maxLEDcnt * 0,2 ms (zehnmal laenger als bei Farben, die Servoplatine braucht
        mehr Zeit). Die Pause von einer Sekunde nach jeder Nachricht entfaellt: Das Original blockierte damit die Oberflaeche, hier sorgt der Sendepuffer fuer die Reihenfolge."""
        port = arduino if arduino is not None else self.arduino  # v1.01
        if not port:  # v1.01
            return  # v1.01
        wait = max(self.get_maxLEDcnt() * 0.0002, 0.001)  # v1.01
        logger.debug("send_to_ARDUINO_servo: %r", message)  # v1.01
        self._ensure_tx_thread()  # v1.01
        self.send_active = True  # v1.01
        self._tx_queue.put((port, str(message), True, wait))  # v1.01

    def tx_idle(self):  # v1.02
        """Ist nichts mehr zu senden (Warteschlange leer, kein Senden aktiv)? Die Seite Servo Test schickt das Keep-Alive nur dann."""  # v1.02
        return self._tx_queue.empty() and not self.send_active  # v1.02

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
    quiet = False  # v1.12: stilles Verbinden (automatisch beim Start oder nach dem Hochladen): Fehler nur ins Protokoll, kein Dialog
    dtr_override = None  # v1.12: True/False ueberschreibt _board_needs_dtr (zum Beispiel ein beim Start gefundener Pico, obwohl ein anderes Board eingestellt ist)

    def _msg(self, text: str, title: str, kind: int = 16):
        if self.quiet:  # v1.12
            logger.info("Stilles Verbinden, Meldung unterdrueckt: %s: %s", title, text)  # v1.12
            return None  # v1.12
        try:
            import ExcelAPI.XLA_Application as X02
            return X02.MsgBox(text, kind, title)
        except Exception:                                 # noqa: BLE001
            logger.info("%s: %s", title, text)
            return None

    # ------------------------------------------------------------------ Eigenschaften des Arduinos
    def determine_ARDUINO_Properties_from_Startmessage(self, startmessage):
        """Startmeldung z. B.: LEDs_AutoProg Ver 4: Type-3.3.2F5 FastLED 3.9.12 25.03.25 11:39,<LEDs je Kanal>"""
        key = str(startmessage or "").strip()  # v1.19
        if key and key == getattr(self, "_evaluated_startmsg", None):  # v1.19: dieselbe Meldung noch einmal (zweiter Aufruf in dieser Verbindung)
            return  # v1.19, v1.20: Ursache: der Handshake legt die Meldung in self.queue (RxLog.on_line -> _on_rx_line wertet sie schon aus, SerialIF_teststring3 = 'LEDs_AutoProg') und ruft danach selbst auf
        self._evaluated_startmsg = key  # v1.19
        self.ARDUINO_version = 0
        self.ARDUINO_startmessage = str(startmessage or "")  # v1.18: fuer die Geraeteauswahl (Version der MobaLedLib-Bibliothek)
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
        logger.info("Startmeldung der Lichtmaschine: %r -> Version %s, LEDs je Kanal %s, Summe %s (hoechste LED-Nummer %s)",  # v1.11
                    startmessage.strip(), self.ARDUINO_version, self.max_ledcnt_list, total, total - 1)  # v1.11
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
            # self._set_connect_status("Verbunden " + self.ARDUINO_current_portname + " - DIRECT Mode", "green")  # v1.05 (entfallen)
            self._set_connect_status(tr("Verbunden") + " " + self.ARDUINO_current_portname + " - DIRECT Mode", "green")  # v1.05
            self.send_to_ARDUINO("#BEGIN\n" if self.mobaledlib_version == 1 else "#?\n")
            time.sleep(_const("ARDUINO_WAITTIME", 0.02))
            self.led_off()

    def ARDUINO_end_direct_mode(self):
        logger.info("Direktmodus beenden (verbunden: %s)", self.is_connection_open())
        self.direct_mode_active = False
        if self.is_connection_open():
            self.send_active = False
            self.led_off()
            # self._set_connect_status("Verbunden " + self.ARDUINO_current_portname + " - EFFECT Mode", "green")  # v1.05 (entfallen)
            self._set_connect_status(tr("Verbunden") + " " + self.ARDUINO_current_portname + " - EFFECT Mode", "green")  # v1.05
            self.send_to_ARDUINO("#END\n" if self.mobaledlib_version == 1 else "#X\n")

    # ------------------------------------------------------------------ Verbinden
    def is_connection_open(self):
        return bool(self.arduino and getattr(self.arduino, "is_open", False))

    def _board_needs_dtr(self) -> bool:  # v1.06
        if self.dtr_override is not None:  # v1.12
            return bool(self.dtr_override)  # v1.12
        """Braucht der Anschluss DTR (und RTS) an? Nur der Pico: sein serieller USB-Anschluss sendet nur mit DTR (Excel-Programm M07_COM_Port: 'pico serial USB port needs DTR to be on').
        Alle anderen (Nano, Uno, ESP32) werden von DTR zurueckgesetzt. Unbekannter Typ: wie bisher (an)."""  # v1.06
        try:  # v1.06
            import proggen.M02_Public as M02  # v1.06
            import proggen.M02a_Public as M02a  # v1.06
            return M02a.Get_BoardTyp() == M02.HT_PICO  # v1.06
        except Exception:                                          # noqa: BLE001  # v1.06
            logger.debug("Board-Typ unbekannt: DTR bleibt an", exc_info=True)  # v1.06
            return True  # v1.06

    def _open_serial(self, serial_module, port):  # v1.06
        """Serielle Verbindung oeffnen: erst die Eigenschaften setzen, DTR und RTS (ausser beim Pico) AUSschalten, dann open(). Beim klassischen serial.Serial(port, ...) steigt DTR
        beim Oeffnen und setzt den Nano zurueck (Rueckmeldung des Excel-Entwicklers: Verbinden loest einen Reset aus, das verzoegert den Aufbau und unterbricht die Anlagensteuerung)."""  # v1.06
        ser = serial_module.Serial()  # v1.06: ohne Port, noch nicht geoeffnet
        ser.port = port  # v1.06
        ser.baudrate = 115200  # v1.06
        ser.timeout = 2  # v1.06
        ser.parity = serial_module.PARITY_NONE  # v1.06
        ser.stopbits = serial_module.STOPBITS_ONE  # v1.06
        ser.bytesize = serial_module.EIGHTBITS  # v1.06
        if not self._board_needs_dtr():  # v1.06
            ser.dtr = False  # v1.06
            ser.rts = False  # v1.06
        ser.open()  # v1.06
        return ser  # v1.06

    def connect_if_not_connected(self, port=None):
        with self._conn_lock:  # v1.20: ein laufender Verbindungsaufbau (self.arduino ist schon gesetzt, der Handshake laeuft noch) wird abgewartet, nicht mitbenutzt
            if self.is_connection_open():
                return True
            return self.connect(port=port, wlan=True)  # v1.10: auch mit Anschlussangabe (Testtasten) zuerst die eingetragene WLAN-Verbindung

    def _set_connect_status(self, text, fg="black"):
        text = tr(text)  # v1.05: feste Texte wie 'Nicht Verbunden' in der eingestellten Sprache (zusammengesetzte Texte sind schon uebersetzt oder bleiben)
        self.connect_status = (text, fg)
        self.set_connectstatusmessage(text, fg=fg)

    def _fail_connect(self):
        self.arduino = None
        self.ARDUINO_status = ""
        self.ARDUINO_current_portname = ""
        self._set_connect_status("Nicht Verbunden", "black")
        return False

    sheet_port_provider = None  # v1.14 (Issue 59): Funktion ohne Argument, liefert den USB-Anschluss des aktiven Blatts (oder None): hat Vorrang vor der globalen Einstellung serportname

    wifi_target_provider = None  # v1.09: Funktion ohne Argument, liefert (Adresse, Passwort) der eingetragenen ESP32-WLAN-Verbindung des aktiven Blatts oder None (setzt webmobaledlib.py)

    def connect(self, port=None, wlan=None):
        """wlan=None: ohne Anschlussangabe zuerst die eingetragene ESP32-WLAN-Verbindung versuchen, dann USB; wlan=False: nur USB."""  # v1.09
        with self._conn_lock:
            if (port is None or wlan) and wlan is not False and self.wifi_target_provider is not None:  # v1.09/v1.10
                try:
                    target = self.wifi_target_provider()
                except Exception:                                  # noqa: BLE001
                    logger.debug("wifi_target_provider fehlgeschlagen", exc_info=True)
                    target = None
                if target:
                    if self._is_connected_to(target[0], via_ip=True):  # v1.20: schon mit diesem ESP32 verbunden: nicht trennen und neu verbinden
                        logger.info("Verbindung zu %s besteht schon, sie wird wiederverwendet", target[0])  # v1.20
                        return True  # v1.20
                    if self.arduino:
                        self.disconnect()
                    logger.info("connect: zuerst WLAN %s", target[0])
                    if self.connectIP(target[0], esp32_password=target[1]) and self.is_connection_open():
                        return True
                    logger.info("connect: WLAN %s nicht erreichbar, weiter mit USB", target[0])
            return self._connect(port)

    def _connect(self, port=None):
        # self.ARDUINO_IP = False  # v1.20 (entfallen: erst nach der Pruefung auf eine bestehende Verbindung, sonst erkennt _is_connected_to eine offene WLAN-Verbindung nicht)
        if port is None and self.sheet_port_provider is not None:  # v1.14 (Issue 59): Anschluss des aktiven Blatts
            try:  # v1.14
                port = self.sheet_port_provider() or None  # v1.14
            except Exception:                                      # noqa: BLE001  # v1.14
                logger.debug("sheet_port_provider fehlgeschlagen", exc_info=True)  # v1.14
                port = None  # v1.14
        if port is None:
            port = self.getConfigData("serportname")
        port = str(port or "")                         # kann eine Zelle (CRange) sein
        if port.isdigit():
            port = "COM" + port                        # wie F00.port_check_format
        if port.startswith("IP:"):
            ok = self.connectIP(IPAdresse=port[3:])  # v1.20
            if not ok:  # v1.20: wie bisher bleibt ARDUINO_IP nach einem Fehlschlag aus
                self.ARDUINO_IP = False  # v1.20
            return ok  # v1.20
        try:  # v1.20: wer verbindet (Aufrufer von connect)
            import sys as _sys  # v1.19
            _c = _sys._getframe(2)  # v1.20
            logger.info("connect %s (von %s:%s %s)", port, _c.f_code.co_filename.split("\\")[-1].split("/")[-1], _c.f_lineno, _c.f_code.co_name)  # v1.19, v1.20
        except ValueError:  # v1.20
            logger.info("connect %s", port)  # v1.20
        try:  # v1.17: der Dialog Geraeteauswahl belegt die Anschluesse (Ident, Abfrage von Typ und Version): stilles Verbinden jetzt nicht
            import proggen.M07_COM_Port_New as _M07Dlg
            if getattr(self, "quiet", False) and getattr(_M07Dlg, "Device_Dialog_Open", False):
                logger.info("Stilles Verbinden mit %s uebersprungen: der Dialog Geraeteauswahl ist offen", port)
                return False
        except Exception:                                  # noqa: BLE001
            logger.debug("Dialog-Zustand nicht lesbar", exc_info=True)
        if self._is_connected_to(port):  # v1.19, v1.20: schon offen am selben Anschluss: wiederverwenden, nicht neu oeffnen (Reset)
            logger.info("Verbindung zu %s besteht schon, sie wird wiederverwendet", port)  # v1.19
            return True  # v1.19
        self.ARDUINO_IP = False  # v1.20 (stand vorher am Anfang von _connect)
        if self.is_connection_open():
            self.disconnect()
        if port == "" or port.upper() == "NO DEVICE":
            self._msg("Es ist kein Port ausgewählt.", "Verbinden")
            return self._fail_connect()
        # self._set_connect_status("Versuch sich mit dem ARDUINO am Port " + port + " zu verbinden ...", "red")  # v1.04 (entfallen)
        # self._set_connect_status(tr('Versuch sich mit dem ARDUINO am Port ') + port + " zu verbinden ...", "red")  # v1.04  # v1.16 (entfallen)
        self._set_connect_status(tr('Versuch sich mit dem Gerät am Port ') + port + " zu verbinden ...", "red")  # v1.16: Gerät statt ARDUINO
        status, err = self._open_and_handshake(port)  # v1.20: Oeffnen und Handshake exklusiv (PORT_ACCESS_LOCK)
        if status == "ok":  # v1.20
            return True  # v1.20
        if status == "open_error":  # v1.20: Fehlerdialog AUSSERHALB der Sperre (der Dialog Geraeteauswahl braucht sie fuer seine Abfragen)
            macro = self.MacroDef.data.get("StartPage", {}) if getattr(self, "MacroDef", None) else {}
            # title = macro.get("connect_open_error_title", "Fehler beim Öffnen des Ports")  # v1.15 (entfallen)
            title = macro.get("connect_open_error_title", tr("Fehler beim Öffnen der Verbindung"))  # v1.15
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
        if status == "dropped":  # v1.20
            return self._fail_connect()  # v1.20
        # status == "read_error"  # v1.20
        self._fail_connect()  # v1.20: erst Status und Anschluss freigeben, dann der Dialog
        # self._msg("Falsche oder keine Antwort vom ARDUINO.\n\nPrüfe, ob das richtige MobaLedLib-Programm auf den "  # v1.16 (entfallen)
        # "Arduino geladen ist. Es muss mit dem Compilerschalter\n  #define RECEIVE_LED_COLOR_PER_RS232\n"  # v1.16 (entfallen)
        # "übersetzt sein. Das Programm kann mit dem Knopf 'Z. Arduino schicken' geladen werden.",  # v1.16 (entfallen)
        # "Fehler beim Lesen der Antwort des ARDUINO")  # v1.16 (entfallen)
        self._msg("Falsche oder keine Antwort vom Gerät.\n\nPrüfe, ob das richtige MobaLedLib-Programm auf das "  # v1.16: Gerät statt Arduino
                  "Gerät geladen ist. Es muss mit dem Compilerschalter\n  #define RECEIVE_LED_COLOR_PER_RS232\n"  # v1.16
                  "übersetzt sein. Das Programm kann mit dem Knopf 'Z. Arduino schicken' geladen werden.",  # v1.16
                  "Fehler beim Lesen der Antwort des Geräts")  # v1.16
        return False  # v1.20

    def _is_connected_to(self, target, via_ip=False):  # v1.20
        """Ist schon eine fertig aufgebaute Verbindung zu diesem Anschluss (COM7, /dev/ttyUSB0) bzw. dieser IP-Adresse offen? ARDUINO_current_portname wird erst nach dem Handshake gesetzt."""  # v1.20
        return (self.is_connection_open() and bool(self.ARDUINO_IP) == bool(via_ip)  # v1.20
                and str(getattr(self, "ARDUINO_current_portname", "") or "").upper() == str(target or "").upper())  # v1.20

    def _open_and_handshake(self, port):  # v1.20: aus _connect verschoben; Ergebnis (Status, Fehler), Status: ok, open_error, dropped, read_error
        """Oeffnet den Anschluss und liest die Startmeldung ('#?'). Alles unter PORT_ACCESS_LOCK: Die Abfragen der Geraeteauswahl und die Erkennung greifen nicht dazwischen
        und oeffnen den Anschluss nicht ein zweites Mal. Keine Dialoge hier (sonst blockiert die Sperre die Geraeteauswahl)."""  # v1.20
        with PORT_ACCESS_LOCK:  # v1.20
            try:
                import serial
                self.ARDUINO_status = "Connecting"
                # self.arduino = serial.Serial(port, baudrate=115200, timeout=2, parity=serial.PARITY_NONE,  # v1.06 (entfallen: oeffnete mit DTR an: Reset des Nano)
                #                              stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)  # v1.06 (entfallen)
                self.arduino = self._open_serial(serial, port)  # v1.06
                self.ARDUINO_startmessage = ""  # v1.18: Startmeldung des vorherigen Geraets verwerfen
                self._evaluated_startmsg = None  # v1.19: neue Verbindung, neue Auswertung
            except BaseException as e:                    # noqa: BLE001
                logger.info("Port %s nicht zu oeffnen: %s", port, e)
                return "open_error", e  # v1.20

            time.sleep(1)
            self.send_to_ARDUINO_init_buffer(immediatly=True)
            try:
                self.arduino.flush()
            except Exception:                             # noqa: BLE001
                pass
            self.send_to_ARDUINO("#?\r\n")
            self._wait_sent(2.0)
            txt, read_error = "", False
            t1 = _const("SerialIF_teststring1", "#?LEDs_AutoProg")
            trials, start = 0, time.time()
            try:  # v1.17: wird die Verbindung waehrend des Verbindens von aussen getrennt (self.arduino ist dann None), kein Traceback
                while True:                                   # wie im Original: bis zu 3 neue Anfragen im Sekundentakt
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
            except (AttributeError, OSError):  # v1.17
                logger.info("Verbindung zu %s wurde waehrend des Verbindens getrennt", port)
                return "dropped", None  # v1.20
            self.send_to_ARDUINO("#X\r\n")
            if read_error:
                try:
                    self.arduino.close()
                except Exception:                         # noqa: BLE001
                    pass
                return "read_error", None  # v1.20
            self.ARDUINO_current_portname = port
            self.ARDUINO_status = "Connected"
            # self._set_connect_status("Verbunden mit " + port + " - EFFECT Mode", "green")  # v1.04 (entfallen)
            self._set_connect_status(tr('Verbunden mit ') + port + " - EFFECT Mode", "green")  # v1.04
            self._start_reader()
            return "ok", None  # v1.20

    def connect_esp32(self, host, password):
        with self._conn_lock:
            if self._is_connected_to(host, via_ip=True):  # v1.20: schon mit diesem ESP32 verbunden
                logger.info("Verbindung zu %s besteht schon, sie wird wiederverwendet", host)  # v1.20
                return True  # v1.20
            if self.arduino:
                self.disconnect()
            return self.connectIP(host, esp32_password=password)

    def connectIP(self, IPAdresse=None, *, esp32_password=None):
        """Connect to a WLAN Pico or authenticate to an ESP32 device session."""
        if not IPAdresse:
            return False
        with self._conn_lock:  # v1.20: auch direkte Aufrufe (Zeitgeber des Dialogs: jede Sekunde) sind serialisiert und verbinden nicht neu, wenn die Verbindung steht
            if self._is_connected_to(IPAdresse, via_ip=True):  # v1.20
                return True  # v1.20
            return self._connectIP_impl(IPAdresse, esp32_password=esp32_password)  # v1.20

    def _connectIP_impl(self, IPAdresse, *, esp32_password=None):  # v1.20: Rumpf von connectIP
        # self._set_connect_status("Versuch sich mit dem PICO- IP: " + IPAdresse + " zu verbinden ...", "red")  # v1.04 (entfallen)
        if esp32_password is None:
            self._set_connect_status(tr('Versuch sich mit dem PICO- IP: ') + IPAdresse + " zu verbinden ...", "red")
        else:
            self._set_connect_status("ESP32-WLAN-Verbindung zu " + IPAdresse + " …", "red")  # v1.04
        t1 = _const("SerialIF_teststring1", "#?LEDs_AutoProg")
        t3 = _const("SerialIF_teststring3", "#?LEDs_AutoProg3")
        try:
            if esp32_password is not None:
                self.arduino = TcpPort(IPAdresse, 2323, timeout=5)
                nonce = self.arduino.read_until(timeout=5).strip()
                if len(nonce) != 32 or any(char not in b"0123456789abcdef" for char in nonce):
                    raise ConnectionError("Keine gültige ESP32-Anmeldeanfrage")
                digest = hmac.digest(esp32_password.encode("utf-8"), nonce, "sha256")
                self.arduino.write(digest.hex().encode("ascii") + b"\n")
                if self.arduino.read_until(timeout=5).strip() != b"OK":
                    raise ConnectionError("ESP32-Anmeldung fehlgeschlagen")
            else:
                try:
                    import telnetlib
                    self.arduino = telnetlib.Telnet(IPAdresse, 23, timeout=5)
                    self.arduino.is_open = True
                    self.arduino.portstr = IPAdresse
                except ImportError:
                    self.arduino = TcpPort(IPAdresse, 23, timeout=5)
            self.arduino.write(b"#?\n")
            txt = self.arduino.read_until(b"\n", 5).decode(errors="ignore")
            pos = txt.find(t1)
            pos = pos + 2 if pos != -1 else txt.find(t3)
            pos2 = txt.find("\n", pos) if pos != -1 else -1
            if pos == -1 or pos2 == -1:
                raise ConnectionError("keine gueltige Antwort: " + txt[:60])
            txt = txt[pos:pos2]
            self.ARDUINO_IP = True
            self._evaluated_startmsg = None  # v1.19
            self.queue.put(txt)
            self.determine_ARDUINO_Properties_from_Startmessage(txt)
            self.ARDUINO_current_portname = IPAdresse
            self.ARDUINO_status = "Connected"
            # self._set_connect_status("Verbunden mit " + IPAdresse + " - EFFECT Mode", "green")  # v1.04 (entfallen)
            self._set_connect_status(tr('Verbunden mit ') + IPAdresse + " - EFFECT Mode", "green")  # v1.04
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
                    # self.led_off()  # v1.13 (entfallen: nur noch mit der Option LedOffOnDisconnect)
                    if str(self.getConfigData("LedOffOnDisconnect")).strip().lower() in ("1", "true"):  # v1.13
                        self.led_off()  # v1.13
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

    def close_arduino_connection_after_write_error(self, expected_port=None, lock_timeout=1.0):
        """Schliesst die Verbindung nach einem Schreibfehler (Sendethread) oder fuer eine Abfrage (expected_port). Unter _conn_lock, damit nicht zugleich verbunden oder getrennt wird;
        kommt die Sperre nicht binnen lock_timeout (0 = nicht warten), wird wie bisher ohne sie geschlossen (kein Stillstand: der Sendethread wird von disconnect abgewartet)."""  # v1.20
        got = self._conn_lock.acquire(timeout=lock_timeout) if lock_timeout and lock_timeout > 0 else self._conn_lock.acquire(blocking=False)  # v1.20
        try:  # v1.20
            if expected_port is not None and self.arduino is not expected_port:
                return
            self._stop_reader()
            try:
                if self.arduino:
                    self.arduino.close()
            except Exception:                             # noqa: BLE001
                pass
            self.arduino = None
            self.ARDUINO_current_portname = ""
            self.ARDUINO_status = ""
            self.send_active = False
            self._set_connect_status("Nicht Verbunden", "black")
        finally:  # v1.20
            if got:  # v1.20
                self._conn_lock.release()  # v1.20

    def connect_silent(self, port=None, wlan=None, dtr=None, esp32=None, verify=None):  # v1.20
        """Verbinden ohne Dialoge (Autoconnect beim Start, nach dem Hochladen, Blattwechsel). quiet und dtr_override gelten nur fuer diesen Aufruf und werden unter _conn_lock gesetzt
        und zurueckgenommen (vorher setzte der Aufrufer sie ungeschuetzt: zwei gleichzeitige Aufrufe stoerten sich). Eine schon offene Verbindung bleibt unberuehrt (Rueckgabe True,
        kein Trennen, kein erneutes Oeffnen); zum Wechseln erst disconnect() unter derselben Sperre aufrufen. verify: Funktion ohne Argument; liefert sie False, wird wieder getrennt."""
        with self._conn_lock:  # v1.20
            if self.is_connection_open():  # v1.20
                return True  # v1.20
            self.quiet, self.dtr_override = True, dtr  # v1.20
            try:  # v1.20
                if esp32:  # v1.20
                    self.connect_esp32(esp32[0], esp32[1])  # v1.20
                else:  # v1.20
                    self.connect(port=port, wlan=wlan)  # v1.20
                ok = bool(self.is_connection_open())  # v1.20
                if ok and verify is not None and not verify():  # v1.20
                    self.disconnect()  # v1.20
                    return False  # v1.20
                return ok  # v1.20
            finally:  # v1.20
                self.quiet, self.dtr_override = False, None  # v1.20
