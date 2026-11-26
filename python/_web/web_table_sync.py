# Datei-Version: 1.10 (2026-11-26) - web_table_sync.py
# Name: web_table_sync.py
# Path: _web/web_table_sync.py
# Version: 1.10
# Last Update: 2026-11-26
# Author: Harold Linke
# Licence: LGPL V2.1
# History of Change:
#   1.10 2026-11-26 Mindestlaenge des Verbindungscodes sechs statt zwoelf Zeichen; bestehende Codes unveraendert.
#   1.09 2026-11-26 IP-/Port-Anzeige auf Basis 5.41 separat bereitgestellt; Backend und M08 unveraendert.
#   1.09 2026-11-25 Quelladresse ohne HTTP-Praefix und separates Portfeld, Verbindung unveraendert.
#   1.08 2026-11-23 Nach Import und Rueckgaengig Tabellenansicht ueber Originalpfad sofort aktualisieren.
#   1.07 2026-11-23 Kanalauswahl wie bei neuer Zeile, Standard 0, Quellkanaele optional erhalten.
#   1.06 2026-11-23 Feature-Branch auf Basis 4.79; Sprachen und Startvorgaben dokumentiert.
#   1.05 2026-11-23 Quellfreigabe nach jedem Start ausgeschaltet; Aktivierung nur im Dialog.
#   1.04 2026-11-23 Dialogmodus Zeilen einfuegen mit Bereich, Zielposition und bestaetigten Konflikthinweisen.
#   1.03 2026-11-23 Dialogtitel Datenuebertragung mit gemeinsamem Uebersetzungsschluessel.
#   1.02 2026-11-23 Kompakter Dialog im Programm statt separater Seite, Uebernahme zuerst, Einrichtung im zweiten Reiter.
#   1.01 2026-11-23 Nach Import und Backup-Ruecknahme originale Tabellenberechnung ausfuehren und Ergebnis speichern.
#   1.00 2026-11-22 Separate Testseite fuer Quellfreigabe, LAN-Suche, Vorschau, Import und Rueckgaengig.
from __future__ import annotations  # v1.06

import asyncio  # v1.06
import json  # v1.06
import os  # v1.06
from pathlib import Path  # v1.06
import socket  # v1.06
import tempfile  # v1.06
from urllib.parse import urlsplit  # v1.09

from nicegui import ui, run  # v1.06
from _web.web_i18n import tr  # v1.06
from headless import headless_table_sync as sync  # v1.06


def split_source_address(value):  # v1.09
    parsed = urlsplit(value if "://" in value else "http://" + value)  # v1.09
    return parsed.hostname or "", str(parsed.port or sync.TCP_PORT), parsed.scheme or "http"  # v1.09


def source_address(host, port, scheme="http"):  # v1.09
    try:  # v1.09
        number = int(str(port or sync.TCP_PORT))  # v1.09
        if not 1 <= number <= 65535:  # v1.09
            raise ValueError()  # v1.09
    except (ValueError, TypeError):  # v1.09
        raise ValueError(tr("Bitte einen Port zwischen 1 und 65535 eingeben.")) from None  # v1.09
    host = host.strip().strip("[]")  # v1.09
    return f"{scheme}://{'[' + host + ']' if ':' in host else host}:{number}"  # v1.09


def recalculate_workbook(wb, *, logic=None, columns=None):  # v1.01
    """Originale Neuberechnung einschliesslich Symbole und Testtasten."""  # v1.01
    if logic is None:  # v1.01
        import proggen.M20_PageEvents_a_Functions as logic  # v1.01
    if columns is None:  # v1.01
        import proggen.M25_Columns as columns  # v1.01
    active = getattr(wb, "ActiveSheet", None)  # v1.01
    try:  # v1.01
        logic.Update_All_Start_LedNr()  # v1.01: auch abhaengige Tabellen neu berechnen
        for sheet in list(wb.sheets):  # v1.01
            if getattr(sheet, "Datasheet", False) and sheet.Name not in sync.EXCLUDED:  # v1.01
                sheet.Select()  # v1.01
                columns.Make_sure_that_Col_Variables_match()  # v1.01
                sheet.refreshicons()  # v1.01: originale Berechnung und Symbole
                logic.ResetTestButtons(False)  # v1.01
    finally:  # v1.01
        if active is not None and active in wb.sheets:  # v1.01
            active.Select()  # v1.01
            columns.Make_sure_that_Col_Variables_match()  # v1.01


