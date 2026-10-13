# Datei-Version: 1.02 (2026-10-12) - headless_app_controller.py
"""HeadlessAppController: Tk-freier Ersatz fuer pyMobaLedLibapp (Startprogramm).

Uebernimmt aus pyMobaLedLibapp nur, was die Excel-Schicht und der Programmgenerator
brauchen: Konfiguration (ConfigData/ParamData/MacroDef), Fonts, Versionen, Statusmeldungen.
Logik von readConfigData()/getConfigData()/setConfigData() ist 1:1 uebernommen, damit
beide Programme dieselben Konfigurationsdateien lesen.

Nicht enthalten (noch): serielle Verbindung zum Arduino, Menues, Notebook, Tooltips.
Fehlende Attribute fuehren absichtlich zu einem AttributeError, damit klar wird, was noch
gebraucht wird.

Benutzung (aus dem Projektordner, MLL_HEADLESS=1 gesetzt):

    from headless_app_controller import HeadlessAppController
    ctrl = HeadlessAppController(mainfile_dir=os.path.dirname(os.path.abspath("pyMobaLedLib.py")))
    ctrl.create_excel_application()
"""
from __future__ import annotations

import logging

from web_serial import SerialMixin
import os
import sys

from headless_controller import HeadlessController

logger = logging.getLogger(__name__)

SCALE_FACTOR = 1   # wie ScaleFactor in pyMobaLedLib.py


