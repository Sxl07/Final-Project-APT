from .fizzbuzz import FizzBuzz
from .problem_creator import ProblemCreator
from .i_problem_solver import IProblemSolver

class FizzbuzzCreator(ProblemCreator):
    def factoryMethod(self) -> IProblemSolver:
        return FizzBuzz()