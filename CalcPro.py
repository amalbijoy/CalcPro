import re
import math
import os
import sys

# Global configuration
angle_mode = 'radians'
sci_mode = False
calc_history = []

# Color constants
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Function suggestions and help
suggestions = {
    "sin": "sin(angle) — sine of angle",
    "cos": "cos(angle) — cosine of angle",
    "tan": "tan(angle) — tangent of angle",
    "asin": "asin(x) — arc sine of x",
    "acos": "acos(x) — arc cosine of x",
    "atan": "atan(x) — arc tangent of x",
    "sinh": "sinh(x) — hyperbolic sine",
    "cosh": "cosh(x) — hyperbolic cosine",
    "tanh": "tanh(x) — hyperbolic tangent",
    "sqrt": "sqrt(x) — square root of x",
    "cbrt": "cbrt(x) — cube root of x (x**(1/3))",
    "log": "log(x) — natural logarithm",
    "log10": "log10(x) — base-10 logarithm",
    "log2": "log2(x) — base-2 logarithm",
    "exp": "exp(x) — e raised to power x",
    "pi": "pi — constant π (3.14159...)",
    "e": "e — Euler's constant (2.71828...)",
    "pow": "pow(x,y) — x raised to power y",
    "abs": "abs(x) — absolute value of x",
    "ceil": "ceil(x) — ceiling function",
    "floor": "floor(x) — floor function",
    "round": "round(x) — round to nearest integer",
    "^": "a ^ b — exponentiation (same as a**b)",
    "factorial": "factorial(n) — factorial of n"
}

def print_banner():
    """Display the main calculator banner with options."""
    print(f"""
{YELLOW}█▀██████▀█▄▀▀█▀▀▀▀█▀▀▀▄▀█▀▀▄▀█▄▀▀▄▀█▀▀▄▀▀▄▀██▀██▀███████{RESET}
{YELLOW}█▀███████████████▀▀██████████▄▀▀▄▀████████▄▄████████████{RESET}
{CYAN}
░█████╗░░█████╗░██╗░░░░░░█████╗░██████╗░██████╗░░█████╗░
██╔══██╗██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔══██╗██╔══██╗
██║░░╚═╝███████║██║░░░░░██║░░╚═╝██████╔╝██████╔╝██║░░██║
██║░░██╗██╔══██║██║░░░░░██║░░██╗██╔═══╝░██╔══██╗██║░░██║
╚█████╔╝██║░░██║███████╗╚█████╔╝██║░░░░░██║░░██║╚█████╔╝
░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░░░░╚═╝░░╚═╝░╚════╝░
{RESET}
{YELLOW}█▀███████████████▀▀█▀▄█▀███▀▀▀█▀▄█▀█▀█▄▀▄▀█▄▀▀█▀▀▀▀█▀▄▄▀{RESET}
{YELLOW}█▀█████████████▀▀█▀▄▀▄▀█▀▀▀▀███████████▀▀▀█▀▄█▀▄████████{RESET}
{BLUE}# OPERATION MODES:{RESET}
{CYAN}[1] Addition [2] Subtraction [3] Multiplication [4] Division [5] Exponentiation
[6] Basic Mode [7] Expression Mode [8] Scientific Mode{RESET}
{BLUE}# ADVANCED OPTIONS:{RESET}
{CYAN}[h] History [c] Clear History [?] Help/Functions [m] Toggle Deg/Rad [s] Sci-Notation
[cl] Clear Screen [demo] Demo Mode [x] Exit{RESET}
{GREEN}# Expression Examples:{RESET} 3+5*2, 2^3, sqrt(16), sin(90), log(100), pi*2
{GREEN}Enter expressions directly or use numbered options above^^{RESET}
""")

def get_input():
    """Get two numbers from user with error handling."""
    try:
        a = float(input(f"{YELLOW}# Enter First Number: {RESET}"))
        b = float(input(f"{YELLOW}# Enter Second Number: {RESET}"))
        return a, b
    except ValueError:
        print(f"{RED}# Invalid input. Please enter numeric values!{RESET}")
        return None, None

def wrap_trig(fn):
    """Wrap trigonometric functions to handle degree/radian mode."""
    return lambda x: fn(math.radians(x)) if angle_mode == 'degrees' else fn(x)

def format_result(value):
    """Format result based on scientific notation setting."""
    if sci_mode:
        return f"{value:.6e}"
    elif isinstance(value, float) and value.is_integer():
        return str(int(value))
    else:
        return str(value)

def is_parentheses_balanced(expr):
    """Check if parentheses are balanced in expression."""
    stack = []
    for char in expr:
        if char == '(': stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return not stack

def factorial(n):
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("# Factorial not defined for negative numbers!")
    return math.factorial(int(n))

def cbrt(x):
    """Calculate cube root of x."""
    return x ** (1/3) if x >= 0 else -((-x) ** (1/3))

