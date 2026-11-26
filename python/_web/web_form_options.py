# Datei-Version: 1.76 (2026-11-26) - web_form_options.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_options.py
# Path:           _web/web_form_options.py
# Version:        1.76
# Last Update:    2026-11-26
# Author:         Harold Linke, Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.76  2026-11-26  Firmware installieren (Pico): der Anschluss wird mit der Geraeteauswahl der Lichtmaschine gewaehlt (web_form_comport 1.45, SelectPicoDevice) statt mit dem eigenen kleinen Dialog; nur Pico-Geraete, auch unbekannte und andere MobaLedLib Geraete sind waehlbar. Zeilen mit '# v1.76'
#   1.75  2026-11-26  Version 5.49 (Issue 75, Juergen): Menue Werkzeuge: die Reiter Entwicklungsumgebung und Update (Wartung) und Firmware Installation stehen nicht mehr in den Hardware Optionen, sondern oeffnen als eigene Fenster ueber Werkzeuge -> Wartung und Werkzeuge -> Firmware installieren (VIEW, Show(view=...))
#   1.74  2026-11-26  Wurde der COM Port der Lichtmaschine in der Hardwaresuche (Geraeteauswahl) geaendert, verbindet das Programm nach dem Schliessen der Optionen automatisch (Einstellung AutoConnect); eine Verbindung zum alten Anschluss wird vorher getrennt. Zeilen mit '# v1.74'
#   1.73  2026-11-26  Displaytyp: Liste nur mit '0,96"' und '1,3"', Standard 2 (0,96") wie in ESP32Extensions.h. Zeilen mit '# v1.73'
#   1.72  2026-11-26  ESP32: Auswahlfeld 'Displaytyp' (OLED_TYP 1 = 1,3 Zoll Adapterplatine, 2 = 0,96 Zoll Hauptplatine) neben 'Anzeige auf dem Display'; gespeichert in esp32_options['oled_typ']. Zeilen mit '# v1.72'
#   1.71  2026-11-25  Anzeige 'Lichtmaschine ... an -3 (offline)': eine negative Portnummer im Blatt (Excel-Kennzeichen fuer einen belegten Port) gilt als kein Port (auch bei Board und USB Port erkennen). Zeilen mit '# v1.71'
#   1.70  2026-11-25  Board-Erkennung ohne serielle Abfrage: Pico wird nur ueber die USB-Kennung erkannt, Servo-Module erkennt der Dialog im Hintergrund (schnelles Oeffnen). Zeilen mit '# v1.70'
#   1.18  2026-11-12  Excel-Programm 3.5.0L3: Der Knopf Firmware installieren steht fuer ALLE Boards im Reiter LED ARDUINO (vorher nur beim Raspberry Pi Pico und nur mit Firmware-Dateien im Ordner); der Firmware-Ordner wird bei Bedarf angelegt (fruehere Versionen ohne Eintrag)
#   1.19  2026-11-12  Excel-Programm 3.5.0L3: Firmware installieren oeffnet die Auswahl auch ohne Firmware-Dateien; der Knopf Firmware laden holt Firmware aus dem Internet (web_form_firmware_download, headless_firmware_dl) und waehlt sie danach vor
#   1.20  2026-11-12  Reiter LED ARDUINO: der Kommentar zum Knopf Firmware installieren steht unter dem Knopf (schmal) statt daneben; die Auswahl des Boards behaelt ihre Breite (keine umbrochenen Beschriftungen) und rutscht auf schmalen Bildschirmen unter die Knoepfe
#   1.21  2026-11-12  Knopf im Dialog Firmware installieren: 'Firmware herunterladen' (vorher 'Firmware laden')
#   1.22  2026-11-13  Schreibfehler im Titel: 'Optionen und spezielle Funktionen' (vorher 'Funktionien')
#   1.23  2026-11-13  Wechsel des Arduino-Typs (Optionen): eine bestehende serielle Verbindung wird getrennt und der gewaehlte COM Port zurueckgesetzt (_web_board_changed), damit beim naechsten Mal die Port-Erkennung startet ohne die Meldung 'Es ist kein ... angeschlossen' (Rueckmeldung des Excel-Entwicklers)
#   1.24  2026-11-14  Reiter OTA (nur bei Board ESP32): WLAN, OTA, Hostname, Adresse, Passwort (Beitrag des Fork-Entwicklers; web_esp32_ota.settings_panel)
#   1.28  2026-11-17  Knopf 'Board und USB Port erkennen' steht ueber 'USB Port erkennen'; Reiter 'LED Arduino' heisst 'Lichtmaschine', Reiter 'OTA' heisst 'WLAN (OTA)'
#   1.29  2026-11-18  Reiter Dateien: Knopf Importieren v. altem Prog. ist aktiv und zeigt eine Anleitung (Daten ueber eine MLL_pgf-Datei uebernehmen); Knopf Kopiere von Seite zu Seite entfaellt (ersetzt durch Seite duplizieren)
#   1.27  2026-11-17  Knopf 'Board und USB Port erkennen': stellt das erste gefundene Board ein und ruft USB Port erkennen auf (Formular mit gefundenem Board und Anschluss, dazu die anderen Boards); Anwender kann uebernehmen oder anderen Typ waehlen
#   1.26  2026-11-17  Erkennen ohne voreingestellten COM Port und Board: der Knopf durchsucht selbst alle seriellen Anschluesse (Classify_Port), fragt bei mehreren Geraeten nach und traegt Board und COM Port ein
#   1.25  2026-11-17  Reiter LED ARDUINO / DCC Arduino: statt des Hakens 'Automatisch erkennen' ein Knopf 'Erkennen' (erkennt das angeschlossene Board einmalig: Nano alt/neu ueber den Bootloader, ESP32, Pico); der Eintrag 'Typ von Arduino IDE benutzen' entfaellt (Vorschlag des Excel-Entwicklers)
#   1.30  2026-11-18  ESP Einstellungen je Blatt mit OLED-Vorschau, Reiternamen aus NiceGUI-Props (Beitrag von moosbewohner, Pull Request 11)
#   1.31  2026-11-18  Neuer Reiter Erweiterungen: bekannte MobaLedLib Extensions (MLX) mit Haken aktiv/inaktiv, Laden beim Einschalten (headless_extensions)
#   1.32  2026-11-18  Reiter Erweiterungen: eigene Erweiterungen (Eingabe Name, Name@=Version, Name=Adresse oder Adresse) mit Haken, Entfernen und Hinweis auf fremden Code
#   1.33  2026-11-18  Reiter des Optionenfensters: Beschriftung bricht um (zweizeilig) und die Reiter teilen die Breite, damit alle sichtbar sind (vorher Pfeile zum Blaettern, Reiter Erweiterungen verdeckt)
#   1.34  2026-11-18  Korrektur Issue 13: Board und USB Port erkennen nimmt nicht mehr blind den ersten Anschluss. Der Anschluss der anderen Seite (Lichtmaschine oder LNet/DCC-Arduino) wird ausgelassen, der eigene gespeicherte Anschluss hat Vorrang
#   1.35  2026-11-18  Korrektur Issue 13 (nach Protokoll): Board und USB Port erkennen setzt auch die Auswahl des Formulars (rb_res), sonst ueberschrieb 'USB Port erkennen' das erkannte Board wieder mit der alten Auswahl; nach dem Erkennen oeffnet das Fenster wieder auf dem Reiter der Seite (nicht auf Lichtmaschine)
#   1.36  2026-11-18  Board und USB Port erkennen (Lichtmaschine): nach dem Schliessen des Fensters verbindet das Programm automatisch (Hook wd._bridge['auto_connect'] aus webmobaledlib 4.04)
#   1.37  2026-11-19  Board und USB Port erkennen: Nano neu oder Full mit Firmware-Version und Signatur des Bootloaders (Issue 14)
#   1.39  2026-11-19  Automatisch verbinden nach Board und USB Port erkennen: der Browserbezug (client) wird mitgegeben, sonst Fehler 'The current slot cannot be determined' (Rueckmeldung Harold, 4.22)
#   1.38  2026-11-19  Erweiterungen: Name und Beschreibung aus libraries.json der Extension anzeigen, wenn vorhanden (Wunsch Juergen, Issue 6)
#   1.39  2026-11-19  Reiter Entwicklungsumgebung: Haken 'Schnelles Update: nur geaenderte Konfiguration uebertragen (ESP32/Pico)' (Einstellung serial_cfg, M42_Dyn_Config; Zeilen mit '# v1.32', die Texte mit '# v1.39')
#   1.40  2026-11-21  Version 4.52: Reiter Entwicklungsumgebung: Knopf ARDUINO-IDE Einstellungen (oeffnet das Fenster der Hauptseite); Reiter WLAN (OTA): Knopf ESP32-Firmware ueber WLAN hochladen
#   1.41  2026-11-21  Version 4.53: Erweiterungen sind ein eigenes Fenster (open_extensions_window, Schliessen) statt eines Reiters im Optionenfenster; ext_panel auf Modulebene
#   1.42  2026-11-21  Version 4.54: Reiter Dateien entfaellt (Importieren v. altem Prog. steht im Menue Datei); Fenster Erweiterungen: Hinweis, dass alle Aenderungen sofort wirksam sind
#   1.43  2026-11-21  Version 4.67: Reiter Bootloader heisst Firmware Installation; der Knopf Firmware installieren (mit Beschreibungstext) ist vom Reiter Lichtmaschine dorthin umgezogen
#   1.44  2026-11-22  Version 4.68: Titel Hardware Optionen; Reiter Entwicklungsumgebung und Firmware Installation nicht im Anfaenger Modus; Boardnamen Lichtmaschine Classic/Pro/Pico; PlatformIO (Standard) zuerst, ARDUINO-IDE (nur Kompatibilitaet), Knopf ARDUINO-IDE Einstellungen nur mit ARDUINO-IDE; Hinweis WLAN (OTA) zu Schnelles Update
#   1.45  2026-11-22  Version 4.70: Reiter Entwicklungsumgebung: roter Hinweis unter dem Haken Schnelles Update (nicht kompatibel mit WLAN)
#   1.46  2026-11-22  Version 4.71: Warnhinweise zu Schnelles Update und WLAN entfernt (Pull Request 54: Schnelles Update geht fuer den ESP32 jetzt auch ueber WLAN); neuer Hinweistext zum Schnellen Update (aus dem Pull Request, dort als 1.44)
#   1.69  2026-11-25  Board und USB Port erkennen: ein PicoServo-Tiny (Servo-Modul, antwortet auf '~MLLINFO') wird nicht als Board angeboten. Zeilen mit '# v1.69'
#   1.68  2026-11-25  Protokoll Selectrix wieder in der Liste (soweit SupportsSelectrix der Plattform true ist) und Wechsel zwischen Selectrix und DCC/LNet/CAN mit Umrechnung der Adressen
#                     (headless_protocol_switch): Rueckfrage, wenn das Blatt Adressen (keine Variablen) enthaelt; Rot/Gruen werden zu Taster. Zeilen mit '# v1.68'
#   1.67  2026-11-25  Die Auswahl der Protokolle richtet sich nach der Tabelle Platform_Parameters (SupportsDCC, SupportsLNet, SupportsCAN je Plattform AM328, ESP32, PICO;
#                     vorher fest: Pico nur DCC); ein eingestelltes, nicht unterstuetztes Protokoll bleibt sichtbar mit Hinweis. Zeilen mit '# v1.67'
#   1.66  2026-11-25  Anzeige auf dem Display: 'WLAN, IP, LDR und Zeit' und 'WLAN, IP und Hostname' nur, wenn WLAN am ESP32 eingeschaltet ist (folgt dem Haken im Reiter WLAN (OTA),
#                     sonst Aus); 'Hardwarevariante' statt 'Board-Variante'; Bild der Hardware 50 % groesser; Texte 'auf die/der Lichtmaschine' statt Arduino; Protokoll 'LNet' ohne den Begriff LocoNet (wie 5.25). Zeilen mit '# v1.66'
#   1.65  2026-11-25  Tooltip des Knopfes Erkennen: Protokoll wird nicht mehr im Dialog gewaehlt. Zeilen mit '# v1.65'
#   1.64  2026-11-25  Reiter DCC/LNet Arduino folgt dem Protokoll im Dialog: Beschriftung wechselt sofort, bei CAN ausgeblendet (der Reiter wird jetzt immer angelegt). Zeilen mit '# v1.64'
#   1.63  2026-11-25  Reiter links ausgerichtet; Knopf Erkennen unter der Hardware-Zeile; Haken heisst nur 'Schnelles Update' (Erklaerung im Tooltip). Zeilen mit '# v1.63'
#   1.62  2026-11-25  Reiter nur so breit wie ihre Beschriftung; Hardware-Zeile: 'Hardware:' fett, danach die gewaehlte Hardware; Knopf Suchen heisst Erkennen. Zeilen mit '# v1.62'
#   1.61  2026-11-25  Board-Variante: 'Nano (alter Bootloader)' und 'Nano (maximaler Speicher)' statt 'Nano Normal (old Bootloader)' und 'Nano (Full memory)'. Zeilen mit '# v1.61'
#   1.60  2026-11-25  Hardware-Zeile zeigt bei Classic nur 'Lichtmaschine Classic, Mini'; Board-Variante: Nano Normal (old Bootloader), Nano (neue Version), Nano (Full memory), Uno. Zeilen mit '# v1.60'
#   1.59  2026-11-25  Reiter Lichtmaschine kompakter: weniger Rand und Abstaende, Knopf Suchen dense, Protokoll und Board-Variante nebeneinander, Haken eng (dense), kleinere Display-Vorschau (esp_panel compact) und kleineres Bild. Zeilen mit '# v1.59'
#   1.58  2026-11-25  Selectrix wieder aus der Protokoll-Liste entfernt (kommt spaeter); Stand wie 1.56. Zeilen mit '# v1.58'
#   1.57  2026-11-25  (v1.58 entfallen) Protokoll Selectrix fuer Classic und Pro (ESP32) in der Liste; der Wechsel eines bestehenden Blattes zwischen Selectrix und DCC/LNet/CAN wird mit Hinweis abgewiesen (andere Spalten). Zeilen mit '# v1.57'
#   1.56  2026-11-25  Pico: Protokoll nur DCC (ein anderes eingestelltes Protokoll bleibt sichtbar mit Hinweis, damit es auf DCC umgestellt werden kann). Zeilen mit '# v1.56'
#   1.55  2026-11-25  Alle Einstellungen der Hauptseite stehen im Blatt: Lichtsensor und Schaltzustaende als Makrozeilen (#define READ_LDR, #define ENABLE_STORE_STATUS(), headless_sheet_settings), Schnelles Update je Blatt (M42 1.08), Display, Protokoll und Variante wie bisher. Zeilen mit '# v1.55'
#   1.54  2026-11-25  Hauptseite: Lichtsensor und 'Schaltzustaende speichern' (vorher Zustaende werden gespeichert) fuer alle Plattformen, nicht nur ESP32. Zeilen mit '# v1.54'
#   1.53  2026-11-25  Hauptseite: Display-Einstellung mit Vorschau (vorher Reiter ESP Einstellungen, der dann entfaellt), Namen 'Anzeige auf dem Display' / 'Vorschau des Displays' statt OLED; Schnelles Update ohne '(ESP32/Pico)'; Hinweis 'Kommunikationsmodus des Blattes' entfernt. Zeilen mit '# v1.53'
#   1.52  2026-11-25  Die ESP32-Haken 'Lichtsensor aktivieren' (vorher Fotowiderstand) und 'Zustaende werden gespeichert' sind vom Reiter ESP Einstellungen auf die Hauptseite (Einstellungen) umgezogen; die OLED-Vorschau liest den Haken Lichtsensor von dort. Zeilen mit '# v1.52'
#   1.51  2026-11-25  Reiter Lichtmaschine: Abschnitt heisst 'Einstellungen'; der Haken Schnelles Update (ESP32/Pico) ist vom Reiter Entwicklungsumgebung dorthin umgezogen (bleibt dort nur beim WLAN-Geraet). Zeilen mit '# v1.51'
#   1.49  2026-11-25  Reiter Lichtmaschine: keine Auswahl des Boards mehr, nur Anzeige von Board, Port und Bild; der Knopf Suchen oeffnet den Port-Dialog (web_form_comport), dort werden Board, Variante, Port und Protokoll gewaehlt. Nur das WLAN-Geraet behaelt die Auswahl. Zeilen mit '# v1.49'
#   1.48  2026-11-24  Pull Request 39 (Juergen, Issue 35), nur der Auswahldialog: Board und USB Port erkennen fragt bei mehreren gefundenen Board-Typen (Nano, ESP32, Pico) vorher nach dem gewuenschten Typ (_choose_detected_board_type). Der Umbau der Boardliste im Optionen-Dialog aus dem PR wurde nicht uebernommen. Zeilen mit '# v1.48'
#   1.47  2026-11-23  Issue 58: Firmware installieren (Pico): eigener Anschluss, immer erfragt (nicht der Anschluss des Blatts, dort haengt die Lichtmaschine); beim Start ungueltig; bei verbundener Lichtmaschine auf diesem Anschluss wird vorher getrennt
#   1.49  2026-11-24  Anzeigename MobaLedLib Studio statt webMobaLedLib in Texten der Oberflaeche. Zeilen mit '# v5.09'
#   1.50  2026-11-25  Tooltip des Knopfes Board und USB Port erkennen nach Pull Request 39 (Juergen): Lichtmaschine nennt Nano, ESP32, Pico und die Auswahl bei mehreren Modellen (linke Seite: light_machine_hint, rechte Seite: detect_hint); der Umbau der Boardliste aus dem PR bleibt aus (Dialog wird von Juergen neu gestaltet)
# ----------------------------------------------------------------------------------------------
"""Web-Ersatz fuer proggen/UserForm_Options.py (Optionen und spezielle Funktionen).

WebOptions erbt von CUserForm_Options. Die Handler des Originals (Port erkennen, Bootloader,
Bibliotheken aktualisieren ...) bleiben unveraendert und werden aus dem Browser heraus im Worker-Thread
aufgerufen. Ersetzt werden nur Show() und Hide():
  * Hide() merkt sich nur, dass der Handler den Dialog schliessen wollte.
  * Show() zeigt den Dialog im Browser. Wird Show() aus einem Handler aufgerufen (z. B. nach der
    Port-Erkennung), wird der Dialog nach dem Handler neu geoeffnet.
  * Boards und "Automatisch erkennen" werden beim Druck auf einen Knopf angewendet (im Original sofort).
Beschriftungen und Beschreibungstexte der Knoepfe werden aus dem Quelltext des Originals gelesen.

Noch nicht im Web verfuegbar (Dateidialoge im Original): Speichern/Laden/Kopieren/Importieren.
"""
from __future__ import annotations

