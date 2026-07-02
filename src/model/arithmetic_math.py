Number = int | float | complex

class ArithmeticMath:
    def add(self, a: Number, b: Number) -> Number:
        return a + b
    
    def subtract(self, a: Number, b: Number) -> Number:
        return a - b
    
    def multiply(self, a: Number, b: Number) -> Number:
        return a * b
    
    def divide(self, a: Number, b: Number) -> float | complex:
        if b == 0:
            raise ZeroDivisionError
        return a / b