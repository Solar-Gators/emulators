from abc import ABC, abstractmethod 
import ctypes

# toCharArray_c
# @desc:    takes the items in a class and outputs them to an array with sizes no larger
#           than a char in the order that is defined in X_MESSAGE_0::dataPacketToArray
# @param:   none
# @returns: a tuple where the first element is the c array and the second is the size
@staticmethod
def toCharArray_c(arr):
    return (ctypes.c_char * len(arr))(*arr), len(arr)

class Message(ABC):
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
    # @param:   none
    # @returns: an array to be received by the pit
    @abstractmethod
    def toPitRFDmsg(self):
        pass
