class BaseConverter:
    def to_binary(self, decimal_val: int) -> str:
        return f"{decimal_val & 0xFFFFFFFF:b}"
    
    def to_hex(self, decimal_val: int) -> str:
        return f"{decimal_val & 0xFFFFFFFF:X}"
    
    def from_binary(self, binary_str: str) -> int:
        val = int(binary_str, 2)
        # Check if the 32nd bit (sign bit) is 1
        if val >= 0x80000000:
            return val - 0x100000000
        return val
    
    def from_hex(self, hex_str: str) -> int:
        val = int(hex_str, 16)
        # Check if the 32nd bit (sign bit) is 1
        if val >= 0x80000000:
            return val - 0x100000000
        return val