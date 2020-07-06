from .Message import Message

class Mitsuba(Message):
    def __init__(self, addr_CAN, addr_telem):
        super().__init__(addr_CAN, addr_telem)
        # Frame 0 data
        self.battVoltage = 12       # 10 bit 0.5v LSB
        self.battCurrent = 11       #  9 bit 1A/LSB
        self.battCurrentDir = 10    #  1 bit '0' (+) / '1' (-)
        self.motorCurrent = 10      # 10 bit 1A/LSB 
        self.FETtemp = 9            #  5 bit 5C/LSB
        self.motorRspeed = 8        # 12 bit 1rpm/LSB
        self.duty = 10              # 10 bit 0.5%/LSB
        self.advancedLeadAngle = 13 #  7 bit 0.5Deg_e/LSB
        # Frame 1 data
        self.mode = 1               #  1 bit '0' (eco) / '1' (power)
        self.control = 1            #  1 bit Current Control Mode PWM Mode
        self.accelPos = 10          # 10 bit 0.5%/LSB
        self.regenPos = 10          # 10 bit 0.5%/LSB
        self.DigiSWNum = 4          #  4 bit Digi SW Number
        self.targetVal = 10         # 10 bit CCM 0.5A LSB / PWM 0.5% LSB
        self.motorStat = 2          #  2 bit Wait/Forward/Reverse
        self.drive = 1              #  1 bit '0' (Drive) / '1' (Regen)
        # Frame 2 data
        self.ADSensorErr = 21       # 16 bit
        self.PowSysErr = 8          #  8 bit
        self.MotorSysErr = 3        #  8 bit
        self.FETOHLvl = 2           #  2 bit
    def createFrame0(self):
        r = (self.advancedLeadAngle << 56) | (self.duty << 46) | (self.motorRspeed << 34) | \
            (self.FETtemp << 29) | (self.motorCurrent << 19) | (self.battCurrentDir << 18) | \
            (self.battCurrent << 9) | self.battVoltage
        return r
    def createFrame1(self):
        pass
    def createFrame2(self):
        pass