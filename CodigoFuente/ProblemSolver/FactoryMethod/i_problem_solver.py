from abc import ABC, abstractmethod
from typing import List

class IProblemSolver(ABC):
    @abstractmethod
    def compute_results(self, data: List) -> List:
        pass
