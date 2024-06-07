"""File to generate a fibonacci object"""
from .fibonacci import Fibonacci# pylint: disable=E0402
from .problem_creator import ProblemCreator# pylint: disable=E0402
from .i_problem_solver import IProblemSolver# pylint: disable=E0402

class FibonacciCreator(ProblemCreator):# pylint: disable=R0903
    """Class FibonacciCreator"""
    def factory_method(self) -> IProblemSolver:
        """method to create Problemsolver fibonacci """
        return Fibonacci()