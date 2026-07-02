Number = int | float | complex
RealNumber = int | float

class RelationalMath:
    def is_greater(self, a: RealNumber, b: RealNumber) -> bool:
        return a > b
    
    def is_less(self, a: RealNumber, b: RealNumber) -> bool:
        return a < b
    
    def is_greater_or_equal(self, a: RealNumber, b: RealNumber) -> bool:
        return a >= b
    
    def is_less_or_equal(self, a: RealNumber, b: RealNumber) -> bool:
        return a <= b
    
    def is_equal(self, a: Number, b: Number) -> bool:
        return a == b
    
    def is_not_equal(self, a: Number, b: Number) -> bool:
        return a != b
    
