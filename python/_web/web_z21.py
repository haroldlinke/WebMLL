# Datei-Version: 1.01 (2026-10-21) - web_z21.py
# ----------------------------------------------------------------------------------------------
# Name:           web_z21.py
# Path:           _web/web_z21.py
# Version:        1.01
# Last Update:    2026-10-21
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-21  Neu: Reiter Z21 Simulator (mlpyproggen/Z21MonitorPage.py ohne Tk), Phase 1: Z21-Protokoll ueber UDP 21105 mit einem Arduino (Start, Stop, Taster-Adressen, Protokollfenster)
#   1.01  2026-10-21  Phase 2: Rueckmeldung (RMBUS) vom Arduino an die Z21-Clients (Zuhoerer fuer die Zeilen JSON:{RMBUS}, zyklische Abfrage ?*, notifyZ21_RMBUS_DATA), LAN_RMBUS_GETDATA antwortet dem Anfragenden, Status mit der Zahl der Clients
# ----------------------------------------------------------------------------------------------
"""Web-Version der Seite "Z21 Simulator" (mlpyproggen/Z21MonitorPage.py, Klasse Z21MonitorPage, ohne Tk).

Die Seite gibt sich gegenueber Steuerprogrammen (Rocrail, iTrain, Traincontroller, WinDigiPet ...) als Roco-Z21-Zentrale aus. Auf UDP-Port 21105 nimmt sie
die Pakete des Z21-LAN-Protokolls an, antwortet wie eine Z21 und schickt Weichen- und Lokbefehle als DCC-Kommando  @ AAA CC AA  an den Arduino
(AAA: Adresse, CC: Kanal 00 oder 01, AA: 00 aus, 01 ein; die Z21 zaehlt Adressen ab 0, die MobaLedLib ab 1).

Aufbau:
  Z21Core       die Pakete: Antworten der Z21 (Seriennummer, Hardware, Version, Broadcast-Flags, Weichen- und Lokinfo) und die Befehle an den Arduino.
                Ohne Netz und ohne Oberflaeche, damit sie sich mit einem Testclient pruefen laesst.
  Z21Simulator  Netz: UDP-Socket und Hintergrund-Thread, Protokollzeilen fuer die Seite, Start und Stop. Es gibt nur einen Simulator je Programm (get_simulator);
                er laeuft weiter, wenn man den Reiter wechselt oder die Seite neu laedt, und endet mit Stop oder mit dem Programm.
  build         die Seite (NiceGUI).

Unterschiede zum Tk-Original (siehe HOC_intern.md, Version 2.05):
  * Ein Arduino (der mit ARDUINO -> Verbinden verbundene). Die Port-Liste (Z21Data: bis zu drei Arduinos mit DCC-Adressbereichen) folgt in Phase 3.
  * Rueckmeldung (RMBUS, Phase 2): Hat ein Client das Broadcast-Flag R-Bus (0x02) gesetzt, fragt der Simulator den Arduino alle 100 ms (Einstellung RMbusTimer x 100 ms) mit ?* und
    gibt die Zeilen JSON:{"RMBUS": ...} (7 Bit je Byte, von web_serial.py aus den Binaernachrichten gebaut) nach 8 Bit umgewandelt als LAN_RMBUS_DATACHANGED an die Clients weiter, wenn
    sich der Stand einer Gruppe (10 Module) aendert. LAN_RMBUS_GETDATA antwortet dem Anfragenden mit dem gemerkten Stand (im Original nur den Clients mit dem Flag).
  * Die Pakete werden direkt im Hintergrund-Thread bearbeitet (das Original reihte sie in eine Warteschlange und las sie alle 100 ms im Tk-Hauptfenster).
  * Fehler im Original behoben: `false` und `FALSE` (NameError) in LAN_GET_BROADCASTFLAGS und remove_client; zu kurze oder unbekannte Pakete beenden den Thread nicht mehr.
  * Das Kommando an den Arduino geht in einem Stueck an send_to_ARDUINO (die serielle Schicht sendet Zeichen fuer Zeichen mit Pause), nicht Zeichen fuer Zeichen mit time.sleep.
  * Die Seite zeigt die IP-Adresse und den Port, die man im Steuerprogramm eintragen muss.
"""
from __future__ import annotations

import asyncio
import binascii
import collections
import json  # v1.01
import logging
import socket
import threading
import time
from datetime import datetime

logger = logging.getLogger(__name__)

Z21_PORT = 21105
SERIAL_NUMBER = (0xF5, 0x1A)               # LSB, MSB
HW_TYPE = (0x01, 0x02)                     # LSB, MSB
FW_VERSION = (0x30, 0x01)                  # LSB, MSB

