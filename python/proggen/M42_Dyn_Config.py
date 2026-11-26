# Datei-Version: 1.14 (2026-11-26) - M42_Dyn_Config.py
# ----------------------------------------------------------------------------------------------
# Name:           M42_Dyn_Config.py
# Path:           proggen/M42_Dyn_Config.py
# Version:        1.14
# Last Update:    2026-11-26
# Author:         Harold Linke, Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.14 2026-11-26 M08-Abgleich auf Original-Release 5.54; Programm-VERSION unveraendert 5.54.
#   1.13 2026-11-26 M08-Upload auf 5.41/MobaLedLib 3.6.0 aktualisiert; neue Originalkorrekturen erhalten.
#   1.12  2026-11-25  Schnelles Update (serial_cfg) je Blatt: Option_Enabled liest zuerst esp32_options des aktiven Blattes, Set_Sheet_Option schreibt dorthin. Zeilen mit '# v1.12'
#   1.11  2026-11-25  Clear_Found_Port: der gefundene Anschluss eines frueheren Uploads wird vor jedem Upload geloescht (sonst haette ein anderes Board den Anschluss eines frueheren Pico ins Blatt bekommen koennen). Zeilen mit '# v1.11'
#   1.10  2026-11-24  Nach dem Upload merkt sich After_Full_Flash den gefundenen Anschluss (Funktion Found_Port), M08 traegt ihn ins Blatt ein. Zeilen mit '# v1.10'
#   1.09  2026-11-24  Timeout fuer die Suche nach dem Pico nach dem Upload von 25 s auf 10 s verkuerzt. Zeile mit '# v1.09'
#   1.08  2026-11-24  Bereitschaftspruefung: Antwort ~MLLERR (Firmware nicht geeignet) bricht sofort ab, ohne weitere Versuche. Zeilen mit '# v1.08'
#   1.08 2026-11-24 M08-Upload auf Original 5.12 aktualisiert, Pico-Identifikation und Firmware-Signatur erhalten.
#   1.07  2026-11-24  Pull Request 66 (Juergen, Issue 64): Die Programmversion (VERSION in webmobaledlib.py) gehoert zur Firmware-Signatur: nach jedem Softwareupdate wird einmal die ganze Firmware geflasht (_program_version). Zeilen mit '# v1.07'
#   1.06  2026-11-23  Identify (Juergen Winkler): After_Full_Flash: Pico nach dem Neustart an Seriennummer und Location erkennen (expected_serial, expected_location aus M08); bis zu 5
#                     Versuche, bis die Firmware auf '~MLLCFG INFO' antwortet (der Anschluss wird zwischen den Versuchen geschlossen). Zeilen mit '# v1.06'
#   1.07-m08 2026-11-24 M08-Vereinheitlichung mit Basis 4.98 zusammengefuehrt; neue Originalkorrekturen erhalten.
#   1.06 2026-11-23 AVR-Werkzeugpfade auch fuer schnelle Pico/ESP32-Konfiguration ueber M08 ermitteln.
#   1.05  2026-11-22  WLAN-Konfiguration bei Transportfehlern hoechstens dreimal mit neuer Sitzung versuchen
#   1.04  2026-11-22  Bei fehlender END-Antwort ueber WLAN gespeicherte Konfiguration nach Neustart verifizieren
#   1.03  2026-11-22  PlatformIO: AVR-Werkzeuge ohne Arduino-IDE-Suche ermitteln
#   1.02  2026-11-22  ESP32-WLAN ueber vorhandenen Geraetekanal; Wiederholungen nach OTA-Neustart
#   1.01  2026-11-19  Ausgabefenster: Der schnelle Weg zeigt, dass nur die Konfiguration uebertragen wird, den Fortschritt (25-%-Schritte) und die Fertigstellung; bei einem Rueckfall auf das ganze Programm steht der Grund da (Zeilen mit '# v1.01')
#   1.00  2026-11-19  Neu: ESP32 und Pico: Das Programm wird nur noch hochgeladen, wenn sich Quellcode, Erweiterungen oder Einstellungen aendern; sonst geht nur die Konfiguration
#                     ueber die serielle Schnittstelle zum Geraet (Einstellung 'serial_cfg'). Die Arbeit steckt in headless/headless_dyn_config.py
#                     ATmega (Nano/Uno) bleibt unveraendert: Decide() und Upload_Possible() gelten nur fuer ESP32 und Pico. Die Signatur der Firmware steht auch in der Konfigurationsdatei.
# ----------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
"""Anbindung der Funktion 'Konfiguration getrennt von der Firmware' an den Programm Generator

Ablauf:
  1. M06 fragt Decide(): Ist die Funktion eingeschaltet und moeglich? Dann schreibt es die Kopfdatei im Modus MLL_DYNAMIC_CONFIG.
  2. M06 ruft Finalize(): Konfigurationsdatei erzeugen, Signatur berechnen und in die Kopfdatei eintragen. Scheitert das, wird die Kopfdatei klassisch neu geschrieben.
  3. M08 ruft vor dem Uebersetzen Try_Config_Only(): Meldet das Geraet dieselbe Signatur, geht nur die Konfiguration hin und es wird nichts uebersetzt oder geflasht.
  4. Nach einem vollstaendigen Hochladen ruft M08 After_Full_Flash(): Die Konfiguration wird hinterher geschickt.
"""
import logging
import os
import time  # v1.01

