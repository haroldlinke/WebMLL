// MLLDynConfig.h - Konfiguration getrennt vom Programm (nur ESP32 und Pico)
// Version 1.04 (2026-11-22): ESP32-Neustart nach Konfiguration aus Hauptschleife statt MLLTask auf Core 0.
// Version 1.03 (2026-11-22): Konfigurationsprotokoll ueber USB oder authentifizierten WLAN-Stream.
// Version 1.02 (2026-11-19): Dateiformat 5 mit Abschnitt 'Parameter': LED Anzahl, LEDs je LED Kanal, ControllerCount und Controller-Tabelle (Pin, erste LED, LED-Anzahl je FastLED-Controller),
//                           LEDS_PER_CHANNEL, START_MSG und Start/Anzahl der Send-Inputs kommen aus der Konfigurationsdatei. SETUP_FASTLED() legt die Controller in einer Schleife
//                           ueber mllControllerConfig[] an (MllAddLeds). Zeilen mit '// v1.02'. Die ATmega Varianten benutzen diese Datei nicht (nur mit MLL_DYNAMIC_CONFIG).
//
// Ist MLL_DYNAMIC_CONFIG gesetzt (der Programm Generator schreibt es in LEDs_AutoProg.h), dann stehen die Datentabellen
//   Config[], Ext_Addr[], Store_Values[] und LED2Var_Tab[]
// nicht im Programm. Sie liegen als eine Datei (/mllcfg.bin) im Dateisystem (LittleFS) und werden beim Start in den RAM geladen.
// Der Programm Generator uebertraegt die Datei ueber die serielle Schnittstelle. Das Programm selbst wird nur geladen, wenn sich
// der Quelltext oder die Struktur (LED Anzahl, Pins, Erweiterungen, ...) geaendert hat. Erkannt wird das mit MLL_FIRMWARE_SIG.
//
// Dateiformat (little endian):
//   0  "MLLC"
//   4  Version (5)                                                                                              // v1.02
//   5  reserviert
//   6  Groesse von Config_RAM (u16)
//   8  Laenge Config (u32)
//  12  Laenge Ext_Addr (u32)
//  16  Laenge Store_Values (u32)
//  20  Laenge LED2Var_Tab (u32)
//  24  Laenge Startwerte (u32, Eintraege zu 3 Bytes: Kanal u16, Wert u8)
//  28  Laenge Parameter (u32)                                                                                   // v1.01
//  32  CRC32 ueber die Nutzdaten (u32)                                                                          // v1.01
//  36  Signatur der Firmware (16 Zeichen, MLL_FIRMWARE_SIG): die Datei wird nur geladen, wenn sie zu dieser Firmware gehoert  // v1.01
//  52  Nutzdaten: Config, Ext_Addr, Store_Values, LED2Var_Tab, Startwerte, Parameter                           // v1.01
//
// Parameter: u16 LED Anzahl, u16 Start der Send-Inputs, u16 Anzahl der Send-Inputs, u8 Zahl der LED Kanaele N, N mal u16 LEDs je Kanal,                   // v1.02
//            u8 ControllerCount, ControllerCount mal { u8 Pin, u16 LEDOffset, u16 LEDCount },                                                              // v1.02
//            LEDS_PER_CHANNEL (Text, mit 0 abgeschlossen), START_MSG (Text, mit 0 abgeschlossen)                                                          // v1.02
//
// Serielles Protokoll (Zeilen, die mit '~' beginnen; Antworten ebenfalls):
//   ~MLLCFG INFO                      -> ~MLLCFG INFO proto=2 sig=<Signatur> cfg=<CRC32 der Datei> valid=<0|1> free=<Bytes>
//   ~MLLCFG BEGIN <Laenge> <CRC32>    -> ~MLLCFG READY                      (CRC32 in Hex, ueber die ganze Datei)
//   ~MLLCFG DATA <Position> <Hex>     -> ~MLLCFG ACK <neue Position>
//   ~MLLCFG END                       -> ~MLLCFG OK  (danach Neustart)
//   ~MLLCFG ABORT                     -> ~MLLCFG OK
//   Fehler:                              ~MLLCFG ERR <Grund>

#ifndef __MLL_DYN_CONFIG_H__
#define __MLL_DYN_CONFIG_H__

