# Datei-Version: 1.08 (2026-10-15) - headless_app_controller.py
"""HeadlessAppController: Tk-freier Ersatz fuer pyMobaLedLibapp (Startprogramm).

Uebernimmt aus pyMobaLedLibapp nur, was die Excel-Schicht und der Programmgenerator
brauchen: Konfiguration (ConfigData/ParamData/MacroDef), Fonts, Versionen, Statusmeldungen.
Logik von readConfigData()/getConfigData()/setConfigData() ist 1:1 uebernommen, damit
beide Programme dieselben Konfigurationsdateien lesen.

Ordner: mainfile_dir ist der PROJEKTORDNER (Programm, Vorlagen, Definitionen: nur lesen). Alles, was das Programm selbst erzeugt
(Konfiguration, Sicherungen der Tabellen), liegt im DATENORDNER data_dir ausserhalb des Projektordners (siehe userdata.py), damit es bei
einem Update des Projektordners erhalten bleibt. Dateien eines frueheren Stands werden einmalig aus dem Projektordner in den
Datenordner kopiert.

Nicht enthalten (noch): serielle Verbindung zum Arduino, Menues, Notebook, Tooltips.
Fehlende Attribute fuehren absichtlich zu einem AttributeError, damit klar wird, was noch
gebraucht wird.

Benutzung (aus dem Projektordner, MLL_HEADLESS=1 gesetzt):

    from headless.headless_app_controller import HeadlessAppController
    ctrl = HeadlessAppController(mainfile_dir=os.path.dirname(os.path.abspath("pyMobaLedLib.py")))
    ctrl.create_excel_application()
"""
from __future__ import annotations

import logging

from _web.web_serial import SerialMixin
import os
import sys

from headless.headless_controller import HeadlessController
import userdata

logger = logging.getLogger(__name__)

SCALE_FACTOR = 1   # wie ScaleFactor in pyMobaLedLib.py


