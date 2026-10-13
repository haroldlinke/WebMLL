# Datei-Version: 1.00 (2026-10-13) - web_access.py
"""Zusatzfelder der Seite Programm Einstellungen: Passwort fuer den Zugriff auf die Web-Oberflaeche aus dem Netz aendern.

Benutzt von web_params.build_settings_page(extra=...): build() baut die Felder, collect() liefert keine Einstellungen (das Passwort
wird nicht in der Konfiguration gespeichert, sondern mit eigenem Knopf als Hash in web_password.json)."""
from __future__ import annotations

import os

import web_password

LOCAL_HOSTS = ("127.0.0.1", "localhost", "::1")


class WebAccess:
    def __init__(self, ctrl=None):
        self.ctrl = ctrl
        self.new = self.again = self.status = self.warning = self.reset_btn = None

    def collect(self) -> dict:
        return {}

    def build(self):
        from nicegui import ui
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
