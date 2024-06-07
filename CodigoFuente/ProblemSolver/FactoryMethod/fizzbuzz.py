"""File to solve fizzbuzz"""
from typing import List
from .i_problem_solver import IProblemSolver # pylint: disable=E0402

class FizzBuzz(IProblemSolver): # pylint: disable=R0903
    """Class FizzBuzz with the solution"""
    def compute_results(self, data: List[str]) -> List[str]:
        """Method to compute the results"""
        result = []
        line = ""
        for element in data:
            line = self.__fizzbuzz(int(element))
            result.append(element + " " + str(line))
        return result

    def __fizzbuzz(self, n):
        output = "Fizz" * (int(n) % 3 == 0) + "Buzz" * (int(n) % 5 == 0)
        return output or str(n)
