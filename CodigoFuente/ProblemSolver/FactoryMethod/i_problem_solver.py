"""File 'Product' of Factory Method"""
from abc import ABC, abstractmethod
from typing import List

class IProblemSolver(ABC):# pylint: disable=R0903
    """Interface to solve Problems"""
    @abstractmethod
    def compute_results(self, data: List) -> List:
        """Abstract Method to compute the results"""