#if defined(MLL_DYNAMIC_CONFIG)

#include <LittleFS.h>

#ifndef MLL_FIRMWARE_SIG
  #define MLL_FIRMWARE_SIG "unknown"
#endif

#define MLL_CFG_PATH         "/mllcfg.bin"
#define MLL_CFG_TMP          "/mllcfg.tmp"
#define MLL_CFG_SIG_LEN      16
// #define MLL_CFG_HEADER_SIZE  48                                                                                  // v1.01 (entfallen)
// #define MLL_CFG_VERSION      2                                                                                   // v1.01 (entfallen)
// #define MLL_CFG_PARTS        5                                                                                   // v1.01 (entfallen)
#define MLL_CFG_VERSION      5                                                                                   // v1.02
#define MLL_CFG_PARTS        6                                                                                   // v1.01
#define MLL_CFG_CRC_OFS      (8 + 4 * MLL_CFG_PARTS)                                                             // v1.01
#define MLL_CFG_SIG_OFS      (MLL_CFG_CRC_OFS + 4)                                                               // v1.01
#define MLL_CFG_HEADER_SIZE  (MLL_CFG_SIG_OFS + MLL_CFG_SIG_LEN)                                                 // v1.01
#define MLL_CFG_LINE_MAX     260
#define MLL_MAX_LED_CH       16                                                                                  // v1.01 (headless_dyn_config.MAX_LED_CHANNELS)
#define MLL_MAX_SEND_INPUTS  1778                                                                                // v1.01 (Laenge des Sendepuffers: (n+6)/7+1 muss in ein Byte passen)

typedef struct
    {
    const uint8_t *config;   uint32_t configLen;
    const uint8_t *extAddr;  uint32_t extAddrLen;
    const uint8_t *store;    uint32_t storeLen;
    const uint8_t *l2v;      uint32_t l2vLen;
    const uint8_t *start;    uint32_t startLen;
    uint8_t       *ram;      uint16_t ramLen;
    uint32_t       id;       // CRC32 der geladenen Datei
    bool           valid;
    } MllDynConfig_T;

static MllDynConfig_T mllDyn;
static const uint8_t  mllEmptyConfig[] = { EndCfg };

// Parameter aus der Konfigurationsdatei (v1.01). mllNumLeds und das Feld leds[] stehen in LEDs_AutoProg.ino (die LED Anzahl ist erst nach MllDynLoad() bekannt)
static uint16_t    mllChCnt[MLL_MAX_LED_CH];                       // LEDs je LED Kanal (DMX_LED_OFFSET/DMX_CHANNEL_COUNT)
static uint16_t    mllChOff[MLL_MAX_LED_CH];                       // erste LED des Kanals (Summe der LEDs der Kanaele davor)

typedef struct                                                                                                   // v1.02
    {
    uint8_t  Pin;                                                  // Arduino Pin (muss in MLL_LED_PINS stehen)
    uint16_t LEDOffset;                                            // erste LED in leds[]
    uint16_t LEDCount;                                             // Zahl der LEDs an diesem Pin
    } MllControllerConfig_T;

static MllControllerConfig_T mllControllerConfig[MLL_MAX_LED_CH];   // ein Eintrag je FastLED-Controller (SETUP_FASTLED)                // v1.02
static uint8_t     mllControllerCount = 0;                          // Zahl der benutzten Eintraege in mllControllerConfig[]           // v1.02
static uint16_t    mllStartSend = 0, mllTotalSend = 0;             // Start und Anzahl der Send-Inputs (ENABLE_SEND_INPUT)
static const char *mllLedsPerChannelTxt = ",0";
static const char *mllStartMsgTxt = "LEDs_AutoProg: no configuration";
#define MllLedsPerChannel()  (mllLedsPerChannelTxt)
#define MllStartMsg()        (mllStartMsgTxt)

MobaLedLib_C* pMobaLedLib;

