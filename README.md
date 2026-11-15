# WebMLL 3.42 mit ESP32-WLAN und OTA

Dieser Fork von [haroldlinke/WebMLL](https://github.com/haroldlinke/WebMLL) verbindet die Upstream-Version 3.42 mit den hier entwickelten Erweiterungen. Das Installationsverzeichnis und die Startskripte sind in der [Installationsanleitung](python/install/ANLEITUNG_Installation.md) beschrieben.

## ESP32 WROOM einrichten

1. Im Programm-Generator unter **Optionen Werkzeuge** den **ESP32 WROOM** wählen. Im Reiter **Entwicklungsumgebung** die vorhandene Installation von **PlatformIO** oder **Arduino IDE** auswählen.
2. Im Reiter **OTA** WLAN und bei Bedarf **OTA-Updates erlauben** aktivieren. Für OTA ein Passwort eintragen. Der Standard-Hostname ist `mobaledlib` und kann geändert werden.
3. Beim ersten Einrichten **Setup übertragen → USB** wählen, falls das Board OTA noch nicht unterstützt. Die OTA-fähige Firmware benötigt eine passende Partitionstabelle mit zwei Anwendungsslots.
4. Unter **OTA → WLAN über USB einrichten** den USB-Port auswählen. **WLANs suchen** zeigt die vom ESP32 gefundenen 2,4-GHz-Netze. Eine versteckte SSID lässt sich direkt eingeben. Nach erfolgreicher Anmeldung übernimmt WebMLL die gemeldete IP-Adresse als Ziel.
5. Für spätere Updates **Setup übertragen → WLAN (OTA)** wählen. WebMLL kompiliert das aktuelle Projekt mit der eingestellten Build-Umgebung. PlatformIO verwendet den persistenten OTA-Buildcache.

**Verbinden → WLAN** öffnet die Geräteverbindung für Testtasten und Farbtest. Der ESP32 kann alternativ über seine IP-Adresse angesprochen werden, wenn der Hostname im Netz nicht aufgelöst wird. Für einen Passwortwechsel per OTA im Übertragungsdialog das bisherige Passwort eingeben. Die neue Firmware erhält das im OTA-Reiter gespeicherte Passwort.

Farbtest, Servo, DM Servo und Sound verwenden eine offene Verbindung weiter. Beim automatischen Verbinden versucht WebMLL zuerst die für das Blatt gespeicherte ESP32-WLAN-Verbindung und greift bei Bedarf auf USB zurück. Über **Verbinden** lässt sich USB oder WLAN gezielt auswählen.

## OLED-Modus 4

In der Spalte **Beleuchtung, Sound oder andere Effekte** kann eine Zeile **Display** diesen Block enthalten:

```cpp
#ifdef ESP32
#define USE_ESP32_EXTENSIONS
#define USE_UI
#define UI_MLLTime 4
#endif
```

Modus 4 zeigt WLAN-Status, IP-Adresse, LDR und MobaLedLib-Zeit in vier zentrierten Zeilen. Die vorhandenen Modi 0 bis 3 bleiben auswählbar. Die Spalte bietet einen mehrzeiligen Editor und passt die Tabellenzeilenhöhe an.

## Patterngenerator und DCC

- RGB-Rampen werden je Dreiergruppe dargestellt. Der RGB-Modus wird aus PCF-Dateien übernommen. Goto-Startnummern und Pfeile stehen über der Goto-Tabelle.
- Der Schalter **RGB LED** aktiviert oder deaktiviert die Dreiergruppierung für das aktuelle Blatt. Größere Goto-Pfeile und kompaktere Abstände ober- und unterhalb der Goto-Tabelle machen mehr von der LED-Tabelle sichtbar.
- **Bild einfügen** fragt nach der Spalten-Nr. und setzt das Bild mittig darunter, eine Zeile unter der letzten LED. **Bilder löschen** entfernt nach Bestätigung ein ausgewähltes Bild oder alle Bilder des aktuellen Blatts. Die Bilddateien bleiben erhalten.
- **Test Pattern** spielt das Muster als LED-Vorschau im Browser ab. Die LED-Kreise zeigen bereits beim Öffnen die Farben des ersten Schritts und wechseln sie nach den eingestellten Schrittzeiten.
- Signalbilder stehen mit einer Zeile Abstand unter der letzten LED-Zeile. Eigene PCF-Dateien mit Bildern können als ZIP geladen werden.
- Per Rechtsklick auf eine Schrittzelle und **LED-Farbe wählen** werden im RGB-Modus die drei Kanalwerte für den gewählten Schritt gesetzt. In Spalte E lässt sich der Schritt im Dialog auswählen oder **Nur Zeilenfarbe** anwenden.
- **Dialog Wizard** startet die geführte Eingabe in der aktiven Datenzeile. Ist eine Kopfzeile ausgewählt, beginnt der Assistent in der ersten Datenzeile.
- **Adresse oder Name** lässt sich direkt in der Tabelle bearbeiten und akzeptiert eine DCC-Startadresse oder Freitext wie `Schalter D1`. Ein Doppelklick auf **Typ** öffnet bei gültiger Adresse den Schalterdialog für DCC, CAN und LNet.
- DCC-Adressspannen werden aus der Zahl der Funktionen berechnet und in die Tabelle geschrieben. Sechs Rot/Grün-Funktionen ab Adresse 2 ergeben direkt nach der Schalterwahl `2 - 4`. Die Testtasten nutzen eine bereits aktive WLAN-Verbindung.

## Neuerungen aus WebMLL 3.42

- Im Programm-Generator gibt es eine Suche über das aktuelle oder alle Blätter mit **Strg+F**.
- Die USB-Portauswahl filtert nach Zentralentyp. Unter **Andere Typen** lässt sich nach Bestätigung zum passenden Typ wechseln.
- WLAN, OTA, Hostname und Zieladresse werden pro Blatt gespeichert. Das Passwort bleibt lokal auf dem Rechner.
- Für die Ersteinrichtung steht im OTA-Reiter **Minimale Firmware per USB hochladen** zur Verfügung.

Die Bilddateien aus Harolds 3.42-Release sind enthalten, einschließlich der Signalbilder, der Werkzeugleisten-Symbole und der beiden Grafiken unter `python/lib`.

## Geprüfter Stand

Der Quellstand wurde mit dem offiziellen Release-ZIP abgeglichen. Python-Syntax und der Bildablauf wurden geprüft. OTA-Upload und Direktmodus stehen am ESP32 noch zur Prüfung aus.
