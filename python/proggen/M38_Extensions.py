# Datei-Version: 1.01 (2026-10-21) - M38_Extensions.py
# ----------------------------------------------------------------------------------------------
# Name:           M38_Extensions.py
# Path:           proggen/M38_Extensions.py
# Version:        1.01
# Last Update:    2026-10-21
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-12  Stand der Umstellung (nicht erfasst)
#   1.01  2026-10-21  Extensions-Schnittstelle V2: MinimumMobaLedLibVersion aus der JSON-Datei, #define USE_EXTENSIONS_V2 ab Mindestversion 3.5.0 (Version K des Excel-Programms)
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


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

import proggen.M02_Public as M02
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
import proggen.M33_WebApi as M33
import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Multiplexer as M80
import proggen.clsExtension as clsext

import mlpyproggen.Prog_Generator as PG

import ExcelAPI.XLA_Application as P01

from ExcelAPI.XLC_Excel_Consts import *

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

# ******************************
# *                            *
# *       M38_Extensions       *
# *                            *
# ******************************

Extensions = []
ExtensionKey = 'EX.'
__ExtensionsActive = {}
__ExtensionLines = {}
JSONData = {} 


class clsExtensionConstructor:
    
    def __init__(self):
        self.Arguments = []
        self.TypeName = ""
        self.LEDs = ""
        self.InCnt = 0
        self.OutCnt = 0
        self.Texts = {}
        

class clsExtensionParameter:
    def __init__(self):
        self.Name = ""
        self.TypeName = ""
        self.Min = 0
        self.Max = 0
        self.Default = 0
        self.Texts = {}
    
class clsExtensionMacro:
    def __init__(self):
        self.Name = ""
        self.Typ = "" # pyMLL specific
        self.Group = "" # pyMLL specific
        self.MacroString = "" # pyMLL specific
        self.Arguments = []
        self.TypeName = ""
        self.LEDs = ""
        self.InCnt = 0
        self.OutCnt = 0
        self.Texts = {}