// Bis zum Neustart gueltige Daten fuer die Tabellen (in der .ino ueber diese Makros benutzt)
#define MLL_EXT_ADDR_TAB      ((const Ext_Addr_T*)mllDyn.extAddr)
#define MLL_EXT_ADDR_SIZE     ((uint16_t)mllDyn.extAddrLen)
#define MLL_STORE_TAB         ((const uint8_t*)mllDyn.store)
#define MLL_STORE_SIZE        (mllDyn.storeLen)
#define MLL_L2V_TAB           ((const LED2Var_Tab_T*)mllDyn.l2v)
#define MLL_L2V_COUNT         (mllDyn.l2vLen / sizeof(LED2Var_Tab_T))

//-----------------------------------------------------------------
static uint32_t MllCrc32(uint32_t crc, const uint8_t *data, size_t len)
//-----------------------------------------------------------------
{
  crc = ~crc;
  while (len--)
     {
     crc ^= *data++;
     for (uint8_t k = 0; k < 8; k++) crc = (crc >> 1) ^ (0xEDB88320u & (0u - (crc & 1u)));
     }
  return ~crc;
}

//--------------------------
static bool MllFsBegin()
//--------------------------
{
  static bool Done = false, Ok = false;
  if (!Done)
     {
     Done = true;
     #ifdef ESP32
       Ok = LittleFS.begin(true);       // true: formatieren, wenn noch kein Dateisystem da ist
     #else
       Ok = LittleFS.begin();           // Pico: die Groesse steht in platformio.ini (board_build.filesystem_size)
     #endif
     }
  return Ok;
}

//---------------------------------
static size_t MllFsFreeBytes()
//---------------------------------
{
  #ifdef ESP32
    return LittleFS.totalBytes() - LittleFS.usedBytes();
  #else
    FSInfo fi;
    if (!LittleFS.info(fi)) return 0;
    return fi.totalBytes - fi.usedBytes;
  #endif
}

//-------------------------------------------------------------
static bool MllCfgParseHeader(const uint8_t *h, size_t fileSize, uint32_t *len /*[MLL_CFG_PARTS]*/, uint16_t *ramLen, uint32_t *crc)
//-------------------------------------------------------------
// Prueft Kennung, Version, Laengen und vor allem die Signatur: Eine Datei, die fuer eine andere Firmware erzeugt wurde, wird nie benutzt.
{
  if (fileSize < MLL_CFG_HEADER_SIZE) return false;
  if (memcmp(h, "MLLC", 4) != 0 || h[4] != MLL_CFG_VERSION) return false;
  if (strlen(MLL_FIRMWARE_SIG) != MLL_CFG_SIG_LEN || memcmp(h + MLL_CFG_SIG_OFS, MLL_FIRMWARE_SIG, MLL_CFG_SIG_LEN) != 0) return false;  // v1.01
  memcpy(ramLen, h + 6, 2);
  memcpy(len,    h + 8, 4 * MLL_CFG_PARTS);
  memcpy(crc,    h + MLL_CFG_CRC_OFS, 4);                                                                         // v1.01
  uint64_t Sum = 0;
  for (uint8_t i = 0; i < MLL_CFG_PARTS; i++) Sum += len[i];
  return Sum + MLL_CFG_HEADER_SIZE == fileSize;
}

