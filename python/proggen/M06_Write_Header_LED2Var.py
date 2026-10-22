# Datei-Version: 1.01 (2026-10-21) - M06_Write_Header_LED2Var.py
# ----------------------------------------------------------------------------------------------
# Name:           M06_Write_Header_LED2Var.py
# Path:           proggen/M06_Write_Header_LED2Var.py
# Version:        1.01
# Last Update:    2026-10-21
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-12  Stand der Umstellung (nicht erfasst)
#   1.01  2026-10-21  Neu: Add_LED_Name_Entry (Makros Name_LED_Number und Name_LED_Offset), LED_Names_Tab (Version K des Excel-Programms)
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
# 2021-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

# fromx proggen.M02_Public import *
# fromx proggen.M06_Write_Header_LED2Var import *
# fromx proggen.M06_Write_Header_Sound import *
# fromx proggen.M06_Write_Header_SW import *
# fromx proggen.M08_ARDUINO import *
# fromx proggen.M09_Language import *
# fromx proggen.M09_Select_Macro import *
# fromx proggen.M20_PageEvents_a_Functions import *
# fromx proggen.M25_Columns import *
# fromx proggen.M28_Diverse import *
# fromx proggen.M30_Tools import *
# fromx proggen.M80_Create_Multiplexer import *

# fromx ExcelAPI.X02_Workbook import *

import proggen.M02_Public as M02
import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M06_Write_Header as M06
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
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Multiplexer as M80

import ExcelAPI.XLA_Application as P01

""" Header file generation for the LED_to_Var function
"""

LED2Var_Tab = String()
LED_Names_Tab = String()                                    # Version K  # v1.01