def Load_Extensions():
    global Extensions
    
    OldEvents = Variant()

    ParamSheet = Variant()

    MacroSheet = Variant()

    Extension = clsext.clsExtension()

    Macro = clsExtensionMacro()

    Parameter = clsExtensionParameter()

    Constructor = clsExtensionConstructor()

    Argument = Variant()

    MacroRow = Integer()

    ParamRow = Integer()

    MacroStr = String()
    __CollectExtensions()
    RemoveExistingExtensions()
    OldEvents = P01.Application.EnableEvents
    P01.Application.EnableEvents = False
    ParamSheet = PG.ThisWorkbook.Sheets(M02.PAR_DESCR_SH)
    MacroSheet = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
    MacroRow = M30.LastUsedRowIn(MacroSheet) + 1
    ParamRow = M30.LastUsedRowIn(ParamSheet) + 1
    for Extension in Extensions:
        for Constructor in Extension.Constructors:
            # TODO translate
            MacroStr = ''
            for Argument in Constructor.Arguments:
                if MacroStr != '':
                    MacroStr = MacroStr + ', '
                # fully qualify the argument name if argument is defined withon the plugin
                if Extension.IsExtensionParameter(Argument):
                    MacroStr = MacroStr + ExtensionKey + Extension.Name + '.'
                MacroStr = MacroStr + Argument
            MacroStr = ExtensionKey + Constructor.TypeName + '(' + MacroStr + ')'
            MacroSheet.CellDict[MacroRow, M02.SM_Typ___COL] = 'EX.Constructor'
            MacroSheet.CellDict[MacroRow, M02.SM_Pic_N_COL] = 'Puzzle | IDE'
            MacroSheet.CellDict[MacroRow, M02.SM_LEDS__COL] = Constructor.LEDs
            MacroSheet.CellDict[MacroRow, M02.SM_InCnt_COL] = Constructor.InCnt
            MacroSheet.CellDict[MacroRow, M02.SM_OutCntCOL] = Constructor.OutCnt
            MacroSheet.CellDict[MacroRow, M02.SM_Macro_COL] = MacroStr
            MacroSheet.CellDict[MacroRow, M02.SM_FindN_COL] = ExtensionKey + Constructor.TypeName + '('
            MacroSheet.CellDict[MacroRow, M02.SM_Name__COL] = ExtensionKey + Constructor.TypeName
            MacroSheet.CellDict[MacroRow, M02.SM_Group_COL] = 'Erweiterungen'
            MacroSheet.CellDict[MacroRow, M02.SM_LName_COL] = Constructor.Texts.get('DisplayName')
            MacroSheet.CellDict[MacroRow, M02.SM_ShrtD_COL] = Constructor.Texts.get('ShortDescription')
            MacroSheet.CellDict[MacroRow, M02.SM_DetailCOL] = Constructor.Texts.get('DetailedDescription')
            MacroRow = MacroRow + 1
        for Parameter in Extension.Parameters:
            parname = 'EX.' + Extension.Name + '.' + Parameter.Name
            ParamSheet.CellDict[ParamRow, M10.ParName_COL] = parname
            ParamSheet.CellDict[ParamRow, M10.ParType_COL] = Parameter.TypeName
            ParamSheet.CellDict[ParamRow, M10.Par_Min_COL] = Parameter.Min
            ParamSheet.CellDict[ParamRow, M10.Par_Max_COL] = Parameter.Max
            ParamSheet.CellDict[ParamRow, M10.Par_Def_COL] = Parameter.Default
            ParamSheet.CellDict[ParamRow, M10.Par_Opt_COL] = Parameter.Options
            ParamSheet.CellDict[ParamRow, M10.ParInTx_COL] = Parameter.Texts.get('DisplayName')
            ParamSheet.CellDict[ParamRow, M10.ParHint_COL] = Parameter.Texts.get('ShortDescription')
            ParamRow = ParamRow + 1
        for Macro in Extension.Macros:
            # TODO translate
            if Macro.MacroString == "":  # pyMLL specific
                MacroStr = ''
                for Argument in Macro.Arguments:
                    # if ".#" in Argument:
                        # Argument = "#" + Argument
                    if MacroStr != '':
                        MacroStr = MacroStr + ','
                    MacroStr = MacroStr + Argument
                if MacroStr == '':
                    MacroStr = Macro.Name
                    FindName = Macro.Name
                else:
                    MacroStr = Macro.Name + '(' + MacroStr + ')'
                    FindName = Macro.Name + "("
            else:
                MacroStr = Macro.MacroString
                FindName = Macro.Name + "("
            if Macro.Typ == "": # pyMLL specific
                Macro.Typ = 'EX.Macro.' + str(Extension.Id)
            if Macro.Group == "": # pyMLL specific
                Macro.Group = 'Erweiterungen'
        
            MacroSheet.CellDict[MacroRow, M02.SM_Typ___COL] = Macro.Typ # EX.Macro.' + str(Extension.Id)
            MacroSheet.CellDict[MacroRow, M02.SM_Pic_N_COL] = 'Puzzle | IDE'
            MacroSheet.CellDict[MacroRow, M02.SM_LEDS__COL] = Macro.LEDs
            MacroSheet.CellDict[MacroRow, M02.SM_InCnt_COL] = Macro.InCnt
            MacroSheet.CellDict[MacroRow, M02.SM_OutCntCOL] = Macro.OutCnt
            MacroSheet.CellDict[MacroRow, M02.SM_Macro_COL] = MacroStr
            MacroSheet.CellDict[MacroRow, M02.SM_FindN_COL] = FindName
            
            MacroSheet.CellDict[MacroRow, M02.SM_Name__COL] = Macro.Name
            MacroSheet.CellDict[MacroRow, M02.SM_Group_COL] = Macro.Group
            MacroSheet.CellDict[MacroRow, M02.SM_LName_COL] = Macro.Texts.get('DisplayName')
            MacroSheet.CellDict[MacroRow, M02.SM_ShrtD_COL] = Macro.Texts.get('ShortDescription')
            MacroSheet.CellDict[MacroRow, M02.SM_DetailCOL] = Macro.Texts.get('DetailedDescription')
            MacroRow = MacroRow + 1
    P01.Application.EnableEvents = OldEvents
    
