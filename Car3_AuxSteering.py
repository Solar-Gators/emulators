import ctypes
import random
from DAD.DAD import DAD
from Mocks.Steering import AuxSteering
import time
import threading

# Configure DAD board to emmulate the CAN bus
emulator = DAD()
emulator.CAN_init(baudRate=500e3)
# Turn on 5v to power the CAN tranciver
emulator.posSupply_init()
steering = AuxSteering(1, 1, emulator)

auxThread = threading.Timer(1, steering.sendCAN)
auxThread.daemon = True
auxThread.start()

cb = {steering.addr_CAN: steering.receiveCAN, steering.addr_CAN: steering.receiveCAN}
try:
    while True:
        emulator.receiveCAN(cb)
except KeyboardInterrupt:
    print("Quitting...")
