# Datei-Version: 1.05 (2026-11-10) - web_auth.py
# ----------------------------------------------------------------------------------------------
# Name:           web_auth.py
# Path:           _web/web_auth.py
# Version:        1.05
# Last Update:    2026-11-10
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.05  2026-11-10  Sitzungs-Cookie nach der Anmeldung: Safari und alle Browser auf dem iPad/iPhone (WebKit) senden die Anmeldung (HTTP Basic) nicht beim Aufbau der WebSocket-Verbindung mit; die Verbindung wurde mit 1008 abgewiesen und brach bei groesseren Aktionen (Wechsel des Blatts) ab. Cookies werden mitgesendet; abgewiesene WebSocket-Verbindungen werden einmal je Adresse ins Protokoll geschrieben (fruehere Versionen ohne Eintrag)
# ----------------------------------------------------------------------------------------------
"""Passwortschutz (HTTP Basic) fuer die Web-Oberflaeche, wenn sie im Netz erreichbar ist (Raspberry Pi).

Reines ASGI-Middleware: Es prueft sowohl normale Seitenaufrufe als auch die WebSocket-Verbindung der Oberflaeche.
Ob und mit welchem Passwort geprueft wird, bestimmt web_password: ein im Programm gesetztes Passwort (Programm Einstellungen) oder
das Passwort aus MLL_PASSWORD. Ohne Passwort wird nichts geprueft. Zugriffe vom Rechner selbst (localhost, z. B. das Desktop-Symbol
auf dem Pi) brauchen kein Passwort (MLL_LOCAL_NO_PASSWORD=0 schaltet das ab). Das Passwort wird im Klartext ueber das Netz
gesendet (kein https): fuer das Heimnetz gedacht, nicht fuer das Internet.
"""
from __future__ import annotations

import base64
import hashlib  # v1.05
import hmac  # v1.05
import logging
import secrets  # v1.05

from _web import web_password

logger = logging.getLogger(__name__)


COOKIE_NAME = "mllsession"  # v1.05
SESSION_SECRET = secrets.token_bytes(32)  # v1.05: nur im Speicher des Programms; nach einem Neustart muss man sich neu anmelden


def session_token() -> str:  # v1.05
    """Wert des Sitzungs-Cookies: HMAC aus Benutzername und Zustand des Passworts (aendert sich mit dem Passwort)"""  # v1.05
    message = ("%s|%s" % (web_password.username(), web_password.state_id())).encode("utf-8")  # v1.05
    return base64.urlsafe_b64encode(hmac.new(SESSION_SECRET, message, hashlib.sha256).digest()).decode("ascii").rstrip("=")  # v1.05


