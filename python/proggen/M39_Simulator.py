# Datei-Version: 1.12 (2026-11-22) - M39_Simulator.py
# ----------------------------------------------------------------------------------------------
# Name:           M39_Simulator.py
# Path:           proggen/M39_Simulator.py
# Version:        1.12
# Last Update:    2026-11-22
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-12  Stand der Umstellung (nicht erfasst)
#   1.01  2026-10-28  M02a importieren: Get_Ardu_LibDir steht in M02a_Public
#   1.02  2026-10-28  Get_Ardu_LibDir steht in M02a_Public
#   1.03  2026-11-15  An VBA (M39_Simulator, Wrapper 1.01) angepasst: CreateEx + L2VConfig.bin,
#                     Wrapper-Version 101, SimLedsY ab 1, Compile-Skript mit L2VConfig,
#                     IsLEDWindowVisible wird aufgerufen, RECT._fields_, "silent"-Pruefung
#   1.04  2026-11-15  Fehlende Konfigurationsdateien (LEDConfig.bin usw.) fuehren nicht mehr zum Absturz beim Start
#   1.05  2026-11-15  Simulatorfenster wird beim Beenden des Programms geschlossen (atexit); CloseSimulator ruft aus Workbook_BeforeClose
#   1.06  2026-11-15  Linux: Simulator ohne Windows-Fenster (libMobaLedLibWrapper.so aus simulator_linux/, Anzeige im Browser ueber _web/web_simulator.py), Uebersetzen mit build_linux.sh
#   1.07  2026-11-15  Auswahl Kein/Nur/Mit Simulator (Get_Sim_Mode, Sim_Select_Enabled, Set_Sim_Mode, Sim_Autostart); gilt statt SimAutostart, wenn die Option Simulator anzeigen an ist
#   1.08  2026-11-16  Knopf Setup simulieren: Set_Sim_Override; Get_Sim_Mode ohne gespeicherte Auswahl (mit der Option Simulator anzeigen gilt nur der Knopf)
#   1.09  2026-11-16  Fenster 'Kompilieren und Hochladen' bei Setup simulieren: Fortschritt und Ergebnis (OK schliesst es nach einigen Sekunden, Fehler bleibt stehen) - _Log
#   1.10  2026-11-16  Linux: Grund nennen, wenn der Simulator nicht verfuegbar ist (Bibliothek MobaLedLib fehlt, g++ fehlt, Bauen fehlgeschlagen)
#   1.11  2026-11-16  Linux: eigene Configuration_linux.cpp mit Schraegstrichen statt der Windows-Pfade der mitgelieferten Configuration.cpp (Meldung 'The FastLED library must be installed')
#   1.12  2026-11-22  Issue 45: Fensterlage des Simulators: ein minimiertes Fenster meldet Windows als -32000/-32000; diese Lage wird nicht mehr gespeichert, und ungueltige gespeicherte Werte werden beim Oeffnen durch 800/400 ersetzt (Fenster lag ausserhalb des Bildschirms)
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
# 2021-01-07 v4.02 HL: - Else:, ByRef check done, first PoC release


import os  # v1.04
import atexit  # v1.05
import platform  # v1.06
import subprocess  # v1.06
import shutil  # v1.06
from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

import proggen.M02_Public as M02
import proggen.M02a_Public as M02a  # v1.01
import proggen.M02_global_variables as M02GV
import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
import proggen.M09_SelectMacro_Treeview as M09SMT
import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M40_ShellandWait as M40
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Multiplexer as M80

import mlpyproggen.Prog_Generator as PG
import proggen.F00_mainbuttons as F00

import ExcelAPI.XLA_Application as P01

from ExcelAPI.XLC_Excel_Consts import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

import ctypes,ctypes.util
import sys,platform

"""# VB2PY (CheckDirective) VB directive took path 1 on VBA7"""
"""
extern "C" {
    __declspec(dllexport) int __stdcall GetWrapperVersion();
    __declspec(dllexport) const unsigned char* __stdcall Create(unsigned char* config, int configLenght);
    __declspec(dllexport) const unsigned char* __stdcall CreateSampleConfig();
    __declspec(dllexport) void __stdcall Update();
    __declspec(dllexport) int __stdcall GetLedColor(unsigned char ledNr);
    __declspec(dllexport) void __stdcall SetInput(unsigned char channel, unsigned char On);
    __declspec(dllexport) unsigned char __stdcall GetInput(unsigned char channel);
    __declspec(dllexport) void __stdcall ShowLEDWindow(unsigned char ledsX, unsigned char ledsY, unsigned char ledSize, unsigned char ledOffset, int windowPosX, int windowPosY, bool autoUpdate);
    __declspec(dllexport) void __stdcall CloseLEDWindow();
    __declspec(dllexport) bool __stdcall IsLEDWindowVisible;
    __declspec(dllexport) bool __stdcall GetLEDWindowRect(LPRECT rect);
}
"""

#Private Declare PtrSafe Function CreateSampleConfig Lib "MobaLedLibWrapper.dll" () As LongPtr
#Private Declare PtrSafe Function CreateSimulator Lib "MobaLedLibWrapper.dll" Alias "Create" ( configData As Any, ByVal configLength As Integer) As LongPtr

#Private Declare Sub SetInput Lib "MobaLedLibWrapper.dll" (ByVal Channel As Byte, ByVal IsOn As Byte)
#Private Declare Sub UpdateLeds Lib "MobaLedLibWrapper.dll" Alias "Update" ()
#Private Declare Function GetInput Lib "MobaLedLibWrapper.dll" (ByRef Channel As Byte) As Byte
#Private Declare Sub ShowLEDWindow Lib "MobaLedLibWrapper.dll" ( _
#        ByVal ledsX As Byte, ByVal ledsY As Byte, ByVal ledSize As Byte, ByVal ledOffset As Byte, _
#        ByVal windowPosX As Integer, ByVal windowPosY As Integer, automaticUpdate As Boolean)
#Private Declare Sub CloseLEDWindow Lib "MobaLedLibWrapper.dll" ()
#Private Declare Function IsLEDWindowVisible Lib "MobaLedLibWrapper.dll" () As Byte
#Private Declare Function GetLEDWindowRect Lib "MobaLedLibWrapper.dll" (lpRect As RECT) As Long
#Private Declare Function GetWrapperVersion Lib "MobaLedLibWrapper.dll" () As Long

