import importlib
import ctypes
import random
from .Message import Message

class Orion(Message):
    def __init__(self, addr_CAN, addr_telem, emmulator=None):
        super().__init__(addr_CAN, addr_telem)
        self.lowCell = 2.8
        self.highCell = 3.7
        self.avgCell = 3.5
        self.packSumVoltage = 96.5
        self.emmulator = emmulator
    def print(self):
        for name in self.__dict__.items():
            print(str(round(name[1], 2)))
    def toCharArray(self):
        r = []
        for name in self.__dict__.items():
            if name[0].startswith("addr"):
                continue
            temp = int(name[1]*100)
            r.append(temp & 0xFF)
            r.append((temp >> 8) & 0xFF)
        return r
    def receiveCAN(self, data):
        print("Orion data: {}".format(data))
    
    def sendCAN(self):
        if self.emmulator != None:
            self.emmulator.sendCAN(self.toCharArray(), self.addr_CAN, False, False)
        else:
            raise NotImplementedError

if __name__ == "__main__":
    data = Orion(0xff, 0x02)
    print(data.toPitRFDmsg())