from FactoryMethod.fibonacci import Fibonacci
from FactoryMethod.i_problem_creator import IProblemCreator
from FactoryMethod.i_problem_solver import IProblemSolver


class FibonacciCreator(IProblemCreator):
    def factoryMethod(self) -> IProblemSolver:
        return Fibonacci()