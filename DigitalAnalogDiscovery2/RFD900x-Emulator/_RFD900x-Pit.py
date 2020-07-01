
from ctypes import *
import math
import sys
import time

# All data is sent from telemetry as uint8_t
# Data is sent lsByte first
# Order is derived from X_MESSAGE_0::dataPacketToArray
class OrionData(Structure):
    _fields_ = ("lowCell", c_uint), ("highCell", c_uint), ("avgCell", c_uint), ("packSumVoltage", c_uint)
    def toArray_8(self):
        pass

class Proton1Data(Structure):
    _fields_ = ("vin", c_uint), ("vout", c_uint), ("iin", c_uint), ("temp", c_uint)

class MitsubaData(Structure):
    _fields_ = ("rpm", c_int), ("temp", c_int), ("FET_oh_level", c_int)

class Axis(Structure):
    _fields_ = ("x", c_uint), ("y", c_uint), ("z", c_uint)

class IMUData(Structure):
    _fields_ = [("accel", Axis), ("gyro", Axis), ("linear", Axis), ("temp", c_uint)]

class GPSData(Structure):
    _fields_ = ("lng", c_int), ("lat", c_int)

if sys.platform.startswith("win"):
    dwf = cdll.LoadLibrary("dwf.dll")
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()

print("Opening first device")
#dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
# device configuration of index 3 (4th) for Analog Discovery has 16kS digital-in/out buffer
dwf.FDwfDeviceConfigOpen(c_int(-1), c_int(3), byref(hdwf)) 

if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

print("Configuring UART...")

cRX = c_int(0)
fParity = c_int(0)

# configure the I2C/TWI, default settings
dwf.FDwfDigitalUartRateSet(hdwf, c_double(9600)) # 9.6kHz
dwf.FDwfDigitalUartTxSet(hdwf, c_int(0)) # TX = DIO-0
dwf.FDwfDigitalUartRxSet(hdwf, c_int(1)) # RX = DIO-1
dwf.FDwfDigitalUartBitsSet(hdwf, c_int(8)) # 8 bits
dwf.FDwfDigitalUartParitySet(hdwf, c_int(0)) # 0 none, 1 odd, 2 even
dwf.FDwfDigitalUartStopSet(hdwf, c_double(1)) # 1 bit stop length

dwf.FDwfDigitalUartTx(hdwf, None, c_int(0))# initialize TX, drive with idle level
dwf.FDwfDigitalUartRx(hdwf, None, c_int(0), byref(cRX), byref(fParity))# initialize RX reception
time.sleep(1)

rgTX = create_string_buffer(b'Hello\r\n')
rgRX = create_string_buffer(101)

print("Sending data...")

try:
    while True:
        time.sleep(0.01)
        dwf.FDwfDigitalUartTx(hdwf, rgTX, c_int(sizeof(rgTX)-1)) # send text, trim zero ending
except KeyboardInterrupt: # wait for ctrl-c
    pass

dwf.FDwfDeviceCloseAll()