import headless.headless_dyn_config as DC
import proggen.M02_Public as M02
import proggen.M02a_Public as M02a
import proggen.M25_Columns as M25
import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
import proggen.M09_Language as M09
import mlpyproggen.Prog_Generator as PG
import ExcelAPI.XLA_Application as P01

log = logging.getLogger("webmobaledlib.arduino")

OPTION_KEY = "serial_cfg"

_state = {"active": False, "off": False, "tools": None, "tools_checked": False, "env": "", "pico": False, "sig": "", "blob": None, "blob_file": "", "output": False}  # v1.01


def Option_Enabled():
    try:  # v1.12: die Einstellung des Blattes (Optionen, Reiter Lichtmaschine -> Einstellungen) hat Vorrang
        opts = getattr(P01.ActiveSheet, "esp32_options", None) or {}  # v1.12
        if OPTION_KEY in opts:  # v1.12
            return bool(opts[OPTION_KEY])  # v1.12
    except Exception:                                      # noqa: BLE001  # v1.12
        pass  # v1.12
    try:
        return bool(PG.global_controller.getConfigData(OPTION_KEY))
    except Exception:                                      # noqa: BLE001
        return False


def Set_Option(value):
    PG.global_controller.setConfigData(OPTION_KEY, bool(value))
    PG.global_controller.SaveConfigData()


def Set_Sheet_Option(value, sheet=None):  # v1.12: Schnelles Update je Blatt (wird mit dem Blatt gesichert); die globale Einstellung bleibt die Vorgabe fuer Blaetter ohne Eintrag
    ws = sheet or P01.ActiveSheet  # v1.12
    opts = dict(getattr(ws, "esp32_options", None) or {})  # v1.12
    opts[OPTION_KEY] = bool(value)  # v1.12
    ws.esp32_options = opts  # v1.12


def Active():
    """True wenn die zuletzt erzeugte Kopfdatei im Modus MLL_DYNAMIC_CONFIG geschrieben wurde"""
    return _state["active"]


def Environment():
    return _state["env"]


def Disable_Once(reason):
    """Die naechste Kopfdatei wird klassisch geschrieben (nach einem Fehler in Finalize)"""
    log.warning("Konfiguration getrennt von der Firmware: %s - es wird das ganze Programm hochgeladen", reason)
    _state["off"] = True
    _state["active"] = False


def _is_ip(text):
    return isinstance(text, str) and "IP:" in text


def _tools():
    if not _state["tools_checked"]:
        _state["tools_checked"] = True
        extra_bin, extra_plat = [], []
        if not M28.Is_PlatformIO():  # v1.03: IDE-Suche darf bei PlatformIO keinen Dialog oeffnen
            try:
                import proggen.M08_ARDUINO as M08
                ide = M30.FilePath(M08.Find_ArduinoExe())
                if ide:
                    extra_bin.append(os.path.join(ide, "hardware", "tools", "avr", "bin"))
                    extra_plat.append(os.path.join(ide, "hardware", "arduino", "avr"))
            except BaseException:                              # noqa: BLE001
                pass
        if M28.Is_PlatformIO():  # v1.06  # v1.08  # v1.13  # v1.14
            try:  # v1.06  # v1.08  # v1.13  # v1.14
                import proggen.M08_ARDUINO as M08  # v1.06  # v1.08  # v1.13  # v1.14
                pio_bin, pio_platform = M08.PIO_AVR_Paths()  # v1.06  # v1.08  # v1.13  # v1.14
                extra_bin.extend(pio_bin)  # v1.06  # v1.08  # v1.13  # v1.14
                extra_plat.extend(pio_platform)  # v1.06  # v1.08  # v1.13  # v1.14
            except Exception as error:  # v1.06: bestehende Suchorte bleiben als Rueckfall erhalten  # v1.08  # v1.13  # v1.14
                log.debug("PlatformIO-Werkzeugpfade nicht verfuegbar: %s", error)  # v1.06  # v1.08  # v1.13  # v1.14
        tools = DC.find_avr_tools(extra_bin, extra_plat)
        if tools is None:
            try:
                import proggen.M08_ARDUINO as M08
                P01.set_statusmessage(M09.Get_Language_Str("AVR-Werkzeuge werden mit PlatformIO installiert (einmalig) ..."))
                if DC.install_avr_tools(M08.Find_PIO()):
                    tools = DC.find_avr_tools(extra_bin, extra_plat)
            except BaseException as e:                     # noqa: BLE001
                log.warning("Konfiguration getrennt: AVR-Werkzeuge konnten nicht installiert werden: %s", e)
        _state["tools"] = tools
        if tools:
            log.info("Konfiguration getrennt: AVR-Werkzeuge in %s", tools["bin"])
    return _state["tools"]


