import ctypes
import math
import sys
import time
from .UART import UART

# toCharArray_c
# @desc:    takes the items in a class and outputs them to an array with sizes no larger
#           than a char in the order that is defined in X_MESSAGE_0::dataPacketToArray
# @param:   none
# @returns: a tuple where the first element is the c array and the second is the size
def c_toCharArray(arr):
    return (ctypes.c_char * len(arr))(*arr)

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
            self.protocol = UART(self.dwf, hdwf)
        elif com_type == "CAN":
            pass
        elif com_type == "SPI":
            pass
        elif com_type == "I2C":
            pass
        else:
            print("invalid comunication protocol.")
            quit()
    def __del__(self):
        self.dwf.FDwfDeviceCloseAll()

    def sendData(self, arr):
        self.protocol.send(c_toCharArray(arr), ctypes.c_int(len(arr)))

    def receiveData(self):
        return self.protocol.receive()