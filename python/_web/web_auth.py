# Datei-Version: 1.03 (2026-10-15) - web_auth.py
"""Passwortschutz (HTTP Basic) fuer die Web-Oberflaeche, wenn sie im Netz erreichbar ist (Raspberry Pi).

Reines ASGI-Middleware: Es prueft sowohl normale Seitenaufrufe als auch die WebSocket-Verbindung der Oberflaeche.
Ob und mit welchem Passwort geprueft wird, bestimmt web_password: ein im Programm gesetztes Passwort (Programm Einstellungen) oder
das Passwort aus MLL_PASSWORD. Ohne Passwort wird nichts geprueft. Zugriffe vom Rechner selbst (localhost, z. B. das Desktop-Symbol
auf dem Pi) brauchen kein Passwort (MLL_LOCAL_NO_PASSWORD=0 schaltet das ab). Das Passwort wird im Klartext ueber das Netz
gesendet (kein https): fuer das Heimnetz gedacht, nicht fuer das Internet.
"""
from __future__ import annotations

import base64
import logging

from _web import web_password

logger = logging.getLogger(__name__)


class BasicAuthMiddleware:
    LOCAL = ("127.0.0.1", "::1", "localhost", "::ffff:127.0.0.1")

    def __init__(self, app, realm: str = "webMobaLedLib", allow_local: bool = True):
        self.app = app
        self.allow_local = allow_local                       # Zugriffe vom Rechner selbst (Desktop-Symbol) brauchen kein Passwort
        self.realm = realm
        self._ok_cache: dict = {}                            # Authorization-Kopfzeile -> Zustand des Passworts, als sie geprueft wurde

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

    def _is_local(self, scope) -> bool:
        client = scope.get("client")
        return bool(self.allow_local and client and client[0] in self.LOCAL)

    async def __call__(self, scope, receive, send):
        if (scope["type"] not in ("http", "websocket") or not web_password.auth_required()
                or self._is_local(scope) or self._ok(scope)):
            await self.app(scope, receive, send)
            return
        if scope["type"] == "websocket":
            await send({"type": "websocket.close", "code": 1008})
            return
        body = "Anmeldung erforderlich".encode("utf-8")
        await send({"type": "http.response.start", "status": 401, "headers": [
            (b"www-authenticate", f'Basic realm="{self.realm}", charset="UTF-8"'.encode("ascii")),
            (b"content-type", b"text/plain; charset=utf-8"), (b"content-length", str(len(body)).encode("ascii"))]})
        await send({"type": "http.response.body", "body": body})


def install(app, allow_local: bool = True):
    """Middleware in die FastAPI-/NiceGUI-App einhaengen (prueft nur, wenn ein Passwort eingerichtet ist)"""
    app.add_middleware(BasicAuthMiddleware, allow_local=allow_local)
    logger.info("Passwortschutz eingehaengt (Passwort eingerichtet: %s, localhost ohne Passwort: %s)", web_password.auth_required(), allow_local)
