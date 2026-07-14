from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

class CalcButton(QPushButton):
    """Tương đương với CalcButton.tsx"""
    def __init__(self, text, variant="number", wide=False, small=False):
        super().__init__(text)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        styles = {
            "number": "background: #1e1e2c; color: #e8e8ff;",
            "operator": "background: rgba(109,40,217,0.22); color: #a78bfa; border: 1px solid rgba(109,40,217,0.28);",
            "equals": "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7c3aed, stop:1 #4338ca); color: #fff;",
            "function": "background: #14141f; color: #c4b5fd;",
            "clear": "background: #1e1e2c; color: #f87171;"
        }
        
        hover_styles = {
            "number": "background: #28283c;",
            "operator": "background: rgba(109,40,217,0.4);",
            "equals": "background: #6d28d9;", 
            "function": "background: #1c1c2a;",
            "clear": "background: #2a1e2a;"
        }

        padding = "10px" if small else "18px"
        font_size = "12px" if small else "18px"
        

        self.setStyleSheet(f"""
            QPushButton {{
                {styles.get(variant, styles["number"])}
                border-radius: 12px;
                padding: {padding};
                font-family: 'Segoe UI', sans-serif;
                font-size: {font_size};
                font-weight: bold;
            }}
            QPushButton:hover {{
                {hover_styles.get(variant, hover_styles["number"])}
            }}
            QPushButton:pressed {{
                margin-top: 2px; /* Mô phỏng hiệu ứng active:scale-[0.93] */
            }}
        """)


class CalcDisplay(QWidget):
    """Tương đương với CalcDisplay.tsx"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)
        self.setLayout(layout)
        
        # Dòng hiển thị biểu thức (expression)
        self.lbl_expression = QLabel("")
        self.lbl_expression.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lbl_expression.setStyleSheet("color: rgba(167,139,250,0.45); font-family: 'JetBrains Mono', monospace; font-size: 13px;")
        
        # Dòng hiển thị kết quả (value)[cite: 1]
        self.lbl_value = QLabel("0")
        self.lbl_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        layout.addWidget(self.lbl_expression)
        layout.addWidget(self.lbl_value)
        
        # Chạy khởi tạo font chữ ban đầu
        self.update_display("", "0")

    def update_display(self, expression, value):
        """Hàm này dùng để React (cập nhật) lại giao diện khi số liệu thay đổi"""
        self.lbl_expression.setText(expression)
        self.lbl_value.setText(value)
        
        length = len(value)
        if length <= 7:
            font_size = "52px"   
        elif length <= 11:
            font_size = "40px"   
        elif length <= 15:
            font_size = "30px"  
        else:
            font_size = "22px"   
            
        self.lbl_value.setStyleSheet(f"""
            color: #f0f0ff; 
            font-family: 'JetBrains Mono', monospace; 
            font-size: {font_size};
        """)