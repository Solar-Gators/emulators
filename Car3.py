import ctypes
import random
from DAD.DAD import DAD
from DummySerial.DummySerial import DummySerial
from Mocks.Mitsuba import Mitsuba
from Mocks.Proton1 import Proton1
from Mocks.Orion import Orion
from Mocks.Steering import AuxSteering
import time
import threading

# Configure DAD board to emmulate the CAN bus
emulator = DummySerial()
# emulator.CAN_init(baudRate=500e3)
# Turn on 5v to power the CAN tranciver
# emulator.posSupply_init()
mc = Mitsuba(0x08F89540, 0x01, emulator)
mppt = Proton1(1, 2, emulator)
bms = Orion(2, 1, emulator)
steering = AuxSteering(4, 1, emulator)

cb = {mc.addr_CAN: mc.receiveCAN, mppt.addr_CAN: mppt.receiveCAN}
try:
    while True:
        time.sleep(1)

        # mcThread = threading.Timer(1, mc.sendCANout)
        # mcThread.daemon = True
        # mcThread.start()

        mpptThread = threading.Timer(1, mppt.sendCAN)
        mpptThread.daemon = True
        mpptThread.start()

        auxThread = threading.Timer(1, steering.sendCAN)
        auxThread.daemon = True
        auxThread.start()

        bmsThread = threading.Timer(0.1, bms.sendCAN)
        bmsThread.daemon = True
        bmsThread.start()

        # emulator.receiveCAN(cb)
except KeyboardInterrupt:
    emulator.__del__
    print("Quitting...")
