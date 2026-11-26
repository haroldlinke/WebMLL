# Datei-Version: 1.25 (2026-11-26) - M07_COM_Port_New.py
# ----------------------------------------------------------------------------------------------
# Name:           M07_COM_Port_New.py
# Path:           proggen/M07_COM_Port_New.py
# Version:        1.25
# Last Update:    2026-11-26
# Author:         Harold Linke, Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.25  2026-11-26  Eine Verbindung pro Geraet: _SERIAL_LOCK ist die gemeinsame Sperre web_serial.PORT_ACCESS_LOCK (auch Verbinden und Erkennung); die Abfragen pruefen NACH dem Warten auf die Sperre noch einmal, ob das Hauptprogramm inzwischen verbunden hat (nicht ein zweites Mal oeffnen, kein falsches 'blockiert'); _Main_Connection nur bei fertigem Handshake. Zeilen mit '# v1.25'
#   1.1.24  2026-11-26  Query_Nano_Bootloader legt das Ergebnis in M07.BOOTLOADER_CACHE ab. Zeilen mit '# v1.24'
#   1.23  2026-11-26  Query_Nano_Bootloader(): Bootloader des Nano ermitteln (alt/neu/Full) fuer die Geraeteauswahl. Zeilen mit '# v1.23'
#   1.00  2026-10-12  Stand der Umstellung (nicht erfasst)
#   1.01  2026-10-28  Hinweis 'PICO im Bootmodus gefunden' funktioniert: Test_IsPicoInBootMode war ein leerer Rumpf, AskBootPico wurde nie auf True gesetzt
#   1.02  2026-10-28  M12 im Aufruf importieren (nicht am Anfang des Moduls)
#   1.03  2026-10-28  Zeitgeber der blinkenden LEDs: Pico/ESP32 unter Linux und macOS nicht jede Sekunde oeffnen; Pruefung des Bootmodus darf den Zeitgeber nicht beenden
#   1.04  2026-11-11  Das Auswahlfenster der Anschluesse nennt den Arduino 'LED Arduino' (vorher 'LED Arduino Arduino': SetArduName haengt 'Arduino' selbst an)
#   1.05  2026-11-23  Identify (Juergen Winkler): ESP32/Pico (LED-Zentrale, ohne WLAN): die LEDs auf der Hauptplatine der gewaehlten Zentrale blinken (Firmware MLLIdentify.h). Der Zeitgeber
#                     des Dialogs schickt jede Sekunde '~MLLIDENT 1' (Anschluss kurz oeffnen, senden, schliessen; kein DetectArduino), Ident_Stop() schickt nach dem Dialog '~MLLIDENT 0'. Neuer
#                     Parameter MainBoard, Hinweistext fuer ESP32/Pico. Zeilen mit '# v1.05'
#   1.06  2026-11-25  Texte: Fenstertitel 'Geräteauswahl' (statt 'Auswahl des COM Ports'), 'Bitte Gerät an einen USB Anschluss ... anschließen' (statt 'LED Arduino');
#                     roter Hinweis 'Tipp: Der ausgewählte Arduino blinkt schnell' entfernt. Zeilen mit '# v1.06'
#   1.07  2026-11-25  Weitere Texte: 'OK, wenn die LEDs am richtigen Gerät schnell blinken.', 'Achtung: Das Gerät wird von einem anderen Programm benutzt.' (jede Zeile
#                     einzeln uebersetzt). Zeilen mit '# v1.07'
#   1.08  2026-11-25  Query_Device_Info(): ESP32/Pico mit '~MLLCFG INFO' nach der Firmware fragen (Antwort: proto, sig, valid, free). Kurz oeffnen wie _Ident_Send_Cmd,
#                     Aufruf im Hintergrund durch web_form_comport (Geraeteliste). Zeilen mit '# v1.08'
#   1.22  2026-11-26  Jeder type in '~MLLINFO' ausser LICHTMASCHINE macht das Geraet zu einem 'Anderen MobaLedLib Geraet' (OTHER_TYPES haelt den type-String). Zeilen mit '# v1.22'
#   1.21  2026-11-26  Ohne gueltige Antwort protokolliert Query_Info alles Empfangene (repr, ungueltige Zeichen gekennzeichnet; ~MLLERR-Zeilen eingeschlossen), ebenso Query_Nano_Info. Zeilen mit '# v1.21'
#   1.20  2026-11-25  BLOCKED_PORTS: Anschluesse, die ein anderes Programm belegt (Query_Info/Query_Nano_Info: Oeffnen mit 'Zugriff verweigert' fehlgeschlagen). Zeilen mit '# v1.20'
#   1.19  2026-11-25  Fehler beim Oeffnen oder Abfragen in Query_Info/Query_Nano_Info stehen im Protokoll (INFO). Zeilen mit '# v1.19'
#   1.18  2026-11-25  Ist ein Anschluss mit dem Hauptprogramm verbunden (Autoconnect der Lichtmaschine), wird er nicht getrennt: Typ/Version (~MLLCFG INFO, ~MLLINFO, Startmeldung des Nano) und MLLIDENT laufen ueber die aktive Verbindung (_Main_Connection). Zeilen mit '# v1.18'
#   1.17  2026-11-25  serial wird beim Laden des Moduls importiert (nicht erst in der ersten Abfrage). Zeilen mit '# v1.17'
#   1.16  2026-11-25  Query_Info protokolliert die Zeiten der Schritte (Sperre, Hauptverbindung, open, CFG, INFO) und erkennt Bootmeldungen nach dem Oeffnen (Reset). Zeilen mit '# v1.16'
#   1.15  2026-11-25  Device_Dialog_Open: Kennzeichen, dass der Dialog Geraeteauswahl offen ist (fuer web_serial). Zeilen mit '# v1.15'
#   1.14  2026-11-25  Query_Nano_Info(): Versionsabfrage fuer klassische Arduinos mit '#?' (LEDs_AutoProg), danach '#X'; das Blinken per DetectArduino setzt waehrend einer Abfrage aus (_SERIAL_LOCK). Zeilen mit '# v1.14'
#   1.13  2026-11-25  _Open_Serial(): DTR/RTS vor open() setzen wie web_serial._open_serial (ESP32/Nano aus: kein Reset; Pico DTR an, RTS unveraendert). Zeilen mit '# v1.13'
#   1.12  2026-11-25  Query_Info: Timeout 1.2 s (0.8 s war fuer einen Pico nach dem Oeffnen zu kurz), zweite Frage kurz, wenn die erste ganz ohne Zeile blieb. Zeilen mit '# v1.12'
#   1.11  2026-11-25  MLLIDENT wird im Hintergrund gesendet (Anschluss exklusiv ueber _SERIAL_LOCK, der Zeitgeber blockiert nicht); Typ und Version in einer Sitzung (Query_Info). Zeilen mit '# v1.11'
#   1.10  2026-11-25  Verbindung des Hauptprogramms wird ueber close_arduino_connection_after_write_error getrennt (Empfangsthread endet sauber; vorher 'Handle ist ungueltig'). Zeilen mit '# v1.10'
#   1.09  2026-11-25  Query_Reply() (gemeinsame Abfrage) und Query_Servo_Info(): PicoServo-Tiny antwortet auf '~MLLINFO' mit 'type=PICOSERVO ver=...'; wird in M07.SERVO_PORTS eingetragen. Zeilen mit '# v1.09'
# ----------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
# *  
# * https://github.com/Hardi-St/MobaLedLib
# *
# * MobaLedCheckColors is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * MobaLedCheckColors is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  if not, see <http://www.gnu.org/licenses/>.
# *
# *
# ***************************************************************************

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *
import logging  # v1.05
import threading  # v1.11
import time  # v1.11
import serial  # v1.17: schon beim Start laden (nicht erst bei der ersten Abfrage)

