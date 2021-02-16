import os, pty, tty
from serial import Serial
import ctypes
import math
import sys
import time
import threading
import termios
import fcntl

# from .UART import UART
# from .CAN import CAN
from .DummyCANAdapter import DummyCANAdapter

# @name:    toCharArray_c
# @desc:    takes the items in a class and outputs them to an array with sizes no larger
#           than a char in the order that is defined in X_MESSAGE_0::dataPacketToArray
# @param:   none
# @returns: c char array
def c_toCharArray(arr):
    return (ctypes.c_char * len(arr))(*arr)

def c_toByteArray(arr):
    return (ctypes.c_ubyte * len(arr))(*arr)

def listener(port):
    #continuously listen to commands on the master device
    while 1:
        res = b""
        while not res.endswith(b"\r\n"):
            #keep reading one byte at a time until we have a full line
            res += os.read(port, 1)
        print("command: %s" % res)
        # #write back the response
        # if res == b'QPGS\r\n':
        #     os.write(port, b"correct result\r\n")
        # else:
        #     os.write(port, b"I dont understand\r\n")

class DummySerial():
    
    def __init__(self, baudrate=2400):
        """
        This opens the DAD board and dlls needed to interface with it. It then opens the device and stores the HWDF.
        """
        # Available Protocols
        self.__CAN = None
        self.__UART = None
        self.__I2C = None
        self.__SPI = None
        #self.adapter = None
        master,slave = os.openpty() #open the pseudoterminal
        print("minicom -D %s" % os.ttyname( slave ))
        s_name = os.ttyname(slave)   #translate the slave fd to a filename
        m_name = os.ttyname(master)  #translate the slave fd to a filename  
        print ("Slave name is: " , s_name, " | Slave FD is: " , slave)
        print ("Master name is: ", m_name, " | Master FD is: " , master)
        print("To test: minicom -H -w -D %s" % s_name)
        # tty.setraw(master, termios.TCSANOW)
        print("Connect to:", os.ttyname(slave))
        # s_name = os.ttyname(slave) #translate the slave fd to a filename
        print(s_name)
        print(os.ttyname(master))
        ser = Serial(s_name, baudrate, timeout=1)

        iflag  = 0
        oflag  = 1
        cflag  = 2
        lflag  = 3
        ispeed = 4
        ospeed = 5
        cc     = 6
        # get current pty attributes
        termAttr = termios.tcgetattr(master)
        print(termAttr)
        # disable canonical and echo modes       
        termAttr[lflag] &= ~termios.ICANON & ~termios.ECHO
        # disable interrupt, quit, and suspend character processing 
        termAttr[cc][termios.VINTR] = b'\x00' 
        termAttr[cc][termios.VQUIT] = b'\x00'
        termAttr[cc][termios.VSUSP] = b'\x00'
        # set revised pty attributes immeaditely
        termios.tcsetattr(master, termios.TCSANOW, termAttr)
        # tty.setraw(master, termios.VINTR)
        # tty.setraw(master, termios.VQUIT)
        # tty.setraw(master, termios.VSUSP)

        # enable non-blocking mode on the file descriptor
        flags = fcntl.fcntl(master, fcntl.F_GETFL) 
        flags |= os.O_NONBLOCK               
        fcntl.fcntl(master, fcntl.F_SETFL, flags)

        self.adapter = DummyCANAdapter(ser, master, baudrate, False)
        print("\nEHEHGEHH\n")

        if sys.platform.startswith("win"):
            print("Good Luck amigo")
            print("(Download Linux or smth)")
            quit()
        elif sys.platform.startswith("darwin"):
            print("Good Luck amigo")
            print("(Download Linux or smth)")
            quit()
          #   self.hdwf = ctypes.c_int()

        # print("Opening first device")
        
        # TODO: Add the ability to open a specific device should there be multiple connected.
        # Open the first device
      #f.dwf.FDwfDeviceConfigOpen(ctypes.c_int(-1), ctypes.c_int(3), ctypes.byref(self.hdwf))

        # Check to see if the device was opened
        if self.adapter.isOpen==False:
            print("failed to open device")
            quit()
            
        # thread = threading.Thread(target=listener, args=[master])
        # thread.start()


    # def CAN_init(self, txPin=0, rxPin=1, polarity=0, baudRate=1e6):
    #     """
    #     This initailizes a CAN interface to the given pins at the polarity and baudrate specified.
    #     """
    #     self.__CAN = CAN(self.dwf, self.hdwf, txPin, rxPin, polarity, baudRate)
    #     return 0

    # def UART_init(self, txPin=0, rxPin=1, length=8, parity=0, stop=1, baudRate=1e6):
    #     """
    #     This initailizes a UART interface to the given pins with the given length, parity, stop length and baudrate specified.
    #     """
    #     self.__UART = UART(self.dwf, self.hdwf, txPin, rxPin, length, parity, stop, baudRate)
    #     return 0

    # def posSupply_init(self, config= None):
    #     """
    #     Initializes the positive power suppy to 5 volts.
    #     """
    #     supplyVoltage = ctypes.c_double()
    #     # set up analog IO channel nodes
    #     # enable positive supply
    #     self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_double(True)) 
    #     # set voltage to 5 V
    #     self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, ctypes.c_int(0), ctypes.c_int(1), ctypes.c_double(5.0))
    #     # master enable
    #     self.dwf.FDwfAnalogIOEnableSet(self.hdwf, ctypes.c_int(True))
    #     self.dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf, ctypes.c_int(2), ctypes.c_int(0), ctypes.byref(supplyVoltage))
    #     # self.setPowerSupply_p(5.0)
    #     IsEnabled = ctypes.c_bool()
    #     self.dwf.FDwfAnalogIOEnableStatus(self.hdwf, ctypes.byref(IsEnabled))
    #     if(IsEnabled):
    #         print("Power supplies on.")
    #     else:
    #         print("Power supplies off.")
    #     print("Supply voltage {}".format(supplyVoltage.value))
        
    def __del__(self):
        """
        Ensures the device is properly closed when the class falls out of scope.
        """
        self.adapter.close()

    # def sendUART(self, data):
    #     """
    #     Sends the given data.
    #     """
    #     self.__UART.send(data)

    # def receiveUART(self, cb):
    #     """
    #     Handle recevied UART data
    #     """
    #     data = self.__UART.receive()
    #     if data.value.decode('utf-8') != "":
    #         print(data.value.decode('utf-8'))
    
    def sendCAN(self, data, ID, isExtended=0, isRemote=0, channel = 0):
        """
        Sends the given data given the parameters.
        """
        if len(data) > 8:
            print("Data too large")
            return -1
        
        rgbTX = c_toByteArray(data)
        self.adapter.send(ID, rgbTX, isExtended)
      #  self.adapter.send(rgbTX, ctypes.c_int(len(rgbTX)), ctypes.c_int(ID), ctypes.c_int(isExtended), ctypes.c_int(isRemote))

    def receiveCAN(self, cb, channel = 0):
        """
        Uses a callback to decode the messages and take appropriet action. If no callback exists for a given address then it prints the message.
        The callback should be a python dictionary with the key being unique CAN adresses and the data being the function to be preformed on the incomming data.
        """
        # call back should be a dictionary of CAN addrs with a parsing function
        # ID, data = self.adapter.receive()
        self.adapter.receive()
        # if ID != -1:
        #     if ID in cb:
        #         cb[ID](data)
        #     else:
        #         CAN.print(ID, data)

    # def setPowerSupply_p(self, val):
    #     if val < 0:
    #         # enable positive supply
    #         self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_double(True)) 
    #         # set voltage to 5 V
    #         self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, ctypes.c_int(0), ctypes.c_int(1), ctypes.c_double(float(5.0)))
        
    #         self.dwf.FDwfAnalogIOEnableSet(self.hdwf, ctypes.c_int(True))
            
    # def setPowerSupply_n(self, val):
    #     if val > 0:
    #         return False
    #     return False

    # def isPowerSupplyOn(self):
    #     IsEnabled = ctypes.c_bool()
    #     self.dwf.FDwfAnalogIOEnableStatus(self.hdwf, ctypes.byref(IsEnabled))
    #     if(IsEnabled):
    #         "Power supplies on."
    #     return IsEnabled

    # # val is a bool
    # def setAnalogIOStatus(self, val):
    #     # self.dwf.FDwfAnalogIOEnableSet(self.hdwf, ctypes.c_int(False)) 
    #     # self.dwf.FDwfAnalogIOEnableSet(self.hdwf, ctypes.c_int(True))
    #     self.dwf.FDwfAnalogIOEnableSet(self.hdwf, ctypes.c_int(val))
    
    # def getSupplyVoltage(self):
    #     supplyVoltage = ctypes.c_double()
    #     time.sleep(0.1)
    #     self.dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf, ctypes.c_int(2), ctypes.c_int(0), ctypes.byref(supplyVoltage))
        
    #     return supplyVoltage.value