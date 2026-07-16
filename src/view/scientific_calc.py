from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal

class ScientificCalc(QWidget):
    evaluate_requested = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.is_shift = False
        self.is_sto_mode = False
        self.shiftable_buttons = {}
        
        # Thêm cờ nhận biết vừa tính toán xong
        self.just_evaluated = False 
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 20)
        main_layout.setSpacing(10)

        # --- 1. MÀN HÌNH HIỂN THỊ (Sử dụng QLineEdit để scroll ngang) ---
        self.lbl_expression = QLabel("")
        self.lbl_expression.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 14px; font-family: 'JetBrains Mono';")
        self.lbl_expression.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.lbl_display = QLineEdit("0")
        self.lbl_display.setReadOnly(True)
        self.lbl_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lbl_display.setStyleSheet("""
            QLineEdit {
                background: transparent; border: none; color: white; 
                font-size: 36px; font-family: 'JetBrains Mono'; font-weight: bold;
            }
        """)
        
        main_layout.addWidget(self.lbl_expression)
        main_layout.addWidget(self.lbl_display)
        
        # --- 2. THANH TRẠNG THÁI VÀ ĐIỀU HƯỚNG (D-PAD) ---
        status_layout = QHBoxLayout()
        
        self.btn_shift = self.create_button("SHIFT", "#f59e0b", "rgba(245, 158, 11, 0.15)", 50)
        self.btn_shift.clicked.connect(self.toggle_shift)
        
        self.btn_sto = self.create_button("STO", "#f472b6", "rgba(244, 114, 182, 0.15)", 50)
        self.btn_sto.clicked.connect(self.toggle_sto)
        
        # Thêm nút chuyển đổi DEG / RAD
        self.is_degree = True
        self.btn_angle = self.create_button("DEG", "#10b981", "rgba(16, 185, 129, 0.15)", 50)
        self.btn_angle.clicked.connect(self.toggle_angle)
        
        # Nút điều hướng (Casio cursor)
        self.btn_left = self.create_button("◀", "#a78bfa", "rgba(109,40,217,0.2)", 40)
        self.btn_left.clicked.connect(lambda: self.lbl_display.cursorBackward(False))
        
        self.btn_right = self.create_button("▶", "#a78bfa", "rgba(109,40,217,0.2)", 40)
        self.btn_right.clicked.connect(lambda: self.lbl_display.cursorForward(False))
        
        status_layout.addWidget(self.btn_shift)
        status_layout.addWidget(self.btn_sto)
        status_layout.addWidget(self.btn_angle) # Đặt nút vào thanh UI
        status_layout.addStretch()
        status_layout.addWidget(self.btn_left)
        status_layout.addWidget(self.btn_right)
        main_layout.addLayout(status_layout)

        # --- 3. BÀN PHÍM LƯỚI ---
        grid = QGridLayout()
        grid.setSpacing(8)
        
        buttons = [
            # Dòng 1: Giải tích, Tổ hợp, Phân số, Mũ (SHIFT của ^ là x²)
            (0, 0, "∫", "∫", "func"), (0, 1, "d/dx", "d/dx", "func"), (0, 2, "ℂ", "ℙ", "comb"), (0, 3, "a/b", "a/b", "func"), (0, 4, "^", "x²", "func"),
            
            # Dòng 2: Biến số
            (1, 0, "A", "A", "var"), (1, 1, "B", "B", "var"), (1, 2, "C", "C", "var"), (1, 3, "X", "X", "var"), (1, 4, "Y", "Y", "var"),
            
            # Dòng 3: Lượng giác, Logarit
            (2, 0, "sin", "arcsin", "func"), (2, 1, "cos", "arccos", "func"), (2, 2, "tan", "arctan", "func"), (2, 3, "log", "10ˣ", "func"), (2, 4, "ln", "eˣ", "func"),
            
            # Dòng 4: Ngoặc, S-D (mới), Hằng số e, Căn (thay vị trí dấu phẩy cũ)
            (3, 0, "(", "(", "func"), (3, 1, ")", ")", "func"), (3, 2, "S-D", "S-D", "func"), (3, 3, "e", "e", "func"), (3, 4, "√", "∛", "func"),
            
            # Dòng 5-6: Số và Toán tử cơ bản
            (4, 0, "7", "7", "num"), (4, 1, "8", "8", "num"), (4, 2, "9", "9", "num"), (4, 3, "DEL", "DEL", "action"), (4, 4, "AC", "AC", "action"),
            (5, 0, "4", "4", "num"), (5, 1, "5", "5", "num"), (5, 2, "6", "6", "num"), (5, 3, "×", "×", "op"), (5, 4, "÷", "÷", "op"),
            
            # Dòng 7-8: Chú ý dấu chấm (.) có SHIFT là dấu phẩy (,), và π thay cho x²
            (6, 0, "1", "1", "num"), (6, 1, "2", "2", "num"), (6, 2, "3", "3", "num"), (6, 3, "+", "+", "op"), (6, 4, "−", "−", "op"),
            (7, 0, "0", "0", "num"), (7, 1, ".", ",", "num"), (7, 2, "π", "π", "func"), (7, 3, "Ans", "Ans", "action"), (7, 4, "=", "=", "equals")
        ]

        for r, c, norm, shift, b_type in buttons:
            btn = QPushButton(norm)
            self.style_button(btn, b_type)
            if norm != shift:
                self.shiftable_buttons[btn] = (norm, shift)
            btn.clicked.connect(lambda checked, b=btn: self.on_button_clicked(b))
            
            # Đảm bảo phím vuông/tròn đều đặn
            btn.setMinimumHeight(45) 
            grid.addWidget(btn, r, c)
            
        main_layout.addLayout(grid)

    def create_button(self, text, color, bg, width):
        btn = QPushButton(text)
        btn.setFixedSize(width, 30)
        btn.setStyleSheet(f"""
            QPushButton {{ color: {color}; background-color: {bg}; border-radius: 15px; font-weight: bold; font-size: 12px; }}
        """)
        return btn

    def style_button(self, btn, btn_type):
        """Thiết kế UI bo tròn (border-radius)"""
        base = "QPushButton { border-radius: 22px; font-family: 'Inter'; font-size: 16px; font-weight: bold; "
        if btn_type == "num": style = base + "background-color: #1e1e2d; color: #ffffff; }"
        elif btn_type == "op": style = base + "background-color: #2a2a40; color: #a78bfa; font-size: 20px; }"
        elif btn_type == "func": style = base + "background-color: #151520; color: #c4b5fd; font-size: 13px; }"
        elif btn_type == "comb": style = base + "background-color: #151520; color: #60a5fa; font-size: 16px; }" # Tổ hợp màu xanh dương
        elif btn_type == "var": style = base + "background-color: #151520; color: #f472b6; font-size: 16px; }" # Biến số màu hồng
        elif btn_type == "action": style = base + "background-color: rgba(239, 68, 68, 0.1); color: #ef4444; }"
        else: style = base + "background-color: #6d28d9; color: #ffffff; font-size: 20px; }"
        btn.setStyleSheet(style)

    def toggle_shift(self):
        self.is_shift = not self.is_shift
        self.btn_shift.setStyleSheet(f"QPushButton {{ color: #f59e0b; background-color: {'rgba(245, 158, 11, 0.5)' if self.is_shift else 'rgba(245, 158, 11, 0.15)'}; border-radius: 15px; font-weight: bold; }}")
        for btn, (norm, shift) in self.shiftable_buttons.items():
            btn.setText(shift if self.is_shift else norm)

    def toggle_sto(self):
        self.is_sto_mode = not self.is_sto_mode
        self.btn_sto.setStyleSheet(f"QPushButton {{ color: #f472b6; background-color: {'rgba(244, 114, 182, 0.5)' if self.is_sto_mode else 'rgba(244, 114, 182, 0.15)'}; border-radius: 15px; font-weight: bold; }}")

    def toggle_angle(self):
        self.is_degree = not self.is_degree
        self.btn_angle.setText("DEG" if self.is_degree else "RAD")
        # Gửi tín hiệu để Controller biết và cấu hình lại Math Model
        self.evaluate_requested.emit("TOGGLE_ANGLE")

    def on_button_clicked(self, btn):
        text = btn.text()
        cur = self.lbl_display.text()
        pos = self.lbl_display.cursorPosition()

        if text == "S-D":
            self.evaluate_requested.emit("S-D")
            return
            
        if text == "AC":
            self.lbl_display.setText("0")
            self.lbl_expression.setText("")
            self.just_evaluated = False # Đặt lại trạng thái
            return
            
        elif text == "DEL":
            # Nếu vừa tính xong mà bấm DEL thì xóa trắng y như AC
            if self.just_evaluated:
                self.lbl_display.setText("0")
                self.just_evaluated = False
                return
                
            if len(cur) > 1 and cur != "Error":
                left_part = cur[:pos]
                deleted_len = 1
                funcs = ["arcsin(", "arccos(", "arctan(", "sin(", "cos(", "tan(", 
                         "log(", "ln(", "√(", "∛(", "abs(", "d/dx(", "∫("]
                for f in funcs:
                    if left_part.endswith(f):
                        deleted_len = len(f)
                        break
                new_text = cur[:pos - deleted_len] + cur[pos:]
                self.lbl_display.setText(new_text if new_text else "0")
                self.lbl_display.setCursorPosition(max(0, pos - deleted_len))
            else:
                self.lbl_display.setText("0")
            return
            
        elif text == "=":
            self.evaluate_requested.emit(cur)
            self.just_evaluated = True # Bật cờ "Đã tính xong"
            return
            
        if self.is_sto_mode and text in ["A", "B", "C", "X", "Y"]:
            self.evaluate_requested.emit(f"STO_{text}")
            self.toggle_sto()
            self.just_evaluated = True # Lưu biến xong cũng tính là 1 chu trình
            return

        # ======================================================
        # TÍNH NĂNG MỚI: TỰ ĐỘNG TIẾP NỐI "Ans" HOẶC TẠO MỚI
        # ======================================================
        if self.just_evaluated:
            self.just_evaluated = False # Tắt cờ đi cho các thao tác sau
            
            # Danh sách các toán tử nối tiếp
            if text in ["+", "−", "×", "÷", "^", "x²", "a/b", "ℂ", "ℙ"]:
                self.lbl_display.setText("Ans")
                cur = "Ans"
                pos = 3
            else:
                # Nếu bấm Số (0-9) hoặc Hàm (sin, cos, căn...) -> Xóa màn hình cũ
                self.lbl_display.setText("0")
                cur = "0"
                pos = 1
        # ======================================================

        # Tiền xử lý ký tự nhập vào
        insert_text = text
        if text in ["sin", "cos", "tan", "log", "ln", "arcsin", "arccos", "arctan", "√", "∛", "abs", "∫", "d/dx"]:
            insert_text += "("
        elif text == "a/b":
            insert_text = "/"
            
        # Nối chữ vào màn hình
        if (cur == "0" or cur == "Error") and text != ".":
            self.lbl_display.setText(insert_text)
        else:
            self.lbl_display.setText(cur[:pos] + insert_text + cur[pos:])
            self.lbl_display.setCursorPosition(pos + len(insert_text))