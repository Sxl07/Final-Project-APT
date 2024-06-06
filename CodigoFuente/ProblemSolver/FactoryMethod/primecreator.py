from .problem_creator import ProblemCreator
from FactoryMethod.i_problem_solver import IProblemSolver
from FactoryMethod.prime import Prime

class PrimeCreator(ProblemCreator):
    def factoryMethod(self) -> IProblemSolver:
        return Prime()