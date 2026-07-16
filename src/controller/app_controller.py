from src.view.main_window import MainWindow
from src.model.expression_parser import ExpressionParser
from src.model.calculus import Calculus
from src.model.memory_manager import MemoryManager
import math
from fractions import Fraction

class AppController:
    def __init__(self):
        # 1. Khởi tạo Giao diện
        self.main_window = MainWindow()
        
        # 2. Khởi tạo các Model
        self.parser = ExpressionParser()
        self.calculus = Calculus()
        self.memory = MemoryManager() # Module quản lý bộ nhớ mới
        
        # 3. Móc nối tín hiệu
        self.setup_connections()
        
    def setup_connections(self):
        self.main_window.page_scientific.evaluate_requested.connect(self.process_scientific)
        
    def process_scientific(self, expression):
        ui = self.main_window.page_scientific
        
        # XỬ LÝ CHUYỂN ĐỔI RAD/DEG
        if expression == "TOGGLE_ANGLE":
            self.parser.math.is_degree = not self.parser.math.is_degree
            return

        # XỬ LÝ S-D: Chuyển đổi Phân số <-> Thập phân
        if expression == "S-D":
            current_text = ui.lbl_display.text()
            try:
                if '/' in current_text:
                    # Đang là phân số -> Đổi sang thập phân
                    parts = current_text.split('/')
                    res = float(parts[0]) / float(parts[1])
                    ui.lbl_display.setText(str(round(res, 10)))
                else:
                    # Đang là số thực -> Đổi sang phân số (loại trừ các sai số cực nhỏ)
                    frac = Fraction(float(current_text)).limit_denominator(1000000)
                    ui.lbl_display.setText(f"{frac.numerator}/{frac.denominator}")
            except Exception:
                pass
            return

        # XỬ LÝ TÍNH TOÁN BÌNH THƯỜNG
        ui.lbl_expression.setText(expression + " =")
        try:
            result = self.evaluate_string(expression)
            
            # Lưu lịch sử và cập nhật giá trị Ans tự động thông qua MemoryManager
            self.memory.save_calculation(expression, result)
            
            ui.lbl_display.setText(str(result))
        except Exception as e:
            ui.lbl_display.setText("Error")

    def evaluate_string(self, expr: str) -> float:
        # Chuẩn hóa toán tử UI sang toán tử chuẩn
        expr = expr.replace('×', '*').replace('÷', '/').replace('−', '-')
        
        # CẤP SỐ THỰC CHO HẰNG SỐ pi VÀ e
        expr = expr.replace('π', str(math.pi)).replace('e', str(math.e))

        # 1. Lấy biến Ans từ MemoryManager
        if 'Ans' in expr:
            expr = expr.replace('Ans', str(self.memory.get_ans()))
        
        # 2. Lấy các biến lưu trữ (A, B, C, x...) từ MemoryManager
        for var_name in self.memory.variables.keys():
            if var_name in expr:
                val = self.memory.recall_variable(var_name)
                expr = expr.replace(var_name, str(val))
                
        # 3. Xử lý Tổ hợp và Chỉnh hợp
        if 'ℂ' in expr:
            parts = expr.split('ℂ')
            return float(math.comb(int(float(parts[0])), int(float(parts[1]))))
        if 'ℙ' in expr:
            parts = expr.split('ℙ')
            return float(math.perm(int(float(parts[0])), int(float(parts[1]))))

        # 4. Xử lý Giải tích
        if expr.startswith("d/dx("):
            inner_expr = expr[5:-1]
            parts = inner_expr.split(',')
            if len(parts) == 2:
                return self.calculus.calculate_derivative_at(parts[0], parts[1])
            else:
                raise ValueError("Syntax Error")
                
        elif expr.startswith("∫("):
            inner_expr = expr[2:-1] 
            parts = inner_expr.split(',')
            if len(parts) == 3:
                return self.calculus.calculate_definite_integral(parts[0], parts[1], parts[2])
            else:
                raise ValueError("Syntax Error")
                
        # 5. Đưa biểu thức còn lại vào Parser để xử lý ngoặc và lượng giác
        result = self.parser.evaluate(expr)
        
        # Xử lý làm tròn số thập phân để tránh lỗi Float Precision của Python
        if isinstance(result, float):
            result = round(result, 10)
            if result.is_integer():
                result = int(result) 
                
        return result

    def run(self):
        self.main_window.show()