# Datei-Version: 1.04 (2026-10-15) - web_access.py
"""Zusatzfelder der Seite Programm Einstellungen: Passwort fuer den Zugriff auf die Web-Oberflaeche aus dem Netz aendern und (nur auf
dem Raspberry Pi mit installiertem Hilfsprogramm) den Namen des Rechners im Netz aendern.

Benutzt von web_params.build_settings_page(extra=...): build() baut die Felder, collect() liefert keine Einstellungen (das Passwort
wird nicht in der Konfiguration gespeichert, sondern mit eigenem Knopf als Hash in web_password.json)."""
from __future__ import annotations

import os
import platform
import re
import socket
import subprocess

from _web import web_dialogs as wd
from _web import web_password

LOCAL_HOSTS = ("127.0.0.1", "localhost", "::1")
HOSTNAME_HELPER = "/usr/local/sbin/mobaledlib-set-hostname"        # von install_pi.sh installiert (root, nicht veraenderbar)
HOSTNAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,30}$")


def hostname_error(name: str) -> str:
    """Fehlertext, wenn der Rechnername nicht erlaubt ist, sonst leerer Text (gleiche Regeln wie das Hilfsprogramm)"""
    if not name:
        return "Bitte einen Namen eingeben."
    if not HOSTNAME_RE.match(name) or name.endswith("-"):
        return "Erlaubt sind Buchstaben, Ziffern und Bindestrich (nicht am Anfang oder Ende), höchstens 31 Zeichen, keine Leerzeichen und Umlaute."
    return ""