#import proggen.M02_Public as M02
#import ExcelAPI.X02_Workbook as P01
#import proggen.M08_ARDUINO as M08
#import proggen.M09_Language as M09
#import proggen.M25_Columns as M25
#import proggen.M30_Tools as M30
#import mlpyproggen.U01_userform as U01

import proggen.M02_Public as M02
import proggen.M02a_Public as M02a

#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header as M06
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
#import proggen.M27_Sheet_Icons as M27
#import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Multiplexer as M80

import mlpyproggen.Prog_Generator as PG

import ExcelAPI.XLA_Application as P01

import proggen.M07_COM_Port as M07
import proggen.F00_mainbuttons as F00

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

#Select_COM_Port_UserForm = D08.CSelect_COM_Port_UserForm()

""" Select the Arduino COM Port
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~

 Uses the Modules
 - M07_COM_Port
 - Select_COM_Port_UserForm
------------------------------
--------------------------------------------------------------------------------------
UT-----------------------------------------------------
---------------------------------------------------------------------------------------------
----------------------------------------------------------------
UT-------------------------------
--------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------
 For some reasons this function was available two times.                              30.10.20:
 The second which is located in "M08_Arduino" was defined as "Private"
 Since the functions are nearely equal only one is active now
'---------------------------------------------------------------------------------------------------------------------------------------------------------------
Public Function Check_If_Arduino_could_be_programmed_and_set_Board_type(ComPortColumn As Long, BuildOptColumn As Long, ByRef BuildOptions As String) As Boolean ' 04.05.20:
'---------------------------------------------------------------------------------------------------------------------------------------------------------------
' The "Buzy" check and the automatic board detection is only active if Autodetect is enabled
' Otherwise the values in the BuildOptColumn are used
' Result: BuildOptions
  Dim Start_Baudrate As Long, BaudRate As Long, ComPort As Long, Msg As String, Retry As Boolean, AutoDetect As Boolean

  Do
    Retry = False
    If Check_USB_Port_with_Dialog(ComPortColumn) = False Then Exit Function ' Display Dialog if the COM Port is negativ and ask the user to correct it

    ' Now we are sure that the com port is positiv. Check if it could be accesed and get the Baud rate
    BuildOptions = Cells(SH_VARS_ROW, BuildOptColumn)
    AutoDetect = InStr(BuildOptions, AUTODETECT_STR) > 0
    If AutoDetect Then
       BuildOptions = Trim(Replace(BuildOptions, AUTODETECT_STR, ""))
       If InStr(BuildOptions, BOARD_NANO_OLD) Or InStr(BuildOptions, BOARD_UNO_NORM) > 0 Then  ' Set the Default Baudrate to speed up the check
             Start_Baudrate = 57600
       Else: Start_Baudrate = 115200
       End If
    End If
    ComPort = val(Cells(SH_VARS_ROW, ComPortColumn))
    Dim DeviceSignatur As Long, FirmwareVer As String
    BaudRate = Get_Arduino_Baudrate(ComPort, Start_Baudrate, DeviceSignatur, FirmwareVer)  ' 28.10.20: Jürgen: Added: DeviceSignatur
    If BaudRate <= 0 Then
          If Check_If_Port_is_Available(ComPort) = False Then
                Msg = Get_Language_Str("Fehler: Es ist kein Arduino an COM Port #1# angeschlossen.")
          ElseIf BaudRate = 0 Then
                Msg = Get_Language_Str("Fehler: Das Gerät am COM Port #1# wurde nicht als Arduino erkannt." & vbCr & _
'                                       "Evtl. ist es ein defekter Arduino oder der Bootloader ist falsch.")
          Else: Msg = Get_Language_Str("Fehler: Der COM Port #1# wird bereits von einem anderen Programm benutzt." & vbCr & _
'                                       "Das kann z.B. der serielle Monitor der Arduino IDE oder das Farbtestprogramm sein." & vbCr & _
'                                       vbCr & _
'                                       "Das entsprechende Programm muss geschlossen werden.")
          End If
          Msg = Replace(Msg, "#1#", ComPort) & vbCr & vbCr & Get_Language_Str("Wollen sie es noch mal mit einem anderen Arduino oder einem anderen COM Port versuchen?")
          If MsgBox(Msg, vbYesNo + vbQuestion, Get_Language_Str("Fehler bei der Überprüfung des angeschlossenen Arduinos")) = vbYes Then
                Retry = True
                With Cells(SH_VARS_ROW, ComPortColumn)
                   .Value = -val(.Value) ' Set to a negativ number to show the COM Port dialog
                End With
          Else: Exit Function
          End If
    Else
          If AutoDetect Then
             'If BaudRate <> Start_Baudrate Then ' Change the board type to speed up the check the next time ' 30.10.20: Always update the board type and Baud rate
                Dim NewBrd As String, LeftArduino As Boolean
                If BaudRate = 57600 Then
                      NewBrd = BOARD_NANO_OLD
                Else: ' An UNO can't be detected every time, but it could be programmed like a Nano with the new bootloader
                      NewBrd = Get_New_Board_Type(FirmwareVer)              ' 29.10.20:
                End If

                LeftArduino = (ComPortColumn = COMPort_COL)
                Change_Board_Typ LeftArduino, NewBrd ' Write the new board type
                BuildOptions = Cells(SH_VARS_ROW, BuildOptColumn) ' Reread the Build options in case the board type was adapted
                BuildOptions = Trim(Replace(BuildOptions, AUTODETECT_STR, "")) ' Remove the Autodetect flag
             'End If
          End If
    End If
  Loop While Retry

  Check_If_Arduino_could_be_programmed_and_set_Board_type = True
End Function
"""

__PRINT_DEBUG = False
#CheckCOMPort = Long()
#CheckCOMPort_Txt = String()
__CheckCOMPort_Res = Long()
on_ledon = False
PicoWL = False
OTHER_TYPES = {}                                               # v1.22: Anschluss -> type aus '~MLLINFO' fuer Geraete der Kategorie 'Andere MobaLedLib Geraete' (alles ausser LICHTMASCHINE)
BLOCKED_PORTS = set()                                          # v1.20: Anschluesse, die ein anderes Programm belegt (Oeffnen schlug mit 'Zugriff verweigert' fehl); gilt fuer den Dialog Geraeteauswahl
Device_Dialog_Open = False                                    # v1.15: der Dialog Geraeteauswahl ist offen (setzt web_form_comport): stilles Verbinden ruht
_Dialog_for_Arduino = True                                    # der Dialog gehoert zu einem Arduino (blinkende LEDs): nur dann wird der Anschluss jede Sekunde geoeffnet und geprueft  # v1.03
_Ident_Active = False                                          # v1.05: MLLIDENT aktiv (Dialog offen, MainBoard, Pico/ESP)


def _Probe_Port_by_Opening():  # v1.03
    """Soll der Zeitgeber den gewaehlten Anschluss jede Sekunde oeffnen (DetectArduino: DTR umschalten, Antwort abwarten)? Fuer einen Arduino ja; fuer Pico und ESP32 unter
    Linux und macOS nein: Das Oeffnen und Schliessen jede Sekunde stoert deren USB-Anschluss (Pico: verschwindet, bis man ihn neu einsteckt; ESP32: Zugriff verweigert)."""
    return bool(_Dialog_for_Arduino) or P01.checkplatform("Windows") is True  # v1.03


