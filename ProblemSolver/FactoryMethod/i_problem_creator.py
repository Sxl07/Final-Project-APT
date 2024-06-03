from abc import ABC, abstractmethod

from .i_problem_solver import IProblemSolver


class IProblemCreator(ABC):
    
    @abstractmethod
    def factoryMethod(self) -> IProblemSolver:
        pass

    def problemSolution(self, data):

        problem = self.factoryMethod()

        result = problem.compute_results(data)

        return result