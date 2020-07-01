from ctypes import *
import random
class OrionData(Structure):
    def __init__(self):
        self.lowCell = random.randint(2, 4)
        self.highCell = random.randint(2, 4)
        self.avgCell = random.randint(2, 4)
        self.packSumVoltage = random.randint(70, 110)
    def toCharArray(self):
        a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))

OrionBMS = OrionData()
OrionBMS.toCharArray()