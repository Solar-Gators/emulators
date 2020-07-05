from abc import ABC, abstractmethod 
import ctypes
# Constatns
STARTBYTE = 0xFF
ENDBYTE = 0x3F
ESCCHAR = 0x2F
class Message(ABC):
    def __init__(self, addr_CAN, addr_telem):
        self.addr_CAN = addr_CAN
        self.addr_telem = addr_telem
        
    @abstractmethod
    def print(self):
        pass
    # @name:    toCharArray
    # @desc:    takes the items in a class and outputs them to an array with sizes no larger
    #           than a char in the order that is defined in X_MESSAGE_0::dataPacketToArray
    # @param:   none
    # @returns: an array of chars
    @abstractmethod
    def toCharArray(self):
        pass

    # @name:    toPitRFDmsg
    # @desc:    turns the data into a message as expected by the pit data collector
    #           inserts start and end byte
    # @param:   none
    # @returns: an array to be received by the pit
    def toPitRFDmsg(self):
        temp = self.toCharArray()
        temp = self.handleSpecialChars(temp)
        temp.insert(0, STARTBYTE)
        temp.insert(1, 1)
        temp.insert(2, self.addr_telem)
        temp.insert(3, len(temp)-3)
        temp.append(ENDBYTE)
        return temp

    def handleSpecialChars(self, arr):
        indices = [i for i, x in enumerate(arr) if x == STARTBYTE or x == ENDBYTE or x==ESCCHAR]
        i = 0
        for index in indices:
            arr.insert(index+i, ESCCHAR)
            i = i + 1
        return arr