def _program_version():  # v1.07
    """Programmversion aus webmobaledlib.py (VERSION = "..."); aus der Datei gelesen, damit das Ergebnis nicht davon abhaengt, wie das Programm gestartet wurde."""  # v1.07
    import re  # v1.07
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "webmobaledlib.py")  # v1.07
    try:  # v1.07
        with open(path, "r", encoding="utf-8", errors="replace") as fh:  # v1.07
            for line in fh:  # v1.07
                m = re.match(r'VERSION\s*=\s*"([^"]*)"', line)  # v1.07
                if m:  # v1.07
                    return m.group(1)  # v1.07
    except OSError:  # v1.07
        pass  # v1.07
    return ""  # v1.07


def Decide(CreateFilesOnly, HeaderOnly, firmware_key=""):  # v1.02
    """Soll die Kopfdatei im Modus MLL_DYNAMIC_CONFIG geschrieben werden?"""
    _state["firmware_key"] = firmware_key  # v1.02
    _state["active"] = False
    _state["output"] = False  # v1.01
    off = _state["off"]
    _state["off"] = False                                  # gilt nur fuer einen Durchlauf
    if not Option_Enabled() or CreateFilesOnly or HeaderOnly or off:
        return False
    board = M02a.Get_BoardTyp()
    if board not in (M02.HT_ESP32, M02.HT_PICO):
        return False
    why = ""
    port = P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL)
    if not M28.Is_PlatformIO():
        why = "nur mit PlatformIO moeglich"
    # elif _is_ip(port) or (board == M02.HT_ESP32 and P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL + 1) not in ("", None)):  # v1.02 (entfallen)
        # why = "nicht beim Hochladen per WLAN (IP-Adresse)"  # v1.02 (entfallen)
    elif board == M02.HT_PICO and _is_ip(port):  # v1.02: Pico-WLAN bleibt beim bisherigen Weg
        why = "Pico-Konfiguration nur ueber USB"  # v1.02
    elif _tools() is None:
        why = "die AVR-Werkzeuge (avr-g++ und Arduino-Kern) fehlen"
    if why:
        log.warning("Konfiguration getrennt von der Firmware ist eingeschaltet, aber %s - es wird das ganze Programm hochgeladen", why)
        return False
    _state.update(active=True, env="pico" if board == M02.HT_PICO else "esp32", pico=(board == M02.HT_PICO), sig="", blob=None, output=False)  # v1.01
    return True


def _lib_src(project_dir):
    lib = project_dir + "/libraries/MobaLedLib/src"
    if not os.path.isfile(lib + "/MobaLedLib.h"):
        lib = M30.DelLast(M02a.Get_Ardu_LibDir()) + "/MobaLedLib/src"
    return lib


