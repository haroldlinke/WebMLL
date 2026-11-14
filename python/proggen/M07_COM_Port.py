# Datei-Version: 1.11 (2026-11-14) - M07_COM_Port.py
# ----------------------------------------------------------------------------------------------
# Name:           M07_COM_Port.py
# Path:           proggen/M07_COM_Port.py
# Version:        1.11
# Last Update:    2026-11-12
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-12  Stand der Umstellung (nicht erfasst)
#   1.01  2026-10-20  EnumComPorts: FTDI-Adapter (VID 0403, Beschreibung FT232 ...) werden erkannt, sonst meldete die Pruefung beim Hochladen 'kein Arduino angeschlossen'; DetectArduino: kein Absturz, wenn die Verbindung inzwischen getrennt wurde
#   1.11  2026-11-14  Other_Type_Port_List (Liste statt Text, fuer die anklickbaren 'Andere Typen')
#   1.10  2026-11-14  EnumComPorts: CP210x/CP2102 nur noch fuer den ESP32 (der ESP32 erschien in Nano- und Pico-Liste); Classify_Port, Other_Type_Ports fuer die Zeile 'Andere Typen'
#   1.02  2026-10-21  Pico: jede Kennung VID 2E8A und Adafruit 239A:813D (vorher nur 2E8A:000A), pyserial- und Windows-Zweig; DetectArduino schaltet RTS ein (Version K des Excel-Programms)
#   1.03  2026-10-26  Linux: die Platzhalter-Anschluesse /dev/ttyS0 ... ttyS31 ohne Geraet erscheinen nicht mehr in der Liste der Anschluesse (auch nicht mit unbekannte Ports anzeigen)
#   1.04  2026-10-27  Find_Nano_Like_Device: erkennt einen Arduino Nano (CH340, FTDI, Arduino) an einem Anschluss, wenn ein Pico oder ESP32 eingestellt ist
#   1.05  2026-11-11  getdeviceinformation gab immer False zurueck (Erfolg der Pruefung nur noch an der Antwort des Bootloaders erkannt). DetectArduino: Verbindung wird in jedem Fall geschlossen, nur noch mit der lokalen Verbindung gearbeitet (kein 'NoneType' ... 'dtr'), gegen gleichzeitige Zugriffe gesichert (Sperre), bei -1/-2/-3 mehrere Versuche mit Pause; Bootloader-Pruefung (STK500) ueber die Einstellung DetectBootloader (Kurzweg: aendert die Wahl des Benutzers nie); Liste der Anschluesse erkennt CH340, FTDI und Arduino an der Hersteller-Kennung (Beschreibung 'USB Serial'); die Pruefung akzeptiert einen gewaehlten Anschluss auch mit unbekannter Beschreibung (nicht bei ESP32 und Pico)
#   1.06  2026-11-11  Bootloader-Pruefung (Einstellung DetectBootloader an): nur eine Pruefung je Baudrate statt vier (DETECT_LOOPS_BOOTLOADER; 'nicht erkannt' nach etwa 6 statt 24 Sekunden); das Protokoll nennt gesendete und empfangene Bytes jeder Synchronisation (__transact) und die Zahl der Bytes im Empfangspuffer vor dem Synchronisieren
#   1.07  2026-11-12  Bootloader-Pruefung: nach dem DTR-Puls 150 ms warten und den Empfangspuffer leeren; GET_SYNC bis zu 10-mal im Abstand von etwa 0,3 s neu senden statt dreimal 2 s zu warten (der alte Bootloader des Nano ist nur kurz erreichbar; Ergebnis von bootloader_test.py auf dem Raspberry Pi: der erste Sync direkt nach dem Loslassen von DTR geht verloren)
#   1.08  2026-11-12  Die Bootloader-Pruefung ist jetzt STANDARD (Einstellung NanoBootloaderDetection, ohne Eintrag oder leer: an); wer sie nicht moechte, schaltet sie in den Programm Einstellungen aus. Neuer Name der Einstellung, damit die in 3.10 bis 3.12 beim Speichern der Seite mitgeschriebene Vorgabe 'aus' (DetectBootloader) nicht gilt
#   1.09  2026-11-12  Excel-Programm 3.5.0L3: Support fuer den Arduino Nano Every (ATmega4809) entfernt (Jürgen, 09.11.26); EnumComPorts, Check_If_Port_is_Available und Check_If_Port_is_Available_And_Get_Name haben den Board-Typ als Parameter (BoardType, Vorgabe: der Board-Typ des aktuellen Blatts), wie im Excel-Programm
# ----------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2021
# * Copyright: Harold Linke 2021
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
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

#------------------------------------------------------------------------------
# CHANGELOG:
# 2020-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2021-01-07 v4.02 HL: - Else: check done, first PoC release
import serial.tools.list_ports as portlist
import logging
import os  # v1.03
import re  # v1.03
import serial
import threading  # v1.05
try:    
    from zeroconf import Zeroconf, ServiceBrowser, ServiceListener,  DNSAddress
    import_zeroconfok = True
except:
    import_zeroconfok = False
    
import socket, time

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *


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
import proggen.M07_COM_Port_New as M07New
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

#import proggen.D08_Select_COM_Port_Userform as D08

import ExcelAPI.XLA_Application as P01
import  proggen.F00_mainbuttons as F00

import mlpyproggen.Prog_Generator as PG


class DCB:
    def __init__(self):
        self.DCBlength = int()
        self.BaudRate = int()
        self.fBitFields = int()
        self.wReserved = Integer()
        self.XonLim = Integer()
        self.XoffLim = Integer()
        self.ByteSize = Byte()
        self.Parity = Byte()
        self.StopBits = Byte()
        self.XonChar = Byte()
        self.XoffChar = Byte()
        self.ErrorChar = Byte()
        self.EofChar = Byte()
        self.EvtChar = Byte()
        self.wReserved1 = Integer()

class COMMCONFIG:
    def __init__(self):
        self.dwSize = int()
        self.wVersion = Integer()
        self.wReserved = Integer()
        self.dcbx = DCB()
        self.dwProviderSubType = int()
        self.dwProviderOffset = int()
        self.dwProviderSize = int()
        self.wcProviderData = Byte()

class COMMTIMEOUTS:
    def __init__(self):
        self.ReadIntervalTimeout = int()
        self.ReadTotalTimeoutMultiplier = int()
        self.ReadTotalTimeoutConstant = int()
        self.WriteTotalTimeoutMultiplier = int()
        self.WriteTotalTimeoutConstant = int()

__ERROR_IO_INCOMPLETE = 996
__ERROR_IO_PENDING = 997
__GENERIC_READ = 0x80000000
__GENERIC_WRITE = 0x40000000
__FILE_ATTRIBUTE_NORMAL = 0x80
__FILE_FLAG_OVERLAPPED = 0x40000000
__FORMAT_MESSAGE_FROM_SYSTEM = 0x1000
__OPEN_EXISTING = 3
__COM_SETXOFF = 1
__COM_SETXON = 2
__COM_SETRTS = 3
__COM_CLRRTS = 4
__COM_SETDTR = 5
__COM_CLRDTR = 6
__COM_SETBREAK = 8
__COM_CLRBREAK = 9
__MS_CTS_ON = 0x10
__MS_DSR_ON = 0x20
__MS_RING_ON = 0x40
__MS_RLSD_ON = 0x80
__PURGE_RXABORT = 0x2
__PURGE_RXCLEAR = 0x8
__PURGE_TXABORT = 0x1
__PURGE_TXCLEAR = 0x4
__Resp_STK_OK = 0x10
__Resp_STK_FAILED = 0x11
__Resp_STK_INSYNC = 0x14
__Sync_CRC_EOP = 0x20
__Cmnd_STK_GET_PARAMETER = 0x41
__Cmnd_STK_GET_SYNC = 0x30
__STK_READ_SIGN = 0x75
__Parm_STK_HW_VER = 0x80
__Parm_STK_SW_MAJOR = 0x81
__Parm_STK_SW_MINOR = 0x82

Resp_STK_OK = b'\x10'
Resp_STK_FAILED = b'\x11'
Resp_STK_INSYNC = b'\x14'
Sync_CRC_EOP = b'\x20'
Cmnd_STK_GET_PARAMETER = b'\x41'
Cmnd_STK_GET_SYNC = b'\x30'
STK_READ_SIGN = b'\x75'
Parm_STK_HW_VER = b'\x80'
Parm_STK_SW_MAJOR = b'\x81'
Parm_STK_SW_MINOR = b'\x82'

CheckCOMPort_Txt = ""
CheckCOMPort = " "#0

def __Test_Get_COM():
    Res = String()

    Line = Variant()
    #-------------------------
    Res = F_shellExec('cmd /c mode')
    for Line in Split(Res, vbCr):
        Debug.Print(Line)

