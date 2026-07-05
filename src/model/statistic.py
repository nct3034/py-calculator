import math
import statistics
from typing import List

class Statistics:
    def factorial(self, n: int) -> int:
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        return math.factorial(n)

    def permutations(self, n: int, k: int) -> int:
        if n < 0 or k < 0:
            raise ValueError("n and k must be non-negative.")
        if k > n:
            raise ValueError("k cannot be greater than n.")
        return math.perm(n, k)

    def combinations(self, n: int, k: int) -> int:
        if n < 0 or k < 0:
            raise ValueError("n and k must be non-negative.")
        if k > n:
            raise ValueError("k cannot be greater than n.")
        return math.comb(n, k)

    def mean(self, data: List[float]) -> float:
        if not data:
            raise ValueError("Dataset cannot be empty.")
        return statistics.mean(data)

    def median(self, data: List[float]) -> float:
        if not data:
            raise ValueError("Dataset cannot be empty.")
        return statistics.median(data)

    def standard_deviation(self, data: List[float]) -> float:
        if len(data) < 2:
            raise ValueError("Standard deviation requires at least two data points.")
        return statistics.stdev(data)