def _Ident_Board():  # v1.05
    """'esp32' oder 'pico', wenn der Dialog der LED-Zentrale gehoert und sie ein ESP32 oder Pico (ohne WLAN) ist, sonst None. Der Typ kann im Dialog umgestellt werden."""
    if not _Ident_Active:  # v1.05
        return None  # v1.05
    try:  # v1.05
        if InStr(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL), 'WLAN') > 0:  # v1.05
            return None  # v1.05
        Board = M02a.Get_BoardTyp()  # v1.05
    except Exception:                                                  # noqa: BLE001  # v1.05
        return None  # v1.05
    if Board == M02.HT_ESP32:  # v1.05
        return "esp32"  # v1.05
    if Board == M02.HT_PICO:  # v1.05
        return "pico"  # v1.05
    return None  # v1.05


def _Release_Main_Connection(Port):  # v1.10
    """Trennt die Verbindung des Hauptprogramms, wenn sie an diesem Anschluss haengt. Ueber close_arduino_connection_after_write_error,
    damit der Empfangsthread vorher sauber beendet wird; sonst meldet er 'Handle ist ungueltig' (GetOverlappedResult)."""
    try:
        con = PG.global_controller
        old = con.arduino
        if old is not None and getattr(old, "port", None) == Port:
            con.close_arduino_connection_after_write_error(expected_port=old, lock_timeout=0)  # v1.25: wir halten schon die Anschluss-Sperre: nicht auf _conn_lock warten (Reihenfolge der Sperren)
    except Exception:                                          # noqa: BLE001
        logging.getLogger(__name__).debug("Verbindung des Hauptprogramms nicht getrennt", exc_info=True)


# _SERIAL_LOCK = threading.Lock()   # v1.11: ein Zugriff auf einen Anschluss gleichzeitig (MLLIDENT-Thread und Abfrage von Typ und Version)  # v1.25 (entfallen: gemeinsame Sperre mit web_serial)
try:  # v1.25: dieselbe Sperre wie beim Verbinden des Hauptprogramms (web_serial._open_and_handshake) und der Erkennung (M07.DetectArduino): ein Zugriff auf Anschluesse gleichzeitig
    from _web.web_serial import PORT_ACCESS_LOCK as _SERIAL_LOCK  # v1.25
except Exception:                                                  # noqa: BLE001  # v1.25
    _SERIAL_LOCK = threading.RLock()  # v1.25
_IDENT_LOCK = threading.Lock()    # v1.11: schuetzt _IDENT_WANTED
_IDENT_WANTED = {}                # v1.11: Anschluss -> (Board, Cmd): zuletzt gewuenschter Befehl; der MLLIdent-Thread sendet ihn
_IDENT_WAKE = threading.Event()   # v1.11
_IDENT_THREAD = None              # v1.11


def _Ident_Send_Cmd(Port, Board, Cmd):  # v1.05; v1.11: synchron (Stop beim Schliessen des Dialogs); ein noch wartender Befehl fuer den Anschluss entfaellt
    """Sendet '~MLLIDENT 1' (Start) oder '~MLLIDENT 0' (Stop) an Port und wartet, bis er gesendet ist.
    Oeffnet den Anschluss kurz, sendet, schliesst wieder. Kein dauerhaft offener Port."""
    if Port is None:  # v1.05
        return  # v1.05
    with _IDENT_LOCK:  # v1.11
        _IDENT_WANTED.pop(Port, None)  # v1.11
    _Ident_Send_Now(Port, Board, Cmd)  # v1.11


def _Open_Serial(Port, Board, Timeout):  # v1.13
    """Oeffnet den Anschluss ohne CPU-Reset, wie _open_serial in web_serial.py: die Eigenschaften werden VOR open() gesetzt.
    ESP32/Nano (alles ausser 'pico'): DTR und RTS aus (sonst starten sie neu). Pico: DTR bleibt an (sein serieller USB-Anschluss sendet nur mit DTR)."""
    ser = serial.Serial()
    ser.port = Port
    ser.baudrate = 115200
    ser.timeout = Timeout
    ser.write_timeout = 0.5
    if Board != "pico":
        ser.dtr = False
        ser.rts = False
    ser.open()
    return ser


def _Ident_Send_Now(Port, Board, Cmd):  # v1.11
    """Sendet Cmd an Port (Anschluss exklusiv, _SERIAL_LOCK). Fehler werden nur protokolliert."""
    con, _ser = _Main_Connection(Port)
    if con is not None:  # v1.18: der Anschluss ist mit dem Hauptprogramm verbunden: ueber diese Verbindung senden, nicht trennen
        con.send_to_ARDUINO(Cmd + "\n")
        return
    with _SERIAL_LOCK:
        con, _ser = _Main_Connection(Port)  # v1.25: das Hauptprogramm kann waehrend des Wartens verbunden haben: ueber diese Verbindung senden
        if con is not None:  # v1.25
            con.send_to_ARDUINO(Cmd + "\n")  # v1.25
            return  # v1.25
        _Release_Main_Connection(Port)  # v1.10
        ser = None
        try:
            ser = _Open_Serial(Port, Board, 0)  # v1.13
            ser.reset_input_buffer()
            ser.write((Cmd + "\n").encode())
            ser.flush()
        except Exception as e:  # noqa: BLE001
            logging.getLogger(__name__).debug("Ident_Send_Cmd: %s fehlgeschlagen: %s", Port, e)
        finally:
            if ser is not None:
                try:
                    ser.close()
                except Exception:  # noqa: BLE001
                    pass


def _Ident_Worker():  # v1.11: Hintergrund-Thread: sendet die wartenden MLLIDENT-Befehle, der Zeitgeber blockiert nicht
    while True:
        _IDENT_WAKE.wait()
        _IDENT_WAKE.clear()
        with _IDENT_LOCK:
            items = list(_IDENT_WANTED.items())
            _IDENT_WANTED.clear()
        for Port, (Board, Cmd) in items:
            _Ident_Send_Now(Port, Board, Cmd)


def _Ident_Post(Port, Board, Cmd):  # v1.11: nicht blockierend; der Thread sendet den Befehl kurz danach
    global _IDENT_THREAD
    if Port is None:
        return
    with _IDENT_LOCK:
        _IDENT_WANTED[Port] = (Board, Cmd)
    if _IDENT_THREAD is None or not _IDENT_THREAD.is_alive():
        _IDENT_THREAD = threading.Thread(target=_Ident_Worker, name="MLLIdent", daemon=True)
        _IDENT_THREAD.start()
    _IDENT_WAKE.set()


def Ident_Enable(MainBoard):  # v1.05
    """Aktiviert MLLIDENT fuer den Dialog."""
    global _Ident_Active  # v1.05
    _Ident_Active = bool(MainBoard)  # v1.05


def Ident_Stop():  # v1.05
    """Sendet Stop und deaktiviert MLLIDENT (bei OK, Abbruch, Port-Wechsel, vor Upload)."""
    global _Ident_Active  # v1.05
    if _Ident_Active:  # v1.05
        # Port zum Senden des Stop-Commands: aktueller CheckCOMPort (wenn gueltig)  # v1.05
        Port = M07.CheckCOMPort  # v1.05
        if Port and Port not in (" ", "999", -1):  # v1.05
            Board = _Ident_Board()  # v1.05
            if Board:  # v1.05
                _Ident_Send_Cmd(Port, Board, "~MLLIDENT 0")  # v1.05
    _Ident_Active = False  # v1.05


def Ident_Send_Keepalive(Port):  # v1.05
    """Sendet '~MLLIDENT 1' waehrend der Polling-Schleife (__Blink_Arduino_LED)."""
    if not _Ident_Active:  # v1.05
        return  # v1.05
    if not Port or Port in (" ", "999", -1):  # v1.05
        return  # v1.05
    Board = _Ident_Board()  # v1.05
    if Board:  # v1.05
        _Ident_Post(Port, Board, "~MLLIDENT 1")  # v1.11: nicht blockierend (Zeitgeber)

