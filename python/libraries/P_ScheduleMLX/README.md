# PeterScheulde MobaLedLib Extension 

The library adds Peters alternativ scheduler to MobaLedLib.

More information see https://wiki.mobaledlib.de.

Questions / suggestions / praise / ...
  mobaledlibl@gmx.de

**Revision History:**

**Ver.: 0.01** 26.03.2024: initial test release
**Ver.: 0.16** 18.10.2024: Erste fertige Version (Beta).
**Ver.: 0.17** 25.10.2024: Fehler, wenn 2 Hausobjekte verwendet wurden.
**Ver.: 0.18** 05.01.2025: Debuging: Dank Jürgen (jueff) gibt es jetzt keinen Kompilerfehler mehr mit Streaming.
					       Debuging: Wenn Zufall verkürzt wird, LED mit ausgeben.
					       Variablendefinition aus Modulen herausgenommen, da Probleme mit ESP32.
**Ver.: 0.19** 29.06.2025: DstVar global definiert.
					       Raspberry Pico hinzugefügt. Danke Gerald.
**Ver.: 0.20** 25.08.2025: Bei einem Neustart wird ein alter Einschaltbefehl sofort aktiviert. Beispiel die LED soll um 8 Uhr angehen.
						   Bisher musste ein mal Mitternacht abgewartet werden, bis der Schaltauftrag aktiviert wurde. 
						   Jetzt passiert es nach dem Reset.
**Ver.: 0.21** 26.02.2026  Übergabe-Parameter DstVar* und enableCh wahlweise 8 oder 16 Bit (DatVar hat dann 16 Bit bei ESP32 & RP20, 8Bit bei Nano)
						   Korrektur der Abarbeitung von mehreren Objekten.
						   Debugausgabe "SchaltzeitInfo" angepasst.
						   Proc_Schedule: Wenn xZufall == 0 ist, wird eine Zwangspause zwischen 2 Schaltungen eingefügt von 100 mSec.
**Ver.: 0.22** 06.03.2026  MobaLedLib.properties angepasst an pyMobaLedLib ab Version 7.1.6 (Danke Harold).
**Ver.: 0.23** 18.06.2026  Random anpassen wegen Pico 2W. Random darf nicht mit Zufall = 0 aufgerufen werden (Danke Jörn).
**Ver.: 0.24** 18.06.2026  Vergessene Debug-Info beseitigt.


