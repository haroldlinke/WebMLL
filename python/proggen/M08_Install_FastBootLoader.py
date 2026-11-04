# Datei-Version: 1.03 (2026-11-03) - M08_Install_FastBootLoader.py
# ----------------------------------------------------------------------------------------------
# Name:           M08_Install_FastBootLoader.py
# Path:           proggen/M08_Install_FastBootLoader.py
# Version:        1.03
# Last Update:    2026-11-03
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-12  Stand der Umstellung (nicht erfasst)
#   1.01  2026-10-28  M02a.Get_BoardTyp und M02a.Get_SrcDirInLib (standen faelschlich bei M02); der nicht uebernommene Dialog meldet sich mit einem Hinweis statt abzustuerzen
#   1.02  2026-11-03  Schneller Bootloader mit PlatformIO: Hinweis zu den Jumpern, ArduinoISP als fertige .hex hochladen, Bootloader mit dem avrdude von PlatformIO schreiben, danach wieder das Programm auf den rechten Arduino
#   1.03  2026-11-03  Jeder Schritt hat im Fenster des Arduino-Monitors eine eigene Ueberschrift (Schritt 1 bis 3)
# ----------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#
#         M08 Fast_ARDUINO
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2022
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
# 2021-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2022-01-07 v4.02 HL: - Else:, ByRef check done, first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

import time


# fromx proggen.M02_Public import *
# fromx proggen.M06_Write_Header_LED2Var import *
# fromx proggen.M06_Write_Header_Sound import *
# fromx proggen.M06_Write_Header_SW import *
# fromx proggen.M09_Language import *
# fromx proggen.M09_Select_Macro import *
# fromx proggen.M20_PageEvents_a_Functions import *
# fromx proggen.M25_Columns import *
# fromx proggen.M28_Diverse import *
# fromx proggen.M30_Tools import *

# fromx proggen.M80_Create_Multiplexer import *


import proggen.M02_Public as M02
import proggen.M02a_Public as M02a
#import proggen.M02_Scripting as Scripting
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
import proggen.M06_Write_Header as M06
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
import proggen.M12_Copy_Prog as M12
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M40_ShellandWait as M40
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Multiplexer as M80

import proggen.F00_mainbuttons as F00

import ExcelAPI.XLA_Application as P01

import mlpyproggen.Prog_Generator as PG


from vb2py.vbfunctions import *
from vb2py.vbdebug import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" Bootloader Programmieren:
 - Jumper setzen unten die linken Pins verbinden
 - ArduinoISP aud DCC spielen
 - Bootloader schreiben
 - Fragen ob noch weitere Arduinos Programmiert werden sollen
 - Wenn Nein, dann wieder das DCC Prog. Installieren (Wichtig)
 - Jumper öffnen
