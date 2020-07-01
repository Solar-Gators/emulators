def

if __name__ == "__main__":
    # initialize the DAD board
    hardware = DAD("CAN")

    mppt1 = Proton1(15)
    mppt2 = Proton1(16)
    bms = Orion(3)
    mitsubaRight(20)
    mitsubaLeft(25)

    while(1):
        mppt1.sendData()
        mppt1.sendData()
        bms.sendData()
        mitsubaRight.sendData()
        mitsubaLeft.sendData()
    
    