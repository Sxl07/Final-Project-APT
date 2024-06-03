from abc import ABC, abstractmethod
from typing import List

class IProblemSolver(ABC):
    @abstractmethod
    def compute_results(self, data: List) -> List:
        """
        Takes a list as input and returns another list as output.

        :param data: List of input data.
        :return: List of computed results.
        """
        pass
