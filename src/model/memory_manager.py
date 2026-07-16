class MemoryManager:
    def __init__(self):
        self.ans = 0.0
        self.history = []

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