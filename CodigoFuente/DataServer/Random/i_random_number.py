from abc import ABC, abstractmethod

class IRandomNumber(ABC):
    @abstractmethod
    def generateNumbers(self,cant,min,max):
        pass