def __Get_USB_Ports():
    fn_return_value = None
    Res = String()

    Lines = Variant()

    Line = Variant()

    p = int()

    ResStr = String()

    Cnt = int()

    ResSplit = Variant()

    ResArray = vbObjectInitialize(objtype=Long)

    i = int()
    #------------------------------------------
    # The function returns an long array with COM numbers
    # COM-10 is allways added because otherwise the array may be empty if no other com port is detected
    # The "find" function dosen't work on Norberts computer => Therefore it's replaced by an own find algo
    Res = M30.F_shellExec('cmd /c mode')
    # Achtung: Der Mode Befehl schickt einen Reset zu allen Ports
    if Res == '':
        # No COM port available ?
        P01.MsgBox(M09.Get_Language_Str('Fehler: Das Abfragen der COM Ports ist fehlgeschlagen ;-('), vbCritical, M09.Get_Language_Str('Fehler beim abfragen der COM Ports'))
        M30.EndProg()
    Res = Replace(Res, ':', '')
    ResStr = '-10 '
    for Line in Split(Res, vbCr):
        p = InStr(Line, 'COM')
        if p > 0:
            ResStr = ResStr + Trim(Mid(Line, p + Len('COM'), 255)) + ' '
            Cnt = Cnt + 1
    ResStr = M30.DelLast(ResStr)
    ResSplit = Split(ResStr, ' ')
    ResArray = vbObjectInitialize((Cnt,), Variant)
    for i in vbForRange(0, Cnt):
        ResArray[i] = P01.val(ResSplit(i))
    fn_return_value = ResArray
    return fn_return_value

def Detect_Com_Port_and_Save_Result(Right):
    ComPortColumn = int()

    BuildOptColumn = int()

    Pic_ID = String()

    Port = int()
    #-----------------------------------------------------------
    if Right:
        ComPortColumn = M25.COMPrtR_COL
        Pic_ID = 'DCC'
        BuildOptColumn = M25.BUILDOpRCOL
    else:
        ComPortColumn = M25.COMPort_COL
        Pic_ID = 'LED'
        BuildOptColumn = M25.BUILDOP_COL
    Port = M07New.Detect_Com_Port(Right, Pic_ID)
    #if Port > 0:
    if F00.port_is_available(Port):    
        P01.CellDict[M02.SH_VARS_ROW, ComPortColumn] = Port
        PG.global_controller.setConfigData("serportname",Port)
        F00.StatusMsg_UserForm.Set_Label(M09.Get_Language_Str('Überprüfe den Arduino Typ'))
        # 30.10.20:
        F00.StatusMsg_UserForm.Show()
        
        BuildOptions = ""
        DeviceSignature = 0        
        Fn_res, BuildOptions, DeviceSignature = M08.Check_If_Arduino_could_be_programmed_and_set_Board_type(ComPortColumn, BuildOptColumn, BuildOptions, DeviceSignature) #*HL Buildoption and devicesignature are return values
        P01.Unload(F00.StatusMsg_UserForm)

def __TestDetect_Com_Port():
    #UT------------------------------
    M07New.Detect_Com_Port(False, 'LED')

def ComPortPage():
    fn_return_value = None
    # 30.12.19:
    #-----------------------------------------
    if M02.ComPortfromOnePage != '':
        fn_return_value = PG.ThisWorkbook.Sheets(M02.ComPortfromOnePage)
    else:
        fn_return_value = P01.ActiveSheet
    return fn_return_value

def Check_USB_Port_with_Dialog(ComPortColumn):
    fn_return_value = False
    #---------------------------------------------------------------------------
    #if P01.val(ComPortPage().Cells(M02.SH_VARS_ROW, ComPortColumn)) <= 0:
    if True: #HL not PG.global_controller.arduino or not PG.global_controller.arduino.is_open:
        if not F00.port_is_available(ComPortPage().Cells(M02.SH_VARS_ROW, ComPortColumn)):
            fn_return_value = M07New.USB_Port_Dialog(ComPortColumn)
            # 04.05.20: Prior Check_USB_Port_with_Dialog ends the program in case of an error
        else:
            fn_return_value = True
    else:
        fn_return_value = True
    return fn_return_value

def __Test_Check_USB_Port_with_Dialog():
    # 30.12.19:
    #UT------------------------------------------
    M25.Make_sure_that_Col_Variables_match()
    Debug.Print(Check_USB_Port_with_Dialog(M25.COMPort_COL))
    # Left Arduino
    #Debug.Print Check_USB_Port_with_Dialog(COMPrtR_COL)   ' Right Arduino
    # Right Arduino
    #Debug.Print Check_USB_Port_with_Dialog(COMPrtT_COL)   ' Tiny_Uniprog
    # Tiny_Uniprog

def Get_USB_Port_with_Dialog(right=VBMissingArgument):
    _fn_return_value = False
    ComPortColumn = Long()
    # 30.12.19:
    #-----------------------------------------------------------------------------
    if Right:
        ComPortColumn = M25.COMPrtR_COL
    else:
        ComPortColumn = M25.COMPort_COL
    with_0 = ComPortPage().Cells(M02.SH_VARS_ROW, ComPortColumn)
    if not F00.port_is_available(with_0.Value):
    #*HL if P01.val(with_0.Value) <= 0:
        if M07New.USB_Port_Dialog(ComPortColumn) == False:
            fn_return_value = - 1
            return fn_return_value
    #fn_return_value = P01.val(with_0.Value)
    fn_return_value = with_0.Value
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Port - ByVal 
def InitComPort(Port, Settings):
    #-------------------------------------------------------------
    if NativeInitComPort(Port, Settings, 100):
        return
    # if previous method failed use command shell and mode command to set serial options
    F_shellRun('cmd /c mode com' + Port + ' ' + Settings, 0, True)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Port - ByVal 
def NativeInitComPort(Port, Settings, readTimeout):
    fn_return_value = None
    DCB = DCB()

    Result = Variant()

    handle = int()
    #------------------------------------------------------------------------------------------------
    handle = 0
    Result = 0
    # VB2PY (UntranslatedCode) On Error GoTo NativeError
    handle = CreateFile('\\\\.\\COM' + Port, 0, 0, 0, __OPEN_EXISTING, __FILE_ATTRIBUTE_NORMAL, 0)
    if handle > 0:
        Result = BuildCommDCB(Settings, DCB)
        if Result == 1:
            Result = SetCommState(handle, DCB)
        if Result == 1:
            if GetCommTimeouts(handle, cts) == 1:
                cts.ReadIntervalTimeout = readTimeout
                cts.ReadTotalTimeoutConstant = readTimeout
                cts.ReadTotalTimeoutMultiplier = 0
                SetCommTimeouts(handle, cts)
                fn_return_value = True
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if handle > 0:
        CloseHandle(( handle ))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ResNames - ByRef 
def EnumComPorts_old(Show_Unknown, ResNames, PrintDebug=True):
    fn_return_value = None
    Ports = vbObjectInitialize((50,), Byte)

    NumberOfPorts = Byte()

    Names = vbObjectInitialize((50,), String)

    CountOnly = Boolean()

    objItem = Variant()

    ESP_Inst = Boolean()

    PICO_Inst = Boolean()

    Result = vbObjectInitialize(objtype=Byte)
    #------------------------------------------------------------------------------------------------------------------------------
    # Generate a list of COM ports which have
    # "CH340" or "Arduino" in there name
    # Doesn't check if the COM Port is used by an other program
    CountOnly = True
    NumberOfPorts = 0
    ESP_Inst = ( M02a.Get_BoardTyp() == M02.HT_ESP32 )
    PICO_Inst = ( M02a.Get_BoardTyp() == M02.HT_PICO )
    for objItem in GetObject('winmgmts:\\\\.\\root\\CIMV2').ExecQuery('SELECT * FROM Win32_PnPEntity WHERE ClassGuid="{4d36e978-e325-11ce-bfc1-08002be10318}"', VBGetMissingArgument(GetObject.ExecQuery, 1), 48):
        # if Show_Unknown or ( ESP_Inst == False and PICO_Inst == False and  (InStr(objItem.Caption, 'CH340') > 0 or InStr(objItem.Caption, 'Arduino') > 0 or InStr(objItem.Caption, 'USB Serial Port') > 0 ) ) or ( ESP_Inst == True and InStr(objItem.Caption, 'Silicon Labs CP210x') > 0 )  or  ( PICO_Inst == True and InStr(objItem.Path_.Path, 'USB\\\\VID_2E8A&PID_000A\\') > 0 ):  # v1.02 (entfallen)
        if Show_Unknown or ( ESP_Inst == False and PICO_Inst == False and  (InStr(objItem.Caption, 'CH340') > 0 or InStr(objItem.Caption, 'Arduino') > 0 or InStr(objItem.Caption, 'USB Serial Port') > 0 ) ) or ( ESP_Inst == True and InStr(objItem.Caption, 'Silicon Labs CP210x') > 0 )  or  ( PICO_Inst == True and ( InStr(objItem.Path_.Path, 'USB\\\\VID_2E8A&PID_') > 0 or InStr(objItem.Path_.Path, 'USB\\\\VID_239A&PID_813D') > 0 ) ):  # v1.02
            # 10.11.20: Added: "Silicon Labs CP210x" for the ESP32  02.05.20: Added: "USB Serial Port" for original Nano (Frank)
            # 21.04.21: Added: "Silicon Labs CP210x" for the PICO
            if PrintDebug:
                Debug.Print(objItem.Caption)
            idx1 = InStr(objItem.Caption, '(COM')
            if idx1 > 0:
                idx2 = InStr(idx1 + 3, objItem.Caption, ')')
                if idx2 > 0:
                    portNumber = P01.val(Mid(objItem.Caption, idx1 + 4, idx2 - idx1 - 4))
                    Ports[NumberOfPorts] = portNumber
                    Names[NumberOfPorts] = objItem.Caption
                    NumberOfPorts = NumberOfPorts + 1
                    if NumberOfPorts >= UBound(Ports):
                        break
        else:
            Debug.Print('Other device (Not added to result): ' + objItem.Caption)
            # Example: "Silicon Labs CP210x USB to UART Bridge (COM10)"
    if NumberOfPorts > 0:
        Result = vbObjectInitialize((NumberOfPorts - 1,), Variant)
        ResNames = vbObjectInitialize((NumberOfPorts - 1,), Variant)
        for idx1 in vbForRange(0, NumberOfPorts - 1):
            Result[idx1] = Ports(idx1)
        M30.Array_BubbleSort(Result)
        # Sort the Ports
        # find the matching names
        for idx1 in vbForRange(0, NumberOfPorts - 1):
            for idx2 in vbForRange(0, NumberOfPorts - 1):
                if Result(idx1) == Ports(idx2):
                    ResNames[idx1] = Names(idx2)
                    break
        fn_return_value = Result
    return fn_return_value

