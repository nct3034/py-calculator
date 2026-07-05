class MemoryManager:
    def __init__(self):
        self.ans = 0.0
        self.history = []

        # Standard M Memory (for M+, M-, MR buttons)
        self.memory_value = 0.0

        self.variables = {
            'A': 0.0,
            'B': 0.0,
            'C': 0.0,
            'D': 0.0,
            'E': 0.0,
            'F': 0.0,
            'x': 0.0
        }

    # --- ANS and History Features ---
    def save_calculation(self, expression: str, result):
        self.ans = result
        self.history.append({"expression": expression, "result": result})
        if len(self.history) > 50:
            self.history.pop(0)

    def get_ans(self):
        return self.ans

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

    # --- Named Variables (A-F, x) ---
    def store_variable(self, name: str, value):
        """Stores a numeric value into a specific variable (e.g., 'A' or 'x')."""
        if name not in self.variables:
            raise ValueError(f"Variable '{name}' is not supported.")
        try:
            self.variables[name] = float(value)
        except ValueError:
            raise ValueError("Can only store numeric values in variables.")

    def recall_variable(self, name: str) -> float:
        """Recalls the current value of a specific variable."""
        if name not in self.variables:
            raise ValueError(f"Variable '{name}' is not supported.")
        return self.variables[name]

    def clear_all_variables(self):
        """Resets A-F and x all back to 0.0."""
        for key in self.variables:
            self.variables[key] = 0.0

    # --- Standard Calculator Memory Buttons (M+, M-, MR, MC) ---
    def memory_add(self, value):
        try:
            self.memory_value += float(value)
        except ValueError:
            raise ValueError("Can only add numeric values to memory.")

    def memory_subtract(self, value):
        try:
            self.memory_value -= float(value)
        except ValueError:
            raise ValueError("Can only subtract numeric values from memory.")

    def memory_recall(self) -> float:
        return self.memory_value

    def memory_clear(self):
        self.memory_value = 0.0