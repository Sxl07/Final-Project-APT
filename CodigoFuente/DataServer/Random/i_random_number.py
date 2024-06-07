"""Interface to generate distribution"""
from abc import ABC, abstractmethod

class IRandomNumber(ABC): # pylint: disable=R0903
    """Interface with abstract method"""
    @abstractmethod
    def generate_numbers(self,cant,mini,maxi):
        """Method to generate numbers with parameters"""
