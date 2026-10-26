Datei-Version: 1.00 (2026-10-23) - UEBERSETZEN.md
Gilt für webMobaLedLib 2.14

# Übersetzen der Web-Oberfläche

Die Texte der Oberfläche (Menüs, Knöpfe, Meldungen, Hinweise) stehen in der Datei **`python/csv/Web_Languages.csv`**. Die Meldungen des Programm Generators und des Patterngenerators
(zum Beispiel die Fragen beim Erzeugen eines Programms) kommen weiter aus dem Tabellenblatt **Languages** der Excel-Datei; die Parameter-Texte der Makros aus **Par_Description**.

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
