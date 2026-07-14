import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from src.ui.standard_calc import StandardCalc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        
        self.setFixedSize(340, 560) 
        
        self.setStyleSheet("background-color: #0b0b13;") 
        
        self.standard_calc = StandardCalc()
        self.setCentralWidget(self.standard_calc)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())