def _Is_Blocked(e):  # v1.20
    """Schlug das Oeffnen fehl, weil ein anderes Programm den Anschluss belegt (Windows: PermissionError 13 'Zugriff verweigert'; Linux/macOS: Errno 13/11/16)?"""
    t = str(e)
    return isinstance(e, PermissionError) or any(k in t for k in ("PermissionError", "Zugriff", "Access is denied", "Errno 13", "Errno 11", "Errno 16", "Permission denied", "busy"))


def _Main_Connection(Port):  # v1.18
    """Aktive Verbindung des Hauptprogramms (zum Beispiel Autoconnect der Lichtmaschine) an diesem Anschluss: (Controller, Port-Objekt), sonst (None, None).
    Ein verbundener Anschluss wird nicht getrennt, sondern ueber diese Verbindung abgefragt und angesprochen."""
    try:
        con = PG.global_controller
        ser = con.arduino
        if (ser is not None and getattr(ser, "is_open", False) and str(getattr(ser, "port", "") or "").upper() == str(Port).upper() and con.is_connection_open()
                and str(getattr(con, "ARDUINO_current_portname", "") or "").upper() == str(Port).upper()):  # v1.25: erst nach dem Handshake (sonst stoert eine Abfrage den Verbindungsaufbau)
            BLOCKED_PORTS.discard(str(Port))  # v1.20
            return con, ser
    except Exception:  # noqa: BLE001
        logging.getLogger(__name__).debug("Hauptverbindung nicht lesbar", exc_info=True)
    return None, None


def _Kv(line, Prefix):  # v1.18
    """'k=v'-Paare hinter Prefix als Dict; None, wenn Prefix nicht in der Zeile steht."""
    p = line.find(Prefix)
    if p < 0:
        return None
    info = {}
    for part in line[p + len(Prefix):].split():
        if "=" in part:
            k, v = part.split("=", 1)
            info[k] = v.strip()
    return info


def _Main_Ask(con, lines, Cmd, Prefix, Timeout):  # v1.18
    """Schickt Cmd ueber die Hauptverbindung und wartet auf die Zeile mit Prefix (die Empfangszeilen sammelt ein rx_listener in lines). None bei '~MLLERR' oder ohne Antwort."""
    mark = len(lines)
    con.send_to_ARDUINO(Cmd + "\n")
    deadline = time.monotonic() + Timeout
    while time.monotonic() < deadline:
        for line in list(lines[mark:]):
            if "~MLLERR" in line:
                return {"_err": "1"}
            info = _Kv(line, Prefix)
            if info is not None:
                return info
        time.sleep(0.01)
    return None


def _Finish_Info(Port, cfg_raw, fw):  # v1.18
    """Antworten von '~MLLCFG INFO' und '~MLLINFO' auswerten: (cfg, fw); ein Servo-Modul wird in M07.SERVO_PORTS eingetragen."""
    cfg = None
    if cfg_raw and "sig" in cfg_raw:
        cfg = {"proto": cfg_raw.get("proto", ""), "sig": cfg_raw["sig"], "valid": cfg_raw.get("valid") == "1", "free": cfg_raw.get("free", "")}
    t = fw.get("type") if fw else None
    if t and t != "LICHTMASCHINE" and cfg is None:  # v1.22: jeder andere type ist ein Geraet der Kategorie 'Andere MobaLedLib Geraete' (nicht als Lichtmaschine waehlbar)
        M07.SERVO_PORTS[Port] = fw.get("ver", "")  # (Name historisch: Liste aller 'anderen' Geraete)
        OTHER_TYPES[Port] = t
    elif cfg is not None or t == "LICHTMASCHINE":
        M07.SERVO_PORTS.pop(Port, None)
        OTHER_TYPES.pop(Port, None)
    return cfg, fw


def _Query_Info_Main(con, Port, Timeout):  # v1.18
    """Wie Query_Info, aber ueber die aktive Verbindung des Hauptprogramms (kein Trennen, kein Oeffnen des Anschlusses)."""
    lines = []

    def listener(text):
        lines.append(str(text).strip())
    cfg_raw = None
    fw = None
    t0 = time.monotonic()
    con.rx_listeners.append(listener)
    try:
        cfg_raw = _Main_Ask(con, lines, "~MLLCFG INFO", "~MLLCFG INFO ", Timeout)
        t1 = time.monotonic()
        fw = _Main_Ask(con, lines, "~MLLINFO", "~MLLINFO ", Timeout if cfg_raw is not None else 0.4)
    except Exception as e:  # noqa: BLE001
        logging.getLogger(__name__).debug("Query_Info (aktive Verbindung) an %s: %s", Port, e)
        t1 = time.monotonic()
    finally:
        try:
            con.rx_listeners.remove(listener)
        except ValueError:
            pass
    logging.getLogger(__name__).info("Query_Info %s: ueber die aktive Verbindung, CFG %.0f ms, INFO %.0f ms", Port, (t1 - t0) * 1000, (time.monotonic() - t1) * 1000)
    return _Finish_Info(Port, cfg_raw, fw)


def _Main_Nano_Text(con):  # v1.18
    """Startmeldung des Arduinos der aktiven Verbindung ('LEDs_AutoProg Ver 3: ...', beim Verbinden mit '#?' gelesen), sonst None."""
    t = str(getattr(con, "ARDUINO_startmessage", "") or "").strip()
    if t.startswith("#?"):
        t = t[2:]
    return t if t.startswith("LEDs_AutoProg") else None


def _Parse_Nano(text):  # v1.18
    """Startmeldung 'LEDs_AutoProg Ver 3: <Board> <MobaLedLib-Version> <Datum> <Zeit>,<LEDs je Kanal>' auswerten: {'ver','board','date','text'} oder None."""
    import re
    if not text:
        return None
    m = re.search(r"Ver (\d+):\s*(.*)", text)
    rest = (m.group(2) if m else text).split(",")[0]
    v = re.search(r"\b(\d+\.\d+(?:\.\d+)?[A-Za-z0-9]*)\b", rest)
    toks = rest.split()
    return {"ver": v.group(1) if v else "", "board": toks[0] if toks else "", "date": " ".join(toks[-2:]) if len(toks) >= 3 else "", "text": text}


def _Ask(ser, Cmd, Prefix, Timeout, seen=None):  # v1.11; v1.16: seen sammelt ueberlesene Zeilen (Bootmeldungen)
    """Schickt Cmd und liest bis zur Antwortzeile mit Prefix. Ergebnis: 'k=v'-Paare hinter Prefix als Dict; None bei '~MLLERR' oder ohne Antwort innerhalb Timeout Sekunden."""
    ser.reset_input_buffer()
    ser.write((Cmd + "\n").encode())
    ser.flush()
    deadline = time.monotonic() + Timeout
    while time.monotonic() < deadline:
        raw = ser.readline()
        line = raw.decode("ascii", errors="replace")
        if seen is not None and raw.strip() and len(seen) < 10:  # v1.21: alles Empfangene merken (auch ungueltige Zeichen), Query_Info protokolliert es ohne Antwort
            bad = any(b > 126 or (b < 32 and b not in (9, 10, 13)) for b in raw)
            seen.append(("UNGUELTIGE ZEICHEN " if bad else "") + repr(bytes(raw[:80])))
        if "~MLLERR" in line:  # Firmware kennt den Befehl nicht (antwortet aber)
            return {"_err": "1"}
        p = line.find(Prefix)
        if p < 0:  # andere Zeilen (MLLIDENT-Echo, Meldungen) ueberlesen
            continue
        info = {}
        for part in line[p + len(Prefix):].split():
            if "=" in part:
                k, v = part.split("=", 1)
                info[k] = v.strip()
        return info
    return None