//-------------------------
static bool MllParseParams(const uint8_t *p, uint32_t len)                                                       // v1.02
//-------------------------
// Abschnitt Parameter lesen (Aufbau siehe oben). Bei einem Fehler bleiben die Vorgabewerte (keine LEDs).
{
  if (len < 7) return false;
  uint16_t Num, Start, Total;
  uint8_t N;
  memcpy(&Num, p, 2); memcpy(&Start, p + 2, 2); memcpy(&Total, p + 4, 2); N = p[6];
  uint32_t Pos = 7;
  if (N > MLL_MAX_LED_CH || Total > MLL_MAX_SEND_INPUTS || len < Pos + 2UL * N + 1) return false;
  uint16_t Cnt[MLL_MAX_LED_CH], Off[MLL_MAX_LED_CH];
  memset(Cnt, 0, sizeof(Cnt)); memset(Off, 0, sizeof(Off));
  uint32_t Sum = 0;
  for (uint8_t i = 0; i < N; i++)
     {
     memcpy(&Cnt[i], p + Pos, 2); Pos += 2;
     Off[i] = (uint16_t)Sum;
     Sum += Cnt[i];
     }
  if (Sum > 0xFFFF) return false;
  uint16_t Leds = Num < Sum ? (uint16_t)Sum : Num;
  uint8_t ControllerCount = p[Pos++];
  if (ControllerCount > MLL_MAX_LED_CH || len < Pos + 5UL * ControllerCount + 2) return false;
  MllControllerConfig_T Ctrl[MLL_MAX_LED_CH];
  memset(Ctrl, 0, sizeof(Ctrl));
  for (uint8_t i = 0; i < ControllerCount; i++)
     {
     Ctrl[i].Pin = p[Pos];
     memcpy(&Ctrl[i].LEDOffset, p + Pos + 1, 2);
     memcpy(&Ctrl[i].LEDCount,  p + Pos + 3, 2);
     Pos += 5;
     if ((uint32_t)Ctrl[i].LEDOffset + Ctrl[i].LEDCount > Leds) return false;
     }
  const char *Txt[2];
  for (uint8_t t = 0; t < 2; t++)                                                                                // zwei Texte, mit 0 abgeschlossen
     {
     Txt[t] = (const char*)p + Pos;
     while (Pos < len && p[Pos]) Pos++;
     if (Pos >= len) return false;
     Pos++;
     }
  memcpy(mllChCnt, Cnt, sizeof(Cnt)); memcpy(mllChOff, Off, sizeof(Off));
  memcpy(mllControllerConfig, Ctrl, sizeof(Ctrl));
  mllControllerCount = ControllerCount;
  mllNumLeds = Leds;
  mllStartSend = Start; mllTotalSend = Total;
  mllLedsPerChannelTxt = Txt[0]; mllStartMsgTxt = Txt[1];
  return true;
}

#if defined(MLL_LED_PINS) && defined(MLL_ADD_LEDS)                                                              // v1.02
//-----------------------------------------------------------------
static CLEDController *MllAddLeds(const MllControllerConfig_T &Cfg)
//-----------------------------------------------------------------
// FastLED braucht den Pin als Konstante (Template-Argument). Die Firmware enthaelt deshalb einen Zweig fuer jeden
// Pin aus MLL_LED_PINS (LEDs_AutoProg.h, fest je Plattform); welcher benutzt wird, steht in der Konfigurationsdatei.
// Unbekannter Pin: NULL (die LEDs an diesem Pin bleiben dunkel).
{
  CRGB *Data = leds + Cfg.LEDOffset;
  switch (Cfg.Pin)
     {
     #define MLL_ADD_LEDS_CASE(P) case P: return &MLL_ADD_LEDS(P, Data, Cfg.LEDCount);
     MLL_LED_PINS(MLL_ADD_LEDS_CASE)
     #undef MLL_ADD_LEDS_CASE
     default: return NULL;
     }
}
#endif

//-------------------------
static bool MllDynLoad()
//-------------------------
// Laedt /mllcfg.bin in den RAM. Ohne gueltige Datei bleibt die Konfiguration leer (die LEDs bleiben dunkel),
// das Programm laeuft aber und kann ueber die serielle Schnittstelle eine neue Konfiguration bekommen.
{
  memset(&mllDyn, 0, sizeof(mllDyn));
  mllDyn.config    = mllEmptyConfig;
  mllDyn.configLen = sizeof(mllEmptyConfig);
  if (!MllFsBegin()) return false;
  File f = LittleFS.open(MLL_CFG_PATH, "r");
  if (!f) return false;
  size_t Size = f.size();
  uint8_t *Buf = Size >= MLL_CFG_HEADER_SIZE ? (uint8_t*)malloc(Size) : NULL;
  bool Ok = Buf != NULL && f.read(Buf, Size) == (int)Size;
  f.close();
  uint32_t Len[MLL_CFG_PARTS], Crc;
  uint16_t RamLen;
  if (Ok) Ok = MllCfgParseHeader(Buf, Size, Len, &RamLen, &Crc) && MllCrc32(0, Buf + MLL_CFG_HEADER_SIZE, Size - MLL_CFG_HEADER_SIZE) == Crc;
  uint8_t *Ram = NULL;
  if (Ok)
     {
     Ram = (uint8_t*)calloc(RamLen ? RamLen : 1, 1);
     Ok  = Ram != NULL;
     }
  if (!Ok)
     {
     free(Buf);
     free(Ram);
     return false;
     }
  const uint8_t *p = Buf + MLL_CFG_HEADER_SIZE;
  mllDyn.config   = p; mllDyn.configLen  = Len[0]; p += Len[0];
  mllDyn.extAddr  = p; mllDyn.extAddrLen = Len[1]; p += Len[1];
  mllDyn.store    = p; mllDyn.storeLen   = Len[2]; p += Len[2];
  mllDyn.l2v      = p; mllDyn.l2vLen     = Len[3]; p += Len[3];
  mllDyn.start    = p; mllDyn.startLen   = Len[4]; p += Len[4];
  if (!MllParseParams(p, Len[5])) { free(Buf); free(Ram); memset(&mllDyn, 0, sizeof(mllDyn)); mllDyn.config = mllEmptyConfig; mllDyn.configLen = sizeof(mllEmptyConfig); return false; }  // v1.01
  mllDyn.ram      = Ram;
  mllDyn.ramLen   = RamLen;
  mllDyn.id       = MllCrc32(0, Buf, Size);
  mllDyn.valid    = true;
  return true;
}

