from Protocol import Protocol
import ctypes
import time
BAUDRATE = 9600
TX_PIN = 0
RX_PIN = 1

class UART(Protocol):
    def __init__(self, dwf, hdwf):
        print("Configuring UART...")
        self.dwf = dwf
        self.hdwf = hdwf
        self.cRX = ctypes.c_int(0)
        self.fParity = ctypes.c_int(0)

        dwf.FDwfDigitalUartRateSet(hdwf, ctypes.c_double(9600)) # 9.6kHz
        dwf.FDwfDigitalUartTxSet(hdwf, ctypes.c_int(0)) # TX = DIO-0
        dwf.FDwfDigitalUartRxSet(hdwf, ctypes.c_int(1)) # RX = DIO-1
        dwf.FDwfDigitalUartBitsSet(hdwf, ctypes.c_int(8)) # 8 bits
        dwf.FDwfDigitalUartParitySet(hdwf, ctypes.c_int(0)) # 0 none, 1 odd, 2 even
        dwf.FDwfDigitalUartStopSet(hdwf, ctypes.c_double(1)) # 1 bit stop length

        dwf.FDwfDigitalUartTx(hdwf, None, ctypes.c_int(0))# initialize TX, drive with idle level
        dwf.FDwfDigitalUartRx(hdwf, None, ctypes.c_int(0), ctypes.byref(self.cRX), ctypes.byref(self.fParity))# initialize RX reception
        time.sleep(1)
    def send(self, data, size):
        self.dwf.FDwfDigitalUartTx(self.hdwf, data, size)

    def receive(self):
        rgRX = ctypes.create_string_buffer(101)
        self.dwf.FDwfDigitalUartRx(self.hdwf, rgRX, ctypes.c_int(ctypes.sizeof(rgRX)-1), ctypes.byref(self.cRX), ctypes.byref(self.fParity)) # read up to 1024 chars
        return rgRX
