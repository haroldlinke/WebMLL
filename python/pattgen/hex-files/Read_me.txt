MainMenu_Form.py, at85neu.py und flashuno.py müssen ins Verzeichnis python/pattgen und die 6 hex files in Verzeichnis python/hex-files!
---------------------------------------------------------------------------------------------------------------------------------------

Bei mir läuft es problemlos unter Linux, wie es beim Mac aussieht -- keine Ahnung.

Verzeichnis pattgen:
--------------------

MainMenu_Form.py    Angepasstes Menu für Spezielle Module
at85neu.py          Programm zum flashen der ATTiny 85 für Servo / MP3 und DM-Servo (Charlieplex noch nicht implemetiert, ich muss mir erst
                                                                                     noch ne Charlipex Platine zum testen löten)
                                                                                     
flashuno.py         Flasht das Programm für den ISP Programmer mit HV Resetter (400 - Tina) auf einen UNO                                                                                    
---------------------------------------------------------------------------------------------------------------------------------------

Verzeichnis hex-files:
----------------------

400_bootloader.hex	ISP flasher für 400 Platine (Tina) mit Bootloader
400_standard.hex    ISP flasher für 400 Platine

510Servo_DIL.hex    Hex Datei für WS2811 in DIL Version auf der Platine
510Servo_SMD.hex    Hex Datei für WS2811 in SMD Version auf der Platine

AT85_Sound.hex      Ansteuerung von MP3 Modulen mit der Servo Platine

DM-Servo.hex        Hex Datei für den Direct Mode Servo


