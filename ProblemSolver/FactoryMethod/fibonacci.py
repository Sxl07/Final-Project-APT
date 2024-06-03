from typing import List
from FactoryMethod.i_problem_solver import IProblemSolver

class Fibonacci(IProblemSolver):
  def compute_results(self, data: List[str]) -> List[str]:
    result = []
    line = ""
    for element in data:
      line = self.__fibonacciVerifier(int(element))
      result.append(element + " " + str(line))
    return result

  def __fibonacciVerifier(self, n):
    a, b = 0, 1
    while b < n:
      a, b = b, a + b
    return b == n