import socket
import struct
import time

sock = None
MCAST_GRP = "224.0.0.251"
MCAST_PORT = 5353
query = b"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"  # DNS query header
query += b"\x09_railmail\x04_tcp\x05local\x00"  # Query for _railmail._tcp.local
query += b"\x00\x0C\x00\x01"  # Type PTR, Class IN

def init_socket():
    global sock
    
    # Get local IP address of the active network interface
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except BaseException as e:
        local_ip = ""
        logging.debug(e)
    
    if not PG.global_controller.getConfigData("UseHostAdapter"):
        local_ip = ""
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    sock.bind((local_ip, MCAST_PORT))
    if local_ip != "":
        mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(local_ip))
    else:
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Funktion zum Leeren des Sockets
def clear_socket(sock):
    
    sock.setblocking(False)  # Setze Socket auf non-blocking Modus
    try:
        while True:
            data, addr = sock.recvfrom(1024)  # Versuche, alte Pakete zu lesen
            #print(f"Verworfen: {addr[0]} → {data}")  # Debug-Ausgabe
    except socket.error:
        pass  # Keine weiteren Daten mehr im Puffer
    finally:
        sock.setblocking(True)  # Setze Socket zurück auf normalen Modus



#starttime = time.time()
#while True:
    #data, addr = sock.recvfrom(1024)

    ## Decode the binary response properly
    #decoded_response = data.decode(errors="ignore")
    #print(f"Response from {addr[0]}: {decoded_response}")
    ## Apply stricter filtering based on structure and presence of RailMail service name
    #if "_railmail._tcp.local" in decoded_response or "railmail" in decoded_response:
        #print(f"Valid RailMail Response from {addr[0]}: {decoded_response}")
    #if int(time.time() - starttime) > 1:
        #starttime = time.time()
        #sock.sendto(query, (MCAST_GRP, MCAST_PORT))


def find_devices2():
    global sock
    
    init_socket()
    clear_socket(sock)
    
    sock.sendto(query, (MCAST_GRP, MCAST_PORT))
    
    sock.settimeout(1.0) # Timeout auf 1 Sekunde setzen
    
    starttime = time.time()
    
    devices = []
    
    while int(time.time() - starttime) < 1:
        try:
            data, addr = sock.recvfrom(1024)
            currtime = time.time() - starttime
    
            # Decode the binary response properly
            decoded_response = data.decode(errors="ignore")
            #print(f"{currtime} - Response from {addr[0]}: {decoded_response}")
        
            # Apply stricter filtering based on structure and presence of RailMail service name
            if "RailMail-" in decoded_response:
                print(f"{currtime} - Valid RailMail Response from {addr[0]}: {decoded_response}")
                description = decoded_response[decoded_response.index("RailMail-"):-10]
                devices.append(["IP:" + addr[0], description])
        except:
            pass
    return devices

# Key: instance name (string)
# Value: dict with resolved info (e.g. host, port, [ips])

services = {}
if import_zeroconfok:
    class TrackingListener(ServiceListener):
        def add_service(self, zc, service_type, name):
            
            for record in zc.cache.entries_with_name(name.lower()):
                if isinstance(record, DNSAddress):
                    ip = socket.inet_ntoa(record.address)
                    Debug.Print(f"Found IP from cache: {ip}")        
            services[ip] = {
                "name": name
            }
            Debug.Print(f"[ADD]   {name}{ip}")
    
        def remove_service(self, zc, service_type, name):
            # Remove from our dict (if present)
            info = services.pop(name, None)
            if info:
                print(f"[DROP]  {name} removed")
    
from concurrent.futures import ThreadPoolExecutor

def is_ip_responsive(ip, port=80, timeout=1):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return ip, True
    except (socket.timeout, socket.error):
        return ip, False

def monitor_ips_concurrently(services, interval=1):
    ip_list = list(services.keys())
    if len(ip_list) > 0:
        with ThreadPoolExecutor(max_workers=len(ip_list)) as executor:
            Debug.Print("Checking IPs...")
            futures = [executor.submit(is_ip_responsive, ip) for ip in ip_list]
            for future in futures:
                ip, status = future.result()
                Debug.Print(f"{ip}: {'Responsive' if status else 'Not responsive'}")
                if status == False:
                    services.pop(ip)
            #print("-" * 40)
            #time.sleep(interval)

def find_devices():
    zc = Zeroconf()
    listener = TrackingListener()
    browser = ServiceBrowser(zc, "_railmail._tcp.local.", listener)
    devices = []

    time.sleep(2)
    monitor_ips_concurrently(services)
    Debug.Print("\n=== CURRENT SERVICES ===")
    for inst, info in services.items():
        Debug.Print(f"{inst}: {info['name']}")
        devices.append(["IP:" + inst, info['name']])

    browser.cancel()
    zc.close()
    return devices


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ResNames - ByRef 
def EnumComPorts(Show_Unknown, ResNames, PrintDebug=True, BoardType=None):  # v1.09: BoardType (Excel 3.5.0L3): der Board-Typ, fuer den die Anschluesse gesucht werden; ohne Angabe der Board-Typ des Blatts
    Ports = vbObjectInitialize((50,), Byte)
    BoardType = BoardType or M02a.Get_BoardTyp()  # v1.09
    ESP_Inst = ( BoardType == M02.HT_ESP32 )  # v1.09 (vorher M02a.Get_BoardTyp())
    PICO_Inst = ( BoardType == M02.HT_PICO )  # v1.09 (vorher M02a.Get_BoardTyp())
    WLAN_inst =  InStr(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL), 'WLAN') > 0
    if WLAN_inst:
        # check for Railmail mDNS
        if import_zeroconfok:
            Ports = []
            ResNames = []
            devices = find_devices()
            temp_device_list = devices
            
            for device in temp_device_list:
                Ports.append(device[0])
                ResNames.append(device[1])
        else:
            Debug.Print("EnumComPorts: Module Zeroconf not imported")
            Ports = ["Fehler"]
            ResNames = ["Achtung:Module Zeroconf nicht gefunden"]
    else:
        temp_comports_list = portlist.comports(include_links=False)
        
        Debug.Print("EnumComPorts:"+repr(temp_comports_list))
    
        NumberOfPorts = len(temp_comports_list)
        Ports = [] #vbObjectInitialize((NumberOfPorts - 1,), Variant)
        ResNames = [] #vbObjectInitialize((NumberOfPorts - 1,), Variant)    
        idx=0
        for comport in temp_comports_list:
            Debug.Print("EnumComPorts:"+repr(comport.description)+" "+repr(comport.device))
            if os.name != 'nt' and re.match(r'^/dev/ttyS\d+$', str(comport.device)) and str(comport.hwid).strip().lower() in ('n/a', ''):  # v1.03
                continue                              # Linux: ttyS0 ... ttyS31 sind Platzhalter ohne Geraet (auch mit "unbekannte Ports anzeigen" nie in der Liste)  # v1.03
            # if Show_Unknown or ( ESP_Inst == False and PICO_Inst == False and  (InStr(comport.description, 'CH340') > 0 or InStr(comport.description, 'Arduino') > 0 or InStr(comport.description, 'USB Serial Port') > 0 or InStr(comport.description, 'USB2.0-Ser') > 0  or InStr(comport.description, 'tty') > 0 ) ) or ( ESP_Inst == True and InStr(comport.description, 'Silicon Labs CP210x') > 0 )  or  ( PICO_Inst == True and InStr(comport.description, 'USB\\\\VID_2E8A&PID_000A\\') > 0 ):
            # if Show_Unknown or ( ESP_Inst == False and PICO_Inst == False and  (InStr(comport.description, 'CH340') > 0 or InStr(comport.description, 'Arduino') > 0 or InStr(comport.description, 'USB Serial Port') > 0 or InStr(comport.description, 'USB2.0-Ser') > 0  or InStr(comport.description, 'tty') > 0 or InStr(comport.description, 'FT232') > 0 or InStr(comport.hwid, 'VID:PID=0403:') > 0 ) ) or ( ESP_Inst == True and ( InStr(comport.description, 'Silicon Labs CP210x') > 0 or InStr(comport.description, 'CP2102 USB to UART') > 0 or getattr(comport, 'vid', None) == 0x10C4 ) )  or  ( PICO_Inst == True and InStr(comport.hwid, 'USB VID:PID=2E8A:000A') > 0 ):  # v1.02 (entfallen)
            # if Show_Unknown or ( ESP_Inst == False and PICO_Inst == False and  (InStr(comport.description, 'CH340') > 0 or InStr(comport.description, 'Arduino') > 0 or InStr(comport.description, 'USB Serial Port') > 0 or InStr(comport.description, 'USB2.0-Ser') > 0  or InStr(comport.description, 'tty') > 0 or InStr(comport.description, 'FT232') > 0 or InStr(comport.hwid, 'VID:PID=0403:') > 0 ) ) or ( ESP_Inst == True and ( InStr(comport.description, 'Silicon Labs CP210x') > 0 or InStr(comport.description, 'CP2102 USB to UART') > 0 or getattr(comport, 'vid', None) == 0x10C4 ) )  or  ( PICO_Inst == True and ( InStr(comport.hwid, 'USB VID:PID=2E8A:') > 0 or InStr(comport.hwid, 'USB VID:PID=239A:813D') > 0 ) ):  # v1.02  # v1.05 (entfallen)
            if Show_Unknown or ( ESP_Inst == False and PICO_Inst == False and  (InStr(comport.description, 'CH340') > 0 or InStr(comport.description, 'Arduino') > 0 or InStr(comport.description, 'USB Serial Port') > 0 or InStr(comport.description, 'USB2.0-Ser') > 0  or InStr(comport.description, 'tty') > 0 or InStr(comport.description, 'FT232') > 0 or InStr(comport.hwid, 'VID:PID=0403:') > 0 or ( getattr(comport, 'vid', None) in NANO_LIKE_VIDS ) ) ) or ( ESP_Inst == True and ( InStr(comport.description, 'Silicon Labs CP210x') > 0 or InStr(comport.description, 'CP2102 USB to UART') > 0 or getattr(comport, 'vid', None) == 0x10C4 ) )  or  ( PICO_Inst == True and ( InStr(comport.hwid, 'USB VID:PID=2E8A:') > 0 or InStr(comport.hwid, 'USB VID:PID=239A:813D') > 0 ) ):  # v1.05
                Ports.append(comport.device)
                ResNames.append(comport.description)
                idx=idx+1

    fn_return_value = Ports
    return fn_return_value, ResNames

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PortNr - ByVal 
def Check_If_Port_is_Available(PortNr, BoardType=None):  # v1.09: BoardType wie im Excel-Programm
    if PortNr.startswith("IP:"):
        return True
    Debug.Print("Check_If_Port_is_Available:"+PortNr)
    fn_return_value = None
    Ports = vbObjectInitialize(objtype=Byte)

    ResNames = vbObjectInitialize(objtype=String)
    #--------------------------------------------------------------------------
    # Ports, ResNames = EnumComPorts(False, ResNames)  # v1.05 (entfallen)
    # Ports, ResNames = EnumComPorts(_Accept_Unknown_Ports(), ResNames)  # v1.05 (entfallen: mit BoardType)
    Ports, ResNames = EnumComPorts(_Accept_Unknown_Ports(BoardType), ResNames, BoardType=BoardType)  # v1.09: ein gewaehlter Anschluss gilt auch mit unbekannter Beschreibung (Nano)
    fn_return_value = M30.Is_Contained_in_Array(PortNr, Ports)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PortNr - ByVal 
