import ctypes
import random
from DAD.DAD import DAD
from Mocks.Mitsuba import Mitsuba
from Mocks.Proton1 import Proton1
import time

emmulator = DAD("CAN", {"baudRate": 500e3})
mc = Mitsuba(0x3FC, 0x01, emmulator)
mppt = Proton1(0x3FD, 0x2, emmulator)

mppt.sendCAN()

data = emmulator.receiveData()