import random
from .Message import Message

class Proton1(Message):
    def __init__(self, addr_CAN, addr_telem, emulator=None):
        super().__init__(addr_CAN, addr_telem, emulator)
        self.vin = 37.4
        self.vout = 85.2
        self.iin = 2.3
        self.temperature = 37.12
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
    def toFrame0(self):
        data = []
        # handle vin
        temp = int(self.vin * 100)
        data.append(int(temp) & 0xFF)
        temp = temp / 0x100
        data.append(int(temp) & 0xFF)
        # handle vout
        temp = int(self.vout * 100)
        data.append(int(temp) & 0xFF)
        temp = temp / 0x100
        data.append(int(temp) & 0xFF)
        # handle iin
        temp = int(self.iin * 100)
        data.append(int(temp) & 0xFF)
        temp = temp / 0x100
        data.append(int(temp) & 0xFF)
        # handle temp
        temp = int(self.temperature * 100)
        data.append(int(temp) & 0xFF)
        temp = temp / 0x100
        data.append(int(temp) & 0xFF)
        return data
    def sendCAN(self):
        if self.emulator != None:
            self.emulator.sendCAN(self.toFrame0(),self.addr_CAN)
        else:
            raise NotImplementedError
    def receiveCAN(self, data):
        self.sendCAN()

if __name__ == "__main__":
    mppt = Proton1(0x034, 0x01)
    data = mppt.toFrame0()
    print(data)
