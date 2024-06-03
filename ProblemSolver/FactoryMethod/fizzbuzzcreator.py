from .fizzbuzz import FizzBuzz
from .i_problem_creator import IProblemCreator

from .i_problem_solver import IProblemSolver


class FizzbuzzCreator(IProblemCreator):
    def factoryMethod(self) -> IProblemSolver:
        return FizzBuzz()