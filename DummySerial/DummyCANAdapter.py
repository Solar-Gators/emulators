import serial
import time
import threading
import os
from decimal import Decimal

# WIP
# VALUES ARE HARDCODED
def listToString(s):
    r = ""
    for ele in s:
        r += "{0:02x}".format(ele)
    return r
class DummyCANAdapter():
    def __init__(self, port, master, baudRate=2400, timeStamp = False):
        self.timeStamp = timeStamp
        self.baudRate = baudRate
        self.port = port
        self.master=master

        # if baudRate == 10e3:
        #     self.baudChar = '0'
        # elif baudRate == 20e3:
        #     self.baudChar = '1'
        # elif baudRate == 50e3:
        #     self.baudChar = '2'
        # elif baudRate == 100e3:
        #     self.baudChar = '3'
        # elif baudRate == 125e3:
        #     self.baudChar = '4'
        # elif baudRate == 250e3:
        #     self.baudChar = '5'
        # elif baudRate == 500e3:
        #     self.baudChar = '6'
        # elif baudRate == 800e3:
        #     self.baudChar = '7'
        # elif baudRate == 1e6:
        #     print("Warning: 1Mbit does not seem to work")
        #     self.baudChar = '8'
        # else:
        #     print("Invalid baud rate")
        #     quit()
        print("Configuring Dummy CANAdapter...")
        # if not self.port.is_open:
        #     self.port.open()
    #     self.setTimeStamp()
    #     self.setBaudRate()
    #     self.openCANChannel()
    # def setTimeStamp(self):
    #     ser.write(b'A0\r')
    #     x = str(ser.read(1))
    #     x = int(x[4:-1])
    #     if x != 6:
    #         print("Failed to configure timestamp")
    #         quit()
    # def setBaudRate(self):
    #     ser.write(b'S0\r')
    #     x = str(ser.read(1))
    #     x = int(x[4:-1])
    #     if x != 6:
    #         print("Failed to configure baudrate")
    #         quit()
    # def openCANChannel(self):
    #     ser.write(b'O\r')
    #     x = str(ser.read(1))
    #     x = int(x[4:-1])
    #     if x != 6:
    #         print("Failed to open CAN channel")
    #         quit()

    # def isOpen(self):
    #     return self.port.is_open
    def close(self):
        #ser.write(b'C\r')
        # if self.port.is_open:
        #     self.port.close()
        os.close(self.port)
        os.close(self.master)
    def send(self, addr, data, isExtended):
        if(isExtended!=0):
            self.sendExtendedFrame(addr, data)
        else:
            self.sendFrame(addr, data)
        # else:
        #     print("Invalid address")
        #     quit()
    def sendExtendedFrame(self, addr, data):
        temp = str('x{}{}{}\r'.format(str(hex(addr))[2:],len(data),listToString(data)))
        print("Sending: " + temp)
        # self.port.write(temp.encode('utf-8'))
        os.write(self.master, temp.encode('utf-8'))
        # x = str(os.read(self.master, 2))
        # x = int(x[4:-1], 16)
        # if x != 6:
        #     print("Failed to send extended frame")
        #     quit()
    def sendFrame(self, addr, data):
        temp = str('t{}{}{}\r'.format(str(hex(addr))[2:],len(data),listToString(data)))
        #y = b't3CF411223344\r'
        print("Sending: " + str(temp))
        # self.port.write(temp.encode('utf-8'))
        os.write(self.master, temp.encode('utf-8'))
        # x = str(os.read(self.master, 100))
        # print("Sent: "+x)
        # ser.write(b't3CF411223344\r')
        # x = str(ser.read(100))
        # x = int(x[4:-1], 16)
        # print(x)
        # if x != 6:
        #     print("Failed to send frame")
        #     quit()
    def parseStandardMsg(self, msg):
            #     if ID != -1:
            # if ID in cb:
            #     cb[ID](data)

        print("Message: " + msg)
        addr = int(msg[1:4], 16)
        length = int(msg[4], 16)
        print("Address: {}".format(hex(addr)))
        print("Length: {}".format(hex(length)))
        if(length>0):
            try:
                data = int(msg[5:], 16).to_bytes(length, "big")
                print("Data: {}".format(data.hex()))
            except:
                data = str(msg[5:])
                print("Data: {}".format(data))

    def parseExtendedMsg(self, msg):
        # if ID != -1:
        #     if ID in cb:
        #         cb[ID](data)

        print("Message: " + msg)
        addr = int(msg[1:9], 16)
        length = int(msg[9], 16)
        print("Address: {}".format(hex(addr)))
        print("Length: {}".format(hex(length)))
        if(length>0):
            try:
                data = int(msg[10:], 16).to_bytes(length, "big")
                print("Data: {}".format(data.hex()))
            except:
                data = str(msg[10:])
                print("Data: {}".format(data))
    def receive(self):
        # x = 0
        print("aaa "+ str(self.master))
        # x = str(os.read(self.master, 100))
        x = b""
        while not x.endswith(b"\r"):
            #keep reading one byte at a time until we have a full line
            x += os.read(self.master, 1)
            # x += str(self.master.read(100))
        # print(x)
        x=str(x)
        x = x[2:-1]
        msgs = x.split("\\r")
        if not msgs[0]:
            return
        for msg in msgs:
            if not msg:
                continue
            if msg[0] == 't':
                self.parseStandardMsg(msg)
                print("\n")
            elif msg[0] == 'x':
                self.parseExtendedMsg(msg)
                print("\n")
            else:
                print("Unknown message: " + msg)


# master,slave = pty.openpty() #open the pseudoterminal
# s_name = os.ttyname(slave) #translate the slave fd to a filename
# ser = serial.Serial(s_name, baudrate, timeout=1)

# test = CANAdapter(ser, 2400, False)

# try:
#     while True:
#         test.receive()
#         time.sleep(0.01)
#         data = [0x13, 0x24, 0x13, 0x01, 0x13, 0x24, 0x13, 0x01]
#         test.send(0x5FF,data)
#         time.sleep(2)
# except KeyboardInterrupt: # wait for ctrl-c
#     print("Closing...")
# finally:
#     test.close()