def hostname_change_possible() -> bool:
    """Gibt es das Hilfsprogramm, und darf der Dienstbenutzer es ohne Passwort ueber sudo aufrufen?"""
    if platform.system() != "Linux" or not os.path.exists(HOSTNAME_HELPER):
        return False
    try:
        return subprocess.run(["sudo", "-n", "-l", HOSTNAME_HELPER, "x"], capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def run_hostname_helper(name: str):
    """(Erfolg, Meldung) - laeuft im Hintergrund-Thread"""
    try:
        r = subprocess.run(["sudo", "-n", HOSTNAME_HELPER, name], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as ex:
        return False, str(ex)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


class WebAccess:
    def __init__(self, ctrl=None):
        self.ctrl = ctrl
        self.layout = None
        self.table = None
        self.new = self.again = self.status = self.warning = self.reset_btn = None
        self.host_input = self.host_status = self.host_result = None

    def collect(self) -> dict:
        values = {}                                                               # Darstellung und Bedienung der Tabelle werden mit gespeichert
        for part in (self.layout, self.table):
            if part is not None:
                values.update(part.collect())
        return values

    def build(self):
        from nicegui import ui
        from _web import web_layout
        self.layout = web_layout.LayoutSetting(self.ctrl)
        self.layout.build()
        self.table = web_layout.TableSetting(self.ctrl)
        self.table.build()
        with ui.card().props("flat bordered").classes("w-full gap-2"):
            ui.label("Zugriff über das Netz (Web-Oberfläche)").classes("text-subtitle1").style("font-weight: 600")
            ui.label("Wird die Oberfläche von einem anderen Rechner im Netz aufgerufen (zum Beispiel beim Raspberry Pi), fragt der Browser "
                     "nach Benutzername und Passwort. Auf dem Rechner, auf dem das Programm läuft, ist kein Passwort nötig."
                     ).classes("text-caption text-grey-8")
            self.status = ui.label("")
            self.warning = ui.label("").classes("text-negative")
            with ui.row().classes("items-end gap-3 w-full"):
                self.new = ui.input("Neues Passwort", password=True, password_toggle_button=True).props("dense outlined").classes("w-64")
                self.again = ui.input("Neues Passwort wiederholen", password=True, password_toggle_button=True).props(
                    "dense outlined").classes("w-64")
                ui.button("Passwort ändern", on_click=self.change).props("color=primary no-caps")
                self.reset_btn = ui.button("Eigenes Passwort entfernen", on_click=self.reset).props("outline no-caps")
        self.refresh()
        if hostname_change_possible():
            self.build_hostname()

    def build_hostname(self):
        from nicegui import ui
        with ui.card().props("flat bordered").classes("w-full gap-2"):
            ui.label("Name des Raspberry Pi im Netz").classes("text-subtitle1").style("font-weight: 600")
            ui.label("Unter diesem Namen ist der Raspberry Pi im Netz erreichbar (zum Beispiel http://NAME.local:8080), ohne dass man seine "
                     "IP-Adresse kennen muss. Erlaubt sind Buchstaben, Ziffern und Bindestrich, höchstens 31 Zeichen."
                     ).classes("text-caption text-grey-8")
            self.host_status = ui.label("")
            with ui.row().classes("items-end gap-3 w-full"):
                self.host_input = ui.input("Neuer Name", value=socket.gethostname()).props("dense outlined").classes("w-64")
                ui.button("Namen ändern", on_click=self.change_host).props("color=primary no-caps")
            self.host_result = ui.column().classes("gap-1")
        self.refresh_host()

    def host_url(self, name: str) -> str:
        return f"http://{name}.local:{os.environ.get('MLL_PORT', '8080')}"

    def refresh_host(self):
        name = socket.gethostname()
        self.host_status.set_text(f"Aktueller Name: {name}   (Adresse im Netz: {self.host_url(name)})")

    async def change_host(self):
        from nicegui import run, ui
        name = str(self.host_input.value or "").strip()
        error = hostname_error(name)
        if error:
            ui.notify(error, type="warning")
            return
        if name == socket.gethostname():
            ui.notify("Der Raspberry Pi hat diesen Namen schon.", type="info")
            return
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
            ui.label("Namen des Raspberry Pi ändern?").classes("text-h6")
            ui.label(f"Der Raspberry Pi heißt danach „{name}“ und ist unter {self.host_url(name)} erreichbar. Die bisherige Adresse "
                     f"({self.host_url(socket.gethostname())}) gilt dann nicht mehr: Öffne die Oberfläche künftig mit der neuen Adresse.")
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen", on_click=lambda: dlg.submit(False)).props("flat").classes("mll-cancel")
                ui.button("Namen ändern", on_click=lambda: dlg.submit(True)).props("color=primary").classes("mll-default")
        answer = await dlg
        wd.safe_delete(dlg)
        if not answer:
            return
        ok, message = await run.io_bound(run_hostname_helper, name)
        self.host_result.clear()
        if not ok:
            ui.notify("Der Name konnte nicht geändert werden: " + (message or "unbekannter Fehler"), type="negative", timeout=15000)
            return
        ui.notify(f"Der Name ist jetzt {name}.", type="positive")
        self.refresh_host()
        with self.host_result:
            ui.label("Neue Adresse (in einem Lesezeichen oder dem Desktop-Symbol anpassen):").classes("text-caption")
            ui.link(self.host_url(name), self.host_url(name), new_tab=True)

    def refresh(self):
        user = web_password.username()
        if web_password.has_stored():
            text = f"Benutzername: {user}. Ein eigenes Passwort ist gesetzt."
        elif web_password.uses_default_password():
            text = f"Benutzername: {user}. Es gilt das Standardpasswort „{web_password.DEFAULT_PASSWORD}“."
        elif web_password.env_password():
            text = f"Benutzername: {user}. Es gilt das Passwort aus der Einstellungsdatei des Dienstes (MLL_PASSWORD)."
        else:
            text = "Es ist kein Passwort eingerichtet: Wer das Netz erreicht, kann die Oberfläche benutzen."
        self.status.set_text(text)
        host = os.environ.get("MLL_HOST", "127.0.0.1")
        warn = web_password.uses_default_password() and host not in LOCAL_HOSTS
        self.warning.set_text("Bitte ein eigenes Passwort setzen: Das Standardpasswort ist allgemein bekannt." if warn else "")
        self.reset_btn.set_visibility(web_password.has_stored())

    def change(self):
        from nicegui import ui
        error = web_password.validate_new(str(self.new.value or ""), str(self.again.value or ""))
        if error:
            ui.notify(error, type="warning")
            return
        web_password.set_password(str(self.new.value))
        self.new.set_value("")
        self.again.set_value("")
        ui.notify("Passwort geändert. Von einem anderen Rechner fragt der Browser beim nächsten Aufruf nach dem neuen Passwort.", type="positive")
        self.refresh()

    def reset(self):
        from nicegui import ui
        web_password.clear_password()
        ui.notify("Das eigene Passwort ist entfernt. Es gilt wieder die Voreinstellung.", type="info")
        self.refresh()
