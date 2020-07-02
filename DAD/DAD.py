import ctypes
import math
import sys
import time
from UART import UART

class DAD():
    def __init__(self, com_type):
        if sys.platform.startswith("win"):
            self.dwf = ctypes.cdll.LoadLibrary("dwf.dll")
        elif sys.platform.startswith("darwin"):
            self.dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            self.dwf = ctypes.cdll.LoadLibrary("libdwf.so")

        hdwf = ctypes.c_int()

        print("Opening first device")
        #dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
        # device configuration of index 3 (4th) for Analog Discovery has 16kS digital-in/out buffer
        self.dwf.FDwfDeviceConfigOpen(ctypes.c_int(-1), ctypes.c_int(3), ctypes.byref(hdwf))
        if hdwf.value == 0:
            print("failed to open device")
            szerr = ctypes.create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            quit()
        if com_type == "UART":
            self.protocol = UART(ctypes.byref(self.dwf), ctypes.byref(hdwf))
        elif com_type == "CAN":
            pass
        elif com_type == "SPI":
            pass
        elif com_type == "I2C":
            pass
        else:
            print("invalid comunication protocol.")
            quit()
    def sendData(self, data, size):
        self.protocol.send(data, size)
    def receiveData(self):
        return self.protocol.receive()