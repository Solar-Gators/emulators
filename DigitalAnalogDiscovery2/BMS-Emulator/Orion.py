import ctypes
import random

class OrionData():
    def __init__(self, addr):
        self.addr = addr
        self.lowCell = random.uniform(2.5, 4.3)
        self.highCell = random.uniform(2.5, 4.3)
        self.avgCell = random.uniform(2.5, 4.3)
        self.packSumVoltage = random.uniform(70, 110)
    def print(self):
        for name in self.__dict__.items():
            print(str(round(name[1], 2)))
    def toCharArray(self):
        r = []
        r.append(self.addr)
        i = 0
        for name in self.__dict__.items():
            if name[0] == "addr":
                continue
            temp = int(name[1]*10000)
            r.append(temp & 0xFF)
            r.append((temp >> 8) & 0xFF)
            i = i+1
        r.insert(1, i*2)
        return r
    def toCharArray_c(self):
        tmp = self.toCharArray()
        return (ctypes.c_char * len(tmp))(*tmp), len(tmp)