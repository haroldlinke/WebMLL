// MLLIdentify.h - Erkennung der gewaehlten Zentrale in der Auswahl des COM Ports (nur ESP32 und Pico) und Status LEDs des ESP32
// Version 1.01 (2026-11-27): Pico: die Pins der Mainboard LEDs werden beim Start des Blinkens Ausgang (die Kopfdatei definiert Mainboard_LED1..3 nicht mehr)
// Version 1.00 (2026-11-23): Neu
// Author: Jürgen Winkler
//   - Zentrale-Erkennung im COM-Port-Dialog: Blinken der 3 Mainboard-LEDs bei ~MLLIDENT 1, Stop bei ~MLLIDENT 0
//   - Protokoll mit '~' Prefix (gemeinsame Empfangsroutine in MLLAdminCommunication.h): ~MLLIDENT 1/0, keine Antwort
//   - ESP32: Status LEDs sind 3 WS2811-Bytes (GRB) auf LED Kanal 7 (gelb=r, weiss=g, blau=b), keine Pins
//   - Pico: Status LEDs an physischen Pins LED1_PIN/LED2_PIN/LED3_PIN (Mainboard_LED1/2/3)
//   - LED-Bus-Pins werden nicht angesteuert (Konfiguration via MLL_DYNAMIC_CONFIG / MLL_LED_BUS_PINS)
//   - LED-Zustand vor dem Blinken speichern, beim Stopp direkt wiederherstellen (ESP32: Bytes in leds[], Pico: Pegel der Pins; die Pins werden beim Start Ausgang)
//   - MllIdentUpdate() wird aus MLLMainLoop() nach Set_Mainboard_LEDs() und vor FastLED.show() aufgerufen (LEDs_AutoProg.ino)
//   - Kein Fallback auf Modul-LED (MLL_IDENT_MODULE_LED entfernt)
//   - MLL_ESP32_STATUS_LEDS Define fuer ESP32-spezifische WS2811 Status LEDs
//   - Keine Serial-Ausgaben (stille Operation)
//   - Timeout 3000 ms, 500 ms an / 500 ms aus (1 Hz)
//
// Solange der Programm Generator (webMLL) in der Auswahl des COM Ports eine ESP32- oder Pico-Zentrale gewaehlt hat,
// blinken deren drei LEDs auf der Hauptplatine. Die Ausgabe der LED Daten
// und die Verarbeitung der MobaLedLib laufen dabei unveraendert weiter.
//
// Serielles Protokoll (Zeilen, die mit '~' beginnen, Empfang in MLLAdminCommunication.h; keine Antwort, Fehler: ~MLLERR MLLIDENT):
//   ~MLLIDENT 1   Blinken starten bzw. verlaengern (der PC schickt die Zeile jede Sekunde)
//   ~MLLIDENT 0   Blinken beenden
// Kommt MLL_IDENT_TIMEOUT ms lang keine Zeile mehr (serielle Verbindung getrennt, Dialog geschlossen), endet das Blinken.
// Ein Neustart beendet es ebenfalls (der Zustand liegt nur im RAM).
//
// ESP32: Die 3 Status LEDs (gelb, weiss, blau) sind die ersten 3 Bytes eines WS2811 auf LED Kanal 7 (kein Pin).
// Pico: Die 3 Status LEDs haengen an den Pins LED1_PIN, LED2_PIN, LED3_PIN (Mainboard_LED1..3).
// Pins, die als LED Bus benutzt werden, werden nicht angesteuert.
// Die Busse kommen aus der Konfigurationsdatei (MLL_DYNAMIC_CONFIG, mllControllerConfig[])
// oder aus MLL_LED_BUS_PINS (vom Programm Generator in LEDs_AutoProg.h geschrieben).
// Die ATmega Varianten benutzen diese Datei nicht (MLL_IDENTIFY ist dort nicht gesetzt).

#ifndef __MLL_IDENTIFY_H__
#define __MLL_IDENTIFY_H__

#include "MLLDynConfig.h"

#define MLL_IDENT_TIMEOUT   3000   // ms ohne Zeile vom PC, danach endet das Blinken
#define MLL_IDENT_PERIOD     500   // ms je Halbperiode (1 Hz)