def ConvertFastbuild():
    # 04.11.23: Juergen:
    return #*HL
    ConvertToCrLf(M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED + 'fastbuild.cmd')
    ConvertToCrLf(M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED + 'fastbuild2.cmd') # 23.01.25: Juergen:

def ConvertToCrLf(fileName):
    fso = Variant()

    objTextFile = Variant()

    content = String()

    newContent = String()
    # 04.11.23: Juergen:
    fso = CreateObject('Scripting.FileSystemObject')
    objTextFile = fso.OpenTextFile(fileName, 1)
    content = objTextFile.ReadAll
    objTextFile.Close()
    newContent = Replace(content, vbLf, vbCrLf)
    newContent = Replace(newContent, vbCr + vbCr, vbCr)
    if newContent != content:
        objTextFile = fso.OpenTextFile(fileName, 2)
        objTextFile.Write(newContent)
        objTextFile.Close()

def __CollectExtensions():
    global Extensions
    #return #*HL
    
    oFSO = Variant()

    DirName = Variant()

    Id = Integer()

    Libs = Collection()
    Extensions = []
    #oFSO = CreateObject('Scripting.FileSystemObject')
    if not M37.CheckArduinoHomeDir():
        return
    Libs = Collection()
    
    DirName = Dir(M02.Sketchbook_Path + '/libraries/*', vbDirectory)
    while DirName != '':
        if DirName != '.' and DirName != '..':
            if os.path.isdir(M02.Sketchbook_Path + '/libraries/' + DirName):
                if os.path.isfile(M02.Sketchbook_Path + '/libraries/' + DirName + '/MobaLedLib.properties'):
                        Libs.Add(M02.Sketchbook_Path + '/libraries/' + DirName + '/MobaLedLib.properties')
        DirName = Dir()
                    
    # workbookpath =  M08.GetWorkbookPath()
    # DirName = Dir(workbookpath + '/libraries/*', vbDirectory)
    # while DirName != '':
        # if DirName != '.' and DirName != '..':
            # if os.path.isdir(workbookpath + '/libraries/' + DirName):
                # if os.path.isfile(M02.Sketchbook_Path + '/libraries/' + DirName + '/MobaLedLib.properties'):
                    # Libs.Add(workbookpath + '/libraries/' + DirName + '/MobaLedLib.properties')
        # DirName = Dir()

    Id = 1
    for DirName in Libs:
        try:
            Message = ""
            LibName = DirName
            JSONData = {}
            # VB2PY (UntranslatedCode) On Error Resume Next
            JSONData = M33.ParseJSONFile(LibName)
            # VB2PY (UntranslatedCode) On Error GoTo 0
            if JSONData != {}:
                Extension = clsext.clsExtension()
                Extension.Platforms = JSONData.get('platforms', [])
                Extension.Name = JSONData.get('id')
                Extension.Path = Replace(LibName, '/MobaLedLib.properties', '')
                Extension.Includes = JSONData.get('includes')
                Extension.MacroIncludes = JSONData.get('macroIncludes')
                Extension.MinimumMobaLedLibVersion = JSONData.get('minimumMobaLedLibVersion', '')                # Version K: Extensions-Schnittstelle V2  # v1.01
                typeslist = JSONData.get("types", [])
                #for Index in __ToIndexList('obj.types(#).TypeName'):
                for Index in range(0, len(typeslist)):
                    ctr = clsExtensionConstructor()
                    typedata = typeslist[Index]
                    ctr.TypeName = typedata.get('TypeName')
                    ctr.LEDs = typedata.get('LEDs')
                    ctr.InCnt = typedata.get('InCount')
                    ctr.OutCnt = typedata.get('OutCnt')
                    ctr.Texts['DisplayName'] = typedata.get('DisplayName')
                    ctr.Texts['ShortDescription'] = typedata.get('ShortDescription')
                    ctr.Texts['DetailedDescription'] = typedata.get('DetailedDescription')
                    ctr.Arguments = typedata.get('Arguments', [])  # Arguments for pyMobaLedLib with "#"-support
                    Extension.Constructors.append(ctr)
                macroslist = JSONData.get("macros", [])   
                for Index in range(0, len(macroslist)):
                    mac = clsExtensionMacro()
                    macrodata = macroslist[Index]
                    mac.Name = macrodata.get('Macro', "")
                    mac.Typ = macrodata.get('Type', "") # pyMLL specific
                    mac.Group = macrodata.get('Group', "") # pyMLL specific
                    mac.LEDs = macrodata.get('LEDs')
                    mac.InCnt = macrodata.get('InCount')
                    mac.Texts['DisplayName'] = macrodata.get('DisplayName')
                    mac.Texts['ShortDescription'] = macrodata.get('ShortDescription')
                    mac.Texts['DetailedDescription'] = macrodata.get('DetailedDescription')
                    mac.Arguments = macrodata.get('Arguments')
                    Extension.Macros.append(mac)
                parlist =  JSONData.get("parameters", [])
                for Index in range(0, len(parlist)):
                    par = clsExtensionParameter()
                    pardata = parlist[Index]
                    par.Name = pardata.get('ParameterName')
                    par.TypeName = pardata.get('Type')
                    par.Min = pardata.get('Min')
                    par.Max = pardata.get('Max')
                    par.Default = pardata.get('Default')
                    par.Options = pardata.get('Options')
                    par.Texts['DisplayName'] = pardata.get('DisplayName')
                    par.Texts['ShortDescription'] = pardata.get('ShortDescription')
                    Extension.Parameters.append(par)
                if Message == '':
                    Extension.Id = Id
                    Extensions.append(Extension)
                    Id = Id + 1
            else:
                P01.MsgBox(Replace('Extension \'#1#\' load error', '#1#', DirName) + vbCrLf + Message, vbExclamation, 'MobaLedLib Extensions')
        except BaseException as ex:
            logging.debug(ex, exc_info=True) 
            Message = ex
            P01.MsgBox(Replace('Extension \'#1#\' load error', '#1#', DirName) + vbCrLf + Message, vbExclamation, 'MobaLedLib Extensions')

