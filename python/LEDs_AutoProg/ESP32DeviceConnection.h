#pragma once

#include <mbedtls/md.h>
#include <esp_system.h>

WiFiServer mllDeviceServer(2323);
WiFiClient mllDeviceClient;
bool mllDeviceAuthenticated = false;
bool mllDeviceNewSession = false;
unsigned long mllDeviceDeadline;
char mllDeviceNonce[33];
char mllDeviceResponse[65];
size_t mllDeviceResponseSize;

void MllDevicePoll()
{
    static bool listening = false;
    if (WiFi.status() != WL_CONNECTED)
    {
        if (listening)
        {
            mllDeviceClient.stop();
            mllDeviceServer.end();
            mllDeviceAuthenticated = false;
            listening = false;
        }
        return;
    }
    if (!listening)
    {
        mllDeviceServer.begin();
        listening = true;
    }
    if (!mllDeviceClient.connected())
    {
        mllDeviceAuthenticated = false;
        if (!mllDeviceServer.hasClient()) return;
        mllDeviceClient = mllDeviceServer.available();
        for (size_t i = 0; i < 32; i += 8)
            snprintf(mllDeviceNonce + i, 9, "%08lx", static_cast<unsigned long>(esp_random()));
        mllDeviceClient.println(mllDeviceNonce);
        mllDeviceDeadline = millis() + 5000;
        mllDeviceResponseSize = 0;
    }
    if (mllDeviceAuthenticated) return;
    if (static_cast<int32_t>(millis() - mllDeviceDeadline) >= 0)
    {
        mllDeviceClient.stop();
        return;
    }
    while (mllDeviceClient.available())
    {
        int ch = mllDeviceClient.read();
        if (ch == '\n' && mllDeviceResponseSize == 64)
        {
            const char *key = MLL_OTA_PASSWORD;
            uint8_t digest[32];
            const auto *algorithm = mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);
            if (mbedtls_md_hmac(algorithm, reinterpret_cast<const uint8_t *>(key), strlen(key),
                                reinterpret_cast<const uint8_t *>(mllDeviceNonce), 32, digest) == 0)
            {
                const char hex[] = "0123456789abcdef";
                uint8_t diff = 0;
                for (size_t i = 0; i < sizeof(digest); ++i)
                {
                    diff |= mllDeviceResponse[i * 2] ^ hex[digest[i] >> 4];
                    diff |= mllDeviceResponse[i * 2 + 1] ^ hex[digest[i] & 15];
                }
                if (!diff)
                {
                    mllDeviceAuthenticated = true;
                    mllDeviceNewSession = true;
                    mllDeviceClient.println("OK");
                    return;
                }
            }
        }
        else if (ch != '\n' && mllDeviceResponseSize < 64)
        {
            mllDeviceResponse[mllDeviceResponseSize++] = static_cast<char>(ch);
            continue;
        }
        mllDeviceClient.stop();
        return;
    }
}
