# Datei-Version: 1.01 (2026-10-21) - clsExtension.py
# ----------------------------------------------------------------------------------------------
# Name:           clsExtension.py
# Path:           proggen/clsExtension.py
# Version:        1.01
# Last Update:    2026-10-21
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-12  Stand der Umstellung (nicht erfasst)
#   1.01  2026-10-21  MinimumMobaLedLibVersion (Extensions-Schnittstelle V2); CheckValid prueft self.Name mit M02.PAT_ExtensionName (vorher globale Variable und nicht importiertes Matches); Version K des Excel-Programms
# ----------------------------------------------------------------------------------------------
from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" the name of the extension must contain only basic letters (A-Z or a-z) and numbers (0-9), underscores (_)and dashes (-).
 They must start with a letter or number. They must contain at least one letter.

-----------------------------------------------------------
return an error message in case of check fails, otherwise empty string
-----------------------------------------------------------
-----------------------------------------------------------
return an error message in case of check fails, otherwise empty string
-----------------------------------------------------------
"""

Platforms = Collection()
Id = Integer()
Name = String()
path = String()
Includes = String()
MacroIncludes = String()
Constructors = Collection()
Macros = Collection()
Parameters = Collection()
NamePattern = '^[A-Za-z0-9][A-Za-z0-9_\\-]*$'


class clsExtension:
    
    def __init__(self):
        self.Platforms = ""
        self.Name = ""
        self.path = ""
        self.Includes = ""
        self.MacroIncludes = ""
        self.Constructors = []
        self.Macros = []
        self.Parameters = []
        self.Id = ""    
        self.MinimumMobaLedLibVersion = ""                  # Version K: Extensions-Schnittstelle V2 ab MobaLedLib 3.5.0  # v1.01

    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: TypeName - ByVal 
    def GetConstructor(self, TypeName):
        _fn_return_value = False
        Constructor = Variant()
        for Constructor in self.Constructors:
            if Constructor.TypeName == TypeName:
                _fn_return_value = Constructor
                return _fn_return_value
        _fn_return_value = None
        return _fn_return_value
    
    def CheckValid(self):
        _fn_return_value = False
        # if not Matches(Name, NamePattern):  # v1.01 (entfallen)
        import re  # v1.01
        import proggen.M02_Public as M02  # v1.01
        if not re.match(M02.PAT_ExtensionName, str(self.Name)):                    # Version K: Muster PAT_ExtensionName (vorher: globale Variable Name und fehlendes Matches)  # v1.01
            _fn_return_value = 'Extension Name is invalid'
            return _fn_return_value
        _fn_return_value = ''
        return _fn_return_value
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Argument - ByVal 
    def IsExtensionParameter(self, Argument):
        _fn_return_value = False
        Parameter = Variant()
        for Parameter in self.Parameters:
            if Parameter.Name == Argument:
                _fn_return_value = True
                return _fn_return_value
        return _fn_return_value
    
    # VB2PY (UntranslatedCode) Option Explicit