def Init_HeaderFile_Generation_LED2Var(firstSheet):
    # global LED2Var_Tab  # v1.01 (entfallen)
    global LED2Var_Tab, LED_Names_Tab  # v1.01
    _fn_return_value = None
    #--------------------------------------------------------------
    if firstSheet:
        LED2Var_Tab = ''
        LED_Names_Tab = ''                                          # Version K  # v1.01
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cmd - ByRef 
def Add_LED2Var_Entry(Cmd, LEDNr):
    global LED2Var_Tab
    _fn_return_value = False
    Parts = vbObjectInitialize(objtype=String)

    Typ = String()

    Offset = Integer()
    #-------------------------------------------------------------------------------
    Parts = Split(Replace(Replace(Replace(Trim(Cmd), M02.SF_LED_TO_VAR, ''), ')', ''), ' ', ''), ',')
    select_0 = Trim(Parts(2))
    if (select_0 == '='):
        Typ = 'T_EQUAL_THEN'
    elif (select_0 == '!='):
        Typ = 'T_NOT_EQUAL_THEN'
    elif (select_0 == '<'):
        Typ = 'T_LESS_THEN'
    elif (select_0 == '>'):
        Typ = 'T_GREATER_THAN'
    elif (select_0 == '&'):
        Typ = 'T_BIN_MASK'
    elif (select_0 == '!&'):
        Typ = 'T_NOT_BIN_MASK'
    else:
        P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Falscher Typ \'#1#\' in der \'LED_to_Var\' Funktion'), "#1#", Parts(2)), vbCritical, M09.Get_Language_Str('Fehler: Falscher Typ in \'LED_to_Var\' Funktion'))
        return _fn_return_value
    Offset = P01.val(Parts(1))
    LED2Var_Tab = LED2Var_Tab + '        { ' + M30.AddSpaceToLen(M06.ExpandName(Parts(0)) + ',', 20) + M30.AddSpaceToLen(str(LEDNr + Offset // 3) + ',', 7) + M30.AddSpaceToLen('(' + str(Offset % 3), 5) + '<< 3) | ' + M30.AddSpaceToLen(Typ + ', ', 19) + M30.AddSpaceToLen(Parts(3), 4) + '},' + vbCrLf    
    #__LED2Var_Tab = __LED2Var_Tab + '        { ' + M30.AddSpaceToLen(Parts(0) + ',', 20) + M30.AddSpaceToLen(LEDNr + Offset // 3 + ',', 7) + M30.AddSpaceToLen('(' + Offset % 3, 5) + '<< 3) | ' + M30.AddSpaceToLen(Typ + ', ', 19) + M30.AddSpaceToLen(Parts(3), 4) + '},' + vbCr
    Cmd = '// ' + Cmd
    _fn_return_value = True
    return _fn_return_value, Cmd

def Add_LED_Name_Entry(Row, Cmd, LEDNr, key):  # v1.01
    # Version K: Name_LED_Number(Name[, Anzahl]) und Name_LED_Offset(Name[, Anzahl]) werden zu "#define Name <LED-Nummer>" (bei Anzahl > 1 eine Folge Name0, Name1, ...)
    #-------------------------------------------------------------------------------
    parts = Split(Replace(Replace(Replace(Trim(Cmd), key + '(', ''), ')', ''), ' ', ''), ',')  # v1.01
    if UBound(parts) == 1:  # v1.01
        NumOfLeds = int(P01.val(parts(1)))  # v1.01
    else:  # v1.01
        NumOfLeds = 1  # v1.01
    if UBound(parts) == 0 or NumOfLeds == 1:  # v1.01
        Cmd = '#define ' + parts(0) + ' ' + str(LEDNr)  # v1.01
    elif UBound(parts) == 1:  # v1.01
        StartNr, TxtLen = M06SW.Check_Nr_From_Var(Row, parts(0), 0, 'VarLed')  # v1.01
        if StartNr < 0:  # v1.01
            return False, Cmd  # v1.01
        Cmd = ''  # v1.01
        for i in vbForRange(1, NumOfLeds):  # v1.01
            TargetVariable = Left(parts(0), TxtLen) + str(StartNr + i - 1)  # v1.01
            if Cmd != '':  # v1.01
                Cmd = Cmd + vbCrLf  # v1.01
            Cmd = Cmd + '#define ' + TargetVariable + ' ' + str(LEDNr + i - 1)  # v1.01
    else:  # v1.01
        # TODO error
        return False, Cmd  # v1.01
    return True, Cmd  # v1.01

def Write_Header_File_LED2Var(fp):
    global LED2Var_Tab
    
    _fn_return_value = None
    #------------------------------------------------------------------
    if LED2Var_Tab != '':
        VBFiles.writeText(fp, '// ----- LED to Var -----', '\n')
        VBFiles.writeText(fp, '  #define USE_LED_TO_VAR', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '  #define T_EQUAL_THEN     0', '\n')
        VBFiles.writeText(fp, '  #define T_NOT_EQUAL_THEN 1', '\n')
        VBFiles.writeText(fp, '  #define T_LESS_THEN      2', '\n')
        VBFiles.writeText(fp, '  #define T_GREATER_THAN   3', '\n')
        VBFiles.writeText(fp, '  #define T_BIN_MASK       4', '\n')
        VBFiles.writeText(fp, '  #define T_NOT_BIN_MASK   5', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '  typedef struct', '\n')
        VBFiles.writeText(fp, '      {', '\n')
        VBFiles.writeText(fp, '      uint8_t  Var_Nr;', '\n')
        VBFiles.writeText(fp, '#ifdef LONG_LED_ADDR', '\n')
        VBFiles.writeText(fp, '      uint16_t  LED_Nr;', '\n')
        VBFiles.writeText(fp, '#else', '\n')
        VBFiles.writeText(fp, '      uint8_t  LED_Nr;', '\n')
        VBFiles.writeText(fp, '#endif', '\n')
        VBFiles.writeText(fp, '      uint8_t  Offset_and_Typ; // ---oottt    Offset: 0..2', '\n')
        VBFiles.writeText(fp, '      uint8_t  Val;', '\n')
        VBFiles.writeText(fp, '      } __attribute__ ((packed)) LED2Var_Tab_T;', '\n')
        # 05.11.20: Added: __attribute__ ((packed)) to be able to use it on oa 32 Bit platform
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#ifdef CONFIG_ONLY', '\n')
        # 17.04.22 Juergen: add Simulator Led2Var feature
        VBFiles.writeText(fp, '  const LED2Var_Tab_T LED2Var_Tab[] __attribute__ ((section (".MLLL2VConfig"))) =', '\n')
        VBFiles.writeText(fp, '#else', '\n')
        VBFiles.writeText(fp, '  const PROGMEM LED2Var_Tab_T LED2Var_Tab[] =', '\n')
        VBFiles.writeText(fp, '#endif', '\n')
        VBFiles.writeText(fp, '      {', '\n')
        VBFiles.writeText(fp, '        // Var name           LED_Nr LED Offset   Typ                Compare value', '\n')
        VBFiles.writeText(fp, M30.DelLast(LED2Var_Tab,2), '\n')
        VBFiles.writeText(fp, '      };', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
