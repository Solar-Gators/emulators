import importlib
import ctypes
import random
from .Message import Message
# Emmulates the main AUX steering board
class AuxSteering(Message):
    def __init__(self, addr_CAN, addr_telem, emulator=None):
        super.__init__(addr_CAN, addr_telem)
        self.cplusOn = 0
        self.cminusOn = 0
        self.hornOn = 0
        self.regenOn = 0
        self.hazardsOn = 0
        self.leftOn = 0
        self.rightOn = 0
        self.headlightsOn = 0
    def toCharArray(self):
        output = []
        output[0] |= self.hazardsOn << 0
        output[0] |= self.headlightsOn << 1
        output[0] |= self.leftOn << 2
        output[0] |= self.rightOn << 3
        output[0] |= self.cplusOn << 4
        output[0] |= self.cminusOn << 5
        output[0] |= self.hornOn << 6
        output[0] |= self.regenOn << 7
        return output
    def print(self):
        print(self.toCharArray())
    def sendCAN(self):
        if self.emulator != None:
            self.emulator.sendCAN(self.toCharArray(), self.addr_CAN, False, False)
        else:
            raise NotImplementedError