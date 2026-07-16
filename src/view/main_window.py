from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont

from src.view.standard_calc import StandardCalc
from src.view.scientific_calc import ScientificCalc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Casio Pro - MVC Architecture")
        self.setFixedSize(400, 650)
        self.setStyleSheet("background-color: #12121a; color: white;")
        
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- 1. SIDEBAR (THANH ĐIỀU HƯỚNG ẨN/HIỆN) ---
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(0) 
        self.sidebar.setStyleSheet("QFrame { background-color: #1e1e2d; border-right: 1px solid #2a2a40; }")
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)
        
        lbl_calc = QLabel("Calculator")
        lbl_calc.setStyleSheet("font-weight: bold; font-size: 14px; color: #a78bfa; margin-top: 10px;")
        
        self.btn_menu_standard = self.create_menu_button("Standard")
        self.btn_menu_scientific = self.create_menu_button("Scientific")
        self.btn_menu_calculus = self.create_menu_button("Calculus")
        self.btn_menu_base = self.create_menu_button("Base converter")
        self.btn_menu_logic = self.create_menu_button("Logic - Relational math")
        self.btn_menu_statistic = self.create_menu_button("Statistic")
        
        sidebar_layout.addWidget(lbl_calc)
        sidebar_layout.addWidget(self.btn_menu_standard)
        sidebar_layout.addWidget(self.btn_menu_scientific)
        sidebar_layout.addWidget(self.btn_menu_calculus)
        sidebar_layout.addWidget(self.btn_menu_base)
        sidebar_layout.addWidget(self.btn_menu_logic)
        sidebar_layout.addWidget(self.btn_menu_statistic)
        sidebar_layout.addStretch()

        # --- 2. KHU VỰC NỘI DUNG CHÍNH ---
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        topbar_layout = QHBoxLayout()
        self.btn_hamburger = QPushButton("≡")
        self.btn_hamburger.setFixedSize(40, 40)
        self.btn_hamburger.setStyleSheet("""
            QPushButton { background: transparent; color: white; font-size: 24px; border: none; border-radius: 8px; }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); }
        """)
        self.btn_hamburger.clicked.connect(self.toggle_sidebar)
        
        self.lbl_title = QLabel("Standard")
        self.lbl_title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        
        topbar_layout.addWidget(self.btn_hamburger)
        topbar_layout.addWidget(self.lbl_title)
        topbar_layout.addStretch()
        
        # --- 3. KHỞI TẠO CÁC TRANG MÁY TÍNH ---
        self.stack = QStackedWidget()
        self.page_standard = StandardCalc()
        self.page_scientific = ScientificCalc()
        
        # Tạo trang "Coming Soon" rỗng
        self.page_coming_soon = QWidget()
        coming_soon_layout = QVBoxLayout(self.page_coming_soon)
        lbl_coming_soon = QLabel("Coming soon...")
        lbl_coming_soon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_coming_soon.setStyleSheet("color: rgba(255, 255, 255, 0.2); font-size: 28px; font-weight: bold; font-family: 'Inter';")
        coming_soon_layout.addWidget(lbl_coming_soon)
        
        self.stack.addWidget(self.page_standard)
        self.stack.addWidget(self.page_scientific)
        self.stack.addWidget(self.page_coming_soon) # Thêm vào danh sách các trang
        
        content_layout.addLayout(topbar_layout)
        content_layout.addWidget(self.stack)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_widget)

        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)

    def create_menu_button(self, text):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                text-align: left; padding: 10px; font-size: 14px; background: transparent;
                border: none; border-radius: 8px; color: white;
            }
            QPushButton:hover { background-color: rgba(167, 139, 250, 0.2); color: #a78bfa; }
        """)
        return btn

    def toggle_sidebar(self):
        width = self.sidebar.width()
        if width == 0:
            self.animation.setStartValue(0)
            self.animation.setEndValue(220)
        else:
            self.animation.setStartValue(220)
            self.animation.setEndValue(0)
        self.animation.start()