NANO_LIKE_VIDS = (0x1A86, 0x0403, 0x2341, 0x2A03)                        # CH340/CH341, FTDI, Arduino: Hersteller der Anschluesse, an denen ein Nano oder Uno haengt (nicht: 0x10C4 Silicon Labs CP210x der ESP32, 0x2E8A Raspberry Pi)  # v1.04

def Classify_Port(comport):  # v1.10: Typ eines Anschlusses (Nano / Pico / ESP32 / "") anhand VID und Beschreibung, wie die Excel-Anzeige "Andere Typen"
    desc = str(getattr(comport, 'description', '') or '')
    hwid = str(getattr(comport, 'hwid', '') or '').upper()
    vid = getattr(comport, 'vid', None)
    if vid == 0x2E8A or 'VID:PID=2E8A:' in hwid or 'VID:PID=239A:813D' in hwid:
        return 'Pico'
    if vid == 0x10C4 or 'CP210x' in desc or 'CP2102 USB to UART' in desc:
        return 'ESP32'
    if vid in NANO_LIKE_VIDS or 'CH340' in desc or 'Arduino' in desc or 'FT232' in desc or 'USB2.0-Ser' in desc or 'VID:PID=0403:' in hwid:
        return 'Nano'
    return ''


def Other_Type_Port_List(BoardType=None):  # v1.11: Liste [(Anschluss, Typ)];  v1.10: "COM3(ESP32), COM5(Pico)" - Anschluesse anderer Zentralentypen als BoardType
    BoardType = BoardType or M02a.Get_BoardTyp()
    mine = 'Pico' if BoardType == M02.HT_PICO else ('ESP32' if BoardType == M02.HT_ESP32 else 'Nano')
    res = []
    try:
        for comport in portlist.comports(include_links=False):
            if os.name != 'nt' and re.match(r'^/dev/ttyS\d+$', str(comport.device)) and str(comport.hwid).strip().lower() in ('n/a', ''):
                continue
            t = Classify_Port(comport)
            if t and t != mine:
                res.append((str(comport.device), t))
    except Exception as e:
        Debug.Print("Other_Type_Ports: " + repr(e))
    def key(x):
        m = re.search(r'(\d+)$', x[0])
        return (int(m.group(1)) if m else 0, x[0])
    res.sort(key=key)
    return res


def Other_Type_Ports(BoardType=None):  # v1.10: "COM3(ESP32), COM5(Pico)"
    return ", ".join("%s(%s)" % (d, t) for d, t in Other_Type_Port_List(BoardType))



def Find_Nano_Like_Device(PortNr):  # v1.04
    """Beschreibung des Geraetes an einem Anschluss, wenn es nach einem Arduino Nano oder Uno aussieht (CH340, FTDI, Arduino), sonst ''.
    Gebraucht, wenn ein Pico oder ESP32 eingestellt ist: Die Liste der Anschluesse enthaelt dann nur dessen Geraete, und die Pruefung meldete
    'kein PICO angeschlossen', obwohl der Anschluss stimmt und ein Nano daran haengt."""
    try:  # v1.04
        for comport in portlist.comports():  # v1.04
            if str(comport.device) != str(PortNr):  # v1.04
                continue  # v1.04
            vid = getattr(comport, "vid", None)  # v1.04
            text = (str(comport.description) + " " + str(getattr(comport, "manufacturer", "") or "") + " " + str(getattr(comport, "product", "") or ""))  # v1.04
            if vid == 0x2E8A:  # v1.04
                return ""  # v1.04
            if vid in NANO_LIKE_VIDS or "CH340" in text or "CH341" in text or "Arduino" in text or "USB2.0-Serial" in text:  # v1.04
                return str(comport.description).strip() or "Arduino"  # v1.04
    except Exception:                                                        # noqa: BLE001  # v1.04
        Debug.Print("Find_Nano_Like_Device fehlgeschlagen")  # v1.04
    return ""  # v1.04


def Check_If_Port_is_Available_And_Get_Name(PortNr, BoardType=None):  # v1.09: BoardType wie im Excel-Programm
    Debug.Print("Check_If_Port_is_Available_And_Get_Name:"+PortNr)
    fn_return_value = ""
    Ports = vbObjectInitialize(objtype=Byte)

    ResNames = vbObjectInitialize(objtype=String)

    Res = int()
    #--------------------------------------------------------------------------------------
    # Ports,ResNames = EnumComPorts(False, ResNames)  # v1.05 (entfallen)
    # Ports,ResNames = EnumComPorts(_Accept_Unknown_Ports(), ResNames)  # v1.05 (entfallen)
    Ports,ResNames = EnumComPorts(_Accept_Unknown_Ports(BoardType), ResNames, BoardType=BoardType)  # v1.09
    Res = M30.Get_Position_In_Array(PortNr, Ports)
    if Res >= 0:
        fn_return_value = ResNames[Res]
    return fn_return_value

def __Test_Check_If_Port_is_Available():
    #UT------------------------------------------
    Debug.Print(Check_If_Port_is_Available(3))

