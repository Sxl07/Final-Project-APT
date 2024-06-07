"""Father Class is the 'Product creator'"""
from .i_problem_solver import IProblemSolver # pylint: disable=E0402

class ProblemCreator():
    """Class to create the ProblemsCreators"""
    def factory_method(self) -> IProblemSolver:
        """method to create the Problem"""

    def problem_solution(self, data):
        """Method to solve the problem"""
        problem = self.factory_method() # pylint: disable=E1111
        result = problem.compute_results(data)
        return result
