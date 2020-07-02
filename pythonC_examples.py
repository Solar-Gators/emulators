from ctypes import *
import random
from Mocks import Orion
# items must be declared in the order they should be received
# index 0 ... index n


OrionBMS = Orion.OrionData(0x12, 0x01)
arr, size = OrionBMS.toCharArray_c()
print(arr)
print(size)