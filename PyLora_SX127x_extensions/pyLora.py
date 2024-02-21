import os
import gc
from PyLora_SX127x_extensions.constants import *

# Attempt to get machine type
try:
    machine = os.uname().machine
except Exception:
    machine = os.name

# Enable garbage collection
gc.enable()

class pyLora:
    IS_RPi = machine.startswith('armv')
    IS_ESP8266 = machine.startswith('ESP8266')
    IS_ESP32 = machine.startswith('ESP32') and not machine.startswith('Generic ESP32S3')
    IS_LORA32 = machine.startswith('LILYGO')
    IS_ESP32S3 = machine.startswith('Generic ESP32S3')  # Corrected check for ESP32S3

    __SX127X_LIB = None

    timeout_socket = None
    blocked_socket = None

    def __init__(self, verbose=False, do_calibration=False, calibration_freq=868, sf=7, cr=8, freq=868):
        auto_board_selection = None

        if self.IS_RPi:
            from PyLora_SX127x_extensions.board_config_rpi import BOARD_RPI
            auto_board_selection = BOARD_RPI

        elif self.IS_ESP32 or self.IS_LORA32:
            from PyLora_SX127x_extensions.board_config_esp32 import BOARD_ESP32
            auto_board_selection = BOARD_ESP32

        elif self.IS_ESP32S3:
            # Import and use the BOARD_ESP32S3 class
            from PyLora_SX127x_extensions.board_config_esp32s3 import BOARD_ESP32S3
            auto_board_selection = BOARD_ESP32S3

        # Collect garbage and check the amount of memory allocated and free again
        gc.collect()
        from PyLora_SX127x_extensions.LoRa import LoRa
        self.__SX127X_LIB = LoRa(Board_specification=auto_board_selection,
                                 verbose=verbose,
                                 do_calibration=do_calibration,
                                 calibration_freq=calibration_freq,
                                 cr=CODING_RATE.CR4_5,
                                 sf=sf,
                                 freq=freq,
                                 rx_crc=True)


    def send(self, content):
        self.__SX127X_LIB.set_mode(MODE.SLEEP)
        self.__SX127X_LIB.set_dio_mapping([1, 0, 0, 0])  # DIO0 = 1 is for TXDone, transmitting mode basically
        self.__SX127X_LIB.set_mode(MODE.STDBY)
        formatted = list(content)
        self.__SX127X_LIB.write_payload(formatted)  # I send my payload to LORA SX1276 interface
        self.__SX127X_LIB.set_mode(MODE.TX)  # I enter on TX Mode
        self.__SX127X_LIB.set_dio0_status(timeout_value=self.timeout_socket, socket_blocked=self.blocked_socket)

    def recv(self, size=230):
        """ Util Method for recv
            It will turn automatically the device on receive mode
        """
        self.__SX127X_LIB.set_mode(MODE.SLEEP)
        self.__SX127X_LIB.set_dio_mapping([0, 0, 0, 0])
        self.__SX127X_LIB.set_mode(MODE.RXCONT)
        self.__SX127X_LIB.set_dio0_status(timeout_value=self.timeout_socket, socket_blocked=self.blocked_socket)
        return bytes(self.__SX127X_LIB.payload)

    def settimeout(self, value):
        """ set timeout for operations
            After we determine if we want to send or receive, we need to specify a timeout
        """
        self.timeout_socket = value


    def setblocking(self, value):
        self.blocked_socket = value

    def get_rssi(self):
        return self.__SX127X_LIB.get_pkt_rssi_value()

    def sf(self, sf):
        self.__SX127X_LIB.set_spreading_factor(sf)
