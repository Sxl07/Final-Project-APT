"""Class implements a interface"""
import numpy # type: ignore
from .i_random_number import IRandomNumber# pylint: disable= E0402

class RandomUniformDistribution(IRandomNumber):# pylint: disable= R0903
    """Class to generate a random list with uniform distribution"""
    def generate_numbers(self, cant, minlimit, maxlimit):
        """method to generate the numbers"""
        numbers = numpy.random.uniform(minlimit,maxlimit,cant).astype(int)
        return numbers.tolist()