class HeadlessAppController(SerialMixin, HeadlessController):
    def __init__(self, mainfile_dir: str, command_line_args: dict | None = None):
        # Imports hier, damit der Fehler klar auf das Projekt zeigt, falls der Pfad nicht stimmt
        from mlpyproggen.configfile import ConfigFile
        from mlpyproggen import DefaultConstants as DC

        self._ConfigFile = ConfigFile
        self._DC = DC
        super().__init__(prog_version=DC.PROG_VERSION, data_version=DC.DATA_VERSION,
                         prog_gen_min_data_version=DC.ProgGen_Min_Data_Version,
                         patt_gen_min_data_version=DC.Pattgen_Min_Data_Version)

        self.mainfile_dir = mainfile_dir
        self.command_line_args = command_line_args or {}
        self.useARDUINO_IDE = self.command_line_args.get("useARDUINO_IDE", False)
        self.UseConfig = self.command_line_args.get("UseConfig", False)
        self.executetests = self.command_line_args.get("test", "") == "True"
        self.colortest_only = False
        self.showspecialfeatures = self.command_line_args.get("special", "") == "True"
        self.loaddatafile = self.command_line_args.get("loaddatafile", "False") != "False"
        self.activeworkbook = None
        self.buttonlist = []
        self._serial_init()                  # arduino, queue, Sende-/Empfangsthreads (web_serial.SerialMixin)
        self.currentTabClass = ""

        self.readConfigData()
        self._init_from_config()

    # ------------------------------------------------------------------ Uebergang: Tk-Wurzel
    def attach_tk_root(self, root):
        """Uebergangsloesung: Die Python-UserForms (Userform_*.py) benutzen den Controller als
        Tk-Elternfenster (tk.StringVar(self.controller), tk.Toplevel(self.controller)). Alle hier
        nicht vorhandenen Attribute werden deshalb an die unsichtbare Tk-Wurzel weitergereicht.
        Entfaellt, sobald die Formulare durch Web-Dialoge ersetzt sind."""
        self.__dict__["_tk_root"] = root

    def __str__(self):
        # Tk uebergibt Widgets als Pfadnamen (z. B. top.transient(controller)); fuer die Wurzel ist das "."
        root = self.__dict__.get("_tk_root")
        return str(root) if root is not None else object.__str__(self)

    def __getattr__(self, name):
        root = self.__dict__.get("_tk_root")
        if root is not None and not name.startswith("__"):
            return getattr(root, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    # ------------------------------------------------------------------ Konfiguration (wie Original)
    def readConfigData(self):
        DC, ConfigFile = self._DC, self._ConfigFile
        filedir = self.mainfile_dir
        self.ParamData = ConfigFile(DC.DEFAULT_PARAM, DC.PARAM_FILENAME, filedir=filedir)
        self.ConfigData = ConfigFile(DC.DEFAULT_CONFIG, DC.CONFIG_FILENAME, filedir=filedir)
        self.ConfigData.data.update(self.command_line_args)
        if hasattr(sys, "_MEIPASS"):                      # PyInstaller-Bundle
            filedir = sys._MEIPASS
        try:
            self.MacroDef = ConfigFile({}, DC.MACRODEF_FILENAME, filedir=filedir)
            self.MacroParamDef = ConfigFile({}, DC.MACROPARAMDEF_FILENAME, filedir=filedir)
        except BaseException as e:                       # wie im Original: nur loggen
            logger.debug("MacroDef konnte nicht gelesen werden", exc_info=True)
            raise

    def getConfigData(self, key, default=None):
        DC = self._DC
        newkey = DC.CONFIG2PARAMKEYS.get(key, key)
        value = self.ParamData.data.get(newkey, self.ConfigData.data.get(key, DC.DEFAULT_CONFIG.get(key, "")))
        if key == "startcmd_filename" and not (value and os.path.isfile(str(value))):
            found = self.find_arduino_ide()                   # Linux/Mac: IDE selbst finden, wenn kein gueltiger Pfad eingetragen ist
            if found:
                return found
        return value

    _arduino_ide_cache = None

    def find_arduino_ide(self) -> str:
        """Pfad der ARDUINO IDE ausserhalb von Windows. Reihenfolge: Umgebungsvariable MLL_ARDUINO_EXE, /opt/arduino*/arduino,
        ~/arduino*/arduino, `arduino` im Suchpfad. Unter Windows sucht das Programm selbst (M08_ARDUINO.Find_ArduinoExe)."""
        import glob
        import platform
        import shutil
        if platform.system() == "Windows":
            return ""
        if self._arduino_ide_cache is not None:
            return self._arduino_ide_cache
        candidates = [os.environ.get("MLL_ARDUINO_EXE", "")]
        if platform.system() == "Darwin":                           # macOS: Programm der IDE 1.8 im Ordner Programme
            candidates += ["/Applications/Arduino.app/Contents/MacOS/Arduino",
                           os.path.expanduser("~/Applications/Arduino.app/Contents/MacOS/Arduino")]
        for pattern in ("/opt/arduino-1.8*/arduino", "/opt/arduino*/arduino", "/usr/local/arduino*/arduino",
                        os.path.expanduser("~/arduino-1.8*/arduino"), os.path.expanduser("~/arduino*/arduino")):
            candidates += sorted(glob.glob(pattern), reverse=True)
        candidates.append(shutil.which("arduino") or "")
        self._arduino_ide_cache = next((x for x in candidates if x and os.path.isfile(x)), "")
        if self._arduino_ide_cache:
            logger.info("ARDUINO IDE gefunden: %s", self._arduino_ide_cache)
        return self._arduino_ide_cache

    def setConfigData(self, key, value):
        self.ConfigData.data[key] = value

    def setConfigDataDict(self, param_dict):
        self.ConfigData.data.update(param_dict)

    def SaveConfigData(self):
        self.ConfigData.save()

    def SaveParamData(self):
        if self.ParamData.data:
            self.ParamData.save()

    # ------------------------------------------------------------------ Seiten und Verbindung (Web)
    ARDUINO_status = ""
    weblog = None                       # WebLog, wird von headless_web.py gesetzt

    # Farbtest (ColorCheckPage) liest/schreibt diese Werte am Controller
    coltab = None                       # Farbtabelle aus dem Makro SetColTab (vom Parameterformular gesetzt)
    checkcolor_callback = None          # wird mit der Palette aufgerufen, wenn der Farbtester beendet wird
    show_colorcheckpage_only = False
    paramDataChanged = False
    lednum_int = 0
    ledcount_int = 1

    def setParamData(self, key, value):
        self.ParamData.data[key] = value

    def setParamDataChanged(self):
        self.paramDataChanged = True

    def get_macrodef_data(self, macro, param):
        macrodata = self.MacroDef.data.get(macro, {})
        return macrodata.get(param, "") if macrodata != {} else ""

    def getFramebyName(self, pagename):
        if pagename == "ARDUINOMonitorPage" and self.weblog is not None:
            return self.weblog
        from web_log import NullFrame
        logger.info("Seite '%s' gibt es im Web nicht (No-Op)", pagename)
        return NullFrame()

    web_show_page = None                # von headless_web.py gesetzt: schaltet im Browser auf eine Registerkarte um

    def showFramebyName(self, pagename):
        if pagename == "ColorCheckPage" and self.web_show_page is not None:
            self.web_show_page(pagename)        # Farbtest oeffnen (wird aus dem Hintergrund-Thread des Makros aufgerufen)
        elif pagename == "ARDUINOMonitorPage" and self.weblog is not None:
            self.weblog.show()
        elif pagename == "ProgGeneratorPage" and self.weblog is not None:
            # M08 schaltet nach einem ERFOLGREICHEN Lauf zur Generator-Seite zurueck: das Log-Fenster
            # bleibt noch kurz lesbar und schliesst sich dann (bei Fehlern wird nicht zurueckgeschaltet).
            self.weblog.close_later()
        else:
            logger.info("Seite '%s' kann im Web nicht angezeigt werden", pagename)

    connectstatus_text = "Nicht verbunden"          # Verbindung zum Arduino: bleibt stehen (links in der Statuszeile von Tk)
    connectstatus_fg = "black"

    def set_connectstatusmessage(self, text, fg="black"):
        """Verbindungsstatus (Verbunden COM5 - EFFECT Mode ...). Getrennt von statusmessage_text, denn diese Meldungen
        verschwinden nach einigen Sekunden, der Verbindungsstatus soll stehen bleiben."""
        self.connectstatus_text = str(text)
        self.connectstatus_fg = fg
        logger.debug("set_connectstatusmessage: %s", text)

    # ------------------------------------------------------------------ Beenden
    def shutdown_program(self, save: bool = True):
        """Wie cancel_step2_with_save / cancel_step2_without_save in pyMobaLedLib.py:
        Konfiguration sichern, pro Workbook das Ereignis BeforeClose ausloesen und das
        temporaere Workbook-JSON speichern. (Fensterposition und persistente Makroparameter
        gibt es im Web nicht.)"""
        import ExcelAPI.XLA_Application as P01
        try:
            if self.is_connection_open():
                self.disconnect()                # LEDs aus, "#X" senden, Port schliessen
        except Exception:                        # noqa: BLE001
            logger.debug("Trennen beim Beenden fehlgeschlagen", exc_info=True)
        if save:
            self.SaveConfigData()
            self.SaveParamData()
        for wb in list(P01.Workbooks):
            wb.Evt_Workbook_BeforeClose()
            if save:
                fname = wb.workbookfilename
                if fname is None:
                    fname = os.path.join(self.mainfile_dir, self.tempworkbookFilname + "_" + wb.Name + ".json")
                wb.Save(filename=fname)

    # ------------------------------------------------------------------ abgeleitete Werte
    def get_font(self, fontname):
        font_size = self.getConfigData(fontname)
        if str(font_size) == "":
            return self._DC.SMALL_FONT
        return ("Verdana", int(font_size))

    def _init_from_config(self):
        g = self.getConfigData
        name = g("FontName")
        self.fontpattgen_name = name
        self.defaultfontnormal = (name, int(g("FontNormal") / SCALE_FACTOR))
        self.defaultfontsmall = (name, int(g("FontSmall") / SCALE_FACTOR))
        self.defaultfontlarge = (name, int(g("FontLarge") / SCALE_FACTOR))
        macrodata = self.MacroDef.data.get("StartPage", {})
        self.tempworkbookFilname = macrodata.get("TEMP_WORKBOOK_FILENAME", "StartPage")
        self.tempLedeffecttableFilname = macrodata.get("TEMP_LEDEFFECTTABLE_FILENAME", "StartPage")
        self.show_hiddentables = g("ShowHiddentables")
        self.maxLEDcnt = g("MaxLEDcnt")
        self.IPUploadTimeout = g("IPUploadTimeout")
        self.smallscreen = False
        # Flags, die M06_Write_Header / M08_ARDUINO am globalen Controller lesen (wie pyMobaLedLibapp)
        self.ARDUINOTest = g("ARDUINOTest")
        self.useESP32WinBat = self.command_line_args.get("useESP32WINBAT", False)
        self.execute_upload = True

    # ------------------------------------------------------------------ Excel-Schicht
    def create_excel_application(self):
        import ExcelAPI.XLA_Application as P01          # muss die Headless-Variante sein
        self.ExcelApplication = P01.CApplication(caption="pyMobaLedLib", Path=self.mainfile_dir,
                                                 p_global_controller=self)
        return self.ExcelApplication