import ast
import inspect
import logging
import os  # v1.10
import sys
import textwrap

from headless import headless_git as HG                          # Git finden und installieren (Windows, macOS, Linux: Texte)  # v1.15  # v1.15

from _web import web_dialogs as wd
try:  # v1.04
    from _web.web_i18n import tr  # v1.04
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v1.04
    def tr(text, **values):  # v1.04
        return text.format(**values) if values else text  # v1.04

logger = logging.getLogger(__name__)

NOT_IN_WEB: set = set()          # Speichern/Laden laufen jetzt ueber Browser-Download und -Upload (web_dialogs)


class Var:
    def __init__(self, v=0):
        self._v = v

    def get(self):
        return self._v

    def set(self, v):
        self._v = v


# ------------------------------------------------------------------ Quelltext des Originals auswerten
def _const(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _lang_arg(node):
    """M09.Get_Language_Str('...') -> Schluessel (sonst die Konstante selbst)."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "Get_Language_Str" and node.args:
        return _const(node.args[0])
    return _const(node)


def harvest_buttons(Base) -> dict:
    """Button_Setup(...)-Aufrufe aus __UserForm_Initialize/create_arduinopage:
    {Handlername: [{'text', 'label', 'disabled', 'row', 'frame'}, ...]}"""
    out: dict[str, list] = {}
    for fn in (Base.__dict__.get("_CUserForm_Options__UserForm_Initialize"), Base.__dict__.get("create_arduinopage")):
        if fn is None:
            continue
        tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "Button_Setup" \
                    and len(node.args) >= 3 and isinstance(node.args[2], ast.Attribute):
                handler = node.args[2].attr
                kw = {k.arg: k.value for k in node.keywords}
                entry = {"text": _lang_arg(node.args[1]) or handler,
                         "label": _const(kw["label_text"]) if "label_text" in kw else "",
                         "disabled": "state" in kw and "DISABLED" in ast.dump(kw["state"]),
                         "row": kw["Row"].value if "Row" in kw and isinstance(kw["Row"], ast.Constant) else 0,
                         "frame": node.args[0].id if isinstance(node.args[0], ast.Name) else ""}
                out.setdefault(handler, []).append(entry)
    return out


def _choose_detected_board_type(cands, *, light_machine):  # v1.48 (Pull Request 39, Juergen)
    """Bei mehreren gefundenen Board-Typen (Nano, ESP32, Pico) den gewuenschten Typ waehlen lassen. cands: [(Anschluss, Typ)]. Rueckgabe: Typ oder None (Abbrechen)"""  # v1.48
    types = [typ for typ in ("Nano", "ESP32", "Pico") if any(candidate_type == typ for _, candidate_type in cands)]  # v1.48
    if len(types) <= 1:  # v1.48
        return types[0] if types else None  # v1.48

    labels = {  # v1.48
        "Nano": tr("Arduino Nano (Typ wird automatisch erkannt)"),  # v1.48
        "ESP32": "ESP32",  # v1.48
        "Pico": tr("Raspberry Pi Pico"),  # v1.48
    }  # v1.48
    options = {  # v1.48
        typ: f"{labels[typ]} ({', '.join(dev for dev, candidate_type in cands if candidate_type == typ)})"  # v1.48
        for typ in types  # v1.48
    }  # v1.48

    async def show_dialog():  # v1.48
        from nicegui import ui  # v1.48
        with wd._bridge["client"]:  # v1.48
            with ui.dialog().props("persistent") as dlg, ui.card().classes("min-w-[380px] max-w-[640px]"):  # v1.48
                title = tr("Unterschiedliche Lichtmaschinen-Modelle gefunden") if light_machine else tr("Mehrere Board-Typen gefunden")  # v1.48
                prompt = tr("Bitte wählen Sie das gewünschte Modell aus:") if light_machine else tr("Bitte wählen Sie den gewünschten Board-Typ aus:")  # v1.48
                ui.label(title).classes("text-h6")  # v1.48
                ui.label(prompt)  # v1.48
                choice = ui.radio(options, value=None).props("dense")  # v1.48
                with ui.row().classes("justify-end w-full"):  # v1.48
                    ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(None)).props("outline").classes("mll-cancel")  # v1.48
                    confirm = ui.button("OK", on_click=lambda: dlg.submit(choice.value)).classes("mll-default")  # v1.48
                    confirm.disable()  # v1.48
                    choice.on_value_change(lambda event: confirm.enable() if event.value in types else confirm.disable())  # v1.48
            result = await dlg  # v1.48
            wd.safe_delete(dlg)  # v1.48
        return result  # v1.48

    selected = wd.call_in_loop(show_dialog, default=None)  # v1.48
    return selected if selected in types else None  # v1.48


def tab_buttons(buttons: dict, handlers: list[str], frame_hint: str | None = None) -> list[dict]:
    res = []
    for h in handlers:
        for e in buttons.get(h, [])[:1]:
            res.append(dict(e, handler=h))
    return res


# ------------------------------------------------------------------ Dialog (Event-Loop)
arduino_settings_handler = None  # v1.40: Funktion der Hauptseite (webmobaledlib.py): Fenster ARDUINO-IDE Einstellungen
ota_upload_handler = None  # v1.40: Funktion der Hauptseite: Fenster ESP32-Firmware ueber WLAN hochladen
_FW_PORT = {"port": ""}  # v1.47 (Issue 58): Anschluss fuer die Firmware-Installation des Pico: eigener Wert, beim Start des Programms ungueltig, unabhaengig vom Blatt und der Lichtmaschine


async def _pick_fw_port_async(ports, connected, stored, title, texts):  # v1.47 (Issue 58)
    """Auswahl des Pico-Anschlusses fuer die Firmware: ports = Liste der Pico-Anschluesse, connected = Anschluss der verbundenen Lichtmaschine (oder ''), stored = zuletzt gewaehlter. Rueckgabe: Anschluss oder None (Abbrechen)."""  # v1.47
    from nicegui import ui  # v1.47
    client = wd._bridge["client"]  # v1.47
    options = {p: (p + (" " + texts["connected"] if connected and p.upper() == connected.upper() else "")) for p in ports}  # v1.47
    free = [p for p in ports if not (connected and p.upper() == connected.upper())]  # v1.47
    start = stored if stored in ports else (free[0] if free else ports[0])  # v1.47
    with client:  # v1.47
        with ui.dialog().props("persistent") as dlg, ui.card().classes("min-w-[380px] max-w-[640px]"):  # v1.47
            ui.label(title).classes("text-h6")  # v1.47
            ui.label(texts["info"]).style("white-space: pre-line")  # v1.47
            sel = ui.select(options, value=start, label=texts["label"]).classes("w-full")  # v1.47
            with ui.row().classes("justify-end w-full"):  # v1.47
                ui.button("OK", on_click=lambda: dlg.submit(sel.value)).classes("mll-default")  # v1.47
                ui.button(texts["cancel"], on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")  # v1.47
        result = await dlg  # v1.47
        wd.safe_delete(dlg)  # v1.47
    return result  # v1.47


VIEW = {"only": None}  # v1.75: None = Hardware Optionen; "wartung" = Reiter Entwicklungsumgebung und Update, "firmware" = Reiter Firmware Installation (Menue Werkzeuge)
_TAB = {"name": None, "keep": False}  # v1.35: zuletzt gewaehlter Reiter; keep: beim naechsten Oeffnen wieder dort beginnen (nach Board erkennen)

def ext_panel(vals):  # v1.41 (vorher in _options_async, Reiter Erweiterungen)  # v1.31  # v1.32
    from nicegui import ui  # v1.41
    import headless.headless_extensions as HE  # v1.31
    from nicegui import run  # v1.31
    ui.label(tr("MobaLedLib Extensions (MLX) erweitern die Makros um zusätzliche Funktionen. Sie sind optional, manche brauchen Zusatzhardware. Eine eingeschaltete Erweiterung erscheint in der Makroauswahl in der Gruppe „Erweiterungen“.")).classes("text-grey-8").style("white-space: pre-line")  # v1.31
    ui.label(tr("Alle Änderungen werden sofort wirksam, du musst nichts speichern.")).classes("text-body2 text-weight-medium")  # v1.42
    state = {"busy": False}  # v1.31
    holder = ui.column().classes("w-full gap-1")  # v1.32

    def status_text(ent):  # v1.31
        st_ = HE.status(ent)  # v1.31
        return {"bundled": tr("im Programmpaket"), "loaded": tr("geladen"), "missing": tr("noch nicht geladen")}[st_]  # v1.31

    async def confirm_foreign_code(spec):  # v1.32
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[520px] max-w-full"):  # v1.32
            ui.label(tr("Fremden Code einbinden?")).classes("text-h6")  # v1.32
            # ui.label(tr("Die Erweiterung {spec} wird aus dem Internet geladen. Ihr Code wird beim Übersetzen in Ihr Programm eingebunden und auf dem Arduino ausgeführt. Fügen Sie nur Erweiterungen aus Quellen hinzu, denen Sie vertrauen.", spec=spec)).style("white-space: pre-line")  # v1.32  # v1.66 (entfallen)
            ui.label(tr("Die Erweiterung {spec} wird aus dem Internet geladen. Ihr Code wird beim Übersetzen in Ihr Programm eingebunden und auf der Lichtmaschine ausgeführt. Fügen Sie nur Erweiterungen aus Quellen hinzu, denen Sie vertrauen.", spec=spec)).style("white-space: pre-line")  # v1.32  # v1.66: Lichtmaschine statt Arduino
            with ui.row().classes("justify-end w-full"):  # v1.32
                ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(False)).props("flat")  # v1.32
                ui.button(tr("Hinzufügen"), on_click=lambda: dlg.submit(True)).props("color=primary")  # v1.32
        dlg.open()  # v1.32
        answer = await dlg  # v1.32
        dlg.delete()  # v1.32
        return bool(answer)  # v1.32

    def render():  # v1.32: die Liste neu aufbauen (nach Hinzufügen oder Entfernen)
        holder.clear()  # v1.32
        with holder:  # v1.32
            for group, title in (("standard", tr("Standard (vorab eingeschaltet)")), ("optional", tr("Optional (vorab ausgeschaltet)")), ("custom", tr("Eigene Erweiterungen"))):  # v1.32
                entries = [e_ for e_ in HE.all_entries() if e_.get("group") == group]  # v1.32
                if not entries:  # v1.32
                    continue  # v1.32
                ui.label(title).classes("text-subtitle2 q-mt-sm")  # v1.31
                for ent in entries:  # v1.31
                    with ui.row().classes("items-start no-wrap w-full"):  # v1.31
                        lib_info = HE.library_info(ent)  # v1.38: Name und Beschreibung aus libraries.json, wenn vorhanden
                        # box = ui.checkbox(ent["name"], value=HE.is_enabled(ent["id"])).classes("w-72")  # v1.31  # v1.38 (entfallen)
                        box = ui.checkbox(lib_info.get("name") or ent["name"], value=HE.is_enabled(ent["id"])).classes("w-72")  # v1.38
                        with ui.column().classes("gap-0 grow"):  # v1.31
                            info = ui.label(status_text(ent)).classes("text-caption")  # v1.31
                            # ui.label(ent.get("description", "")).classes("text-caption text-grey-8")  # v1.31  # v1.38 (entfallen)
                            ui.label(lib_info.get("description") or ent.get("description", "")).classes("text-caption text-grey-8")  # v1.38
                            if ent.get("hardware"):  # v1.31
                                ui.label(tr("Braucht Zusatzhardware: {hardware}", hardware=ent["hardware"])).classes("text-caption text-orange-9")  # v1.31
                        if group == "custom":  # v1.32
                            def remove(ent=ent):  # v1.32
                                HE.remove_custom(ent["id"])  # v1.32
                                vals["ext_changed"] = True  # v1.32
                                render()  # v1.32
                            ui.button(tr("Entfernen"), on_click=remove).props("flat dense no-caps color=negative")  # v1.32

                    async def toggled(event, ent=ent, box=box, info=info):  # v1.31
                        if state["busy"]:  # v1.31
                            return  # v1.31
                        if event.value and HE.status(ent) == "missing":  # v1.31: erst laden, dann einschalten
                            state["busy"] = True  # v1.31
                            info.set_text(tr("wird geladen …"))  # v1.31
                            try:  # v1.31
                                await run.io_bound(HE.download, ent)  # v1.31
                            except HE.ExtensionError as ex:  # v1.31
                                ui.notify(tr("Die Erweiterung {name} konnte nicht geladen werden: {fehler}", name=ent["id"], fehler=ex), type="negative")  # v1.31
                                state["busy"] = False  # v1.32
                                box.set_value(False)  # v1.31
                                info.set_text(status_text(ent))  # v1.31
                                return  # v1.31
                            state["busy"] = False  # v1.31
                        HE.set_enabled(ent["id"], bool(event.value))  # v1.31
                        info.set_text(status_text(ent))  # v1.31
                        vals["ext_changed"] = True  # v1.31
                    box.on_value_change(toggled)  # v1.31
            ui.label(tr("Eigene Erweiterung hinzufügen")).classes("text-subtitle2 q-mt-md")  # v1.32
            with ui.row().classes("items-center no-wrap w-full"):  # v1.32
                spec_input = ui.input(placeholder="MeineNeueExtensionMLX=https://github.com/…").props("outlined dense clearable").classes("grow")  # v1.32

                async def add():  # v1.32
                    if state["busy"]:  # v1.32
                        return  # v1.32
                    try:  # v1.32
                        parsed = HE.parse_spec(spec_input.value)  # v1.32
                    except HE.ExtensionError as ex:  # v1.32
                        ui.notify(tr(str(ex)), type="negative")  # v1.32
                        return  # v1.32
                    if parsed["kind"] == "url" and not HE.warned():  # v1.32: beim ersten Hinzufügen einer Adresse
                        if not await confirm_foreign_code(parsed["spec"]):  # v1.32
                            return  # v1.32
                        HE.set_warned()  # v1.32
                    state["busy"] = True  # v1.32
                    ui.notify(tr("wird geladen …"))  # v1.32
                    try:  # v1.32
                        await run.io_bound(HE.add_custom, parsed["spec"])  # v1.32
                    except HE.ExtensionError as ex:  # v1.32
                        state["busy"] = False  # v1.32
                        ui.notify(tr("Die Erweiterung {name} konnte nicht geladen werden: {fehler}", name=parsed["id"], fehler=ex), type="negative")  # v1.32
                        return  # v1.32
                    state["busy"] = False  # v1.32
                    vals["ext_changed"] = True  # v1.32
                    render()  # v1.32
                ui.button(tr("Hinzufügen"), on_click=add).props("outline no-caps")  # v1.32
            ui.label(tr("Eine Zeile: Name (aktuelle Version aus der PlatformIO-Registry), Name@=1.1.0 (genau diese Version), Name=https://github.com/Besitzer/Repo (Code aus dem Repository, nach # ein Tag oder Zweig) oder nur die Adresse.")).classes("text-caption text-grey-8")  # v1.32
    render()  # v1.32


async def open_extensions_window():  # v1.41
    """Eigenes Fenster Erweiterungen (Menue Einstellungen): wie der fruehere Reiter, die Haken wirken sofort; nur Schliessen. Danach werden die Makros neu eingelesen, wenn sich etwas geaendert hat"""  # v1.41
    from nicegui import ui, run  # v1.41
    state = {}  # v1.41
    with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full").style("max-height: 96vh; overflow-y: auto"):  # v1.41
        ui.label(tr("Erweiterungen")).classes("text-h6")  # v1.41
        ext_panel(state)  # v1.41
        with ui.row().classes("justify-end w-full"):  # v1.41
            ui.button(tr("Schließen"), on_click=lambda: dlg.submit(True)).props("color=primary no-caps").classes("mll-default mll-cancel")  # v1.41
    await dlg  # v1.41
    wd.safe_delete(dlg)  # v1.41
    if state.get("ext_changed"):  # v1.41: Erweiterungen ein- oder ausgeschaltet: die Makros neu einlesen (wie vorher beim Schliessen der Optionen)
        try:  # v1.41
            import proggen.M38_Extensions as M38  # v1.41
            await run.io_bound(M38.Load_Extensions)  # v1.41
        except Exception:                                      # noqa: BLE001  # v1.41
            logger.exception("Erweiterungen konnten nicht neu eingelesen werden")  # v1.41


async def _options_async(spec: dict, st: dict):
    from nicegui import ui
    from _web.web_esp32_ota import settings_panel
    vals = dict(st)

    with wd._bridge["client"]:
        # with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full"):  # v1.12 (entfallen)
        # with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full").style("max-height: 96vh; overflow-y: auto"):    # auf kleinen Bildschirmen (Laptop) scrollen, sonst fehlen die unteren Boards (Pico)  # v1.14 (entfallen)
        # ui.add_css(".mll-opttabs .q-tab { flex: 1 1 auto; min-width: 0; padding: 0 6px; }"                                     # v1.33  # v1.62 (entfallen)
        ui.add_css(".mll-opttabs .q-tab { flex: 0 1 auto; min-width: 0; padding: 0 10px; min-height: 36px; }"                    # v1.33  # v1.62: Reiter nur so breit wie ihre Beschriftung
                   ".mll-opttabs .q-tab__label { white-space: normal; text-align: center; line-height: 1.15; font-size: 0.78rem; overflow-wrap: anywhere; }"  # v1.33
                   ".mll-opttabs .q-tabs__content { flex-wrap: nowrap; }")  # v1.33: lange Beschriftungen zweizeilig, alle Reiter sichtbar (ESP Einstellungen, Erweiterungen)
        ui.add_css(".mll-optcard .mll-hw-panel.q-tab-panel { padding: 8px 4px; }")  # v1.59: Reiter Lichtmaschine kompakter
        ui.add_css(".mll-optcard > * { flex-shrink: 0; }")       # die Karte ist eine Spalte (flex): ohne das schrumpfen die Reiter und schneiden die unteren Knoepfe und Texte ab  # v1.14
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full mll-optcard").style("max-height: 96vh; overflow-y: auto"):    # auf kleinen Bildschirmen (Laptop) scrollen, sonst fehlen die unteren Boards (Pico)  # v1.14
            ui.label(spec["title"]).classes("text-h6")

            def collect():
                return dict(vals)

            def action(handler):
                return lambda: dlg.submit(("action", handler, collect()))

            # The options are committed by the same OK/action flow as the board selection.  # v1.30
            esp_settings = dict(vals.get("esp32_options") or {})  # v1.30
            modes = {  # v1.30
                0: tr("Aus"), 1: tr("MLL-Zeit"), 2: tr("LDR-Wert"),  # v1.30
                3: tr("MLL-Zeit und LDR-Wert"), 4: tr("WLAN, IP, LDR und Zeit"),  # v1.30
                5: tr("WLAN, IP und Hostname"),  # v1.30
            }  # v1.30
            wifi_state = {"apply": None}  # v1.66: die Anzeigen mit WLAN (4, 5) gibt es nur, wenn WLAN am ESP32 eingeschaltet ist (Haken im Reiter WLAN (OTA))

            def shown_modes():  # v1.66
                return {k: v for k, v in modes.items() if vals.get("esp32_wifi") or k not in (4, 5)}  # v1.66

            def esp_panel(compact=False):  # v1.30  # v1.59: compact (Hauptseite): kleinere Vorschau
                with ui.row().classes("items-start " + ("gap-3 no-wrap" if compact else "gap-6")):  # v1.30  # v1.59
                    with ui.column():  # v1.30
                        # mode = ui.select(modes, value=esp_settings.get("oled", 0), label=tr("Anzeige auf dem Display")).props("outlined dense" if compact else "").classes("w-56" if compact else "w-64")  # v1.30  # v1.53: verstaendlicher Name statt OLED-Anzeige  # v1.66 (entfallen)
                        start_mode = esp_settings.get("oled", 0) if esp_settings.get("oled", 0) in shown_modes() else 0  # v1.66: ohne WLAN keine WLAN-Anzeige
                        mode = ui.select(shown_modes(), value=start_mode, label=tr("Anzeige auf dem Display")).props("outlined dense" if compact else "").classes("w-56" if compact else "w-64")  # v1.30  # v1.53  # v1.66: nur die Anzeigen, die zum WLAN passen
                        oled_types = {2: '0,96"', 1: '1,3"'}  # v1.72: OLED_TYP der Firmware (ESP32Extensions.h); v1.73: nur die Groesse, ohne Uebersetzung
                        OLED_TYP_DEFAULT = 2  # v1.73: wie in ESP32Extensions.h (#define OLED_TYP 2 = 0,96" an der ESP32-Hauptplatine)
                        start_typ = esp_settings.get("oled_typ", OLED_TYP_DEFAULT) if esp_settings.get("oled_typ", OLED_TYP_DEFAULT) in oled_types else OLED_TYP_DEFAULT  # v1.72  # v1.73
                        oled_typ = ui.select(oled_types, value=start_typ, label=tr("Displaytyp")).props("outlined dense" if compact else "").classes("w-56" if compact else "w-64")  # v1.72
                        # ldr/store (Lichtsensor, Zustaende speichern) stehen jetzt auf der Hauptseite (Einstellungen)  # v1.52
                    with ui.column().classes("items-center gap-0" if compact else "items-center gap-1"):  # v1.30  # v1.59
                        if not compact:  # v1.59: auf der Hauptseite steht die Ueberschrift als Tooltip
                            ui.label(tr("Vorschau des Displays")).classes("text-caption")  # v1.30  # v1.53
                        size = ("width:176px; height:88px; padding:4px; font: 10px/19px monospace; " if compact else  # v1.59
                                "width:256px; height:128px; padding:8px; font: 15px/27px monospace; ")  # v1.30
                        display = ui.label().style(  # v1.30
                            size + "max-width:100%; "  # v1.30  # v1.59
                            "background:#0c151b; color:#8edaff; white-space:pre; overflow:hidden; "  # v1.30
                            "text-align:center; border-radius:6px"  # v1.30  # v1.59
                        )  # v1.30
                        if compact:  # v1.59
                            display.tooltip(tr("Vorschau des Displays"))  # v1.59

                frame = 0  # v1.30

                def preview():  # v1.30
                    minutes = 18 * 60 + frame % 60  # v1.30
                    clock = f"{minutes // 60:02d}:{minutes % 60:02d}"  # v1.30
                    sensor = f"LDR: {110 + frame % 30}" if vals.get("ldr") else "LDR: aus"  # v1.30  # v1.52  # v1.55
                    hostname = vals["esp32_hostname"]  # v1.30
                    # The firmware uses a smaller font when a long hostname needs two lines.  # v1.30
                    split = 18 if len(hostname) <= 36 else 32  # v1.30
                    host_lines = [hostname[:split], hostname[split:]]  # v1.30
                    connected = vals["esp32_wifi"] and frame % 12 >= 2  # v1.30
                    status = "WLAN verbunden" if connected else (  # v1.30
                        "WLAN getrennt" if vals["esp32_wifi"] else "WLAN deaktiviert"  # v1.30
                    )  # v1.30
                    address = "192.168.1.42" if connected else "IP: -"  # v1.30
                    lines = {  # v1.30
                        0: [], 1: ["MobaLedLib", "Zeit", clock],  # v1.30
                        2: ["MobaLedLib", "LDR SunSet", sensor],  # v1.30
                        3: ["MobaLedLib", f"PM {clock}", sensor],  # v1.30
                        4: [status, address, sensor, f"MLL-Zeit: {clock}"],  # v1.30
                        5: [status, address, *host_lines],  # v1.30
                    }  # v1.30
                    big, small = ("10px", "7px") if compact else ("15px", "11px")  # v1.59
                    display.style("font-size: " + (small if mode.value == 5 and split == 32 else big))  # v1.30  # v1.59
                    display.set_text("\n".join(lines[mode.value]))  # v1.30

                def tick():  # v1.30
                    nonlocal frame  # v1.30
                    # if tabs.value == esp_tab.name:  # v1.30 (entfallen: ui.tab hat kein Attribut name)
                    if tabs.value in (esp_tab.props["name"], tab_objs[0].props["name"]):  # v1.30  # v1.53: auch auf der Hauptseite (Lichtmaschine)
                        frame += 1  # v1.30
                        preview()  # v1.30

                def update(_event):  # v1.30
                    vals["esp32_options"] = {**vals["esp32_options"], "oled": mode.value, "oled_typ": oled_typ.value}  # v1.30  # v1.52: ldr und store setzt die Hauptseite  # v1.72: Displaytyp
                    preview()  # v1.30

                for control in (mode, oled_typ):  # v1.30  # v1.52  # v1.72: Displaytyp
                    control.on_value_change(update)  # v1.30

                def apply_wifi(on):  # v1.66: Haken 'WLAN am ESP32 aktivieren' geaendert: Auswahl anpassen
                    vals["esp32_wifi"] = bool(on)  # v1.66
                    mode.set_options(shown_modes(), value=mode.value if mode.value in shown_modes() else 0)  # v1.66
                    preview()  # v1.66
                wifi_state["apply"] = apply_wifi  # v1.66
                if mode.value != esp_settings.get("oled", 0):  # v1.66: WLAN-Anzeige ohne WLAN wurde auf Aus gestellt
                    vals["esp32_options"] = {**vals["esp32_options"], "oled": mode.value}  # v1.66
                preview()  # v1.30
                ui.timer(1, tick)  # v1.30

            # def ext_panel():  # v1.31  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # import headless.headless_extensions as HE  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # from nicegui import run  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("MobaLedLib Extensions (MLX) erweitern die Makros um zusätzliche Funktionen. Sie sind optional, manche brauchen Zusatzhardware. Eine eingeschaltete Erweiterung erscheint in der Makroauswahl in der Gruppe „Erweiterungen“.")).classes("text-grey-8").style("white-space: pre-line")  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state = {"busy": False}  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # holder = ui.column().classes("w-full gap-1")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # def status_text(ent):  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # st_ = HE.status(ent)  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return {"bundled": tr("im Programmpaket"), "loaded": tr("geladen"), "missing": tr("noch nicht geladen")}[st_]  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # async def confirm_foreign_code(spec):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[520px] max-w-full"):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("Fremden Code einbinden?")).classes("text-h6")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("Die Erweiterung {spec} wird aus dem Internet geladen. Ihr Code wird beim Übersetzen in Ihr Programm eingebunden und auf dem Arduino ausgeführt. Fügen Sie nur Erweiterungen aus Quellen hinzu, denen Sie vertrauen.", spec=spec)).style("white-space: pre-line")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with ui.row().classes("justify-end w-full"):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(False)).props("flat")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.button(tr("Hinzufügen"), on_click=lambda: dlg.submit(True)).props("color=primary")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # dlg.open()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # answer = await dlg  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # dlg.delete()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return bool(answer)  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # def render():  # v1.32: die Liste neu aufbauen (nach Hinzufügen oder Entfernen)  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # holder.clear()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with holder:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # for group, title in (("standard", tr("Standard (vorab eingeschaltet)")), ("optional", tr("Optional (vorab ausgeschaltet)")), ("custom", tr("Eigene Erweiterungen"))):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # entries = [e_ for e_ in HE.all_entries() if e_.get("group") == group]  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if not entries:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # continue  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(title).classes("text-subtitle2 q-mt-sm")  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # for ent in entries:  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with ui.row().classes("items-start no-wrap w-full"):  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # lib_info = HE.library_info(ent)  # v1.38: Name und Beschreibung aus libraries.json, wenn vorhanden  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # # box = ui.checkbox(ent["name"], value=HE.is_enabled(ent["id"])).classes("w-72")  # v1.31  # v1.38 (entfallen)  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # box = ui.checkbox(lib_info.get("name") or ent["name"], value=HE.is_enabled(ent["id"])).classes("w-72")  # v1.38  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with ui.column().classes("gap-0 grow"):  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # info = ui.label(status_text(ent)).classes("text-caption")  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # # ui.label(ent.get("description", "")).classes("text-caption text-grey-8")  # v1.31  # v1.38 (entfallen)  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(lib_info.get("description") or ent.get("description", "")).classes("text-caption text-grey-8")  # v1.38  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if ent.get("hardware"):  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("Braucht Zusatzhardware: {hardware}", hardware=ent["hardware"])).classes("text-caption text-orange-9")  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if group == "custom":  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # def remove(ent=ent):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # HE.remove_custom(ent["id"])  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # vals["ext_changed"] = True  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # render()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.button(tr("Entfernen"), on_click=remove).props("flat dense no-caps color=negative")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # async def toggled(event, ent=ent, box=box, info=info):  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if state["busy"]:  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if event.value and HE.status(ent) == "missing":  # v1.31: erst laden, dann einschalten  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = True  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # info.set_text(tr("wird geladen …"))  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # try:  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # await run.io_bound(HE.download, ent)  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # except HE.ExtensionError as ex:  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.notify(tr("Die Erweiterung {name} konnte nicht geladen werden: {fehler}", name=ent["id"], fehler=ex), type="negative")  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = False  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # box.set_value(False)  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # info.set_text(status_text(ent))  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = False  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # HE.set_enabled(ent["id"], bool(event.value))  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # info.set_text(status_text(ent))  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # vals["ext_changed"] = True  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # box.on_value_change(toggled)  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("Eigene Erweiterung hinzufügen")).classes("text-subtitle2 q-mt-md")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with ui.row().classes("items-center no-wrap w-full"):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # spec_input = ui.input(placeholder="MeineNeueExtensionMLX=https://github.com/…").props("outlined dense clearable").classes("grow")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # async def add():  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if state["busy"]:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # try:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # parsed = HE.parse_spec(spec_input.value)  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # except HE.ExtensionError as ex:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.notify(tr(str(ex)), type="negative")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if parsed["kind"] == "url" and not HE.warned():  # v1.32: beim ersten Hinzufügen einer Adresse  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if not await confirm_foreign_code(parsed["spec"]):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # HE.set_warned()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = True  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.notify(tr("wird geladen …"))  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # try:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # await run.io_bound(HE.add_custom, parsed["spec"])  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # except HE.ExtensionError as ex:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = False  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.notify(tr("Die Erweiterung {name} konnte nicht geladen werden: {fehler}", name=parsed["id"], fehler=ex), type="negative")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = False  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # vals["ext_changed"] = True  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # render()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.button(tr("Hinzufügen"), on_click=add).props("outline no-caps")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("Eine Zeile: Name (aktuelle Version aus der PlatformIO-Registry), Name@=1.1.0 (genau diese Version), Name=https://github.com/Besitzer/Repo (Code aus dem Repository, nach # ein Tag oder Zweig) oder nur die Adresse.")).classes("text-caption text-grey-8")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # render()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # (ext_panel steht jetzt auf Modulebene, siehe oben)  # v1.41

            pico_rows = []                                             # Knoepfe nur fuer den Pico (Firmware installieren)  # v1.09
            pico_values = list(spec["pages"]["left"].get("pico_values") or [])  # v1.09
            fw_avail = bool(spec["pages"]["left"].get("firmware_available"))        # nur mit mindestens einer *.uf2 im Ordner MobaLedLib/firmware  # v1.11

            def update_pico_buttons():  # v1.09
                # show = vals.get("L") in pico_values  # v1.11 (entfallen)
                show = vals.get("L") in pico_values and fw_avail  # v1.11
                for r_ in pico_rows:  # v1.09
                    r_.set_visibility(show)  # v1.09

            def button_row(b, compact=False):  # v1.20: compact (Reiter LED ARDUINO): der Kommentar steht unter dem Knopf, nicht daneben (er nahm der Auswahl des Boards den Platz)
                # with ui.row().classes("items-center w-full no-wrap"):  # v1.09 (entfallen)
                if compact:  # v1.20
                    with ui.column().classes("gap-0") as row_el:  # v1.20
                        btn = ui.button(wd.clean_text(b["text"]), on_click=action(b["handler"])).props("outline no-caps").classes("w-64")  # v1.20
                        if b.get("disabled"):  # v1.20
                            btn.disable()  # v1.20
                        if b.get("label"):  # v1.20
                            ui.label(b["label"]).classes("text-caption text-grey-7").style("width: 16rem; white-space: pre-line")  # v1.20: so breit wie der Knopf
                else:  # v1.20
                  with ui.row().classes("items-center w-full no-wrap") as row_el:  # v1.09
                    btn = ui.button(wd.clean_text(b["text"]), on_click=action(b["handler"])).props("outline no-caps").classes("w-64")
                    if b.get("disabled"):
                        btn.disable()
                    if b.get("label"):
                        ui.label(b["label"]).classes("text-grey-8").style("white-space: pre-line")
                if b.get("pico_only"):  # v1.09
                    pico_rows.append(row_el)  # v1.09
                    # row_el.set_visibility(vals.get("L") in pico_values)  # v1.11 (entfallen)
                    row_el.set_visibility(vals.get("L") in pico_values and fw_avail)  # v1.11

            ide_tabs = []                                              # Reiter, die es nur mit der ARDUINO IDE gibt (nicht mit PlatformIO)  # v1.07

            def update_ide_tabs():  # v1.07
                for tab in ide_tabs:  # v1.07
                    set_tab_visible(tab, not vals.get("use_pio"))  # v1.07
                refresh_boards()  # v1.08

            dcc = {"tab": None}  # v1.06

            def set_tab_visible(tab, visible):  # v1.06
                try:  # v1.06
                    tab.set_visibility(bool(visible))  # v1.06
                except AttributeError:                                     # andere NiceGUI-Version: Eigenschaft visible  # v1.06
                    tab.visible = bool(visible)  # v1.06

            def update_dcc_tab():  # v1.06
                """Reiter DCC Arduino nur zeigen, wenn oben ein Nano gewaehlt ist (bei automatischer Erkennung bleibt der Stand von vorher)"""  # v1.06
                tab = dcc["tab"]  # v1.06
                if tab is None:  # v1.06
                    return  # v1.06
                nano_values = spec["pages"]["left"].get("nano_values")  # v1.06
                if vals.get("auto_L") or vals.get("L") is None or nano_values is None:  # v1.06
                    # set_tab_visible(tab, dcc["initial"])  # v1.06  # v1.64 (entfallen)
                    nano = dcc["nano"]  # v1.64
                else:  # v1.06
                    # set_tab_visible(tab, vals["L"] in nano_values)  # v1.06  # v1.64 (entfallen)
                    nano = vals["L"] in nano_values  # v1.64
                proto = vals.get("protocol") or dcc["proto"]  # v1.64: Reiter heisst wie das Protokoll (DCC/LNet Arduino), bei CAN gibt es ihn nicht
                set_tab_visible(tab, nano and proto != "CAN")  # v1.64
                if proto != "CAN" and tab.props.get("label") != proto + " Arduino":  # v1.64
                    tab.props["label"] = proto + " Arduino"  # v1.64
                    tab.update()  # v1.64

            boards = []                                                # (Seite der Spezifikation, Radiogruppen) fuer refresh_boards  # v1.08

            def board_second(p):  # v1.08
                """Boards ab Wert 4 (Uno, IDE, ESP32, Pico ...): ESP32 nur, wenn PlatformIO eingestellt ist oder die ARDUINO IDE das ESP32-Paket hat"""  # v1.08
                esp = p.get("esp32_value")  # v1.08
                hide_esp = esp is not None and not (vals.get("use_pio") or p.get("esp32_lib"))  # v1.08
                return {v: t for v, t in p["radios"] if v > 3 and not (hide_esp and v == esp)}  # v1.08

            def refresh_boards():  # v1.08
                """Nach dem Wechsel der Entwicklungsumgebung im Dialog die Boardliste anpassen (ESP32 erscheint oder verschwindet sofort, ohne den Dialog neu zu oeffnen)"""  # v1.08
                for p, g in boards:  # v1.08
                    if g.get("b") is not None:  # v1.08
                        g["b"].set_options(board_second(p))  # v1.08

            def board_group(side, tab):
                p = spec["pages"][side]
                key = "L" if side == "left" else "R"
                # with ui.column().classes("gap-0"):  # v1.20 (entfallen)
                with ui.column().classes("gap-0 shrink-0").style("min-width: 20rem"):  # v1.20: behaelt ihre Breite, die Beschriftungen (zum Beispiel Nano Normal (old Bootloader)) brechen nicht um
                    # ui.checkbox(p["auto_text"], value=bool(vals["auto_" + key]),  # v1.25 (entfallen: Knopf Erkennen statt Haken)
                                # on_change=lambda e, k=key: vals.__setitem__("auto_" + k, bool(e.value)))  # v1.06 (entfallen)
                                # on_change=lambda e, k=key: (vals.__setitem__("auto_" + k, bool(e.value)), update_dcc_tab()))  # v1.06  # v1.25 (entfallen)
                    # ui.button(p["detect_text"], on_click=action("__Detect_Board_" + key)).props("outline no-caps dense").classes("q-mb-xs").tooltip(p["detect_hint"])  # v1.25: erkennt das angeschlossene Board einmalig (statt des Hakens Automatisch erkennen)  # v1.28 (entfallen: der Knopf steht jetzt ueber USB Port erkennen)
                    first = {v: t for v, t in p["radios"] if v <= 3}
                    # second = {v: t for v, t in p["radios"] if v > 3}  # v1.08 (entfallen)
                    second = board_second(p)  # v1.08
                    g = {}

                    def pick(which, e, k=key):
                        if e.value is None:
                            return
                        vals[k] = e.value
                        update_pico_buttons()
                        ota_tab.set_visibility(vals.get("L") == esp32_value and esp32_value is not None and not view_only)  # v1.09  # v1.75
                        esp_tab.set_visibility(vals.get("L") == esp32_value and esp32_value is not None and not has_summary and not view_only)  # v1.30  # v1.53  # v1.75
                        update_dcc_tab()  # v1.06
                        other = g["b"] if which == "a" else g["a"]
                        if other is not None:
                            other.value = None
                    # g["a"] = ui.radio(first, value=vals[key] if vals[key] in first else None)  # v1.12 (entfallen)
                    g["a"] = ui.radio(first, value=vals[key] if vals[key] in first else None).props("dense")  # v1.12
                    g["a"].on_value_change(lambda e: pick("a", e))
                    ui.label(p["subtitle"]).classes("text-caption q-ml-md")
                    # g["b"] = ui.radio(second, value=vals[key] if vals[key] in second else None) if second else None  # v1.12 (entfallen)
                    g["b"] = ui.radio(second, value=vals[key] if vals[key] in second else None).props("dense") if second else None  # v1.12
                    if g["b"] is not None:
                        g["b"].on_value_change(lambda e: pick("b", e))
                    if not second:
                        g["b"] = None
                    boards.append((p, g))  # v1.08

            esp32_value = spec["pages"]["left"].get("esp32_value")
            view_only = bool(spec.get("view"))  # v1.75: Fenster Wartung / Firmware installieren: ohne die Reiter ESP Einstellungen und WLAN (OTA)
            has_summary = bool(spec["pages"]["left"].get("summary"))  # v1.53
            # with ui.tabs().classes("w-full") as tabs:  # v1.33 (entfallen)
            with ui.tabs().classes("w-full mll-opttabs").props("align=left") as tabs:  # v1.33  # v1.63: Reiter links ausgerichtet
                tab_objs = [ui.tab(t["name"]) for t in spec["tabs"]]
                for t, tab_obj in zip(spec["tabs"], tab_objs):  # v1.06
                    if t.get("ide_only"):  # v1.07
                        ide_tabs.append(tab_obj)  # v1.07
                        set_tab_visible(tab_obj, not vals.get("use_pio"))  # v1.07
                    if t.get("nano_only"):  # v1.06
                        dcc["tab"], dcc["initial"] = tab_obj, bool(t.get("visible", True))  # v1.06
                        dcc["nano"], dcc["proto"] = bool(t.get("nano", dcc["initial"])), str(vals.get("protocol") or "")  # v1.64
                        set_tab_visible(tab_obj, dcc["initial"])  # v1.06
                esp_tab = ui.tab(tr("ESP Einstellungen"))  # v1.30
                esp_tab.set_visibility(vals.get("L") == esp32_value and esp32_value is not None and not has_summary and not view_only)  # v1.30  # v1.53: mit Hauptseite stehen die Einstellungen dort
                ota_tab = ui.tab(tr("WLAN (OTA)"))
                # ext_tab = ui.tab(tr("Erweiterungen"))  # v1.31  # v1.41 (entfallen: eigenes Fenster, Menue Einstellungen)
                ota_tab.set_visibility(vals.get("L") == esp32_value and esp32_value is not None and not view_only)  # v1.75
            # with ui.tab_panels(tabs, value=tab_objs[0]).classes("w-full"):  # v1.35 (entfallen)
            start_tab = next((t_ for t_ in tab_objs if _TAB["keep"] and t_.props["name"] == _TAB["name"]), tab_objs[0])  # v1.35
            _TAB["keep"] = False  # v1.35
            tabs.on_value_change(lambda e: _TAB.__setitem__("name", e.value))  # v1.35
            with ui.tab_panels(tabs, value=start_tab).classes("w-full"):  # v1.35
                with ui.tab_panel(esp_tab):  # v1.30
                    if not has_summary:  # v1.53: sonst auf der Hauptseite (esp_panel nur einmal aufbauen)
                        esp_panel()  # v1.30
                with ui.tab_panel(ota_tab):
                    # ui.label(tr('ACHTUNG: Die WLAN-Einstellung ist nicht kompatibel mit der Einstellung "Schnelles Update". "Schnelles Update" wird ignoriert, wenn WLAN eingeschaltet ist.')).classes("text-negative text-weight-medium")  # v1.44  # v1.46 (entfallen)
                    # settings_panel()  # v1.66 (entfallen)
                    wifi_cb = settings_panel()  # v1.66: Haken WLAN, damit die Anzeige auf dem Display folgt
                    if wifi_cb is not None:  # v1.66
                        wifi_cb.on_value_change(lambda e: wifi_state["apply"] and wifi_state["apply"](bool(e.value)))  # v1.66
                    if ota_upload_handler is not None:  # v1.40
                        ui.button(tr("ESP32-Firmware über WLAN hochladen …"), on_click=lambda: ota_upload_handler()).props("outline no-caps")  # v1.40
                # with ui.tab_panel(ext_tab):  # v1.31  # v1.41 (entfallen)
                    # ext_panel()  # v1.31  # v1.41 (entfallen)
                for t, tab in zip(spec["tabs"], tab_objs):
                    with ui.tab_panel(tab).classes("mll-hw-panel" if t["kind"] == "arduino" and t["side"] == "left" and has_summary else ""):  # v1.59
                        if t["kind"] == "arduino" and t["side"] == "left" and spec["pages"]["left"].get("summary"):  # v1.49: nur Anzeige, die Auswahl steht im Dialog des Knopfes Suchen
                            sm = spec["pages"]["left"]["summary"]
                            with ui.row().classes("items-start w-full no-wrap gap-4"):  # v1.59: kompakt
                                with ui.column().classes("grow gap-1"):  # v1.59
                                    with ui.row().classes("items-baseline gap-2 no-wrap"):  # v1.62: fester Text fett, danach die gewaehlte Hardware
                                        ui.label(sm["hw_label"]).classes("text-body1 text-bold")  # v1.62
                                        ui.label(sm["line"]).classes("text-body1")  # v1.62
                                    for b in t["buttons"]:  # v1.63: Knopf Erkennen unter der Hardware-Zeile
                                        sb = ui.button(wd.clean_text(b["text"]), on_click=action(b["handler"])).props("outline no-caps dense").classes("q-px-md")  # v1.59
                                        if b.get("label"):
                                            sb.tooltip(b["label"])
                                    ui.separator().classes("q-my-xs")  # v1.59
                                    ui.label(sm["config_title"]).classes("text-subtitle2")
                                    with ui.row().classes("items-center gap-3 no-wrap"):  # v1.59: Protokoll und Variante nebeneinander
                                        ui.select(sm["protocols"], value=sm["protocol"], label=sm["protocol_label"],
                                                  on_change=lambda e: (vals.__setitem__("protocol", e.value), update_dcc_tab())).props("outlined dense").classes("w-40").set_enabled(len(sm["protocols"]) > 1)  # v1.58 (wie v1.56)  # v1.59
                                        if sm["variants"]:
                                            ui.select(sm["variants"], value=vals["L"] if vals.get("L") in sm["variants"] else 2, label=sm["variant_label"],
                                                      on_change=lambda e: vals.__setitem__("L", e.value) if e.value else None).props("outlined dense").classes("w-80")  # v1.59
                                    if sm["protocol_hint"]:  # v1.53: nur noch der Hinweis bei Selectrix
                                        ui.label(sm["protocol_hint"]).classes("text-caption text-grey-7")
                                    with ui.column().classes("gap-0"):  # v1.59: Haken eng untereinander
                                        if sm["fast_update"]:  # v1.51: Schnelles Update (nur ESP32/Pico)
                                            ui.checkbox(sm["serial_cfg_text"], value=bool(vals.get("serial_cfg")),
                                                        on_change=lambda e: vals.__setitem__("serial_cfg", bool(e.value))).props("dense").classes("q-py-xs").tooltip(
                                                next((x_["serial_cfg_hint"] for x_ in spec["tabs"] if x_.get("kind") == "ide"), ""))  # v1.59
                                        # v1.55: Lichtsensor und Schaltzustaende sind Makrozeilen des Blattes (headless_sheet_settings)
                                        ui.checkbox(sm["ldr_text"], value=bool(vals.get("ldr")), on_change=lambda e: vals.__setitem__("ldr", bool(e.value))).props("dense").classes("q-py-xs")  # v1.55  # v1.59
                                        ui.checkbox(sm["store_text"], value=bool(vals.get("store_status")), on_change=lambda e: vals.__setitem__("store_status", bool(e.value))).props("dense").classes("q-py-xs")  # v1.55  # v1.59
                                    if sm["esp_options"]:  # v1.52: nur die Display-Einstellung bleibt beim ESP32
                                        esp_panel(compact=True)  # v1.53  # v1.59
                                if sm["image"]:
                                    # ui.image(sm["image"]).classes("w-40")  # v1.59  # v1.66 (entfallen)
                                    ui.image(sm["image"]).classes("w-60")  # v1.59  # v1.66: Bild 50 % groesser (15rem statt 10rem)
                        elif t["kind"] == "arduino":
                            # with ui.row().classes("items-start no-wrap w-full"):  # v1.20 (entfallen)
                            with ui.row().classes("items-start w-full").style("flex-wrap: wrap; gap: 1rem 2rem"):  # v1.20: auf schmalen Bildschirmen rutscht die Auswahl des Boards unter die Knoepfe
                                with ui.column().classes("grow"):  # v1.20
                                    _dp = spec["pages"]["left" if t["side"] == "left" else "right"]  # v1.28
                                    ui.button(_dp["detect_text"], on_click=action("__Detect_Board_" + ("L" if t["side"] == "left" else "R"))).props("outline no-caps").classes("w-64").tooltip(_dp["detect_hint"])  # v1.28: Board und USB Port erkennen steht ueber USB Port erkennen
                                    for b in t["buttons"]:
                                        button_row(b, compact=True)  # v1.20
                                board_group(t["side"], tab)
                        elif t["kind"] == "ide":  # v1.04
                            ui.label(t["intro"]).classes("text-grey-8").style("white-space: pre-line")  # v1.04
                            # ui.radio({0: t["arduino_text"], 1: t["pio_text"]}, value=1 if vals.get("use_pio") else 0,  # v1.04  # v1.44 (entfallen: PlatformIO zuerst)
                            ide_btn = {}  # v1.44
                            ui.radio({1: t["pio_text"], 0: t["arduino_text"]}, value=1 if vals.get("use_pio") else 0,  # v1.44
                                     # on_change=lambda e: vals.__setitem__("use_pio", bool(e.value)))  # v1.07 (entfallen)
                                     on_change=lambda e: (vals.__setitem__("use_pio", bool(e.value)), update_ide_tabs(), ide_btn["b"].set_visibility(not bool(e.value)) if "b" in ide_btn else None))  # v1.07  # v1.44
                            if not spec["pages"]["left"].get("summary"):  # v1.51: sonst steht der Haken auf der Hauptseite (Einstellungen)
                                ui.checkbox(t["serial_cfg_text"], value=bool(vals.get("serial_cfg")),  # v1.32
                                            on_change=lambda e: vals.__setitem__("serial_cfg", bool(e.value))).tooltip(t["serial_cfg_hint"])  # v1.32
                            # ui.label(tr('ACHTUNG: Die "Schnelles Update" Einstellung ist nicht kompatibel mit der Einstellung "WLAN". "Schnelles Update" wird ignoriert, wenn WLAN eingeschaltet ist.')).classes("text-negative text-weight-medium")  # v1.45  # v1.46 (entfallen)
                            ui.label(t["status"]).classes("text-grey-8").style("white-space: pre-line")  # v1.04
                            for b in t["buttons"]:  # v1.04
                                button_row(b)  # v1.04
                            if arduino_settings_handler is not None:  # v1.40
                                # ui.button(tr("ARDUINO-IDE Einstellungen"), on_click=lambda: arduino_settings_handler()).props("outline no-caps")  # v1.40  # v1.44 (entfallen)
                                ide_btn["b"] = ui.button(tr("ARDUINO-IDE Einstellungen"), on_click=lambda: arduino_settings_handler()).props("outline no-caps")  # v1.44
                                ide_btn["b"].set_visibility(not vals.get("use_pio"))  # v1.44: nur mit ARDUINO-IDE
                            for text in t.get("texts", []):  # v1.07
                                ui.label(text).classes("text-grey-8").style("white-space: pre-line")  # v1.07
                        else:
                            for b in t["buttons"]:
                                button_row(b)
                            for text in t.get("texts", []):
                                ui.label(text).classes("text-grey-8").style("white-space: pre-line")
            with ui.row().classes("justify-end w-full"):
                for b in spec["lower"]:
                    ui.button(wd.clean_text(b["text"]), on_click=action(b["handler"])).props("outline no-caps" if b["handler"] != "__Close_Button_Click" else "no-caps").classes(
                        "mll-default mll-cancel" if b["handler"] == "__Close_Button_Click" else "")
        res = await dlg
        wd.safe_delete(dlg)
    return res


# ------------------------------------------------------------------ Klasse
def make_class(Base):
    ns = sys.modules[Base.__module__].__dict__
    M02, M09, M25, M37, P01 = (ns[n] for n in ("M02", "M09", "M25", "M37", "P01"))
    vbCritical = ns["vbCritical"]
    import proggen.M28_Diverse as M28pio  # v1.07
    vbYes, vbYesNo, vbQuestion = ns.get("vbYes", 6), ns.get("vbYesNo", 4), ns.get("vbQuestion", 32)  # v1.07
    PFX = "_" + Base.__name__            # Praefix fuer private Methoden (Name Mangling)
    buttons = harvest_buttons(Base)

    class WebOptions(Base):
        def Hide(self):
            if not wd.bridge_usable():
                return super().Hide()
            self._web_hidden = True

        def Show(self, first_page_only=False, view=None):  # v1.75: view: None, 'wartung' oder 'firmware' (Menue Werkzeuge)
            if not wd.bridge_usable():
                return super().Show(first_page_only=first_page_only)
            if getattr(self, "_web_running", False):       # Aufruf aus einem Handler: danach neu oeffnen
                self._web_reshow = True
                return
            self._web_running = True
            VIEW["only"] = view  # v1.75
            self._web_auto_connect = False  # v1.36
            port_before = self._web_port_state()  # v1.74
            try:
                self._web_loop(first_page_only)
            finally:
                self._web_running = False
                VIEW["only"] = None  # v1.75
                self.IsActive = False
                self._web_port_changed(port_before)  # v1.74: COM Port in der Hardwaresuche geaendert: Autoconnect nach dem Schliessen
                if getattr(self, "_web_auto_connect", False):  # v1.36: Anschluss der Lichtmaschine erkannt: danach gleich verbinden
                    self._web_auto_connect = False  # v1.36
                    hook, loop = wd._bridge.get("auto_connect"), wd._bridge.get("loop")  # v1.36
                    client = wd._bridge.get("client")  # v1.39: die Seite, zu der der Befehl gehoert (die Bruecke wird nach dem Befehl geleert)
                    if hook is not None and loop is not None:  # v1.36
                        try:  # v1.36
                            import asyncio  # v1.36
                            asyncio.run_coroutine_threadsafe(hook(client), loop)  # v1.39 (v1.36: hook()): nicht warten: der Befehl Optionen ist erst nach diesem Aufruf fertig
                        except Exception:                          # noqa: BLE001  # v1.36
                            logger.warning("Automatisches Verbinden nicht gestartet", exc_info=True)  # v1.36

        # --------------------------------------------------------------
        def _web_port_state(self):  # v1.74: (Anschluss im Blatt, Einstellung serportname) fuer den Vergleich vor/nach dem Oeffnen der Optionen
            try:
                cell = str(P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL) or "")
            except Exception:                                  # noqa: BLE001
                cell = ""
            try:
                import mlpyproggen.Prog_Generator as PG
                cfg = str(PG.global_controller.getConfigData("serportname") or "")
            except Exception:                                  # noqa: BLE001
                cfg = ""
            return cell, cfg

        @staticmethod
        def _web_norm_port(raw):  # v1.74: Geraetename oder "" (kein Anschluss: leer, 999, COM?, NO DEVICE, negative Zahl, IP:)
            raw = str(raw or "").strip().lstrip("*").strip()
            if raw.startswith("-") or raw.upper() in ("", "999", "COM?", "NO DEVICE") or raw.upper().startswith("IP:"):
                return ""
            if raw.isdigit():
                return ("COM" + raw) if os.name == "nt" else ""
            return raw

        def _web_port_changed(self, before):  # v1.74: Wurde der COM Port in der Hardwaresuche (Geraeteauswahl) geaendert, laeuft nach dem Schliessen des Fensters der Autoconnect
            try:
                after = self._web_port_state()
                if after == before or getattr(self, "_web_auto_connect", False):
                    return
                new_port = self._web_norm_port(after[1]) or self._web_norm_port(after[0])
                if not new_port:
                    return
                import mlpyproggen.Prog_Generator as PG
                from _web import web_tabs
                ctrl = PG.global_controller
                if not web_tabs.is_auto_connect(ctrl):
                    logger.info("Optionen: COM Port geaendert (%s), Autoconnect ist ausgeschaltet", new_port)
                    return
                if ctrl.is_connection_open() and str(getattr(ctrl.arduino, "port", "") or "").upper() != new_port.upper():
                    ctrl.disconnect()                          # die Verbindung zum alten Anschluss beenden
                self._web_auto_connect = True
                logger.info("Optionen: COM Port geaendert (%s -> %s): nach dem Schliessen wird verbunden", before, after)
            except Exception:                                  # noqa: BLE001
                logger.debug("Aenderung des COM Ports nicht geprueft", exc_info=True)

        def _web_prepare(self, first_page_only):
            """Zustand wie UserForm_Initialize/Activate, aber ohne Tk."""
            M25.Make_sure_that_Col_Variables_match()
            # Die im Konstruktor (Hauptthread) angelegten tk.IntVar-Objekte duerfen nicht im Worker-Thread
            # freigegeben werden (Variable.__del__ ruft Tk auf): Referenz dauerhaft behalten.
            if not hasattr(self, "_tk_refs"):
                self._tk_refs = [self.__dict__.get("rb_res")]
            self.rb_res = {"_R": Var(0), "_L": Var(0)}
            self.Autodetect_Typ_L_CheckBox_var = Var(0)
            self.Autodetect_Typ_R_CheckBox_var = Var(0)
            self.Controls = {rb: P01.CControl(False) for rb in self.radiobuttons}
            setattr(self, PFX + "__Disable_Set_Arduino_Typ", True)
            getattr(self, PFX + "__Get_Arduino_Typ")(True)
            if not first_page_only:
                getattr(self, PFX + "__Get_Arduino_Typ")(False)
            setattr(self, PFX + "__Disable_Set_Arduino_Typ", False)
            self.control_to_radiobutton()
            import proggen.M28_Diverse as M28  # v1.04
            from headless import headless_sheet_settings as HSS  # v1.55
            # return {"L": self.rb_res["_L"].get() or None, "R": self.rb_res["_R"].get() or None,  # v1.30 (entfallen)
            from headless.headless_esp32_ota import load_settings  # v1.30
            import proggen.M42_Dyn_Config as M42  # v1.32
            wlan = load_settings(P01.ActiveSheet)  # v1.30
            return {"esp32_options": dict(getattr(P01.ActiveSheet, "esp32_options", None) or {}),  # v1.30
                    "esp32_hostname": wlan["hostname"], "esp32_wifi": wlan["wifi"],  # v1.30
                    "L": self.rb_res["_L"].get() or None, "R": self.rb_res["_R"].get() or None,  # v1.30
                    "auto_L": bool(self.Autodetect_Typ_L_CheckBox_var.get()),
                    # "auto_R": bool(self.Autodetect_Typ_R_CheckBox_var.get())}  # v1.04 (entfallen)
                    "auto_R": bool(self.Autodetect_Typ_R_CheckBox_var.get()),  # v1.04
                    "protocol": str(M25.Page_ID or ""),  # v1.49
                    "use_pio": bool(M28.Get_Bool_Config_Var("Use_PlatformIO")),  # v1.04
                    "serial_cfg": bool(M42.Option_Enabled()),  # v1.32  # v1.55: Einstellung des Blattes (M42 1.08)
                    "ldr": HSS.is_set("ldr"), "store_status": HSS.is_set("store_status")}  # v1.55: Makrozeilen des Blattes

        def _is_nano_value(self, value):  # v1.06
            """Gehoert der Wert des Radioknopfes zu einem Arduino Nano oder Uno (nicht ESP32 und nicht Pico)?"""  # v1.06
            try:  # v1.06
                board = str(self.boardlist[value]).lower()  # v1.06
            except (IndexError, KeyError, TypeError):  # v1.06
                return True  # v1.06
            return "esp32" not in board and "rp2040" not in board  # v1.06

        def _radios(self, side):
            items = []
            for rb, d in self.radiobuttons.items():
                if not rb.endswith(side):
                    continue
                if d.get("value") == 5:                                   # v1.25: 'Typ von Arduino IDE benutzen' entfaellt im Web (Vorschlag des Excel-Entwicklers)
                    continue  # v1.25
                # if rb.startswith("ESP32") and not M37.ESP32_Lib_Installed():  # v1.07 (entfallen)
                # if rb.startswith("ESP32") and not M37.ESP32_Lib_Installed() and not M28pio.Is_PlatformIO():  # v1.08 (entfallen)
                    # continue  # v1.08 (entfallen)
                # items.append((d["value"], d["text"]))  # v1.08 (entfallen)
                text_ = d["text"]  # v1.44
                if side == "_L":  # v1.44: Namen der Lichtmaschinen
                    text_ = {"Nano_New_L": tr("Lichtmaschine Classic, Mini (Nano (neue Version))"), "ESP32_L": tr("Lichtmaschine Pro (ESP32)"),  # v1.44
                             "PICO_L": tr("Lichtmaschine Pico Zero, MoLLi (Raspberry Pico)")}.get(rb, text_)  # v1.44
                # items.append((d["value"], d["text"]))  # v1.44 (entfallen)
                items.append((d["value"], text_))  # v1.44 (Kommentar v1.08: ESP32 immer: ob er angezeigt wird, entscheidet der Dialog live)
            return sorted(items)

        def _board_summary(self, M02a):  # v1.49: Anzeige im Reiter Lichtmaschine: Board, Variante, Port, Bild
            from _web import web_form_comport as wfc
            bt = M02a.Get_BoardTyp()
            buildopt = str(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL) or "")
            if bt == M02.HT_ESP32:
                board, picture = tr("Lichtmaschine Pro (ESP32)"), "ESP32_Image"
            elif bt == M02.HT_PICO:
                board, picture = tr("Lichtmaschine Pico Zero, MoLLi (Raspberry Pico)"), "PICO_Image"
            else:
                picture = "LED_Image"
                # names = [(M02.BOARD_NANO_OLD, "Nano Normal (old Bootloader)"), (M02.BOARD_NANO_FULL, "Nano (Full memory)"),  # v1.60 (entfallen)
                #          (M02.BOARD_NANO_NEW, "Lichtmaschine Classic, Mini (Nano (neue Version))"), (M02.BOARD_UNO_NORM, "Uno")]  # v1.60 (entfallen)
                # board = next((tr(t_) for b_, t_ in names if b_ in buildopt), tr("Lichtmaschine Classic, Mini (Nano (neue Version))"))  # v1.60 (entfallen)
                board = tr("Lichtmaschine Classic, Mini")  # v1.60: nur der Haupttyp, die Variante steht im Feld Board-Variante
            raw = str(P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL) or "").strip().lstrip("*").strip()
            port = "" if raw.upper() in ("", "999", "COM?", "NO DEVICE") or (raw.startswith("-") and raw[1:].isdigit()) else (("COM" + raw) if raw.isdigit() and os.name == "nt" else raw)  # v1.71: negative Zahl (Excel-Kennzeichen fuer einen belegten Port) ist kein Port
            offline = False
            if port:
                try:  # ist der gespeicherte Anschluss gerade am USB zu finden?
                    from serial.tools import list_ports as _lp
                    offline = port.upper() not in {str(c.device).upper() for c in _lp.comports(include_links=False)}
                except Exception:                                  # noqa: BLE001
                    logger.debug("Anschlussliste nicht lesbar", exc_info=True)
            if not port:
                # line = tr("Hardware: {board} (kein Port gewählt)", board=board)  # v1.62 (entfallen)
                line = board + " (" + tr("kein Port gewählt") + ")"  # v1.62: 'Hardware:' steht als fester Text davor
            else:
                # line = tr("Hardware: {board} an {port}", board=board, port=port) + (" (" + tr("offline") + ")" if offline else "")  # v1.62 (entfallen)
                line = tr("{board} an {port}", board=board, port=port) + (" (" + tr("offline") + ")" if offline else "")  # v1.62
            cur_pid = str(M25.Page_ID or "")                       # Protokoll: Selectrix hat andere Spalten als DCC/LNet/CAN, dort ist kein Wechsel moeglich
            # pids = ["Selectrix"] if cur_pid == "Selectrix" else ["DCC", "LNet", "CAN"]  # v1.57 (entfallen)
            # proto_hint = "" if len(pids) > 1 else tr("Selectrix kann nicht auf ein anderes Protokoll umgestellt werden.")  # v1.56  # v1.57 (entfallen)
            # pids = ["DCC", "LNet", "CAN", "Selectrix"]  # v1.57: Classic und Pro (ESP32) koennen auch Selectrix  # v1.58 (entfallen: Selectrix kommt spaeter)
            # proto_hint = ""  # v1.57  # v1.58 (entfallen)
            # pids = ["Selectrix"] if cur_pid == "Selectrix" else ["DCC", "LNet", "CAN"]  # v1.58 (wie v1.56)  # v1.67 (entfallen)
            # proto_hint = "" if len(pids) > 1 else tr("Selectrix kann nicht auf ein anderes Protokoll umgestellt werden.")  # v1.58 (wie v1.56)  # v1.67 (entfallen)
            # if bt == M02.HT_PICO:  # v1.56: der Pico kann nur DCC  # v1.67 (entfallen: die Tabelle Platform_Parameters bestimmt die Protokolle)
            #     if cur_pid == "Selectrix":  # v1.56  # v1.67 (entfallen)
            #         pids = ["Selectrix"]  # v1.57: gesperrt  # v1.67 (entfallen)
            #         proto_hint = tr("Beim Pico ist nur DCC möglich. Ein Selectrix-Blatt kann nicht umgestellt werden.")  # v1.56  # v1.67 (entfallen)
            #     else:  # v1.56  # v1.67 (entfallen)
            #         pids = ["DCC"]  # v1.56  # v1.67 (entfallen)
            #         if cur_pid and cur_pid != "DCC":  # v1.56: das eingestellte Protokoll bleibt sichtbar, damit es auf DCC umgestellt werden kann  # v1.67 (entfallen)
            #             pids.insert(0, cur_pid)  # v1.56  # v1.67 (entfallen)
            #             proto_hint = tr("Beim Pico ist nur DCC möglich. Bitte auf DCC umstellen.")  # v1.56  # v1.67 (entfallen)
            import proggen.M30_Tools as M30_  # v1.67

            def _supports(pid):  # v1.67: Zeile Supports<Protokoll> der Tabelle Platform_Parameters (Spalte AM328, ESP32 oder PICO); nicht lesbar = unterstuetzt
                try:  # v1.67
                    return bool(M30_.Get_Platform_Bool(bt, "Supports" + pid, True))  # v1.67
                except Exception:                                  # noqa: BLE001  # v1.67
                    logger.debug("Supports%s fuer %s nicht lesbar", pid, bt, exc_info=True)  # v1.67
                    return True  # v1.67
            # if cur_pid == "Selectrix":  # v1.67: Selectrix hat andere Spalten als DCC/LNet/CAN, kein Wechsel  # v1.68 (entfallen)
            # pids = ["Selectrix"]  # v1.67  # v1.68 (entfallen)
            # proto_hint = tr("Selectrix kann nicht auf ein anderes Protokoll umgestellt werden.")  # v1.67  # v1.68 (entfallen)
            # else:  # v1.67  # v1.68 (entfallen)
            # pids = [p for p in ("DCC", "LNet", "CAN") if _supports(p)] or ["DCC"]  # v1.67  # v1.68 (entfallen)
            # proto_hint = ""  # v1.67  # v1.68 (entfallen)
            # if cur_pid and cur_pid not in pids:  # v1.67: das eingestellte Protokoll bleibt sichtbar, damit es umgestellt werden kann  # v1.68 (entfallen)
            # proto_hint = tr("Dieses Protokoll wird von der gewählten Hardware nicht unterstützt. Bitte auf {liste} umstellen.", liste=", ".join(pids))  # v1.67  # v1.68 (entfallen)
            # pids.insert(0, cur_pid)  # v1.67  # v1.68 (entfallen)
            pids = [p for p in ("DCC", "LNet", "CAN", "Selectrix") if _supports(p)] or ["DCC"]  # v1.68: Selectrix gehoert dazu, der Wechsel rechnet die Adressen um
            proto_hint = ""  # v1.68
            if cur_pid and cur_pid not in pids:  # v1.68: das eingestellte Protokoll bleibt sichtbar, damit es umgestellt werden kann
                proto_hint = tr("Dieses Protokoll wird von der gewählten Hardware nicht unterstützt. Bitte auf {liste} umstellen.", liste=", ".join(pids))  # v1.68
                pids.insert(0, cur_pid)  # v1.68
            if cur_pid and cur_pid not in pids:
                pids.append(cur_pid)
            variants = None                                        # Board-Variante nur fuer Classic (Wert = Index der Boardliste)
            if bt not in (M02.HT_ESP32, M02.HT_PICO):
                # variants = {1: tr("Nano Normal (old Bootloader)"), 2: tr("Nano (neue Version)"),  # v1.60: ohne 'Lichtmaschine Classic, Mini'  # v1.61 (entfallen)
                #             3: tr("Nano (Full memory)"), 4: tr("Uno")}  # v1.61 (entfallen)
                variants = {1: tr("Nano (alter Bootloader)"), 2: tr("Nano (neue Version)"),  # v1.61
                            3: tr("Nano (maximaler Speicher)"), 4: tr("Uno")}  # v1.61
            return {"line": line, "hw_label": tr("Hardware") + ":", "image": wfc.find_image(picture),  # v1.62
                    "config_title": tr("Einstellungen"),  # v1.51: vorher Weitere Einstellungen des Blattes
                    "serial_cfg_text": tr("Schnelles Update"), "fast_update": bt in (M02.HT_ESP32, M02.HT_PICO),  # v1.51
                    "esp_options": bt == M02.HT_ESP32, "ldr_text": tr("Lichtsensor aktivieren"), "store_text": tr("Schaltzustände speichern"),  # v1.54
                     # v1.52
                    # "protocols": {o: ("LNet (LocoNet)" if o == "LNet" else o) for o in pids}, "protocol": cur_pid, "protocol_label": tr("Protokoll"),  # v1.66 (entfallen)
                    "protocols": {o: o for o in pids}, "protocol": cur_pid, "protocol_label": tr("Protokoll"),  # v1.66: nur 'LNet', der geschuetzte Begriff LocoNet steht nicht mehr in der Oberflaeche (5.25)
                    "protocol_hint": proto_hint,  # v1.56
                    # "variants": variants, "variant_label": tr("Board-Variante")}  # v1.66 (entfallen)
                    "variants": variants, "variant_label": tr("Hardwarevariante")}  # v1.66: Hardwarevariante statt Board-Variante

        def _web_spec(self, first_page_only):
            import proggen.M02a_Public as M02a  # v1.06
            try:  # v1.44
                import mlpyproggen.Prog_Generator as PG_  # v1.44
                from _web import web_tabs as WT_  # v1.44
                beginner = WT_.is_beginner_mode(PG_.global_controller)  # v1.44
            except Exception:                                      # noqa: BLE001  # v1.44
                beginner = False  # v1.44
            buildopt = str(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL))
            wlan_device = "WLAN" in buildopt
            cands = buttons.get("__Detect_LED_Port_Button_Click", [])
            # Quelltext: erst der WLAN-Zweig ("IP Adresse suchen"), dann der USB-Zweig ("USB Port erkennen")
            port_btn = (cands[0] if wlan_device else cands[-1]) if cands else {"text": "USB Port", "label": "", "disabled": False}
            left = [dict(port_btn, handler="__Detect_LED_Port_Button_Click")]
            summary = None  # v1.49: Reiter Lichtmaschine zeigt nur Board und Port; gewaehlt wird im Dialog des Knopfes Suchen
            if not wlan_device:  # v1.49
                summary = self._board_summary(M02a)  # v1.49
                left = [{"text": tr("Erkennen"), "handler": "__Detect_LED_Port_Button_Click", "disabled": False,  # v1.49
                         "label": tr("Sucht die angeschlossenen Boards an allen USB Anschlüssen und zeigt sie in einer Liste. Dort werden Board und Port gewählt.")}]  # v1.49  # v1.65: Protokoll steht auf der Hauptseite
            if wlan_device and buttons.get("__Detect_LED_IP_Button_Click"):
                left.append(dict(buttons["__Detect_LED_IP_Button_Click"][0], handler="__Detect_LED_IP_Button_Click"))
            # left.append({"text": tr("Firmware installieren"), "handler": "__Boot_Firmware_Button_Click", "disabled": False,  # v1.18: nicht mehr nur Pico (pico_only entfallen),       # nur mit dem Pico (wie im Excel-Programm)  # v1.09  # v1.43 (entfallen: Knopf steht jetzt im Reiter Firmware Installation)
            # "label": tr("Schreibt eine fertige Firmware (UF2-Datei aus dem Ordner MobaLedLib/firmware) auf den Raspberry Pi Pico")})  # v1.09  # v1.43 (entfallen: Knopf steht jetzt im Reiter Firmware Installation)
            subtitle = M09.Get_Language_Str("Für andere Hauptplatine")
            auto_text = M09.Get_Language_Str("Automatisch erkennen")
            detect_text = tr("Board und USB Port erkennen")  # v1.25
            # detect_hint = tr("Sucht den angeschlossenen Arduino (Nano alt oder neu, ESP32, Pico) an allen USB Anschlüssen, stellt das erste gefundene Board ein und zeigt es mit dem USB Port an. Dort kann es übernommen oder ein anderer Typ gewählt werden.")  # v1.25  # v5.18 (entfallen)
            detect_hint = tr("Sucht an allen USB-Anschlüssen nach Nano, ESP32 und Pico. Werden mehrere Board-Typen gefunden, können Sie den gewünschten Typ auswählen. Anschließend wird der passende USB-Port angezeigt.")
            light_machine_hint = tr("Sucht an allen USB-Anschlüssen nach Lichtmaschinen (Nano, ESP32, Pico). Werden unterschiedliche Typen gefunden, können Sie die gewünschte Lichtmaschine auswählen. Anschließend wird der passende USB-Port angezeigt.")  # v5.18 (Pull Request 39, Juergen)  # v1.25  # v5.18
            tabs = [{"name": tr("Lichtmaschine"), "kind": "arduino", "side": "left", "buttons": left}]
            # pages = {"left": {"radios": self._radios("_L"), "subtitle": subtitle, "auto_text": auto_text}}  # v1.08 (entfallen)
            esp32_value = next((d["value"] for rb, d in self.radiobuttons.items() if rb.startswith("ESP32") and rb.endswith("_L")), None)  # v1.08
            # pages = {"left": {"radios": self._radios("_L"), "subtitle": subtitle, "auto_text": auto_text, "detect_text": detect_text, "detect_hint": detect_hint,  # v1.08  # v1.25  # v5.18 (entfallen)
            pages = {"left": {"radios": self._radios("_L"), "subtitle": subtitle, "auto_text": auto_text, "detect_text": detect_text, "detect_hint": light_machine_hint,  # v1.08  # v1.25  # v5.18
                              # "esp32_value": esp32_value, "esp32_lib": bool(M37.ESP32_Lib_Installed())}}  # v1.09 (entfallen)
                              "esp32_value": esp32_value, "esp32_lib": bool(M37.ESP32_Lib_Installed()),  # v1.09
                              # "pico_values": [d["value"] for rb, d in self.radiobuttons.items() if rb.startswith("PICO") and rb.endswith("_L")]}}  # v1.11 (entfallen)
                              "pico_values": [d["value"] for rb, d in self.radiobuttons.items() if rb.startswith("PICO") and rb.endswith("_L")],  # v1.11
                              "firmware_available": self._firmware_available()}}  # v1.11
            pages["left"]["summary"] = summary  # v1.49
            if not first_page_only:
                # if M25.Page_ID != "CAN":  # v1.64 (entfallen: der Reiter wird immer angelegt und bei CAN ausgeblendet, damit er beim Wechsel des Protokolls im Dialog erscheinen kann)
                if True:  # v1.64
                    # Wie im Excel-Programm (UpdateDCCSubPage): Der Reiter DCC Arduino gehoert nur zu einem Nano; bei Pico und ESP32 ist er ausgeblendet
                    # (und erscheint wieder, wenn man oben ein Nano-Board waehlt: nano_values, siehe _options_async)
                    tabs.append({"name": M25.Page_ID + " Arduino", "kind": "arduino", "side": "right",
                                 # "buttons": tab_buttons(buttons, ["__Detect_Right_Port_Button_Click", "__ProInstall_Button_Click"])})  # v1.06 (entfallen)
                                 "buttons": tab_buttons(buttons, ["__Detect_Right_Port_Button_Click", "__ProInstall_Button_Click"]),  # v1.06
                                 # "nano_only": True, "visible": M02a.Get_BoardTyp() == M02.HT_AM328})  # v1.06  # v1.64 (entfallen)
                                 "nano_only": True, "nano": M02a.Get_BoardTyp() == M02.HT_AM328,  # v1.64: Nano und Protokoll getrennt, der Dialog rechnet die Sichtbarkeit
                                 "visible": M02a.Get_BoardTyp() == M02.HT_AM328 and M25.Page_ID != "CAN"})  # v1.06  # v1.64
                    pages["right"] = {"radios": self._radios("_R"), "subtitle": subtitle, "auto_text": auto_text, "detect_text": detect_text, "detect_hint": detect_hint}  # v1.25
                    pages["left"]["nano_values"] = [v for v, _text in pages["left"]["radios"] if self._is_nano_value(v)]  # v1.06
                files = tab_buttons(buttons, ["__Import_Button_Click", "__Save_Button_Click", "__Load_Button_Click", "__Copy_Page_Button_Click"])
                files = [b for b in files if b["handler"] != "__Copy_Page_Button_Click"]  # v1.29: ersetzt durch Seite duplizieren
                for b in files:
                    if b["handler"][2:] in {h[2:] for h in NOT_IN_WEB}:
                        b["disabled"] = True
                    if b["handler"] == "__Import_Button_Click":  # v1.29
                        b["disabled"] = False  # v1.29
                # tabs.append({"name": M09.Get_Language_Str("Dateien"), "kind": "list", "buttons": files,  # v1.42 (entfallen: Importieren v. altem Prog. steht im Menue Datei)
                # "texts": ["Speichern lädt die Datei über den Browser herunter, Laden öffnet einen Upload-Dialog."]})  # v1.42 (entfallen: Importieren v. altem Prog. steht im Menue Datei)
                # Der Knopf des Originals "Update pyMobaLedLib" (__Update_pyMobaLedLib_Button_Click) fehlt hier absichtlich: Er laedt master.zip des
                # Original-Repositorys und ueberschreibt den ganzen Programmordner (Tk-Version), das gibt es im Web nicht. Das Update der Web-Oberflaeche
                # ist das Menue Hilfe -> Update webMobaLedLib (_web/web_update.py).
                import proggen.M08_ARDUINO as M08  # v1.04
                pio = M08.Find_PIO()  # v1.04
                tabs.append({"name": tr("Entwicklungsumgebung"), "kind": "ide",  # v1.04
                             # "intro": tr("Womit sollen die Programme übersetzt und auf den Arduino geladen werden?"),  # v1.04  # v1.66 (entfallen)
                             "intro": tr("Womit sollen die Programme übersetzt und auf die Lichtmaschine geladen werden?"),  # v1.04  # v1.66: Lichtmaschine statt Arduino
                             # "texts": [tr("Das Programm webMobaLedLib selbst aktualisieren: Menü Hilfe → Update webMobaLedLib …")],  # v1.07  # v5.09 (entfallen)
                             "texts": [tr("Das Programm MobaLedLib Studio selbst aktualisieren: Menü Hilfe → Update MobaLedLib Studio …")],  # v1.07  # v5.09
                             "arduino_text": tr("ARDUINO-IDE (nur Kompatibilität - nicht mehr nutzen)"), "pio_text": tr("PlatformIO (Standard)"),  # v1.04  # v1.44
                             "serial_cfg_text": tr("Schnelles Update: nur geänderte Konfiguration übertragen (ESP32/Pico)"),  # v1.39
                             "serial_cfg_hint": tr("Übertragen werden nur Änderungen an der Konfiguration, also Makros, Farben und Startwerte. Das dauert wenige Sekunden. Das Programm selbst wird nur beim ersten Mal oder nach Änderungen an Programm, Erweiterungen, LED-Anzahl oder Pins neu übertragen. Arduino Nano und Uno sind nicht betroffen. Nur mit PlatformIO und USB."),  # v1.39
                             "status": (tr("PlatformIO gefunden: {pfad}", pfad=pio) if pio else  # v1.04
                                        # tr("PlatformIO wurde nicht gefunden. Installation: https://platformio.org/install/cli (zum Beispiel mit: pip install platformio)")),  # v1.05 (entfallen)
                                        tr("PlatformIO wurde nicht gefunden. Installation: {hinweis}", hinweis=tr(M08.PIO_Install_Hint()))),  # v1.05
                             "buttons": [{"text": tr("PlatformIO prüfen"), "handler": "__Check_PIO_Button_Click", "disabled": False,  # v1.04
                                          # "label": tr("Zeigt, ob PlatformIO installiert ist, und seine Version")}]})  # v1.05 (entfallen)
                                          "label": tr("Zeigt, ob PlatformIO installiert ist, und seine Version")}] +  # v1.05
                                        [{"text": tr("PlatformIO-Zwischenspeicher löschen"), "handler": "__Pio_Cache_Button_Click", "disabled": False,                     # v1.16  # v1.16
                                          "label": tr("Löscht den Zwischenspeicher von PlatformIO (übersetzte Dateien und Kopien der Bibliotheken im Projekt, Download-Zwischenspeicher) und erzwingt beim nächsten Übersetzen einen vollständigen Neuaufbau. Sinnvoll, wenn PlatformIO nach einer Änderung der Bibliothek MobaLedLib noch die alte Fassung benutzt. Plattformen und Compiler bleiben erhalten.")}] +  # v1.16
                                        ([{"text": tr("USB-Zugriff für den Pico einrichten"), "handler": "__Pico_Udev_Button_Click", "disabled": False,  # v1.05
                                           "label": tr("Linux: richtet einmalig die Regel ein, mit der PlatformIO den Pico im BOOTSEL-Modus ansprechen darf (fragt nach dem Passwort). Ohne sie meldet das Hochladen: picotool was unable to connect.")}]  # v1.05
                                         # if sys.platform.startswith("linux") else [])})  # v1.13 (entfallen)
                                         if sys.platform.startswith("linux") else []) +  # v1.13
                                        # ([{"text": tr("Git installieren"), "handler": "__Install_Git_Button_Click", "disabled": False,          # nur Linux und nur, wenn git fehlt  # v1.15 (entfallen)
                                           # "label": tr("Linux: installiert den Git-Client (git). PlatformIO braucht ihn für das Board Raspberry Pi Pico (fragt nach dem Passwort). Ohne git meldet das Übersetzen: Please install Git client.")}]  # v1.15 (entfallen)
                                         # if sys.platform.startswith("linux") and not M08.Git_Installed() else [])})  # v1.15 (entfallen)
                                        ([{"text": tr("Git installieren"), "handler": "__Install_Git_Button_Click", "disabled": False,          # unter Linux, Windows und macOS, nur wenn git fehlt  # v1.15
                                           "label": tr(HG.button_label())}]  # v1.15
                                         if not M08.Git_Installed() else [])})  # v1.15
                tabs.append({"name": M09.Get_Language_Str("Update"), "kind": "list", "buttons": tab_buttons(
                    buttons, ["__Update_to_Arduino_Button_Click", "__Update_Beta_Button_Click",
                              "__Show_Lib_and_Board_Page_Button_Click"]),
                    # "texts": ["Das Programm webMobaLedLib selbst aktualisieren: Menü Hilfe → Update webMobaLedLib …"]})  # v1.07 (entfallen)
                    # "texts": ["Das Programm webMobaLedLib selbst aktualisieren: Menü Hilfe → Update webMobaLedLib …"],  # v1.07  # v5.09 (entfallen)
                    "texts": ["Das Programm MobaLedLib Studio selbst aktualisieren: Menü Hilfe → Update MobaLedLib Studio …"],  # v1.07  # v5.09
                    "ide_only": True})                               # nur mit der ARDUINO IDE (Bibliotheken und Boards aktualisieren)  # v1.07
                wlan_inst = "WLAN" in buildopt
                fw_btn = {"text": tr("Firmware installieren"), "handler": "__Boot_Firmware_Button_Click", "disabled": False,  # v1.43 (vorher im Reiter Lichtmaschine)
                          "label": tr("Schreibt eine fertige Firmware (UF2-Datei aus dem Ordner MobaLedLib/firmware) auf den Raspberry Pi Pico")}  # v1.43
                # tabs.append({"name": M09.Get_Language_Str("Bootloader"), "kind": "list", "buttons": tab_buttons(  # v1.43 (entfallen)
                tabs.append({"name": tr("Firmware Installation"), "kind": "list", "buttons": [fw_btn] + tab_buttons(  # v1.43

                    # buttons, ["__WLAN_Pico_Button_Click"] if wlan_inst else ["__FastBootloader_Button_Click"])})  # v1.07 (entfallen)
                    buttons, ["__WLAN_Pico_Button_Click"] if wlan_inst else ["__FastBootloader_Button_Click"]),  # v1.07
                    # "ide_only": not wlan_inst})                      # der schnelle Bootloader braucht ArduinoISP und avrdude der IDE; der Knopf fuer den WLAN-Pico nur eine Webseite  # v1.17 (entfallen)
                    "ide_only": False})                      # der schnelle Bootloader braucht ArduinoISP und avrdude der IDE; der Knopf fuer den WLAN-Pico nur eine Webseite  # v1.17
            lower = [dict(buttons[h][0], handler=h) for h in ("__HardiForum_Button_Click", "__Close_Button_Click") if h in buttons]
            # return {"title": M09.Get_Language_Str("Optionen und spezielle Funktionien"), "tabs": tabs,  # v1.22 (entfallen: Schreibfehler)
            if beginner:  # v1.44: im Anfaenger Modus fehlen die Reiter Entwicklungsumgebung und Firmware Installation
                tabs = [t_ for t_ in tabs if t_["name"] not in (tr("Entwicklungsumgebung"), tr("Firmware Installation"))]  # v1.44
            # return {"title": M09.Get_Language_Str("Optionen und spezielle Funktionen"), "tabs": tabs,  # v1.22  # v1.44 (entfallen)
            view = VIEW["only"]  # v1.75: Menue Werkzeuge (Issue 75)
            names_ide = (tr("Entwicklungsumgebung"), M09.Get_Language_Str("Update"))  # v1.75
            names_fw = (tr("Firmware Installation"),)  # v1.75
            if view == "wartung":  # v1.75
                tabs = [t_ for t_ in tabs if t_["name"] in names_ide]  # v1.75
            elif view == "firmware":  # v1.75
                tabs = [t_ for t_ in tabs if t_["name"] in names_fw]  # v1.75
            else:  # v1.75: die Hardware Optionen enthalten diese Reiter nicht mehr
                tabs = [t_ for t_ in tabs if t_["name"] not in names_ide + names_fw]  # v1.75
            if view and not tabs:  # v1.75: nichts anzuzeigen (zum Beispiel Anfaenger Modus): alle Reiter wie bisher
                view = None  # v1.75
                VIEW["only"] = None  # v1.75
            # return {"title": tr("Hardware Optionen"), "tabs": tabs,  # v1.44  # v1.75 (entfallen)
            return {"title": tr({"wartung": "Wartung", "firmware": "Firmware installieren"}.get(view, "Hardware Optionen")), "tabs": tabs, "view": view,  # v1.75
                    "pages": pages, "lower": lower}

        def _web_ensure_text(self, left):
            """Die Handler des Originals rufen InStr(Zelle.Value, ...) auf; bei einer leeren Zelle ist
            Value None und InStr bricht ab (das gilt auch fuer das Tk-Original). Daher leere Zelle -> ''."""
            cell = P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL if left else M25.BUILDOpRCOL)
            if cell.Value is None:
                cell.Value = ""

        def _web_apply(self, vals, initial):
            """Aenderungen von Autodetect und Board wie die Klick-Handler des Originals ausfuehren."""
            if vals.get("ext_changed"):  # v1.31: Erweiterungen ein- oder ausgeschaltet: die Makros neu einlesen
                try:  # v1.31
                    import proggen.M38_Extensions as M38  # v1.31
                    M38.Load_Extensions()  # v1.31
                except Exception:                                      # noqa: BLE001  # v1.31
                    logger.exception("Optionen: Erweiterungen konnten nicht neu eingelesen werden")  # v1.31
            if vals["esp32_options"] != initial["esp32_options"]:  # v1.30
                P01.ActiveSheet.esp32_options = dict(vals["esp32_options"])  # v1.30
            if "serial_cfg" in vals and vals["serial_cfg"] != initial.get("serial_cfg"):  # v1.32
                import proggen.M42_Dyn_Config as M42  # v1.32
                # M42.Set_Option(vals["serial_cfg"])  # v1.32  # v1.55 (entfallen: global)
                M42.Set_Sheet_Option(vals["serial_cfg"])  # v1.55: im Blatt
            from headless import headless_sheet_settings as HSS  # v1.55: Lichtsensor und Schaltzustaende als Makrozeilen des Blattes setzen oder entfernen
            for key_, text_ in (("ldr", "Lichtsensor aktivieren"), ("store_status", "Schaltzustände speichern")):  # v1.55
                if key_ in vals and vals[key_] != initial.get(key_):  # v1.55
                    try:  # v1.55
                        HSS.apply(key_, vals[key_], description=tr(text_))  # v1.55
                    except Exception:                                  # noqa: BLE001  # v1.55
                        logger.exception("Optionen: Einstellung %s nicht ins Blatt uebernommen", key_)  # v1.55
            try:  # v1.55: fruehere Eintraege in esp32_options (ldr, store_status) in Makrozeilen uebernehmen
                HSS.migrate_legacy()  # v1.55
            except Exception:                                          # noqa: BLE001  # v1.55
                logger.exception("Optionen: fruehere Einstellungen nicht uebernommen")  # v1.55
            if vals.get("protocol") and vals["protocol"] != initial.get("protocol"):  # v1.49: Protokoll (Page-ID) des Blattes
                # P01.CellDict[M02.SH_VARS_ROW, M02.PAGE_ID_COL] = vals["protocol"]  # v1.49  # v1.68 (entfallen: steht in _web_set_protocol)
                # M25.Page_ID = vals["protocol"]  # v1.49  # v1.68 (entfallen)
                # logger.info("Optionen: Protokoll des Blattes auf %s gestellt", vals["protocol"])  # v1.49  # v1.68 (entfallen)
                self._web_set_protocol(initial.get("protocol"), vals)  # v1.68
            self.rb_res["_L"].set(vals["L"] or 0)
            self.rb_res["_R"].set(vals["R"] or 0)
            self.Autodetect_Typ_L_CheckBox_var.set(1 if vals["auto_L"] else 0)
            self.Autodetect_Typ_R_CheckBox_var.set(1 if vals["auto_R"] else 0)
            logger.info("Optionen: Zustand vorher %s, nachher %s", initial, vals)
            if "use_pio" in vals and vals["use_pio"] != initial.get("use_pio"):  # v1.04
                import proggen.M28_Diverse as M28  # v1.04
                M28.Set_String_Config_Var("Use_PlatformIO", "1" if vals["use_pio"] else "0")           # Config: PlatformIO Build verwenden  # v1.04
                M02.Sketchbook_Path = ""                                  # der Sketchbook-Pfad der neuen Entwicklungsumgebung wird neu bestimmt (Python-Ordner oder preferences.txt der IDE)  # v1.07
                self._web_switched_to_ide = not vals["use_pio"]  # v1.07
            if vals["auto_L"] != initial["auto_L"]:
                self._web_ensure_text(True)
                getattr(self, PFX + "__Autodetect_Typ_L_CheckBox_Click")()     # inkl. Check_Board
            if vals["auto_R"] != initial["auto_R"]:
                self._web_ensure_text(False)
                getattr(self, PFX + "__Autodetect_Typ_R_CheckBox_Click")()
            if vals["L"] != initial["L"] and self.rb_res["_L"].get():
                self.Change_Board(True, self.boardlist[self.rb_res["_L"].get()])
                self._web_board_changed(True, keep_port=initial["L"] is not None and self._is_nano_value(initial["L"]) and self._is_nano_value(vals["L"]))  # v1.23  # v1.49: Variante eines Nano: der Anschluss bleibt
            if vals["R"] != initial["R"] and self.rb_res["_R"].get():
                self.Change_Board(False, self.boardlist[self.rb_res["_R"].get()])
                self._web_board_changed(False)  # v1.23

        def _web_set_protocol(self, old_pid, vals):  # v1.68
            """Protokoll des Blattes umstellen. Zwischen Selectrix und DCC/LNet/CAN aendern sich die Spalten: dann werden die Adressen umgerechnet, mit vorheriger Rueckfrage,
            wenn das Blatt Adressen (keine Variablen) enthaelt. Antwort Nein: das Protokoll bleibt, wie es war."""
            from headless import headless_protocol_switch as PS  # v1.68
            new_pid = vals["protocol"]  # v1.68
            if not PS.crosses(old_pid, new_pid):  # v1.68: DCC, LNet und CAN haben dieselben Spalten
                P01.CellDict[M02.SH_VARS_ROW, M02.PAGE_ID_COL] = new_pid  # v1.49
                M25.Page_ID = new_pid  # v1.49
                logger.info("Optionen: Protokoll des Blattes auf %s gestellt", new_pid)  # v1.49
                return  # v1.68
            ws = P01.ActiveSheet  # v1.68
            info = PS.analyze(ws, old_pid)  # v1.68
            if info["addresses"]:  # v1.68
                if P01.MsgBox(PS.warning_text(info, old_pid, new_pid, tr), vbQuestion + vbYesNo, tr("Protokoll umstellen")) != vbYes:  # v1.68
                    vals["protocol"] = old_pid  # v1.68
                    logger.info("Optionen: Wechsel des Protokolls %s -> %s abgebrochen", old_pid, new_pid)  # v1.68
                    return  # v1.68
            try:  # v1.68
                PS.convert(ws, new_pid)  # v1.68
            except Exception as ex:                                    # noqa: BLE001  # v1.68
                logger.exception("Optionen: Protokoll konnte nicht umgestellt werden")  # v1.68
                vals["protocol"] = old_pid  # v1.68
                P01.MsgBox(tr("Das Protokoll konnte nicht umgestellt werden: {ex}", ex=ex), vbCritical, tr("Protokoll umstellen"))  # v1.68

        def _web_board_changed(self, left, keep_port=False):  # v1.23  # v1.49: keep_port
            """Der Arduino-Typ wurde gewechselt: eine bestehende serielle Verbindung trennen und den gewaehlten COM Port zuruecksetzen. Beim naechsten Setup uebertragen startet dann
            die Port-Erkennung (port_is_available(' ') ist falsch) und es kommt nicht die Meldung 'Es ist kein ... an COM ... angeschlossen'."""  # v1.23
            try:  # v1.23
                import mlpyproggen.Prog_Generator as PG  # v1.23
                if PG.global_controller.is_connection_open():  # v1.23
                    PG.global_controller.disconnect()  # v1.23
            except Exception:                                  # noqa: BLE001  # v1.23
                logger.debug("Trennen beim Typwechsel fehlgeschlagen", exc_info=True)  # v1.23
            try:  # v1.23
                if keep_port:  # v1.49
                    return  # v1.49
                P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL if left else M25.COMPrtR_COL).Value = " "  # v1.23
            except Exception:                                  # noqa: BLE001  # v1.23
                logger.debug("COM Port nicht zurueckgesetzt", exc_info=True)  # v1.23
            logger.info("Optionen: Arduino-Typ links/rechts gewechselt (%s): Verbindung getrennt, COM Port zurueckgesetzt", "links" if left else "rechts")  # v1.23

        def _web_detect_board(self, left):  # v1.25  # v1.26  # v1.27 (Board und USB Port erkennen)
            """Knopf 'Board und USB Port erkennen': sucht unter allen seriellen Anschluessen nach einem Arduino. Beim ersten gefundenen Board wird dieses
            eingestellt und 'USB Port erkennen' aufgerufen; das Formular zeigt das gefundene Board mit Anschluss und wie bisher die anderen gefundenen Boards.
            ESP32 (CP210x) und Pico nach der Beschreibung des Anschlusses, bei einem Nano ueber den Bootloader: 57600 Baud alt, 115200 Baud neu."""
            import re  # v1.26
            import proggen.M07_COM_Port as M07  # v1.25
            import proggen.M08_ARDUINO as M08  # v1.25
            try:  # v1.25: eine bestehende Verbindung des Programms belegt den Anschluss
                import mlpyproggen.Prog_Generator as PG  # v1.25
                if PG.global_controller.is_connection_open():  # v1.25
                    PG.global_controller.disconnect()  # v1.25
            except Exception:                                  # noqa: BLE001  # v1.25
                logger.debug("Trennen vor dem Erkennen fehlgeschlagen", exc_info=True)  # v1.25
            cands = []  # v1.26: [(Anschluss, Typ)]
            try:  # v1.26
                from serial.tools import list_ports as portlist  # v1.26
                for cp in portlist.comports(include_links=False):  # v1.26
                    if os.name != "nt" and re.match(r"^/dev/ttyS\d+$", str(cp.device)) and str(cp.hwid).strip().lower() in ("n/a", ""):  # v1.26
                        continue  # v1.26
                    t = M07.Classify_Port(cp)  # v1.26
                    # v1.70: keine serielle Abfrage beim Erkennen (nur USB-Kennung); Servo-Module erkennt der Dialog im Hintergrund
                    if t and t != "Servo":  # v1.26  # v1.69: Servo-Module werden nicht als Board angeboten
                        cands.append((str(cp.device), t))  # v1.26
            except Exception:                                  # noqa: BLE001  # v1.26
                logger.debug("Anschlussliste nicht lesbar", exc_info=True)  # v1.26
            def _num(x):  # v1.27: wie im Formular nach der Nummer des Anschlusses sortiert
                m = re.search(r"(\d+)$", x[0])  # v1.27
                return (int(m.group(1)) if m else 0, x[0])  # v1.27
            cands.sort(key=_num)  # v1.27
            if not cands:  # v1.26
                P01.MsgBox(tr("Es wurde kein angeschlossener Arduino gefunden. Bitte den Arduino per USB anschließen und noch einmal „Board und USB Port erkennen“ drücken."), vbCritical, tr("Board und USB Port erkennen"))  # v1.26  # v1.27
                return  # v1.26
            # dev, typ = cands[0]  # v1.27 (entfallen v1.34: bei zwei Arduinos (Lichtmaschine und LNet/DCC) wurde so der Anschluss der anderen Seite genommen und dessen Board eingestellt)
            def _stored_port(col):  # v1.34: gespeicherter Anschluss einer Seite als Geraetename, "" wenn keiner
                try:  # v1.34
                    raw = str(P01.Cells(M02.SH_VARS_ROW, col)).strip().lstrip("*").strip()  # v1.34
                except Exception:                              # noqa: BLE001  # v1.34
                    return ""  # v1.34
                if raw.startswith("-") and raw[1:].isdigit():  # v1.71: negative Zahl = belegter Port, kein Anschluss
                    return ""  # v1.71
                if raw.isdigit():  # v1.34: Nummer: unter Windows COM<n>
                    return ("COM" + raw) if os.name == "nt" else ""  # v1.34
                return raw if raw.upper() not in ("COM?", "NO DEVICE") and not raw.upper().startswith("IP:") else ""  # v1.34
            own_port = _stored_port(M25.COMPort_COL if left else M25.COMPrtR_COL)  # v1.34
            other_port = _stored_port(M25.COMPrtR_COL if left else M25.COMPort_COL)  # v1.34
            logger.info("Erkennen: Seite %s, eigener Anschluss '%s', Anschluss der anderen Seite '%s', gefunden %s", "Lichtmaschine" if left else "LNet/DCC", own_port, other_port, cands)  # v1.34
            rest = [c for c in cands if not (other_port and c[0].upper() == other_port.upper())]  # v1.34: den Anschluss der anderen Seite auslassen
            if rest:  # v1.34
                cands = rest  # v1.34
            if len(set(t for _, t in cands)) > 1:  # v1.48: mehrere Board-Typen gefunden: den gewuenschten Typ waehlen lassen (Pull Request 39, Issue 35)
                selected_type = _choose_detected_board_type(cands, light_machine=left)  # v1.48
                if selected_type is None:  # v1.48
                    logger.info("Erkennen: Auswahl des Board-Typs abgebrochen")  # v1.48
                    return  # v1.48
                cands = [candidate for candidate in cands if candidate[1] == selected_type]  # v1.48
            own = [c for c in cands if own_port and c[0].upper() == own_port.upper()]  # v1.34: der gespeicherte eigene Anschluss hat Vorrang
            dev, typ = (own or cands)[0]  # v1.34
            if typ == "ESP32":  # v1.26
                new_board = M02.BOARD_ESP32  # v1.26
            elif typ == "Pico":  # v1.26
                new_board = M02.BOARD_PICO  # v1.26
            else:  # v1.26: Nano: Bootloader ansprechen
                baud = M07.Get_Arduino_Baudrate(dev, 115200, 0, "")  # v1.26: probiert auch die andere Baudrate
                logger.info("Erkennen: COM Port %s, Baudrate %s", dev, baud)  # v1.26
                if baud == 57600:  # v1.26
                    new_board = M02.BOARD_NANO_OLD  # v1.26
                elif baud == 115200:  # v1.26
                    # new_board = M08.Get_New_Board_Type("", 0)  # v1.26 (entfallen v1.37: ohne Firmware-Version wurde nie Nano Full erkannt, Issue 14)
                    _fw, _sig = M07.Get_Last_Detect_Info()  # v1.37
                    logger.info("Erkennen: Bootloader-Firmware '%s', Signatur 0x%06X", _fw, _sig)  # v1.37
                    new_board = M08.Get_New_Board_Type(_fw, _sig)  # v1.37
                else:  # v1.27: Bootloader antwortet nicht: das Formular zeigt trotzdem den Anschluss; das Board bleibt unveraendert
                    new_board = None  # v1.27
            if new_board:  # v1.27
                M28pio.Change_Board_Typ(left, new_board)  # v1.25
                try:  # v1.35: auch die Auswahl des Formulars setzen. Sonst liest USB Port erkennen die alte Auswahl und ueberschreibt das erkannte Board (Issue 13)
                    idx = list(self.boardlist).index(new_board)  # v1.35
                    self.rb_res["_L" if left else "_R"].set(idx)  # v1.35
                except (ValueError, KeyError, AttributeError):  # v1.35
                    logger.warning("Erkennen: Board %s steht nicht in der Boardliste", new_board)  # v1.35
                logger.info("Erkennen: Board %s eingestellt (COM Port %s)", new_board, dev)  # v1.26
            # USB Port erkennen aufrufen: zeigt das Formular mit dem gefundenen Board und Anschluss und die anderen gefundenen Boards  # v1.27
            getattr(self, PFX + ("__Detect_LED_Port_Button_Click" if left else "__Detect_Right_Port_Button_Click"))()  # v1.27
            if left:  # v1.36: wurde ein Anschluss eingetragen, nach dem Schliessen des Fensters verbinden
                try:  # v1.36
                    import mlpyproggen.Prog_Generator as PG  # v1.36
                    port = str(PG.global_controller.getConfigData("serportname") or "").strip()  # v1.36
                    self._web_auto_connect = port != "" and port.upper() not in ("NO DEVICE", "COM?")  # v1.36
                except Exception:                              # noqa: BLE001  # v1.36
                    logger.debug("Anschluss nach dem Erkennen nicht gelesen", exc_info=True)  # v1.36

        def _web_ide_libs_question(self):  # v1.07
            """Zurueck auf die ARDUINO IDE: Gibt es sie, und sollen die Bibliotheken und Boards jetzt geprueft werden (beim Start war das wegen PlatformIO entfallen)?"""  # v1.07
            import proggen.M08_ARDUINO as M08  # v1.07
            import proggen.M37_Inst_Libraries as M37mod  # v1.07
            if M08.Find_ArduinoExe() == "":  # v1.07
                P01.MsgBox(M09.Get_Language_Str('Die ARDUINO IDE wurde nicht gefunden. Entweder wurde ARDUINO noch nicht installiert (Windows) oder das ARDUINO-Verzeichnis wurde noch nicht eingegeben (LINUX/Mac)'), vbCritical, M09.Get_Language_Str('ARDUINO IDE nicht gefunden'))  # v1.07
                return  # v1.07
            if P01.MsgBox(tr("Die ARDUINO IDE ist jetzt die Entwicklungsumgebung. Sollen die Bibliotheken und Boards jetzt geprüft werden?"), vbYesNo + vbQuestion, tr("Entwicklungsumgebung")) == vbYes:  # v1.07
                M37mod.Install_Missing_Libraries_and_Board()  # v1.07

        def _web_check_pio(self):  # v1.04
            """Knopf PlatformIO pruefen: Ist pio installiert? Welche Version?"""  # v1.04
            import proggen.M08_ARDUINO as M08  # v1.04
            pio = M08.Find_PIO()  # v1.04
            if not pio:  # v1.04
                P01.MsgBox(tr("PlatformIO wurde nicht gefunden.") + "\n\n" +  # v1.04
                           # tr("Installation: https://platformio.org/install/cli (zum Beispiel mit: pip install platformio). Danach findet das Programm pio selbst."), ns["vbInformation"], "PlatformIO")  # v1.05 (entfallen)
                           tr("Installation: {hinweis}. Danach findet das Programm pio selbst.", hinweis=tr(M08.PIO_Install_Hint())), ns["vbInformation"], "PlatformIO")  # v1.05
                return  # v1.04
            version = M08.PIO_Version(pio)  # v1.04
            P01.MsgBox((version or tr("PlatformIO ist vorhanden, antwortet aber nicht.")) + "\n" + pio, ns["vbInformation"] if version else vbCritical, "PlatformIO")  # v1.04

        def _web_import_info(self):  # v1.29
            """Knopf Importieren v. altem Prog.: erklaert, wie Daten des Excel-Programms ueber eine MLL_pgf-Datei uebernommen werden"""  # v1.29
            P01.MsgBox(tr("So übernimmst du die Daten des alten Excel-Programms:") + "\n\n"  # v1.29
                       + tr("1. Öffne im alten Programm Optionen und spezielle Funktionen, Reiter Dateien, und klicke auf Speichern in Datei. Speichere die Daten (alle Seiten oder die Seiten, die du brauchst) als Datei mit der Endung MLL_pgf.") + "\n"  # v1.29
                       + tr("2. Öffne hier das Menü Datei und wähle ProgrammGenerator: PGF-Datei lesen. Du kannst die Datei auch auf die Tabelle ziehen.") + "\n"  # v1.29
                       + tr("3. Prüfe danach die Tabelle, zum Beispiel die Spalten Verteiler-Nr. und Aktiv.") + "\n\n"  # v1.29
                       + tr("Mehr dazu in der Online-Anleitung (Hilfe, Online Wiki), Seite Häufige Fragen."), ns["vbInformation"], tr("Importieren v. altem Prog."))  # v1.29

        def _web_pico_udev(self):  # v1.05
            """Knopf USB-Zugriff fuer den Pico einrichten (Linux): udev-Regel mit pkexec einrichten (install/install_pico_udev.sh)"""  # v1.05
            import proggen.M08_ARDUINO as M08  # v1.05
            if M08.Pico_Udev_Ok():  # v1.05
                P01.MsgBox(tr("Es gibt schon eine Regel für den USB-Zugriff auf den Raspberry Pi Pico."), ns["vbInformation"], "PlatformIO")  # v1.05
                return  # v1.05
            ok, text = M08.Setup_Pico_Udev()  # v1.05
            if ok:  # v1.05
                P01.MsgBox(tr("Die Regel für den USB-Zugriff auf den Pico ist eingerichtet. Bitte den Pico neu anstecken (BOOTSEL-Taste gedrückt halten) und das Hochladen wiederholen. Nach dem nächsten An- und Abmelden gilt es auch für Programme außerhalb dieser Sitzung."), ns["vbInformation"], "PlatformIO")  # v1.05
            else:  # v1.05
                P01.MsgBox(tr("Die Regel konnte nicht eingerichtet werden.") + "\n\n" + text, vbCritical, "PlatformIO")  # v1.05

        def _web_pio_cache(self):  # v1.16
            """Knopf PlatformIO-Zwischenspeicher löschen: nach Rückfrage den Ordner .pio der Projekte dieses Programms und den Download-Zwischenspeicher von PlatformIO löschen;
            das nächste Übersetzen baut alles neu auf (PlatformIO behält sonst Kopien der Bibliothek MobaLedLib, auch wenn sich eine .h-Datei geändert hat)"""
            import proggen.M08_ARDUINO as M08  # v1.16
            import headless.headless_pio_cache as HC  # v1.16
            title = tr("PlatformIO-Zwischenspeicher löschen")  # v1.16
            plan = M08.PIO_Cache_Plan()  # v1.16
            if not plan:  # v1.16
                P01.MsgBox(tr("Es gibt nichts zu löschen: PlatformIO hat noch keinen Zwischenspeicher angelegt."), ns["vbInformation"], title)  # v1.16
                return  # v1.16
            lines = []  # v1.16
            for entry in plan:  # v1.16
                if entry["kind"] == "project":  # v1.16
                    lines.append("  " + tr("Übersetzte Dateien und Kopien der Bibliotheken im Projekt: {pfad} ({groesse})", pfad=entry["path"], groesse=HC.human_size(entry["size"])))  # v1.16
                else:  # v1.16
                    lines.append("  " + tr("Download-Zwischenspeicher von PlatformIO: {pfad} ({groesse})", pfad=entry["path"], groesse=HC.human_size(entry["size"])))  # v1.16
            question = (tr("Der Zwischenspeicher von PlatformIO wird gelöscht, damit beim nächsten Übersetzen alles neu aufgebaut wird (zum Beispiel nach einer Änderung der Bibliothek MobaLedLib):")  # v1.16
                        + "\n\n" + "\n".join(lines) + "\n\n"  # v1.16
                        + tr("Die Plattformen und Compiler von PlatformIO bleiben erhalten. Das nächste Übersetzen dauert länger, weil die Bibliotheken neu geholt werden. Fortfahren?"))  # v1.16
            if P01.MsgBox(question, ns.get("vbYesNo", 4) + ns.get("vbQuestion", 32), title) != ns.get("vbYes", 6):  # v1.16
                return  # v1.16
            busy = wd.show_busy(tr("Der Zwischenspeicher von PlatformIO wird gelöscht ..."), title)  # v1.16
            try:  # v1.16
                result = M08.PIO_Cache_Clean(plan)  # v1.16
            finally:  # v1.16
                wd.hide_busy(busy)  # v1.16
            if not result["failed"]:  # v1.16
                P01.MsgBox(tr("Der Zwischenspeicher wurde gelöscht ({groesse} freigegeben). Das nächste Übersetzen baut alles neu auf.", groesse=HC.human_size(result["freed"])), ns["vbInformation"], title)  # v1.16
                return  # v1.16
            details = "\n".join("  %s: %s" % (entry["path"], message) for entry, message in result["failed"])  # v1.16
            P01.MsgBox(tr("Nicht alles konnte gelöscht werden:") + "\n\n" + details + "\n\n" + tr("Läuft gerade ein Übersetzen oder ist eine Datei geöffnet? Bitte danach noch einmal versuchen."), vbCritical, title)  # v1.16

        def _web_install_git(self):  # v1.13
            # """Knopf Git installieren (Linux): git mit pkexec installieren (install/install_git.sh); PlatformIO braucht den Git-Client fuer den Pico"""  # v1.15 (entfallen)
            """Knopf Git installieren: Linux pkexec mit install/install_git.sh, Windows winget oder das Installationsprogramm von Git for Windows, macOS Homebrew oder die Entwicklerwerkzeuge
            von Apple (siehe headless/headless_git.py); PlatformIO braucht den Git-Client fuer den Pico"""
            import proggen.M08_ARDUINO as M08  # v1.13
            if M08.Git_Installed():  # v1.13
                P01.MsgBox(tr("git ist schon installiert."), ns["vbInformation"], "PlatformIO")  # v1.13
                return  # v1.13
            # ok, text = M08.Setup_Git()  # v1.14 (entfallen)
            # busy = wd.show_busy(tr("Git wird installiert. Das Betriebssystem fragt gleich nach dem Passwort. Die Installation kann mehrere Minuten dauern, bitte warten ..."), tr("Git installieren"))  # v1.15 (entfallen)
            busy = wd.show_busy(tr(HG.busy_text()), tr("Git installieren"))  # v1.15
            try:  # v1.14
                ok, text = M08.Setup_Git()  # v1.14
            finally:  # v1.14
                wd.hide_busy(busy)  # v1.14
            # if ok:  # v1.15 (entfallen)
            if ok is None:                                  # macOS: die Installation der Entwicklerwerkzeuge laeuft im Hintergrund weiter (Fenster von macOS)  # v1.15
                P01.MsgBox(text, ns["vbInformation"], "PlatformIO")  # v1.15
            elif ok:  # v1.15
                P01.MsgBox(tr("git ist installiert. Das Übersetzen für den Raspberry Pi Pico kann jetzt wiederholt werden."), ns["vbInformation"], "PlatformIO")  # v1.13
            else:  # v1.13
                P01.MsgBox(tr("git konnte nicht installiert werden.") + "\n\n" + text, vbCritical, "PlatformIO")  # v1.13

        def _firmware_available(self):  # v1.11
            """Liegt im Ordner MobaLedLib/firmware (Sketchbook-Ordner) mindestens eine Datei *.uf2?"""  # v1.11
            try:  # v1.11
                import headless.headless_pico as HP  # v1.11
                import proggen.M02a_Public as M02a  # v1.11
                return bool(HP.has_firmware(M02a.Get_FirmwareDir()))  # v1.11
            except Exception:                                                          # noqa: BLE001  # v1.11
                logger.debug("Firmware-Ordner nicht geprueft", exc_info=True)  # v1.11
                return False  # v1.11

        def _web_pico_firmware(self):  # v1.09
            """Knopf Firmware installieren (nur Pico): Firmware und Version waehlen, dann die UF2-Datei auf den Pico schreiben (Bootmodus-Laufwerk RPI-RP2 oder
            ueber den seriellen Anschluss in den Bootmodus versetzen, wie uf2conv.py im Excel-Programm)."""
            import headless.headless_pico as HP  # v1.09
            import proggen.M02a_Public as M02a  # v1.09
            from _web import web_form_firmware as WFF  # v1.09
            from _web.web_i18n import current_language  # v1.09
            title = tr("Firmware installieren")  # v1.09
            # folder = M02a.Get_FirmwareDir()  # v1.11 (entfallen)
            folder = HP.resolve_firmware_dir(M02a.Get_FirmwareDir())                      # auch Firmware statt firmware (Linux)  # v1.11
            try:  # v1.18: wie CreateFolder Get_FirmwareDir() im Excel-Programm 3.5.0L3
                os.makedirs(folder, exist_ok=True)  # v1.18
            except OSError:                                                            # noqa: BLE001  # v1.18
                logger.debug("Firmware-Ordner nicht angelegt", exc_info=True)  # v1.18
            lang_id = HP.language_id(current_language())  # v1.19
            groups = HP.scan_firmware(folder, lang_id)  # v1.09
            # if not groups:  # v1.09 (entfallen v1.19: die Auswahl oeffnet auch ohne Firmware-Dateien, mit Hinweis und dem Knopf Firmware laden)
            #     P01.MsgBox(tr("Im Ordner {ordner} gibt es keine Firmware-Dateien (*.uf2). Die fertigen Firmware-Dateien gehören in diesen Ordner (Unterordner MobaLedLib/firmware des Sketchbook-Ordners).", ordner=folder),  # v1.09
            #                ns.get("vbInformation", 64), title)  # v1.09
            #     return  # v1.09
            import headless.headless_firmware_dl as HFD  # v1.19
            from _web import web_form_firmware_download as WFD  # v1.19
            download_texts = WFD.translated_texts(M09.Get_Language_Str)                  # im Worker-Thread uebersetzen (Sprachtabelle des Excel-Programms)  # v1.19
                        # fw_texts = {"download": M09.Get_Language_Str("Firmware laden")}  # v1.19 (entfallen)
            fw_texts = {"download": M09.Get_Language_Str("Firmware herunterladen")}  # v1.21

            async def download():  # v1.19: Dialog Firmware Herunterladen (Liste von GitHub, Download, Entpacken)
                return await WFD.firmware_download_async(folder, download_texts, HFD.language_code(current_language()))  # v1.19

            def rescan():  # v1.19: den Ordner nach dem Herunterladen neu einlesen
                return HP.scan_firmware(folder, lang_id)  # v1.19
            # path = wd.call_in_loop(WFF.firmware_async, groups, folder, default=None)  # v1.09 (entfallen)
            path = wd.call_in_loop(WFF.firmware_async, groups, folder, download, rescan, fw_texts, default=None)  # v1.19
            if not path:  # v1.09
                return  # v1.09
            serial_port = None  # v1.47 (Issue 58): nicht der Anschluss des Blatts (dort haengt die Lichtmaschine), sondern ein eigener, immer erfragter Pico-Anschluss
            if not HP.find_boot_drives():  # v1.47: ein Pico im Bootmodus (Laufwerk RPI-RP2) braucht keinen Anschluss
                # Die Geraeteauswahl der Lichtmaschine mit anderen Regeln (v1.76): nur Pico-Geraete, auch unbekannte und andere MobaLedLib Geraete sind waehlbar; das Blatt bleibt unveraendert
                import mlpyproggen.Prog_Generator as PG_  # v1.47
                import proggen.F00_mainbuttons as F00_  # v1.76
                ctrl_ = PG_.global_controller  # v1.47
                connected = ""  # v1.47
                try:  # v1.47
                    if ctrl_.is_connection_open():  # v1.47
                        connected = str(getattr(ctrl_, "ARDUINO_current_portname", "") or "").strip()  # v1.47
                except Exception:                                  # noqa: BLE001  # v1.47
                    connected = ""  # v1.47
                serial_port = F00_.Select_COM_Port_UserForm.SelectPicoDevice(M09.Get_Language_Str("Geräteauswahl", False, M09.xlWhole), _FW_PORT["port"])  # v1.76
                if not serial_port:  # v1.47
                    return  # v1.47
                _FW_PORT["port"] = serial_port  # v1.47
                if connected and serial_port.upper() == connected.upper():  # v1.47: der gewaehlte Anschluss ist die verbundene Lichtmaschine: Verbindung vorher trennen
                    try:  # v1.47
                        ctrl_.disconnect()  # v1.47
                    except Exception:                              # noqa: BLE001  # v1.47
                        logger.debug("Trennen vor der Firmware nicht moeglich", exc_info=True)  # v1.47
            try:  # v1.09
                # HP.flash_uf2(path, log=lambda text: logger.info("%s", text))  # v1.09  # v1.47 (entfallen)
                HP.flash_uf2(path, serial_port=serial_port, log=lambda text: logger.info("%s", text))  # v1.47
            except RuntimeError as ex:  # v1.09
                P01.MsgBox(tr(str(ex)), vbCritical, title)  # v1.09
                return  # v1.09
            P01.MsgBox(tr("Die Firmware {datei} wurde auf den Pico geschrieben. Der Pico startet jetzt neu.", datei=os.path.basename(path)), ns.get("vbInformation", 64), title)  # v1.09

        def _web_loop(self, first_page_only):
            while True:
                initial = self._web_prepare(first_page_only)
                spec = self._web_spec(first_page_only)
                res = wd.call_in_loop(_options_async, spec, initial, default=None)
                if res is None:
                    break
                _kind, handler, vals = res
                self._web_switched_to_ide = False  # v1.07
                self._web_apply(vals, initial)
                if self._web_switched_to_ide:  # v1.07
                    self._web_switched_to_ide = False  # v1.07
                    self._web_ide_libs_question()  # v1.07
                self._web_hidden = False
                self._web_reshow = False
                if handler in ("__Detect_Board_L", "__Detect_Board_R"):    # Knopf Erkennen (gibt es nur im Web)  # v1.25
                    _TAB["keep"] = True  # v1.35: danach auf dem Reiter dieser Seite weitermachen
                    try:  # v1.25
                        self._web_detect_board(handler.endswith("L"))  # v1.25
                    except Exception as ex:                                # noqa: BLE001  # v1.25
                        logger.exception("Optionen: Board erkennen fehlgeschlagen")  # v1.25
                        P01.MsgBox("Aktion fehlgeschlagen: " + str(ex), vbCritical, "Optionen")  # v1.25
                    continue  # v1.25
                if handler == "__Check_PIO_Button_Click":                 # gibt es nur im Web (kein Knopf des Originals)  # v1.04
                    self._web_check_pio()  # v1.04
                    continue  # v1.09
                if handler == "__Boot_Firmware_Button_Click":             # Firmware des Pico installieren (Version K des Excel-Programms)  # v1.09
                    self._web_pico_firmware()  # v1.09
                    continue  # v1.05
                if handler == "__Pio_Cache_Button_Click":                 # gibt es nur im Web (kein Knopf des Originals)  # v1.16
                    self._web_pio_cache()  # v1.16
                    continue  # v1.16
                if handler == "__Install_Git_Button_Click":               # gibt es nur im Web, nur unter Linux, nur wenn git fehlt  # v1.13
                    self._web_install_git()  # v1.13
                    continue  # v1.13
                if handler == "__Import_Button_Click":                    # v1.29: Anleitung statt Import aus der Excel-Datei
                    self._web_import_info()  # v1.29
                    continue  # v1.29
                if handler == "__Pico_Udev_Button_Click":                 # gibt es nur im Web, nur unter Linux  # v1.05
                    self._web_pico_udev()  # v1.05
                    continue  # v1.04
                try:
                    getattr(self, PFX + handler)()
                except Exception as ex:                                  # noqa: BLE001
                    logger.exception("Optionen: Aktion %s fehlgeschlagen", handler)
                    P01.MsgBox("Aktion fehlgeschlagen: " + str(ex), vbCritical, "Optionen")
                    continue
                if handler == "__Close_Button_Click":
                    break
                if self._web_reshow or not self._web_hidden:
                    continue
                break

    WebOptions.__name__ = Base.__name__          # fuer das Name Mangling der geerbten privaten Methoden
    return WebOptions
