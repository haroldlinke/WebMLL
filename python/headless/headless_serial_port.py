# Datei-Version: 1.00 (2026-11-19) - headless_serial_port.py
# Name:           headless_serial_port.py
# Path:           headless/headless_serial_port.py
# Version:        1.00
# Last Update:    2026-11-19
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-19  Konfigurationsfehler des COM-Treibers durch Initialisierung mit 9600 Baud behandeln
import logging  # v1.00
import time  # v1.00

import serial  # v1.00

logger = logging.getLogger(__name__)  # v1.00


def open_serial_port(connection):  # v1.00
    requested = connection.baudrate  # v1.00
    try:  # v1.00
        connection.open()  # v1.00
        return  # v1.00
    except serial.SerialException as error:  # v1.00
        if "Cannot configure port" not in str(error):  # v1.00
            raise  # v1.00
        logger.info("COM-Treiber konnte %s Baud nicht setzen; Initialisierung mit 9600 Baud", requested)  # v1.00
    connection.close()  # v1.00
    for delay in (.2, .5):  # v1.00
        time.sleep(delay)  # v1.00
        connection.baudrate = 9600  # v1.00
        try:  # v1.00
            connection.open()  # v1.00
        except serial.SerialException as error:  # v1.00
            connection.close()  # v1.00
            if "Cannot configure port" not in str(error) or delay == .5:  # v1.00
                raise  # v1.00
            continue  # v1.00
        try:  # v1.00
            if requested != 50:  # v1.00
                connection.baudrate = requested  # v1.00
            return  # v1.00
        except Exception:  # v1.00
            connection.close()  # v1.00
            raise  # v1.00