# Z21 LAN Protokoll
LAN_X_Header = 0x40
LAN_GET_SERIAL_NUMBER = 0x10
LAN_GET_CODE = 0x18
LAN_LOGOFF = 0x30
LAN_X_GET_SETTING = 0x21
LAN_X_STATUS_CHANGED = 0x62
LAN_X_GET_VERSION = 0x63
LAN_X_SET_STOP = 0x80
LAN_X_GET_FIRMWARE_VERSION = 0xF1
LAN_SET_BROADCASTFLAGS = 0x50
LAN_GET_BROADCASTFLAGS = 0x51
LAN_SYSTEMSTATE_DATACHANGED = 0x84
LAN_SYSTEMSTATE_GETDATA = 0x85
LAN_GET_HWINFO = 0x1A
LAN_GET_LOCOMODE = 0x60
LAN_SET_LOCOMODE = 0x61
LAN_GET_TURNOUTMODE = 0x70
LAN_SET_TURNOUTMODE = 0x71
LAN_X_GET_LOCO_INFO = 0xE3
LAN_X_SET_LOCO = 0xE4
LAN_X_SET_LOCO_FUNCTION = 0xF8
LAN_X_LOCO_INFO = 0xEF
LAN_X_GET_TURNOUT_INFO = 0x43
LAN_X_SET_TURNOUT = 0x53
LAN_X_CV_READ = 0x23
LAN_X_CV_WRITE = 0x24
LAN_X_CV_POM = 0xE6
LAN_RMBUS_DATACHANGED = 0x80
LAN_RMBUS_GETDATA = 0x81
LAN_RMBUS_PROGRAMMODULE = 0x82
LAN_RAILCOM_GETDATA = 0x89
LAN_LOCONET_FROM_LAN = 0xA2
LAN_LOCONET_DISPATCH_ADDR = 0xA3
LAN_LOCONET_DETECTOR = 0xA4
LAN_CAN_DETECTOR = 0xC4

CSS = """
.mll-z21 { max-width: 980px; margin: 0 auto; padding: 8px; }
.mll-z21-desc { cursor: pointer; }
.mll-z21-btn { min-height: 44px; }
.mll-z21-log { height: 46vh; font-family: monospace; font-size: 12px; background: #f6f7f9; border: 1px solid #b7c0cc; }
"""


