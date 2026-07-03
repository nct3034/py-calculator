# 🧮 Scientific Python Calculator

A versatile, multi-functional calculator application built with Python, featuring a complete graphical user interface (GUI). The project strictly follows the MVC (Model-View-Controller) architecture to ensure the code remains clean, scalable, and easy to maintain.

## 🌟 Features

- **Basic Mathematics:** Standard algebraic operations with full support for complex numbers.
- **Base Conversion & Logic:** Convert between Binary, Decimal, and Hexadecimal bases. Full support for bitwise and Boolean logic operations.
- **Equation Solver:** Quickly solve quadratic (2nd degree) and cubic (3rd degree) equations, as well as inequalities.
- **Advanced Math (SymPy):** Calculus operations including derivatives and integrals, plus probability and statistics functions.
- **Memory Management:** Store, retrieve, and manage custom values using variable keys (A, B, C, etc.).

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **UI/UX:** PyQt6 / PySide6
- **Math Processing:** `SymPy` (Symbolic mathematics), `NumPy`
- **Architecture:** MVC (Model - View - Controller)

## 🚀 Installation

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/nct3034/py-calculator.git](https://github.com/nct3034/py-calculator.git)
   cd py-calculator
   ```

2. **Virtual Environment and Dependencies**

- Create a Virtual Environment

```bash
   python -m venv venv
```

- Activate the Environment (window)

```bash
   venv\Scripts\activate
```

- Install the Dependencies

```bash
   pip install -r requirements.txt
```

3. **Running and Testing command**

- Running the application

```bash
   python main.py
```

- Testing

```bash
   python -m unittest discover -s tests -v
```