def Finalize(header_path):
    """Nach dem Schreiben der Kopfdatei: Konfigurationsdatei erzeugen, Signatur eintragen. False bei einem Fehler."""
    try:
        import proggen.M08_ARDUINO as M08
        sketch_dir = os.path.dirname(os.path.abspath(header_path))
        project_dir = os.path.dirname(sketch_dir)
        env = _state["env"]
        if not M08.Write_PIO_Project(env, sketch_dir + os.sep):         # platformio.ini gehoert zur Signatur
            raise DC.DynConfigError("platformio.ini konnte nicht geschrieben werden")
        with open(header_path, "rb") as fh:
            raw = fh.read()
        sig = DC.compute_signature(raw.decode("utf-8", errors="replace"), sketch_dir, header_path, project_dir, os.path.join(project_dir, "platformio.ini"), env)
        import hashlib  # v1.07
        sig = hashlib.sha256((sig + "|prog|" + _program_version()).encode("utf-8")).hexdigest()[:16]  # v1.07: nach einem Softwareupdate einmal ganz flashen (Issue 64)
        if _state.get("firmware_key"):  # v1.02: WLAN-Einstellungen gehoeren zur Firmware
            import hashlib  # v1.02
            sig = hashlib.sha256((sig + _state["firmware_key"]).encode("utf-8")).hexdigest()[:16]  # v1.02
        workdir = os.path.join(project_dir, M02.Cfg_Dir_LED.strip("/\\"), "dyn")
        blob = DC.build_blob(sketch_dir, _lib_src(project_dir), _state["tools"], workdir, sig)
        blob_file = os.path.join(workdir, "mllcfg.bin")
        with open(blob_file, "wb") as fh:
            fh.write(blob)
        placeholder = DC.SIG_PLACEHOLDER.encode("ascii")
        if placeholder not in raw:
            raise DC.DynConfigError("Die Signatur fehlt in der Kopfdatei")
        with open(header_path, "wb") as fh:
            fh.write(raw.replace(placeholder, sig.encode("ascii")))
    except BaseException as e:                             # noqa: BLE001
        log.warning("Konfiguration getrennt von der Firmware: %s", e)
        _state["active"] = False
        return False
    _state.update(sig=sig, blob=blob, blob_file=blob_file)
    log.info("Konfiguration getrennt von der Firmware: Signatur %s, Konfigurationsdatei %d Bytes (%s)", sig, len(blob), blob_file)
    return True


def Upload_Possible(Mode, ComPort):
    """Gilt fuer den Upload, der gerade ansteht (M08)? """
    return (_state["active"] and _state["blob"] is not None and Mode in (M02.HT_ESP32, M02.HT_PICO) and not _is_ip(ComPort)
            and M28.Is_PlatformIO() and getattr(PG.global_controller, "execute_upload", True))


def _status(text):
    try:
        P01.set_statusmessage(text)
    except Exception:                                      # noqa: BLE001
        pass
    log.info(text)


def _t(text, **values):  # v1.01
    """Text in der eingestellten Sprache (Katalog csv/Web_Languages.csv); ohne die Web-Uebersetzung bleibt er deutsch"""  # v1.01
    try:  # v1.01
        from _web.web_i18n import tr  # v1.01
        return tr(text, **values)  # v1.01
    except Exception:                                      # noqa: BLE001  # v1.01
        return text.format(**values) if values else text  # v1.01


def _page():  # v1.01
    try:  # v1.01
        return PG.global_controller.getFramebyName("ARDUINOMonitorPage")  # v1.01
    except Exception:                                      # noqa: BLE001  # v1.01
        return None  # v1.01


def _out(text, highlight=None):  # v1.01
    """Zeile im Ausgabefenster (und damit im Protokoll)"""  # v1.01
    page = _page()  # v1.01
    if page is None:  # v1.01
        log.info(text)  # v1.01
        return  # v1.01
    try:  # v1.01
        if highlight:  # v1.01
            page.add_text_to_textwindow(text + "\n", highlight=highlight)  # v1.01
        else:  # v1.01
            page.add_text_to_textwindow(text + "\n")  # v1.01
    except Exception:                                      # noqa: BLE001  # v1.01
        log.info(text)  # v1.01


def _open_output():  # v1.01
    """Ausgabefenster fuer den schnellen Weg oeffnen und leeren"""  # v1.01
    _state["output"] = True  # v1.01
    page = _page()  # v1.01
    try:  # v1.01
        page.set_title(_t("Schnelles Update: Konfiguration übertragen"))  # v1.01
        page.delete_text_from_textwindow()  # v1.01
        PG.global_controller.showFramebyName("ARDUINOMonitorPage")  # v1.01
    except Exception:                                      # noqa: BLE001  # v1.01
        log.debug("Ausgabefenster nicht zu oeffnen", exc_info=True)  # v1.01


def _restore_title():  # v1.01
    """Nach dem Rueckfall auf das ganze Programm: wieder die Ueberschrift des normalen Hochladens"""  # v1.01
    try:  # v1.01
        from _web import web_log  # v1.01
        _page().set_title(web_log.DEFAULT_TITLE)  # v1.01
    except Exception:                                      # noqa: BLE001  # v1.01
        pass  # v1.01