MobaLedLibWrapper = None
CreateSampleConfig  = None
CreateSimulator = None
CreateSimulatorEx = None  # v1.03
SetInput = None
UpdateLeds = None
GetInput = None
ShowLEDWindow = None
CloseLEDWindow = None
IsLEDWindowVisible = None
GetLEDWindowRect = None
GetWrapperVersion = None


__AddressMapping = None

class RECT(ctypes.Structure):
    _fields_ = [("left",ctypes.c_int),
                  ("top",ctypes.c_int),
                  ("right",ctypes.c_int),
                  ("bottom",ctypes.c_int)]
    def __init__(self):
        self.left = 0 
        self.top = 0
        self.right = 0
        self.bottom = 0


# ---------------------------------------------------------------------------------------------- v1.07 Auswahl Simulator (Web)
SIM_OPTION = "ShowSimulator"  # v1.07 Programm Einstellungen, Spezialeinstellungen: Simulator anzeigen
SIM_MODE_KEY = "SimModeWeb"   # v1.07 gewaehlt: 0 Kein Simulator, 3 Nur Simulator, 2 Mit Simulator

def Sim_Select_Enabled():  # v1.07
    # Ist die Auswahl (Kein / Nur / Mit Simulator) eingeschaltet? Dann gilt sie statt der Option SimAutostart der Config-Seite.
    try:
        value = PG.get_global_controller().getConfigData(SIM_OPTION)
        return str(value if value is not None else "").strip().lower() in ("1", "true", "ja", "yes", "an", "ein", "on")
    except BaseException:
        return False

_sim_override = None  # v1.08 gilt waehrend eines Laufs von Setup simulieren (Knopf), sonst None

def Set_Sim_Override(value):  # v1.08 Knopf Setup simulieren: fuer einen Lauf Betriebsart 3 (nur Simulator); None hebt es wieder auf
    global _sim_override
    _sim_override = value

# def Get_Sim_Mode():  # v1.07 Wert wie SimAutostart: 0 kein Simulator, 1 mit Programmstart, 2 mit Simulator, 3 nur Simulator  # v1.08 (entfallen)
#     if Sim_Select_Enabled():  # v1.08 (entfallen)
#         try:  # v1.08 (entfallen)
#             value = int(str(PG.get_global_controller().getConfigData(SIM_MODE_KEY) or 0))  # v1.08 (entfallen)
#         except (ValueError, TypeError):  # v1.08 (entfallen)
#             value = 0  # v1.08 (entfallen)
#         return value if value in (0, 2, 3) else 0  # v1.08 (entfallen)
#     return M28.Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0)  # v1.08 (entfallen)
def Get_Sim_Mode():  # v1.08 Wert wie SimAutostart: 0 kein Simulator, 1 mit Programmstart, 2 mit Simulator, 3 nur Simulator
    if Sim_Select_Enabled():  # Option Simulator anzeigen: die Option SimAutostart der Config-Seite gilt nicht; Simulator nur ueber den Knopf Setup simulieren
        return _sim_override if _sim_override is not None else 0
    return M28.Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0)

def Set_Sim_Mode(value):  # v1.07
    ctrl = PG.get_global_controller()
    ctrl.setParamData(SIM_MODE_KEY, str(int(value)))
    ctrl.SaveParamData()

def Sim_Autostart():  # v1.07 Simulator beim Programmstart oeffnen? (Option 1 der Config-Seite, mit der Auswahl: Nur Simulator oder Mit Simulator)
    mode = Get_Sim_Mode()
    return mode == 1 or (Sim_Select_Enabled() and mode in (2, 3))

# ---------------------------------------------------------------------------------------------- v1.06 Linux
sim_params = {}  # v1.06 Linux: Anzeigeeinstellungen (x, y, size, offset) fuer die Anzeige im Browser

def _linux():  # v1.06
    return platform.system() == "Linux"

def _so_dir():  # v1.06
    m = platform.machine().lower()
    arch = {"x86_64": "x64", "amd64": "x64", "aarch64": "arm64", "arm64": "arm64"}.get(m, "arm" if m.startswith("arm") else m)
    return PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'linux_' + arch

_sim_problem = ""  # v1.10 Grund, warum der Simulator unter Linux nicht verfuegbar ist (fuer die Meldung)

# def _so_file():  # v1.06 vorhandene Bibliothek, sonst einmal aus dem Quelltext bauen (g++ noetig)  # v1.10 (entfallen)
def _so_file():  # v1.10 vorhandene Bibliothek, sonst einmal aus dem Quelltext bauen (g++ noetig); der Grund eines Fehlschlags steht in _sim_problem
    global _sim_problem
    _sim_problem = ""
    sofile = _so_dir() + '/libMobaLedLibWrapper.so'
    if os.path.isfile(sofile):
        return sofile
    script = PG.ThisWorkbook.Path + '/simulator_linux/build_simulator_linux.sh'
    libsrc = PG.ThisWorkbook.Path + '/libraries/MobaLedLib/src'
    if not os.path.isfile(script):
        _sim_problem = "Datei fehlt: " + script
    elif not os.path.isfile(libsrc + '/MobaLedLib.cpp'):
        _sim_problem = "Die Bibliothek MobaLedLib wurde nicht gefunden (" + libsrc + "). Bitte erst Bibliotheken installieren."
    elif shutil.which("g++") is None:
        _sim_problem = "Der C++-Übersetzer fehlt. Bitte im Terminal eingeben: sudo apt install build-essential"
    else:
        try:
            res = subprocess.run(["bash", script, libsrc, _so_dir()], capture_output=True, text=True, timeout=300)
            Debug.Print("Simulator bauen: " + (res.stdout + res.stderr)[-400:])
            if res.returncode != 0:
                _sim_problem = "Der Simulator konnte nicht gebaut werden:\n" + "\n".join((res.stdout + res.stderr).strip().splitlines()[-8:])
        except BaseException as e:
            Debug.Print("Simulator bauen fehlgeschlagen: " + str(e))
            _sim_problem = "Der Simulator konnte nicht gebaut werden: " + str(e)
    if os.path.isfile(sofile):
        return sofile
    if not _sim_problem:
        _sim_problem = "Die Datei libMobaLedLibWrapper.so fehlt: " + sofile
    return None

