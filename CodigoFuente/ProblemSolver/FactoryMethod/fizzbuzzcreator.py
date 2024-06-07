"""File to generate a fizzbuzz object"""
from .fizzbuzz import FizzBuzz# pylint: disable=E0402
from .problem_creator import ProblemCreator# pylint: disable=E0402
from .i_problem_solver import IProblemSolver# pylint: disable=E0402

class FizzbuzzCreator(ProblemCreator):# pylint: disable=R0903
    """Class FizzbuzzCreator"""
    def factory_method(self) -> IProblemSolver:
        """method to create Problemsolver fizzbuzz """
        return FizzBuzz()