# --------------------------------------------------------------------------- Protokoll (ohne Netz und ohne Oberflaeche)
class Z21Core:
    """Die Pakete der Z21. send_udp(Bytes, Client), send_arduino(Adresse, Kanal, Ein), send_raw(Text) und log(Text) kommen vom Aufrufer."""

    def __init__(self, send_udp, send_arduino, log, send_raw=None):
        self.send_udp, self.send_arduino, self.log, self.send_raw = send_udp, send_arduino, log, send_raw
        self.reset()

    def reset(self):
        self.client_turnout_info_dict = {}
        self.client_broadcast_flag_dict = {}
        self.client_RMBUS_GETDATA_dict = {}
        self.RMBUS_DATA_bytearray = {0: bytearray(10)}

    # ---- Senden
    def EthSend(self, DataLen, Header, dataString, withXOR, client=None):
        data = bytearray(b" " * 24)
        data[0] = DataLen & 0xFF
        data[1] = DataLen >> 8
        data[2] = Header & 0xFF
        data[3] = Header >> 8
        data[DataLen - 1] = 0                                       # XOR
        xorlen = 0 if withXOR else 1
        for i in range(DataLen - 5 + xorlen):                       # ohne Laenge, Header und XOR
            if withXOR:
                data[DataLen - 1] = data[DataLen - 1] ^ dataString[i]
            data[i + 4] = dataString[i]
        packet = bytes(data[0:DataLen])
        self.send_udp(packet, client)
        return packet

    # ---- Clients
    def add_client(self, client, broadcastflags):
        self.client_broadcast_flag_dict[client] = broadcastflags
        if broadcastflags & 0b0001:
            self.client_turnout_info_dict[client] = broadcastflags
        if broadcastflags & 0b0010:
            self.client_RMBUS_GETDATA_dict[client] = broadcastflags         # Phase 2: dem Arduino sagen, dass Rueckmeldungen gebraucht werden

    def remove_client(self, client):
        self.client_broadcast_flag_dict.pop(client, None)
        self.client_turnout_info_dict.pop(client, None)
        self.client_RMBUS_GETDATA_dict.pop(client, None)

    # ---- Rueckmeldung (RMBUS)
    # def send_RMBUS_DATA(self, send_data, groupidx=0):  # v1.01 (entfallen)
    def send_RMBUS_DATA(self, send_data, groupidx=0, only_client=None):  # v1.01
        empty = bytearray(12)
        data = bytearray(1)
        data[0] = groupidx
        data.extend(send_data)
        if len(data) < 10:
            data.extend(empty[len(data):11])
        # for info_client in list(self.client_RMBUS_GETDATA_dict.keys()):  # v1.01 (entfallen)
        clients = [only_client] if only_client is not None else list(self.client_RMBUS_GETDATA_dict.keys())  # v1.01
        for info_client in clients:  # v1.01
            self.EthSend(0x0F, LAN_RMBUS_DATACHANGED, data[0:12], False, client=info_client)
            self.log(" - LAN_RMBUS_DATACHANGED: " + data.hex())

    def set_RMBUS_DATA(self, data, groupidx=0):
        if self.RMBUS_DATA_bytearray.get(groupidx, {}) != data:
            self.RMBUS_DATA_bytearray[groupidx] = data
            self.send_RMBUS_DATA(data, groupidx=groupidx)

    # def get_RMBUS_DATA(self, groupidx=0):  # v1.01 (entfallen)
        # self.send_RMBUS_DATA(self.RMBUS_DATA_bytearray.get(groupidx, bytearray(10)), groupidx=groupidx)  # v1.01 (entfallen)
    def get_RMBUS_DATA(self, groupidx=0, client=None):  # v1.01
        """LAN_RMBUS_GETDATA: den gemerkten Stand der Gruppe an den Anfragenden schicken (im Original nur an die Clients mit dem Flag R-Bus) und den Arduino fragen"""  # v1.01
        self.send_RMBUS_DATA(self.RMBUS_DATA_bytearray.get(groupidx, bytearray(10)), groupidx=groupidx, only_client=client)  # v1.01
        if self.send_raw is not None:
            self.send_raw("?*\n")                                    # den Arduino nach dem aktuellen Stand fragen

    def notifyZ21_RMBUS_DATA(self, json_data_str):  # v1.01
        """Rueckmeldung vom Arduino: JSON:{"RMBUS": "<Hex, 7 Bit je Byte>"}; in 8 Bit umwandeln und je 10 Bytes (eine Gruppe, 10 Module) an die Clients melden, wenn sich etwas aenderte"""  # v1.01
        try:  # v1.01
            hex_7bit = json.loads(json_data_str).get("RMBUS", "")  # v1.01
        except (ValueError, AttributeError):  # v1.01
            self.log(" - Rückmeldung nicht lesbar: " + str(json_data_str)[:60])  # v1.01
            return  # v1.01
        # if len(hex_7bit) == 2 and hex_7bit[0] == "?":  # v1.01  # v1.01 (entfallen)
        # return  # v1.01 (entfallen)
        if not isinstance(hex_7bit, str):  # v1.01
            self.log(" - Rückmeldung nicht lesbar: " + str(hex_7bit)[:60])  # v1.01
            return  # v1.01
        if hex_7bit == "" or (len(hex_7bit) == 2 and hex_7bit[0] == "?"):                 # leer (kein RMBUS-Eintrag) oder die Antwort auf eine Frage: ignorieren (die Umwandlung machte aus "" ein Byte 00 und ueberschrieb die Gruppe 0)  # v1.01
            return  # v1.01
        try:  # v1.01
            data_8bit = self.convert_7bit_to_8bit(bytearray.fromhex(hex_7bit))  # v1.01
        except ValueError:  # v1.01
            self.log(" - Rückmeldung nicht lesbar: " + str(hex_7bit)[:60])  # v1.01
            return  # v1.01
        rmbus_data_str = data_8bit.hex()  # v1.01
        group_idx = 0  # v1.01
        while group_idx * 20 < len(rmbus_data_str):  # v1.01
            self.set_RMBUS_DATA(bytearray.fromhex(rmbus_data_str[group_idx * 20:group_idx * 20 + 20]), groupidx=group_idx)  # v1.01
            group_idx += 1  # v1.01

    @staticmethod
    def convert_7bit_to_8bit(bytestring):
        result = bytearray()
        countbits = 7
        byte = 0
        if len(bytestring) == 1:
            bytestring += b"\x00"
        for i in range(0, len(bytestring)):
            testbyte = bytestring[i]
            for j in range(7, 0, -1):
                bit = (testbyte >> (j - 1)) & 1
                if countbits == 0:
                    byte |= bit << 7
                    result.append(byte)
                    countbits = 7
                    byte = 0
                else:
                    byte |= bit << (7 - countbits)
                    countbits -= 1
        if countbits != 0:
            result.append(byte)
        return bytes(result)

    # ---- Empfangen
    def slicePacket(self, client, data):
        """Ein Datagramm kann mehrere Pakete enthalten (Laenge little endian in den ersten zwei Bytes)"""
        while len(data) > 0:
            dataLen = int.from_bytes(data[0:2], byteorder="little")
            if dataLen == 0:
                data = data[2:]
            else:
                try:
                    self.receive_message(client, data[0:dataLen])
                except IndexError:
                    self.log(" - Paket zu kurz")
                data = data[dataLen:]

    def receive_message(self, client, packet):
        if len(packet) < 4:
            self.log(" - Paket zu kurz")
            return
        header = (packet[3] << 8) + packet[2]
        data = bytearray(b" " * 16)
        if header == LAN_GET_SERIAL_NUMBER:
            self.log(" - LAN_GET_SERIAL_NUMBER")
            data[0], data[1], data[2], data[3] = SERIAL_NUMBER[0], SERIAL_NUMBER[1], 0, 0
            self.EthSend(0x08, LAN_GET_SERIAL_NUMBER, data, False, client=client)
        elif header == LAN_GET_HWINFO:
            self.log(" - LAN_GET_HWINFO")
            data[0], data[1], data[2], data[3] = HW_TYPE[0], HW_TYPE[1], 0, 0
            data[4], data[5], data[6], data[7] = FW_VERSION[0], FW_VERSION[1], 0, 0
            self.EthSend(0x0C, LAN_GET_HWINFO, data, False, client=client)
        elif header == LAN_LOGOFF:
            self.log(" - LAN_LOGOFF")
            self.remove_client(client)
        elif header == LAN_GET_CODE:
            self.log(" - LAN_GET_CODE")
            data[0] = 0x00                                             # keine Features gesperrt
            self.EthSend(0x05, LAN_GET_CODE, data, False, client=client)
        elif header == LAN_X_Header:
            self._x_message(client, packet, data)
        elif header == LAN_SET_BROADCASTFLAGS:
            self.log(" - LAN_SET_BROADCASTFLAGS")
            self.add_client(client, (packet[5] << 8) + packet[4])
        elif header == LAN_GET_BROADCASTFLAGS:
            self.log(" - LAN_GET_BROADCASTFLAGS")
            flag = self.client_broadcast_flag_dict.get(client, 0)
            data[0], data[1], data[2], data[3] = flag & 0xFF, (flag >> 8) & 0xFF, (flag >> 16) & 0xFF, (flag >> 24) & 0xFF
            self.EthSend(0x08, LAN_GET_BROADCASTFLAGS, data, False, client=client)      # im Original stand hier "false" (NameError)
        elif header in (LAN_GET_LOCOMODE, LAN_SET_LOCOMODE, LAN_GET_TURNOUTMODE, LAN_SET_TURNOUTMODE, LAN_RMBUS_PROGRAMMODULE):
            pass
        elif header == LAN_RMBUS_GETDATA:
            self.log(" - LAN_RMBUS_GETDATA " + str(packet[4]))
            # self.get_RMBUS_DATA(packet[4])  # v1.01 (entfallen)
            self.get_RMBUS_DATA(packet[4], client=client)  # v1.01
        elif header == LAN_SYSTEMSTATE_GETDATA:
            self.log(" - LAN_SYSTEMSTATE_GETDATA")
            for i in range(16):
                data[i] = 0                                            # Strom, Temperatur, Spannung, Zentralenstatus: alles 0
            self.EthSend(0x14, LAN_SYSTEMSTATE_DATACHANGED, data, False, client=client)
        elif header in (LAN_RAILCOM_GETDATA, LAN_LOCONET_FROM_LAN, LAN_LOCONET_DISPATCH_ADDR, LAN_LOCONET_DETECTOR, LAN_CAN_DETECTOR, 0x12, 0x13, 0x16, 0x17):
            pass
        else:
            self.log(" - unbekanntes Paket 0x%04X" % header)

    def _x_message(self, client, packet, data):
        x_header = packet[4]
        if x_header == LAN_X_GET_SETTING:
            kind = packet[5]
            if kind == 0x21:
                self.log(" - LAN_X_GET_SETTING - X_GET_VERSION")
                data[0], data[1], data[2], data[3] = LAN_X_GET_VERSION, 0x21, 0x30, 0x12          # X-Header, DB0, X-Bus Version, ID der Zentrale
                self.EthSend(0x09, LAN_X_Header, data, True, client=client)
            elif kind == 0x24:
                data[0], data[1], data[2] = LAN_X_STATUS_CHANGED, 0x22, 0                         # Status
                self.EthSend(0x08, LAN_X_Header, data, True, client=client)
            elif kind == 0x80:
                self.log(" - LAN_X_GET_SETTING - X_SET_TRACK_POWER_OFF")
                self.EthSend(0x07, LAN_X_Header, data, True, client=client)
            elif kind == 0x81:
                self.log(" - LAN_X_GET_SETTING - X_SET_TRACK_POWER_ON")
                data[0], data[1] = 0x61, 0x01
                self.EthSend(0x07, LAN_X_Header, data, True, client=client)
        elif x_header == LAN_X_CV_READ:
            if packet[5] == 0x11:
                self.log(" - X_CV_READ")
        elif x_header == LAN_X_CV_WRITE:
            if packet[5] == 0x12:
                self.log(" - X_CV_WRITE")
        elif x_header == LAN_X_CV_POM:
            self.log(" - LAN_X_CV_POM")
        elif x_header == LAN_X_GET_TURNOUT_INFO:
            self.log(" - X_GET_TURNOUT_INFO")
            data[0], data[1], data[2], data[3] = 0x43, packet[5], packet[6], 1                    # 1: inaktiv
            self.EthSend(0x09, LAN_X_Header, data, True, client=client)
        elif x_header == LAN_X_SET_TURNOUT:
            if (packet[7] & 1) == 0:
                status_str, ret_value, state = "Contact 2", 1, 0
            else:
                status_str, ret_value, state = "Contact 1", 2, 1
            if (packet[7] & 8) == 0:
                active_str, activate = "deactivate", 0
            else:
                active_str, activate = "activate", 1
            dccaddress = (packet[5] << 8) + packet[6] + 1                                         # die Z21 zaehlt ab 0, die MobaLedLib ab 1
            self.log(" - X_SET_TURNOUT Addr:" + str(dccaddress) + "-" + status_str + "-" + active_str)
            data[0], data[1], data[2], data[3] = 0x43, packet[5], packet[6], ret_value
            for info_client in list(self.client_turnout_info_dict.keys()):
                self.EthSend(0x09, LAN_X_Header, data, True, client=info_client)
            self.send_arduino(dccaddress, state, activate)
        elif x_header == LAN_X_SET_STOP:
            self.log(" - X_SET_STOP")
        elif x_header == LAN_X_GET_LOCO_INFO:
            if packet[5] == 0xF0:
                self.log(" - LAN_X_GET_LOCO_INFO")
                data[0], data[1], data[2] = LAN_X_LOCO_INFO, packet[6] & 0x3F, packet[7]
                for i in range(3, 9):
                    data[i] = 0
                self.EthSend(0x0E, LAN_X_Header, data, True, client=client)
        elif x_header == LAN_X_SET_LOCO:
            if packet[5] == LAN_X_SET_LOCO_FUNCTION:
                self.log(" - LAN_X_SET_LOCO_FUNCTION")
            else:
                self.log(" - X_SET_LOCO_DRIVE")
            data[0], data[1], data[2], data[3], data[4] = LAN_X_LOCO_INFO, packet[6] & 0x3F, packet[7], 2, packet[8]
            for i in range(5, 9):
                data[i] = 0
            self.EthSend(0x0C, LAN_X_Header, data, True, client=client)                            # Loco_Info zurueck
        elif x_header == LAN_X_GET_FIRMWARE_VERSION:
            self.log(" - X_GET_FIRMWARE_VERSION")
            data[0], data[1], data[2], data[3] = 0xF3, 0x0A, FW_VERSION[1], FW_VERSION[0]
            self.EthSend(0x09, LAN_X_Header, data, True, client=client)


