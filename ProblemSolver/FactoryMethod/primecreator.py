from FactoryMethod.i_problem_creator import IProblemCreator
from FactoryMethod.i_problem_solver import IProblemSolver
from FactoryMethod.prime import Prime

class PrimeCreator(IProblemCreator):
    def factoryMethod(self) -> IProblemSolver:
        return Prime()