def __ToList(Pattern):
    fn_return_value = None
    search = String()

    cnt = Integer()
    cnt = 0
    fn_return_value = Collection()
    while 1:
        search = Replace(Pattern, '#', cnt)
        if not JSONData.Exists(search):
            break
        fn_return_value.Add(JSONData(search))
        cnt = cnt + 1
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Index - ByVal 
def __GetDataAtIndex(Pattern, Index):
    fn_return_value = None
    search = String()
    fn_return_value = ''
    search = Replace(Pattern, '#', Index)
    if not __JSONData.Exists(search):
        return fn_return_value
    fn_return_value = __JSONData(search)
    return fn_return_value

def __ToIndexList(Pattern):
    fn_return_value = None
    search = String()

    cnt = Integer()
    cnt = 0
    fn_return_value = Collection()
    while 1:
        search = Replace(Pattern, '#', cnt)
        if not __JSONData.Exists(search):
            break
        fn_return_value.Add(cnt)
        cnt = cnt + 1
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Id - ByVal 
def GetExtension(Id):
    fn_return_value = None
    Extension = Variant()
    for Extension in Extensions:
        if Extension.Id == Id:
            fn_return_value = Extension
            return fn_return_value
    fn_return_value = None
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Key - ByVal 
def GetConstructor(Key):
    fn_return_value = None
    Splits = Variant()
    Splits = Split(Key, '.')
    if UBound(Splits) == 3 and Splits(0) == 'PI' and Splits(1) == 'Constructor':
        Extension = GetExtension(Splits(2))
        if not Extension is None:
            fn_return_value = Extension.GetConstructor(Splits(3))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: TypeName - ByVal 
