from .i_random_number import IRandomNumber
import numpy # type: ignore

class RandomNormalDistribution(IRandomNumber):
    def generateNumbers(self, cant, minlimit, maxlimit):
        numbers=numpy.random.uniform(cant,minlimit,maxlimit)
        mean=numpy.mean(numbers)
        deviation=numpy.std(numbers)
        numbers_random = numpy.random.normal(mean,deviation,cant).astype(int)
        return numbers_random.tolist()