_open_dialog = None  # v1.02


def open_dialog(on_changed=None):  # v1.08
    if _open_dialog is None:  # v1.02
        raise RuntimeError("Tabellenabgleich noch nicht initialisiert")  # v1.02
    _open_dialog(on_changed=on_changed)  # v1.08


def install(app, ctrl, workbook, version):  # v1.06
    folder = Path(ctrl.data_dir)  # v1.06
    settings = sync.read_settings(folder)  # v1.06
    settings["enabled"] = False  # v1.05: Freigabe bewusst je Sitzung aktivieren
    state = {"share": None, "busy": False}  # v1.06
    sync.save_settings(folder, settings)  # v1.06

    def local_columns():  # v1.06
        import proggen.M25_Columns as columns  # v1.06
        return [columns.COMPort_COL - 1, columns.COMPort_COL]  # v1.06

    def capture():  # v1.06
        wb = workbook()  # v1.06
        path = folder / "tabellenabgleich_snapshot.json"  # v1.06
        path.unlink(missing_ok=True)  # v1.06
        wb.SaveWorkbook(str(path))  # v1.06
        if not path.is_file():  # v1.06
            raise ValueError(tr("Tabellen konnten nicht gespeichert werden."))  # v1.06
        return json.loads(path.read_text(encoding="utf-8"))  # v1.06

    def package():  # v1.06
        return sync.make_package(capture(), settings["selected"], name=settings["name"], local_columns=local_columns())  # v1.06

    def refresh():  # v1.06
        if state["share"] is not None and not state["busy"]:  # v1.06
            try:  # v1.06
                data = package()  # v1.06
                with state["share"].lock:  # v1.06
                    state["share"].package = data  # v1.06
            except Exception:  # v1.06
                import logging  # v1.06
                logging.getLogger(__name__).exception("Tabellenfreigabe aktualisieren")  # v1.06

    async def refresh_loop():  # v1.06
        while True:  # v1.06
            await asyncio.sleep(3)  # v1.06
            refresh()  # v1.06

    async def start_refresh():  # v1.06
        # v1.05 (entfallen) if settings.get("enabled"):
        # v1.05 (entfallen) try:
        # v1.05 (entfallen) state["share"] = await run.io_bound(sync.Share, settings["name"], settings["code"], package())
        # v1.05 (entfallen) except Exception:
        # v1.05 (entfallen) import logging
        # v1.05 (entfallen) logging.getLogger(__name__).exception("Tabellenfreigabe beim Start")
        asyncio.create_task(refresh_loop())  # v1.06

    app.on_startup(start_refresh)  # v1.06
    app.on_shutdown(lambda: state["share"].close() if state["share"] else None)  # v1.06

    def target_file():  # v1.06
        wb = workbook()  # v1.06
        return Path(wb.workbookfilename or folder / (Path(str(ctrl.tempworkbookFilname)).name + "_" + wb.Name + ".json"))  # v1.06

    def load_target():  # v1.06
        wb = workbook()  # v1.06
        saved = json.loads(target_file().read_bytes())  # v1.06
        for sheet in list(wb.sheets):  # v1.06
            if getattr(sheet, "Datasheet", False) and sheet.Name not in saved["Workbookdata"] and sheet.Name not in sync.EXCLUDED:  # v1.06
                wb.delete_sheet(sheet.Name)  # v1.06
        wb.LoadWorkbook(str(target_file()), workbookname=wb.Name, keep_filename=True)  # v1.06
        recalculate_workbook(wb)  # v1.01
        sync.atomic_write(target_file(), sync.encode(capture()))  # v1.01: berechneten Stand sichern
        # Auch die Zwischensicherung muss denselben Stand tragen.
        auto = target_file().with_suffix(".autosave.json")  # v1.06
        sync.atomic_write(auto, target_file().read_bytes())  # v1.06

    def apply(raw, *, row_options=None, allow_conflicts=False):  # v1.04
        if state["busy"]:  # v1.06
            raise ValueError(tr("Ein Abgleich läuft bereits."))  # v1.06
        state["busy"] = True  # v1.06
        try:  # v1.06
            before = sync.encode(capture())  # v1.06
            sync.atomic_write(target_file(), before)  # v1.06
            if row_options is None:  # v1.04
                sync.import_tables(folder, target_file(), raw, local_columns=local_columns())  # v1.06
            else:  # v1.04
                sync.import_rows(folder, target_file(), raw, allow_conflicts=allow_conflicts, **row_options)  # v1.04
            load_target()  # v1.06
        finally:  # v1.06
            state["busy"] = False  # v1.06

    def build_dialog(on_changed=None):  # v1.08
        ui.add_css("""
            /* v1.02: Dialog bleibt innerhalb des Browserfensters, Inhalt scrollt. */
            .mll-sync-dialog { width: 760px; max-width: 94vw !important; max-height: 90vh;
                padding: 0; border-radius: 12px; gap: 0; overflow: hidden; }
            .mll-sync-heading { padding: 18px 22px 12px; }
            .mll-sync-tabs { border-bottom: 1px solid rgba(130,145,165,.24); }
            .mll-sync-intro { padding: 14px 24px 0; opacity: .75; }
            .mll-sync-status { padding: 6px 24px 0; min-height: 24px; }
            .mll-sync-panels { overflow-y: auto; flex: 1; min-height: 0; background: transparent; }
            .mll-sync-pane { padding: 16px 24px; display: flex; flex-direction: column; gap: 14px; }
            .mll-sync-footer { padding: 8px 16px; border-top: 1px solid rgba(130,145,165,.24); }
            .mll-sync-pane .q-field { margin: 0; }
            @media(max-width: 600px) { .mll-sync-heading { padding: 12px 14px; }
                .mll-sync-pane { padding: 14px; } .mll-sync-heading .text-h6 { font-size: 17px; } }
        """)  # v1.06

        with ui.dialog().props("persistent") as dialog, ui.card().classes("mll-sync-dialog"):  # v1.06
            with ui.row().classes("w-full items-center justify-between no-wrap mll-sync-heading"):  # v1.06
                with ui.row().classes("items-center gap-3 no-wrap"):  # v1.06
                    ui.icon("sync", size="26px").classes("text-primary")  # v1.06
                    # ui.label(tr("Tabellenabgleich – Testkopie")).classes("text-h6")  # v1.03 (entfallen)
                    ui.label(tr("Datenübertragung")).classes("text-h6")  # v1.03
                ui.button(icon="close", on_click=dialog.close).props("flat round dense").tooltip(tr("Schließen"))  # v1.06
            with ui.tabs().classes("w-full mll-sync-tabs") as tabs:  # v1.06
                receive_tab = ui.tab(tr("Tabellen übernehmen"), icon="download")  # v1.06
                share_tab = ui.tab(tr("Dieser PC als Quelle"), icon="computer")  # v1.06
            ui.label(tr("Quelle und Ziel arbeiten unabhängig. Nur ausgewählte Tabellen werden übernommen.")).classes("text-caption mll-sync-intro")  # v1.06
            status = ui.label("").classes("text-sm text-primary mll-sync-status")  # v1.06
            with ui.tab_panels(tabs, value=receive_tab).classes("w-full mll-sync-panels"):  # v1.06
                with ui.tab_panel(share_tab).classes("mll-sync-pane"):  # v1.06
                    source_name = ui.input(tr("Name des Quell-PCs"), value=settings["name"]).props("outlined dense").classes("w-full")  # v1.06
                    code = ui.input(tr("Verbindungscode"), value=settings["code"], password=True, password_toggle_button=True).props("outlined dense").classes("w-full")  # v1.06
                    choices = [s.Name for s in workbook().sheets if getattr(s, "Datasheet", False) and s.Name not in sync.EXCLUDED]  # v1.06
                    selected = ui.select(choices, value=[n for n in settings["selected"] if n in choices], multiple=True, label=tr("Freigegebene Tabellen")).props("use-chips").props("outlined dense").classes("w-full")  # v1.06
                    source_status = ui.label(tr("Freigabe ausgeschaltet") if not state["share"] else tr("Freigabe aktiv"))  # v1.06

                    async def enable():  # v1.06
                        try:  # v1.06
                            if not selected.value:  # v1.06
                                raise ValueError(tr("Bitte Tabellen auswählen."))  # v1.06
                            # if len(code.value or "") < 12:  # v1.10 (entfallen)
                            #     raise ValueError(tr("Der Verbindungscode muss mindestens 12 Zeichen haben."))  # v1.10 (entfallen)
                            if len(code.value or "") < 6:  # v1.10
                                raise ValueError(tr("Der Verbindungscode muss mindestens 6 Zeichen haben."))  # v1.10
                            settings.update(name=source_name.value.strip() or socket.gethostname(), code=code.value, selected=list(selected.value))  # v1.06
                            data = package()  # v1.06
                            if state["share"]:  # v1.06
                                await run.io_bound(state["share"].close)  # v1.06
                                state["share"] = None  # v1.06
                            state["share"] = await run.io_bound(sync.Share, settings["name"], settings["code"], data)  # v1.06
                            settings["enabled"] = True  # v1.06
                            sync.save_settings(folder, settings)  # v1.06
                            source_status.set_text(tr("Freigabe aktiv"))  # v1.06
                            status.set_text(tr("Die ausgewählten Tabellen werden laufend bereitgestellt."))  # v1.06
                        except Exception as error:  # v1.06
                            ui.notify(tr(str(error)), type="negative")  # v1.06

                    async def disable():  # v1.06
                        if state["share"]:  # v1.06
                            await run.io_bound(state["share"].close)  # v1.06
                            state["share"] = None  # v1.06
                        settings["enabled"] = False  # v1.06
                        sync.save_settings(folder, settings)  # v1.06
                        source_status.set_text(tr("Freigabe ausgeschaltet"))  # v1.06

                    def firewall():  # v1.06
                        if os.name != "nt":  # v1.06
                            ui.notify(tr("Auf Linux die Firewall für TCP 45875 und UDP 45874 prüfen."), type="info")  # v1.06
                            return  # v1.06
                        import ctypes  # v1.06
                        script = folder / "tabellenabgleich_firewall.ps1"  # v1.06
                        script.write_text(
                            "$ErrorActionPreference='Stop'\n"
                            "Get-NetFirewallRule -DisplayName 'WebMLL Tabellenabgleich Test TCP','WebMLL Tabellenabgleich Test UDP' -ErrorAction SilentlyContinue | Remove-NetFirewallRule\n"
                            "New-NetFirewallRule -DisplayName 'WebMLL Tabellenabgleich Test TCP' -Direction Inbound -Action Allow -Profile Private -RemoteAddress LocalSubnet -Protocol TCP -LocalPort 45875\n"
                            "New-NetFirewallRule -DisplayName 'WebMLL Tabellenabgleich Test UDP' -Direction Inbound -Action Allow -Profile Private -RemoteAddress LocalSubnet -Protocol UDP -LocalPort 45874\n", encoding="utf-8")  # v1.06
                        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", '-NoProfile -ExecutionPolicy Bypass -File "' + str(script) + '"', None, 0)  # v1.06
                        if result <= 32:  # v1.06
                            raise OSError(tr("Firewall-Einrichtung wurde nicht gestartet."))  # v1.06
                        ui.notify(tr("Bitte die Windows-Administratorabfrage bestätigen."))  # v1.06

                    with ui.row():  # v1.06
                        ui.button(tr("Tabellenfreigabe aktivieren"), on_click=enable)  # v1.06
                        ui.button(tr("Freigabe ausschalten"), on_click=disable).props("flat")  # v1.06
                    with ui.expansion(tr("Firewall einrichten"), icon="settings_ethernet").classes("w-full text-sm"):  # v1.06
                        ui.button(tr("Firewall einrichten"), on_click=firewall).props("flat dense")  # v1.06
                        ui.label(tr("Im Heimnetz: TCP 45875 und UDP 45874 nur im privaten Netzwerk freigeben.")).classes("text-caption")  # v1.06
                with ui.tab_panel(receive_tab).classes("mll-sync-pane"):  # v1.06
                    # address = ui.input(tr("Quelladresse"), value=settings.get("source", ""), placeholder="http://192.168.10.20:45875").props("outlined dense").classes("w-full")  # v1.09 (entfallen)
                    source_host, source_port, source_scheme = split_source_address(settings.get("source", ""))  # v1.09
                    with ui.row().classes("w-full flex-nowrap items-start gap-2"):  # v1.09
                        address = ui.input(tr("Quelladresse"), value=source_host, placeholder="192.168.10.20").props("outlined dense").classes("grow min-w-0")  # v1.09
                        port = ui.input(tr("Port"), value=source_port).props('outlined dense type=number min=1 max=65535').classes("w-28 shrink-0")  # v1.09
                    source_code = ui.input(tr("Verbindungscode"), value=settings.get("source_code", ""), password=True, password_toggle_button=True).props("outlined dense").classes("w-full")  # v1.06
                    results = ui.column().classes("w-full")  # v1.06

                    async def search():  # v1.06
                        status.set_text(tr("Quell-PCs werden gesucht …"))  # v1.06
                        try:  # v1.06
                            found = await run.io_bound(sync.discover)  # v1.06
                            results.clear()  # v1.06
                            with results:  # v1.06
                                for item in found:  # v1.06
                                    def choose(item=item):  # v1.06
                                        nonlocal source_scheme  # v1.09
                                        selected_host, selected_port, source_scheme = split_source_address(item["address"])  # v1.09
                                        # address.value = item["address"]  # v1.09 (entfallen)
                                        address.value = selected_host  # v1.09
                                        port.value = selected_port  # v1.09
                                    # ui.button(item["name"] + " · " + item["address"], on_click=choose).props("outline")  # v1.09 (entfallen)
                                    ui.button(item["name"] + " · " + item["address"].split("://", 1)[-1], on_click=choose).props("outline")  # v1.09
                            status.set_text(tr("Gefundene Quellen: {count}", count=len(found)))  # v1.06
                        except Exception as error:  # v1.06
                            ui.notify(tr(str(error)), type="negative")  # v1.06

                    async def preview():  # v1.06
                        status.set_text(tr("Verbindung wird geprüft …"))  # v1.06
                        try:  # v1.06
                            # raw = await run.io_bound(sync.fetch, address.value, source_code.value)  # v1.09 (entfallen)
                            endpoint = source_address(address.value, port.value, source_scheme)  # v1.09
                            raw = await run.io_bound(sync.fetch, endpoint, source_code.value)  # v1.09
                            incoming = sync.validate(raw)  # v1.06
                            current = capture()  # v1.06
                            sync.merge(current, raw, local_columns=local_columns())  # v1.06
                            # settings.update(source=address.value.strip(), source_code=source_code.value)  # v1.09 (entfallen)
                            settings.update(source=endpoint, source_code=source_code.value)  # v1.09
                            sync.save_settings(folder, settings)  # v1.06
                            names = list(incoming["sheets"])  # v1.06
                            with ui.dialog().props("persistent") as dialog, ui.card().classes("w-[760px] max-w-[94vw]").style("max-height:90vh;overflow-y:auto"):  # v1.06
                                ui.label(tr("Übernahme bestätigen")).classes("text-h6")  # v1.06
                                mode = ui.select({"replace":tr("Tabellen ersetzen"), "insert":tr("Zeilen in bestehende Tabelle einfügen")}, value="replace", label=tr("Übernahmeart")).props("outlined dense").classes("w-full")  # v1.06
                                with ui.column().classes("w-full").bind_visibility_from(mode, "value", backward=lambda value:value=="replace"):  # v1.06
                                    ui.label(", ".join(names))  # v1.06
                                    ui.label(tr("Diese Tabellen werden ersetzt. Der bisherige Stand wird als letztes Backup gesichert. Bitte andere Bearbeitungsfenster schließen."))  # v1.06
                                with ui.column().classes("w-full gap-3").bind_visibility_from(mode, "value", backward=lambda value:value=="insert"):  # v1.06
                                    source_sheet = ui.select(names, value=names[0], label=tr("Quelltabelle")).props("outlined dense").classes("w-full")  # v1.06
                                    end = len(incoming["sheets"][names[0]]["data"]["TKSHEET_data"])  # v1.06
                                    source_rows = ui.input(tr("Quellzeilen"), value=f"3-{end}", placeholder="3-8, 12").props("outlined dense").classes("w-full")  # v1.06
                                    ui.label(tr("Zeilennummern wie in der Tabelle, zum Beispiel 3-8, 12. Kopfzeilen werden nicht eingefügt.")).classes("text-caption")  # v1.06
                                    targets = [sheet.Name for sheet in workbook().sheets if getattr(sheet,"Datasheet",False) and sheet.Name not in sync.EXCLUDED]  # v1.06
                                    active = getattr(workbook(), "ActiveSheet", None)  # v1.06
                                    default = active.Name if active and active.Name in targets else (targets[0] if targets else None)  # v1.06
                                    target_sheet = ui.select(targets, value=default, label=tr("Zieltabelle")).props("outlined dense").classes("w-full")  # v1.06
                                    import proggen.M02_Public as public  # v1.07
                                    channel_options = {"keep": tr("LED-Kanäle der Quelle beibehalten")}  # v1.07
                                    for channel_index in range(public.LED_CHANNELS):  # v1.07
                                        channel_options[channel_index] = str(channel_index)  # v1.07
                                    channel_options[0] = "0 – " + tr("Standard LEDs")  # v1.07
                                    channel_options[1] = "1 – " + tr("Taster LEDs")  # v1.07
                                    led_channel = ui.select(channel_options, value=0, label=tr("LED-Kanal für eingefügte Zeilen")).props("outlined dense").classes("w-full")  # v1.07
                                    ui.label(tr("Der gewählte Kanal gilt für alle eingefügten Zeilen. Vorhandene Zeilen bleiben unverändert.")).classes("text-caption")  # v1.07
                                    with ui.row().classes("w-full items-start"):  # v1.06
                                        position = ui.select({"end":tr("Am Ende"), "before":tr("Vor Zeile"), "after":tr("Nach Zeile")}, value="end", label=tr("Einfügeposition")).props("outlined dense").classes("grow")  # v1.06
                                        target_row = ui.number(tr("Zielzeile"), value=3, min=3, step=1, format="%d").props("outlined dense").classes("w-32").bind_visibility_from(position,"value",backward=lambda value:value!="end")  # v1.06
                                    ui.label(tr("Vorhandene Zeilen bleiben erhalten. Vor dem Einfügen wird das letzte Backup erneuert.")).classes("text-caption")  # v1.06
                                    report = ui.column().classes("w-full gap-1")  # v1.06
                                    accepted = ui.checkbox(tr("Ich habe die Konflikthinweise geprüft und möchte trotzdem einfügen."), value=False)  # v1.06
                                    accepted.set_visibility(False)  # v1.06
                                    report_state = {"warnings":None}  # v1.06

                                    def reset_acceptance(_event=None):  # v1.06
                                        accepted.value = False  # v1.06

                                    def selection():  # v1.06
                                        # return dict(source_name=source_sheet.value, rows=source_rows.value, target_name=target_sheet.value, where=position.value, target_row=target_row.value)  # v1.06 (entfallen v1.07)
                                        import proggen.M25_Columns as columns  # v1.07
                                        target = next(sheet for sheet in workbook().sheets if sheet.Name == target_sheet.value)  # v1.07
                                        try:  # v1.07
                                            columns.Make_sure_that_Col_Variables_match(target)  # v1.07
                                            channel_column = columns.LED_Cha_Col - 1  # v1.07
                                        finally:  # v1.07
                                            columns.Make_sure_that_Col_Variables_match(workbook().ActiveSheet)  # v1.07
                                        return dict(source_name=source_sheet.value, rows=source_rows.value, target_name=target_sheet.value, where=position.value, target_row=target_row.value, led_channel=None if led_channel.value == "keep" else led_channel.value, channel_column=channel_column, channel_limit=public.LED_CHANNELS)  # v1.07

                                    def check_insert():  # v1.06
                                        options = selection()  # v1.06
                                        _result, warnings, summary = sync.plan_row_insert(capture(), raw, **options)  # v1.06
                                        if warnings != report_state["warnings"]:  # v1.06
                                            accepted.value = False  # v1.06
                                        report_state["warnings"] = warnings  # v1.06
                                        report.clear()  # v1.06
                                        labels = {"address":tr("Adressüberschneidung"),"name":tr("Name bereits vorhanden"),"reference":tr("Tabellenverweis fehlt")}  # v1.06
                                        with report:  # v1.06
                                            ui.label(tr("{count} Zeilen werden ab Zielzeile {row} in {table} eingefügt.",count=summary["count"],row=summary["at"],table=summary["target"]))  # v1.06
                                            for warning in warnings:  # v1.06
                                                ui.label(tr("Quellzeile {row}: {kind} – {value}",row=warning["row"],kind=labels[warning["kind"]],value=warning["value"])).classes("text-warning text-sm")  # v1.06
                                        accepted.set_visibility(bool(warnings))  # v1.06
                                        return options,warnings  # v1.06

                                    def preview_insert():  # v1.06
                                        try:  # v1.06
                                            check_insert()  # v1.06
                                        except Exception as error:  # v1.06
                                            ui.notify(tr(str(error)),type="negative")  # v1.06

                                    def source_changed(_event):  # v1.06
                                        total=len(incoming["sheets"][source_sheet.value]["data"]["TKSHEET_data"])  # v1.06
                                        source_rows.value=f"3-{total}"  # v1.06
                                        reset_acceptance()  # v1.06

                                    source_sheet.on_value_change(source_changed)  # v1.06
                                    for field in [source_rows,target_sheet,position,target_row,led_channel]:  # v1.06
                                        field.on_value_change(reset_acceptance)  # v1.06
                                    ui.button(tr("Einfügen prüfen"),icon="fact_check",on_click=preview_insert).props("outline")  # v1.06

                                async def commit():  # v1.06
                                    try:  # v1.06
                                        if mode.value=="insert":  # v1.06
                                            options,warnings=check_insert()  # v1.06
                                            if warnings and not accepted.value:  # v1.06
                                                ui.notify(tr("Bitte die Konflikthinweise vor dem Einfügen bestätigen."),type="warning")  # v1.06
                                                return  # v1.06
                                            apply(raw,row_options=options,allow_conflicts=bool(accepted.value))  # v1.06
                                            ui.notify(tr("Zeilen eingefügt und neu berechnet."),type="positive")  # v1.06
                                        else:  # v1.06
                                            apply(raw)  # v1.06
                                            ui.notify(tr("Tabellen übernommen. Das letzte Backup wurde erneuert."), type="positive")  # v1.06
                                        dialog.close()  # v1.06
                                        # status.set_text(tr("Bitte die Programmseite neu laden."))  # v1.08 (entfallen)
                                        if on_changed is not None:  # v1.08
                                            on_changed()  # v1.08
                                        status.set_text(tr("Zeilen eingefügt und neu berechnet.") if mode.value == "insert" else tr("Tabellen übernommen. Das letzte Backup wurde erneuert."))  # v1.08
                                    except Exception as error:  # v1.06
                                        ui.notify(tr(str(error)), type="negative")  # v1.06

                                with ui.row().classes("justify-end w-full"):  # v1.06
                                    ui.button(tr("Übernehmen und sichern"), on_click=commit)  # v1.06
                                    ui.button(tr("Abbrechen"), on_click=dialog.close).props("flat")  # v1.06
                            dialog.open()  # v1.06
                            status.set_text(tr("Quelle erreichbar"))  # v1.06
                        except Exception as error:  # v1.06
                            status.set_text(tr("Verbindung fehlgeschlagen"))  # v1.06
                            ui.notify(tr(str(error)), type="negative")  # v1.06

                    async def undo():  # v1.06
                        if not (folder / sync.BACKUP).is_file():  # v1.06
                            ui.notify(tr("Noch kein Importbackup vorhanden."), type="warning")  # v1.06
                            return  # v1.06
                        with ui.dialog() as dialog, ui.card():  # v1.06
                            ui.label(tr("Letzten Import rückgängig machen?"))  # v1.06
                            def confirm():  # v1.06
                                try:  # v1.06
                                    sync.restore(folder, target_file())  # v1.06
                                    load_target()  # v1.06
                                    dialog.close()  # v1.06
                                    if on_changed is not None:  # v1.08
                                        on_changed()  # v1.08
                                    status.set_text(tr("Backup wiederhergestellt."))  # v1.08
                                except Exception as error:  # v1.06
                                    ui.notify(tr(str(error)), type="negative")  # v1.06
                            ui.button(tr("Backup wiederherstellen"), on_click=confirm)  # v1.06
                            ui.button(tr("Abbrechen"), on_click=dialog.close).props("flat")  # v1.06
                        dialog.open()  # v1.06

                    with ui.row():  # v1.06
                        ui.button(tr("Quell-PC suchen"), icon="search", on_click=search).props("outline")  # v1.06
                        ui.button(tr("Verbindung prüfen und übernehmen"), icon="download", on_click=preview).props("unelevated")  # v1.06
                    ui.separator().classes("my-2")  # v1.06
                    with ui.row().classes("w-full items-center justify-between"):  # v1.06
                        ui.icon("history", size="20px").classes("text-grey-6")  # v1.06
                        ui.button(tr("Letzten Import rückgängig machen"), on_click=undo).props("flat dense")  # v1.06
                    with ui.expansion(tr("Quelladresse"), icon="help_outline").classes("w-full text-sm"):  # v1.06
                        ui.label(tr("Debian-VM: Für die Suche Netzwerkbrücke verwenden. Bei NAT die Quelladresse direkt eingeben.")).classes("text-caption")  # v1.06
            with ui.row().classes("w-full justify-end mll-sync-footer"):  # v1.06
                ui.button(tr("Schließen"), on_click=dialog.close).props("flat")  # v1.06
        dialog.open()  # v1.02

    global _open_dialog  # v1.02
    _open_dialog = build_dialog  # v1.02
