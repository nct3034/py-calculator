import unittest
from src.model.bitwise_math import BitwiseMath

class TestBitwiseMath(unittest.TestCase):
    def setUp(self):
        self.math = BitwiseMath()

    def test_bitwise_and(self):
        self.assertEqual(self.math.and_op(5, 3), 1)
        self.assertEqual(self.math.and_op(12, 10), 8)
        self.assertEqual(self.math.and_op(7, 0), 0)

    def test_bitwise_or(self):
        self.assertEqual(self.math.or_op(5, 3), 7)
        self.assertEqual(self.math.or_op(8, 4), 12)
        self.assertEqual(self.math.or_op(10, 0), 10)

    def test_bitwise_xor(self):
        self.assertEqual(self.math.xor_op(5, 3), 6)
        self.assertEqual(self.math.xor_op(15, 15), 0)

    def test_bitwise_not(self):
        self.assertEqual(self.math.not_op(5), -6)
        self.assertEqual(self.math.not_op(0), -1)
        self.assertEqual(self.math.not_op(-10), 9)

    def test_left_shift(self):
        self.assertEqual(self.math.shift_left_op(5, 1), 10)
        self.assertEqual(self.math.shift_left_op(3, 3), 24)

    def test_right_shift(self):
        self.assertEqual(self.math.shift_right_op(10, 1), 5)
        self.assertEqual(self.math.shift_right_op(15, 2), 3)