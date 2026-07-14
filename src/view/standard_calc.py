from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from .components import CalcButton, CalcDisplay
from src.model.arithmetic_math import ArithmeticMath

class StandardCalc(QWidget):
    def __init__(self):
        super().__init__()
        
        self.display_val = "0"
        self.expression_val = ""
        self.should_reset = False
        self.pending_op = None
        self.math_logic = ArithmeticMath()

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        self.display = CalcDisplay()
        main_layout.addWidget(self.display)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        main_layout.addLayout(grid_layout)

        buttons = [
            ("AC", 0, 0, 1, 1, "clear"), ("⌫", 0, 1, 1, 1, "function"), ("%", 0, 2, 1, 1, "function"), ("÷", 0, 3, 1, 1, "operator"),
            ("7",  1, 0, 1, 1, "number"),("8", 1, 1, 1, 1, "number"),   ("9", 1, 2, 1, 1, "number"),   ("×", 1, 3, 1, 1, "operator"),
            ("4",  2, 0, 1, 1, "number"),("5", 2, 1, 1, 1, "number"),   ("6", 2, 2, 1, 1, "number"),   ("−", 2, 3, 1, 1, "operator"),
            ("1",  3, 0, 1, 1, "number"),("2", 3, 1, 1, 1, "number"),   ("3", 3, 2, 1, 1, "number"),   ("+", 3, 3, 1, 1, "operator"),
            ("0",  4, 0, 1, 2, "number"),(".", 4, 2, 1, 1, "number"),   ("=", 4, 3, 1, 1, "equals")
        ]

        for text, row, col, row_span, col_span, variant in buttons:
            is_wide = col_span > 1 
            btn = CalcButton(text, variant=variant, wide=is_wide)
            grid_layout.addWidget(btn, row, col, row_span, col_span)
            
            btn.clicked.connect(lambda checked, t=text, v=variant: self.on_button_click(t, v))

    # --- BỘ ĐỊNH TUYẾN (ROUTER) ---
    def on_button_click(self, text, variant):
        """Phân loại hành động dựa trên loại nút bấm"""
        if variant == "number":
            if text == ".":
                self.handle_decimal()
            else:
                self.handle_digit(text)
        elif variant == "clear":
            self.handle_clear()
        elif variant == "function":
            if text == "⌫":
                self.handle_backspace()
            elif text == "%":
                self.handle_percent()
        elif variant == "operator":
            self.handle_operator(text)
        elif variant == "equals":
            self.handle_equals()
            
        self.refresh_display()

    # --- CÁC HÀM XỬ LÝ LOGIC ---
    def handle_digit(self, digit):
        """Xử lý gõ số"""
        if self.should_reset:
            self.display_val = digit if digit != "0" else "0"
            self.should_reset = False
        elif self.display_val == "0" and digit != ".":
            self.display_val = digit
        else:
            # Giới hạn 10 chữ số để không bị tràn màn hình
            if len(self.display_val.replace(".", "")) < 10:
                self.display_val += digit

    def handle_decimal(self):
        """Xử lý gõ dấu chấm thập phân"""
        if self.should_reset:
            self.display_val = "0."
            self.should_reset = False
        elif "." not in self.display_val:
            self.display_val += "."

    def handle_clear(self):
        """Nút AC: Khôi phục tất cả về mặc định"""
        self.display_val = "0"
        self.expression_val = ""
        self.pending_op = None
        self.should_reset = False

    def handle_backspace(self):
        """Nút ⌫: Xóa lùi từng ký tự"""
        if self.should_reset:
            self.display_val = "0"
            self.should_reset = False
            return
            
        if len(self.display_val) <= 1 or self.display_val == "Error":
            self.display_val = "0"
        else:
            self.display_val = self.display_val[:-1]

    def refresh_display(self):
        """Cập nhật dữ liệu từ State lên giao diện UI"""
        self.display.update_display(self.expression_val, self.display_val)

    def _execute_math(self, a, op, b):
        if op == '+': return self.math_logic.add(a, b)
        if op == '−': return self.math_logic.subtract(a, b)
        if op == '×': return self.math_logic.multiply(a, b)
        if op == '÷': 
            try:
                return self.math_logic.divide(a, b)
            except ZeroDivisionError:
                return float('inf')
        return b

    def fmt_num(self, n):
        if n == float('inf'): return "Error"
        return f"{n:.10g}"

    def handle_percent(self):
        try:
            val = float(self.display_val) / 100
            self.display_val = self.fmt_num(val)
        except ValueError:
            pass

    def handle_operator(self, op):
        try:
            cur = float(self.display_val)
            if self.pending_op and not self.should_reset:
                res = self._execute_math(self.pending_op["value"], self.pending_op["op"], cur)
                fmt_res = self.fmt_num(res)
                
                self.display_val = fmt_res
                self.expression_val = f"{fmt_res} {op}"
                self.pending_op = {"value": res, "op": op}
            else:
                self.expression_val = f"{self.display_val} {op}"
                self.pending_op = {"value": cur, "op": op}
            
            self.should_reset = True
        except ValueError:
            pass

    def handle_equals(self):
        if not self.pending_op:
            return
        try:
            cur = float(self.display_val)
            res = self._execute_math(self.pending_op["value"], self.pending_op["op"], cur)
            fmt_res = self.fmt_num(res)
            
            self.expression_val = f"{self.fmt_num(self.pending_op['value'])} {self.pending_op['op']} {self.display_val} ="
            self.display_val = fmt_res
            
            self.pending_op = None
            self.should_reset = True
        except ValueError:
            pass