----------------------------------------------------------------
------------------------------------------------------------------------------------
UT---------------------------------------------------------
---------------------------------------------
----------------------------------
"""


def __Install_ArduinoISP_to_Right_Arduino():
    fn_return_value = False
    InoName = String()

    SrcDir = String()

    DstDir = String()
    #----------------------------------------------------------------
    # Compile and upload the ArduinoISP program to the right Arduino
    M25.Make_sure_that_Col_Variables_match()
    InoName = 'ArduinoISP.ino'
    DstDir = M08.GetWorkbookPath() + '/' + M30.FileName(InoName) + '/'
    SrcDir = M30.FilePath(M08.Find_ArduinoExe()) + 'examples/11.ArduinoISP/ArduinoISP/'
    M30.CreateFolder(DstDir)
    if not M12.FileCopy_with_Check(DstDir, InoName, SrcDir + InoName):
        return fn_return_value
    if M08.Compile_and_Upload_Prog_to_Arduino(InoName, M25.COMPrtR_COL, M25.BUILDOpRCOL, DstDir):
        P01.CellDict[M02.SH_VARS_ROW, M25.R_UPLOD_COL] = 'R ISP'
        fn_return_value = True
    return fn_return_value

def Create_WriteFastBootloader_cmd(SrcDir):
    fn_return_value = False
    Name = String()

    fp = Integer()
    #------------------------------------------------------------------------------------
    # "C:\Users\Hardi\AppData\Local\Arduino15\packages\arduino\tools\avrdude\6.3.0-arduino17/bin/avrdude" ^
    #    "-CC:\Users\Hardi\AppData\Local\Arduino15\packages\arduino\tools\avrdude\6.3.0-arduino17/etc/avrdude.conf"
    #    -v -patmega328p -cstk500v1 -PCOM3 -b19200 ^
    #    "-Uflash:w:C:\Program Files (x86)\Arduino\hardware\arduino\avr/bootloaders/optiboot/optiboot_atmega328.hex:i" ^
    #    -Ulock:w:0x0F:m
    Name = SrcDir + 'WriteFastBootloader.cmd'
    #If Dir(Name) <> "" Then                                                  ' 04.11.20: Always write the file
    #   Create_WriteFastBootloader_cmd = Name
    #   Exit Function
    #End If
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM Write the fast Bootloader to the left Arduino', '\n')
    VBFiles.writeText(fp, 'REM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', '\n')
    VBFiles.writeText(fp, 'REM Parameter:               Example', '\n')
    VBFiles.writeText(fp, 'REM  1: Arduino EXE Path:    "C:\\Program Files (x86)\\Arduino\\"', '\n')
    VBFiles.writeText(fp, 'REM  2: Port:                -PCOM3', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM The program uses the captured and adapted command line from the Arduino IDE', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'Rem Using the private OptiBoot version 108.1 to indicate that the HFUSE is set to DE', '\n')
    VBFiles.writeText(fp, 'Rem This bootloader is equal to version 8.1', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM This file was automatically generated by the program ' + PG.ThisWorkbook.Name + ' ' + M02.Prog_Version + '      by Hardi', '\n')
    VBFiles.writeText(fp, 'REM File creation: ' + P01.Date() + ' ' + P01.Time_str(), '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'SET ArduinoExePath=%~1', '\n')
    VBFiles.writeText(fp, 'SET Port=%2', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '"%ArduinoExePath%\\hardware\\tools\\avr/bin/avrdude" ^', '\n')
    VBFiles.writeText(fp, '   "-C%ArduinoExePath%hardware\\tools\\avr\\etc\\avrdude.conf" ^', '\n')
    VBFiles.writeText(fp, '   -patmega328p -F -cstk500v1 %Port%  -b19200 ^', '\n')
    VBFiles.writeText(fp, '   -U signature:r:signature.hex:h', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'if %errorlevel%==1 goto :error', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'set /p signature=<signature.hex', '\n')
    VBFiles.writeText(fp, 'if %errorlevel%==1 goto :error', '\n')
    VBFiles.writeText(fp, 'set cpuType=', '\n')
    VBFiles.writeText(fp, 'set message=', '\n')
    VBFiles.writeText(fp, 'if "%signature%"=="0x1e,0x95,0x16" (', '\n')
    VBFiles.writeText(fp, '  set cpuType=atmega328pb', '\n')
    if FlashAs328P:
        VBFiles.writeText(fp, '  set filename=optiboot_atmega328_Ver108.1.hex', '\n')
    else:
        VBFiles.writeText(fp, '  set filename=optiboot_atmega328pb_16mhz.hex', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, 'if "%signature%"=="0x1e,0x95,0xf" (', '\n')
    VBFiles.writeText(fp, '  set cpuType=atmega328p', '\n')
    VBFiles.writeText(fp, '  set filename=optiboot_atmega328_Ver108.1.hex', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, 'if "%cpuType%"=="" set message=CPU with signature %signature% is not supported', '\n')
    VBFiles.writeText(fp, 'if "%signature%"=="0x0,0x0,0x0" set message=           can\'t read device signature', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'ECHO/', '\n')
    VBFiles.writeText(fp, 'ECHO/', '\n')
    VBFiles.writeText(fp, 'ECHO/', '\n')
    VBFiles.writeText(fp, 'ECHO/', '\n')
    VBFiles.writeText(fp, 'ECHO/', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'if not "%message%"=="" (', '\n')
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO ******************************************************', '\n')
    VBFiles.writeText(fp, '   ECHO *                                                    *', '\n')
    VBFiles.writeText(fp, '   ECHO * %message% *', '\n')
    VBFiles.writeText(fp, '   ECHO *                                                    *', '\n')
    VBFiles.writeText(fp, '   ECHO ******************************************************', '\n')
    VBFiles.writeText(fp, '   PAUSE', '\n')
    VBFiles.writeText(fp, '   goto :eof', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '"%ArduinoExePath%\\hardware\\tools\\avr/bin/avrdude" ^', '\n')
    VBFiles.writeText(fp, '   "-C%ArduinoExePath%hardware\\tools\\avr\\etc\\avrdude.conf" ^', '\n')
    VBFiles.writeText(fp, '   -v -p%cpuType% -cstk500v1 %Port%  -b19200 ^', '\n')
    #Print #fp, "   ""-Uflash:w:%ArduinoExePath%hardware\arduino\avr/bootloaders/optiboot/optiboot_atmega328.hex:i"" ^"
    # Standard Optiboot bootloader
    #Print #fp, "   ""-Uflash:w:" & GetShortPath(SrcDir & "optiboot_atmega328_Ver108.1.hex") & ":i"" ^"
    # 08.12.23:
    # VBFiles.writeText(fp, '   "-Uflash:w:' + M08.GetShortPath(M02.Get_SrcDirInLib() + 'ArduinoISP\\') + '\\%filename%' + ':i" ^', '\n')  # v1.01 (entfallen)
    VBFiles.writeText(fp, '   "-Uflash:w:' + M08.GetShortPath(M02a.Get_SrcDirInLib() + 'ArduinoISP\\') + '\\%filename%' + ':i" ^', '\n')  # v1.01
    # 08.12.23:
    VBFiles.writeText(fp, '   -Ulock:w:0x0F:m ^', '\n')
    VBFiles.writeText(fp, '   -Uhfuse:w:0xDE:m', '\n')
    # 29.10.20: Reserve only 512 Byte for the bootloader
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'if %errorlevel%==1 goto error', '\n')
    VBFiles.writeText(fp, 'goto :eof', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, ':error', '\n')
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO *************************************', '\n')
    VBFiles.writeText(fp, '   ECHO *                                   *', '\n')
    VBFiles.writeText(fp, '   ECHO * Error writing the boot loader ;-( *', '\n')
    VBFiles.writeText(fp, '   ECHO *                                   *', '\n')
    VBFiles.writeText(fp, '   ECHO *************************************', '\n')
    VBFiles.writeText(fp, '   PAUSE', '\n')
    VBFiles.writeText(fp, ')', '\n') # may be not needed anymore
    VBFiles.writeText(fp, '', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = Name
    return fn_return_value
    P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Compile und Flash Datei'))
    return fn_return_value

def __Test_Create_WriteFastBootloader_cmd():
    #UT---------------------------------------------------------
    Debug.Print(Create_WriteFastBootloader_cmd(M08.GetWorkbookPath() + '\\ArduinoISP\\'))

def Write_Bootloader(FlashAs328P):
    fn_return_value = None
    #hwnd = LongPtr()

    #CmdName = String()

    #CommandStr = String()

    #Res = ShellAndWaitResult()
    #---------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    #*HL hwnd = Application.hwnd
    CmdName = Create_WriteFastBootloader_cmd(M08.GetWorkbookPath() + '\\ArduinoISP\\', FlashAs328P)
    # 09.12.23 Juergen Support of ATMega328PB
    if CmdName == '':
        return fn_return_value
    CommandStr = '"' + CmdName + '" "' + M30.FilePath(M08.Find_ArduinoExe()) + '"' + ' -PCOM' + P01.Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL)
    Res = M40.ShellAndWait(CommandStr, 0, vbNormalFocus, M40.PromptUser)
    if (Res == M40.Success) or (Res == M40.Timeout):
        pass
    else:
        P01.Unload(F00.StatusMsg_UserForm)
        P01.MsgBox(M09.Get_Language_Str('Fehler ') + Res + M09.Get_Language_Str(' beim Starten des Arduino Programms \'') + CommandStr + '\'', vbCritical,M09.Get_Language_Str('Fehler beim Starten des Arduino programms'))
    #*HL Bring_to_front(hwnd)
    fn_return_value = True
    return fn_return_value

def __Old_Prog():
    M08.Compile_and_Upload_Prog_to_Right_Arduino()

# def __Run_Avrdude(Command):  # v1.03 (entfallen)
def __Run_Avrdude(Command, Title=''):  # v1.03
    # PlatformIO: einen avrdude-Befehl im Fenster des Arduino-Monitors ausfuehren (wie das Hochladen); True, wenn er ohne Fehler endete
    PG.global_controller.disconnect()  # v1.02
    # Res = PG.dialog_parent.start_ARDUINO_program_cmd(Command, arduino_type='Right', empty_text=False, show_intro=False)  # v1.03 (entfallen)
    Res = PG.dialog_parent.start_ARDUINO_program_cmd(Command, arduino_type='Right', empty_text=False, show_intro=False, title=Title)  # v1.03
    return (Res == M40.Success) or (Res == M40.Timeout)  # v1.02


def __Jumper_Text():  # v1.02
    # Der Hinweis zu den Jumpern wie im Dialog des Excel-Programms (Texte des Blatts Languages)
    return M09.Get_Language_Str('Mit dem verbesserten Bootloader wird das Programm, bei einer Änderung der Konfiguration, deutlich schneller zum Arduino geschickt. ' + vbCr + vbCr + 'Dazu müssen die Jumper unter dem linken Arduino so wie im Bild gezeigt gesetzt werden (Der untere Jumper verbindet den linken mit dem mittleren Pin.)' + vbCr + vbCr + 'Danach wird der Arduino wieder eingesteckt und der rechte Arduino mit dem USB Anschluss des PC\'s verbunden.' + vbCr + vbCr + 'Die Jumper sind erst ab der Hardware Version 1.5 der Hauptplatine vorhanden.')  # v1.02


def __Install_ArduinoISP_hex_to_Right_Arduino():  # v1.02
    # PlatformIO: die fertige Datei 03.ArduinoISP.hex (Ordner libraries/MobaLedLib/firmware) auf den rechten Arduino laden (statt die Quelle ArduinoISP.ino der IDE zu uebersetzen)
    import os  # v1.02
    import headless.headless_isp as HI  # v1.02
    fn_return_value = False  # v1.02
    M25.Make_sure_that_Col_Variables_match()  # v1.02
    HexFile = M08.Right_Arduino_Hex(HI.ISP_INO)  # v1.02
    if HexFile == '':  # v1.02
        M08.Show_Hex_Missing(HI.ISP_INO)  # v1.02
        return fn_return_value  # v1.02
    if F00.port_is_available(M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value):  # v1.02
        M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value = F00.port_set_busy(M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value)  # v1.02
    # if M08.Compile_and_Upload_Prog_to_Arduino(HI.ISP_INO, M25.COMPrtR_COL, M25.BUILDOpRCOL, os.path.dirname(HexFile) + '/', HexFile=HexFile):  # v1.03 (entfallen)
    if M08.Compile_and_Upload_Prog_to_Arduino(HI.ISP_INO, M25.COMPrtR_COL, M25.BUILDOpRCOL, os.path.dirname(HexFile) + '/', HexFile=HexFile, StepTitle=M09.Get_Language_Str('Schritt 1 von 3: ArduinoISP auf den rechten Arduino laden')):  # v1.03
        P01.CellDict[M02.SH_VARS_ROW, M25.R_UPLOD_COL] = 'R ISP'  # v1.02
        fn_return_value = True  # v1.02
    return fn_return_value  # v1.02


def Write_Bootloader_PIO(State):  # v1.02
    # PlatformIO: den Bootloader auf den linken Arduino schreiben (ueber den ArduinoISP des rechten Arduino): Signatur lesen, Bootloader-Datei waehlen, schreiben.
    # State['FlashAs328P'] merkt die Antwort auf die Frage bei einem ATmega328PB (None = noch nicht gefragt). True bei Erfolg.
    import os  # v1.02
    import tempfile  # v1.02
    import headless.headless_isp as HI  # v1.02
    Exe, Conf = HI.find_avrdude()  # v1.02
    if Exe == '':  # v1.02
        P01.MsgBox(M09.Get_Language_Str('avrdude wurde nicht gefunden.') + vbCr + vbCr + M09.Get_Language_Str('avrdude gehört zu PlatformIO (Paket tool-avrdude) und wird mit der Plattform atmelavr installiert, zum Beispiel beim ersten Hochladen für einen Nano. Bitte einmal ein Programm für den Nano übersetzen oder hochladen und es dann noch einmal versuchen.'), vbCritical, 'PlatformIO')  # v1.02
        return False  # v1.02
    Port = F00.port_check_format(P01.Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL))  # v1.02
    SigFile = os.path.join(tempfile.gettempdir(), 'webmobaledlib_signature.hex')  # v1.02
    if os.path.isfile(SigFile):  # v1.02
        os.remove(SigFile)  # v1.02
    if os.name == 'nt':  # v1.02
        Exe, Conf, SigFile = M08.GetShortPath(Exe), M08.GetShortPath(Conf), M08.GetShortPath(os.path.dirname(SigFile)) + '\\' + os.path.basename(SigFile)  # v1.02
    # if not __Run_Avrdude(HI.read_signature_cmd(Exe, Conf, Port, SigFile)):  # v1.03 (entfallen)
    if not __Run_Avrdude(HI.read_signature_cmd(Exe, Conf, Port, SigFile), M09.Get_Language_Str('Schritt 2 von 3: Signatur des linken Arduino lesen')):  # v1.03
        P01.MsgBox(M09.Get_Language_Str('Fehler beim Schreiben des Bootloaders.') + vbCr + M09.Get_Language_Str('Die Meldungen von avrdude stehen im Fenster des Arduino-Monitors.'), vbCritical, M09.Get_Language_Str('Bootloader nicht geschrieben'))  # v1.02
        return False  # v1.02
    SigText = HI.read_text(SigFile)  # v1.02
    Cpu, Problem = HI.signature_cpu(SigText)  # v1.02
    if Problem == 'unreadable':  # v1.02
        P01.MsgBox(M09.Get_Language_Str('Die Signatur des Mikrocontrollers am linken Arduino konnte nicht gelesen werden.') + vbCr + vbCr + M09.Get_Language_Str('Sind die Jumper gesetzt und ist der linke Arduino eingesteckt?'), vbCritical, M09.Get_Language_Str('Bootloader nicht geschrieben'))  # v1.02
        return False  # v1.02
    if Problem == 'unsupported':  # v1.02
        P01.MsgBox(Replace(M09.Get_Language_Str('Der Mikrocontroller mit der Signatur #1# wird nicht unterstützt (nur ATmega328P und ATmega328PB).'), '#1#', HI.signature_text(SigText)), vbCritical, M09.Get_Language_Str('Bootloader nicht geschrieben'))  # v1.02
        return False  # v1.02
    if Cpu == 'atmega328pb' and State.get('FlashAs328P') is None:  # v1.02
        State['FlashAs328P'] = P01.MsgBox(M09.Get_Language_Str('Am linken Arduino sitzt ein ATmega328PB.') + vbCr + vbCr + M09.Get_Language_Str('Soll der Bootloader für den ATmega328P geschrieben werden (die Signatur wird die des ATmega328P)? Das ist die Vorgabe des Excel-Programms.'), vbYesNo + vbQuestion, M09.Get_Language_Str('ATmega328PB erkannt')) == vbYes  # v1.02
    Name = HI.bootloader_name(Cpu, State.get('FlashAs328P') is not False)  # v1.02
    Dirs = HI.bootloader_dirs(M02a.Get_SrcDirInLib())  # v1.02
    BootFile = HI.find_bootloader(Name, Dirs)  # v1.02
    if BootFile == '':  # v1.02
        P01.MsgBox(Replace(M09.Get_Language_Str('Die Datei #1# mit dem Bootloader wurde nicht gefunden.'), '#1#', Name) + vbCr + vbCr + M09.Get_Language_Str('Sie muss in diesem Ordner liegen:') + vbCr + Join(Dirs, vbCr), vbCritical, M09.Get_Language_Str('Datei nicht gefunden'))  # v1.02
        return False  # v1.02
    if os.name == 'nt':  # v1.02
        BootFile = M08.GetShortPath(BootFile)  # v1.02
    # if not __Run_Avrdude(HI.write_cmd(Exe, Conf, Cpu, Port, BootFile)):  # v1.03 (entfallen)
    if not __Run_Avrdude(HI.write_cmd(Exe, Conf, Cpu, Port, BootFile), M09.Get_Language_Str('Schritt 3 von 3: Bootloader auf den linken Arduino schreiben')):  # v1.03
        P01.MsgBox(M09.Get_Language_Str('Fehler beim Schreiben des Bootloaders.') + vbCr + M09.Get_Language_Str('Die Meldungen von avrdude stehen im Fenster des Arduino-Monitors.'), vbCritical, M09.Get_Language_Str('Bootloader nicht geschrieben'))  # v1.02
        return False  # v1.02
    return True  # v1.02


def Install_FastBootloader_PIO():  # v1.02
    # PlatformIO: Hinweis zu den Jumpern, ArduinoISP als fertige .hex auf den rechten Arduino, Bootloader auf den linken Arduino schreiben (so oft, wie gewuenscht),
    # danach wieder das DCC/LNet/Selectrix-Programm auf den rechten Arduino. Ablauf wie im Excel-Programm (Install_FastBootloader).
    if P01.MsgBox(__Jumper_Text(), vbOKCancel + vbInformation, M09.Get_Language_Str('Installieren des schnellen Bootloaders')) != vbOK:  # v1.02
        return  # v1.02
    if not __Install_ArduinoISP_hex_to_Right_Arduino():  # v1.02
        return  # v1.02
    State = {'FlashAs328P': None}  # v1.02
    while 1:  # v1.02
        if Write_Bootloader_PIO(State):  # v1.02
            Again = P01.MsgBox(M09.Get_Language_Str('Installation des Bootloaders abgeschlossen') + vbCr + vbCr + M09.Get_Language_Str('Soll der Bootloader auf einen weiteren Arduino geladen werden?') + vbCr + vbCr + M09.Get_Language_Str('Wenn ja, dann muss dieser jetzt in den linken Steckplatz gesteckt werden.') + vbCr + M09.Get_Language_Str('Mit \'Nein\' wird wieder das DCC/LNet/Selectrix Programm auf den rechten Nano installiert.') + vbCr + vbCr + M09.Get_Language_Str('Achtung der rechte Arduino darf nicht entfernt werden!'), vbYesNo + vbDefaultButton2, M09.Get_Language_Str('Noch einen Arduino aktualisieren?')) == vbYes  # v1.02
        else:  # v1.02
            Again = P01.MsgBox(M09.Get_Language_Str('Soll es noch einmal versucht werden?') + vbCr + M09.Get_Language_Str('Wenn ja, jetzt den linken Arduino prüfen (Jumper, Steckplatz).'), vbYesNo + vbQuestion, M09.Get_Language_Str('Bootloader nicht geschrieben')) == vbYes  # v1.02
        if not Again:  # v1.02
            break  # v1.02
    M08.Compile_and_Upload_Prog_to_Right_Arduino(True)                  # wieder das DCC/LNet/Selectrix-Programm auf den rechten Arduino (dort liegt noch der ArduinoISP)  # v1.02
    P01.MsgBox(M09.Get_Language_Str('Achtung: Die Jumper müssen unbedingt wieder entfernt werden sonst geht nichts mehr ;-(' + vbCr + 'Damit sie nicht verloren gehen können sie so eingesteckt werden, dass sie nur auf einem Pin stecken.' + vbCr + vbCr + 'Das USB Kabel sollte wieder auf den linken Arduino gesteckt werden.'), vbInformation, M09.Get_Language_Str('Bootloader Programmierung abgeschlossen'))  # v1.02


def Install_FastBootloader():
    Res = Boolean()
    #----------------------------------
    M25.Make_sure_that_Col_Variables_match()
    if M25.Page_ID != 'DCC' and M25.Page_ID != 'Selectrix'  and M25.Page_ID != 'LNet':
        P01.MsgBox(M09.Get_Language_Str('Die schnelle Bootloader kann nur von einer DCC, LNet oder Selectrix Seite aus installiert werden.'), vbInformation, M09.Get_Language_Str('Falsche Seite zum aktualisieren des Bootloaders ausgewählt'))
        return
    # if M02.Get_BoardTyp() != M02.HT_AM328:  # v1.01 (entfallen)
    if M02a.Get_BoardTyp() != M02.HT_AM328:  # v1.01
        # 08.12.23: Juergen
        P01.MsgBox(M09.Get_Language_Str('Der schnelle Bootloader kann nur für Arduino installiert werden.'), vbInformation, M09.Get_Language_Str('Falsche Plattform zum Aktualisieren des Bootloaders ausgewählt'))
        return  # v1.02
    if M28.Is_PlatformIO():                                                                # PlatformIO: ArduinoISP als fertige .hex hochladen, den Bootloader mit dem avrdude von PlatformIO schreiben  # v1.02
        Install_FastBootloader_PIO()  # v1.02
        return
    # Der schnelle Bootloader ist in der Webversion noch nicht umgesetzt: BootJumper_Form (Dialog fuer die Jumper) ist nur ein Geruest ohne Oberflaeche, das Schreiben
    # mit avrdude und ArduinoISP laeuft ueber eine Windows-Stapeldatei. Bis dahin eine Meldung statt eines Absturzes (siehe HOC 2.49).
    P01.MsgBox(M09.Get_Language_Str('Der schnelle Bootloader lässt sich in der Webversion noch nicht installieren (der Dialog für die Jumper und das Schreiben mit avrdude sind noch nicht übernommen). Bitte dafür das Excel-Programm benutzen.'), vbInformation, M09.Get_Language_Str('Schneller Bootloader'))  # v1.01
    return  # v1.01
    Res = BootJumper_Form.ShowDialog
    time.sleep(1000)
    if Res:
        if not __Install_ArduinoISP_to_Right_Arduino():
            return
        while 1:
            Write_Bootloader( BootJumper_Form.FlashAs328P )
            # 09.12.23: Juergen
            if not (P01.MsgBox(M09.Get_Language_Str('Installation des Bootloaders abgeschlossen' + vbCr + vbCr + 'Soll der Bootloader auf einen weiteren Arduino geladen werden?' + vbCr + vbCr + 'Wenn ja, dann muss dieser jetzt in den linken Steckplatz gesteckt werden.' + vbCr + 'Mit \'Nein\' wird wieder das DCC/LNet/Selectrix Programm auf den rechten Nano installiert.' + vbCr + vbCr + 'Achtung der rechte Arduino darf nicht entfernt werden!'), vbYesNo + vbDefaultButton2, M09.Get_Language_Str('Noch einen Arduino aktualisieren?')) == vbYes):
                break
        M08.Compile_and_Upload_Prog_to_Right_Arduino(( True ))
        # 09.12.23: Juergen improved bootloader update
        P01.MsgBox(M09.Get_Language_Str('Achtung: Die Jumper müssen unbedingt wieder entfernt werden sonst geht nichts mehr ;-(' + vbCr + 'Damit sie nicht verloren gehen können sie so eingesteckt werden, dass sie nur auf einem Pin stecken.' + vbCr + vbCr + 'Das USB Kabel sollte wieder auf den linken Arduino gesteckt werden.'), vbInformation, M09.Get_Language_Str('Bootloader Programmierung abgeschlossen'))

# VB2PY (UntranslatedCode) Option Explicit
