import ctypes
import math
import sys
import time
from .UART import UART
from .CAN import CAN

# @name:    toCharArray_c
# @desc:    takes the items in a class and outputs them to an array with sizes no larger
#           than a char in the order that is defined in X_MESSAGE_0::dataPacketToArray
# @param:   none
# @returns: c char array
def c_toCharArray(arr):
    return (ctypes.c_char * len(arr))(*arr)

def c_toByteArray(arr):
    return (ctypes.c_ubyte * len(arr))(*arr)

class DAD():
    def __init__(self, com_type, config=0):
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
            self.protocol = CAN(self.dwf, hdwf, config)
        elif com_type == "SPI":
            pass
        elif com_type == "I2C":
            pass
        else:
            print("invalid comunication protocol.")
            quit()
    def __del__(self):
        self.dwf.FDwfDeviceCloseAll()

    def sendUART(self, data):
        if isinstance(self.protocol, UART):
            self.protocol.send(c_toCharArray(data), ctypes.c_int(len(data)))
        else:
            print("invalid")
            return 0
        return 1

    def sendCAN(self, data, ID, isExtended=0, isRemote=0):

        if len(data) > 8:
            print("Data too large")
            return -1
        
        rgbTX = c_toByteArray(data)
        self.protocol.send(rgbTX, ctypes.c_int(len(rgbTX)), ctypes.c_int(ID), ctypes.c_int(isExtended), ctypes.c_int(isRemote))

    def receiveCAN(self, cb):
        # call back should be a dictionary of CAN addrs with a parsing function
        ID, data = self.protocol.receive()
        cb[ID](data) if ID in cb else self.protocol.print(ID, data)
        