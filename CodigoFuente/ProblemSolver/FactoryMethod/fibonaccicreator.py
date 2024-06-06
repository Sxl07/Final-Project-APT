from FactoryMethod.fibonacci import Fibonacci
from .problem_creator import ProblemCreator
from FactoryMethod.i_problem_solver import IProblemSolver

class FibonacciCreator(ProblemCreator):
    def factoryMethod(self) -> IProblemSolver:
        return Fibonacci()