def __TestDetect():
    Ports = vbObjectInitialize(objtype=Byte)

    Start = Variant()

    SWMajorVersion = Byte()

    SWMinorVersion = Byte()

    HWVersion = Byte()

    DeviceSignatur = int()

    BaudRate = int()

    i = Integer()

    ComPort = Variant()

    ComPorts = vbObjectInitialize(objtype=Byte)

    Names = vbObjectInitialize(objtype=String)

    Ub = int()
    #UT---------------------
    Start = Time
    ComPorts, Names = EnumComPorts(False, Names)
    # VB2PY (UntranslatedCode) On Error GoTo IsEmpty
    Ub = UBound(ComPorts)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    for ComPort in ComPorts:
        for i in vbForRange(1, 2):
            if i == 1:
                BaudRate = 57600
            else:
                BaudRate = 115200
            Debug.Print('Trying COM' + ComPort + ' with Baudrate ' + BaudRate)
            select_0, DeviceSignatur = DetectArduino(ComPort, BaudRate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur)
            if (select_0 == 1):
                Debug.Print('  Serial Port     : COM' + ComPort)
                Debug.Print('  Serial Baudrate : ' + BaudRate)
                Debug.Print('  Hardware Version: ' + HWVersion)
                Debug.Print('  Firmware Version: ' + SWMajorVersion + '.' + SWMinorVersion)
                Debug.Print('  Device signature: ')
                if DeviceSignatur == 2004239:
                    Debug.Print('ATMega328 ')
                if DeviceSignatur == 0x1E9651:
                    Debug.Print('ATMega4809 ')
                    # 28.10.20: Jürgen
                Debug.Print('0x' + Right('00000' + Hex(DeviceSignatur), 6) + vbCr)
                break
            elif (select_0 == 0):
                pass
            else:
                break
    Debug.Print('End')
    Debug.Print('Check duration: ' + Format(Time - Start, 'hh:mm:ss'))
    return
    P01.MsgBox('No Arduino detected')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DeviceSignatur - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: FirmwareVer - ByRef 
def Get_Arduino_Baudrate(ComPort, Start_Baudrate, DeviceSignatur, FirmwareVer, DebugPrint=False):
    fn_return_value = 0
    SWMajorVersion = Byte()

    SWMinorVersion = Byte()

    HWVersion = Byte()

    BaudRate = int()

    i = Integer()

    Res = int()

    SleepTime = int()
    # 28.10.20: Jürgen: Added: DeviceSignatur  30.10.20: Added: FirmwareVer
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Return  >0: Baudrate 57600/115200
    #          0: if no arduino is detected
    #         -1: can't open com port => used by an other program ?
    #         -2: can't create com port file
    #         -3: can't reset arduino
    if (Start_Baudrate == 1):
        BaudRate = 115200
    elif (Start_Baudrate == 2):
        BaudRate = 57600
    else:
        BaudRate = Start_Baudrate
    if BaudRate != 115200 and BaudRate != 57600:
        BaudRate = 115200
    SleepTime = 20
    Loops = DETECT_LOOPS_BOOTLOADER if Detect_Bootloader_Enabled() else 8  # v1.06: mit der Bootloader-Pruefung nur ein Durchlauf je Baudrate (sonst Kurzweg: der erste Durchlauf antwortet)
    # for i in vbForRange(1, 8):  # v1.06 (entfallen)
    for i in vbForRange(1, Loops):  # v1.06
        # In case of an error we check each baudrate 4 times because sometimes the Baudrate is not detected if started with the wrong Baudrate   13.10.20: old:  For i = 1 To 6
        if DebugPrint:
            Debug.Print('Trying COM' + str(ComPort) + ' with Baudrate ' + str(BaudRate))
        if 0:
            # Faster
            # 30.10.20: Old: 1 (Seemes to be not much slower)
            Res, DeviceSignatur = DetectArduino(ComPort, BaudRate, DeviceSignatur= DeviceSignatur, SleepTime= SleepTime)
        else:
            Res, DeviceSignatur = DetectArduino(ComPort, BaudRate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur= DeviceSignatur, SleepTime= SleepTime)
        if (Res == 1):
            # Detected an arduino
            if DebugPrint:
                Debug.Print('  Serial Port     : COM' + str(ComPort))
                Debug.Print('  Serial Baudrate : ' + str(BaudRate))
                Debug.Print('  Hardware Version: ' + str(HWVersion))
                Debug.Print('  Firmware Version: ' + str(SWMajorVersion) + '.' + str(SWMinorVersion))
                Debug.Print('  Device signature: ')
                if DeviceSignatur == 2004239:
                    Debug.Print('ATMega328 ')
                if DeviceSignatur == 0x1E9651:
                    Debug.Print('ATMega4809 ')
                    # 28.10.20: Jürgen
                Debug.Print('0x' + Right('00000' + Hex(DeviceSignatur), 6) + vbCr)
            FirmwareVer = str(SWMajorVersion) + '.' + str(SWMinorVersion)
            fn_return_value = BaudRate
            break
        elif (Res == 0):
            pass
        else:
            fn_return_value = Res
            break
        if BaudRate == 115200:
            BaudRate = 57600
        else:
            BaudRate = 115200
            # Check again with the other baud rate
        if i == 4:
            SleepTime = 150
    return fn_return_value

def __Test_Get_Arduino_Baudrate():
    Start = Variant()

    DeviceSignatur = int()

    FirmwareVer = String()
    #UT------------------------------------
    Start = Time
    #Debug.Print "Get_Arduino_Baudrate=" & Get_Arduino_Baudrate(6, 115200, DeviceSignatur, FirmwareVer, True)
    Debug.Print('Get_Arduino_Baudrate=' + Get_Arduino_Baudrate(6, 57600, DeviceSignatur, FirmwareVer, True))
    #Debug.Print "Get_Arduino_Baudrate=" & Get_Arduino_Baudrate(8, 115200, DeviceSignatur, FirmwareVer, True)  ' Matching Baudrate 3 Sec, Not matching 6 Sek
    Debug.Print('Check duration: ' + Format(Time - Start, 'hh:mm:ss'))
    
def getdeviceinformation():
    logging.debug("getdeviceinformation")
    DeviceSignatur = b''
    HWVersion = b''
    SWMajorVersion  = b''
    SWMinorVersion  = b''
    Data = __transact(STK_READ_SIGN, 5)
    Res = False  # v1.05
    if len(Data)==5:
        if Data[4].to_bytes(1,byteorder="little") == Resp_STK_OK:
            DeviceSignatur = Data[1:4]
            Res = True  # v1.05
            #logging.debug("getdeviceinformation: %s",str(DeviceSignatur))
            if DeviceSignatur == b'\x1E\x95\x0F':
                logging.info("ATMEGA328P")
            else:
                logging.info("Device Signatur: %s",str(DeviceSignatur))
    # return False, DeviceSignatur  # v1.05 (entfallen: gab immer False zurueck, auch wenn der Bootloader die Signatur lieferte)
    return Res, DeviceSignatur  # v1.05
    
# def DetectArduino(port,baudrate, HWVersion=255, SWMajorVersion=255, SWMinorVersion=255, DeviceSignatur=- 1, Trials=3, PrintDebug=True, SleepTime=20):  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     global Cmnd_STK_GET_SYNC, CheckCOMPort_Txt  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     # protocol see application note 1AVR061 here http://ww1.microchip.com/downloads/en/Appnotes/doc2525.pdf  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     # Result:  1: O.K  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     #          0: Give up after n trials => if no arduino is detected  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     #         -1: can't open com port  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     #         -2: can't close and assign port  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     #         -3: can't reset arduino  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     fn_return_value=0  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     No_of_trials = Trials  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     logging.debug ("M07.detect_arduino: %s",port)  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     no_port=None  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     try: # close the port if it is open and reopen it with DTR = False  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         if PG.global_controller.arduino and PG.global_controller.arduino.is_open:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#             PG.global_controller.arduino.close()  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         # hack for Mac  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         if P01.checkplatform("Darwin"):  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#             logging.debug("Hack for Mac: Set baudrate to 19200")  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#             baudrate=19200  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         PG.global_controller.arduino = serial.Serial(no_port,baudrate=baudrate,timeout=0.2,write_timeout=1,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         logging.info("Serial-params: " + repr(PG.global_controller.arduino))  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     except BaseException as e:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         logging.debug(e, exc_info=True)   # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         logging.debug("M07.detect_arduino: Error assigning port")  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         return -2, None  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     if type(port)==int:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         port_str="COM"+str(port)  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     else:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         port_str = port  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     ser = PG.global_controller.arduino  # v1.01  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     if ser is None:                                     # die Verbindung wurde inzwischen getrennt (zum Beispiel nach einem Schreibfehler im Sendethread): kein Absturz  # v1.01  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         logging.debug("M07.detect_arduino: Verbindung zum Arduino ist weg")  # v1.01  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         return -2, None  # v1.01  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     ser.port = port_str  # v1.01  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     ser.dtr = False  # v1.01  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     try:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         ser.open()  # v1.01  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     except BaseException as e:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         logging.debug("M07.detect_arduino: Error opening  port "+port_str)  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         logging.debug(e, exc_info=True)   # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         return -1, None             # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     try:  # v1.02  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         ser.rts = True                                  # 11.02.26: Version K - manche Module brauchen RTS high, um senden zu duerfen  # v1.02  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     except BaseException as e:  # v1.02  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         logging.debug(e, exc_info=True)  # v1.02  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     try:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         PG.global_controller.arduino.dtr = True  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         time.sleep(0.250)  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         PG.global_controller.arduino.dtr = False  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     except BaseException as e:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         logging.debug(e, exc_info=True)                   # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         logging.debug("M07.detect_arduino: Error, reset ARDUINO")  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         return -3, None  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     # now get in sync  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     message = Cmnd_STK_GET_SYNC  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     fn_return_value = 0  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     if not(Left(CheckCOMPort_Txt, 18) == 'Arduino NANO Every'):  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         fn_return_value = 1  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         DeviceSignatur = 2004561  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         HWVersion = 1  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         SWMajorVersion = 1  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         SWMinorVersion = 7  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         if baudrate == 115200:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#             fn_return_value = 1  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         else:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#             fn_return_value = 0  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     else:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         for i in range (No_of_trials):  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#             message = __transact(Cmnd_STK_GET_SYNC,2)  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#             if message == Resp_STK_INSYNC + Resp_STK_OK:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#                 DeviceSignatur = b''  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#                 HWVersion = b''  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#                 SWMajorVersion  = b''  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#                 SWMinorVersion  = b''              # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#                 res,devicesignatur = getdeviceinformation()  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#                 if res==True:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#                     fn_return_value=1  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#                     PG.global_controller.arduino.close()  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#                     return fn_return_value, devicesignatur  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#         if fn_return_value != 1:  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#             logging.debug("Give up after %s trials",No_of_trials)  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)
#     return fn_return_value, None  # v1.05 (entfallen: ersetzt durch _DetectArduino_once und den Rahmen DetectArduino)

