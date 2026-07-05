import unittest
from src.model.arithmetic_math import ArithmeticMath

class TestArithmeticMath(unittest.TestCase):
    def setUp(self):
        self.math = ArithmeticMath()

    def test_add(self):
        self.assertEqual(self.math.add(59, 23), 82)
        self.assertEqual(self.math.add(60, -42), 18)
        self.assertEqual(self.math.add(-1, -6), -7)

    def test_subtract(self):
        self.assertEqual(self.math.subtract(20, 7), 13)
        self.assertEqual(self.math.subtract(-5, -20), 15)
        self.assertEqual(self.math.subtract(15, -16), 31)

    def test_multiply(self):
        self.assertEqual(self.math.multiply(2, 2), 4)
        self.assertEqual(self.math.multiply(-6, 3), -18)
        self.assertEqual(self.math.multiply(-5, -3), 15)
        self.assertEqual(self.math.multiply(-100, 0), 0)

    def test_divide_basic_integers(self):
        self.assertEqual(self.math.divide(10, 2), 5.0)
        self.assertEqual(self.math.divide(-12, 6), -2.0)
        self.assertEqual(self.math.divide(-50, -5), 10.0)

    def test_divide_by_zero_raises_error(self):
        with self.assertRaises(ZeroDivisionError):
            self.math.divide(10, 0)

    def test_floating_point(self):
        self.assertAlmostEqual(self.math.add(0.1, 0.2), 0.3)
        self.assertAlmostEqual(self.math.divide(1, 3), 0.3333333, places=7)

    def test_complex_numbers(self):
        self.assertEqual(self.math.add(2 + 3j, 1 + 1j), 3 + 4j)
        self.assertEqual(self.math.subtract(5 + 5j, 2 + 1j), 3 + 4j)
        
        self.assertEqual(self.math.multiply(2 + 1j, 1 + 2j), 5j) 
        self.assertEqual(self.math.divide(4 + 2j, 2 + 0j), 2 + 1j)

        self.assertEqual(self.math.add(3 + 4j, 10), 13 + 4j)           # Complex + Int
        self.assertEqual(self.math.subtract(5.5, 2 + 1j), 3.5 - 1j)    # Float - Complex
        self.assertEqual(self.math.multiply(2 + 3j, 2.5), 5.0 + 7.5j)  # Complex * Float
        self.assertEqual(self.math.divide(10 + 5j, 5), 2 + 1j)         # Complex / Int


if __name__ == '__main__':
    unittest.main()