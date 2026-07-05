import unittest
from src.model.base_converter import BaseConverter

class TestBaseConverter(unittest.TestCase):
    def setUp(self):
        self.converter = BaseConverter()

    def test_to_binary(self):
        self.assertEqual(self.converter.to_binary(5), "101")
        self.assertEqual(self.converter.to_binary(0), "0")

        # Negative (Two's Complement 32-bit)
        self.assertEqual(self.converter.to_binary(-5), "11111111111111111111111111111011")

    def test_to_hex(self):
        self.assertEqual(self.converter.to_hex(255), "FF")
        self.assertEqual(self.converter.to_hex(0), "0")

        # Negative (Two's Complement 32-bit)
        self.assertEqual(self.converter.to_hex(-5), "FFFFFFFB")

    def test_from_binary(self):
        self.assertEqual(self.converter.from_binary("101"), 5)
        self.assertEqual(self.converter.from_binary("0"), 0)

        # 2. Negative (Checking if the 32nd bit sign logic works)
        self.assertEqual(self.converter.from_binary("11111111111111111111111111111011"), -5)

    def test_from_hex(self):
        self.assertEqual(self.converter.from_hex("FF"), 255)
        self.assertEqual(self.converter.from_binary("0"), 0)

        # 2. Negative
        self.assertEqual(self.converter.from_hex("FFFFFFFB"), -5)

    def test_mixed_conversion(self):
        test_numbers = [42, -42, 1024, -9999, 0]

        for num in test_numbers:
            bin_str = self.converter.to_binary(num)
            self.assertEqual(self.converter.from_binary(bin_str), num)
            
            hex_str = self.converter.to_hex(num)
            self.assertEqual(self.converter.from_hex(hex_str), num)

if __name__ == '__main__':
    unittest.main()