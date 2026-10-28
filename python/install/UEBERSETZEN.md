Datei-Version: 1.04 (2026-10-27) - UEBERSETZEN.md
Gilt für webMobaLedLib 2.22

# Übersetzen der Web-Oberfläche

Die Texte der Oberfläche (Menüs, Knöpfe, Meldungen, Hinweise) stehen in der Datei **`python/csv/Web_Languages.csv`**. Die Meldungen des Programm Generators und des Patterngenerators
(zum Beispiel die Fragen beim Erzeugen eines Programms) kommen weiter aus dem Tabellenblatt **Languages** der Excel-Datei; die Parameter-Texte der Makros aus **Par_Description**.

## Wo die Texte stehen

1. **Katalog `csv/Web_Languages.csv`** (diese Datei): alle Texte der Web-Oberfläche und alle Texte, die es im Excel-Programm nicht gab. Er geht vor.
2. **Tabelle Languages der Excel-Datei** (`csv/Prog_Generator_MobaLedLib.xlsm`): die Texte der Formulare und Meldungen aus dem Excel-Programm, mit Übersetzungen in sieben Sprachen. Ein Text, der **nicht** im Katalog steht, wird dort gesucht; Einträge mit „ToDo“ gelten als nicht übersetzt.
3. **Reihenfolge** (seit 2.22): gewählte Sprache im Katalog, gewählte Sprache in der Tabelle Languages, dann English im Katalog, English in der Tabelle, zuletzt der deutsche Text. Ein englischer Text des Katalogs verdrängt also keine vorhandene Übersetzung der Tabelle mehr (vorher mischten sich Niederländisch und Englisch).
4. **Stand der Sprachen:** **English** (Entwurf) und **Nederlands, Français, Italiano, Español, Dansk** (Entwürfe, von Claude geschrieben, **nicht von Muttersprachlern geprüft**): Für je 744 von 766 Texten des Katalogs gibt es eine Übersetzung; die übrigen stehen in der Tabelle Languages. Fachwörter und Anrede (Niederländisch „je“, Französisch „vous“, Italienisch und Spanisch „tu“/„tú“, Dänisch „du“) sind Vorschläge. Zum Prüfen gibt es `Web_Languages_Nederlands_Entwurf.csv` (Deutsch;English;Nederlands) und `Web_Languages_Entwurf_FR_IT_ES_DA.csv` (Deutsch;English;Francais;Italiano;Espanol;Dansk, jeweils mit „(Entwurf)“ im Spaltenkopf): die eigene Spalte verbessern und die Datei zurückschicken; sie wird in `csv/Web_Languages.csv` eingearbeitet. Eigene Verbesserungen kann man auch direkt in `csv/Web_Languages.csv` eintragen.

Für eine neue Übersetzung genügt es, den Eintrag im Katalog zu ergänzen, auch für Texte, die in der Tabelle Languages noch „ToDo“ sind.

## Aufbau der Datei

| Spalte | Sprache | Sprachnummer im Programm |
|---|---|---|
| 1 Deutsch | der deutsche Text, **gleichzeitig der Schlüssel** (nicht ändern) | 0 |
| 2 English | Entwurf liegt vor | 1 |
| 3 Nederlands | | 2 |
| 4 Francais | | 3 |
| 5 Italiano | | 4 |
| 6 Espanol | | 5 |
| 7 Dansk | | 6 |

- Die Datei ist UTF-8 (mit Kennzeichen) mit **Semikolon** als Trennzeichen und lässt sich in Excel oder LibreOffice öffnen. Beim Speichern **UTF-8 und Semikolon** beibehalten (LibreOffice: „CSV (Text)“, Zeichensatz Unicode UTF-8, Feldtrenner `;`).
- In die Spalte der eigenen Sprache die Übersetzung eintragen. **Fehlt sie, erscheint der englische Text**, fehlt auch der, der deutsche.
- Mehrere Sprachen können von verschiedenen Personen bearbeitet werden; bitte nur die eigene Spalte ändern und die Datei zurückschicken (oder als Pull Request auf GitHub).

## Regeln

- **Platzhalter** wie `{name}` oder `{port}` unverändert übernehmen (sie werden vom Programm ersetzt).
- **Tastenkürzel in Klammern** wie `(A)` oder `(J)` in Dialogknöpfen **nicht ändern**: Das Programm reagiert auf diesen Buchstaben, auch wenn der Text in einer anderen Sprache steht.
- **Zeilenumbrüche** im Text (Alt+Enter) beibehalten.
- Namen von Knöpfen und Menüs, die in den Meldungen vorkommen („Hilfe → Update“), so übersetzen, wie sie in der Oberfläche stehen.
- Einheiten, Dateinamen und Beispiele (`/home/name/…`, `COM3`, `TCP`) nicht übersetzen.
- Die Texte der Tabellen (Spaltenköpfe, Beschreibungen in den Beispielblättern) und der Anleitung gehören noch nicht dazu.

## Prüfen

- In den **Programm Einstellungen** die Sprache wählen und speichern: Die Seite lädt neu, alle Texte erscheinen in der Sprache (fehlende auf Englisch).
- Abdeckung je Sprache: `python _web/web_i18n.py check` im Ordner `python` (zeigt, wie viele Texte übersetzt sind und ob Texte im Programm im Katalog fehlen).
- **Testsprache:** Mit der Umgebungsvariablen `MLL_TEST_LANGUAGE=1` wird jeder Text, der durch die Übersetzung läuft, in Klammern gesetzt (`⟦Text⟧`). Texte ohne Klammern werden noch nicht übersetzt (zum Beispiel Meldungen mit eingesetzten Werten); bitte melden.
- Neue Texte, die im Programm dazugekommen sind, nimmt `python _web/web_i18n.py extract` in die Datei auf (bestehende Übersetzungen bleiben).
