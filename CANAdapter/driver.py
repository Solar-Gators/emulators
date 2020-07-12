import serial
import time
class CANAdapter():
    def __init__(self, baudRate, timeStamp = False):
        self.timeStamp = timeStamp
        self.baudRate = baudRate
        if baudRate == 10e3:
            self.baudChar = '0'
        elif baudRate == 20e3:
            self.baudChar = '1'
        elif baudRate == 50e3:
            self.baudChar = '2'
        elif baudRate == 100e3:
            self.baudChar = '3'
        elif baudRate == 125e3:
            self.baudChar = '4'
        elif baudRate == 250e3:
            self.baudChar = '5'
        elif baudRate == 500e3:
            self.baudChar = '6'
        elif baudRate == 800e3:
            self.baudChar = '7'
        elif baudRate == 1e6:
            print("Warning: 1Mbit does not seem to work")
            self.baudChar = '8'
        else:
            raise ValueError
        self.setTimeStamp()
        self.setBaudRate()
        self.openCANChannel()
    def setTimeStamp(self):
        ser.write(b'A0\r')
        x = ser.read(2)
        # if x != "b'\\x06'":
        #     print("Failed to configure timestamp: {}".format(x))
        #     raise ValueError
    def setBaudRate(self):
        ser.write(b'S6\r')
        x = ser.read(2)
        # if x != b'\\x06':
        #     print("Failed to configure baudrate")
        #     raise ValueError
    def openCANChannel(self):
        ser.write(b'O\r')
        x = ser.read(2)
        # if x != b'\\x06':
        #     print("Failed to open CAN channel")
        #     raise ValueError

    def sendExtendedFrame(self, addr, data):
        pass
    def sendFrame(self, addr, data):
        pass


ser = serial.Serial(port = 'COM6', timeout=1)
if ser.is_open:
    ser.close()
ser.open()

test = CANAdapter(500e3, False)

try:
    while True:
        x = 0
        x = ser.read(100)
        print(str(x))
        time.sleep(2)
except KeyboardInterrupt: # wait for ctrl-c
    pass

ser.close()