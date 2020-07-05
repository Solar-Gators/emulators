import time
from DAD.DAD import DAD
from Mocks.Orion import Orion
from Mocks.GPS import GPS
GPS_DATA = "Mocks/Support/GPS_7-4-2020.csv"
BMS = Orion(0x1234, 0x2)
# MPPT1 = Proton1(0x3456, 0x1)
# MPPT2 = Proton1(0x3457, 0x1)
# IMU = BNO555(0x3)
GPS = GPS(0x1235, 0x0, GPS_DATA)
emulator = DAD("UART")

print("Sending data...")

if __name__ == "__main__":
    i = 0
    try:
        while True:
            time.sleep(0.5)
            data = BMS.toPitRFDmsg()
            print(data)
            data = GPS.toPitRFDmsg()
            print(data)
            emulator.sendData(BMS.toPitRFDmsg())
            emulator.sendData(GPS.toPitRFDmsg())
            i = i + 1
            print(i)
    except KeyboardInterrupt: # wait for ctrl-c
        pass