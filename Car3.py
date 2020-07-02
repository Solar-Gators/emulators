def

if __name__ == "__main__":
    # initialize the DAD board
    hardware = DAD("CAN")

    mppt1 = Proton1(15)
    mppt2 = Proton1(16)
    bms = Orion(3)
    mitsubaRight(20)
    mitsubaLeft(25)

    # wait for data to be put on the CAN line
    while(1):
        time.sleep(0.01)
        #                    HDWF *ID          *Extended        *Remote         *DLC         *rgRX   cRX                  *Status
        dwf.FDwfDigitalCanRx(hdwf, byref(vID), byref(fExtended), byref(fRemote), byref(cDLC), rgbRX, c_int(sizeof(rgbRX)), byref(vStatus)) 
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
    
    