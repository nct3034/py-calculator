import math

class ScientificMath:
    def __init__(self):
        # Default to Degree mode
        self.is_degree = True 

    def _to_rad(self, value: float) -> float:
        # Convert to Radian if currently in Degree mode
        return math.radians(value) if self.is_degree else value

    def _to_deg(self, value: float) -> float:
        # Convert back to Degree if needed
        return math.degrees(value) if self.is_degree else value

    # --- Trigonometry ---
    def sin(self, x: float) -> float:
        return math.sin(self._to_rad(x))

    def cos(self, x: float) -> float:
        return math.cos(self._to_rad(x))

    def tan(self, x: float) -> float:
        # Handle asymptotes (e.g., tan(90 degrees))
        rad_val = self._to_rad(x)
        if math.isclose(math.cos(rad_val), 0, abs_tol=1e-9):
            raise ValueError("Math Error: Tangent undefined")
        return math.tan(rad_val)

    def arcsin(self, x: float) -> float:
        if x < -1 or x > 1:
            raise ValueError("Domain Error: arcsin accepts [-1, 1]")
        return self._to_deg(math.asin(x))

    def arccos(self, x: float) -> float:
        if x < -1 or x > 1:
            raise ValueError("Domain Error: arccos accepts [-1, 1]")
        return self._to_deg(math.acos(x))

    def arctan(self, x: float) -> float:
        return self._to_deg(math.atan(x))

    # --- Logarithm & Exponential ---
    def log10(self, x: float) -> float:
        if x <= 0:
            raise ValueError("Domain Error: log10 accepts (0, +inf)")
        return math.log10(x)

    def ln(self, x: float) -> float:
        if x <= 0:
            raise ValueError("Domain Error: ln accepts (0, +inf)")
        return math.log(x)

    def exp(self, x: float) -> float:
        # Calculate e^x
        return math.exp(x)

    def power(self, base: float, exponent: float) -> float:
        # Calculate base^exponent
        return math.pow(base, exponent)

    # --- Roots & Absolute Value ---
    def sqrt(self, x: float) -> float:
        if x < 0:
            raise ValueError("Domain Error: square root of negative number")
        return math.sqrt(x)

    def cbrt(self, x: float) -> float:
        # Calculate cube root
        # Handle negative numbers since math.pow doesn't support negative bases with fractional exponents in Python
        if x < 0:
            return -math.pow(-x, 1/3)
        return math.pow(x, 1/3)

    def absolute(self, x: float) -> float:
        return abs(x)

    # --- Fraction ---
    def fraction_to_decimal(self, numerator: float, denominator: float) -> float:
        if denominator == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return numerator / denominator