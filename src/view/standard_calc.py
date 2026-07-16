from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, QEvent # Thêm QEvent
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
        # Cài đặt bộ lọc sự kiện để bắt phím bàn phím
        self.display.installEventFilter(self) 
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

    def showEvent(self, event):
        super().showEvent(event)
        self.display.setFocus() # Ép tập trung vào display khi trang hiện ra

    # --- BỘ LỌC PHÍM (EVENT FILTER) ---
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            char = event.text()

            if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
                self.handle_equals()
            elif key == Qt.Key.Key_Backspace:
                self.handle_backspace()
            elif key == Qt.Key.Key_Delete:
                self.handle_clear()
            elif char in "0123456789":
                self.handle_digit(char)
            elif char == ".":
                self.handle_decimal()
            elif char in "+-*/":
                mapping = {'+': '+', '-': '−', '*': '×', '/': '÷'}
                self.handle_operator(mapping[char])
            self.refresh_display()
            return True
        return super().eventFilter(obj, event)

    # --- ROUTER & LOGIC ---
    def on_button_click(self, text, variant):
        if variant == "number":
            if text == ".": self.handle_decimal()
            else: self.handle_digit(text)
        elif variant == "clear": self.handle_clear()
        elif variant == "function":
            if text == "⌫": self.handle_backspace()
            elif text == "%": self.handle_percent()
        elif variant == "operator": self.handle_operator(text)
        elif variant == "equals": self.handle_equals()
        self.refresh_display()

    # --- CÁC HÀM XỬ LÝ LOGIC CƠ BẢN ---
    def handle_digit(self, digit):
        """Xử lý gõ số"""
        if self.should_reset:
            self.display_val = digit if digit != "0" else "0"
            self.should_reset = False
        elif self.display_val == "0" and digit != ".":
            self.display_val = digit
        else:
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
            
        if len(self.display_val) <= 1 or self.display_val in ["Error", "Division zero", "Value Error"]:
            self.display_val = "0"
        else:
            self.display_val = self.display_val[:-1]

    def handle_percent(self):
        """Xử lý phần trăm"""
        try:
            val = float(self.display_val) / 100
            self.display_val = self.fmt_num(val)
        except ValueError:
            self.display_val = "Value Error"

    def refresh_display(self):
        """Cập nhật dữ liệu từ State lên giao diện UI"""
        self.display.update_display(self.expression_val, self.display_val)

    def fmt_num(self, n):
        """Định dạng số hiển thị"""
        if n == float('inf'): return "Error"
        return f"{n:.10g}"

    # --- CẬP NHẬT LỖI XỬ LÝ ---
    def _execute_math(self, a, op, b):
        if op == '+': return self.math_logic.add(a, b)
        if op == '−': return self.math_logic.subtract(a, b)
        if op == '×': return self.math_logic.multiply(a, b)
        if op == '÷': 
            return self.math_logic.divide(a, b) # Để hàm này ném ZeroDivisionError ra ngoài
        return b

    def handle_operator(self, op):
        try:
            cur = float(self.display_val)
            if self.pending_op and not self.should_reset:
                res = self._execute_math(self.pending_op["value"], self.pending_op["op"], cur)
                self.display_val = self.fmt_num(res)
                self.expression_val = f"{self.display_val} {op}"
                self.pending_op = {"value": res, "op": op}
            else:
                self.expression_val = f"{self.display_val} {op}"
                self.pending_op = {"value": cur, "op": op}
            self.should_reset = True
        except ZeroDivisionError:
            self.display_val = "Division zero"
        except ValueError:
            self.display_val = "Value Error"

    def handle_equals(self):
        if not self.pending_op: return
        try:
            # 1. Lưu toán hạng thứ hai vào biến tạm để hiển thị đúng
            cur_str = self.display_val 
            cur_val = float(self.display_val)
            
            # 2. Tính toán
            res = self._execute_math(self.pending_op["value"], self.pending_op["op"], cur_val)
            
            # 3. Cập nhật biểu thức (Sử dụng cur_str thay vì self.display_val vừa bị thay đổi)
            self.expression_val = f"{self.fmt_num(self.pending_op['value'])} {self.pending_op['op']} {cur_str} ="
            
            # 4. Cập nhật kết quả lên màn hình
            self.display_val = self.fmt_num(res)
            
            self.pending_op = None
            self.should_reset = True
        except ZeroDivisionError:
            self.display_val = "Division zero"
        except ValueError:
            self.display_val = "Value Error"
