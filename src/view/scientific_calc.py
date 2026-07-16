from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal

class ScientificCalc(QWidget):
    evaluate_requested = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.is_shift = False
        self.just_evaluated = False 
        self.shiftable_buttons = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 15)
        main_layout.setSpacing(10)

        # --- 1. MÀN HÌNH HIỂN THỊ ---
        self.lbl_expression = QLabel("")
        self.lbl_expression.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 14px; font-family: 'JetBrains Mono';")
        self.lbl_expression.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.lbl_display = QLineEdit("")
        self.lbl_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lbl_display.setStyleSheet("background: transparent; border: none; color: white; font-size: 36px; font-weight: bold; padding-right: 5px;")
        
        main_layout.addWidget(self.lbl_expression)
        main_layout.addWidget(self.lbl_display)
        
        # --- 2. THANH TRẠNG THÁI (SHIFT & D-PAD) ---
        status_layout = QHBoxLayout()
        self.btn_shift = self.create_button("SHIFT", "#f59e0b", "rgba(245, 158, 11, 0.15)", 60)
        self.btn_shift.clicked.connect(self.toggle_shift)
        
        self.is_degree = True
        self.btn_angle = self.create_button("DEG", "#10b981", "rgba(16, 185, 129, 0.15)", 60)
        self.btn_angle.clicked.connect(self.toggle_angle)
        
        self.btn_left = self.create_button("◀", "#a78bfa", "rgba(109,40,217,0.2)", 45)
        self.btn_left.clicked.connect(lambda: self.lbl_display.cursorBackward(False))
        
        self.btn_right = self.create_button("▶", "#a78bfa", "rgba(109,40,217,0.2)", 45)
        self.btn_right.clicked.connect(lambda: self.lbl_display.cursorForward(False))
        
        status_layout.addWidget(self.btn_shift)
        status_layout.addWidget(self.btn_angle)
        status_layout.addStretch()
        status_layout.addWidget(self.btn_left)
        status_layout.addWidget(self.btn_right)
        main_layout.addLayout(status_layout)

        # --- 3. BÀN PHÍM LƯỚI ---
        grid = QGridLayout()
        grid.setSpacing(6)
        
        buttons = [
            # Dòng 1: Tổ hợp, Chỉnh hợp, Giai thừa, Mũ, Căn
            (0, 0, "ℂ", "ℂ", "comb"), (0, 1, "ℙ", "ℙ", "comb"), (0, 2, "!", "!", "func"), (0, 3, "x²", "^", "func"), (0, 4, "√", "∛", "func"),
            # Dòng 2: Lượng giác, Logarit
            (1, 0, "sin", "arcsin", "func"), (1, 1, "cos", "arccos", "func"), (1, 2, "tan", "arctan", "func"), (1, 3, "log", "10ˣ", "func"), (1, 4, "ln", "eˣ", "func"),
            # Dòng 3: Ngoặc, S-D, Hằng số
            # Dòng 3: Ngoặc, Hằng số e, π, S-D
            (2, 0, "(", "(", "func"), (2, 1, ")", ")", "func"), (2, 2, "e", "e", "func"), (2, 3, "π", "π", "func"), (2, 4, "S-D", "S-D", "yellow_btn"),
            # Dòng 4-7: Số và toán tử cơ bản
            (3, 0, "7", "7", "num"), (3, 1, "8", "8", "num"), (3, 2, "9", "9", "num"), (3, 3, "DEL", "DEL", "action"), (3, 4, "AC", "AC", "action"),
            (4, 0, "4", "4", "num"), (4, 1, "5", "5", "num"), (4, 2, "6", "6", "num"), (4, 3, "×", "×", "op"), (4, 4, "÷", "÷", "op"),
            (5, 0, "1", "1", "num"), (5, 1, "2", "2", "num"), (5, 2, "3", "3", "num"), (5, 3, "+", "+", "op"), (5, 4, "−", "−", "op"),
            (6, 0, "0", "0", "num"), (6, 1, ".", ".", "num"), (6, 2, "Ans", "Ans", "yellow_btn"), (6, 3, "=", "=", "equals"), (6, 4, "", "", "empty")
        ]

        for r, c, norm, shift, b_type in buttons:
            if not norm: continue # Bỏ qua ô trống
            btn = QPushButton(norm)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.style_button(btn, b_type)
            if norm != shift:
                self.shiftable_buttons[btn] = (norm, shift)
            btn.clicked.connect(lambda checked, b=btn: self.on_button_clicked(b))
            btn.setMinimumHeight(45) 
            
            # Ô dấu '=' chiếm 2 cột cho đẹp
            if norm == "=": grid.addWidget(btn, r, c, 1, 2)
            else: grid.addWidget(btn, r, c)
            
        main_layout.addLayout(grid)
        self.lbl_display.setFocus()

    def create_button(self, text, color, bg, width):
        btn = QPushButton(text)
        btn.setFixedSize(width, 30)
        btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        btn.setStyleSheet(f"QPushButton {{ color: {color}; background-color: {bg}; border-radius: 10px; font-weight: bold; font-size: 11px; }} QPushButton:hover {{ background-color: {color}; color: black; }}")
        return btn

    def style_button(self, btn, btn_type):
        """Bổ sung hiệu ứng HOVER mạnh mẽ"""
        base = "QPushButton { border-radius: 12px; font-family: 'Inter'; font-weight: bold; "
        if btn_type == "num": style = base + "background-color: #1e1e2d; color: #ffffff; font-size: 16px; } QPushButton:hover { background-color: #3b3b54; }"
        elif btn_type == "op": style = base + "background-color: #2a2a40; color: #a78bfa; font-size: 20px; } QPushButton:hover { background-color: #8b5cf6; color: white; }"
        elif btn_type == "func": style = base + "background-color: #151520; color: #c4b5fd; font-size: 14px; } QPushButton:hover { background-color: #4c1d95; color: white; }"
        elif btn_type == "comb": style = base + "background-color: #151520; color: #60a5fa; font-size: 16px; } QPushButton:hover { background-color: #2563eb; color: white; }"
        elif btn_type == "action": style = base + "background-color: rgba(239, 68, 68, 0.1); color: #ef4444; font-size: 14px;} QPushButton:hover { background-color: #ef4444; color: white; }"
        elif btn_type == "equals": style = base + "background-color: #6d28d9; color: #ffffff; font-size: 20px; } QPushButton:hover { background-color: #a855f7; }"
        elif btn_type == "yellow_btn": style = base + "background-color: rgba(245, 158, 11, 0.15); color: #f59e0b; font-size: 14px;} QPushButton:hover { background-color: #f59e0b; color: black; }"
        # ----------------------------------
        btn.setStyleSheet(style)

    def toggle_shift(self):
        self.is_shift = not self.is_shift
        self.btn_shift.setStyleSheet(f"QPushButton {{ color: #f59e0b; background-color: {'rgba(245, 158, 11, 0.5)' if self.is_shift else 'rgba(245, 158, 11, 0.15)'}; border-radius: 10px; font-weight: bold; }}")
        for btn, (norm, shift) in self.shiftable_buttons.items():
            btn.setText(shift if self.is_shift else norm)

    def toggle_angle(self):
        self.is_degree = not self.is_degree
        self.btn_angle.setText("DEG" if self.is_degree else "RAD")
        self.evaluate_requested.emit("TOGGLE_ANGLE")

    def on_button_clicked(self, btn):
        text = btn.text()
        cur = self.lbl_display.text()
        pos = self.lbl_display.cursorPosition()

        if text == "S-D":
            self.evaluate_requested.emit("S-D")
            return
            
        if text == "AC":
            self.lbl_display.setText("") # Đổi thành chuỗi rỗng
            self.lbl_expression.setText("")
            self.just_evaluated = False
            return
            
        elif text == "DEL":
            if self.just_evaluated:
                self.lbl_display.setText("") # Đổi thành chuỗi rỗng
                self.just_evaluated = False
                return
            if len(cur) > 0 and cur != "Error": # Sửa điều kiện từ > 1 thành > 0
                left_part = cur[:pos]
                deleted_len = 1
                funcs = ["arcsin(", "arccos(", "arctan(", "sin(", "cos(", "tan(", "log(", "ln(", "√(", "∛("]
                for f in funcs:
                    if left_part.endswith(f):
                        deleted_len = len(f)
                        break
                new_text = cur[:pos - deleted_len] + cur[pos:]
                self.lbl_display.setText(new_text if new_text else "") # Đổi thành chuỗi rỗng
                self.lbl_display.setCursorPosition(max(0, pos - deleted_len))
            else:
                self.lbl_display.setText("") # Đổi thành chuỗi rỗng
            return
            
        elif text == "=":
            if not cur: return # Tránh lỗi bấm '=' khi màn hình trống
            self.evaluate_requested.emit(cur)
            self.just_evaluated = True
            return

        # Tính năng nối tiếp Ans
        if self.just_evaluated:
            self.just_evaluated = False
            if text in ["+", "−", "×", "÷", "^", "x²", "ℂ", "ℙ", "!"]:
                self.lbl_display.setText("Ans")
                cur = "Ans"
                pos = 3
            else:
                self.lbl_display.setText("") # Đổi thành chuỗi rỗng
                cur = ""
                pos = 0

        insert_text = text
        if text == "x²":
            insert_text = "²"
        elif text in ["sin", "cos", "tan", "log", "ln", "arcsin", "arccos", "arctan", "√", "∛"]:
            insert_text += "("
            
        # Sửa điều kiện để nhận diện màn hình trống ""
        if (cur == "" or cur == "Error") and text != ".":
            self.lbl_display.setText(insert_text)
        else:
            self.lbl_display.setText(cur[:pos] + insert_text + cur[pos:])
            self.lbl_display.setCursorPosition(pos + len(insert_text))

        self.lbl_display.setFocus()