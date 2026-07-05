import unittest
import sympy as sp
from src.model.equation_solver import EquationSolver

class TestEquationSolver(unittest.TestCase):
    def setUp(self):
        self.math = EquationSolver()

    def test_equation_linear(self):
        self.assertCountEqual(self.math.solve_linear(2, -4), [2])
        self.assertCountEqual(self.math.solve_linear(5, 0), [0])
        self.assertCountEqual(self.math.solve_linear(0, 3), ["No solution"])
        self.assertCountEqual(self.math.solve_linear(0, 0), ["Infinite solutions"])

    def test_equation_quadratic(self):
        self.assertCountEqual(self.math.solve_quadratic(1, -5, 6), [2, 3])
        self.assertCountEqual(self.math.solve_quadratic(1, -4, 4), [2])
        self.assertCountEqual(self.math.solve_quadratic(1, 0, 1), [-sp.I, sp.I])
        self.assertCountEqual(self.math.solve_quadratic(0, 2, -4), [2])
        self.assertCountEqual(self.math.solve_quadratic(0, 0, 6), ["No solution"])

    def test_equation_cubic(self):
        self.assertCountEqual(self.math.solve_cubic(1, -6, 11, -6), [1, 2, 3])
        
        expected_complex = [
            1,
            -sp.Rational(1, 2) - sp.sqrt(3) * sp.I / 2,
            -sp.Rational(1, 2) + sp.sqrt(3) * sp.I / 2
        ]
        self.assertCountEqual(self.math.solve_cubic(1, 0, 0, -1), expected_complex)
        
        self.assertCountEqual(self.math.solve_cubic(0, 1, -5, 6), [2, 3])