class BasicAuthMiddleware:
    LOCAL = ("127.0.0.1", "::1", "localhost", "::ffff:127.0.0.1")

    def __init__(self, app, realm: str = "webMobaLedLib", allow_local: bool = True):
        self.app = app
        self.allow_local = allow_local                       # Zugriffe vom Rechner selbst (Desktop-Symbol) brauchen kein Passwort
        self.realm = realm
        self._ok_cache: dict = {}                            # Authorization-Kopfzeile -> Zustand des Passworts, als sie geprueft wurde
        self._ws_rejected: set = set()                       # v1.05: Adressen, deren abgewiesene WebSocket-Verbindung schon im Protokoll steht

    def _ok(self, scope) -> bool:
        header = None
        for name, value in scope.get("headers", []):
            if name == b"authorization":
                header = value.decode("latin-1")
                break
        if header is None:
            return False
        state = web_password.state_id()
        if self._ok_cache.get(header) == state:              # schon geprueft: jede Seite laedt viele Dateien, der Hash ist langsam
            return True
        if not header.lower().startswith("basic "):
            return False
        try:
            user, _, password = base64.b64decode(header[6:]).decode("utf-8").partition(":")
        except (ValueError, UnicodeDecodeError):
            return False
        if web_password.verify(user, password):
            if len(self._ok_cache) > 200:
                self._ok_cache.clear()
            self._ok_cache[header] = state
            return True
        return False

    def _cookie_ok(self, scope) -> bool:  # v1.05
        """Gueltiges Sitzungs-Cookie? Browser senden Cookies auch beim Aufbau der WebSocket-Verbindung (die Anmeldung per HTTP Basic nicht immer: Safari/WebKit nicht)"""  # v1.05
        expected = session_token()  # v1.05
        for name, value in scope.get("headers", []):  # v1.05
            if name != b"cookie":  # v1.05
                continue  # v1.05
            for part in value.decode("latin-1").split(";"):  # v1.05
                key, _, val = part.strip().partition("=")  # v1.05
                if key == COOKIE_NAME and hmac.compare_digest(val.encode("utf-8"), expected.encode("utf-8")):  # v1.05
                    return True  # v1.05
        return False  # v1.05

    @staticmethod
    def _with_cookie(send):  # v1.05
        """Antwort um das Sitzungs-Cookie ergaenzen (nach einer Anmeldung per HTTP Basic)"""  # v1.05
        async def wrapped(message):  # v1.05
            if message.get("type") == "http.response.start":  # v1.05
                headers = list(message.get("headers", []))  # v1.05
                headers.append((b"set-cookie", ("%s=%s; Path=/; HttpOnly; SameSite=Lax; Max-Age=86400" % (COOKIE_NAME, session_token())).encode("ascii")))  # v1.05
                message = dict(message, headers=headers)  # v1.05
            await send(message)  # v1.05
        return wrapped  # v1.05

    def _is_local(self, scope) -> bool:
        client = scope.get("client")
        return bool(self.allow_local and client and client[0] in self.LOCAL)

    async def __call__(self, scope, receive, send):
        # if (scope["type"] not in ("http", "websocket") or not web_password.auth_required()  # v1.05 (entfallen)
        #         or self._is_local(scope) or self._ok(scope)):  # v1.05 (entfallen)
        if scope["type"] not in ("http", "websocket") or not web_password.auth_required() or self._is_local(scope):  # v1.05
            await self.app(scope, receive, send)
            return
        if self._cookie_ok(scope):                                               # v1.05: schon angemeldet (Sitzungs-Cookie)
            await self.app(scope, receive, send)  # v1.05
            return  # v1.05
        if self._ok(scope):                                                      # Anmeldung per HTTP Basic: bei Seitenaufrufen zusaetzlich das Cookie setzen  # v1.05
            await self.app(scope, receive, self._with_cookie(send) if scope["type"] == "http" else send)  # v1.05
            return  # v1.05
        if scope["type"] == "websocket":
            client = (scope.get("client") or ("?", 0))[0]  # v1.05
            if client not in self._ws_rejected:  # v1.05: einmal je Adresse ins Protokoll (hilft bei der Fehlersuche, zum Beispiel iPad)
                self._ws_rejected.add(client)  # v1.05
                logger.warning("WebSocket-Verbindung von %s abgewiesen: weder Anmeldung noch Sitzungs-Cookie. Der Browser hat sich noch nicht angemeldet "  # v1.05
                               "oder blockiert Cookies (Safari und alle Browser auf dem iPad senden die Anmeldung nicht mit der WebSocket-Verbindung).", client)  # v1.05
            await send({"type": "websocket.close", "code": 1008})
            return
        # body = "Anmeldung erforderlich".encode("utf-8")  # v1.04 (entfallen)
        from _web import web_i18n  # v1.04
        body = web_i18n.tr("Anmeldung erforderlich").encode("utf-8")  # v1.04
        await send({"type": "http.response.start", "status": 401, "headers": [
            (b"www-authenticate", f'Basic realm="{self.realm}", charset="UTF-8"'.encode("ascii")),
            (b"content-type", b"text/plain; charset=utf-8"), (b"content-length", str(len(body)).encode("ascii"))]})
        await send({"type": "http.response.body", "body": body})


def install(app, allow_local: bool = True):
    """Middleware in die FastAPI-/NiceGUI-App einhaengen (prueft nur, wenn ein Passwort eingerichtet ist)"""
    app.add_middleware(BasicAuthMiddleware, allow_local=allow_local)
    logger.info("Passwortschutz eingehaengt (Passwort eingerichtet: %s, localhost ohne Passwort: %s)", web_password.auth_required(), allow_local)
