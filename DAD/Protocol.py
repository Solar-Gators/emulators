from abc import ABC, abstractmethod 
import ctypes

class Protocol (ABC):
    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def receive(self):
        pass