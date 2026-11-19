# webMobaLedLib

Mit der MobaLedLib bringst du Leben auf deine Modellbahn: ein belebtes Haus, Straßenlaternen, Signale, Blaulicht, bewegte Servos und Sound. Die Steuerung übernimmt die Lichtmaschine, ein kleiner Computer auf einer Platine. Sie braucht dafür ein Programm.

Die webMobaLedLib ist das Programm für deinen Computer, mit dem du dieses Programm ohne Programmierkenntnisse erstellst. Du klickst aus einer Liste aus, was passieren soll. Die webMobaLedLib macht daraus das Programm für die Lichtmaschine und schickt es per USB-Kabel zur Lichtmaschine.

Details findest Du im Wiki: https://wiki.mobaledlib.de/anleitungen/webmobaledlib/einfuehrung

## OLED-Modus 5

`#define UI_MLLTime 5` zeigt in Zeile 1 den WLAN-Status und in Zeile 2 die IP-Adresse wie in Modus 4. Der Hostname steht in Zeile 3 und wird bei Bedarf in Zeile 4 fortgesetzt.

## ESP Einstellungen pro Blatt

Wähle unter **Optionen Werkzeuge** einen ESP32 als LED-Zentrale. Der Reiter **ESP Einstellungen** bietet die OLED-Modi 1 bis 5, eine animierte Vorschau mit Beispieldaten und die Optionen **Fotowiderstand aktivieren** und **Zustände werden gespeichert**. Beim Übertragen erzeugt WebMLL die entsprechenden Defines aus den Einstellungen des aktiven Blatts. Bereits in der Tabelle eingetragene Defines bleiben wirksam. Ein ausgewählter OLED-Modus hat Vorrang vor der Modusnummer aus der Tabelle.

Vorhandene Define-Zeilen bleiben auch bei aktivierten ESP-Einstellungen in der Tabelle sichtbar.

| Einstellung | Wirkung beim Übertragen |
| --- | --- |
| OLED-Anzeige, Modus 1 bis 5 | Setzt `USE_ESP32_EXTENSIONS`, `USE_UI` und `UI_MLLTime`. |
| Fotowiderstand aktivieren | Setzt `READ_LDR`. |
| Zustände werden gespeichert | Setzt `ENABLE_STORE_STATUS()`. |

Speichere die Optionen in der Arbeitsmappe und übertrage das Setup für das gewählte Blatt erneut auf den ESP32, damit die Firmware die Auswahl übernimmt.
Wenn du OLED, Fotowiderstand und Zustandsspeicherung im ESP-Reiter für das Blatt eingerichtet hast, kannst du die entsprechenden manuellen Define-Zeilen löschen. Beim nächsten **Setup übertragen** erzeugt WebMLL die Defines aus den gespeicherten Einstellungen.

Unter Windows startet die Desktop-Verknüpfung WebMLL ohne sichtbare Konsole. Für die Fehlersuche lässt sich weiterhin `install/start_windows.bat` direkt starten. Die OLED-Vorschau verwendet den von NiceGUI hinterlegten Namen des ESP-Reiters.

OLED-Modus 4 zeigt die berechnete MLL-Zeit auch bei deaktiviertem Fotowiderstand. Bei gleichbleibendem Dunkelheitswert bleibt die berechnete Zeit entsprechend stehen.
