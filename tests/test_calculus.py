import unittest
import math
from src.model.calculus import Calculus

class TestCalculus(unittest.TestCase):
    def setUp(self):
        self.calc = Calculus()

    def test_calculate_derivative(self):
        self.assertEqual(self.calc.calculate_derivative("x**2"), "2*x")
        self.assertEqual(self.calc.calculate_derivative("sin(x)"), "cos(x)")
        self.assertEqual(self.calc.calculate_derivative("x**3 + 3*x"), "3*x**2 + 3")

    def test_calculate_derivative_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_derivative("x +* 2")

    def test_calculate_indefinite_integral(self):
        self.assertEqual(self.calc.calculate_indefinite_integral("2*x"), "x**2")
        self.assertEqual(self.calc.calculate_indefinite_integral("cos(x)"), "sin(x)")
        self.assertEqual(self.calc.calculate_indefinite_integral("3*x**2"), "x**3")

    def test_calculate_indefinite_integral_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_indefinite_integral("x +* 2")

    def test_calculate_definite_integral(self):
        self.assertAlmostEqual(self.calc.calculate_definite_integral("x", 0, 2), 2.0)
        self.assertAlmostEqual(self.calc.calculate_definite_integral("x**2", 0, 3), 9.0)
        self.assertAlmostEqual(self.calc.calculate_definite_integral("cos(x)", 0, math.pi / 2), 1.0)

    def test_calculate_definite_integral_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_definite_integral("x +* 2", 0, 1)