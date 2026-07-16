import re
from src.model.scientific_math import ScientificMath
from src.model.statistic import Statistics
from src.model.arithmetic_math import ArithmeticMath

class ExpressionParser:
    def __init__(self):
        self.math = ScientificMath()
        self.stat = Statistics()
        self.arithmetic = ArithmeticMath() # Tích hợp class mới
        
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
        
        # Regex nhận diện
        pattern = r"(\d+\.?\d*|[a-zA-Z]+|[+\-−×*÷/^()!ℂℙ])"
        raw_tokens = re.findall(pattern, expr)
        
        # --- XỬ LÝ TRIỆT ĐỂ LỖI DẤU TRỪ ÂM (UNARY MINUS) ---
        tokens = []
        for i, token in enumerate(raw_tokens):
            if token in ('-', '−'):
                # Nếu dấu trừ nằm ở đầu biểu thức, hoặc ngay sau dấu ngoặc mở '('
                if i == 0 or raw_tokens[i-1] == '(':
                    tokens.append('0') # Chèn ngầm số 0 vào để biến thành phép trừ 2 ngôi
            tokens.append(token)
            
        return tokens
    
    def to_postfix(self, tokens: list) -> list:
        output = []
        stack = []
        
        for token in tokens:
            if re.match(r"^\d+\.?\d*$", token):
                output.append(float(token))
            elif token == '!':
                output.append(token)
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
            
            elif token == '!':
                if not stack: raise ValueError("Syntax error")
                a = stack.pop()
                if not float(a).is_integer():
                    raise ValueError("Domain Error: Factorial requires an integer")
                stack.append(float(self.stat.factorial(int(a))))
            
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
            
            elif token in self.precedence:
                if len(stack) < 2: raise ValueError("Insufficient operands")
                b = stack.pop()
                a = stack.pop()
                
                # --- ÁP DỤNG CLASS ARITHMETIC MATH CHO CÁC TOÁN TỬ CƠ BẢN ---
                if token in ('+',): 
                    stack.append(float(self.arithmetic.add(a, b)))
                elif token in ('-', '−'): 
                    stack.append(float(self.arithmetic.subtract(a, b)))
                elif token in ('*', '×'): 
                    stack.append(float(self.arithmetic.multiply(a, b)))
                elif token in ('/', '÷'): 
                    stack.append(float(self.arithmetic.divide(a, b)))
                # ------------------------------------------------------------
                
                elif token == '^': stack.append(self.math.power(a, b))
                elif token == 'ℂ': stack.append(float(self.stat.combinations(int(a), int(b))))
                elif token == 'ℙ': stack.append(float(self.stat.permutations(int(a), int(b))))
                
        if len(stack) != 1:
            raise ValueError("Invalid expression")
            
        return stack[0]

    def evaluate(self, expression: str) -> float:
        tokens = self.tokenize(expression)
        postfix = self.to_postfix(tokens)
        return self.evaluate_postfix(postfix)