def GetExtensionByTypeName(TypeName):
    fn_return_value = None

    for Extension in Extensions:
        for Constructor in Extension.Constructors:
            if Constructor.TypeName == TypeName:
                fn_return_value = Extension
                return fn_return_value
    fn_return_value = None
    return fn_return_value

def IsExtensionKey(Key):
    fn_return_value = InStr(str(Key), ExtensionKey) == 1
    return fn_return_value

def Init_HeaderFile_Generation_Extension(firstSheet):
    global __ExtensionsActive, __ExtensionLines
    fn_return_value = None
    if firstSheet:
        __ExtensionsActive = {} #Scripting.Dictionary()
        __ExtensionLines = {} #Scripting.Dictionary()
        __CollectExtensions()
    fn_return_value = True
    return fn_return_value

def Add_Macro_Extension_Entry(cmd: str) -> bool:
    global __ExtensionsActive
    # Default return value
    result = False

    # Must start with "EX.Macro."
    if not cmd.startswith("EX.Macro."):
        return result

    # Extract numeric ID after prefix
    extension_id_text = cmd[9:]   # Mid(Cmd, 10) in VBA (1‑based → 0‑based)
    if not extension_id_text.isdigit():
        return result

    extension_id = int(extension_id_text)
    extension = GetExtension(extension_id)

    if extension is not None:
        # Equivalent to: If Not ExtensionsActive.Exists(Extension.Id)
        if extension.Id not in __ExtensionsActive:
            __ExtensionsActive[extension.Id] = extension

        result = True

    return result

    

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cmd - ByRef 
def Add_Extension_Entry(Cmd):
    fn_return_value = None
    p_str = String()

    #Extension = clsExtension()
    Cmd = Mid(Cmd, Len(ExtensionKey) + 1)
    p_str = Cmd
    if InStr(Cmd, '(') > 0:
        p_str = Split(p_str, '(')(0)
    Extension = GetExtensionByTypeName(p_str)
    if Extension is None:
        P01.MsgBox(Replace('Extension \'#1#\' not found', '#1#', p_str), vbCritical, 'MobaLedLib Extensions')
        fn_return_value = False
        return fn_return_value, Cmd
    if __ExtensionsActive.get(Extension.Id, -1) == -1:
        __ExtensionsActive[Extension.Id] = Extension
    __ExtensionLines[len(__ExtensionLines) + 1] = Cmd
    fn_return_value = True
    return fn_return_value, Cmd #*HL ByRef

def __GetExtensionsMinimumMobaLedLibVersion():  # v1.01
    # hoechste Mindestversion der MobaLedLib aller aktiven Extensions (Version K)
    result = '0.0.0'  # v1.01
    for Extension in __ExtensionsActive.values():  # v1.01
        if M30.VersionStr_is_GreaterEqual(Extension.MinimumMobaLedLibVersion, result):  # v1.01
            result = Extension.MinimumMobaLedLibVersion  # v1.01
    return result  # v1.01

def Write_Header_File_Extension_Before_Config(fp):
    fn_return_value = None
    #Extension = clsExtension()

    p_str = Variant()

    HeaderWritten = Boolean()
    #------------------------------------------------------------------
    # here we write include all the header files, that have definitions already needed inside the config block
    # e.g. macros
    HeaderWritten = False
    if len(__ExtensionsActive) > 0:
        if M30.VersionStr_is_GreaterEqual(__GetExtensionsMinimumMobaLedLibVersion(), '3.5.0'):                # Version K: Extensions-Schnittstelle V2  # v1.01
            VBFiles.writeText(fp, '// ----- at least one extion uses Externions API V2 -----', '\n')  # v1.01
            VBFiles.writeText(fp, '#define USE_EXTENSIONS_V2', '\n')  # v1.01
            VBFiles.writeText(fp, '', '\n')  # v1.01
        for Extension in Extensions:
            if Extension.MacroIncludes != '':
                if HeaderWritten == False:
                    VBFiles.writeText(fp, '// ----- dynamic extensions section begin -----', '\n')
                    VBFiles.writeText(fp, '#define MLL_EXTENSIONS_ACTIVE', '\n')
                    VBFiles.writeText(fp, '#include <MLLExtension.h>', '\n')
                    VBFiles.writeText(fp, '', '\n')
                    HeaderWritten = True
                VBFiles.writeText(fp, '// Extension ' + Extension.Name, '\n')
                for p_str in Split(Extension.MacroIncludes, ','):
                    VBFiles.writeText(fp, '#include <' + p_str + '>')
                VBFiles.writeText(fp, '', '\n')
        if HeaderWritten:
            VBFiles.writeText(fp, '// ----- dynamic Extensions section end -----', '\n')
    fn_return_value = True
    return fn_return_value

