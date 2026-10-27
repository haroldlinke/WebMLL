# Datei-Version: 1.05 (2026-10-27) - web_logging.py
"""Protokoll (Logging) der Web-Oberflaeche, im gleichen Stil wie im Original pyMobaLedLib.py.

Die Originalmodule benutzen den Standard-Logger (logging.getLogger(__name__)) und schreiben bis zur Stufe DEBUG. Damit dieses Protokoll
bei der Fehlersuche vollstaendig ist, gilt wie im Original: OHNE Angabe wird auf der Stufe DEBUG in die Datei geschrieben.

Kommandozeile (wie im Original) oder Umgebungsvariable (fuer den Dienst auf dem Raspberry Pi in /etc/mobaledlib-web.env):
    --loglevel DEBUG|INFO|WARNING|ERROR|CRITICAL      MLL_LOGLEVEL      Stufe der Protokolldatei (Standard DEBUG)
    --logfile NAME                                     MLL_LOGFILE       Dateiname (Standard webmobaledlib.log), "stdout" = keine Datei
Ein Dateiname ohne Pfad liegt im Datenordner (userdata.py), NICHT im Projektordner (anders als beim Original): Das Protokoll
ueberlebt dadurch ein Update des Projektordners. Ein absoluter Pfad wird unveraendert benutzt.

Die Datei dreht sich (2 MB, 5 alte Dateien: webmobaledlib.log.1 ... .5), damit sie nicht endlos waechst. Auf der Konsole (und im Journal des
Dienstes) erscheint ab INFO. Die sehr gespraechigen Bibliotheken (socketio, engineio, uvicorn.access, asyncio, PIL, httpx ...) bleiben
auf WARNING bzw. INFO, auch wenn die Stufe DEBUG ist; mit MLL_LOG_LIBS=1 werden sie nicht gedaempft.
"""
from __future__ import annotations

import argparse
import asyncio
import atexit
import faulthandler
import importlib.metadata
import logging
import logging.handlers
import os
import platform
import sys
import threading
import time

import userdata

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
DEFAULT_FILE = "webmobaledlib.log"
FILE_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
CONSOLE_FORMAT = "%(levelname)s %(name)s: %(message)s"
MAX_BYTES = 2_000_000
BACKUPS = 5
QUIET_LIBRARIES = {"engineio": logging.WARNING, "socketio": logging.WARNING, "uvicorn.access": logging.WARNING,
                   "asyncio": logging.WARNING, "PIL": logging.INFO, "urllib3": logging.WARNING, "httpx": logging.WARNING,
                   "httpcore": logging.WARNING, "multipart": logging.WARNING, "watchfiles": logging.WARNING,
                   "markdown_it": logging.WARNING, "charset_normalizer": logging.WARNING}

_state: dict = {"file_handler": None, "crash_file": None, "lag_task": None}


