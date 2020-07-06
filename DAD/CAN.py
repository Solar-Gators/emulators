from .Protocol import Protocol
import ctypes
import time
# defaults
DEFAULT_TX_PIN = 0      # DIO-0
DEFAULT_RX_PIN = 1      # DIO-1
DEFAULT_POLARITY = 0    # normal
DEFUALT_RATE = 1e6      # 1 MHz

class CAN(Protocol):
    def __init__(self, dwf, hdwf, config):
        # set the properties
        self.rate = config.get('baudRate') if 'baudRate' in config else DEFUALT_RATE
        self.tx = config.get('tx') if 'tx' in config else DEFAULT_TX_PIN
        self.rx = config.get('rx') if 'rx' in config else DEFAULT_RX_PIN
        self.polarity = config.get('polarity') if 'polarity' in config else DEFAULT_POLARITY

        print("Configuring CAN...")
        self.dwf = dwf
        self.hdwf = hdwf
        self.cRX = ctypes.c_int(0)
        self.fParity = ctypes.c_int(0)

        dwf.FDwfDigitalCanRateSet(hdwf, ctypes.c_double(self.rate))
        dwf.FDwfDigitalCanPolaritySet(hdwf, ctypes.c_int(self.polarity))
        dwf.FDwfDigitalCanTxSet(hdwf, ctypes.c_int(self.tx))
        dwf.FDwfDigitalCanRxSet(hdwf, ctypes.c_int(self.rx))

        #                    HDWF  ID                Extended         Remote           DLC             *rgTX
        dwf.FDwfDigitalCanTx(hdwf, ctypes.c_int(-1), ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), None) # initialize TX, drive with idle level
        #                    HDWF *ID   *Exte *Remo *DLC  *rgRX  cRX      *Status 0 = no data, 1 = data received, 2 = bit stuffing error, 3 = CRC error
        dwf.FDwfDigitalCanRx(hdwf, None, None, None, None, None, ctypes.c_int(0), None) # initialize RX reception

        time.sleep(1)
    def handleReceive(self):
        pass
    def send(self, data, size, ID, isExtended=0, isRemote=0):
        #                         HDWF       ID                fExtended                 fRemote                 cDLC  *rgTX
        self.dwf.FDwfDigitalCanTx(self.hdwf, ctypes.c_int(ID), ctypes.c_int(isExtended), ctypes.c_int(isRemote), size, data)
    def receive(self): #TODO
        vStatus  = ctypes.c_int()
        vID  = ctypes.c_int()
        fExtended  = ctypes.c_int()
        fRemote  = ctypes.c_int()
        cDLC = ctypes.c_int()
        rgbRX = (ctypes.c_ubyte*8)()
        #                         HDWF       *ID                *Extended                *Remote                *DLC                *rgRX  cRX                                 *Status
        self.dwf.FDwfDigitalCanRx(self.hdwf, ctypes.byref(vID), ctypes.byref(fExtended), ctypes.byref(fRemote), ctypes.byref(cDLC), rgbRX, ctypes.c_int(ctypes.sizeof(rgbRX)), ctypes.byref(vStatus)) 
        if vStatus.value != 0:
            print("RX: "+('0x{:08x}'.format(vID.value)) +" "+("Extended " if fExtended.value!=0 else "")+("Remote " if fRemote.value!=0 else "")+"DLC: "+str(cDLC.value))
            if vStatus.value == 1:
                print("no error")
            elif vStatus.value == 2:
                print("bit stuffing error")
            elif vStatus.value == 3:
                print("CRC error")
            else:
                print("error")
            if fRemote.value == 0 and cDLC.value != 0:
                print("Data: "+(" ".join("0x{:02x}".format(c) for c in rgbRX[0:cDLC.value])))
            return rgbRX
