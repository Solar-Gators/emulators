from ctypes import *
import math
import sys
import time
from './UART'

class DAD():
    def __init__(self, com_type):
        if sys.platform.startswith("win"):
            self.dwf = cdll.LoadLibrary("dwf.dll")
        elif sys.platform.startswith("darwin"):
            self.dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            self.dwf = cdll.LoadLibrary("libdwf.so")

        hdwf = c_int()

        print("Opening first device")
        #dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
        # device configuration of index 3 (4th) for Analog Discovery has 16kS digital-in/out buffer
        self.dwf.FDwfDeviceConfigOpen(c_int(-1), c_int(3), byref(hdwf))
        if hdwf.value == 0:
            print("failed to open device")
            szerr = create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            quit()
        if com_type == "UART":
            self.protocol = UART()
        elif com_type == "CAN":
            pass
        elif com_type == "SPI":
            pass
        elif com_type == "I2C":
            pass
        else:
            print("invalid comunication protocol.")
            quit()
    # Return received data
    def receive(self):
        if self.protocol == "UART":
            pass
        elif self.protocol == "CAN":
            dwf.FDwfDigitalCanRx(hdwf, byref(vID), byref(fExtended), byref(fRemote), byref(cDLC), rgbRX, c_int(sizeof(rgbRX)), byref(vStatus))
        