//-----------------------------------------------------------------
static void MllDynSetStartValues(MobaLedLib_C &MobaLedLib)
//-----------------------------------------------------------------
// Ersatz fuer Set_Start_Values(): die Startwerte der Eingangskanaele stehen in der Konfigurationsdatei
{
  for (uint32_t i = 0; i + 3 <= mllDyn.startLen; i += 3)
     {
     uint16_t Channel;
     memcpy(&Channel, mllDyn.start + i, 2);
     MobaLedLib.Set_Input(Channel, mllDyn.start[i + 2]);
     }
}

// ---- Empfang einer neuen Konfiguration ----------------------------------------------------------
static File     mllRxFile;
static bool     mllRxActive = false;
static uint32_t mllRxSize, mllRxPos, mllRxCrcExp, mllRxCrc;
static uint8_t  mllRxHead[MLL_CFG_HEADER_SIZE];

//----------------------------------------
static void MllRxAbort()
//----------------------------------------
{
  if (mllRxActive)
     {
     mllRxFile.close();
     mllRxActive = false;
     }
  if (MllFsBegin()) LittleFS.remove(MLL_CFG_TMP);
}

//----------------------------------------
// static void MllCfgErr(const __FlashStringHelper *Reason) // v1.03 (entfallen)
static void MllCfgErr(Stream &port, const __FlashStringHelper *Reason) // v1.03
//----------------------------------------
{
//   Serial.print(F("~MLLCFG ERR ")); // v1.03 (entfallen)
//   Serial.println(Reason); // v1.03 (entfallen)
  port.print(F("~MLLCFG ERR ")); // v1.03
  port.println(Reason); // v1.03
}

//---------------------------------------
static int MllHexVal(char c)
//---------------------------------------
{
  if (c >= '0' && c <= '9') return c - '0';
  if (c >= 'a' && c <= 'f') return c - 'a' + 10;
  if (c >= 'A' && c <= 'F') return c - 'A' + 10;
  return -1;
}

//------------------------------------------
// static void MllRestart() // v1.03 (entfallen)
static volatile bool mllCfgRestartPending = false; // v1.04
static uint32_t mllCfgRestartAt = 0; // v1.04

static void MllCfgPollRestart() // v1.04
{
#ifdef ESP32
  if (mllCfgRestartPending && (int32_t)(millis() - mllCfgRestartAt) >= 0) ESP.restart(); // v1.04
#endif
}

static void MllRestart(Stream &port) // v1.04
{
#ifdef ESP32
  // ESP.restart(); // v1.04 (entfallen: Empfang laeuft auf Core 0, Neustart in loop auf Core 1)
  mllCfgRestartAt = millis() + 750; // v1.04: Zeit fuer TCP-Abschlussantwort
  mllCfgRestartPending = true; // v1.04: nach dem Termin setzen
#else
  port.flush();
  delay(300);
  rp2040.restart();
#endif
}

