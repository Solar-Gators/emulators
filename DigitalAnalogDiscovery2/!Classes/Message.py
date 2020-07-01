from abc import ABC, abstractmethod 
  
class Message(ABC):
    @abstractmethod
    def send_message(self):
        pass