# --------------------------------------------------------------------------- Netz
def local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:                                                              # das Ziel muss nicht erreichbar sein, es wird nichts gesendet
        s.connect(("192.0.0.1", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


class Z21Simulator:
    """UDP-Server mit Hintergrund-Thread. start() und stop() blockieren kurz (Socket, Verbindung zum Arduino): nicht im Event-Loop aufrufen."""

    def __init__(self, ctrl, port=Z21_PORT, ip_func=local_ip):
        self.ctrl, self.port, self.ip_func = ctrl, port, ip_func
        self.lines = collections.deque(maxlen=2000)
        self.seq = 0
        self.lock = threading.Lock()
        self.sock = None
        self.thread = None
        self.stop_event = threading.Event()
        self.ip = ""
        self._fragments: list = []
        self.core = Z21Core(self._send_udp, self._send_arduino, self._core_log, send_raw=self._send_raw)
        self.poll_thread = None  # v1.01
        self.poll_count = 0                                                  # Anzahl der Abfragen ?* (fuer die Pruefung)  # v1.01

    # ---- Protokollzeilen
    def emit(self, text):
        with self.lock:
            self.seq += 1
            self.lines.append((self.seq, text))

    def lines_since(self, seq):
        """(neue Nummer, [Zeilen]) seit der Nummer seq"""
        with self.lock:
            new = [(n, t) for n, t in self.lines if n > seq]
            return (new[-1][0] if new else seq), [t for _, t in new]

    def _core_log(self, text):
        self._fragments.append(text)

    # ---- Senden
    def _send_udp(self, data, client):
        sock = self.sock
        if sock is None or client is None:
            return
        try:
            sock.sendto(data, client)
            logger.debug("Z21 gesendet %s an %s", binascii.hexlify(data), client)
        except OSError as e:
            self.emit(f"Fehler beim Senden an {client}: {e}")

    def _connected(self):
        try:
            return bool(self.ctrl.is_connection_open())
        except Exception:                                            # noqa: BLE001
            return False

    def _send_arduino(self, dccaddress, channel, activate):
        command = "@ {:03} {:02} {:02}".format(dccaddress, channel, activate)
        if not self._connected():
            self._fragments.append(f" [nicht mit dem ARDUINO verbunden: {command} nicht gesendet]")
            return
        self.ctrl.send_to_ARDUINO(command + "\n")
        self._fragments.append(" -> ARDUINO: " + command)

    def _send_raw(self, text):
        if self._connected():
            self.ctrl.send_to_ARDUINO(text)

    # ---- Datagramm
    def handle_datagram(self, data, client):
        self._fragments = []
        head = datetime.now().strftime("%H:%M:%S") + f"  {client[0]}:{client[1]}  " + binascii.hexlify(data).decode()
        try:
            self.core.slicePacket(client, data)
        except Exception as e:                                       # noqa: BLE001
            logger.warning("Z21-Paket nicht bearbeitet", exc_info=True)
            self._fragments.append(f" - Fehler: {type(e).__name__}: {e}")
        self.emit(head + "".join(self._fragments))

    # ---- Rueckmeldung vom Arduino
    def rmbus_interval(self):  # v1.01
        """Wartezeit zwischen zwei Abfragen ?* in Sekunden: Einstellung RMbusTimer (x 100 ms), ohne gueltigen Wert (0 oder leer) 100 ms"""  # v1.01
        try:  # v1.01
            n = int(float(str(self.ctrl.getConfigData("RMbusTimer")).strip() or 0))  # v1.01
        except (ValueError, TypeError, AttributeError):  # v1.01
            n = 0  # v1.01
        return (n if n > 0 else 1) * 0.1  # v1.01

    def _on_arduino_line(self, text):  # v1.01
        """Zeile vom Arduino: JSON:{"RMBUS": ...} an die Clients mit dem Flag R-Bus weitergeben"""  # v1.01
        if not text.startswith("JSON:") or not self.core.client_RMBUS_GETDATA_dict:  # v1.01
            return  # v1.01
        self._fragments = []  # v1.01
        self.core.notifyZ21_RMBUS_DATA(text[5:].strip())  # v1.01
        if self._fragments:                                                  # nur wenn sich etwas geaendert hat (sonst kaeme alle 100 ms eine Zeile)  # v1.01
            self.emit(datetime.now().strftime("%H:%M:%S") + "  ARDUINO  " + text.strip()[:80] + "".join(self._fragments))  # v1.01

    def _poll_loop(self, stop_event):  # v1.01
        """Solange ein Client die Rueckmeldung will (Flag R-Bus) den Arduino regelmaessig nach dem Stand fragen (wie der Zeitgeber der Seite Serial Monitor im Original)"""  # v1.01
        while not stop_event.wait(self.rmbus_interval()):  # v1.01
            if self.core.client_RMBUS_GETDATA_dict and self._connected():  # v1.01
                self.ctrl.send_to_ARDUINO("?*\n")  # v1.01
                self.poll_count += 1  # v1.01

    def rmbus_clients(self):  # v1.01
        return len(self.core.client_RMBUS_GETDATA_dict)  # v1.01

    def _loop(self, sock, stop_event):
        logger.debug("Z21Thread gestartet")
        try:
            sock.settimeout(1)
        except OSError:
            return                                                   # schon wieder geschlossen
        while not stop_event.is_set():
            try:
                data, client = sock.recvfrom(1024)
            except (socket.timeout, ConnectionResetError):
                continue
            except OSError:
                break                                                # Socket geschlossen (Stop)
            self.handle_datagram(data, client)
        logger.debug("Z21Thread beendet")

    # ---- Start und Stop
    @property
    def running(self):
        return self.thread is not None and self.thread.is_alive()

    def start(self):
        """Rueckgabe: (ok, Meldung)"""
        if self.running:
            return True, "Der Z21 Simulator läuft schon."
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind(("", self.port))
        except OSError as e:
            sock.close()
            text = f"Der UDP-Port {self.port} ist nicht frei ({e}). Läuft schon ein anderer Z21-Simulator oder eine Z21-Software?"
            self.emit("Fehler: " + text)
            return False, text
        self.ip = self.ip_func()
        self.sock = sock
        self.core.reset()
        hostname = socket.gethostname()
        self.emit(f"Socket opened: Host {hostname} IP-adress {self.ip} Port {self.port}")
        try:
            connected = bool(self.ctrl.connect_if_not_connected())
        except Exception:                                            # noqa: BLE001
            logger.warning("Verbinden mit dem ARDUINO fehlgeschlagen", exc_info=True)
            connected = False
        if not connected:
            self.emit("Hinweis: keine Verbindung zum ARDUINO. Die Befehle werden erst gesendet, wenn „Mit ARDUINO verbinden“ (Kopfzeile) gelungen ist.")
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._loop, args=(sock, self.stop_event), daemon=True, name="Z21Simulator")
        self.thread.start()
        listeners = getattr(self.ctrl, "rx_listeners", None)  # v1.01
        if listeners is not None:  # v1.01
            if self._on_arduino_line not in listeners:  # v1.01
                listeners.append(self._on_arduino_line)  # v1.01
            self.poll_thread = threading.Thread(target=self._poll_loop, args=(self.stop_event,), daemon=True, name="Z21Rueckmeldung")  # v1.01
            self.poll_thread.start()  # v1.01
        else:  # v1.01
            self.emit("Hinweis: Die Rückmeldung (RMBUS) vom Arduino ist mit dieser Version der seriellen Schicht nicht verfügbar (web_serial.py aktualisieren).")  # v1.01
        self.emit("Z21 Simulator started")
        return True, ""

    def stop(self):
        if self.thread is None:
            return
        self.stop_event.set()
        listeners = getattr(self.ctrl, "rx_listeners", None)  # v1.01
        if listeners is not None and self._on_arduino_line in listeners:  # v1.01
            listeners.remove(self._on_arduino_line)  # v1.01
        sock, self.sock = self.sock, None
        if sock is not None:
            try:
                sock.close()
            except OSError:
                pass
        if self.thread.is_alive():
            self.thread.join(3)
        if self.poll_thread is not None and self.poll_thread.is_alive():  # v1.01
            self.poll_thread.join(1)  # v1.01
        self.thread = None
        self.poll_thread = None  # v1.01
        self.core.reset()
        self.emit("Z21 Simulator stopped")


_SIMULATOR = {"sim": None}


def get_simulator(ctrl):
    """Den einen Simulator des Programms liefern (bleibt beim Wechsel des Reiters und beim Neuladen der Seite erhalten)"""
    sim = _SIMULATOR["sim"]
    if sim is None or sim.ctrl is not ctrl:
        if sim is not None:
            sim.stop()
        sim = _SIMULATOR["sim"] = Z21Simulator(ctrl)
    return sim


def stop_all():
    """Beim Beenden des Programms"""
    sim = _SIMULATOR["sim"]
    if sim is not None:
        try:
            sim.stop()
        except Exception:                                            # noqa: BLE001
            logger.warning("Z21 Simulator nicht sauber beendet", exc_info=True)


# --------------------------------------------------------------------------- Taster-Adressen
SEARCH_START = "// Input channel defines for local inputs and expert users\n"
SEARCH_END = "/*********************/"


def key_address_lines(file_data):
    """Die Zeilen mit den Eingangskanaelen aus der Header-Datei (wie show_key_adresses im Original)"""
    out = []
    found = False
    for line in file_data:
        if line == SEARCH_START:
            found = True
            out += ["", "", "*" * 62]
        if found:
            if line.startswith(SEARCH_END):
                out += ["*" * 62, "", ""]
                break
            out.append(line.rstrip("\r\n"))
    return out


def read_key_addresses():
    """(Zeilen, Fehlermeldung)"""
    import proggen.M02_Public as M02
    import proggen.M08_ARDUINO as M08
    filepath = M08.GetWorkbookPath() + "/" + M02.Ino_Dir_LED + M02.Include_FileName
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            data = fh.readlines()
    except OSError:
        return [], "Datei: " + filepath + " nicht gefunden"
    return key_address_lines(data), ""


# --------------------------------------------------------------------------- Oberflaeche (NiceGUI)
class Z21Page:
    """Rueckgabe von build: tab_selected(), tab_unselected(), page_closed()"""

    def __init__(self, refresh):
        self._refresh = refresh

    def tab_selected(self):
        self._refresh()

    def tab_unselected(self):
        pass

    def page_closed(self):
        pass


def build(ctrl, is_active=None, simulator=None):
    """Baut die Seite "Z21 Simulator" in den aktuellen Container."""
    from nicegui import ui

    sim = simulator or get_simulator(ctrl)
    macro = ctrl.MacroDef.data.get("Z21MonitorPage", {}) if getattr(ctrl, "MacroDef", None) else {}
    title = macro.get("Title") or "Z21 Simulator"
    description = macro.get("Ausführliche Beschreibung") or macro.get("Kurzbeschreibung") or ""
    texts = [(macro.get(k) or d).replace("\n", " ") for k, d in (("Button_1", "Start Simulator"), ("Button_2", "Stop Simulator"), ("Button_3", "Zeige Taster-Adressen"))]
    ui.add_head_html("<style>" + CSS + "</style>")
    refs: dict = {"seen": 0}
    desc = {"open": False}

    def refresh_description():
        opened = desc["open"]
        refs["description"].set_text(description if opened else description.split("\n")[0])
        shape = "white-space: pre-line; overflow: visible; text-overflow: clip" if opened else "white-space: nowrap; overflow: hidden; text-overflow: ellipsis"
        refs["description"].style(f"background: #f0f0f0; padding: 6px 10px; border: 1px solid #aaa; min-width: 0; {shape}")
        refs["desc_toggle"].props(f"icon={'expand_less' if opened else 'expand_more'}")

    def toggle_description(_=None):
        desc["open"] = not desc["open"]
        refresh_description()

    def refresh():
        refresh_description()
        running = sim.running
        # refs["status"].set_text("Z21 Simulator läuft" if running else "Z21 Simulator gestoppt")  # v1.01 (entfallen)
        n_rm = sim.rmbus_clients() if running else 0  # v1.01
        refs["status"].set_text(("Z21 Simulator läuft" + (f", Rückmeldung für {n_rm} Programm{'e' if n_rm != 1 else ''}" if n_rm else "")) if running else "Z21 Simulator gestoppt")  # v1.01
        refs["status"].style("color: #2e7d32; font-weight: 600" if running else "color: #c62828; font-weight: 600")
        refs["address"].set_text(f"Im Steuerprogramm eintragen: IP-Adresse {sim.ip}, Port {sim.port} (UDP)" if running else "")
        refs["start"].set_enabled(not running)
        refs["stop"].set_enabled(running)
        seq, lines = sim.lines_since(refs["seen"])
        refs["seen"] = seq
        for line in lines:
            refs["log"].push(line)

    async def on_start():
        refs["start"].set_enabled(False)
        ok, message = await asyncio.get_running_loop().run_in_executor(None, sim.start)
        if not ok:
            ui.notify(message, type="negative", timeout=0, close_button="OK")
        refresh()

    async def on_stop():
        refs["stop"].set_enabled(False)
        await asyncio.get_running_loop().run_in_executor(None, sim.stop)
        refresh()

    def on_show():
        lines, error = read_key_addresses()
        if error:
            refs["log"].push(error)
        for line in lines:
            refs["log"].push(line)

    with ui.column().classes("w-full items-stretch gap-3 mll-z21"):
        ui.label(title).classes("text-h6")
        with ui.row().classes("w-full items-center no-wrap gap-1 mll-z21-desc"):
            refs["description"] = ui.label(description).classes("grow").tooltip("Antippen zum Auf- und Zuklappen")
            refs["description"].on("click", toggle_description)
            refs["desc_toggle"] = ui.button(icon="expand_more", on_click=toggle_description).props("flat dense round")
        refs["status"] = ui.label("")
        refs["address"] = ui.label("").classes("text-caption")
        with ui.row().classes("w-full items-stretch gap-2"):
            refs["start"] = ui.button(texts[0], on_click=on_start).props("unelevated no-caps color=primary").classes("mll-z21-btn")
            refs["stop"] = ui.button(texts[1], on_click=on_stop).props("outline no-caps").classes("mll-z21-btn")
            refs["show"] = ui.button(texts[2], on_click=on_show).props("outline no-caps").classes("mll-z21-btn")
        refs["log"] = ui.log(max_lines=1000).classes("w-full mll-z21-log")
        ui.timer(0.4, refresh)
    refs["seen"] = max(0, sim.seq - 200)                  # die letzten Zeilen des laufenden Simulators zeigen (Seite neu geladen)
    refresh()
    return Z21Page(refresh)
