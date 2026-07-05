import sympy as sp
from typing import List, Any

class EquationSolver:
    def __init__(self):
        self.x = sp.Symbol('x')

    def solve_linear(self, a: float, b: float) -> List[Any]:
        if a == 0:
            if b == 0:
                return ["Infinite solutions"]
            return ["No solution"]
        expr = a * self.x + b
        return sp.solve(expr, self.x)

    def solve_quadratic(self, a: float, b: float, c: float) -> List[Any]:
        if a == 0:
            return self.solve_linear(b, c)
        expr = a * self.x**2 + b * self.x + c
        return sp.solve(expr, self.x)
    
    def solve_cubic(self, a: float, b: float, c: float, d: float) -> List[Any]:
        if a == 0:
            return self.solve_quadratic(b, c, d)
        expr = a * self.x**3 + b * self.x**2 + c * self.x + d
        return sp.solve(expr, self.x)