def Query_Info(Port, Board, Timeout=1.2):  # v1.11
    """Fragt ESP32/Pico/Servo-Modul in EINER Sitzung ab (ein Oeffnen des Anschlusses): '~MLLCFG INFO' und '~MLLINFO'.
    Liefert (cfg, fw): cfg = {'proto','sig','valid','free'} (Lichtmaschine mit MLLDynConfig) oder None;
    fw = {'type','platform','ver'} (type=LICHTMASCHINE oder PICOSERVO) oder None.
    Ein Servo-Modul wird in M07.SERVO_PORTS eingetragen: es ist dann nicht als Lichtmaschine waehlbar.
    v1.16: Die Zeiten der einzelnen Schritte (Sperre, Hauptverbindung trennen, Oeffnen, Antworten) stehen im Protokoll; Bootmeldungen, die nach dem Oeffnen kommen
    (ESP32: 'rst:', 'ets ', 'ESP-ROM'), zeigen einen Reset durch das Oeffnen."""
    cfg_raw = None
    fw = None
    if not Port or Port in (" ", "999", -1):
        return None, None
    con, _ser = _Main_Connection(Port)
    if con is not None:  # v1.18: aktive Verbindung des Hauptprogramms benutzen
        return _Query_Info_Main(con, Port, Timeout)
    seen = []
    marks = []
    t0 = time.monotonic()
    with _SERIAL_LOCK:
        marks.append(("Sperre", time.monotonic() - t0))
        con, _ser = _Main_Connection(Port)  # v1.25: das Hauptprogramm kann waehrend des Wartens auf die Sperre verbunden haben
        if con is None:  # v1.25
            t1 = time.monotonic()
            _Release_Main_Connection(Port)
            marks.append(("Hauptverbindung", time.monotonic() - t1))
            ser = None
            try:
                t1 = time.monotonic()
                ser = _Open_Serial(Port, Board, 0.1)  # v1.13
                BLOCKED_PORTS.discard(str(Port))  # v1.20
                marks.append(("open", time.monotonic() - t1))
                t1 = time.monotonic()
                cfg_raw = _Ask(ser, "~MLLCFG INFO", "~MLLCFG INFO ", Timeout, seen)
                marks.append(("CFG", time.monotonic() - t1))
                t1 = time.monotonic()
                fw = _Ask(ser, "~MLLINFO", "~MLLINFO ", Timeout if cfg_raw is not None else 0.4, seen)   # blieb die erste Frage ganz ohne Zeile, ist das Geraet vermutlich still
                marks.append(("INFO", time.monotonic() - t1))
            except Exception as e:  # noqa: BLE001
                if _Is_Blocked(e):  # v1.20
                    BLOCKED_PORTS.add(str(Port))
                logging.getLogger(__name__).info("Query_Info %s (%s): Fehler beim Oeffnen oder Abfragen: %r", Port, Board, e)  # v1.19: sichtbar (vorher nur DEBUG)
            finally:
                if ser is not None:
                    try:
                        ser.close()
                    except Exception:  # noqa: BLE001
                        pass
    if con is not None:  # v1.25: aktive Verbindung benutzen (ausserhalb der Sperre: die Antwort dauert)
        return _Query_Info_Main(con, Port, Timeout)  # v1.25
    boot = next((l for l in seen if "rst:" in l or "ets " in l or "ESP-ROM" in l or "boot:" in l), None)  # v1.16
    positive = bool(fw and fw.get("type")) or bool(cfg_raw and "sig" in cfg_raw)  # v1.21
    extra = "" if positive or not seen else ", Empfangen: " + " | ".join(seen)  # v1.21: ohne gueltige Antwort alles Empfangene zeigen
    logging.getLogger(__name__).info("Query_Info %s (%s): %s%s%s", Port, Board, ", ".join("%s %.0f ms" % (k, v * 1000) for k, v in marks),
                                     (", RESET beim Oeffnen erkannt (Bootmeldung: %s)" % boot) if boot else "", extra)  # v1.16
    return _Finish_Info(Port, cfg_raw, fw)


def Query_Nano_Info(Port, Timeout=1.5):  # v1.14
    """Klassischer Arduino (Nano/Uno) mit LEDs_AutoProg: '#?' (LEDs_AutoProg.ino, Receive_LED_Color_per_RS232; wie web_serial: '#?' mehrmals, danach '#X').
    Antwort: '#?LEDs_AutoProg Ver 3: <Board> <MobaLedLib-Version> <Datum> <Zeit>,<LEDs je Kanal>'. Danach wird '#X' gesendet (verlaesst den Farbmodus ohne Neustart).
    Der Anschluss wird ohne Reset geoeffnet (DTR/RTS aus, _Open_Serial). Liefert {'ver','board','date','text'} oder None (keine Antwort, belegt)."""
    import re
    if not Port or Port in (" ", "999", -1):
        return None
    con, _ser = _Main_Connection(Port)
    if con is not None:  # v1.18: aktive Verbindung: die beim Verbinden gelesene Startmeldung auswerten, nichts senden
        return _Parse_Nano(_Main_Nano_Text(con))
    text = None
    with _SERIAL_LOCK:
        con, _ser = _Main_Connection(Port)  # v1.25: das Hauptprogramm kann waehrend des Wartens auf die Sperre verbunden haben
        if con is None:  # v1.25
            _Release_Main_Connection(Port)
            ser = None
            try:
                ser = _Open_Serial(Port, "nano", 0.1)
                BLOCKED_PORTS.discard(str(Port))  # v1.20
                ser.reset_input_buffer()
                deadline = time.monotonic() + Timeout
                next_send = 0.0
                buf = ""
                while time.monotonic() < deadline and text is None:
                    now = time.monotonic()
                    if now >= next_send:
                        ser.write(b"#?\r\n")
                        ser.flush()
                        next_send = now + 0.7
                    buf += ser.read(ser.in_waiting or 1).decode("ascii", errors="replace")
                    p = buf.find("#?LEDs_AutoProg")
                    if p >= 0:
                        e = buf.find("\n", p)
                        if e >= 0:
                            text = buf[p + 2:e].strip()
                if text is None and buf:  # v1.21: keine gueltige Antwort: Empfangenes protokollieren
                    bad = any(ord(c) > 126 or (ord(c) < 32 and c not in "\t\r\n") for c in buf)
                    logging.getLogger(__name__).info("Query_Nano_Info %s: keine gueltige Antwort, empfangen: %s%r", Port, "UNGUELTIGE ZEICHEN " if bad else "", buf[:120])
                ser.write(b"#X\r\n")                                   # Farbmodus beenden (auch ohne Antwort: harmlos)
                ser.flush()
            except Exception as e:  # noqa: BLE001
                if _Is_Blocked(e):  # v1.20
                    BLOCKED_PORTS.add(str(Port))
                logging.getLogger(__name__).info("Query_Nano_Info %s: Fehler beim Oeffnen oder Abfragen: %r", Port, e)  # v1.19: sichtbar (vorher nur DEBUG)
            finally:
                if ser is not None:
                    try:
                        ser.close()
                    except Exception:  # noqa: BLE001
                        pass
    if con is not None:  # v1.25
        return _Parse_Nano(_Main_Nano_Text(con))  # v1.25
    return _Parse_Nano(text)


