#pragma once

// USB-only provisioning. Hex encoding keeps SSIDs and passwords out of the line framing.
static char wifiUsbLine[210];
static size_t wifiUsbLength = 0;
static bool wifiUsbReading = false;
static bool wifiUsbOverflow = false;
static unsigned long wifiUsbDeadline = 0;

static bool WifiUsbDecode(const char *src, char *dst, size_t capacity)
{
    size_t size = strlen(src);
    if (size % 2 || size / 2 >= capacity) return false;
    for (size_t i = 0; i < size; i += 2)
    {
        char hex[3] = {src[i], src[i + 1], 0};
        if (strspn(hex, "0123456789abcdefABCDEF") != 2) return false;
        dst[i / 2] = static_cast<char>(strtoul(hex, nullptr, 16));
        if (!dst[i / 2]) return false;
    }
    dst[size / 2] = 0;
    return true;
}

static bool WifiUsbReceive(char ch)
{
    if (!wifiUsbReading)
    {
        if (ch != '!') return false;
        wifiUsbLength = 0;
        wifiUsbOverflow = false;
        wifiUsbReading = true;
        return true;
    }
    if (ch == '\r') return true;
    if (ch != '\n')
    {
        if (wifiUsbLength < sizeof(wifiUsbLine) - 1) wifiUsbLine[wifiUsbLength++] = ch;
        else wifiUsbOverflow = true;
        return true;
    }
    wifiUsbReading = false;
    wifiUsbLine[wifiUsbLength] = 0;
    if (!wifiUsbOverflow && !strcmp(wifiUsbLine, "MLLWIFI SCAN") && !wifiUsbDeadline)
    {
        int count = WiFi.scanNetworks(false, false);
        for (int i = 0; i < count; ++i)
        {
            String ssid = WiFi.SSID(i);
            if (!ssid.length()) continue;
            Serial.print("!MLLWIFI NET ");
            Serial.print(WiFi.RSSI(i));
            Serial.print(' ');
            for (size_t j = 0; j < ssid.length(); ++j)
                Serial.printf("%02x", static_cast<unsigned char>(ssid[j]));
            Serial.println();
        }
        WiFi.scanDelete();
        Serial.println(count < 0 ? "!MLLWIFI ERROR Scan" : "!MLLWIFI DONE");
    }
    else if (!wifiUsbOverflow && !strncmp(wifiUsbLine, "MLLWIFI JOIN ", 13) && !wifiUsbDeadline)
    {
        char ssid[33], password[65];
        char *separator = strchr(wifiUsbLine + 13, ' ');
        if (separator)
        {
            *separator = 0;
            if (WifiUsbDecode(wifiUsbLine + 13, ssid, sizeof(ssid)) && *ssid &&
                WifiUsbDecode(separator + 1, password, sizeof(password)))
            {
                WiFi.disconnect();
                WiFi.persistent(true);
                WiFi.begin(ssid, password);
                wifiUsbDeadline = millis() + 25000;
                memset(password, 0, sizeof(password));
            }
        }
        if (!wifiUsbDeadline) Serial.println("!MLLWIFI ERROR Eingabe");
    }
    memset(wifiUsbLine, 0, sizeof(wifiUsbLine));
    return true;
}

static void WifiUsbPoll()
{
    if (!wifiUsbDeadline) return;
    if (WiFi.status() == WL_CONNECTED && WiFi.localIP() != IPAddress(0, 0, 0, 0))
    {
        Serial.print("!MLLWIFI IP ");
        Serial.println(WiFi.localIP());
    }
    else if (static_cast<int32_t>(millis() - wifiUsbDeadline) >= 0)
        Serial.println("!MLLWIFI ERROR Keine WLAN-Verbindung");
    else return;
    wifiUsbDeadline = 0;
}
