from .i_problem_solver import IProblemSolver

class ProblemCreator():   
    def factoryMethod(self) -> IProblemSolver:
        pass

    def problemSolution(self, data):
        problem = self.factoryMethod()
        result = problem.compute_results(data)
        return result