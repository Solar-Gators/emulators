import ctypes
import random

class Proton1Data():
    def __init__(self, addr):
        self.vin = random.uniform(2.5, 4.3)
        self.vout = random.uniform(2.5, 4.3)
        self.iin = random.uniform(2.5, 4.3)
        self.temp = random.uniform(30, 40)
        self.addr = addr
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