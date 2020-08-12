import ctypes
import random
from DAD.DAD import DAD
from Mocks.Mitsuba import Mitsuba
from Mocks.Proton1 import Proton1
from Mocks.Orion import Orion
import time
import threading

# Configure DAD board to emmulate the CAN bus
emmulator = DAD()
emmulator.CAN_init(baudRate=500e3)
# Turn on 5v to power the CAN tranciver
emmulator.posSupply_init()
mc = Mitsuba(0x08F89540, 0x01, emmulator)
mppt = Proton1(1024, 0x2, emmulator)
bms = Orion(0x6B0, 0x1)

bmsThread = threading.Timer(0.1, bms.sendCAN)
bmsThread.daemon = True
bmsThread.start()

cb = {mc.addr_CAN: mc.receiveCAN, mppt.addr_CAN: mppt.receiveCAN, bms.addr_CAN: bms.receiveCAN}
try:
    while True:
        emmulator.receiveCAN(cb)
except KeyboardInterrupt:
    print("Quitting...")
