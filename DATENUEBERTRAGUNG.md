# Datenübertragung zwischen PCs

Datei-Version: 1.00 (2026-11-23), gilt für webMobaLedLib 4.79, Branch `feature/datenuebertragung`.

Öffne **Einstellungen → Datenübertragung**. Beide PCs arbeiten unabhängig mit ihren eigenen Daten. Die Funktion überträgt ausgewählte Programmgenerator-Tabellen oder ausgewählte Zeilen über das lokale Netzwerk. Sie benötigt weder ein Konto noch einen VPN-Tunnel.

## Quell-PC freigeben

1. Öffne auf dem Quell-PC den Reiter **Dieser PC als Quelle**.
2. Vergib einen frei wählbaren Namen und wähle die Tabellen aus.
3. Übernimm den erzeugten Verbindungscode oder verwende einen eigenen mit mindestens zwölf Zeichen.
4. Klicke auf **Tabellenfreigabe aktivieren**. Der Quell-PC muss laufen und erreichbar bleiben.

**Die Freigabe ist nach jedem Programmstart ausgeschaltet.** Name, Code und Auswahl bleiben gespeichert. **Freigabe ausschalten** beendet sie sofort. Die Freigabe stellt den aktuellen Stand regelmäßig bereit, sie schreibt nichts auf anderen PCs.

## Am Ziel übernehmen

1. Öffne **Tabellen übernehmen**, dann **Quell-PC suchen**. Wähle die Quelle aus. Alternativ gib deren Adresse ein, etwa `http://192.168.1.20:45875`.
2. Trage den Verbindungscode des Quell-PCs ein und klicke **Verbindung prüfen und übernehmen**.
3. Wähle die Übernahmeart. **Tabellen ersetzen** ersetzt die aufgelisteten gleichnamigen Tabellen; fehlende Tabellen werden angelegt.
4. **Zeilen in bestehende Tabelle einfügen** erlaubt eine Quelltabelle und Zeilen wie `3-8, 12`, eine Zieltabelle sowie **Am Ende**, **Vor Zeile** oder **Nach Zeile**. Zeile 1 und 2 bleiben ausgeschlossen. Protokoll und Spaltenstruktur müssen passen.
5. Mit **Einfügen prüfen** siehst du die Zielposition und Hinweise zu direkten numerischen Adressüberschneidungen, bereits definierten Namen und fehlenden include-Tabellen. Prüfe die Hinweise; bei Konflikten ist eine ausdrückliche Bestätigung nötig. Eigene Makros und symbolische Adressen werden nicht vollständig semantisch geprüft. Adressen werden nicht automatisch geändert.
6. Klicke **Übernehmen und sichern** und lade die Programmseite anschließend neu.

Vorhandene Zeilen bleiben beim Einfügen erhalten. Zeilenfarben, Höhen und Sichtbarkeit werden übertragen, vorhandene Bildanker verschoben. Handgezeichnete Formen der Quellzeilen und externe Bilddateien werden nicht mitkopiert. Tabellen, Icons und Testtasten werden über die ursprünglichen Programmfunktionen neu berechnet.

## Welche Daten bleiben am Ziel?

Globale Programmeinstellungen, WLAN-Zugangsdaten und ESP-Einstellungen werden nicht übernommen. COM-Port und WLAN-Zieladresse bleiben lokal. Beim Ersetzen einer ganzen Tabelle werden deren übrige Tabelleninhalte und Kopfwerte einschließlich Boardkonfiguration übernommen. Beim Einfügen von Zeilen bleiben die Kopfwerte der Zieltabelle bestehen. Andere Tabellen bleiben erhalten; die Neuberechnung kann davon abhängige Tabellenwerte aktualisieren.

## Sicherung und Rückgängig

Vor jeder bestätigten Übernahme wird die komplette bisherige Arbeitsmappe in `tabellenabgleich_letztes_backup.json` im Datenordner gesichert. Jede weitere Übernahme ersetzt diese eine Sicherung. **Letzten Import rückgängig machen** stellt diesen Stand wieder her und berechnet neu. Die Funktion ersetzt keine langfristige Datensicherung. Schließe andere Bearbeitungsfenster während der Übernahme.

## Netzwerk und Sprachen

Die Quellfreigabe nutzt TCP **45875**, die Suche UDP **45874**. Die Windows-Schaltfläche richtet nach Administratorbestätigung Regeln nur für private lokale Netze ein. Unter Linux müssen die Ports entsprechend freigegeben sein. Bei einer VM hilft eine Netzwerkbrücke; bei NAT ist die direkte Quelladresse nötig. Freigaben nicht ins Internet weiterleiten.

Der Verbindungscode wird mit einmaliger Challenge und HMAC geprüft; die Antwort wird ebenfalls signiert. Der Code wird nicht im Klartext gesendet. **Die Tabellendaten sind bei HTTP nicht verschlüsselt**; verwende die Funktion im vertrauenswürdigen lokalen Netz. Verbindungscodes werden im lokalen Datenordner gespeichert und nicht in Git aufgenommen.

Dialog und Validierungsmeldungen sind auf Deutsch, Englisch, Niederländisch, Französisch, Italienisch, Spanisch und Dänisch verfügbar. Betriebssystem- und Netzwerkfehlermeldungen können von der Sprache des Betriebssystems abhängen.

## Prüfung und Grenzen

22 automatisierte Tests prüfen Paketgrenzen, lokale Einstellungen, Backup/Restore, Schreibfehler, Zeilenauswahl, Metadaten, Konflikte, Neuberechnung, deaktivierte Startfreigabe, alle sieben Sprachen sowie echte HTTP- und UDP-Kommunikation auf Loopback. Der Prototyp wurde auf Windows und der Linux-VM betrieben; Hardware-Upload, macOS, Raspberry Pi und iPad sind für diesen Branch nicht geprüft.