def Query_Nano_Bootloader(Port):  # v1.23
    """Bootloader eines Nano ermitteln (STK500 wie 'Board und USB Port erkennen': 57600 Baud = alter, 115200 Baud = neuer Bootloader, optiboot 108.1 = Full memory).
    Liefert die Board-Option (M02.BOARD_NANO_OLD, BOARD_NANO_NEW, BOARD_NANO_FULL) oder None (keine Antwort, belegt, Pruefung in den Einstellungen aus, aktive Verbindung).
    Der Arduino wird dabei per DTR zurueckgesetzt (so spricht man den Bootloader an); eine aktive Verbindung des Hauptprogramms wird deshalb nicht angefasst."""
    log = logging.getLogger(__name__)
    if not Port or Port in (" ", "999", -1):
        return None
    if not M07.Detect_Bootloader_Enabled():
        log.info("Bootloader-Abfrage %s: in den Einstellungen ausgeschaltet", Port)
        return None
    con, _ser = _Main_Connection(Port)
    if con is not None:
        log.info("Bootloader-Abfrage %s: aktive Verbindung des Hauptprogramms, nicht abgefragt", Port)
        return None
    t0 = time.monotonic()
    with _SERIAL_LOCK:
        con, _ser = _Main_Connection(Port)  # v1.25: das Hauptprogramm kann waehrend des Wartens auf die Sperre verbunden haben
        if con is not None:  # v1.25
            log.info("Bootloader-Abfrage %s: aktive Verbindung des Hauptprogramms, nicht abgefragt", Port)  # v1.25
            return None  # v1.25
        M07.BOOTLOADER_CACHE.pop(str(Port).upper(), None)  # v1.24: frisch abfragen, kein alter Wert
        baud = M07.Get_Arduino_Baudrate(Port, 115200, 0, "")
        fw, sig = M07.Get_Last_Detect_Info()
        if baud and baud > 0:  # v1.24: die Pruefung nach OK (Check_If_Arduino_could_be_programmed...) nutzt dieses Ergebnis, ohne den Nano noch einmal zurueckzusetzen
            M07.BOOTLOADER_CACHE[str(Port).upper()] = (time.monotonic(), baud, fw, sig)
    board = None
    if baud == 57600:
        board = M02.BOARD_NANO_OLD
    elif baud == 115200:
        board = M08.Get_New_Board_Type(fw, sig)
    log.info("Bootloader-Abfrage %s: Baudrate %s, Firmware '%s', Signatur 0x%06X, Board %s, %.0f ms", Port, baud, fw, sig or 0, board, (time.monotonic() - t0) * 1000)
    return board


def __Blink_Arduino_LED():
    global __CheckCOMPort_Res, on_ledon
    
    SWMajorVersion = Byte()

    SWMinorVersion = Byte()

    HWVersion = Byte()

    DeviceSignatur = Long()

    BaudRate = Long()
    #------------------------------
    # Is called by OnTime and flashes the LEDs of the Arduino connected to
    # the port stored in the global variable "CheckCOMPort"
    # It's aborted if CheckCOMPort = "-1 "
    # Attention: This function doesn't check if the connected device is an Arduino
    # because this would be to slow. In addition the blinking frequence is more visible if
    # A baudrate of 50 is used.
    BaudRate = 50
    
    #if M07.CheckCOMPort > 0:
    Debug.Print("__Blink_Arduino_LED - CheckComPort:"+str(M07.CheckCOMPort))
    if F00.port_is_available(M07.CheckCOMPort):    
        Debug.Print("Blink_LED start")
        F00.Select_COM_Port_UserForm.Update_SpinButton(0)
        # Rescan COM Ports
        if not M07.CheckCOMPort.startswith("IP:"):
            if M07.CheckCOMPort != "999":
                # __CheckCOMPort_Res, DeviceSignatur = M07.DetectArduino(M07.CheckCOMPort, BaudRate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur, 1, PrintDebug= __PRINT_DEBUG)  # v1.03 (entfallen)
                # v1.05: ESP32/Pico (LED-Zentrale): MLLIDENT statt DetectArduino.
                # Fuer Pico/ESP (Zentrale): MLLIDENT KeepAlive ueber Polling senden (Ident_Send_Keepalive),  # v1.05
                # KEIN DetectArduino (Port-Konflikt vermeiden).  # v1.05
                # Fuer Arduino (klassisch): DetectArduino mit 50 Baud fuer Blinken.  # v1.05
                Ident_Send_Keepalive(M07.CheckCOMPort)  # v1.05: MLLIDENT 1 senden falls aktiv
                IdentBoard = _Ident_Board()  # v1.05
                if IdentBoard is None:  # Arduino (klassisch): DetectArduino mit 50 Baud fuer Blinken  # v1.05
                    if _Probe_Port_by_Opening():  # v1.03  # v1.05
                        if _SERIAL_LOCK.acquire(timeout=0.2):  # v1.14: waehrend einer Abfrage von Typ/Version nicht gleichzeitig am Anschluss
                            try:
                                __CheckCOMPort_Res, DeviceSignatur = M07.DetectArduino(M07.CheckCOMPort, BaudRate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur, 1, PrintDebug= __PRINT_DEBUG)  # v1.03  # v1.05
                            finally:
                                _SERIAL_LOCK.release()
                        else:
                            __CheckCOMPort_Res = 1  # v1.14: Abfrage laeuft: diesmal nicht blinken
                    else:  # v1.03  # v1.05
                        __CheckCOMPort_Res = 1                                   # Pico, ESP32 (Linux, macOS): der Anschluss steht in der Liste, mehr wird nicht geprueft  # v1.03  # v1.05
                else:  # v1.03
                    __CheckCOMPort_Res = 1  # Pico/ESP: MLLIDENT laeuft, Erkennung ok  # v1.05
            else:
                Ident_Send_Keepalive(None)  # v1.05: 999 = kein Port gewaehlt
                __CheckCOMPort_Res = - 9
            #*HLApplication.Cursor = xlNorthwestArrow
            #Debug.Print "CheckCOMPort_Res=" & CheckCOMPort_Res & "  CheckCOMPort=" & CheckCOMPort
            if __CheckCOMPort_Res < 0:
                if M07.CheckCOMPort == "999": #999:
                    if PicoWL:
                        F00.Select_COM_Port_UserForm.Show_Status(True, M09.Get_Language_Str('Kein PICO WL (mDNS Gerät) erkannt.' + vbCr + 'Bitte PICO WL einschalten'))

                    else:
                        # F00.Select_COM_Port_UserForm.Show_Status(True, Replace(M09.Get_Language_Str("Kein COM Port erkannt." + vbCr + "Bitte #1 an einen USB Anschluss des Computers anschließen"), "#1", M08.GetArduName()))  # v1.06 (entfallen)
                        F00.Select_COM_Port_UserForm.Show_Status(True, M09.Get_Language_Str("Kein COM Port erkannt.", False, M09.xlWhole) + vbCr + M09.Get_Language_Str("Bitte Gerät an einen USB Anschluss des Computers anschließen", False, M09.xlWhole))  # v1.06: Gerät statt 'LED Arduino'
                else:
                    # F00.Select_COM_Port_UserForm.Show_Status(True, Replace(M09.Get_Language_Str("Achtung: Der #1 wird von einem anderen Programm benutzt." + vbCr + "(Serieller Monitor?)" + vbCr + "Das Programm muss geschlossen werden! "), "#1", M08.GetArduName()))  # v1.07 (entfallen)
                    F00.Select_COM_Port_UserForm.Show_Status(True, M09.Get_Language_Str("Achtung: Das Gerät wird von einem anderen Programm benutzt.", False, M09.xlWhole) + vbCr  # v1.07: Gerät statt 'LED Arduino'
                                                             + M09.Get_Language_Str("(Serieller Monitor?)", False, M09.xlWhole) + vbCr + M09.Get_Language_Str("Das Programm muss geschlossen werden!", False, M09.xlWhole))  # v1.07
            else:
                F00.Select_COM_Port_UserForm.Show_Status(False, M07.CheckCOMPort_Txt)
        else:
            Ident_Send_Keepalive(None)  # v1.05
            F00.Select_COM_Port_UserForm.Show_Status(False, M07.CheckCOMPort_Txt)
        # Test_IsPicoInBootMode()  # v1.03 (entfallen)
        try:                                                               # eine Ausnahme darf den Zeitgeber nicht beenden: er aktualisiert auch die Liste der Anschluesse  # v1.03
            Test_IsPicoInBootMode()  # v1.03
        except Exception:                                              # noqa: BLE001  # v1.03
            logging.getLogger(__name__).exception("Pruefung auf einen Pico im Bootmodus fehlgeschlagen")  # v1.03
        #*HL Sleep(10)
        P01.DoEvents()
        if M07.CheckCOMPort.startswith("IP:"):
            # try to connet to device
            #try to switch on LED
            try:
                PG.global_controller.connectIP(IPAdresse=M07.CheckCOMPort[3:])

                if on_ledon:
                    PG.global_controller.send_ledcolor_to_ARDUINO(1, 1, "#FFFFFF")
                    on_ledon = False
                else:
                    PG.global_controller.send_ledcolor_to_ARDUINO(1, 1, "#000000")
                    on_ledon = True
            except BaseException as e:
                print (e)
                
        if M07.CheckCOMPort != -1:  
            P01.Application.OnTime(1000, __Blink_Arduino_LED)
        Debug.Print("Blink_LED end")

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort_IO - ByRef 
# def Select_Arduino_w_Blinking_LEDs_Dialog(Caption, Title, Text, Picture, IsArduino, Buttons, ComPort_IO):  # v1.05 (entfallen)
def Select_Arduino_w_Blinking_LEDs_Dialog(Caption, Title, Text, Picture, IsArduino, Buttons, ComPort_IO, MainBoard=False):  # v1.05: MainBoard: der Dialog gehoert zur LED-Zentrale (ESP32/Pico: Erkennen per MLLIdentify)
    # global __CheckCOMPort_Res, PicoWL  # v1.03 (entfallen)
    global __CheckCOMPort_Res, PicoWL, _Dialog_for_Arduino  # v1.03
    fn_return_value = None
    Res = Long()
    hint = String()
    _Dialog_for_Arduino = bool(IsArduino)  # v1.03
    #--------------------------------------------------------------------------------------
    # This function is called if several Arduinos have been detected
    # or if the COM port of the actual Arduino is buzy
    # Variables:
    #  Caption     Dialog Caption
    #  Title       Dialog Title
    #  Text        Message in the text box on the top left side
    #  Picture     Name of the picture to be shown. Available pictures: "LED_Image", "CAN_Image", "Tiny_Image", "DCC_Image"
    #  Buttons     List of 3 buttons with Accelerator. Example "H Hallo; A Abort; O Ok"  Two Buttons: " ; A Abort; "O Ok"
    #  ComPort_IO  is used as input and output. Negativ numbe if it's buzy (Used by an other program)
    # Return:
    #  1: If the left   Button is pressed  (Install, ...)
    #  2: If the middle Button is pressed  (Abort)
    #  3: If the right  Button is pressed  (OK)
    M07.CheckCOMPort = "999" #999
    Ident_Enable(MainBoard)  # v1.05
    P01.Application.OnTime(1000, __Blink_Arduino_LED)
    #__Blink_Arduino_LED()
    # Return values of Select_COM_Port_UserForm.ShowDialog:
    #  -1: If Abort is pressed
    #   0: If No COM Port is available
    #  >0: Selected COM Port
    # The variable "CheckCOMPort_Res" is >= 0 if the Port is available
    if IsArduino:
        # hint = M09.Get_Language_Str(( 'Tipp: Der ausgewählte Arduino blinkt schnell' )) #VBA Error?  # v1.06 (entfallen: Hinweis ganz entfernt)
        hint = ''  # v1.06
        PicoWL = False
    else:
        hint = ''
        PicoWL = False # True
    fn_return_value, ComPort_IO = F00.Select_COM_Port_UserForm.ShowDialog(Caption, Title, Text, Picture, Buttons, '', True, hint, ComPort_IO, __PRINT_DEBUG)
    Ident_Stop()  # v1.05: Blinken beenden und den Anschluss freigeben (z.B. fuer das Hochladen)
    if __CheckCOMPort_Res < 0:
        ComPort_IO = F00.port_set_busy(ComPort_IO)
        # Port is buzy
    P01.Application.Cursor = 0 #*HL xlDefault
    try:
        
        PG.global_controller.send_ledcolor_to_ARDUINO(1, 1, "#000000")
    except:
        pass
    return fn_return_value, ComPort_IO

