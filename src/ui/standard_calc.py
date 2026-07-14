from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from .components import CalcButton, CalcDisplay

class StandardCalc(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # 1. Bố cục chính (Xếp dọc từ trên xuống)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # 2. Thêm màn hình (Đã làm ở file components)
        self.display = CalcDisplay()
        main_layout.addWidget(self.display)

        # 3. Bố cục lưới cho bàn phím
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        main_layout.addLayout(grid_layout)

        # 4. Định nghĩa các nút giống hệt file StandardCalc.tsx của bạn
        # Format: (Text, Hàng, Cột, Số hàng chiếm, Số cột chiếm, Variant)
        buttons = [
            ("AC", 0, 0, 1, 1, "clear"), ("⌫", 0, 1, 1, 1, "function"), ("%", 0, 2, 1, 1, "function"), ("÷", 0, 3, 1, 1, "operator"),
            ("7",  1, 0, 1, 1, "number"),("8", 1, 1, 1, 1, "number"),   ("9", 1, 2, 1, 1, "number"),   ("×", 1, 3, 1, 1, "operator"),
            ("4",  2, 0, 1, 1, "number"),("5", 2, 1, 1, 1, "number"),   ("6", 2, 2, 1, 1, "number"),   ("−", 2, 3, 1, 1, "operator"),
            ("1",  3, 0, 1, 1, "number"),("2", 3, 1, 1, 1, "number"),   ("3", 3, 2, 1, 1, "number"),   ("+", 3, 3, 1, 1, "operator"),
            ("0",  4, 0, 1, 2, "number"),(".", 4, 2, 1, 1, "number"),   ("=", 4, 3, 1, 1, "equals")
        ]

        # Vòng lặp để tạo và gắn nút bấm vào lưới
        for text, row, col, row_span, col_span, variant in buttons:
            is_wide = col_span > 1 
            
            btn = CalcButton(text, variant=variant, wide=is_wide)
            grid_layout.addWidget(btn, row, col, row_span, col_span)
            
            # Tạm thời: In ra terminal khi bấm nút để kiểm tra
            btn.clicked.connect(lambda checked, t=text: print(f"You click button: {t}"))