def setup(argv=None) -> dict:
    """Protokoll einrichten (so frueh wie moeglich aufrufen, vor dem Import der Originalmodule). Gibt die Einstellungen zurueck:
    {"level": Name, "level_explicit": bool, "file": Pfad oder None, "problems": [Hinweise, die nach dem Einrichten gemeldet werden]}"""
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument("--loglevel")
    parser.add_argument("--logfile")
    ns, _ = parser.parse_known_args(argv)
    problems = []

    level_text = (ns.loglevel or os.environ.get("MLL_LOGLEVEL") or "").strip().upper()
    explicit = level_text in LEVELS
    if level_text and not explicit:
        problems.append(f"Unbekannte Protokollstufe '{level_text}' (erlaubt: {', '.join(LEVELS)}): es gilt DEBUG")
    level_name = level_text if explicit else "DEBUG"                   # wie im Original: ohne Angabe DEBUG
    level = getattr(logging, level_name)

    file_arg = (ns.logfile or os.environ.get("MLL_LOGFILE") or DEFAULT_FILE).strip()
    if file_arg.lower() == "stdout":
        path = None
    elif os.path.isabs(file_arg):
        path = file_arg
    else:
        path = userdata.path(file_arg)                                    # Datenordner statt Projektordner

    console = logging.StreamHandler()
    console.setLevel(max(logging.INFO, level))
    console.setFormatter(logging.Formatter(CONSOLE_FORMAT))
    handlers = [console]
    file_handler = None
    if path:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(path, maxBytes=MAX_BYTES, backupCount=BACKUPS, encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(logging.Formatter(FILE_FORMAT))
            handlers.append(file_handler)
        except OSError as ex:
            problems.append(f"Protokolldatei {path} nicht beschreibbar ({ex}): nur Konsole")
            path = None
    logging.basicConfig(level=level if file_handler else console.level, handlers=handlers, force=True)
    _state["file_handler"] = file_handler
    if os.environ.get("MLL_LOG_LIBS") != "1":
        for name, lvl in QUIET_LIBRARIES.items():
            logging.getLogger(name).setLevel(lvl)
    info = {"level": level_name, "level_explicit": explicit, "file": path, "problems": problems}
    for text in problems:
        logging.getLogger(__name__).warning(text)
    return info


def log_banner(logger: logging.Logger, program: str, project_dir: str, info: dict, argv=None) -> None:
    """Kopf des Protokolls wie im Original (Python-Version, System, Parameter, Ordner, Stufe, Datei)"""
    stars = "*" * 107
    logger.info(stars)
    logger.info("Python Version: %s", sys.version.replace("\n", " "))
    logger.info("MLL Web-Oberflaeche gestartet: %s", program)
    logger.info(" Platform: %s", platform.platform())
    logger.info("Parameters: %s", repr(list(sys.argv[1:] if argv is None else argv)))
    logger.debug("Installationfolder %s", project_dir)
    logger.debug("Datenordner %s", userdata.data_dir())
    logger.debug("Logging Level: %s Logfilename: %s", info.get("level"), info.get("file"))
    log_environment(logger)
    logger.info(stars)
    logger.info(" ")


def log_environment(logger: logging.Logger) -> None:
    """Versionen der wichtigsten Pakete und die Umgebung (Sitzungsart, Display, Tk): hilft bei Verbindungsabbruechen und Abstuerzen"""
    found = []
    for name in ("nicegui", "uvicorn", "python-socketio", "python-engineio", "starlette", "fastapi", "websockets", "uvloop", "httptools",
                 "orjson", "pyserial", "Pillow", "openpyxl"):
        try:
            found.append(f"{name} {importlib.metadata.version(name)}")
        except importlib.metadata.PackageNotFoundError:
            pass
    logger.info("Pakete: %s", ", ".join(found) or "keine gefunden")
    logger.info("Umgebung: Sitzung=%s DISPLAY=%s WAYLAND_DISPLAY=%s MLL_TK_ROOT=%s MLL_HEADLESS=%s",
                os.environ.get("XDG_SESSION_TYPE", "-"), os.environ.get("DISPLAY", "-"), os.environ.get("WAYLAND_DISPLAY", "-"),
                os.environ.get("MLL_TK_ROOT", "-"), os.environ.get("MLL_HEADLESS", "-"))
    try:
        from _web import web_pi_status  # v1.05
        web_pi_status.log_banner()                                           # Raspberry Pi: Modell, Unterspannung, Temperatur, Speicher (sonst nichts)  # v1.05
    except Exception:                                                        # noqa: BLE001  # v1.05
        logger.debug("Raspberry Pi: Status nicht lesbar", exc_info=True)  # v1.05
    try:  # v1.05
        import tkinter
        if getattr(tkinter, "__file__", "") == "<no_tk>":
            logger.info("tkinter: Ersatz no_tk (kein Tk noetig)")
        else:
            logger.info("tkinter %s: echtes Tk", tkinter.TkVersion)
    except Exception as ex:                                              # noqa: BLE001
        logger.info("tkinter nicht verfuegbar (%s)", type(ex).__name__)


class _AbortedRequestFilter(logging.Filter):
    """Bricht der Browser eine Anfrage ab (Seite neu geladen, Reiter geschlossen, langsamer Server), meldet Starlette "RuntimeError: No response
    returned" mit einem Traceback von rund 50 Zeilen. Das ist harmlos, kommt auf langsamen Rechnern aber dutzendfach und fuellt das Protokoll.
    Der Filter unterdrueckt den Traceback und meldet nur die erste Anfrage und danach jede fuenfzigste."""

    def filter(self, record: logging.LogRecord) -> bool:
        exc = record.exc_info[1] if record.exc_info else None
        if isinstance(exc, RuntimeError) and "No response returned" in str(exc):
            _state["aborted"] = _state.get("aborted", 0) + 1
            n = _state["aborted"]
            if n == 1 or n % 50 == 0:
                logging.getLogger("webmobaledlib.http").info("Der Browser hat Anfragen abgebrochen (bisher %d, harmlos)", n)
            return False
        return True


def attach_to_uvicorn() -> None:
    """uvicorn richtet beim Start eigene Handler ein und schreibt Fehler der Webanwendung nur auf die Konsole. Die Protokolldatei
    haengt sich deshalb nach dem Start zusaetzlich an die uvicorn-Logger (Aufruf aus app.on_startup). Abgebrochene Anfragen des Browsers
    ("No response returned") werden nur gezaehlt."""
    handler = _state.get("file_handler")
    for name in ("uvicorn", "uvicorn.error"):
        lg = logging.getLogger(name)
        if not any(isinstance(f, _AbortedRequestFilter) for f in lg.filters):
            lg.addFilter(_AbortedRequestFilter())
        if handler is not None and handler not in lg.handlers:
            lg.addHandler(handler)


def install_crash_hooks() -> None:
    """Abstuerze und unbemerkte Fehler ins Protokoll bringen:
    - faulthandler: Abbruch des Python-Prozesses (Segmentation fault, "Aborted" durch Tcl/Tk ...) schreibt die Aufrufe aller Threads in die
      Datei webmobaledlib-crash.log im Datenordner (die Protokolldatei selbst koennte dabei nicht mehr geschrieben werden),
    - Ausnahmen im Hauptthread und in Threads (auch sys.exit() der Originalmodule in einem Thread, das Python sonst stillschweigend
      ignoriert) und Ausnahmen in __del__/Aufraeumcode,
    - Ende des Prozesses."""
    log = logging.getLogger("webmobaledlib.crash")
    try:
        crash_file = open(userdata.path("webmobaledlib-crash.log"), "a", encoding="utf-8", buffering=1)
        crash_file.write(f"\n===== Start {time.strftime('%Y-%m-%d %H:%M:%S')}, Prozess {os.getpid()} =====\n")
        faulthandler.enable(file=crash_file, all_threads=True)
        _state["crash_file"] = crash_file                                   # offen halten
    except OSError as ex:
        log.warning("Absturzprotokoll nicht moeglich: %s", ex)

    def excepthook(exc_type, exc, tb):
        log.critical("Unbehandelte Ausnahme im Hauptthread", exc_info=(exc_type, exc, tb))
        sys.__excepthook__(exc_type, exc, tb)

    def thread_hook(args):
        name = getattr(args.thread, "name", "?")
        if args.exc_type is SystemExit:
            log.warning("sys.exit() im Thread %s (ein Modul hat das Programm beenden wollen)", name,
                        exc_info=(args.exc_type, args.exc_value, args.exc_traceback))
        else:
            log.critical("Unbehandelte Ausnahme im Thread %s", name, exc_info=(args.exc_type, args.exc_value, args.exc_traceback))

    def unraisable(u):
        log.error("Nicht abfangbare Ausnahme (%s) in %r", u.err_msg or "Aufraeumcode", u.object,
                  exc_info=(u.exc_type, u.exc_value, u.exc_traceback))

    sys.excepthook = excepthook
    threading.excepthook = thread_hook
    sys.unraisablehook = unraisable
    atexit.register(lambda: log.info("Prozess %s beendet", os.getpid()))


async def _lag_monitor(interval: float = 1.0, warn_after: float = 1.0) -> None:
    """Meldet, wenn die Ereignisschleife des Servers blockiert war: Dann antwortet der Server dem Browser nicht mehr rechtzeitig, und
    die Oberflaeche zeigt "Connection lost" (Verbindung verloren) und laedt neu."""
    log = logging.getLogger("webmobaledlib.loop")
    last = time.monotonic()
    while True:
        await asyncio.sleep(interval)
        now = time.monotonic()
        lag = now - last - interval
        last = now
        if lag > warn_after:
            log.warning("Die Ereignisschleife war %.1f s blockiert (der Browser kann die Verbindung verlieren)", lag)


async def attach_loop_diagnostics() -> None:
    """Aus app.on_startup: Fehler in asyncio-Aufgaben protokollieren und die Ereignisschleife auf Blockaden ueberwachen"""
    log = logging.getLogger("webmobaledlib.loop")
    loop = asyncio.get_running_loop()

    def handler(_loop, context):
        log.error("Fehler in der Ereignisschleife: %s", context.get("message", ""), exc_info=context.get("exception"))

    loop.set_exception_handler(handler)
    _state["lag_task"] = loop.create_task(_lag_monitor())                  # Verweis behalten, sonst wird die Aufgabe eingesammelt