def __Test_Select_Arduino_w_Blinking_LEDs_Dialog():
    ComPort = Long()
    #UT-----------------------------------------------------
    ComPort = 3
    Debug.Print('Res=' + Select_Arduino_w_Blinking_LEDs_Dialog('LED_Image"Auswahl des Com Ports', 'New Title', 'Mit diesem Dialog wird der COM Port gewählt an den der Arduino angeschlossen ist.', 'LED_Image', 'H Hallo;T Test;O O', ComPort))
    Debug.Print('ComPort=' + ComPort)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort - ByRef 
def Show_USB_Port_Dialog(ComPortColumn, ComPort):
    M08.AskBootPico = True                         # wie im Excel-Programm: solange der Dialog offen ist, nach einem Pico im Bootmodus fragen  # v1.01
    fn_return_value = False
    Res = Long()

    Picture = String()

    ArduName = String()
    #---------------------------------------------------------------------------------------------
    #ComPort = P01.val(P01.Cells(M02.SH_VARS_ROW, ComPortColumn))
    ComPort = P01.Cells(M02.SH_VARS_ROW, ComPortColumn)
    IsArduino = True    # 06.03.23: Juergen for better ESP selection
    if F00.port_is_busy(ComPort):
        F00.port_reset(ComPort)
    #if ComPort < 0:
    #    ComPort = - ComPort
    #if ComPort > 255:                       # 03.03.22: Juergen avoid overrun error
    #    ComPort = 0
    if (ComPortColumn == M25.COMPort_COL):
        if M02a.Get_BoardTyp() == M02.HT_ESP32:
            Picture = 'ESP32_Image'
            M08.SetArduName()
            IsArduino = False
        elif M02a.Get_BoardTyp() == M02.HT_PICO:
            Picture = "PICO_Image"
            M08.SetArduName()
            IsArduino = False            
        elif  InStr(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL), 'WLAN') > 0:
            Picture = "PICOWL_Image"
            M08.SetArduName("PICOWL")
            IsArduino = False
        else:
            Picture = 'LED_Image'
            # M08.SetArduName('LED Arduino')  # v1.04 (entfallen: ergab 'LED Arduino Arduino')
            M08.SetArduName('LED')  # v1.04
    elif (ComPortColumn == M25.COMPrtR_COL):
        Picture = 'DCC_image'
        M08.SetArduName(M25.Page_ID)
    elif (ComPortColumn == M25.COMPrtT_COL):
        Picture = 'Tiny_image'
        M08.SetArduName('ISP')
    else:
        P01.MsgBox('Internal Error: Unsupported  ComPortColumn=' + str(ComPortColumn) + ' in \'USB_Port_Dialog()\'', vbCritical, 'Internal Error')
        M30.EndProg()
        
    Text = Replace(M09.Get_Language_Str("Es wird der COM Port überprüft " + "bzw. ausgewählt, an den der #1# angeschlossen ist."), "#1#", M08.GetArduName())
               
    if IsArduino:
        # Text = Text + vbCr + vbCr + M09. Get_Language_Str("OK, wenn die LEDs am richtigen Arduino schnell blinken.")  # v1.07 (entfallen)
        Text = Text + vbCr + vbCr + M09.Get_Language_Str("OK, wenn die LEDs am richtigen Gerät schnell blinken.", False, M09.xlWhole)  # v1.07: Gerät statt Arduino
    elif Picture in ('ESP32_Image', 'PICO_Image'):  # v1.05
        Text = Text + vbCr + vbCr + Replace(M09.Get_Language_Str("OK, wenn die LEDs auf der Hauptplatine des richtigen #1# schnell blinken."), "#1#", M08.GetArduName())  # v1.05
      
    # Res, ComPort = Select_Arduino_w_Blinking_LEDs_Dialog(M09.Get_Language_Str("Überprüfung des USB Ports"), M09.Get_Language_Str("Auswahl des COM Ports"), Text, Picture, IsArduino, M09.Get_Language_Str(' ; A Abbruch; O Ok'), ComPort)  # v1.05 (entfallen)
    # Res, ComPort = Select_Arduino_w_Blinking_LEDs_Dialog(M09.Get_Language_Str("Überprüfung des USB Ports"), M09.Get_Language_Str("Auswahl des COM Ports"), Text, Picture, IsArduino, M09.Get_Language_Str(' ; A Abbruch; O Ok'), ComPort, MainBoard=(ComPortColumn == M25.COMPort_COL))  # v1.05  # v1.06 (entfallen)
    Res, ComPort = Select_Arduino_w_Blinking_LEDs_Dialog(M09.Get_Language_Str("Überprüfung des USB Ports"), M09.Get_Language_Str("Geräteauswahl", False, M09.xlWhole), Text, Picture, IsArduino, M09.Get_Language_Str(' ; A Abbruch; O Ok'), ComPort, MainBoard=(ComPortColumn == M25.COMPort_COL))  # v1.05  # v1.06: Titel Geräteauswahl
    fn_return_value = ( Res == 3 )
    return fn_return_value, ComPort

