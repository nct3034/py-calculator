import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QStackedWidget, QLabel)
from PyQt6.QtCore import Qt

# Import giao diện StandardCalc (Các máy tính khác sẽ import sau)
from src.ui.standard_calc import StandardCalc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python React-Style Calculator")
        
        self.setFixedSize(360, 620) 
        self.setStyleSheet("background-color: #0b0b13;") 
        
        # Tạo canvas chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- 1. THANH ĐIỀU HƯỚNG (NAVIGATION BAR) ---
        nav_bar = QWidget()
        nav_bar.setStyleSheet("background-color: #1a1a28; border-bottom: 1px solid rgba(109,40,217,0.2);")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        
        # Tạo nút bấm chuyển trang
        self.btn_standard = self.create_nav_button("Standard", active=True)
        self.btn_scientific = self.create_nav_button("Scientific")
        self.btn_solver = self.create_nav_button("Solver")
        self.btn_base = self.create_nav_button("Programmer")
        self.btn_statistic = self.create_nav_button("Statistic")
        
        nav_layout.addWidget(self.btn_standard)
        nav_layout.addWidget(self.btn_scientific)
        nav_layout.addWidget(self.btn_solver)
        nav_layout.addWidget(self.btn_base)
        nav_layout.addWidget(self.btn_statistic)
        
        main_layout.addWidget(nav_bar)
        
        # --- 2. BỘ CHUYỂN TRANG (QSTACKEDWIDGET) ---
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        # Trang 0: Máy tính Standard đã hoàn thiện
        self.page_standard = StandardCalc()
        
        # Các trang 1, 2, 3: Tạm thời để màn hình trống chờ phát triển
        self.page_scientific = self.create_placeholder("This feature is comming soon!")
        self.page_solver = self.create_placeholder("This feature is comming soon!")
        self.page_base = self.create_placeholder("This feature is comming soon!")
        self.page_statistic = self.create_placeholder("This feature is comming soon!")
        
        # Đưa tất cả các trang vào Stack
        self.stack.addWidget(self.page_standard)   
        self.stack.addWidget(self.page_scientific) 
        self.stack.addWidget(self.page_solver)     
        self.stack.addWidget(self.page_base)     
        self.stack.addWidget(self.page_statistic)  
        
        # --- 3. GẮN TÍN HIỆU CLICK NÚT ---
        self.btn_standard.clicked.connect(lambda: self.switch_page(0, self.btn_standard))
        self.btn_scientific.clicked.connect(lambda: self.switch_page(1, self.btn_scientific))
        self.btn_solver.clicked.connect(lambda: self.switch_page(2, self.btn_solver))
        self.btn_base.clicked.connect(lambda: self.switch_page(3, self.btn_base))
        self.btn_statistic.clicked.connect(lambda: self.switch_page(4, self.btn_statistic))

    # --- CÁC HÀM HỖ TRỢ GIAO DIỆN ---
    def create_placeholder(self, text):
        """Tạo một màn hình trống để giữ chỗ"""
        label = QLabel(text)
        label.setStyleSheet("color: rgba(167,139,250,0.5); font-family: 'JetBrains Mono'; font-size: 16px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def create_nav_button(self, text, active=False):
        """Tạo nút điều hướng với style dựa theo React Figma"""
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        color = "#c4b5fd" if active else "rgba(255,255,255,0.3)"
        bg = "rgba(109,40,217,0.35)" if active else "transparent"
        border = "1px solid rgba(109,40,217,0.35)" if active else "1px solid transparent"
        
        btn.setStyleSheet(f"""
            QPushButton {{
                color: {color};
                background-color: {bg};
                border: {border};
                border-radius: 8px;
                padding: 8px 4px;
                font-size: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(109,40,217,0.15);
            }}
        """)
        return btn

    def switch_page(self, index, active_btn):
        """Chuyển trang và đổi màu nút đang được chọn"""
        # 1. Đổi trang hiển thị
        self.stack.setCurrentIndex(index)
        
        # 2. Làm mờ toàn bộ các nút
        buttons = [self.btn_standard, self.btn_scientific, self.btn_solver, self.btn_base, self.btn_statistic]
        for btn in buttons:
            btn.setStyleSheet("""
                QPushButton {
                    color: rgba(255,255,255,0.3);
                    background-color: transparent;
                    border: 1px solid transparent;
                    border-radius: 8px;
                    padding: 8px 4px;
                    font-size: 11px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(109,40,217,0.15);
                }
            """)
            
        # 3. Làm sáng nút được bấm
        active_btn.setStyleSheet("""
            QPushButton {
                color: #c4b5fd;
                background-color: rgba(109,40,217,0.35);
                border: 1px solid rgba(109,40,217,0.35);
                border-radius: 8px;
                padding: 8px 4px;
                font-size: 11px;
                font-weight: bold;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())