//-------------------------------------------
// static void MllCfgProcessLine(char *Line) // v1.03 (entfallen)
static void MllCfgProcessLine(Stream &port, char *Line) // v1.03
//-------------------------------------------
{
  if (strcmp(Line, "INFO") == 0)
     {
     char s[120];
     sprintf(s, "~MLLCFG INFO proto=2 sig=%s cfg=%08lx valid=%d free=%lu", MLL_FIRMWARE_SIG, (unsigned long)mllDyn.id, mllDyn.valid ? 1 : 0, (unsigned long)(MllFsBegin() ? MllFsFreeBytes() : 0));
//      Serial.println(s); // v1.03 (entfallen)
     port.println(s); // v1.03
     }
  else if (strncmp(Line, "BEGIN ", 6) == 0)
     {
     MllRxAbort();
     char *End;
     uint32_t Size = strtoul(Line + 6, &End, 10);
     uint32_t Crc  = strtoul(End, NULL, 16);
//      if (Size < MLL_CFG_HEADER_SIZE)                  { MllCfgErr(F("size"));  return; } // v1.03 (entfallen)
//      if (!MllFsBegin())                               { MllCfgErr(F("fs"));    return; } // v1.03 (entfallen)
//      if (Size + 4096 > MllFsFreeBytes())              { MllCfgErr(F("full"));  return; } // v1.03 (entfallen)
     if (Size < MLL_CFG_HEADER_SIZE)                  { MllCfgErr(port, F("size"));  return; } // v1.03
     if (!MllFsBegin())                               { MllCfgErr(port, F("fs"));    return; } // v1.03
     if (Size + 4096 > MllFsFreeBytes())              { MllCfgErr(port, F("full"));  return; } // v1.03
     mllRxFile = LittleFS.open(MLL_CFG_TMP, "w");
//      if (!mllRxFile)                                  { MllCfgErr(F("open"));  return; } // v1.03 (entfallen)
     if (!mllRxFile)                                  { MllCfgErr(port, F("open"));  return; } // v1.03
     mllRxActive = true;
     mllRxSize = Size; mllRxCrcExp = Crc; mllRxPos = 0; mllRxCrc = 0;
//      Serial.println(F("~MLLCFG READY")); // v1.03 (entfallen)
     port.println(F("~MLLCFG READY")); // v1.03
     }
  else if (strncmp(Line, "DATA ", 5) == 0)
     {
//      if (!mllRxActive)                                { MllCfgErr(F("nobegin")); return; } // v1.03 (entfallen)
     if (!mllRxActive)                                { MllCfgErr(port, F("nobegin")); return; } // v1.03
     char *End;
     uint32_t Pos = strtoul(Line + 5, &End, 10);
//      if (Pos != mllRxPos)                             { MllCfgErr(F("pos"));   return; } // v1.03 (entfallen)
     if (Pos != mllRxPos)                             { MllCfgErr(port, F("pos"));   return; } // v1.03
     while (*End == ' ') End++;
     size_t Len = strlen(End);
     uint8_t Buf[MLL_CFG_LINE_MAX / 2];
//      if ((Len & 1) || Len / 2 > sizeof(Buf) || mllRxPos + Len / 2 > mllRxSize) { MllCfgErr(F("len")); return; } // v1.03 (entfallen)
     if ((Len & 1) || Len / 2 > sizeof(Buf) || mllRxPos + Len / 2 > mllRxSize) { MllCfgErr(port, F("len")); return; } // v1.03
     for (size_t i = 0; i < Len; i += 2)
        {
        int h = MllHexVal(End[i]), l = MllHexVal(End[i + 1]);
//         if (h < 0 || l < 0)                           { MllCfgErr(F("hex"));   return; } // v1.03 (entfallen)
        if (h < 0 || l < 0)                           { MllCfgErr(port, F("hex"));   return; } // v1.03
        Buf[i / 2] = (uint8_t)(h << 4 | l);
        }
     size_t n = Len / 2;
     if (mllRxFile.write(Buf, n) != n)
        {
        MllRxAbort();
//         MllCfgErr(F("write")); // v1.03 (entfallen)
        MllCfgErr(port, F("write")); // v1.03
        return;
        }
     for (size_t i = 0; i < n && mllRxPos + i < MLL_CFG_HEADER_SIZE; i++) mllRxHead[mllRxPos + i] = Buf[i];
     mllRxCrc = MllCrc32(mllRxCrc, Buf, n);
     mllRxPos += n;
//      Serial.print(F("~MLLCFG ACK ")); // v1.03 (entfallen)
//      Serial.println(mllRxPos); // v1.03 (entfallen)
     port.print(F("~MLLCFG ACK ")); // v1.03
     port.println(mllRxPos); // v1.03
     }
  else if (strcmp(Line, "END") == 0)
     {
//      if (!mllRxActive)                                { MllCfgErr(F("nobegin")); return; } // v1.03 (entfallen)
     if (!mllRxActive)                                { MllCfgErr(port, F("nobegin")); return; } // v1.03
     mllRxFile.close();
     mllRxActive = false;
     uint32_t Len[MLL_CFG_PARTS], Crc;
     uint16_t RamLen;
     bool Ok = mllRxPos == mllRxSize && mllRxCrc == mllRxCrcExp && MllCfgParseHeader(mllRxHead, mllRxSize, Len, &RamLen, &Crc);
     if (!Ok)
        {
        MllRxAbort();
//         MllCfgErr(F("check")); // v1.03 (entfallen)
        MllCfgErr(port, F("check")); // v1.03
        return;
        }
     LittleFS.remove(MLL_CFG_PATH);
//      if (!LittleFS.rename(MLL_CFG_TMP, MLL_CFG_PATH))   { LittleFS.remove(MLL_CFG_TMP); MllCfgErr(F("rename")); return; } // v1.03 (entfallen)
//      Serial.println(F("~MLLCFG OK")); // v1.03 (entfallen)
//      MllRestart(); // v1.03 (entfallen)
     if (!LittleFS.rename(MLL_CFG_TMP, MLL_CFG_PATH))   { LittleFS.remove(MLL_CFG_TMP); MllCfgErr(port, F("rename")); return; } // v1.03
     port.println(F("~MLLCFG OK")); // v1.03
     MllRestart(port); // v1.03
     }
  else if (strcmp(Line, "ABORT") == 0)
     {
     MllRxAbort();
//      Serial.println(F("~MLLCFG OK")); // v1.03 (entfallen)
     port.println(F("~MLLCFG OK")); // v1.03
     }
//   else MllCfgErr(F("cmd")); // v1.03 (entfallen)
  else MllCfgErr(port, F("cmd")); // v1.03
}

