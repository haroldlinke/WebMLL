# Datei-Version: 1.00 (2026-10-13) - web_password.py
"""Zugangsdaten der Web-Oberflaeche (Benutzername und Passwort fuer den Zugriff aus dem Netz).

Quellen, in dieser Reihenfolge:
  1. Ein vom Anwender im Programm gesetztes Passwort (Programm Einstellungen -> Zugriff ueber das Netz). Es steht NUR als Hash
     (PBKDF2-SHA256 mit Salz) in der Datei web_password.json im Projektordner, nie im Klartext.
  2. Das Passwort der Umgebungsvariable MLL_PASSWORD (auf dem Raspberry Pi in /etc/mobaledlib-web.env; Voreinstellung der
     Installation: "mobaledlib").
  Ohne beides ist kein Passwortschutz eingerichtet.
Passwort vergessen: web_password.json im Projektordner loeschen, dann gilt wieder das Passwort aus MLL_PASSWORD.
Benutzername: MLL_USER, sonst "mobaledlib".
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os
import secrets

logger = logging.getLogger(__name__)

HERE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(HERE, "web_password.json")
DEFAULT_USER = "mobaledlib"
DEFAULT_PASSWORD = "mobaledlib"
ITERATIONS = 150_000
MIN_LENGTH = 4

_cache = {"mtime": None, "data": None}


def username() -> str:
    return os.environ.get("MLL_USER") or DEFAULT_USER


def env_password() -> str:
    return os.environ.get("MLL_PASSWORD", "")


def _load():
    """Gespeicherten Hash lesen (nur neu, wenn sich die Datei geaendert hat)"""
    try:
        mtime = os.stat(FILE).st_mtime_ns
    except OSError:
        _cache.update(mtime=None, data=None)
        return None
    if _cache["mtime"] == mtime:
        return _cache["data"]
    data = None
    try:
        with open(FILE, encoding="utf-8") as fh:
            raw = json.load(fh)
        data = {"salt": base64.b64decode(raw["salt"]), "hash": base64.b64decode(raw["hash"]), "iterations": int(raw["iterations"])}
    except (OSError, ValueError, KeyError, TypeError):
        logger.warning("%s ist unlesbar und wird ignoriert", FILE)
    _cache.update(mtime=mtime, data=data)
    return data


def state_id():
    """Aendert sich, wenn sich das gueltige Passwort aendert (fuer den Zwischenspeicher der Anmeldungen)"""
    _load()
    return (_cache["mtime"], env_password())


def has_stored() -> bool:
    return _load() is not None


def auth_required() -> bool:
    """Ist ein Passwortschutz eingerichtet? Eine vorhandene, aber unlesbare Datei web_password.json gilt auch als eingerichtet (dann
    ist niemand mit einem unbekannten Passwort angemeldet: sicherer als ein offener Zugang); auf dem Rechner selbst geht es weiter."""
    return os.path.exists(FILE) or bool(env_password())


def uses_default_password() -> bool:
    """True, wenn noch das Standardpasswort aus der Installation gilt (kein eigenes gesetzt)"""
    return not has_stored() and env_password() == DEFAULT_PASSWORD


def _hash(password: str, salt: bytes, iterations: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def verify(user: str, password: str) -> bool:
    ok_user = hmac.compare_digest(user.encode("utf-8"), username().encode("utf-8"))
    data = _load()
    if data is not None:
        return bool(hmac.compare_digest(_hash(password, data["salt"], data["iterations"]), data["hash"]) and ok_user)
    env = env_password()
    return bool(env) and bool(hmac.compare_digest(password.encode("utf-8"), env.encode("utf-8"))) and ok_user


def validate_new(password: str, repeat: str) -> str:
    """Fehlertext, wenn das neue Passwort nicht angenommen wird, sonst leerer Text"""
    if password != repeat:
        return "Die beiden Eingaben sind nicht gleich."
    if len(password) < MIN_LENGTH:
        return f"Das Passwort muss mindestens {MIN_LENGTH} Zeichen lang sein."
    if password != password.strip():
        return "Das Passwort darf nicht mit einem Leerzeichen beginnen oder enden."
    return ""


def set_password(password: str) -> None:
    salt = secrets.token_bytes(16)
    data = {"salt": base64.b64encode(salt).decode("ascii"), "hash": base64.b64encode(_hash(password, salt, ITERATIONS)).decode("ascii"),
            "iterations": ITERATIONS, "algorithm": "pbkdf2-sha256"}
    tmp = FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
    os.replace(tmp, FILE)                                      # erst fertig schreiben, dann ersetzen
    logger.info("Passwort der Web-Oberflaeche geaendert")


def clear_password() -> None:
    try:
        os.remove(FILE)
        logger.info("Eigenes Passwort der Web-Oberflaeche entfernt")
    except FileNotFoundError:
        pass
