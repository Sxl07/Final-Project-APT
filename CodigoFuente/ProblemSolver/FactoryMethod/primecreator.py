"""File to generate a prime object"""
from .problem_creator import ProblemCreator# pylint: disable=E0402
from .i_problem_solver import IProblemSolver# pylint: disable=E0402
from .prime import Prime# pylint: disable=E0402

class PrimeCreator(ProblemCreator): # pylint: disable=R0903
    """Class PrimeCreator"""
    def factory_method(self) -> IProblemSolver:
        """method to create Problemsolver prime """
        return Prime()
