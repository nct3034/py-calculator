import unittest
from src.model.logical_math import LogicalMath

class TestLogicalMath(unittest.TestCase):
    def setUp(self):
        self.math = LogicalMath()

    def test_logical_and(self):
        self.assertEqual(self.math.logical_and(True, True), True)
        self.assertEqual(self.math.logical_and(True, False), False)
        self.assertEqual(self.math.logical_and(False, True), False)
        self.assertEqual(self.math.logical_and(False, False), False)

    def test_logical_or(self):
        self.assertEqual(self.math.logical_or(True, True), True)
        self.assertEqual(self.math.logical_or(True, False), True)
        self.assertEqual(self.math.logical_or(False, True), True)
        self.assertEqual(self.math.logical_or(False, False), False)

    def test_logical_not(self):
        self.assertEqual(self.math.logical_not(True), False)
        self.assertEqual(self.math.logical_not(False), True)

    def test_logical_xor(self):
        self.assertEqual(self.math.logical_xor(True, True), False)
        self.assertEqual(self.math.logical_xor(True, False), True)
        self.assertEqual(self.math.logical_xor(False, True), True)
        self.assertEqual(self.math.logical_xor(False, False), False)


if __name__ == '__main__':
    unittest.main()