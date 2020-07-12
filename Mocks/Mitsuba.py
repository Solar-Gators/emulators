from .Message import Message
# address for rtr to motor
RL1 = 0x8F89540
RR1 = 0x8F91540
FL1 = 0x8F99540
FR1 = 0x8FA1540
# address for each motor's frame 0 message
RL1_FRAME_0 = 0x8850225
RR1_FRAME_0 = 0x8850245
FL1_FRAME_0 = 0x8850265
FR1_FRAME_0 = 0x8850285
# address for each motor's frame 1 message
RL1_FRAME_1 = 0x8950225
RR1_FRAME_1 = 0x8950245
FL1_FRAME_1 = 0x8950265
FR1_FRAME_1 = 0x8950285
# address for each motor's frame 2 message
RL1_FRAME_2 = 0x8A50225
RR1_FRAME_2 = 0x8A50245
FL1_FRAME_2 = 0x8A50265
FR1_FRAME_2 = 0x8A50285

class Mitsuba(Message):
    def __init__(self, addr_CAN, addr_telem):
        super().__init__(addr_CAN, addr_telem)
        # Frame 0 data
        self.battVoltage = 1023       # 10 bit 0.5v LSB                        0 -> 1023
        self.battCurrent = 0       #  9 bit 1A/LSB                          0 ->  511
        self.battCurrentDir = 10    #  1 bit '0' (+) / '1' (-)               0 ->    1
        self.motorCurrent = 10      # 10 bit 1A/LSB                          0 -> 1023
        self.FETtemp = 9            #  5 bit 5C/LSB                          0 ->   31
        self.motorRspeed = 8        # 12 bit 1rpm/LSB                        0 -> 4095
        self.duty = 1023              # 10 bit 0.5%/LSB                        0 -> 1023
        self.advancedLeadAngle = 0 #  7 bit 0.5Deg_e/LSB                    0 ->  127
        # Frame 1 data
        self.mode = 1               #  1 bit '0' (eco) / '1' (power)         0 ->    1
        self.control = 1            #  1 bit Current Control Mode PWM Mode   0 ->    1
        self.accelPos = 10          # 10 bit 0.5%/LSB                        0 -> 1023
        self.regenPos = 10          # 10 bit 0.5%/LSB                        0 -> 1023
        self.DigiSWNum = 4          #  4 bit Digi SW Number                  0 ->   15
        self.targetVal = 10         # 10 bit CCM 0.5A LSB / PWM 0.5% LSB     0 -> 1023
        self.motorStat = 2          #  2 bit Wait/Forward/Reverse            0 ->    3
        self.drive = 1              #  1 bit '0' (Drive) / '1' (Regen)       0 ->    1
        # Frame 2 data
        self.ADSensorErr = 65535       # 16 bit                                 0 -> 65535
        self.PowSysErr = 255          #  8 bit                                 0 ->   255
        self.MotorSysErr = 255        #  8 bit                                 0 ->   255
        self.FETOHLvl = 3           #  2 bit                                 0 ->     3
    def createFrame0(self):
        r = ((self.advancedLeadAngle << 57) | (self.duty << 47) | (self.motorRspeed << 35) | \
            (self.FETtemp << 30) | (self.motorCurrent << 20) | (self.battCurrentDir << 19) | \
            (self.battCurrent << 10) | self.battVoltage)
        return r.to_bytes(8, 'little')
    def createFrame1(self):
        r = (self.drive << 38) | (self.motorStat << 36) | (self.targetVal << 26) | \
            (self.DigiSWNum << 22) | (self.regenPos << 12) | (self.accelPos << 2) | \
            (self.control << 1) | self.mode
        return r.to_bytes(8, 'little')
    def createFrame2(self):
        r = (self.FETOHLvl << 32) | (self.MotorSysErr << 24) | (self.PowSysErr << 16) | (self.ADSensorErr)
        return r.to_bytes(8, 'little')
    def handleRTR(self, addr, msg):
        pass
    def print(self):
        for name in self.__dict__.items():
            print(str(round(name[1], 2)))
    def toCharArray(self):
        pass