import unittest
import math
from src.model.scientific_math import ScientificMath

class TestScientificMath(unittest.TestCase):
    def setUp(self):
        self.math = ScientificMath()

    def test_trigonometry_degrees(self):
        # Default to Degree mode
        self.assertAlmostEqual(self.math.sin(30), 0.5)
        self.assertAlmostEqual(self.math.sin(90), 1.0)
        self.assertAlmostEqual(self.math.cos(60), 0.5)
        self.assertAlmostEqual(self.math.cos(180), -1.0)
        self.assertAlmostEqual(self.math.tan(45), 1.0)

    def test_trigonometry_radians(self):
        self.math.is_degree = False
        self.assertAlmostEqual(self.math.sin(math.pi / 2), 1.0)
        self.assertAlmostEqual(self.math.cos(math.pi), -1.0)
        self.assertAlmostEqual(self.math.tan(math.pi / 4), 1.0)

    def test_tan_undefined(self):
        with self.assertRaises(ValueError):
            self.math.tan(90)
        
        self.math.is_degree = False
        with self.assertRaises(ValueError):
            self.math.tan(math.pi / 2)

    def test_inverse_trigonometry(self):
        self.assertAlmostEqual(self.math.arcsin(0.5), 30.0)
        self.assertAlmostEqual(self.math.arccos(0.5), 60.0)
        self.assertAlmostEqual(self.math.arctan(1), 45.0)

    def test_inverse_trigonometry_domain_errors(self):
        with self.assertRaises(ValueError):
            self.math.arcsin(2)
        with self.assertRaises(ValueError):
            self.math.arccos(-1.5)

    def test_logarithms(self):
        self.assertEqual(self.math.log10(100), 2.0)
        self.assertEqual(self.math.log10(1000), 3.0)
        self.assertAlmostEqual(self.math.ln(math.e), 1.0)
        self.assertAlmostEqual(self.math.ln(math.exp(5)), 5.0)

    def test_logarithm_domain_errors(self):
        with self.assertRaises(ValueError):
            self.math.log10(0)
        with self.assertRaises(ValueError):
            self.math.ln(-5)

    def test_exponentials(self):
        self.assertEqual(self.math.exp(0), 1.0)
        self.assertAlmostEqual(self.math.exp(1), math.e)
        self.assertEqual(self.math.power(2, 3), 8.0)
        self.assertEqual(self.math.power(9, 0.5), 3.0)
        self.assertEqual(self.math.power(-2, 3), -8.0)

    def test_roots(self):
        self.assertEqual(self.math.sqrt(16), 4.0)
        self.assertEqual(self.math.sqrt(0), 0.0)
        self.assertEqual(self.math.cbrt(27), 3.0)
        self.assertEqual(self.math.cbrt(-8), -2.0)

    def test_sqrt_domain_error(self):
        with self.assertRaises(ValueError):
            self.math.sqrt(-4)

    def test_absolute(self):
        self.assertEqual(self.math.absolute(-15.5), 15.5)
        self.assertEqual(self.math.absolute(42), 42)
        self.assertEqual(self.math.absolute(0), 0)

    def test_fraction_to_decimal(self):
        self.assertEqual(self.math.fraction_to_decimal(1, 4), 0.25)
        self.assertEqual(self.math.fraction_to_decimal(-3, 2), -1.5)

    def test_fraction_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.math.fraction_to_decimal(5, 0)

if __name__ == '__main__':
    unittest.main()