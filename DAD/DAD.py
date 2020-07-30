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
    
    def __init__(self):
        # Available Protocols
        self.__CAN = []
        self.__UART = []
        self.__I2C = []
        self.__SPI = []

        if sys.platform.startswith("win"):
            self.dwf = ctypes.cdll.LoadLibrary("dwf.dll")
        elif sys.platform.startswith("darwin"):
            self.dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            self.dwf = ctypes.cdll.LoadLibrary("libdwf.so")

        self.hdwf = ctypes.c_int()
        

        print("Opening first device")
        #dwf.FDwfDeviceOpen(c_int(-1), byref(self.hdwf))
        # device configuration of index 3 (4th) for Analog Discovery has 16kS digital-in/out buffer
        self.dwf.FDwfDeviceConfigOpen(ctypes.c_int(-1), ctypes.c_int(3), ctypes.byref(self.hdwf))
        if self.hdwf.value == 0:
            print("failed to open device")
            szerr = ctypes.create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            quit()

    def CAN_init(self, config = None):
        self.__CAN.append(CAN(self.dwf, self.hdwf, config))
        return 0

    def UART_init(self, config = None):
        self.__UART.append(UART(self.dwf, self.hdwf))
        return 0

    def posSupply_init(self, config= None):
        supplyVoltage = ctypes.c_double()
        # set up analog IO channel nodes
        # enable positive supply
        self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_double(True)) 
        # set voltage to 5 V
        self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, ctypes.c_int(0), ctypes.c_int(1), ctypes.c_double(5.0))
        # master enable
        self.dwf.FDwfAnalogIOEnableSet(self.hdwf, ctypes.c_int(True))
        self.dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf, ctypes.c_int(2), ctypes.c_int(0), ctypes.byref(supplyVoltage))
        # self.setPowerSupply_p(5.0)
        IsEnabled = ctypes.c_bool()
        self.dwf.FDwfAnalogIOEnableStatus(self.hdwf, ctypes.byref(IsEnabled))
        if(IsEnabled):
            print("Power supplies on.")
        else:
            print("Power supplies off.")
        print("Supply voltage {}".format(supplyVoltage.value))
        
    def __del__(self):
        self.dwf.FDwfDeviceCloseAll()

    def sendUART(self, data, channel = 0):
        self.__UART[channel].send(data)

    def sendCAN(self, data, ID, isExtended=0, isRemote=0, channel = 0):

        if len(data) > 8:
            print("Data too large")
            return -1
        
        rgbTX = c_toByteArray(data)
        self.__CAN[channel].send(rgbTX, ctypes.c_int(len(rgbTX)), ctypes.c_int(ID), ctypes.c_int(isExtended), ctypes.c_int(isRemote))

    def receiveCAN(self, cb, channel = 0):
        # call back should be a dictionary of CAN addrs with a parsing function
        ID, data = self.__CAN[channel].receive()
        if ID != -1:
            if ID in cb:
                cb[ID](data)
            else:
                CAN.print(ID, data)
                
    def setPowerSupply_p(self, val):
        if val < 0:
            # enable positive supply
            self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_double(True)) 
            # set voltage to 5 V
            self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, ctypes.c_int(0), ctypes.c_int(1), ctypes.c_double(float(5.0)))
        
            self.dwf.FDwfAnalogIOEnableSet(self.hdwf, ctypes.c_int(True))
            
    def setPowerSupply_n(self, val):
        if val > 0:
            return False
        return False

    def isPowerSupplyOn(self):
        IsEnabled = ctypes.c_bool()
        self.dwf.FDwfAnalogIOEnableStatus(self.hdwf, ctypes.byref(IsEnabled))
        if(IsEnabled):
            "Power supplies on."
        return IsEnabled

    # val is a bool
    def setAnalogIOStatus(self, val):
        # self.dwf.FDwfAnalogIOEnableSet(self.hdwf, ctypes.c_int(False)) 
        # self.dwf.FDwfAnalogIOEnableSet(self.hdwf, ctypes.c_int(True))
        self.dwf.FDwfAnalogIOEnableSet(self.hdwf, ctypes.c_int(val))
    
    def getSupplyVoltage(self):
        supplyVoltage = ctypes.c_double()
        time.sleep(0.1)
        self.dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf, ctypes.c_int(2), ctypes.c_int(0), ctypes.byref(supplyVoltage))
        
        return supplyVoltage.value