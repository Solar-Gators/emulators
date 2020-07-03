import time
from DAD.DAD import DAD
from Mocks.Orion import Orion

BMS = Orion(0x1234, 0x2)
# MPPT1 = Proton1(0x3456, 0x1)
# MPPT2 = Proton1(0x3457, 0x1)
# IMU = BNO555(0x3)
# GPS = GPS(0x0)
emulator = DAD("UART")

print("Sending data...")

if __name__ == "__main__":
    i = 0
    try:
        while i < 5:
            time.sleep(0.01)
            emulator.sendData(BMS.toPitRFDmsg())
            i = i + 1
            print(i)
    except KeyboardInterrupt: # wait for ctrl-c
        pass