# ---- Verbindung zum Arduino pruefen (v1.05) --------------------------------------------------------------------------------------
_DETECT_LOCK = threading.RLock()  # v1.05: Zeitgeber der blinkenden LEDs, Pruefung und Hochladen duerfen den Anschluss nicht gleichzeitig benutzen
DETECT_RETRIES = 3  # v1.05: Versuche, wenn sich der Anschluss nicht oeffnen oder der Arduino nicht zuruecksetzen laesst (-1, -2, -3)
DETECT_RETRY_PAUSE = 0.4  # v1.05: Sekunden zwischen den Versuchen
REOPEN_PAUSE_WIN = 0.3  # v1.05: Windows (CH340): nach dem Schliessen braucht der Treiber einen Moment, bevor sich der Anschluss wieder oeffnen laesst
DETECT_LOOPS_BOOTLOADER = 2  # v1.06: Durchlaeufe von Get_Arduino_Baudrate bei eingeschalteter Bootloader-Pruefung (je Baudrate einer; vorher 8: 24 Sekunden bis 'nicht erkannt')
SYNC_START_DELAY = 0.15  # v1.07: Sekunden Wartezeit nach dem Loslassen von DTR, bevor der erste Sync gesendet wird (wie avrdude)
SYNC_ATTEMPTS = 10  # v1.07: Anzahl der GET_SYNC je Baudrate (jeweils neu gesendet)
SYNC_RETRY_PAUSE = 0.1  # v1.07: Pause zwischen zwei GET_SYNC (dazu kommt das Lesen mit 0,2 s Zeitgrenze: etwa 0,3 s je Versuch)
SYNC_BAUDRATES = (57600, 115200)  # v1.05: nur bei diesen Baudraten wird der Bootloader angesprochen (nicht beim Blinken mit 50 Baud)


# def Detect_Bootloader_Enabled():  # v1.05  # v1.08 (entfallen: Vorgabe war aus, Name DetectBootloader)
#     """Einstellung DetectBootloader (Programm Einstellungen, Spezialeinstellungen): Mit Haken wird der Bootloader des Nano angesprochen (STK500) und dadurch alt (57600) und  # v1.08 (entfallen: Vorgabe war aus, Name DetectBootloader)
#     neu (115200) erkannt. Ohne Haken (Vorgabe) wird nur geprueft, ob sich der Anschluss oeffnen laesst; die Wahl des Benutzers bleibt, wie sie ist."""  # v1.05  # v1.08 (entfallen: Vorgabe war aus, Name DetectBootloader)
#     try:  # v1.05  # v1.08 (entfallen: Vorgabe war aus, Name DetectBootloader)
#         value = PG.global_controller.getConfigData("DetectBootloader")  # v1.05  # v1.08 (entfallen: Vorgabe war aus, Name DetectBootloader)
#     except Exception:                                                  # noqa: BLE001  # v1.05  # v1.08 (entfallen: Vorgabe war aus, Name DetectBootloader)
#         return False  # v1.05  # v1.08 (entfallen: Vorgabe war aus, Name DetectBootloader)
#     return str(value if value is not None else "").strip().lower() in ("1", "true", "ja", "yes", "an", "ein", "on")  # v1.05  # v1.08 (entfallen: Vorgabe war aus, Name DetectBootloader)


BOOTLOADER_DETECTION_PARAM = "NanoBootloaderDetection"  # v1.08: Name der Einstellung (Programm Einstellungen, Spezialeinstellungen)


def Detect_Bootloader_Enabled():  # v1.08
    """Einstellung NanoBootloaderDetection (Programm Einstellungen, Spezialeinstellungen, 'Bootloader des Nano beim Prüfen erkennen'): VORGABE AN.
    An: Das Programm spricht den Bootloader des Nano an (STK500) und erkennt alt (57600 Baud) und neu (115200 Baud); mit 'Automatisch erkennen' stellt es das Board passend ein.
    Aus (nur auf ausdruecklichen Wunsch): Es wird nur geprueft, ob sich der Anschluss oeffnen laesst; die Wahl des Benutzers bleibt, wie sie ist.
    Ohne Eintrag, leer oder bei einem Fehler beim Lesen: an. Die Seite der Einstellungen speichert Wahrheitswerte (True/False)."""  # v1.08
    try:  # v1.08
        value = PG.global_controller.getConfigData(BOOTLOADER_DETECTION_PARAM)  # v1.08
    except Exception:                                                  # noqa: BLE001  # v1.08
        return True  # v1.08
    text = str(value if value is not None else "").strip().lower()  # v1.08
    if text == "":  # v1.08: nie gespeichert: Vorgabe
        return True  # v1.08
    return text in ("1", "true", "ja", "yes", "an", "ein", "on")  # v1.08


def _Accept_Unknown_Ports(BoardType=None):  # v1.05 (v1.09: BoardType)
    """Fuer die Pruefung eines gewaehlten Anschlusses: Bei einem Nano (nicht ESP32, nicht Pico) gilt jeder vorhandene Anschluss, auch mit unbekannter Beschreibung"""  # v1.05
    try:  # v1.05
        return (BoardType or M02a.Get_BoardTyp()) not in (M02.HT_ESP32, M02.HT_PICO)  # v1.09 (vorher M02a.Get_BoardTyp())
    except Exception:                                                  # noqa: BLE001  # v1.05
        return False  # v1.05


def _Close_Quiet(ser):  # v1.05
    try:  # v1.05
        if ser is not None and ser.is_open:  # v1.05
            ser.close()  # v1.05
    except BaseException as e:                                         # noqa: BLE001  # v1.05
        logging.debug(e, exc_info=True)  # v1.05


def DetectArduino(port, baudrate, HWVersion=255, SWMajorVersion=255, SWMinorVersion=255, DeviceSignatur=- 1, Trials=3, PrintDebug=True, SleepTime=20):  # v1.05
    """Rahmen um _DetectArduino_once: serialisiert die Zugriffe (Sperre) und wiederholt bei -1 (Anschluss nicht zu oeffnen), -2 (nicht zuweisbar) und -3 (Arduino nicht
    zuruecksetzbar) bis zu DETECT_RETRIES-mal mit Pause (beim Blinken mit 50 Baud nur einmal: der Zeitgeber ruft jede Sekunde auf).
    Ergebnis wie bisher: 1 erkannt, 0 nicht erkannt, -1 Anschluss nicht zu oeffnen, -2 nicht zuweisbar, -3 nicht zuruecksetzbar."""  # v1.05
    retries = 1 if baudrate == 50 else DETECT_RETRIES  # v1.05
    with _DETECT_LOCK:  # v1.05
        result = (0, None)  # v1.05
        for attempt in range(1, retries + 1):  # v1.05
            result = _DetectArduino_once(port, baudrate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur, Trials, PrintDebug, SleepTime)  # v1.05
            if result[0] >= 0:  # v1.05
                break  # v1.05
            logging.debug("M07.detect_arduino: Versuch %s von %s gescheitert (Ergebnis %s)", attempt, retries, result[0])  # v1.05
            if attempt < retries:  # v1.05
                time.sleep(DETECT_RETRY_PAUSE)  # v1.05
        return result  # v1.05


