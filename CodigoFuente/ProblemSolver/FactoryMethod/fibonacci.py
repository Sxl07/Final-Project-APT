"""File to solve fibonacci"""
from typing import List
from .i_problem_solver import IProblemSolver# pylint: disable=E0402

class Fibonacci(IProblemSolver):# pylint: disable=R0903
    """Class Fibonacci with the solution"""
    def compute_results(self, data: List[str]) -> List[str]:
        """Method to compute the results"""
        result = []
        line = ""
        for element in data:
            line = self.__fibonacci_verifier(int(element))
            result.append(element + " " + str(line))
        return result

    def __fibonacci_verifier(self, n):
        a, b = 0, 1
        while b < n:
            a, b = b, a + b
        return b == n
