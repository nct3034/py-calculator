import unittest
from src.model.relational_math import RelationalMath

class TestRelationalMath(unittest.TestCase):
    def setUp(self):
        self.math = RelationalMath()

    def test_is_greater(self):
        self.assertEqual(self.math.is_greater(10, 5), True)
        self.assertEqual(self.math.is_greater(5, 10), False)
        self.assertEqual(self.math.is_greater(10.5, 10.5), False)

    def test_is_less(self):
        self.assertEqual(self.math.is_less(5, 10), True)
        self.assertEqual(self.math.is_less(10, 5), False)
        self.assertEqual(self.math.is_less(10.5, 10.5), False)

    def test_is_greater_or_equal(self):
        self.assertEqual(self.math.is_greater_or_equal(10, 5), True)
        self.assertEqual(self.math.is_greater_or_equal(10.5, 10.5), True)
        self.assertEqual(self.math.is_greater_or_equal(5, 10), False)

    def test_is_less_or_equal(self):
        self.assertEqual(self.math.is_less_or_equal(5, 10), True)
        self.assertEqual(self.math.is_less_or_equal(10.5, 10.5), True)
        self.assertEqual(self.math.is_less_or_equal(10, 5), False)

    def test_is_equal(self):
        self.assertEqual(self.math.is_equal(10, 10), True)
        self.assertEqual(self.math.is_equal(10, 5), False)
        self.assertEqual(self.math.is_equal(10.5, 10.5), True)
        self.assertEqual(self.math.is_equal(2 + 3j, 2 + 3j), True)
        self.assertEqual(self.math.is_equal(2 + 3j, 2 + 4j), False)

    def test_is_not_equal(self):
        self.assertEqual(self.math.is_not_equal(10, 5), True)
        self.assertEqual(self.math.is_not_equal(10, 10), False)
        self.assertEqual(self.math.is_not_equal(2 + 3j, 4 + 1j), True)
        self.assertEqual(self.math.is_not_equal(2 + 3j, 2 + 3j), False)