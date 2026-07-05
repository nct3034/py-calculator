import unittest
from src.model.memory_manager import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.memory = MemoryManager()

    # --- ANS and History Tests ---
    def test_save_calculation_and_history(self):
        self.memory.save_calculation("2 + 2", 4.0)
        self.assertEqual(self.memory.get_ans(), 4.0)
        
        history = self.memory.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["expression"], "2 + 2")
        self.assertEqual(history[0]["result"], 4.0)

    def test_history_limit(self):
        # Simulate doing 55 calculations
        for i in range(55):
            self.memory.save_calculation(f"{i} + 1", i + 1.0)
        
        # History should cap at 50
        self.assertEqual(len(self.memory.get_history()), 50)
        # The oldest calculations should be gone, meaning the last one is 54+1
        self.assertEqual(self.memory.get_history()[-1]["result"], 55.0)

    def test_clear_history(self):
        self.memory.save_calculation("10 / 2", 5.0)
        self.memory.clear_history()
        self.assertEqual(len(self.memory.get_history()), 0)

    # --- Named Variables (A-F, x) Tests ---
    def test_store_and_recall_variable(self):
        self.memory.store_variable('A', 42.5)
        self.memory.store_variable('x', -10.0)
        self.assertEqual(self.memory.recall_variable('A'), 42.5)
        self.assertEqual(self.memory.recall_variable('x'), -10.0)

    def test_variable_invalid_name(self):
        with self.assertRaises(ValueError):
            self.memory.store_variable('Z', 100) # Z is not in our dictionary
        with self.assertRaises(ValueError):
            self.memory.recall_variable('Y')

    def test_variable_invalid_value(self):
        with self.assertRaises(ValueError):
            self.memory.store_variable('B', "x + 2") # Cannot store algebra string as a number

    def test_clear_all_variables(self):
        self.memory.store_variable('C', 99.9)
        self.memory.store_variable('F', 1.1)
        self.memory.clear_all_variables()
        self.assertEqual(self.memory.recall_variable('C'), 0.0)
        self.assertEqual(self.memory.recall_variable('F'), 0.0)

    # --- Standard Memory (M) Tests ---
    def test_memory_add_subtract_recall_clear(self):
        self.memory.memory_add(10.5)
        self.memory.memory_subtract(2.5)
        self.assertEqual(self.memory.memory_recall(), 8.0)
        
        self.memory.memory_clear()
        self.assertEqual(self.memory.memory_recall(), 0.0)

    def test_memory_invalid_value(self):
        with self.assertRaises(ValueError):
            self.memory.memory_add("2*x")
        with self.assertRaises(ValueError):
            self.memory.memory_subtract("invalid")

if __name__ == '__main__':
    unittest.main()