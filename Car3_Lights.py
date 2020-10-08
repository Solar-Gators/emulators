import ctypes
import random
from DAD.DAD import DAD
from Mocks.Lights import Lights
import time
import threading

# Configure DAD board to emmulate the CAN bus
emulator = DAD()
emulator.CAN_init(baudRate=500e3)
# Turn on 5v to power the CAN tranciver
emulator.posSupply_init()
lights = Lights(1, 1, emulator)

auxThread = threading.Timer(1, lights.sendCAN)
auxThread.daemon = True
auxThread.start()

cb = {lights.addr_CAN: lights.receiveCAN, lights.addr_CAN: lights.receiveCAN}
try:
    while True:
        emulator.receiveCAN(cb)
except KeyboardInterrupt:
    print("Quitting...")
