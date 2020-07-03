import time
from DAD.DAD import DAD
from .Mocks import BNO555, Orion, Mitsuba, Proton1, GPS

BMS = Orion(0x1234, 0x2)
# MPPT1 = Proton1(0x3456, 0x1)
# MPPT2 = Proton1(0x3457, 0x1)
# IMU = BNO555(0x3)
# GPS = GPS(0x0)
emulator = DAD("UART")

print("Sending data...")

try:
    while True:
        time.sleep(0.01)
        emulator.sendData(BMS.toPitRFDmsg())
except KeyboardInterrupt: # wait for ctrl-c
    pass