import unittest
from src.model.expression_parser import ExpressionParser

class TestExpressionParser(unittest.TestCase):
    def setUp(self):
        self.parser = ExpressionParser()

    # --- Kiểm tra tính toán cơ bản ---
    def test_arithmetic_basic(self):
        self.assertEqual(self.parser.evaluate("2+3"), 5.0)
        self.assertEqual(self.parser.evaluate("10-4"), 6.0)
        self.assertEqual(self.parser.evaluate("5*2"), 10.0)
        self.assertEqual(self.parser.evaluate("10/2"), 5.0)

    # --- Kiểm tra độ ưu tiên ---
    def test_precedence(self):
        self.assertEqual(self.parser.evaluate("2+3*4"), 14.0)
        self.assertEqual(self.parser.evaluate("10-6/2"), 7.0)
        self.assertEqual(self.parser.evaluate("2^3+1"), 9.0)

    # --- Kiểm tra dấu ngoặc ---
    def test_parentheses(self):
        self.assertEqual(self.parser.evaluate("(2+3)*4"), 20.0)
        self.assertEqual(self.parser.evaluate("2*(3+4)"), 14.0)
        self.assertEqual(self.parser.evaluate("((1+2)*3)"), 9.0)

    # --- Kiểm tra hàm số ---
    def test_functions(self):
        self.assertAlmostEqual(self.parser.evaluate("sin(90)"), 1.0)
        self.assertAlmostEqual(self.parser.evaluate("sqrt(16)"), 4.0)
        self.assertAlmostEqual(self.parser.evaluate("log(100)"), 2.0)

    # --- Kiểm tra các trường hợp lỗi ---
    def test_invalid_parentheses(self):
        # Trường hợp thừa dấu mở
        with self.assertRaises(ValueError):
            self.parser.evaluate("(1+2")
        with self.assertRaises(ValueError):
            self.parser.evaluate("1+2)")
        
    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.parser.evaluate("10/0")

if __name__ == '__main__':
    unittest.main()