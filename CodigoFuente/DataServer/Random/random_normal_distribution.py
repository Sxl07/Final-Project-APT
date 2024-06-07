"""Class implements a interface"""
import numpy # type: ignore
from .i_random_number import IRandomNumber # pylint: disable= E0402

class RandomNormalDistribution(IRandomNumber): # pylint: disable= R0903
    """Class to generate a random list with normal distribution"""
    def generate_numbers(self, cant, minlimit, maxlimit):
        """Method to generate numbers"""
        numbers=numpy.random.uniform(minlimit,maxlimit,cant).astype(int)
        mean=numpy.mean(numbers)
        deviation=numpy.std(numbers)
        numbers_random = numpy.random.normal(mean,deviation,cant).astype(int)
        return numbers_random.tolist()
