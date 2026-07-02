class BitwiseMath:
    def and_op(self, a: int, b: int) -> int:
        return a & b
    
    def or_op(self, a: int, b: int) -> int:
        return a | b
    
    def not_op(self, a: int) -> int:
        return ~a
    
    def xor_op(self, a: int, b: int) -> int:
        return a ^ b
    
    def shift_left_op(self, a: int, b: int) -> int:
        return a << b
    
    def shift_right_op(self, a: int, b: int) -> int:
        return a >> b