def USB_Port_Dialog(ComPortColumn):
    fn_return_value = False
    ComPort = Long()
    #----------------------------------------------------------------
    res, ComPort= Show_USB_Port_Dialog(ComPortColumn, ComPort)
    if res:
        #if IsNumeric(ComPort):
        if F00.port_is_available(ComPort):
            #if int(ComPort) > 0:
            fn_return_value = True
        M07.ComPortPage().CellDict[M02.SH_VARS_ROW, ComPortColumn] = ComPort
        P01.ActiveSheet.Redraw_table()
    return fn_return_value

def __Test_USB_Port_Dialog():
    #UT-------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    M25.Make_sure_that_Col_Variables_match()
    USB_Port_Dialog(M25.COMPort_COL)
    #USB_Port_Dialog COMPrtR_COL
    #USB_Port_Dialog COMPrtT_COL  ' Could only be used im the Pattern_COnfigurator

def Detect_Com_Port(RightSide=False, Pic_ID='DCC'):
    fn_return_value = " "#None
    Res = Boolean()

    ComPortColumn = Long()

    ComPort = Long()
    #--------------------------------------------------------------------------------------------------------
    if RightSide:
        ComPortColumn = M25.COMPrtR_COL
    else:
        ComPortColumn = M25.COMPort_COL
    
    #if __Show_USB_Port_Dialog(ComPortColumn, ComPort):
    res, ComPort= Show_USB_Port_Dialog(ComPortColumn, ComPort)
    if res:        
        fn_return_value = ComPort
    return fn_return_value

def __Test_Check_If_Arduino_could_be_programmed_and_set_Board_type():
    BuildOptions = String()

    DeviceSignature = Long()
    #-------------------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
    # TinyUniProg
    with_0 = P01.Cells(M02.SH_VARS_ROW, M25.BuildOT_COL)
    if with_0.Value == '':
        with_0.Value = 115200
    Debug.Print(M08.Check_If_Arduino_could_be_programmed_and_set_Board_type(M25.COMPrtT_COL, M08.BuildOT_COL, BuildOptions, DeviceSignature) + ' BuildOptions: ' + BuildOptions)
    
def Test_IsPicoInBootMode():                                                          # 28.11.2025 Juergen
    """Ist ein Pico im Bootmodus (Laufwerk RPI-RP2) angeschlossen? Dann fragen, ob er mit der Start-Firmware (Boards/Heartbeat.uf2) initialisiert werden soll."""  # v1.01
    import time  # v1.01
    import proggen.M12_Copy_Prog as M12                                              # hier, nicht oben: sonst ein Kreis der Importe  # v1.02
    if not M08.AskBootPico:
        return
# def test_is_pico_in_boot_mode():  # v1.01 (entfallen)
    drive_letters, drive_names, cnt = M30.enum_disk_drives(False)  # v1.01
    for i in range(cnt):  # v1.01
        message = M09.Get_Language_Str("PICO im Bootmodus gefunden\nSoll der PICO mit einer Start-Firmware initialisiert werden?")  # v1.01
        title = M09.Get_Language_Str("Aktualisieren der MobaLedLib")  # v1.01
        if P01.MsgBox(message, vbQuestion + vbYesNo, title) != vbYes:  # v1.01
            M08.AskBootPico = False  # v1.01
            return  # v1.01
        M08.AskBootPico = False                                                       # nur einmal fragen; das Laufwerk verschwindet, wenn der Pico neu startet  # v1.01
        try:  # v1.01
            M12.FileCopy_with_Check(drive_letters[i] + "/", "Heartbeat.uf2", M08.GetWorkbookPath() + "/Boards/Heartbeat.uf2")  # v1.01
        except Exception as ex:                                                       # noqa: BLE001  # v1.01
            P01.MsgBox(M09.Get_Language_Str("Die Start-Firmware konnte nicht geschrieben werden: ") + str(ex), vbCritical, title)  # v1.01
            return  # v1.01
        time.sleep(3)                                                                 # warten, bis der Pico neu gestartet hat  # v1.01
        return  # v1.01

def _test_is_pico_in_boot_mode_alt():  # v1.01
    # Early exit
    if not M08.AskBootPico:
        return

    # Enumerate USB drives
    drive_letters, drive_names = EnumDiskDrives(include_usb=True)
    cnt = len(drive_letters)

    Debug.Print(f"Anzahl gefundener USB-Laufwerke: {cnt}")

    for i in range(cnt):
        Debug.Print(f"Laufwerk {drive_letters[i]} - {drive_names[i]}")

        # Ask user for confirmation
        message = (
            M09.Get_Language_Str("PICO im Bootmodus gefunden\n"
                             "Soll der PICO mit einer Start-Firmware initialisiert werden?")
        )
        title = M09.Get_Language_Str("Aktualisieren der MobaLedLib")

        # Replace MsgBox with your GUI or console prompt
        user_answer = P01.MsgBox(message, "question_yesno", title)

        if user_answer != "yes":
            M08.AskBootPico = False
            return

        # Copy UF2 file
        M12.FileCopy_with_Check(
            drive_letters[i] + "/",
            "Heartbeat.uf2",
            M08.GetWorkbookPath() + "/Boards/Heartbeat.uf2"
        )

        # Wait for CPU reset
        time.sleep(3)
      
      # Dim DriveLetters() As String, DriveNames() As String
      # Dim cnt As Long, i As Long
      # cnt = EnumDiskDrives(DriveLetters, DriveNames, True)
      # Debug.Print "Anzahl gefundener USB-Laufwerke: " & cnt
      # For i = 0 To cnt - 1
        # Debug.Print "Laufwerk " & DriveLetters(i) & " - " & DriveNames(i)
        # If MsgBox(Get_Language_Str("PICO im Bootmodus gefunden" & vbCr & _
                                 # "Soll der PICO mit einer Start-Firmware initialisiert werden?"), _
                                 # vbQuestion + vbYesNo, Get_Language_Str("Aktualisieren der MobaLedLib")) <> vbYes Then
          # AskBootPico = False
          # Exit Sub
       # End If
       # FileCopy_with_Check DriveLetters(i) & "\", "Heartbeat.uf2", GetWorkbookPath() & "\Boards\Heartbeat.uf2"
       # ' wait until CPU resets
       # Sleep (3000)
      # Next
    # End Sub

# VB2PY (UntranslatedCode) Option Explicit

