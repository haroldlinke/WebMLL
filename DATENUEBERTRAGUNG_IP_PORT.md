# 5.41 – Datenübertragung: Quelladresse und Port

Datei-Version: 1.00 (2026-11-26), gilt für MobaLedLib Studio 5.41.

Nur optische Anpassung: Quelladresse ohne http:// und schmales separates Portfeld mit Vorgabe 45875. Gespeicherte URLs und Suchergebnisse werden automatisch aufgeteilt; intern wird die bisherige URL wieder zusammengesetzt. Eigene Ports, Hostnamen, IPv6 und vorhandenes HTTPS bleiben möglich. Ungültige Ports erhalten eine verständliche übersetzte Meldung. Datenübertragungsprotokoll und M08 bleiben unverändert. Dieser Git-Branch basiert direkt auf Original 5.41 und enthält keine M08-Vereinheitlichung.

Geprüft: 24 ursprüngliche Datenübertragungstests unter Windows; Aufteilung/Zusammensetzen und Portprüfung zusätzlich geprüft. Auf der Linux-VM bestehen dieselben 24 Tests im kombinierten Installationsstand; Backend startet. Neue Beschriftung und Portmeldung werden in DE/EN/NL/FR/IT/ES/DA mit dem echten Übersetzer geprüft.

Nicht geprüft: visuelle Browserbedienung des neuen 5.41-Stands und Datenübertragung zwischen zwei realen PCs mit dieser UI; native Ausführung unter macOS/Raspberry Pi. Keine Tabellen wurden zur Prüfung importiert.

| Datei (python/) | Version | Änderung |
|---|---|---|
| `_web/web_table_sync.py` | 1.09 | Getrennte Quelladress-/Portanzeige und Übersetzungen. |
| `csv/Web_Languages.csv` | Katalogergänzung 2026-11-26 | Getrennte Quelladress-/Portanzeige und Übersetzungen. |

Änderungspakete enthalten nur geänderte Dateien, keine Symbole, Tabellen oder Zugangsdaten. Basis ist das Original-Testrelease V3.6.0-5.41/webmobaledlib.zip. Kleines und kumulatives Paket enthalten deshalb die gleichen Featureänderungen gegen diese Basis. Installationsstände mit beiden Features werden getrennt von den beiden Git-Branches zusammengestellt.

Installationsprüfung 2026-11-26: Windows D:/WebMll mit beiden Features aktualisiert, release_tools full in Ordnung; offenes Windows-Programm muss noch neu gestartet werden. Linux-VM: /home/moosbewohner/WebMLL, WebMLL-TabellenSync-Test und WebMLL-M08-Test über den Original-Updater mit Sicherung auf 5.41 aktualisiert, danach beide Featureanpassungen eingespielt. Hauptdienst und Testinstanz neu gestartet; HTTP 8080 und 8098 jeweils 200. Keine bestehenden Tabellen importiert oder ersetzt.