//-----------------------------------
// static bool MllCfgReceive(char c) // v1.03 (entfallen)
static bool MllCfgReceive(char c, Stream &port) // v1.03
//-----------------------------------
// Wird fuer jedes empfangene Zeichen aufgerufen. Zeilen, die mit '~' beginnen, werden hier vollstaendig gelesen
// und ausgefuehrt (dauert bei 115200 Baud etwa 20 ms). Gibt true zurueck, wenn das Zeichen verbraucht wurde.
{
  if (c != '~') return false;
  static char Line[MLL_CFG_LINE_MAX];
  size_t n = 0;
  bool Over = false, Complete = false;
  unsigned long Deadline = millis() + 1000;
  while (millis() < Deadline)
     {
//      if (!Serial.available()) continue; // v1.03 (entfallen)
//      char x = Serial.read(); // v1.03 (entfallen)
     if (!port.available()) { delay(1); continue; }  // v1.03: WLAN und Watchdog bedienen
     char x = port.read(); // v1.03
     Deadline = millis() + 1000;
     if (x == '\n') { Complete = true; break; }
     if (x == '\r') continue;
     if (n < sizeof(Line) - 1) Line[n++] = x;
     else Over = true;
     }
  Line[n] = 0;
//   if (!Complete || Over)                      MllCfgErr(F("line")); // v1.03 (entfallen)
//   else if (strncmp(Line, "MLLCFG ", 7) == 0)  MllCfgProcessLine(Line + 7); // v1.03 (entfallen)
//   else                                        MllCfgErr(F("cmd")); // v1.03 (entfallen)
  if (!Complete || Over)                      MllCfgErr(port, F("line")); // v1.03
  else if (strncmp(Line, "MLLCFG ", 7) == 0)  MllCfgProcessLine(port, Line + 7); // v1.03
  else                                        MllCfgErr(port, F("cmd")); // v1.03
  return true;
}

#endif // MLL_DYNAMIC_CONFIG
#endif // __MLL_DYN_CONFIG_H__
