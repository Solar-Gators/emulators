import importlib
import ctypes
import random

importlib.import_module("../!Classes/Message")

class OrionData(Message):
    def __init__(self, addr_CAN, addr_telem):
        self.addr_CAN = addr_CAN
        self.addr_telem = addr_telem
        self.lowCell = random.uniform(2.5, 4.3)
        self.highCell = random.uniform(2.5, 4.3)
        self.avgCell = random.uniform(2.5, 4.3)
        self.packSumVoltage = random.uniform(70, 110)
    def print(self):
        for name in self.__dict__.items():
            print(str(round(name[1], 2)))
    def toCharArray(self):
        r = []
        for name in self.__dict__.items():
            if name[0].startswith("addr"):
                continue
            temp = int(name[1]*10000)
            r.append(temp & 0xFF)
            r.append((temp >> 8) & 0xFF)
        return r
    def toRFDmsg(self):
        temp = self.toCharArray()
        return toCharArray_c(temp), len(temp)