def _DetectArduino_once(port, baudrate, HWVersion=255, SWMajorVersion=255, SWMinorVersion=255, DeviceSignatur=- 1, Trials=3, PrintDebug=True, SleepTime=20):  # v1.05
    global Cmnd_STK_GET_SYNC, CheckCOMPort_Txt  # v1.05
    # protocol see application note 1AVR061 here http://ww1.microchip.com/downloads/en/Appnotes/doc2525.pdf
    # Result:  1: O.K
    #          0: Give up after n trials => if no arduino is detected
    #         -1: can't open com port
    #         -2: can't close and assign port
    #         -3: can't reset arduino
    No_of_trials = Trials  # v1.05
    logging.debug("M07.detect_arduino: %s", port)  # v1.05
    ser = None  # v1.05
    try:  # close the port if it is open and reopen it with DTR = False  # v1.05
        old_connection = PG.global_controller.arduino  # v1.05
        if old_connection and old_connection.is_open:  # v1.05
            old_connection.close()  # v1.05
            if os.name == 'nt':  # v1.05
                time.sleep(REOPEN_PAUSE_WIN)  # v1.05
        # hack for Mac
        if P01.checkplatform("Darwin"):  # v1.05
            logging.debug("Hack for Mac: Set baudrate to 19200")  # v1.05
            baudrate = 19200  # v1.05
        ser = serial.Serial(None, baudrate=baudrate, timeout=0.2, write_timeout=1, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)  # v1.05
        PG.global_controller.arduino = ser  # v1.05: __transact und getdeviceinformation arbeiten mit dieser Verbindung
        logging.info("Serial-params: " + repr(ser))  # v1.05
    except BaseException as e:                                         # noqa: BLE001  # v1.05
        logging.debug(e, exc_info=True)  # v1.05
        logging.debug("M07.detect_arduino: Error assigning port")  # v1.05
        return -2, None  # v1.05
    port_str = "COM" + str(port) if type(port) == int else port  # v1.05
    try:  # v1.05: ab hier wird die Verbindung in jedem Fall wieder geschlossen
        try:  # v1.05
            ser.port = port_str  # v1.05
            ser.dtr = False  # v1.05
            ser.open()  # v1.05
        except BaseException as e:                                     # noqa: BLE001  # v1.05
            logging.debug("M07.detect_arduino: Error opening  port " + str(port_str))  # v1.05
            logging.debug(e, exc_info=True)  # v1.05
            return -1, None  # v1.05
        try:  # v1.05
            ser.rts = True                                  # 11.02.26: Version K - manche Module brauchen RTS high, um senden zu duerfen  # v1.05
        except BaseException as e:                                     # noqa: BLE001  # v1.05
            logging.debug(e, exc_info=True)  # v1.05
        try:  # v1.05
            ser.dtr = True  # v1.05
            time.sleep(0.250)  # v1.05
            ser.dtr = False  # v1.05
        except BaseException as e:                                     # noqa: BLE001  # v1.05
            logging.debug(e, exc_info=True)  # v1.05
            logging.debug("M07.detect_arduino: Error, reset ARDUINO")  # v1.05
            return -3, None  # v1.05
        # if Left(CheckCOMPort_Txt, 18) == 'Arduino NANO Every':  # v1.05 (entfallen v1.09: Nano Every wird nicht mehr unterstuetzt)
        #     return (1 if baudrate == 115200 else 0), None  # v1.05 (entfallen)
        if (not Detect_Bootloader_Enabled()) or baudrate not in SYNC_BAUDRATES:  # v1.05: Kurzweg: der Anschluss laesst sich oeffnen (die Wahl des Benutzers bleibt)
            return 1, None  # v1.05
        try:  # now get in sync (Bootloader ansprechen)  # v1.05
            try:  # v1.06: fuer die Fehlersuche: Bytes, die nach dem Zuruecksetzen schon im Empfangspuffer liegen
                pending = ser.in_waiting  # v1.06
            except BaseException:                                      # noqa: BLE001  # v1.06
                pending = -1  # v1.06
            logging.debug("M07.detect_arduino: %s Baud, vor dem Synchronisieren %s Byte(s) im Empfangspuffer", baudrate, pending)  # v1.06
            time.sleep(SYNC_START_DELAY)  # v1.07: der Bootloader braucht nach dem Loslassen von DTR einen Moment; ein sofort gesendeter Sync geht verloren
            try:  # v1.07
                ser.reset_input_buffer()  # v1.07: Ausgabe des Sketches und Reste verwerfen
            except BaseException as e:                                 # noqa: BLE001  # v1.07
                logging.debug(e, exc_info=True)  # v1.07
            # for i in range(No_of_trials):  # v1.07 (entfallen: einmal senden und 2 s warten; der alte Bootloader war dann schon im Sketch)
            for i in range(SYNC_ATTEMPTS):  # v1.07: GET_SYNC wiederholt senden (je Versuch nur einmal lesen)
                message = __transact(Cmnd_STK_GET_SYNC, 2, 1)  # v1.07
                if message == Resp_STK_INSYNC + Resp_STK_OK:  # v1.05
                    res, devicesignatur = getdeviceinformation()  # v1.05: die Signatur ist nur eine Zugabe; Erfolg heisst: der Bootloader antwortet (wie in der Tk-Fassung)
                    logging.info("M07.detect_arduino: Bootloader antwortet mit %s Baud (Versuch %s)", baudrate, i + 1)  # v1.07
                    return 1, devicesignatur  # v1.05
                time.sleep(SYNC_RETRY_PAUSE)  # v1.07
        except BaseException as e:                                     # noqa: BLE001  # v1.05
            logging.debug(e, exc_info=True)  # v1.05
            logging.debug("M07.detect_arduino: Fehler beim Ansprechen des Bootloaders")  # v1.05
            return -3, None  # v1.05
        logging.debug("Give up after %s trials", SYNC_ATTEMPTS)  # v1.07 (vorher No_of_trials)
        return 0, None  # v1.05
    finally:  # v1.05
        _Close_Quiet(ser)  # v1.05

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Port - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: BaudRate - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: HWVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMajorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMinorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DeviceSignatur=- 1 - ByRef 
def DetectArduino_old(Port, BaudRate, HWVersion=255, SWMajorVersion=255, SWMinorVersion=255, DeviceSignatur=- 1, Trials=3, PrintDebug=True, SleepTime=20):
    fn_return_value = None
    handle = int()

    i = Integer()

    Result = Boolean()
    #---------------------------------------------------------------------------
    # protocol see application note 1AVR061 here http://ww1.microchip.com/downloads/en/Appnotes/doc2525.pdf
    # Result:  1: O.K
    #          0: Give up after n trials => if no arduino is detected
    #         -1: can't open com port
    #         -2: can't create com port file
    #         -3: can't reset arduino
    
    return 1 #*HL

    handle = 0
    fn_return_value = 0
    if PrintDebug:
        Debug.Print('SleepTime=' + str(SleepTime))
    if not NativeInitComPort(Port, 'BAUD=' + BaudRate + ' PARITY=N DATA=8 STOP=1 dtr=off', 500):
        if PrintDebug:
            Debug.Print('can\'t open com port')
        fn_return_value = - 1
        return fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo NativeError
    handle = CreateFile('\\\\.\\COM' + str(Port), __GENERIC_READ or __GENERIC_WRITE, 0, 0, __OPEN_EXISTING, __FILE_ATTRIBUTE_NORMAL, 0)
    if handle <= 0:
        if PrintDebug:
            Debug.Print('can\'t create com port file')
        fn_return_value = - 2
        return fn_return_value
    #if PrintDebug then Debug.Print "reset arduino"
    Result = EscapeCommFunction(handle, __COM_SETDTR)
    if Result:
        DoEvents()
        Sleep(( SleepTime )      )
        # Bei einem meiner Arduinos funktioniert die Erkennung nicht zuverlässig mit 10 ms.    13.10.20:
        # Mit 150ms geht es gut. Aber nur dann wenn die Konfiguration groß ist
        # (Mainboard Test: "MB Test 1 DCC" 66 LEDs)
        # Bei einer kleinen Konfiguration mit nur 2 LEDs geht es aber nicht mit 150 ms.
        # Dann müssen 20 ms verwendet werden
        # => Ich habe eine umschaltung der Wartetzeit in Get_Arduino_Baudrate() eingebaut.
        #    Jetzt werden jeweils zwei versoche mit jeder Baudrate mit 20 ms gemacht und
        #    danach 2 mit 150 ms.
        #    Damit scheint es zu Funktionieren. Getestet mit 2 verschiedenen Arduinos.
        #    Zwei mit neuem BL und einer mit altem BL.
        #  - Zusätzlich habe ic "Trials" von 5 auf 3 reduziert weil ich beobachtet habe,
        #    dass der Arduino entweder beim ersten oder zweiten Versuch erkannt wird
        #    oder gar nicht erkannt wird.
        Result = EscapeCommFunction(handle, __COM_CLRDTR)
    if Result == False:
        if PrintDebug:
            Debug.Print('can\'t reset arduino')
            # I never get this message ?
        CloseHandle(( handle ))
        fn_return_value = - 3
        return fn_return_value
    DoEvents()
    if Left(CheckCOMPort_Txt, 18) == 'Arduino NANO Every':
        fn_return_value = 1
        DeviceSignatur = 2004561
        HWVersion = 1
        SWMajorVersion = 1
        SWMinorVersion = 7
        if BaudRate == 115200:
            fn_return_value = 1
        else:
            fn_return_value = 0
    else:
        for i in vbForRange(1, Trials):
            message = __Transact(handle, Chr(__Cmnd_STK_GET_SYNC), 2)
            if UBound(message) == 1:
                if message(0) == __Resp_STK_INSYNC and message(1) == __Resp_STK_OK:
                    #if PrintDebug then Debug.Print "in sync with arduino"
                    if __GetDeviceInformation(handle, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur):
                        fn_return_value = 1
                        if PrintDebug:
                            Debug.Print('Detected after ' + i + ' trials')
                        break
                    #Exit For                                                           ' 13.10.20: Old position
    if DetectArduino() != 1:
        if PrintDebug:
            Debug.Print('Give up after ' + Trials + ' trials')
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if handle > 0:
        CloseHandle(( handle ))
    return fn_return_value

