import serial
import time
class CANAdapter():
    def __init__(self, port, baudRate, timeStamp = False):
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
            print("Invalid baud rate")
            quit()
        print("Configuring CANAdapter...")
        if not ser.is_open:
            ser.open()
        self.setTimeStamp()
        self.setBaudRate()
        self.openCANChannel()
    def setTimeStamp(self):
        ser.write(b'A0\r')
        x = str(ser.read(1))
        x = int(x[4:-1])
        if x != 6:
            print("Failed to configure timestamp")
            quit()
    def setBaudRate(self):
        ser.write(b'S6\r')
        x = str(ser.read(1))
        x = int(x[4:-1])
        if x != 6:
            print("Failed to configure baudrate")
            quit()
    def openCANChannel(self):
        ser.write(b'O\r')
        x = str(ser.read(1))
        x = int(x[4:-1])
        if x != 6:
            print("Failed to open CAN channel")
            quit()

    def close(self):
        ser.write(b'C\r')
        if ser.is_open:
            ser.close()

    def sendExtendedFrame(self, addr, data):
        pass
    def sendFrame(self, addr, data):
        pass
    def parseStandardMsg(self, msg):
        print("Message: " + msg)
        addr = int(msg[1:4], 16)
        length = int(msg[4], 16)
        data = int(msg[5:], 16).to_bytes(length, "big")
        print("Address: {}".format(hex(addr)))
        print("Length: {}".format(hex(length)))
        print("Data: {}".format(data.hex()))
    def parseExtendedMsg(self, msg):
        print("Message: " + msg)
        addr = int(msg[1:9], 16)
        length = int(msg[9], 16)
        data = int(msg[10:], 16).to_bytes(length, "big")
        print("Address: {}".format(hex(addr)))
        print("Length: {}".format(hex(length)))
        print("Data: {}".format(data.hex()))
    def readFIFO(self):
        x = 0
        x = str(ser.read(100))
        x = x[2:-1]
        msgs = x.split("\\r")
        if not msgs[0]:
            return
        for msg in msgs:
            if not msg:
                continue
            if msg[0] == 't':
                self.parseStandardMsg(msg)
            elif msg[0] == 'x':
                self.parseExtendedMsg(msg)
            else:
                print("Unknown message: " + msg)

ser = serial.Serial(port = 'COM6', timeout=1)

test = CANAdapter(ser, 500e3, False)

try:
    while True:
        test.readFIFO()
        time.sleep(2)
except KeyboardInterrupt: # wait for ctrl-c
    test.close()