def safe_eval(expr, allowed_names, max_depth=50, max_nodes=200):
    """Evaluate a validated mathematical expression without changing process-global limits."""
    import ast

    if len(expr) > 500:
        raise ValueError("Expression is too long.")

    allowed_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Load, ast.Call, ast.Name,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.USub, ast.UAdd,
        ast.FloorDiv, ast.Constant, ast.Num
    )

    class SafeEval(ast.NodeVisitor):
        def __init__(self):
            self.depth = 0
            self.nodes = 0

        def visit(self, node):
            self.nodes += 1
            if self.nodes > max_nodes:
                raise ValueError("Expression is too complex.")
            self.depth += 1
            if self.depth > max_depth:
                raise ValueError("Expression is too deeply nested.")
            try:
                if not isinstance(node, allowed_nodes):
                    raise ValueError(f"Unsafe node: {type(node).__name__}")
                return super().visit(node)
            finally:
                self.depth -= 1

        def visit_Name(self, node):
            if node.id not in allowed_names:
                raise NameError(f"Unknown function or constant: {node.id}")

        def visit_Constant(self, node):
            if not isinstance(node.value, (int, float)):
                raise ValueError("Only numeric constants are allowed.")

        def visit_Call(self, node):
            if not isinstance(node.func, ast.Name) or node.func.id not in allowed_names:
                raise NameError(f"Unknown function: {getattr(node.func, 'id', None)}")
            if len(node.args) > 2 or node.keywords:
                raise ValueError("Only simple positional function arguments are allowed.")
            self.generic_visit(node)

    tree = ast.parse(expr, mode="eval")
    SafeEval().visit(tree)

    return eval(
        compile(tree, filename="<ast>", mode="eval"),
        {"__builtins__": None},
        allowed_names,
    )

def evaluate_expression(expr):
    """Evaluate mathematical expression safely with extended functions."""
    # Pre-process 'x' to '*' for validation
    validation_expr = expr.replace('x', '*')
    
    # Tightened regex - only allow safe mathematical characters
    if not re.match(r'^[0-9a-zA-Z+\-*/.^() ]*$', validation_expr):
        print(f"{RED}# Error: Invalid characters in expression!{RESET}")
        return
    
    if not is_parentheses_balanced(expr):
        print(f"{RED}# Error: Unmatched parentheses in expression!{RESET}")
        return
    
    try:
        # Replace common operators
        expr = expr.replace('x', '*').replace('^', '**')
        
        # Extended allowed functions
        allowed_names = {
            # Basic math
            "sqrt": math.sqrt, "pow": pow, "abs": abs,
            "ceil": math.ceil, "floor": math.floor, "round": round,
            "factorial": factorial, "cbrt": cbrt,
            # Trigonometric functions
            "sin": wrap_trig(math.sin), "cos": wrap_trig(math.cos), "tan": wrap_trig(math.tan),
            "asin": wrap_trig(math.asin), "acos": wrap_trig(math.acos), "atan": wrap_trig(math.atan),
            "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
            # Logarithmic and exponential
            "log": math.log, "log10": math.log10, "log2": math.log2, "exp": math.exp,
            # Constants
            "pi": math.pi, "e": math.e
        }
        
        result = safe_eval(expr, allowed_names)
        display = format_result(result)
        print(f"{GREEN}# Result: {display}{RESET}")
        calc_history.append(f"{expr} = {display}")
    
    except ZeroDivisionError:
        print(f"{RED}# Error: Cannot divide by zero!{RESET}")
    except ValueError as e:
        print(f"{RED}# Error: {e}{RESET}")
    except NameError as e:
        print(f"{RED}# Error: Unknown function or variable! {e}{RESET}")
    except SyntaxError:
        print(f"{RED}# Error: Invalid syntax in expression!{RESET}")
    except RecursionError:
        print(f"{RED}# Error: Expression too complex (recursion depth exceeded)!{RESET}")
    except Exception as e:
        print(f"{RED}# Error: {e}{RESET}")

def basic_operation(op_name, a, b, operation):
    """Perform basic operation with formatting."""
    try:
        result = operation()
        print(f"{GREEN}# Result: {a} {op_name} {b} = {format_result(result)}{RESET}")
        calc_history.append(f"{a} {op_name} {b} = {format_result(result)}")
    except ZeroDivisionError:
        print(f"{RED}# Error: Cannot divide by zero!{RESET}")
    except Exception as e:
        print(f"{RED}# Error: {e}{RESET}")
def demo_mode():
    """Run demonstration of calculator features."""
    print(f"{CYAN}=== CALCULATOR DEMO MODE ==={RESET}")
    demo_expressions = [
        "2 + 3 * 4",
        "sqrt(16) + 2^3",
        "sin(90) + cos(0)" if angle_mode == 'degrees' else "sin(pi/2) + cos(0)",
        "log10(100) + log(e)",
        "factorial(5) / 10",
        "pi * 2"
    ]
    for expr in demo_expressions:
        print(f"{YELLOW}# Demo: {expr}{RESET}")
        evaluate_expression(expr)
        print()
