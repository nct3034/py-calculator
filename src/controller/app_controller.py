from src.view.main_window import MainWindow
from src.model.expression_parser import ExpressionParser
from src.model.calculus import Calculus
from src.model.memory_manager import MemoryManager
from fractions import Fraction
import math

class AppController:
    def __init__(self):
        self.main_window = MainWindow()
        self.parser = ExpressionParser()
        self.calculus = Calculus()
        self.memory = MemoryManager()
        
        self.setup_connections()
        
    def setup_connections(self):
        # Kết nối thanh Menu Sidebar
        self.main_window.btn_menu_standard.clicked.connect(lambda: self.change_page(0, "Standard"))
        self.main_window.btn_menu_scientific.clicked.connect(lambda: self.change_page(1, "Scientific"))
        
        # Tín hiệu tính toán từ Scientific
        self.main_window.page_scientific.evaluate_requested.connect(self.process_scientific)

    def change_page(self, index, title):
        self.main_window.stack.setCurrentIndex(index)
        self.main_window.lbl_title.setText(title)
        self.main_window.toggle_sidebar() # Tự động đóng sidebar sau khi chọn
        
    def process_scientific(self, expression):
        ui = self.main_window.page_scientific
        
        if expression == "TOGGLE_ANGLE":
            self.parser.math.is_degree = not self.parser.math.is_degree
            return
            
        if expression == "S-D":
            current_text = ui.lbl_display.text()
            try:
                if '/' in current_text:
                    parts = current_text.split('/')
                    res = float(parts[0]) / float(parts[1])
                    ui.lbl_display.setText(str(round(res, 10)))
                else:
                    frac = Fraction(float(current_text)).limit_denominator(1000000)
                    ui.lbl_display.setText(f"{frac.numerator}/{frac.denominator}")
            except Exception:
                pass
            return

        # TÍNH TOÁN BÌNH THƯỜNG
        ui.lbl_expression.setText(expression + " =")
        try:
            result = self.evaluate_string(expression)
            self.memory.save_calculation(expression, result)
            ui.lbl_display.setText(str(result))
        except Exception as e:
            ui.lbl_display.setText("Error")

    def evaluate_string(self, expr: str):
        expr = expr.replace('×', '*').replace('÷', '/').replace('−', '-')
        expr = expr.replace('π', str(math.pi)).replace('e', str(math.e))
        expr = expr.replace('²', '^2')

        if 'Ans' in expr:
            expr = expr.replace('Ans', str(self.memory.get_ans()))
                
        # Xử lý Tổ hợp và Chỉnh hợp (Ép về số nguyên int)
        if 'ℂ' in expr:
            parts = expr.split('ℂ')
            # Ép kiểu int cho kết quả
            return int(math.comb(int(float(parts[0])), int(float(parts[1]))))
        if 'ℙ' in expr:
            parts = expr.split('ℙ')
            # Ép kiểu int cho kết quả
            return int(math.perm(int(float(parts[0])), int(float(parts[1]))))

        result = self.parser.evaluate(expr)
        
        if isinstance(result, float):
            result = round(result, 10)
            if result.is_integer():
                result = int(result) 
                
        return result

    def run(self):
        self.main_window.show()