def __transact(bytemessage,nNumberOfBytesToRead=10, Reads=10):  # v1.07: Reads = Anzahl der Lesevorgaenge je Senden (Vorgabe wie bisher 10)
    
    bytemessage += Sync_CRC_EOP
    # write message to serport
    nbytes_written = PG.global_controller.arduino.write(bytemessage)
    if nbytes_written != len(bytemessage):
        logging.debug("ERROR write to ARDUINO")
        return b''
    no_of_trials=Reads  # v1.07 (vorher 10)
    first_seen = b''  # v1.06: erste nicht leere Antwort (fuer das Protokoll)
    started = time.time()  # v1.06
    for i in range (no_of_trials):
        # read from serport nNumberOfBytesToRead
        read_data = PG.global_controller.arduino.read(size=nNumberOfBytesToRead)
        #logging.debug("transact: %s",read_data)
        if read_data and not first_seen:  # v1.06
            first_seen = read_data  # v1.06
        if (read_data[:1] == Resp_STK_INSYNC and read_data[-1:] == Resp_STK_OK) or read_data[-1:] == Resp_STK_FAILED:
        # return response
            #logging.debug("transact data_ok: %s",read_data)
            logging.debug("M07.transact: gesendet %s, Antwort %s (Lesevorgang %s von %s, %.2f s)", bytemessage.hex(" "), read_data.hex(" "), i + 1, no_of_trials, time.time() - started)  # v1.06
            return read_data
    logging.debug("M07.transact: gesendet %s, keine passende Antwort; erste empfangene Bytes: %s (%s Lesevorgaenge, %.2f s)", bytemessage.hex(" "), first_seen.hex(" ") if first_seen else "keine", no_of_trials, time.time() - started)  # v1.06
    return b''

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: handle - ByVal 
def __Transact_old(handle, message, nNumberOfBytesToRead=10):
    fn_return_value = None
    CbWritten = Variant()

    CbRead = Variant()

    ToSend = Variant()

    j = int()

    Buffer = vbObjectInitialize(objtype=Byte)

    Response = vbObjectInitialize(((0, 9),), Byte)

    EmptyResp = vbObjectInitialize((0,), Byte)

    Rc = int()
    #-----------------------------------------------------------------------------------------------------------------------
    message = message + Chr(__Sync_CRC_EOP)
    ToSend = Len(message)
    Buffer = vbObjectInitialize((ToSend,), Variant)
    for j in vbForRange(0, ToSend - 1):
        Buffer[j] = Asc(Mid(message, j + 1, 1))
    #Debug.Print "nNumberOfBytesToRead = 10"
    #nNumberOfBytesToRead = 10
    PurgeComm(handle, __PURGE_TXABORT or __PURGE_RXABORT or __PURGE_TXCLEAR or __PURGE_RXCLEAR)
    if WriteFile(handle, Buffer(0), ToSend, CbWritten, 0) == 0:
        return fn_return_value
    if CbWritten != ToSend:
        return fn_return_value
    fn_return_value = EmptyResp
    while 1:
        Rc = ReadFile(handle, Response(0), nNumberOfBytesToRead, CbRead, 0)
        if Rc == 0 or CbRead < 1:
            return fn_return_value
        DoEvents()
        if Response(0) == __Resp_STK_INSYNC and Response(CbRead - 1) == __Resp_STK_OK or Response(CbRead - 1) == __Resp_STK_FAILED:
            resp = vbObjectInitialize(((0, CbRead - 1),), Variant)
            for j in vbForRange(0, CbRead - 1):
                resp[j] = Response(j)
            fn_return_value = resp
            return fn_return_value
        #Debug.Print "invalid packet"
        return fn_return_value
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: handle - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: HWVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMajorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMinorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DeviceSignatur=- 1 - ByRef 
def __GetDeviceInformation(handle, HWVersion=255, SWMajorVersion=255, SWMinorVersion=255, DeviceSignatur=- 1):
    fn_return_value = None
    data = vbObjectInitialize(objtype=Byte)

    Tmp = int()
    #--------------------------------------------------------------------------------------------------------------------
    # Added option to speed up by not requesting all values                     ' 04.05.20:
    # 1 sec instead of 3 if only the DeviceSignatur is requested
    # Attention: At least one value has to be requested
    fn_return_value = False
    if DeviceSignatur != - 1:
        data = __Transact(handle, Chr(__STK_READ_SIGN), 5)
        if UBound(data) != 4:
            return fn_return_value
        if data(4) != __Resp_STK_OK:
            return fn_return_value
        Tmp = data(1)
        DeviceSignatur = Tmp * 65536
        Tmp = data(2)
        DeviceSignatur = DeviceSignatur + Tmp * 256
        Tmp = data(3)
        DeviceSignatur = DeviceSignatur + Tmp
    if HWVersion != 255:
        data = __Transact(handle, Chr(__Cmnd_STK_GET_PARAMETER) + Chr(__Parm_STK_HW_VER), 3)
        if UBound(data) != 2:
            return fn_return_value
        if data(2) != __Resp_STK_OK:
            return fn_return_value
        HWVersion = data(1)
    if SWMinorVersion != 255:
        data = __Transact(handle, Chr(__Cmnd_STK_GET_PARAMETER) + Chr(__Parm_STK_SW_MAJOR), 3)
        if UBound(data) != 2:
            return fn_return_value
        if data(2) != __Resp_STK_OK:
            return fn_return_value
        SWMajorVersion = data(1)
    if SWMinorVersion != 255:
        data = __Transact(handle, Chr(__Cmnd_STK_GET_PARAMETER) + Chr(__Parm_STK_SW_MINOR), 3)
        if UBound(data) != 2:
            return fn_return_value
        if data(2) != __Resp_STK_OK:
            return fn_return_value
        SWMinorVersion = data(1)
    fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort - ByVal 
def SendMLLCommand(ComPort, message, UseHardwareHandshake, ShowResult):
    fn_return_value = False
    handle = int()

    CbWritten = Variant()

    CbRead = int()

    t = Variant()

    Repeat = Integer()

    by = Byte()

    Msg = String()
    # VB2PY (UntranslatedCode) On Error GoTo serialError
    if UseHardwareHandshake:
        InitComPort(ComPort, 'BAUD=115200 PARITY=N DATA=8 STOP=1 dtr=off octs=on')
    else:
        if M02a.Get_BoardTyp() != M02.HT_PICO:
            InitComPort(ComPort, 'BAUD=115200 PARITY=N DATA=8 STOP=1 dtr=off octs=off')
        else:
            InitComPort(ComPort, 'BAUD=115200 PARITY=N DATA=8 STOP=1 dtr=on octs=off')
    UseHardwareHandshake = M30.Get_Current_Platform_Bool('UseHardwareHandshake')
    handle = CreateFile('\\\\.\\COM' + ComPort, __GENERIC_READ or __GENERIC_WRITE, 0, 0, __OPEN_EXISTING, __FILE_ATTRIBUTE_NORMAL, 0)
    if handle < 0:
        Err.Raise(1, VBGetMissingArgument(Err.Raise, 1), '')
    if M02a.Get_BoardTyp() == M02.HT_PICO:
        EscapeCommFunction(handle, __COM_SETDTR)
    if UseHardwareHandshake:
        Repeat = 1
    else:
        Repeat = 2
        # 03.04.20: Old: to 10
    if DEBUG_DCCSEND:
        Debug.Print(Format(Time, 'hh.mm.ss') + ' sending ' + Repeat + ' times to receiver: \'' + message + '\'')
        # Debug
    # The interrupts in the Arduino are locked while the LEDs are updatet
    # => To avoid loosing bits maximal one byte could be send over the RS232 while the interrupts are locked
    # The delay is calculated by:
    # 0.9 + 0.35us + 0.3 us = 1.55us / Bit
    # 24 Bit / LED
    # Resttime > 50 us
    # 256 LEDs => Delay 10 ms
    # Send duration 11 * 10 ms = 110 ms
    while Repeat > 0:
        Repeat = Repeat - 1
        for t in vbForRange(1, Len(message)):
            by = Asc(Mid(message, t, 1))
            WriteFile(handle, by, 1, CbWritten, 0)
            if UseHardwareHandshake == False:
                Sleep(10)()
                # 03.04.20: Added delay
    # write response(s) to the debug output
    if 1 & ShowResult:
        while 1:
            by = 0
            if ReadFile(handle, by, 1, CbRead, 0):
                Msg = Msg + Chr(by)
            if not (by > 0):
                break
        if Len(Msg) > 0:
            Debug.Print(Format(Time, 'hh.mm.ss') + ' Response from Arduino:       \'' + Replace(Msg, vbLf, '\\n') + '\'')
    #Close #1
    if handle > 0:
        CloseHandle(( handle ))
    fn_return_value = True
    return fn_return_value
    if handle > 0:
        CloseHandle(( handle ))
    Msg = Err.Description
    if DEBUG_DCCSEND:
        Debug.Print(Format(Time, 'hh.mm.ss') + ' send to receiver failed with ' + Msg)
    MsgBox(Get_Language_Str('Fehler beim senden an die serielle Schnittstelle COM') + ComPort + ':' + vbCr + '  \'' + Get_Language_Str(Msg) + '\'' + vbCr + Get_Language_Str('Eventuell ist der serielle Monitor noch offen'), vbCritical, Get_Language_Str('Fehler: Decoder senden fehlgeschlagen'))
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = False
    return fn_return_value

