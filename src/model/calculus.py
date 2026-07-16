import sympy as sp

class Calculus:
    def __init__(self):
        self.x = sp.Symbol('x')

    def calculate_derivative(self, expression: str) -> str:
        try:
            parsed_expression = sp.sympify(expression)
            result = sp.diff(parsed_expression, self.x)
            return str(result)
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
    
    def calculate_derivative_at(self, expression: str, value: str) -> float:
        try:
            parsed_expression = sp.sympify(expression)
            derivative = sp.diff(parsed_expression, self.x)
            val = sp.sympify(value)
            # Thay thế x bằng giá trị cụ thể và tính toán ra số thực
            result = derivative.evalf(subs={self.x: val})
            return float(result)
        except Exception as e:
            raise ValueError(f"Invalid expression or value: {e}")

    def calculate_indefinite_integral(self, expression: str) -> str:
        try:
            parsed_expression = sp.sympify(expression)
            result = sp.integrate(parsed_expression, self.x)
            return f"{result} + C"
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
        
    def calculate_definite_integral(self, expression: str, lower_limit: str, upper_limit: str) -> float:
        try:
            parsed_expression = sp.sympify(expression)
            lower = sp.sympify(lower_limit)
            upper = sp.sympify(upper_limit)
            
            result = sp.integrate(parsed_expression, (self.x, lower, upper))
            return float(result.evalf())
        except Exception as e:
            raise ValueError(f"Invalid expression or limits: {e}")