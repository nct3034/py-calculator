import sys
from PyQt6.QtWidgets import QApplication
from src.controller.app_controller import AppController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Khởi tạo và chạy Controller
    controller = AppController()
    controller.run()
    
    sys.exit(app.exec())