def sim_frame():  # v1.06 Linux: eine Simulationsrunde, liefert die LED-Farben (RGB-Tripel) fuer die Anzeige im Browser
    if not _linux() or MobaLedLibWrapper is None or not IsLEDWindowVisible():
        return None
    UpdateLeds()
    count = min(256, max(1, sim_params.get('x', 8) * sim_params.get('y', 8) + sim_params.get('offset', 0)))
    buf = (ctypes.c_ubyte * (3 * count))()
    n = MobaLedLibWrapper.GetLedColors(ctypes.c_ubyte(0), count, buf)
    return list(buf)[:3 * n]

def loaddll():
    global MobaLedLibWrapper, CreateSampleConfig, CreateSimulator, CreateSimulatorEx, SetInput, UpdateLeds, GetInput, ShowLEDWindow, CloseLEDWindow, IsLEDWindowVisible, GetLEDWindowRect, GetWrapperVersion 

    #if platform.system() == "Windows":
    #    MLL_DLL = ctypes.util.find_library("MobaLedLibWrapper")
    #else:
    #    MLL_DLL = None
    #    return
    
    # Get a handle to the sytem C library
    try:
    #   if MLL_DLL == None:
    #       print("MLL_DLL not found")
    #       return
    
        if _linux():  # v1.06
            dllfilename = _so_file() or ''  # v1.06
        elif F00.is_64bit():
            dllfilename = PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x64/MobaLedLibWrapper.dll'
        else:
            dllfilename = PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x86/MobaLedLibWrapper.dll'
        
        Debug.Print("LoadDll:"+dllfilename)    
        if MobaLedLibWrapper is not None and _linux():  # v1.06 schon geladen
            return
        MobaLedLibWrapper = ctypes.CDLL(dllfilename)

    except OSError:
        Debug.Print("Unable to load MLL_DLL "+dllfilename)
        sys.exit()
    
    Debug.Print('Succesfully loaded the MLL_DLL'+dllfilename) 
    
    #Private Declare PtrSafe Function CreateSampleConfig Lib "MobaLedLibWrapper.dll" () As LongPtr
    CreateSampleConfig = MobaLedLibWrapper.CreateSampleConfig
    CreateSampleConfig.argtypes=[]
    CreateSampleConfig.restype = ctypes.c_char_p
    
    #Private Declare PtrSafe Function CreateSimulator Lib "MobaLedLibWrapper.dll" Alias "Create" ( configData As Any, ByVal configLength As Integer) As LongPtr
    CreateSimulator = MobaLedLibWrapper.Create
    CreateSimulator.argtypes=[ctypes.c_char_p,ctypes.c_int]
    CreateSimulator.restype = ctypes.c_char_p
    CreateSimulatorEx = MobaLedLibWrapper.CreateEx  # v1.03
    CreateSimulatorEx.argtypes=[ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_int]  # v1.03
    CreateSimulatorEx.restype = ctypes.c_char_p  # v1.03
    
    #Private Declare Sub SetInput Lib "MobaLedLibWrapper.dll" (ByVal Channel As Byte, ByVal IsOn As Byte)
    SetInput = MobaLedLibWrapper.SetInput
    SetInput.argtypes=[ctypes.c_char,ctypes.c_char]
    SetInput.restype = None
    
    #Private Declare Sub UpdateLeds Lib "MobaLedLibWrapper.dll" Alias "Update" ()
    UpdateLeds = MobaLedLibWrapper.Update
    UpdateLeds.argtypes=[]
    UpdateLeds.restype = None
    
    #Private Declare Function GetInput Lib "MobaLedLibWrapper.dll" (ByRef Channel As Byte) As Byte
    GetInput = MobaLedLibWrapper.GetInput
    GetInput.argtypes=[ctypes.c_char]
    GetInput.restype = ctypes.c_char
        
    #Private Declare Sub ShowLEDWindow Lib "MobaLedLibWrapper.dll" ( _
    #        ByVal ledsX As Byte, ByVal ledsY As Byte, ByVal ledSize As Byte, ByVal ledOffset As Byte, _
    #        ByVal windowPosX As Integer, ByVal windowPosY As Integer, automaticUpdate As Boolean)
    ShowLEDWindow = MobaLedLibWrapper.ShowLEDWindow
    ShowLEDWindow.argtypes=[ctypes.c_char,ctypes.c_char,ctypes.c_char,ctypes.c_char,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    ShowLEDWindow.restype = None    
    
    #Private Declare Sub CloseLEDWindow Lib "MobaLedLibWrapper.dll" ()
    CloseLEDWindow = MobaLedLibWrapper.CloseLEDWindow
    CloseLEDWindow.argtypes=[]
    CloseLEDWindow.restype = None 
    
    #Private Declare Function IsLEDWindowVisible Lib "MobaLedLibWrapper.dll" () As Byte
    IsLEDWindowVisible = MobaLedLibWrapper.IsLEDWindowVisible
    IsLEDWindowVisible.argtypes=[]
    IsLEDWindowVisible.restype = ctypes.c_bool
    
    #Private Declare Function GetLEDWindowRect Lib "MobaLedLibWrapper.dll" (lpRect As RECT) As Long
    GetLEDWindowRect = MobaLedLibWrapper.GetLEDWindowRect
    GetLEDWindowRect.argtypes=[ctypes.POINTER(RECT)]
    GetLEDWindowRect.restype = ctypes.c_long
    
    #Private Declare Function GetWrapperVersion Lib "MobaLedLibWrapper.dll" () As Long    
    GetWrapperVersion = MobaLedLibWrapper.GetWrapperVersion
    GetWrapperVersion.argtypes=[]
    GetWrapperVersion.restype = ctypes.c_long
    if _linux():  # v1.06 Zusatzfunktion der Linux-Bibliothek
        MobaLedLibWrapper.GetLedColors.argtypes = [ctypes.c_ubyte, ctypes.c_int, ctypes.c_void_p]  # v1.06
        MobaLedLibWrapper.GetLedColors.restype = ctypes.c_int  # v1.06
        GetInput.restype = ctypes.c_ubyte  # v1.06


def IsSimualtorAvailable():
    fn_return_value = False
    WrapperVersion = Long()
    
    if _linux():  # v1.06 Linux: Bibliothek ohne Fenster
        try:
            if _so_file() is None:
                return fn_return_value
            loaddll()
            return Int(GetWrapperVersion() / 100) == 101
        except BaseException as e:
            Debug.Print("IsSimulatorAvailable (Linux): " + str(e))
            return fn_return_value
    if not P01.checkplatform("Windows"): # Simulator only in Windows available
        return fn_return_value
    
    if F00.is_64bit():
        dllfilename = PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x64/MobaLedLibWrapper.dll'
        Debug.Print("IsSimulatorAvailable:"+dllfilename)
        if Dir(dllfilename) == '':
            Debug.Print("IsSimulatorAvailable:"+dllfilename + " Not found")
            return fn_return_value
        ChDir(PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x64')
    else:
        dllfilename = PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x86/MobaLedLibWrapper.dll'
        Debug.Print("IsSimulatorAvailable:"+dllfilename)
        if Dir(dllfilename) == '':
            Debug.Print("IsSimulatorAvailable:"+dllfilename + " Not found")
            return fn_return_value
        ChDir(PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x86')
    # VB2PY (UntranslatedCode) On Error GoTo SimError
    # call any function to test binding
    loaddll()
    WrapperVersion = GetWrapperVersion()
    # major.minor.revision e.g. 10000 = 01.00.00
    # in case the exported function interface changes you need to increase major/and or minor version
    # if interface is compatible only revision changes
    # fn_return_value = Int(WrapperVersion / 100) == 100  # v1.03 (entfallen)
    fn_return_value = Int(WrapperVersion / 100) == 101  # v1.03
    return fn_return_value

def OpenSimulator():
    Debug.Print("OpenSimulator")
    loaddll()
    
    if not IsSimualtorAvailable():
        return
    if not __LoadConfiguration():  # v1.04 Konfiguration fehlt (noch nicht uebersetzt)
        return  # v1.04
    __StorePosition()
    
    SimLedsX=M28.Get_Num_Config_Var_Range('SimLedsX', 1, 128, 8)
    SimLedsY=M28.Get_Num_Config_Var_Range('SimLedsY', 1, 64, 8)  # v1.03
    SimLedSize=M28.Get_Num_Config_Var_Range('SimLedSize', 4, 64, 24)
    SimOffset=M28.Get_Num_Config_Var_Range('SimOffset', 0, 255, 1)
    SimPosX=M28.Get_Num_Config_Var_Range('SimPosX', - 16383, 16383, 800)
    SimPosY=M28.Get_Num_Config_Var_Range('SimPosY', - 16383, 16383, 400)
    SimOnTop=M28.Get_Num_Config_Var_Range('SimOnTop', 0, 1, 1)==1
    if SimPosX <= -10000 or SimPosY <= -10000 or SimPosX >= 16000 or SimPosY >= 16000:  # v1.12: gespeicherte Lage ungueltig (zum Beispiel -32000 eines minimierten Fensters): Vorgabe, auch in den Einstellungen
        SimPosX, SimPosY = 800, 400  # v1.12
        M28.Set_String_Config_Var('SimPosX', Str(SimPosX))  # v1.12
        M28.Set_String_Config_Var('SimPosY', Str(SimPosY))  # v1.12
    
    Debug.Print("ShowLEDWindow",SimLedsX,SimLedsY,SimLedSize,SimOffset,SimPosX,SimPosY,SimOnTop)
    sim_params.update({'x': int(SimLedsX), 'y': int(SimLedsY), 'size': int(SimLedSize), 'offset': int(SimOffset)})  # v1.06
    ShowLEDWindow(SimLedsX,SimLedsY,SimLedSize,SimOffset,SimPosX,SimPosY,SimOnTop)
    __register_close_at_exit()  # v1.05
    M30.Bring_Application_to_front()
    
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Buffer - ByRef 
def __LoadFile(FileName):
    Debug.Print("__LoadConfiguration:",FileName)
    #fileInt = Integer()
    fileInt = FreeFile()
    try:
        VBFiles.openFile(fileInt, FileName, 'rb')
        f=VBFiles.getFile(fileInt)
        mybytearray = b"" #bytearray()
        length = 0
        byte = f.read(1)
        while byte:
            # Do stuff with byte.
            mybytearray+=byte
            length += 1
            byte = f.read(1)
        
        #VBFiles.openFile(fileInt, FileName, 'rb') # VB2PY (UnknownFileMode) 'Access', 'Read'
        #if LOF(fileInt) == 0:
        #    Buffer = vbObjectInitialize((1,), Variant)
        #    Buffer[0] = 0
        #else:
        #    Buffer = vbObjectInitialize(((0, LOF(fileInt) - 1),), Variant)
        #    Get(fileInt, None , Buffer)
        VBFiles.closeFile(fileInt)
        if length == 0:  # v1.03 wie VBA: leere Datei -> 1 Nullbyte
            mybytearray = b'\0'
            length = 1
        return mybytearray,length
    except IOError:
        # VBFiles.closeFile(fileInt)  # v1.04 (entfallen) Datei war nie geoeffnet -> KeyError
        Debug.Print('Error While Opening the file!')
        return None, 0  # v1.04 (vorher None: Entpacken schlug fehl)

def __LoadConfiguration():
    global __AddressMapping
    
    Debug.Print("__LoadConfiguration")
    Buffer = vbObjectInitialize(objtype=Byte)

    Index = Integer()

    Address = Long()

    Length = Integer()

    if not IsSimualtorAvailable():
        return False  # v1.04
    for fname in ('LEDConfig.bin', 'L2VConfig.bin', 'AddressConfig.bin'):  # v1.04
        if not os.path.isfile(PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + fname):  # v1.04
            Debug.Print("Simulator: Datei fehlt:", fname)  # v1.04
            return False  # v1.04
    Buffer,buflen = __LoadFile(PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'LEDConfig.bin')
    dllBuffer = ctypes.create_string_buffer(Buffer)

    #print(repr(dllBuffer.raw))
    bufferLen = ctypes.c_int(buflen)
    #print(bufferLen,bufferLen.value)
    
    L2VBuffer,l2vlen = __LoadFile(PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'L2VConfig.bin')  # v1.03
    l2vDllBuffer = ctypes.create_string_buffer(L2VBuffer)  # v1.03
    # res=CreateSimulator(dllBuffer, bufferLen)  # v1.03 (entfallen)
    res=CreateSimulatorEx(dllBuffer, bufferLen, l2vDllBuffer, ctypes.c_int(l2vlen))  # v1.03
    #print(res)
    
    Buffer, buflen=__LoadFile(PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'AddressConfig.bin')
    Debug.Print(Buffer)
    Length = buflen #len(Buffer) #UBound(Buffer) - LBound(Buffer) + 1
    __AddressMapping = {} #Scripting.Dictionary()
    if Length >= 3:
        for Index in vbForRange(0, ( Length / 3 )  - 1):
            Address = Buffer[Index * 3 + 1]
            Address = 256 * Address + Buffer[Index * 3]
            __AddressMapping[Address] = Buffer[Index * 3 + 2]
    return True  # v1.04

def ReloadConfiguration():
    Debug.Print("ReloadConfiguration")
    if IsSimualtorAvailable():
        if IsLEDWindowVisible():  # v1.03
            __LoadConfiguration()

def UpdateSimulatorIfNeeded(CreateHeaderFile, AlwaysOpenWindow):
    Debug.Print("UpdateSimulatorIfNeeded")
    fn_return_value = True
    if IsSimualtorAvailable():
        if AlwaysOpenWindow or IsLEDWindowVisible():
            fn_return_value = UploadToSimulator(CreateHeaderFile)
    return fn_return_value
            

_close_registered = False  # v1.05

def __close_at_exit():  # v1.05
    # beim Beenden des Programms das Simulatorfenster schliessen (in Excel schliesst es mit Excel)
    try:
        if IsLEDWindowVisible is not None and IsLEDWindowVisible():
            CloseSimulator()
    except BaseException:
        pass

def __register_close_at_exit():  # v1.05
    global _close_registered
    if not _close_registered:
        _close_registered = True
        atexit.register(__close_at_exit)

def CloseSimulator():
    if IsSimualtorAvailable():
        __StorePosition()
        CloseLEDWindow()

def IsSimulatorActive():
    fn_return_value = None
    if IsSimualtorAvailable():
        fn_return_value = IsLEDWindowVisible()  # v1.03
    Debug.Print("IsSimulatorActive:",fn_return_value)
    return fn_return_value

def ToggleSimulator():
    Debug.Print("ToggleSimulator")
    if IsSimualtorAvailable():
        if IsLEDWindowVisible():  # v1.03
            CloseSimulator()
        else:
            OpenSimulator()
            time.sleep(( 50 ))
            # set focus back to excel
            #*HL AppActivate(ActiveWorkbook.Windows(1).Caption)
            M30.Bring_Application_to_front()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Addr - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Direction - ByVal 
def SendToSimulator(Addr, Direction):
    global __AddressMapping
    Debug.Print("SendToSimulator:",Addr,Direction)
    fn_return_value = False
    if not IsSimualtorAvailable():
        return fn_return_value
    if __AddressMapping is None:
        return fn_return_value
    if IsLEDWindowVisible():
        Channel = 0
        #*HL for Index in vbForRange(0, len(__AddressMapping) - 1):
        for key in __AddressMapping.keys():
            #Address = __AddressMapping.Keys(Index) and 16383
            Address = key & 16383
            Address = Address - P01.val(M28.Get_String_Config_Var("DCC_Offset"))                          # 24.03.21: Juergen
            #AddressType = ( ( __AddressMapping.Keys(Index) and 49152 )  / 16385 )
            
            AddressType = round((key & 49152) / 16385)
            #InCnt = __AddressMapping.Items(Index)
            InCnt = __AddressMapping[key]
            CurrentType = AddressType
            for Index2 in vbForRange(1, InCnt):
                if Address == Addr:
                    if AddressType == 0:
                        SetInput(Channel, Direction)
                        fn_return_value = True
                        return fn_return_value
                    elif CurrentType == 1 and Direction == 0:
                        SetInput(Channel, 1)
                        time.sleep(( 0.400 ))
                        SetInput(Channel, 0)
                        fn_return_value = True
                        return fn_return_value
                    elif CurrentType == 2 and Direction == 1:
                        SetInput(Channel, 1)
                        time.sleep(( 0.400 ))
                        SetInput(Channel, 0)
                        fn_return_value = True
                        return fn_return_value
                if (CurrentType == 0):
                    Address = Address + 1
                elif (CurrentType == 1):
                    CurrentType = 2
                elif (CurrentType == 2):
                    CurrentType = 1
                    Address = Address + 1
                Channel = Channel + 1
    return fn_return_value

def _Log(text, highlight=None):  # v1.09 Meldung ins Fenster "Kompilieren und Hochladen" (Web); mit "OK" schliesst es sich nach einigen Sekunden von selbst
    try:
        weblog = getattr(PG.get_global_controller(), "weblog", None)
        if weblog is not None:
            weblog.add_text_to_textwindow(text, "\n", highlight)
    except BaseException:
        pass

def UploadToSimulator(CreateHeaderFiles):
    Debug.Print("UploadToSimulator")
    fn_return_value = False
    if not IsSimualtorAvailable():
        _Log(M09.Get_Language_Str('Der Simulator ist nicht verfügbar.'), "Error")  # v1.09
        if _linux() and _sim_problem:  # v1.10: Grund nennen
            _Log(_sim_problem, "Error")  # v1.10
            P01.MsgBox(M09.Get_Language_Str('Der Simulator ist nicht verfügbar.') + vbCr + vbCr + _sim_problem, vbCritical, M09.Get_Language_Str('Simulator'))  # v1.10
        return fn_return_value
    _Log(M09.Get_Language_Str('Konfiguration wird für den Simulator übersetzt ...'))  # v1.09
    if CreateHeaderFiles:
        fn_return_value = M06.Create_HeaderFile(True)
    else:
        fn_return_value = True

    if fn_return_value and _linux():  # v1.06 Linux: build_linux.sh mit bash, Ausgabe bei Fehler anzeigen
        fn_return_value = __Upload_Linux()  # v1.09
        if fn_return_value:  # v1.09
            _Log(M09.Get_Language_Str('Simulator ist aktualisiert.'), "OK")  # v1.09
        else:  # v1.09
            _Log(M09.Get_Language_Str('Der Simulator konnte nicht aktualisiert werden.'), "Error")  # v1.09
        return fn_return_value  # v1.09
    if fn_return_value:
        CommandStr = PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + M02.CfgBuild_Script + " silent"
        if __Create_Compile_Script():
            fn_return_value = M40.ShellAndWait(CommandStr, 0, vbMinimizedNoFocus, M40.PromptUser) == M40.Success
            if fn_return_value:
                if Dir(PG.ThisWorkbook.Path + "/" + M02.Cfg_Dir_LED + "result.txt") == "" :
                    OpenSimulator()
                else:
                    #rerun command to show output to user
                    CommandStr = PG.ThisWorkbook.Path + "/" + M02.Cfg_Dir_LED + M02.CfgBuild_Script
                    Res = PG.get_dialog_parent().execute_shell_cmd(CommandStr,"Compile Simulator")
                    #M40.ShellAndWait(CommandStr, 0, vbNormalFocus, M40.PromptUser)
        #*HL AppActivate(ActiveWorkbook.Windows(1).Caption)
        M30.Bring_Application_to_front()
    # v1.09: Ergebnis ins Log-Fenster, sonst bleibt es mit der Kopfzeile stehen
    if fn_return_value:
        _Log(M09.Get_Language_Str('Simulator ist aktualisiert.'), "OK")
    else:
        _Log(M09.Get_Language_Str('Der Simulator konnte nicht aktualisiert werden.'), "Error")
    return fn_return_value

def __Upload_Linux():  # v1.06
    cfgdir = PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED
    script = __Create_Compile_Script_Linux()
    if not script:
        return False
    try:
        res = subprocess.run(["bash", script, "silent"], capture_output=True, text=True, timeout=300, cwd=cfgdir)
    except BaseException as e:
        P01.MsgBox(str(e), vbCritical, M09.Get_Language_Str('Simulator'))
        return False
    if os.path.isfile(cfgdir + 'result.txt') or res.returncode != 0:
        tail = "\n".join((res.stdout + res.stderr).strip().splitlines()[-15:])
        P01.MsgBox(M09.Get_Language_Str('Fehler beim Uebersetzen fuer den Simulator') + ":\n" + tail, vbCritical, M09.Get_Language_Str('Simulator'))
        return False
    if not IsLEDWindowVisible():
        OpenSimulator()
    else:
        __LoadConfiguration()
    return True

def __Create_Compile_Script_Linux():  # v1.06
    # Werkzeuge suchen: eigene Angabe MLL_AVR_BIN, PlatformIO (toolchain-atmelavr), Arduino IDE, Suchpfad
    core = os.environ.get("PLATFORMIO_CORE_DIR") or os.path.join(os.path.expanduser("~"), ".platformio")
    packages = os.path.join(core, "packages")
    tooldirs = [os.environ.get("MLL_AVR_BIN", ""), os.path.join(packages, "toolchain-atmelavr", "bin")]
    platdirs = [os.environ.get("MLL_AVR_PLATFORM", ""), os.path.join(packages, "framework-arduino-avr")]
    try:
        ide = M30.FilePath(M08.Find_ArduinoExe())
        if ide:
            tooldirs.append(os.path.join(ide, "hardware", "tools", "avr", "bin"))
            platdirs.append(os.path.join(ide, "hardware", "arduino", "avr"))
    except BaseException:
        pass
    found = shutil.which("avr-g++")
    if found:
        tooldirs.append(os.path.dirname(found))
    tool = next((d for d in tooldirs if d and os.path.isfile(os.path.join(d, "avr-g++"))), None)
    plat = next((d for d in platdirs if d and os.path.isdir(os.path.join(d, "cores", "arduino"))), None)
    lib = PG.ThisWorkbook.Path + '/libraries/MobaLedLib/src'
    if not os.path.isfile(lib + '/MobaLedLib.h'):
        lib = M30.DelLast(M02a.Get_Ardu_LibDir()) + '/MobaLedLib/src'
    if tool is None or plat is None:
        P01.MsgBox(M09.Get_Language_Str('Fuer den Simulator werden die AVR-Werkzeuge gebraucht (PlatformIO: Paket toolchain-atmelavr und framework-arduino-avr, oder Arduino IDE). Ordner mit avr-g++:') + ' ' + str(tool) + ' / ' + str(plat), vbCritical, M09.Get_Language_Str('Simulator'))
        return None
    name = PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'build_linux.sh'
    Debug.Print("Create_Compile_Script_Linux:" + name)
    # v1.10: Die mitgelieferte Configuration.cpp bindet die Header mit Windows-Pfaden ein (..\\LEDs_AutoProg\\...): unter Linux unbrauchbar (dann bleibt FastLED.h uebrig und die Meldung
    # "The FastLED library must be installed"). Deshalb eine eigene Datei mit Schraegstrichen; CONFIG_ONLY verhindert, dass die FastLED-Bibliothek eingebunden wird.
    cfgdir = PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED
    inodir = PG.ThisWorkbook.Path + '/' + M02.Ino_Dir_LED
    src = ['#define CONFIG_ONLY', '', '#include <Arduino.h>']
    if os.path.isfile(inodir + 'MP3.h'):
        src.append('#include "../' + M02.Ino_Dir_LED.strip('/') + '/MP3.h"')
    src += ['#include "../' + M02.Ino_Dir_LED.strip('/') + '/LEDs_AutoProg.h"', '', 'int main()', '{', '#if defined(USE_EXT_ADDR)', '    int ex = (int)&Ext_Addr[0];', '#else', '    int ex = 0;', '#endif',
            '#if defined(USE_LED_TO_VAR)', '    int ldv = (int)&LED2Var_Tab[0];', '#else', '    int ldv = 0;', '#endif', '  return (int)&Config[0]+ex+ldv;', '}', '']
    try:
        with open(cfgdir + 'Configuration_linux.cpp', 'w', encoding='utf-8', newline='\n') as fh:
            fh.write("\n".join(src))
    except OSError as e:
        P01.MsgBox(M09.Get_Language_Str('Fehler beim Schreiben der Datei') + " 'Configuration_linux.cpp': " + str(e), vbCritical, M09.Get_Language_Str('Simulator'))
        return None
    q = lambda t: '"' + t + '"'
    cc = ('-c -g -Os -Wall -std=gnu++11 -fpermissive -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -Wno-error=narrowing -MMD -flto '
          '-mmcu=atmega328p -DF_CPU=16000000L -DARDUINO=10813 -DARDUINO_AVR_NANO -DARDUINO_ARCH_AVR')
    lines = ['#!/usr/bin/env bash', '# erzeugt von webMobaLedLib (M39_Simulator 1.06), nicht von Hand aendern',
             'cd "$(dirname "$0")"', 'errorfile=result.txt', 'tool=' + q(tool), 'plat=' + q(plat), 'lib=' + q(lib),
             'fail() { echo fail > "$errorfile"; echo "Da ist was schief gegangen"; exit 1; }',
             '"$tool/avr-g++" ' + cc + ' "-I$plat/cores/arduino" "-I$plat/variants/eightanaloginputs" "-I$lib" Configuration_linux.cpp -o Configuration.cpp.o || fail',
             '"$tool/avr-gcc" -Wall -Os -g -flto -fuse-linker-plugin -Wl,--gc-sections -mmcu=atmega328p -o Configuration.elf Configuration.cpp.o -lm || fail',
             '"$tool/avr-objcopy" -O binary -j .MLLLedConfig Configuration.elf LEDConfig.bin || fail',
             '"$tool/avr-objcopy" -O binary -j .MLLAddressConfig Configuration.elf AddressConfig.bin || fail',
             '"$tool/avr-objcopy" -O binary -j .MLLL2VConfig Configuration.elf L2VConfig.bin || fail',
             'rm -f "$errorfile"', '']
    try:
        with open(name, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write("\n".join(lines))
        os.chmod(name, 0o755)
        rf = PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'result.txt'
        if os.path.isfile(rf):
            os.remove(rf)
    except OSError as e:
        P01.MsgBox(M09.Get_Language_Str('Fehler beim Schreiben der Datei') + " '" + name + "': " + str(e), vbCritical, M09.Get_Language_Str('Simulator'))
        return None
    return name

def __StorePosition():
    Debug.Print("StorePosition")
    currentPos = RECT()
    if GetLEDWindowRect(currentPos) == 1:
        if currentPos.left <= -10000 or currentPos.top <= -10000 or currentPos.left >= 16000 or currentPos.top >= 16000:  # v1.12: minimiertes Fenster (Windows: -32000), Lage nicht speichern
            Debug.Print("StorePosition: Fenster minimiert oder ausserhalb, Lage nicht gespeichert", currentPos.left, currentPos.top)  # v1.12
            return  # v1.12
        M28.Set_String_Config_Var('SimPosX', Str(currentPos.left))
        M28.Set_String_Config_Var('SimPosY', Str(currentPos.top))

def __ConfigurationToFile():
    Debug.Print("ConfigurationToFile")
    fName = String()

    fName2 = String()

    Line = String()

    fn = Integer()

    fn2 = Integer()

    i = Integer()

    OutputFilename = String()
    fName = Environ(M02.Env_USERPROFILE) + '\\AppData\\Local\\Temp\\pyMobaLedLib_build\\ATMega\\LEDs_AutoProg.ino.elf.txt'
    fName2 = Environ(M02.Env_USERPROFILE) + '\\AppData\\Local\\Temp\\pyMobaLedLib_build\\ATMega\\LEDs_AutoProg.ino.with_bootloader.bin'
    if Dir(fName) == '':
        return
    if Dir(fName2) == '':
        return
    fn = FreeFile()
    VBFiles.openFile(fn, fName, 'r') 
    while not EOF(fn):
        Line = VBFiles.getLineInput(fn, 1)
        i = InStrRev(Line, ' ')
        if i > 0:
            TypeName = Mid(Line, i + 1)
            if TypeName == '_ZL6Config' or TypeName == '_ZL8Ext_Addr':
                Line = Replace(Line, '  ', ' ')
                Line = Replace(Line, '  ', ' ')
                Line = Replace(Line, '  ', ' ')
                Splits = Split(Line)
                Offset = CInt('&h0' + Splits(2))
                Length = P01.val(Splits(3))
                fn2 = FreeFile()
                VBFiles.openFile(fn2, fName2, 'b') 
                VBFiles.seekFile(fn2, Offset + 1)
                Buffer = vbObjectInitialize((Length - 1,), Variant)
                Get(fn2, VBGetMissingArgument(Get, 1), Buffer)
                VBFiles.closeFile(fn2)
                fn2 = FreeFile()
                if TypeName == '_ZL6Config':
                    OutputFilename = PG.ThisWorkbook.Path + '\\LEDs_AutoProg\\LEDConfig.bin'
                elif TypeName == '_ZL8Ext_Addr':
                    OutputFilename = PG.ThisWorkbook.Path + '\\LEDs_AutoProg\\DCCConfig.bin'
                if Dir(OutputFilename) != '':
                    Kill(OutputFilename)()
                VBFiles.openFile(fn2, OutputFilename, 'b') 
                Put(fn2, VBGetMissingArgument(Put, 1), Buffer)
                VBFiles.closeFile(fn2)
    VBFiles.closeFile(fn)
    ReloadConfiguration()

def __Create_Compile_Script():
   
    fn_return_value = None
    Name = String()

    fp = Integer()
    Name = PG.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + M02.CfgBuild_Script
    Debug.Print("Create_Compile_Script:"+Name)
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM This file was generated by \'' + PG.ThisWorkbook.Name + '\'  ' + Time, '\n')
    if M30.Win10_or_newer():
        VBFiles.writeText(fp, 'CHCP 65001 >NUL', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'color 79', '\n')
    VBFiles.writeText(fp, 'set scriptDir=%~d0%~p0', '\n')
    VBFiles.writeText(fp, 'set errorfile="%~d0%~p0\\result.txt"', '\n')
    VBFiles.writeText(fp, '%~d0', '\n')
    VBFiles.writeText(fp, 'cd "%~p0"', '\n')
    VBFiles.writeText(fp, 'set packagePath=%USERPROFILE%\\' + M02.AppLoc_Ardu, '\n')
    VBFiles.writeText(fp, 'set toolPath=' + M30.FilePath(M08.Find_ArduinoExe()) + 'hardware\\tools\\avr\\bin', '\n')
    VBFiles.writeText(fp, 'set platformPath=' + M30.FilePath(M08.Find_ArduinoExe()) + 'hardware\\arduino\\avr', '\n')
    # VBFiles.writeText(fp, 'set libraryPath=' + M08.GetShortPath(M30.DelLast(M02.Get_Ardu_LibDir())), '\n')  # v1.02 (entfallen)
    VBFiles.writeText(fp, 'set libraryPath=' + M08.GetShortPath(M30.DelLast(M02a.Get_Ardu_LibDir())), '\n')  # v1.02
    VBFiles.writeText(fp, '"%toolPath%/avr-g++" -c -g -Os -Wall -std=gnu++11 -fpermissive -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -Wno-error=narrowing -MMD -flto -mmcu=atmega328p -DF_CPU=16000000L -DARDUINO=10813 -DARDUINO_AVR_NANO -DARDUINO_ARCH_AVR "-I%platformPath%\\cores\\\\arduino" "-I%platformPath%\\variants\\\\eightanaloginputs"  "-I%libraryPath%\\MobaLedLib\\src"  "%scriptDir%Configuration.cpp" -o "%scriptDir%Configuration.cpp.o"', '\n')
    VBFiles.writeText(fp, 'if errorlevel 1 goto :error', '\n')
    VBFiles.writeText(fp, '"%toolPath%/avr-gcc" -Wall -Os -g -flto -fuse-linker-plugin -Wl,--gc-sections -mmcu=atmega328p -o "%scriptDir%Configuration.elf" "%scriptDir%Configuration.cpp.o" -lm', '\n')
    VBFiles.writeText(fp, 'if errorlevel 1 goto :error', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'Rem "%toolPath%/avr-readelf" -a "%scriptDir%Configuration.elf" >"%scriptDir%Configuration.elf.txt"', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '"%toolPath%/avr-objcopy" -O binary -j .MLLLedConfig "%scriptDir%Configuration.elf" "%scriptDir%LEDConfig.bin"', '\n')
    VBFiles.writeText(fp, 'if errorlevel 1 goto :error', '\n')
    VBFiles.writeText(fp, '"%toolPath%/avr-objcopy" -O binary -j .MLLAddressConfig "%scriptDir%Configuration.elf" "%scriptDir%AddressConfig.bin"', '\n')
    VBFiles.writeText(fp, 'if errorlevel 1 goto :error', '\n')
    VBFiles.writeText(fp, '"%toolPath%/avr-objcopy" -O binary -j .MLLL2VConfig "%scriptDir%Configuration.elf" "%scriptDir%L2VConfig.bin"', '\n')  # v1.03
    VBFiles.writeText(fp, 'if errorlevel 1 goto :error', '\n')  # v1.03
    VBFiles.writeText(fp, 'if exist %errorfile% del %errorfile%', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'goto :eof', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, ':error', '\n')
    VBFiles.writeText(fp, 'if not "%1"=="silent" (', '\n')  # v1.03
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO   ****************************************', '\n')
    VBFiles.writeText(fp, '   ECHO    Da ist was schief gegangen ;-(', '\n')
    VBFiles.writeText(fp, '   ECHO   ****************************************', '\n')
    VBFiles.writeText(fp, '   Pause', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, 'echo fail>%errorfile%', '\n')
    VBFiles.writeText(fp, 'exit /b 1', '\n')
    VBFiles.closeFile(fp)
    fn_return_value = True
    return fn_return_value
    VBFiles.closeFile(fp)
    P01.MsgBox(M09.Get_Language_Str('Fehler beim Schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Start Datei'))
    fn_return_value = False
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function CreateSampleConfig Lib "MobaLedLibWrapper.dll" () As LongPtr
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function CreateSimulator Lib "MobaLedLibWrapper.dll" Alias "Create" ( _\nconfigData As Any, ByVal configLength As Integer) As LongPtr
# VB2PY (UntranslatedCode) Private Declare Sub SetInput Lib "MobaLedLibWrapper.dll" (ByVal Channel As Byte, ByVal IsOn As Byte)
# VB2PY (UntranslatedCode) Private Declare Sub UpdateLeds Lib "MobaLedLibWrapper.dll" Alias "Update" ()
# VB2PY (UntranslatedCode) Private Declare Function GetInput Lib "MobaLedLibWrapper.dll" (ByRef Channel As Byte) As Byte
# VB2PY (UntranslatedCode) Private Declare Sub ShowLEDWindow Lib "MobaLedLibWrapper.dll" ( _\nByVal ledsX As Byte, ByVal ledsY As Byte, ByVal ledSize As Byte, ByVal ledOffset As Byte, _\nByVal windowPosX As Integer, ByVal windowPosY As Integer, automaticUpdate As Boolean)
# VB2PY (UntranslatedCode) Private Declare Sub CloseLEDWindow Lib "MobaLedLibWrapper.dll" ()
# VB2PY (UntranslatedCode) Private Declare Function IsLEDWindowVisible Lib "MobaLedLibWrapper.dll" () As Byte
# VB2PY (UntranslatedCode) Private Declare Function GetLEDWindowRect Lib "MobaLedLibWrapper.dll" (lpRect As RECT) As Long
# VB2PY (UntranslatedCode) Private Declare Function GetWrapperVersion Lib "MobaLedLibWrapper.dll" () As Long
