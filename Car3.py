import ctypes
import random
from DAD.DAD import DAD
from Mocks.Mitsuba import Mitsuba
from Mocks.Proton1 import Proton1
from Mocks.Orion import Orion
import time
import threading

# Configure DAD board to emmulate the CAN bus
emulator = DAD()
emulator.CAN_init(baudRate=500e3)
# Turn on 5v to power the CAN tranciver
emulator.posSupply_init()
mc = Mitsuba(0x08F89540, 0x01, emulator)
mppt = Proton1(1024, 0x2, emulator)
bms = Orion(0x6B0, 0x1, emulator)

bmsThread = threading.Timer(0.1, bms.sendCAN)
bmsThread.daemon = True
bmsThread.start()

cb = {mc.addr_CAN: mc.receiveCAN, mppt.addr_CAN: mppt.receiveCAN}
try:
    while True:
        emulator.receiveCAN(cb)
except KeyboardInterrupt:
    print("Quitting...")