def Write_Header_File_Extension_After_Config(fp):
    fn_return_value = None
    Extension = Variant()

    p_str = Variant()

    Index = Integer()
    #------------------------------------------------------------------
    if len(__ExtensionsActive) > 0:
        VBFiles.writeText(fp, '// ----- dynamic extensions section begin -----', '\n')
        VBFiles.writeText(fp, '#include <MLLExtension.h>', '\n')
        VBFiles.writeText(fp, '', '\n')
        for Extension in Extensions:
            if Extension.Includes != '':
                VBFiles.writeText(fp, '// Extension ' + Extension.Name, '\n')
                for p_str in Split(Extension.Includes, ','):
                    VBFiles.writeText(fp, '#include <' + p_str + '>')
                    VBFiles.writeText(fp, '', '\n')
            VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        if len(__ExtensionLines) > 0:
            VBFiles.writeText(fp, '// ----- dynamic extensions section begin -----', '\n')
            VBFiles.writeText(fp, 'MLLExtension* mllExtensions[] = {', '\n')
            for Index in vbForRange(1, len(__ExtensionLines)):
                if Index == len(__ExtensionLines):
                    VBFiles.writeText(fp, '  new ' + __ExtensionLines.get(Index), '\n')
                else:
                    VBFiles.writeText(fp, '  new ' + __ExtensionLines.get(Index) + ',', '\n')
            VBFiles.writeText(fp, '} ;', '\n')
            VBFiles.writeText(fp, '#define MLL_EXTENSIONS_COUNT ' + str(len(__ExtensionLines)), '\n')
            VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '// ----- dynamic Extensions section end -----', '\n')
        VBFiles.writeText(fp, '', '\n')
    fn_return_value = True
    return fn_return_value

def Write_PIO_Extension(fp):
    fn_return_value = False

    #for Index in vbForRange(0, len(__ExtensionsActive) - 1
    for Index in __ExtensionsActive.keys():
        VBFiles.writeText(fp, '    ' + __ExtensionsActive[Index].Name + '=file://' + M08.GetShortPath(__ExtensionsActive[Index].Path), '\n')
    fn_return_value = True
    return fn_return_value

def ExtensionsActiveCount():
    return len(__ExtensionsActive)

def RemoveExistingExtensions():

    MacroSheet = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
    ParamSheet = PG.ThisWorkbook.Sheets(M02.PAR_DESCR_SH)
    
    
    for r in vbForRange(1, M30.LastUsedRowIn(ParamSheet)):
        if IsExtensionKey(ParamSheet.Cells(r, M10.ParName_COL)):
            ParamSheet.Rows(r).EntireRow.Delete()
            # r = r - 1
            # raise() #*HL diese For Schleifen funktionieren nicht, da die Schleifenvariable in der Schleife reduziert wird!!
    for r in vbForRange(M02.SM_DIALOGDATA_ROW1, M30.LastUsedRowIn(MacroSheet)):
        if IsExtensionKey(MacroSheet.Cells(r, M02.SM_Typ___COL)):
            MacroSheet.Rows(r).EntireRow.Delete()
            # r = r - 1
            # raise() #*HL diese For Schleifen funktionieren nicht, da die Schleifenvariable in der Schleife reduziert wird!!



