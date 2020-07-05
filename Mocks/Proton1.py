
import random
from .Message import Message

class Proton1Data(Message):
    def __init__(self, addr_CAN, addr_telem):
        super().__init__(addr_CAN, addr_telem)
        self.vin = random.uniform(2.5, 4.3)
        self.vout = random.uniform(2.5, 4.3)
        self.iin = random.uniform(2.5, 4.3)
        self.temp = random.uniform(30, 40)
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