// ESP32: Die drei Status LEDs der Hauptplatine (gelb, weiss, blau) haengen an einem WS2811 am Anfang von LED Kanal 7: das erste Pixel des Kanals
// ist leds[First] (First = MllStatusLedFirst()): LED1 (gelb) = leds[First].r, LED2 (weiss) = leds[First].g, LED3 (blau) = leds[First].b. Die Farbreihenfolge
// der LED Busse ist immer GRB (NEOPIXEL). Der Programm Generator legt dazu immer einen Controller fuer LED Kanal 7 mit mindestens einer LED an.
// First ist der Index in leds[] (uint16_t):
//   mit Konfigurationsdatei: LEDOffset des Eintrags mit LEDChannel == 7 in mllControllerConfig[]
//   klassische Kopfdatei:    MLL_STATUS_LED_OFFSET (vom Programm Generator geschrieben)
// Die Werte werden in leds[] geschrieben, bevor FastLED.show() die Daten sendet. Fehlt LED Kanal 7 (alte Kopfdatei), bleiben die Status LEDs aus.
#if defined(ESP32) && (defined(MLL_DYNAMIC_CONFIG) || defined(MLL_STATUS_LED_OFFSET))
  #define MLL_ESP32_STATUS_LEDS
  #define MLL_STATUS_LED_CHANNEL  7        // LED Kanal mit den Status LEDs
  #define MLL_STATUS_LED_NONE     0xFFFF   // kein Pixel fuer die Status LEDs
  #ifndef MLL_STATUS_LED1_ON
    #define MLL_STATUS_LED1_ON    255      // Wert der gelben LED1 bei eingeschalteter LED
  #endif
  #ifndef MLL_STATUS_LED2_ON
    #define MLL_STATUS_LED2_ON    90       // Wert der weissen LED2 (reduzierte Helligkeit)
  #endif
  #ifndef MLL_STATUS_LED3_ON
    #define MLL_STATUS_LED3_ON    180      // Wert der blauen LED3 (reduzierte Helligkeit)
  #endif

//-----------------------------------------
static uint16_t MllStatusLedFirst()
//-----------------------------------------
// Index des Pixels mit den Status LEDs in leds[]. MLL_STATUS_LED_NONE, wenn es kein Pixel gibt
{
#if defined(MLL_DYNAMIC_CONFIG)
  static uint16_t First = 0xFFFE;     // 0xFFFE: noch nicht gesucht (beim ersten Aufruf in loop() ist die Konfiguration schon geladen)
  if (First == 0xFFFE)
     {
     First = MLL_STATUS_LED_NONE;
     for (uint8_t i = 0; i < mllControllerCount; ++i)
         if (mllControllerConfig[i].LEDChannel == MLL_STATUS_LED_CHANNEL && mllControllerConfig[i].LEDCount > 0 && mllControllerConfig[i].LEDOffset < mllNumLeds)
            {
            First = mllControllerConfig[i].LEDOffset;
            break;
            }
     }
  return First;
#else
  return MLL_STATUS_LED_OFFSET;
#endif
}

//-----------------------------------------
static void MllStatusLedSet(uint8_t Nr, bool On)
//-----------------------------------------
// Nr 0..2 = LED1 (gelb) = .r, LED2 (weiss) = .g, LED3 (blau) = .b des Pixels leds[MllStatusLedFirst()]
{
  uint16_t First = MllStatusLedFirst();
  if (First == MLL_STATUS_LED_NONE) return;
  switch (Nr)
     {
     case 0: leds[First].r = On ? MLL_STATUS_LED1_ON : 0; break;
     case 1: leds[First].g = On ? MLL_STATUS_LED2_ON : 0; break;
     case 2: leds[First].b = On ? MLL_STATUS_LED3_ON : 0; break;
     }
}
#endif // ESP32 && (MLL_DYNAMIC_CONFIG || MLL_STATUS_LED_OFFSET)

#if defined(ESP32)
  #define MLL_IDENT_FIRST_PIN_LED  0  // keine Pin-LEDs (Status LEDs sind WS2811-Bytes auf Kanal 7)
  static const uint8_t mllIdentPins[] = { };
#else
  #define MLL_IDENT_FIRST_PIN_LED  0
  static const uint8_t mllIdentPins[] = { LED1_PIN, LED2_PIN, LED3_PIN };
#endif

static uint8_t       mllIdentMask    = 0;      // Bit i: mllIdentPins[i] blinkt (0..2 = Mainboard LEDs)
static bool          mllIdentActive  = false;
static unsigned long mllIdentLastCmd = 0;

// Gespeicherte LED-Zustaende vor dem Blinken (fuer Wiederherstellung bei Stopp)
#if defined(MLL_ESP32_STATUS_LEDS)
  static uint8_t mllIdentSavedR = 0, mllIdentSavedG = 0, mllIdentSavedB = 0;
#else
  // Ausgangspegel jedes Pins beim Start von Ident; die Pins werden dabei Ausgang
  static bool mllIdentSavedLevel[3] = { false, false, false };
#endif

//-----------------------------------------
static bool MllIdentPinUsed(uint8_t Pin)
//-----------------------------------------
// true, wenn der Pin als LED Bus (oder DMX) benutzt wird
{
#if defined(MLL_DYNAMIC_CONFIG)
  for (uint8_t ch = 0; ch < mllControllerCount; ++ch)
      if (mllControllerConfig[ch].Pin == Pin) return true;
#elif defined(MLL_LED_BUS_PINS)
  static const uint8_t BusPins[] = { MLL_LED_BUS_PINS };
  for (uint8_t i = 0; i < sizeof(BusPins); ++i)
      if (BusPins[i] == Pin) return true;
#elif defined(ESP32)
  return true;   // aeltere Kopfdatei ohne MLL_LED_BUS_PINS: alle Pins koennten LED Busse sein
#endif
#if defined(USE_DMX_PIN)
  if (Pin == USE_DMX_PIN) return true;
#endif
  return false;
}

