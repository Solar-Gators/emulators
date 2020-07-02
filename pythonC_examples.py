from ctypes import *
import random
import Orion
# items must be declared in the order they should be received
# index 0 ... index n


Orion.OrionBMS = Orion.OrionData(0x12)
arr, size = OrionBMS.toCharArray_c()
print(arr)
print(size)