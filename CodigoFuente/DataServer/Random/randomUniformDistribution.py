from .i_random_number import IRandomNumber
import numpy # type: ignore

class RandomUniformDistribution(IRandomNumber):
    def generateNumbers(self, cant, minlimit, maxlimit):
        numbers = numpy.random.uniform(minlimit,maxlimit,cant).astype(int)
        return numbers.tolist()