def Output_Written():  # v1.01
    """True wenn Try_Config_Only etwas ins Ausgabefenster geschrieben hat (M08 loescht es dann beim ganzen Programm nicht, die Begruendung bleibt lesbar)"""  # v1.01
    return _state["output"]  # v1.01


def _progress():  # v1.01
    """Fortschrittsanzeige in 25-%-Schritten (die Datei hat nur wenige KB)"""  # v1.01
    nxt = [25]  # v1.01

    def callback(pos, total):  # v1.01
        pct = pos * 100 // total  # v1.01
        if pct >= nxt[0]:  # v1.01
            _out(_t("Konfiguration: {percent} % übertragen ({done} von {total} Bytes)", percent=pct, done=pos, total=total))  # v1.01
            nxt[0] = (pct // 25 + 1) * 25  # v1.01
    return callback  # v1.01


def _fallback(text, **values):  # v1.01
    """Der schnelle Weg geht nicht: Grund anzeigen, dann laedt M08 das ganze Programm hoch"""  # v1.01
    _out(_t(text, **values))  # v1.01
    _restore_title()  # v1.01
    return False  # v1.01


def _wlan_attempts(operation, *, after_flash=False):  # v1.05
    for attempt in range(1, 4):  # v1.05: drei Versuche insgesamt
        try:  # v1.05
            return operation()  # v1.05: Signaturfehler wird nicht wiederholt
        except (DC.DynConfigError, OSError) as error:  # v1.05
            _out(_t("WLAN-Konfiguration: Versuch {attempt} von {total} fehlgeschlagen ({reason}).", attempt=attempt, total=3, reason=error))  # v1.05
            if attempt < 3:  # v1.05
                time.sleep(1.0)  # v1.05: vorherige Sitzung freigeben lassen
                continue  # v1.05
            if after_flash:  # v1.05
                _out(_t("Die Konfiguration konnte nicht übertragen werden ({reason}).", reason=error), "Error")  # v1.05
                return False  # v1.05
            return _fallback("Die Konfiguration konnte nicht übertragen werden ({reason}). Es wird das ganze Programm hochgeladen.", reason=error)  # v1.05


def Try_Config_Only(ComPort, *, host="", password=""):  # v1.05
    _open_output()  # v1.05
    if host:  # v1.05
        return _wlan_attempts(lambda: _try_config_once(ComPort, host=host, password=password))  # v1.05
    return _try_config_once(ComPort)  # v1.05: USB bleibt bei einem Versuch


# def Try_Config_Only(ComPort):  # v1.02 (entfallen)
def _send_config(link, blob, host="", password=""):  # v1.04
    done = [0]  # v1.04
    report = _progress()  # v1.04
    def progress(pos, total):  # v1.04
        done[0] = pos  # v1.04
        report(pos, total)  # v1.04
    try:  # v1.04
        DC.send_blob(link, blob, progress)  # v1.04
        return  # v1.04
    except (DC.DynConfigError, OSError):  # v1.04
        if not host or done[0] != len(blob):  # v1.04
            raise  # v1.04
        link.close()  # v1.04
        # END kann bereits gespeichert und den Neustart ausgeloest haben.  # v1.04
        deadline = time.monotonic() + 25.0  # v1.04
        while time.monotonic() < deadline:  # v1.04
            check = None  # v1.04
            try:  # v1.04
                check = DC.TcpLink(host, password)  # v1.04
                info = DC.query_info(check, 2.0)  # v1.04
                if info and info.get("sig") == _state["sig"] and info.get("valid") == "1" and info.get("cfg") == "%08x" % DC.blob_crc(blob):  # v1.04
                    log.info("Konfiguration nach fehlender END-Antwort ueber WLAN verifiziert (Signatur und CRC)")  # v1.04
                    return  # v1.04
            except (DC.DynConfigError, OSError):  # v1.04
                pass  # v1.04
            finally:  # v1.04
                if check is not None:  # v1.04
                    check.close()  # v1.04
            time.sleep(0.5)  # v1.04
        raise  # v1.04: ohne gueltigen Nachweis bleibt die Uebertragung fehlgeschlagen


def _try_config_once(ComPort, *, host="", password=""):  # v1.05
    """True wenn das Geraet die Firmware dieser Kopfdatei hat und die Konfiguration uebertragen wurde (oder schon aktuell ist). Sonst False: dann das ganze Programm hochladen."""
    blob = _state["blob"]
    t0 = time.time()  # v1.01
    # _open_output()  # v1.05 (entfallen: Ausgabe bleibt zwischen Versuchen erhalten)
    try:
        # link = DC.Link(ComPort, dtr=_state["pico"])  # v1.02 (entfallen)
        link = DC.TcpLink(host, password) if host else DC.Link(ComPort, dtr=_state["pico"])  # v1.02
    except Exception as e:                                 # noqa: BLE001
        if host:  # v1.05
            raise DC.DynConfigError(str(e)) from e  # v1.05
        log.info("Konfiguration getrennt: Anschluss %s nicht zu oeffnen (%s) - ganzes Programm", ComPort, e)
        return _fallback("Der Anschluss {port} lässt sich nicht öffnen ({reason}). Es wird das ganze Programm hochgeladen.", port=ComPort, reason=e)  # v1.01
    try:
        _status("Die Firmware des Geraets wird geprueft ...")
        _out(_t("Die Firmware im Gerät ({port}) wird geprüft ...", port=ComPort))  # v1.01
        info = DC.query_info(link, 8.0)
        if info is None:
            if host:  # v1.05
                raise DC.DynConfigError("Keine Antwort auf INFO")  # v1.05
            log.info("Konfiguration getrennt: das Geraet antwortet nicht (Firmware ohne diese Funktion?) - ganzes Programm")
            return _fallback("Das Gerät antwortet nicht (noch nicht programmiert oder eine Firmware ohne diese Funktion). Es wird das ganze Programm hochgeladen.")  # v1.01
        if info.get("sig") != _state["sig"]:
            log.info("Konfiguration getrennt: Firmware %s passt nicht zu %s - ganzes Programm", info.get("sig"), _state["sig"])
            return _fallback("Die Firmware im Gerät passt nicht zu dieser Konfiguration. Es wird das ganze Programm hochgeladen.")  # v1.01
        if info.get("valid") == "1" and info.get("cfg") == "%08x" % DC.blob_crc(blob):
            log.info("Konfiguration getrennt: die Konfiguration im Geraet ist schon aktuell")
            _out(_t("Die Konfiguration im Gerät ist schon aktuell. Es muss nichts übertragen werden."), "OK")  # v1.01
            return True
        _status("Die Konfiguration wird uebertragen ...")
        _out(_t("Die Firmware im Gerät passt. Das Programm wird nicht neu hochgeladen, es wird nur die Konfiguration übertragen ({n} Bytes).", n=len(blob)))  # v1.01
        # DC.send_blob(link, blob, _progress())  # v1.04 (entfallen)
        _send_config(link, blob, host, password)  # v1.04
        log.info("Konfiguration getrennt: %d Bytes uebertragen, das Geraet startet neu", len(blob))
        _out(_t("Fertig: Die Konfiguration wurde in {seconds} s übertragen, das Gerät startet neu.", seconds="%.1f" % (time.time() - t0)), "OK")  # v1.01
        return True
    # except DC.DynConfigError as e:  # v1.02 (entfallen)
    except (DC.DynConfigError, OSError) as e:  # v1.02
        if host:  # v1.05
            raise  # v1.05: aeussere Schleife wiederholt erst nach link.close()
        log.warning("Konfiguration getrennt: %s - ganzes Programm", e)
        return _fallback("Die Konfiguration konnte nicht übertragen werden ({reason}). Es wird das ganze Programm hochgeladen.", reason=e)  # v1.01
    finally:
        link.close()


def Clear_Found_Port():  # v1.11
    """Vor jedem Upload aufrufen: ein Anschluss aus einem frueheren Upload (anderes Board) darf nicht ins Blatt geschrieben werden."""  # v1.11
    _state["found_port"] = None  # v1.11


def Found_Port():  # v1.10
    """Anschluss, an dem der Pico nach dem letzten Upload gefunden wurde (None, wenn keiner)."""  # v1.10
    return _state.get("found_port")  # v1.10

# def After_Full_Flash(ComPort):  # v1.02 (entfallen)
# def After_Full_Flash(ComPort, *, host="", password=""):  # v1.02  # v1.06 (entfallen)
def After_Full_Flash(ComPort, *, host="", password="", expected_serial=None, expected_location=None):  # v1.02  # v1.06
    """Nach dem Flashen die Konfiguration schicken. True wenn sie im Geraet angekommen ist.
    expected_serial/expected_location: Serial Number und Location des Pico VOR dem Upload (für erneute Erkennung nach Reboot)."""
    blob = _state["blob"]
    _state["found_port"] = None  # v1.10: je Upload neu
    t0 = time.time()  # v1.01
    _out("")  # v1.01
    _out(_t("Das Programm ist hochgeladen. Jetzt wird die Konfiguration übertragen ..."))  # v1.01
    # port = DC.wait_for_port(ComPort, _state["pico"], 25.0)  # v1.02 (entfallen)
    # if port is None:  # v1.02 (entfallen)
        # log.warning("Konfiguration getrennt: der Anschluss %s erscheint nach dem Hochladen nicht wieder", ComPort)  # v1.02 (entfallen)
        # _out(_t("Der Anschluss {port} erscheint nach dem Hochladen nicht wieder. Die Konfiguration wurde nicht übertragen.", port=ComPort), "Error")  # v1.01  # v1.02 (entfallen)
        # return False  # v1.02 (entfallen)
    # try:  # v1.02 (entfallen)
        # link = DC.Link(port, dtr=_state["pico"])  # v1.02 (entfallen)
    # except Exception as e:                                 # noqa: BLE001  # v1.02 (entfallen)
        # log.warning("Konfiguration getrennt: Anschluss %s nicht zu oeffnen: %s", port, e)  # v1.02 (entfallen)
        # _out(_t("Der Anschluss {port} lässt sich nicht öffnen ({reason}). Die Konfiguration wurde nicht übertragen.", port=port, reason=e), "Error")  # v1.01  # v1.02 (entfallen)
        # return False  # v1.02 (entfallen)
    if host:  # v1.02
        deadline = time.monotonic() + 30.0  # v1.02
        while True:  # v1.02
            try:  # v1.02
                link = DC.TcpLink(host, password)  # v1.02
                link.close()  # v1.05: Bereitschaft geprueft; jeder Versuch bekommt eine neue Sitzung
                return _wlan_attempts(lambda: _try_config_once(ComPort, host=host, password=password), after_flash=True)  # v1.05
                # break  # v1.05 (entfallen)  # v1.02
            except (OSError, DC.DynConfigError):  # v1.02
                if time.monotonic() >= deadline:  # v1.02
                    _out(_t("Die Konfiguration konnte nicht übertragen werden ({reason}).", reason="WLAN-Verbindung nach Neustart nicht verfuegbar"), "Error")  # v1.02
                    return False  # v1.02
                time.sleep(0.5)  # v1.02
    # else:  # v1.02  # v1.06 (entfallen)
        # port = DC.wait_for_port(ComPort, _state["pico"], 25.0)  # v1.02  # v1.06 (entfallen)
    else:  # v1.02: USB (Pico/ESP32/Arduino)  # v1.06
        # Nach Upload (insbesondere Pico) wartet das Geraet auf Neustart.  # v1.06
        # Port suchen, Verbindung oeffnen, dann warten bis Firmware bereit ist (Retry bis 5x mit 500ms).  # v1.06
        # expected_serial/expected_location wurden VOR dem Upload ermittelt und uebergeben  # v1.06
        port = DC.wait_for_port(ComPort, _state["pico"], 10.0, expected_serial, expected_location)  # v1.02  # v1.06  # v1.09: Timeout 10 s
        if port is not None:  # v1.10
            _state["found_port"] = port  # v1.10: Anschluss nach dem Neustart; M08 traegt ihn ins Blatt ein
        if port is None:  # v1.02
            log.warning("Konfiguration getrennt: der Anschluss %s erscheint nach dem Hochladen nicht wieder", ComPort)  # v1.02
            _out(_t("Der Anschluss {port} erscheint nach dem Hochladen nicht wieder. Die Konfiguration wurde nicht übertragen.", port=ComPort), "Error")  # v1.01  # v1.02
            return False  # v1.02
        # try:  # v1.02  # v1.06 (entfallen)
            # link = DC.Link(port, dtr=_state["pico"])  # v1.02  # v1.06 (entfallen)
        # except Exception as e:                                 # noqa: BLE001  # v1.02  # v1.06 (entfallen)
            # log.warning("Konfiguration getrennt: Anschluss %s nicht zu oeffnen: %s", port, e)  # v1.02  # v1.06 (entfallen)
            # _out(_t("Der Anschluss {port} lässt sich nicht öffnen ({reason}). Die Konfiguration wurde nicht übertragen.", port=port, reason=e), "Error")  # v1.01  # v1.02  # v1.06 (entfallen)
            # return False  # v1.02  # v1.06 (entfallen)

        link = None  # v1.06
        for attempt in range(5):  # max 5 Versuche  # v1.06
            fatal = None  # v1.08
            try:  # v1.06
                link = DC.Link(port, dtr=_state["pico"])  # v1.06
                # Firmware ready testen: INFO abfragen (bis 500ms warten, 5x retry = ~2.5s)  # v1.06
                for retry in range(5):  # v1.06
                    try:  # v1.06
                        log.info("TX: ~MLLCFG INFO (ready-check %d/%d)", retry + 1, 5)  # v1.06
                        link.send("~MLLCFG INFO")  # v1.06
                        msg = link.read("INFO", 0.5)  # v1.06
                        if msg:  # v1.06
                            log.info("RX: %s", msg)  # v1.06
                            info = DC.parse_info(msg)  # v1.06
                            if info:  # v1.06
                                break  # v1.06
                    except DC.DynConfigError as e:  # v1.08
                        if str(e).startswith("Fehler vom Geraet"):  # v1.08: ~MLLERR = Firmware nicht geeignet, nicht wiederholen
                            fatal = e  # v1.08
                            break  # v1.08
                    except Exception:  # v1.06
                        pass  # v1.06
                    if retry < 4:  # v1.06
                        time.sleep(0.5)  # v1.06
                else:  # v1.06
                    # Keine Antwort nach 5 Versuchen  # v1.06
                    raise DC.DynConfigError("Keine Antwort auf INFO nach Neustart")  # v1.06
                if fatal is not None:  # v1.08: Firmware meldet ~MLLERR -> sofort abbrechen, keine weiteren Versuche
                    link.close()  # v1.08
                    log.warning("Konfiguration getrennt: Firmware an %s ist fuer die Konfiguration nicht geeignet: %s", port, fatal)  # v1.08
                    _out(_t("Die Firmware am Anschluss {port} ist für die Konfiguration nicht geeignet ({reason}). Die Konfiguration wurde nicht übertragen.", port=port, reason=fatal), "Error")  # v1.08
                    return False  # v1.08
                break  # Verbindung ok, Firmware bereit  # v1.06
            except Exception as e:                                 # noqa: BLE001  # v1.06
                if link:  # v1.06: Anschluss vor dem naechsten Versuch freigeben
                    link.close()  # v1.06
                    link = None  # v1.06
                if attempt < 4:  # v1.06
                    log.info("Konfiguration: Versuch %d fehlgeschlagen, warte 500ms: %s", attempt + 1, e)  # v1.06
                    time.sleep(0.5)  # v1.06
                else:  # v1.06
                    log.warning("Konfiguration getrennt: Anschluss %s nicht bereit nach 5 Versuchen: %s", port, e)  # v1.06
                    _out(_t("Der Anschluss {port} lässt sich nicht öffnen ({reason}). Die Konfiguration wurde nicht übertragen.", port=port, reason=e), "Error")  # v1.06: vorhandener Text (Uebersetzungen)
                    return False  # v1.06

        # Link ist nun offen und Firmware bereit  # v1.06
    try:
        _status("Die Konfiguration wird uebertragen ...")
        info = DC.query_info(link, 20.0)
        if info is None:
            log.warning("Konfiguration getrennt: das Geraet antwortet nach dem Hochladen nicht")
            _out(_t("Das Gerät antwortet nach dem Hochladen nicht. Die Konfiguration wurde nicht übertragen."), "Error")  # v1.01
            return False
        if info.get("sig") != _state["sig"]:
            log.warning("Konfiguration getrennt: Firmware %s statt %s", info.get("sig"), _state["sig"])
            return False  # v1.02: keine fremde Konfiguration senden
        _out(_t("Die Konfiguration wird übertragen ({n} Bytes) ...", n=len(blob)))  # v1.01
        # DC.send_blob(link, blob, _progress())  # v1.04 (entfallen)
        _send_config(link, blob, host, password)  # v1.04
        log.info("Konfiguration getrennt: %d Bytes uebertragen, das Geraet startet neu", len(blob))
        _out(_t("Fertig: Die Konfiguration wurde in {seconds} s übertragen, das Gerät startet neu.", seconds="%.1f" % (time.time() - t0)), "OK")  # v1.01
        return True
    # except DC.DynConfigError as e:  # v1.02 (entfallen)
    except (DC.DynConfigError, OSError) as e:  # v1.02
        log.warning("Konfiguration getrennt: %s", e)
        _out(_t("Die Konfiguration konnte nicht übertragen werden ({reason}).", reason=e), "Error")  # v1.01
        return False
    finally:
        if link:  # v1.06
            link.close()  # v1.06