class HeadlessAppController(SerialMixin, HeadlessController):
    def __init__(self, mainfile_dir: str, command_line_args: dict | None = None, data_dir: str | None = None):
        # Imports hier, damit der Fehler klar auf das Projekt zeigt, falls der Pfad nicht stimmt
        from mlpyproggen.configfile import ConfigFile
        from mlpyproggen import DefaultConstants as DC

        self._ConfigFile = ConfigFile
        self._DC = DC
        super().__init__(prog_version=DC.PROG_VERSION, data_version=DC.DATA_VERSION,
                         prog_gen_min_data_version=DC.ProgGen_Min_Data_Version,
                         patt_gen_min_data_version=DC.Pattgen_Min_Data_Version)

        self.mainfile_dir = mainfile_dir                  # Projektordner (nur lesen)
        self.data_dir = data_dir or userdata.data_dir()    # Datenordner des Anwenders (Konfiguration, Sicherungen, Protokolle)
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
        # Die Dateinamen aus DefaultConstants koennen "../" enthalten: im Datenordner liegen sie flach (userdata.flat). Einmalig werden Dateien
        # der Versionen 1.17 bis 1.22 uebernommen, die irrtuemlich ausserhalb des Datenordners lagen (Datenordner plus "../"). Dateien der
        # Tk-Version werden nicht uebernommen: Die Web-Version teilt keine Dateien mit ihr.
        for fname in (DC.PARAM_FILENAME, DC.CONFIG_FILENAME):
            userdata.copy_if_missing(os.path.normpath(os.path.join(self.data_dir, fname)), os.path.join(self.data_dir, userdata.flat(fname)))
        self.ParamData = ConfigFile(DC.DEFAULT_PARAM, userdata.flat(DC.PARAM_FILENAME), filedir=self.data_dir)
        self.ConfigData = ConfigFile(DC.DEFAULT_CONFIG, userdata.flat(DC.CONFIG_FILENAME), filedir=self.data_dir)
        filedir = self.mainfile_dir                       # die Definitionen (MacroDef ...) gehoeren zum Programm
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

    _arduino_ide_cache = ""
    _arduino_ide_miss = 0.0                                    # Zeitpunkt der letzten erfolglosen Suche
    _arduino_ide_logged = False

    @staticmethod
    def arduino_ide_patterns() -> list:
        """Orte, an denen die automatische Suche nachsieht (Reihenfolge = Vorrang). Muster mit * werden aufgeloest."""
        import platform
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            roots = [os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"), os.environ.get("ProgramFiles", r"C:\Program Files")]
            return [os.path.join(r, "Arduino", "arduino.exe") for r in roots]
        if platform.system() == "Darwin":                           # macOS: Programm der IDE 1.8 im Ordner Programme
            return ["/Applications/Arduino.app/Contents/MacOS/Arduino", os.path.join(home, "Applications/Arduino.app/Contents/MacOS/Arduino")]
        return ["/opt/arduino-1.8*/arduino", "/opt/arduino*/arduino", "/usr/local/arduino*/arduino",
                os.path.join(home, "arduino-1.8*/arduino"), os.path.join(home, "arduino*/arduino"),
                os.path.join(home, "*/arduino-1.8*/arduino")]       # eine Ebene tiefer: ~/Downloads/arduino-1.8.19, ~/Programme/arduino-1.8.19 ...

    def find_arduino_ide(self) -> str:
        """Pfad der ARDUINO IDE ausserhalb von Windows (die Startdatei `arduino`). Reihenfolge: Umgebungsvariable MLL_ARDUINO_EXE, dann die
        Orte aus arduino_ide_patterns() (neueste Version zuerst), zuletzt `arduino` im Suchpfad. Ein Treffer wird gemerkt, ein Misserfolg
        nur 10 Sekunden (die IDE kann nachtraeglich installiert werden). Unter Windows sucht das Programm selbst (M08_ARDUINO.Find_ArduinoExe)."""
        import glob
        import platform
        import shutil
        import time
        if platform.system() == "Windows":
            return ""
        if self._arduino_ide_cache and os.path.isfile(self._arduino_ide_cache):
            return self._arduino_ide_cache
        if time.monotonic() - self._arduino_ide_miss < 10.0:
            return ""
        candidates = [os.environ.get("MLL_ARDUINO_EXE", "")]
        for pattern in self.arduino_ide_patterns():
            candidates += sorted(glob.glob(pattern), reverse=True)
        candidates.append(shutil.which("arduino") or "")
        self._arduino_ide_cache = next((x for x in candidates if x and os.path.isfile(x)), "")
        if self._arduino_ide_cache:
            logger.info("ARDUINO IDE gefunden: %s", self._arduino_ide_cache)
            self._arduino_ide_logged = False
        else:
            self._arduino_ide_miss = time.monotonic()
            if not self._arduino_ide_logged:                       # nur einmal melden, mit den Orten, die geprueft wurden
                self._arduino_ide_logged = True
                logger.warning("ARDUINO IDE nicht gefunden. Gesucht in: MLL_ARDUINO_EXE=%s; %s; im Suchpfad (arduino). "
                               "Pfad in 'ARDUINO Einstellungen' eintragen oder die IDE 1.8.19 nach ~/arduino-1.8.19 legen.",
                               os.environ.get("MLL_ARDUINO_EXE", "(nicht gesetzt)"), "; ".join(self.arduino_ide_patterns()))
        return self._arduino_ide_cache

    @staticmethod
    def arduino_ide_version(start_file: str) -> str:
        """Versionsnummer der IDE aus revisions.txt neben der Startdatei (leer, wenn nicht lesbar)"""
        import re
        folder = os.path.dirname(start_file)
        for rel in ("revisions.txt", os.path.join("..", "Java", "revisions.txt")):          # Linux/Windows, macOS
            try:
                with open(os.path.join(folder, rel), encoding="utf-8", errors="replace") as fh:
                    match = re.search(r"ARDUINO\s+([0-9][0-9.]*)", fh.readline())
                    if match:
                        return match.group(1)
            except OSError:
                pass
        return ""

    def search_arduino_ide(self, max_seconds: float = 12.0, max_depth: int = 4) -> list:
        """Gruendliche Suche (Schaltflaeche "IDE suchen" in den ARDUINO Einstellungen): die ueblichen Orte und danach alle Ordner bis zur Tiefe
        max_depth unter dem Home-Ordner, /opt, /usr/local und /usr/share (ohne versteckte Ordner, Python-Umgebungen und aehnliches), hoechstens
        max_seconds lang. Gefunden wird eine Startdatei `arduino`, neben der die Ordner hardware und lib der IDE 1.8 liegen (nicht die IDE 2.x).
        Ergebnis: Liste von {"path", "version"}, die Version 1.8 zuerst, neueste zuerst."""
        import glob
        import platform
        import shutil
        import time
        windows = platform.system() == "Windows"
        name = "arduino.exe" if windows else "arduino"
        found: dict = {}

        def is_ide(path: str) -> bool:
            folder = os.path.dirname(path)
            return os.path.isfile(path) and os.path.isdir(os.path.join(folder, "hardware")) and (
                os.path.isdir(os.path.join(folder, "lib")) or os.path.isfile(os.path.join(folder, "revisions.txt")))

        for pattern in self.arduino_ide_patterns():
            for path in glob.glob(pattern):
                if os.path.isfile(path) and (platform.system() == "Darwin" or is_ide(path)):
                    found[path] = None
        which = shutil.which("arduino")
        if which and is_ide(os.path.realpath(which)):
            found[os.path.realpath(which)] = None
        if platform.system() != "Darwin":
            home = os.path.expanduser("~")
            roots = [home, "/opt", "/usr/local", "/usr/share"] if not windows else [home, os.environ.get("ProgramFiles(x86)", ""), os.environ.get("ProgramFiles", "")]
            skip = {"node_modules", "site-packages", "venv", "venv_web", "__pycache__", "snap", "proc", "sys", "Library", "AppData"}
            deadline = time.monotonic() + max_seconds
            for root in roots:
                if not root or not os.path.isdir(root):
                    continue
                base = root.rstrip(os.sep).count(os.sep)
                for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
                    if time.monotonic() > deadline:
                        break
                    depth = dirpath.count(os.sep) - base
                    dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in skip] if depth < max_depth else []
                    if name in filenames and is_ide(os.path.join(dirpath, name)):
                        found[os.path.join(dirpath, name)] = None
        result = [{"path": p, "version": self.arduino_ide_version(p)} for p in found]

        def sort_key(item):
            parts = [int(x) if x.isdigit() else 0 for x in item["version"].split(".")] if item["version"] else [0]
            return (0 if item["version"].startswith("1.8") else 1, [-x for x in parts])

        return sorted(result, key=sort_key)

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
    weblog = None                       # WebLog, wird von webmobaledlib.py gesetzt

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
        from _web.web_log import NullFrame
        logger.info("Seite '%s' gibt es im Web nicht (No-Op)", pagename)
        return NullFrame()

    web_show_page = None                # von webmobaledlib.py gesetzt: schaltet im Browser auf eine Registerkarte um

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
                    fname = os.path.join(self.data_dir, userdata.flat(self.tempworkbookFilname) + "_" + wb.Name + ".json")
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
        self.ExcelApplication = P01.CApplication(caption="webMobaLedLib", Path=self.mainfile_dir,
                                                 p_global_controller=self)
        return self.ExcelApplication
