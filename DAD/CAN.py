from .Protocol import Protocol
import ctypes
import time

class CAN(Protocol):
    def __init__(self, dwf, hdwf, tx=0, rx=1, polarity=0, baudRate=1e6):
        """
        This is the constructor for the CAN protocol
        it configures the tx and rx pins and sets the polatiry and baudRate.
        """
        # set the properties
        self.baudRate = baudRate
        self.tx = tx
        self.rx = rx
        self.polarity = polarity
        
        print("Configuring CAN...")
        print("BaudRate: {}\nCan High {}\nCan Low  {}\npolarity {}"\
            .format(self.baudRate, self.tx, self.rx, self.polarity))
        self.dwf = dwf
        self.hdwf = hdwf
        self.cRX = ctypes.c_int(0)
        self.fParity = ctypes.c_int(0)

        dwf.FDwfDigitalCanRateSet(hdwf, ctypes.c_double(self.baudRate))
        dwf.FDwfDigitalCanPolaritySet(hdwf, ctypes.c_int(self.polarity))
        dwf.FDwfDigitalCanTxSet(hdwf, ctypes.c_int(self.tx))
        dwf.FDwfDigitalCanRxSet(hdwf, ctypes.c_int(self.rx))

        #                    HDWF  ID                Extended         Remote           DLC             *rgTX
        dwf.FDwfDigitalCanTx(hdwf, ctypes.c_int(-1), ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), None) # initialize TX, drive with idle level
        #                    HDWF *ID   *Exte *Remo *DLC  *rgRX  cRX      *Status 0 = no data, 1 = data received, 2 = bit stuffing error, 3 = CRC error
        dwf.FDwfDigitalCanRx(hdwf, None, None, None, None, None, ctypes.c_int(0), None) # initialize RX reception

        time.sleep(0.1)
    def send(self, data, size, ID, isExtended, isRemote):
        """
        This sends the given data on the TX line.
        """
        #                         HDWF       ID  fExtended   fRemote   cDLC *rgTX
        self.dwf.FDwfDigitalCanTx(self.hdwf, ID, isExtended, isRemote, size, data)
    def receive(self):
        """
        This returns any data that the DAD has in the CAN FIFO in a tuple ID, data.
        If there is an error it displays the error and returns -1, -1.
        """
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

            if self._checkError(vStatus.value):
                return

            data = []
            # convert the data into a python list
            for c in rgbRX[0:cDLC.value]:
                data.append(c)
            return vID.value, data
        return -1, -1
    @staticmethod
    def print(ID, data):
        """
        This prints a CAN message given the ID and the data in a list.
        """
        print("Address: "+('0x{:08x}'.format(ID)))
        print("Data: "+(" ".join("0x{:02x}".format(c) for c in data)))
    @staticmethod
    def _checkError(status):
        """
        This checks to see if there was an error when receiving a new CAN message.
        """
        if status == 1:
            # print("no error")
            return False
        elif status == 2:
            print("bit stuffing error")
            return True
        elif status == 3:
            print("CRC error")
            return True
        else:
            print("error")
            return True
        return False