def handle_command(cmd):
    """Handle user commands and operations."""
    global angle_mode, sci_mode
    if cmd == '1': # Addition
        a, b = get_input()
        if a is not None:
            basic_operation('+', a, b, lambda: a + b)
    elif cmd == '2': # Subtraction
        a, b = get_input()
        if a is not None:
            basic_operation('-', a, b, lambda: a - b)
    elif cmd == '3': # Multiplication
        a, b = get_input()
        if a is not None:
            basic_operation('*', a, b, lambda: a * b)
    elif cmd == '4': # Division
        a, b = get_input()
        if a is not None:
            basic_operation('/', a, b, lambda: a / b)
    elif cmd == '5': # Exponentiation
        a, b = get_input()
        if a is not None:
            basic_operation('^', a, b, lambda: a ** b)
    elif cmd == '6': # Basic Mode
        print(f"{CYAN}=== BASIC CALCULATOR MODE ==={RESET}")
        print("# Select operation: [1]+ [2]- [3]* [4]/ [5]^ [back] Return :")
        while True:
            sub_cmd = input(f"{YELLOW}# Basic: {RESET}").strip()
            if sub_cmd == 'back':
                break
            elif sub_cmd in ['1', '2', '3', '4', '5']:
                handle_command(sub_cmd)
            else:
                print(f"{RED}# Invalid option. Use 1-5 or 'back'{RESET}")
    elif cmd == '7': # Expression Mode
        print(f"{CYAN}=== EXPRESSION CALCULATOR MODE ==={RESET}")
        print("# Enter mathematical expressions (type 'back' to return):")
        while True:
            expr = input(f"{YELLOW}Expression>> {RESET}").strip()
            if expr.lower() == 'back':
                break
            evaluate_expression(expr)
    elif cmd == '8': # Scientific Mode
        print(f"{CYAN}=== SCIENTIFIC CALCULATOR MODE ==={RESET}")
        print("# Advanced functions available. Type '?' for help or 'back' to return:")
        while True:
            expr = input(f"{YELLOW}Scientific>>> {RESET}").strip()
            if expr.lower() == 'back':
                break
            elif expr == '?':
                print(f"{GREEN}# Scientific Functions:{RESET}")
                for k, v in suggestions.items():
                    print(f"{CYAN}- {v}{RESET}")
            else:
                evaluate_expression(expr)
    elif cmd == 'h': # History
        if not calc_history:
            print(f"{YELLOW}# No calculation history yet.{RESET}")
        else:
            print(f"{GREEN}=== CALCULATION HISTORY ==={RESET}")
            for i, h in enumerate(calc_history, 1):
                print(f"{CYAN}{i:2d}. {h}{RESET}")
    elif cmd == 'c': # Clear History
        calc_history.clear()
        print(f"{GREEN}# History cleared.{RESET}")
    elif cmd == 'cl': # Clear Screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
    elif cmd == '?': # Help
        print(f"{GREEN}=== AVAILABLE FUNCTIONS ==={RESET}")
        for k, v in suggestions.items():
            print(f"{CYAN}- {v}{RESET}")
    elif cmd == 'm': # Toggle Angle Mode
        angle_mode = 'degrees' if angle_mode == 'radians' else 'radians'
        print(f"{GREEN}# Angle mode set to: {YELLOW}{angle_mode}{RESET}")
    elif cmd == 's': # Toggle Scientific Notation
        sci_mode = not sci_mode
        print(f"{GREEN}# Scientific notation: {YELLOW}{'ON' if sci_mode else 'OFF'}{RESET}")
    elif cmd == 'demo': # Demo Mode
        demo_mode()
    elif cmd == 'x': # Exit
        print(f"{CYAN}# Exiting Calculator. See you next time. Goodbye! :){RESET}")
        return False
    else: # Treat as expression
        evaluate_expression(cmd)
    return True
def main():
    """Main calculator function."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    print(f"{GREEN}# Calculator started successfully! All features available.{RESET}")
    print(f"{YELLOW}# Current settings: Angle mode = {angle_mode}, Scientific notation = {'ON' if sci_mode else 'OFF'}{RESET}\n")
    while True:
        try:
            cmd = input(f"{BLUE}Calculator> {RESET}").strip()
            if not cmd:
                continue
            if not handle_command(cmd):
                break
        except KeyboardInterrupt:
            print(f"\n{CYAN}# Exiting Calculator. Goodbye! :){RESET}")
            break
        except Exception as e:
            print(f"{RED}# Unexpected error: {e}{RESET}")
if __name__ == '__main__':
    main()
