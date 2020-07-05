from Message import Message

class Axis():
    def __init__(self, x, y ,z):
        self.x = x
        self.y = y
        self.z = z
    def print(self):
        print("x: "+str(self.x)+", y: "+str(self.y)+", z: "+str(self.z))

class BNO555(Message):
    def __init__(self, addr_CAN, addr_telem):
        self.addr_CAN = addr_CAN
        self.addr_telem = addr_telem
        self.data = []
