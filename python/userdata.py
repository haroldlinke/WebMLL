# Datei-Version: 1.03 (2026-10-15) - userdata.py
"""Datenordner des Anwenders: alles, was das Programm selbst erzeugt, liegt AUSSERHALB des Projektordners.

Dazu gehoeren die Konfigurationsdateien, die Sicherungen der Tabellen (Arbeitsmappen), die Zwischensicherung, die Passwort-Datei
und die Protokolle. Dadurch bleiben sie erhalten, wenn der Projektordner (python) bei einem Update ersetzt oder ueberschrieben wird.

Ort (je Benutzer):
    Windows        %APPDATA%\\webMobaLedLib                        (C:\\Users\\<Name>\\AppData\\Roaming\\webMobaLedLib)
    macOS          ~/Library/Application Support/webMobaLedLib
    Linux, Pi      $XDG_DATA_HOME/webMobaLedLib, sonst ~/.local/share/webMobaLedLib
Bis Version 1.30 hiess der Ordner pyMobaLedLib: Beim ersten Start wird er umbenannt (Ersatz: kopiert), die Daten bleiben erhalten.
Anderer Ort: Umgebungsvariable MLL_DATA_DIR (zum Beispiel D:\\MobaLedDaten). Ist der Ordner nicht beschreibbar, wird ein Ordner im
temporaeren Verzeichnis benutzt (mit Warnung), damit das Programm trotzdem startet.

Aufruf als Programm gibt den Ordner aus (benutzt von den Startskripten):   python userdata.py
"""
from __future__ import annotations

import logging
import os
import platform
import shutil
import sys
import tempfile

logger = logging.getLogger(__name__)

APP_NAME = "webMobaLedLib"
OLD_APP_NAMES = ("pyMobaLedLib",)                  # Name des Datenordners bis Version 1.30
_cache: dict = {}


def default_dir() -> str:
    system = platform.system()
    home = os.path.expanduser("~")
    if system == "Windows":
        base = os.environ.get("APPDATA") or os.path.join(home, "AppData", "Roaming")
    elif system == "Darwin":
        base = os.path.join(home, "Library", "Application Support")
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.join(home, ".local", "share")
    return os.path.join(base, APP_NAME)


def _migrate_old_folder(new: str) -> None:
    """Datenordner eines frueheren Namens (pyMobaLedLib) uebernehmen: umbenennen, sonst kopieren. Nur wenn der neue Ordner noch fehlt."""
    base = os.path.dirname(new)
    for old_name in OLD_APP_NAMES:
        old = os.path.join(base, old_name)
        if os.path.isdir(old) and not os.path.exists(new):
            try:
                os.rename(old, new)
                logger.info("Datenordner umbenannt: %s -> %s", old, new)
            except OSError:
                try:                                          # zum Beispiel Windows, wenn eine Datei noch offen ist
                    shutil.copytree(old, new)
                    logger.warning("Datenordner kopiert (Umbenennen nicht moeglich): %s -> %s. Der alte Ordner darf spaeter geloescht werden.", old, new)
                except OSError:
                    logger.exception("Datenordner %s konnte nicht uebernommen werden", old)
            return


def data_dir() -> str:
    """Datenordner (wird bei Bedarf angelegt)"""
    key = os.environ.get("MLL_DATA_DIR", "")
    if _cache.get("key") == key and _cache.get("dir"):
        return _cache["dir"]
    folder = os.path.abspath(os.path.expanduser(key or default_dir()))
    if not key:
        _migrate_old_folder(folder)                           # nur beim Standardort, nie bei MLL_DATA_DIR
    try:
        os.makedirs(folder, mode=0o700, exist_ok=True)         # 0700: nur der Benutzer (Passwort-Hash, Konfiguration)
        if not os.access(folder, os.W_OK):
            raise OSError("nicht beschreibbar")
    except OSError as ex:
        fallback = os.path.join(tempfile.gettempdir(), APP_NAME)
        os.makedirs(fallback, exist_ok=True)
        logger.warning("Datenordner %s nicht nutzbar (%s): Ersatz %s. Die Daten gehen beim Neustart des Rechners eventuell verloren.",
                       folder, ex, fallback)
        folder = fallback
    _cache.update(key=key, dir=folder)
    return folder


def path(name: str) -> str:
    return os.path.join(data_dir(), name)


def log_file() -> str:
    return path("webmobaledlib.log")


def flat(name: str) -> str:
    """Nur der Dateiname, ohne Ordner. Das Originalprogramm benutzt Namen mit "../" (Konfiguration zwei Ordner, Sicherung der Tabellen einen
    Ordner ueber dem Programmordner). Im Datenordner liegen alle Dateien flach; mit dem "../" wuerden sie ueber dem Datenordner landen
    (zum Beispiel direkt in ~/.local oder ~/.local/share)."""
    return os.path.basename(str(name).replace("\\", "/"))


def copy_if_missing(old: str, new: str) -> bool:
    """Eine Datei aus dem alten Ort (Projektordner) einmalig in den Datenordner KOPIEREN, wenn es sie dort noch nicht gibt.
    Die alte Datei bleibt liegen (sie kann spaeter geloescht werden). True, wenn kopiert wurde."""
    try:
        if os.path.isfile(old) and not os.path.exists(new) and os.path.abspath(old) != os.path.abspath(new):
            os.makedirs(os.path.dirname(new), exist_ok=True)
            shutil.copy2(old, new)
            logger.info("Datei in den Datenordner kopiert: %s -> %s (die alte Datei darf geloescht werden)", old, new)
            return True
    except OSError:
        logger.exception("Datei konnte nicht in den Datenordner kopiert werden: %s", old)
    return False


if __name__ == "__main__":
    print(data_dir())
    sys.exit(0)
