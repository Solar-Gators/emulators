from .Message import Message

class Axis():
    def __init__(self, x, y ,z):
        self.x = x
        self.y = y
        self.z = z
    def print(self):
        print("x: "+str(self.x)+", y: "+str(self.y)+", z: "+str(self.z))

class BNO555(Message):
    def __init__(self, addr_CAN, addr_telem):
        super.__init__(addr_CAN, addr_telem)
        self.gyro = Axis(5, 4, 3)
        self.accel = Axis(1, 2, 3)
    def toCharArray(self):
        # TODO figure out how the IMU is sending from the car 
        pass
