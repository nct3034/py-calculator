import unittest
from src.model.statistic import Statistics

class TestStatistics(unittest.TestCase):
    def setUp(self):
        self.stats = Statistics()

    # --- Factorial Tests ---
    def test_factorial(self):
        self.assertEqual(self.stats.factorial(5), 120)
        self.assertEqual(self.stats.factorial(0), 1)

    def test_factorial_invalid(self):
        with self.assertRaises(ValueError):
            self.stats.factorial(-5)

    # --- Permutations Tests ---
    def test_permutations(self):
        self.assertEqual(self.stats.permutations(5, 3), 60)
        self.assertEqual(self.stats.permutations(5, 0), 1)

    def test_permutations_invalid(self):
        with self.assertRaises(ValueError):
            self.stats.permutations(-5, 2)
        with self.assertRaises(ValueError):
            self.stats.permutations(3, 5) # k > n

    # --- Combinations Tests ---
    def test_combinations(self):
        self.assertEqual(self.stats.combinations(5, 3), 10)
        self.assertEqual(self.stats.combinations(5, 0), 1)

    def test_combinations_invalid(self):
        with self.assertRaises(ValueError):
            self.stats.combinations(5, -2)
        with self.assertRaises(ValueError):
            self.stats.combinations(2, 5) # k > n

    # --- Mean Tests ---
    def test_mean(self):
        self.assertEqual(self.stats.mean([1, 2, 3, 4, 5]), 3.0)
        self.assertEqual(self.stats.mean([10.5, 20.5]), 15.5)

    def test_mean_invalid(self):
        with self.assertRaises(ValueError):
            self.stats.mean([])

    # --- Median Tests ---
    def test_median(self):
        self.assertEqual(self.stats.median([1, 3, 3, 6, 7, 8, 9]), 6.0) # Odd amount of data
        self.assertEqual(self.stats.median([1, 2, 3, 4]), 2.5)          # Even amount of data

    def test_median_invalid(self):
        with self.assertRaises(ValueError):
            self.stats.median([])

    # --- Standard Deviation Tests ---
    def test_standard_deviation(self):
        self.assertEqual(self.stats.standard_deviation([1, 2, 3]), 1.0)
        self.assertAlmostEqual(self.stats.standard_deviation([1.5, 2.5, 2.5, 2.75, 3.25, 4.75]), 1.081087, places=5)

    def test_standard_deviation_invalid(self):
        with self.assertRaises(ValueError):
            self.stats.standard_deviation([5.0]) # Requires at least 2 points
        with self.assertRaises(ValueError):
            self.stats.standard_deviation([])

if __name__ == '__main__':
    unittest.main()