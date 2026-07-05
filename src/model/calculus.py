import sympy as sp

class Calculus:
    def __init__(self):
        self.x = sp.Symbol('x')

    def derivative(self, expression: str) -> str:
        try:
            parsed_expression = sp.sympify(expression)
            result = sp.diff(parsed_expression, self.x)
            return str(result)
        except Exception as e:
            raise ValueError(f"Invalid expressionession: {e}")
    
    def calculate_indefinite_integral(self, expression: str) -> str:
        try:
            parsed_expression = sp.sympify(expression)
            result = sp.integrate(parsed_expression, self.x)
            return str(result)
        except Exception as e:
            raise ValueError(f"Invalid expressionession: {e}")

    def calculate_definite_integral(self, expression: str, lower_limit: float, upper_limit: float) -> float:
        try:
            parsed_expression = sp.sympify(expression)
            result = sp.integrate(parsed_expression, (self.x, lower_limit, upper_limit))
            return float(result.evalf())
        except Exception as e:
            raise ValueError(f"Invalid expressionession or limits: {e}")