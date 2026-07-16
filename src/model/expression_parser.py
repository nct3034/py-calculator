import re
from src.model.scientific_math import ScientificMath
from src.model.statistic import Statistics  # Import class Statistics của bạn

class ExpressionParser:
    def __init__(self):
        self.math = ScientificMath()
        self.stat = Statistics()  # Khởi tạo instance của Statistics
        
        # Định nghĩa độ ưu tiên toán tử
        self.precedence = {
            '+': 1, '−': 1, '-': 1,
            '×': 2, '*': 2, '÷': 2, '/': 2,
            '^': 3, 'ℂ': 3, 'ℙ': 3
        }
        
        # Danh sách các hàm số hỗ trợ
        self.functions = {
            'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan',
            'log', 'ln', 'sqrt', 'cbrt', 'abs'
        }

    def tokenize(self, expression: str) -> list:
        # Xóa các khoảng trắng dư thừa
        expr = expression.replace(" ", "")
        
        # Regex nhận diện: số thập phân | chữ cái (tên hàm) | các ký tự toán học (bao gồm cả !, ℂ, ℙ)
        pattern = r"(\d+\.?\d*|[a-zA-Z]+|[+\-−×*÷/^()!ℂℙ])"
        tokens = re.findall(pattern, expr)
        return tokens
    
    def to_postfix(self, tokens: list) -> list:
        output = []
        stack = []
        
        for token in tokens:
            if re.match(r"^\d+\.?\d*$", token):
                output.append(float(token))
            elif token == '!':
                if not stack: raise ValueError("Syntax error")
                a = stack.pop()
                
                # Kiểm tra xem a có phải là số nguyên không (ví dụ: 5.0 là hợp lệ, 5.2 thì không)
                if not float(a).is_integer():
                    raise ValueError("Domain Error: Factorial requires an integer")
                stack.append(float(self.stat.factorial(int(a))))
            elif token in self.functions or token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Invalid close parentheses")
                stack.pop()
                if stack and stack[-1] in self.functions:
                    output.append(stack.pop())
                    
            # Xử lý toán tử
            elif token in self.precedence:
                while (stack and stack[-1] != '(' and 
                       stack[-1] in self.precedence and 
                       self.precedence[stack[-1]] >= self.precedence[token]):
                    output.append(stack.pop())
                stack.append(token)
                
        if '(' in stack:
            raise ValueError("Invalid open parentheses")
        
        while stack:
            output.append(stack.pop())
            
        return output
    
    def evaluate_postfix(self, postfix: list) -> float:
        stack = []
        
        for token in postfix:
            if isinstance(token, float):
                stack.append(token)
            
            # --- ÁP DỤNG CLASS STATISTICS CHO GIAI THỪA ---
            elif token == '!':
                if not stack: raise ValueError("Syntax error")
                a = stack.pop()
                stack.append(float(self.stat.factorial(int(a))))
            
            # Xử lý Hàm số lượng giác/logarit
            elif token in self.functions:
                if not stack: raise ValueError("Syntax error")
                a = stack.pop()
                
                if token == 'sin': stack.append(self.math.sin(a))
                elif token == 'cos': stack.append(self.math.cos(a))
                elif token == 'tan': stack.append(self.math.tan(a))
                elif token == 'arcsin': stack.append(self.math.arcsin(a))
                elif token == 'arccos': stack.append(self.math.arccos(a))
                elif token == 'arctan': stack.append(self.math.arctan(a))
                elif token == 'log': stack.append(self.math.log10(a))
                elif token == 'ln': stack.append(self.math.ln(a))
                elif token == 'sqrt': stack.append(self.math.sqrt(a))
                elif token == 'cbrt': stack.append(self.math.cbrt(a))
                elif token == 'abs': stack.append(self.math.absolute(a))
            
            # Xử lý Toán tử 2 ngôi
            elif token in self.precedence:
                if len(stack) < 2: raise ValueError("Insufficient operands")
                b = stack.pop()
                a = stack.pop()
                
                if token in ('+',): stack.append(a + b)
                elif token in ('-', '−'): stack.append(a - b)
                elif token in ('*', '×'): stack.append(a * b)
                elif token in ('/', '÷'): 
                    if b == 0: raise ZeroDivisionError("Division by zero")
                    stack.append(a / b)
                elif token == '^': stack.append(self.math.power(a, b))
                
                # --- ÁP DỤNG CLASS STATISTICS CHO TỔ HỢP / CHỈNH HỢP ---
                elif token == 'ℂ': stack.append(float(self.stat.combinations(int(a), int(b))))
                elif token == 'ℙ': stack.append(float(self.stat.permutations(int(a), int(b))))
                
        if len(stack) != 1:
            raise ValueError("Invalid expression")
            
        return stack[0]

    def evaluate(self, expression: str) -> float:
        tokens = self.tokenize(expression)
        postfix = self.to_postfix(tokens)
        return self.evaluate_postfix(postfix)