//-----------------------------------------
static bool MllIdentLedAvailable(uint8_t i)
//-----------------------------------------
// true, wenn die Mainboard LED i (0..2) zum Blinken benutzt werden kann
{
#if defined(ESP32)
  #if defined(MLL_ESP32_STATUS_LEDS)
    return MllStatusLedFirst() != MLL_STATUS_LED_NONE;  // die Status LEDs sind Bytes im WS2811 auf LED Kanal 7 und stoeren die LED Daten nicht
  #else
    return false;
  #endif
#else
  return !MllIdentPinUsed(mllIdentPins[i]);
#endif
}

//-----------------------------------------
static void MllIdentSetPins(bool On)
//-----------------------------------------
{
#if defined(MLL_ESP32_STATUS_LEDS)
  for (uint8_t i = 0; i < 3; ++i)
      if (mllIdentMask & (1 << i)) MllStatusLedSet(i, On ^ (i==1));
#endif
  for (uint8_t i = MLL_IDENT_FIRST_PIN_LED; i < sizeof(mllIdentPins); ++i)
      if (mllIdentMask & (1 << i)) digitalWrite(mllIdentPins[i], (On ^(i==1)) ? HIGH : LOW);
}

//-----------------------------------------
static void MllIdentStart()
//-----------------------------------------
{
  mllIdentLastCmd = millis();
  if (mllIdentActive) return;
  mllIdentMask = 0;
  for (uint8_t i = 0; i < 3; ++i)
      if (MllIdentLedAvailable(i)) mllIdentMask |= 1 << i;
  // Kein Fallback auf Modul-LED: wenn keine Mainboard LED verfuegbar, wird nicht geblinkt

  // Aktuellen LED-Zustand speichern (vor dem Blinken)
  #if defined(MLL_ESP32_STATUS_LEDS)
    uint16_t First = MllStatusLedFirst();
    if (First != MLL_STATUS_LED_NONE) {
      mllIdentSavedR = leds[First].r;
      mllIdentSavedG = leds[First].g;
      mllIdentSavedB = leds[First].b;
    }
  #else
    for (uint8_t i = 0; i < sizeof(mllIdentPins); ++i)
      if (mllIdentMask & (1 << i)) pinMode(mllIdentPins[i], OUTPUT);  // nur Pins, die blinken (nicht die LED Busse)
    for (uint8_t i = 0; i < sizeof(mllIdentPins); ++i)
      mllIdentSavedLevel[i] = digitalRead(mllIdentPins[i]);  // gelesen wird der aktuelle Pegel
  #endif

  mllIdentActive = true;
}

//-----------------------------------------
static void MllIdentStop()
//-----------------------------------------
{
  if (!mllIdentActive) return;

  // Gespeicherten LED-Zustand wiederherstellen (direkt, ohne Zwischenschritt 'aus': sonst blitzt die mittlere LED kurz auf)
  #if defined(MLL_ESP32_STATUS_LEDS)
    uint16_t First = MllStatusLedFirst();
    if (First != MLL_STATUS_LED_NONE) {
      leds[First].r = mllIdentSavedR;
      leds[First].g = mllIdentSavedG;
      leds[First].b = mllIdentSavedB;
    }
  #else
    for (uint8_t i = 0; i < sizeof(mllIdentPins); ++i)
      if (mllIdentMask & (1 << i)) digitalWrite(mllIdentPins[i], mllIdentSavedLevel[i] ? HIGH : LOW);  // nur Pins, die geblinkt haben
  #endif

  mllIdentMask = 0;
  mllIdentActive = false;
}

//-----------------------------------------
static void MllIdentUpdate()
//-----------------------------------------
// Wird in jedem Durchlauf nach Set_Mainboard_LEDs() aufgerufen: waehrend des Blinkens gilt der Zustand von hier
{
  if (!mllIdentActive) return;
  unsigned long Now = millis();
  if (Now - mllIdentLastCmd > MLL_IDENT_TIMEOUT) { MllIdentStop(); return; }
  MllIdentSetPins((Now / MLL_IDENT_PERIOD) & 1);
}

//-----------------------------------------
static void MllIdentProcessLine(Stream &port, char *Line)
//-----------------------------------------
// Verarbeitet MLLIDENT Kommandos: "MLLIDENT 1" startet Blinken, "MLLIDENT 0" stoppt
{
    if (strcmp(Line, "1") == 0) MllIdentStart();
    else if (strcmp(Line, "0") == 0) MllIdentStop();
    else MllCommunicationError(port, F("MLLIDENT"));
}

#endif // __MLL_IDENTIFY_H__
