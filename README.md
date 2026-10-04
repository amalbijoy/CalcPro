# `CalcPro` (Advanced Calculator):

A feature-rich, colorful command-line calculator with multiple operation modes, scientific functions, and an intuitive user interface.

## Features:

### Advanced Scientific Functions:
- **Trigonometric**: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`
- **Mathematical**: `sqrt`, `cbrt`, `factorial`, `abs`, `ceil`, `floor`, `round`
- **Logarithmic**: `log`, `log10`, `log2`, `exp`
- **Constants**: `pi`, `e`

### Multiple Operation Modes:
- **Basic Mode** - Simple numbered operations (addition, subtraction, multiplication, division, exponentiation).
- **Expression Mode** - Direct mathematical expression input with complex calculations.
- **Scientific Mode** - Advanced functions and constants with comprehensive help system.

### User Interface Features:
- **Colorized terminal output** with beautiful ASCII art banners.
- **Color-coded results** (green for results, red for errors, cyan for prompts).
- **Clean input/output formatting** for enhanced readability.
- **Structured operation menus** for easy navigation.

### Smart Features:
- **Calculation history** with storage and viewing capabilities.
- **Settings management**: degree/radian mode toggle, scientific notation toggle.
- **Enhanced error handling** with descriptive error messages.
- **Complex expression evaluation** with safety checks.
- **Parentheses balancing validation** for mathematical expressions.
- **Demo mode** to showcase calculator capabilities.
- **Built-in help system** with function descriptions and examples.
- **Screen clearing** and history management.

### Safety & Validation:
- AST-based expression validation instead of unrestricted evaluation
- Expression length and AST complexity limits to prevent pathological inputs
- Input validation for numeric values.
- Expression syntax validation.
- Safe evaluation using restricted eval with allowed functions only.
- Comprehensive error handling for division by zero, invalid inputs, and syntax errors.

## Installation:

### Prerequisites:
- Python 3.6 (or) higher.
- Terminal/Command Prompt with ANSI color support (most modern terminals).

### Setup:
1. **Download the calculator**:
   ```bash
   # Clone or download the CalcPro.py file.
   wget -L https://raw.githubusercontent.com/amalbijoy/CalcPro/main/CalcPro.py
   # or simply copy the CalcPro.py file to your desired directory.
   ```

2. **Make it executable** (optional, for Unix-based systems):
   ```bash
   chmod +x CalcPro.py
   ```

## Usage:

### Starting the Calculator:
```bash
python CalcPro.py
```
or
```bash
python3 CalcPro.py
```

### Basic Operations:
Choose from numbered options:
- `[1]` Addition
- `[2]` Subtraction  
- `[3]` Multiplication
- `[4]` Division
- `[5]` Exponentiation

### Expression Examples:
```bash
# Basic arithmetic
Calculator> 3 + 5 * 2

# Scientific functions
Calculator> sqrt(16) + 2^3

# Trigonometric (respects angle mode)
Calculator> sin(90) + cos(0)

# Logarithmic
Calculator> log10(100) + log(e)

# Complex expressions
Calculator> (2 + 3) * sqrt(25) / factorial(3)
```

### Available Commands:
| Command | Description                       |
| ------- | --------------------------------- |
| `1-5`   | Basic arithmetic operations       |
| `6`     | Enter Basic Mode                  |
| `7`     | Enter Expression Mode             |
| `8`     | Enter Scientific Mode             |
| `h`     | View calculation history          |
| `c`     | Clear calculation history         |
| `cl`    | Clear screen                      |
| `?`     | Show help and available functions |
| `m`     | Toggle degree/radian mode         |
| `s`     | Toggle scientific notation        |
| `demo`  | Run demonstration mode            |
| `x`     | Exit calculator                   |

### Scientific Functions Reference:
```bash
# Trigonometric functions:
sin(angle), cos(angle), tan(angle),
asin(x), acos(x), atan(x),
sinh(x), cosh(x), tanh(x)

# Mathematical functions:  
sqrt(x), cbrt(x), factorial(n),
abs(x), ceil(x), floor(x), round(x)

# Logarithmic functions:
log(x), log10(x), log2(x), exp(x)

# Constants:
pi, e

# Power operations:
pow(x,y), x^y, x**y
```

## Configuration:

### Angle Mode:
- **Radians** (default): For mathematical calculations
- **Degrees**: For practical applications
- Toggle with `m` command

### Scientific Notation:
- **OFF** (default): Standard decimal notation
- **ON**: Scientific notation (e.g., 1.234567e+02)
- Toggle with `s` command

## Examples:

### Basic Calculations:
```bash
Calculator> 1
# Enter First Number: 15
# Enter Second Number: 25
# Result: 15.0 + 25.0 = 40

Calculator> 2 + 3 * 4
# Result: 14
```

### Scientific Calculations:
```bash
Calculator> sqrt(144)
# Result: 12

Calculator> sin(90)  # (in degree mode)
# Result: 1

Calculator> log10(1000)
# Result: 3

Calculator> factorial(5)
# Result: 120
```

### Complex Expressions:
```bash
Calculator> (sqrt(16) + 2^3) / factorial(3)
# Result: 2

Calculator> pi * 2
# Result: 6.283185307179586
```

## Error Handling:

The calculator provides comprehensive error handling for:
- **Invalid numeric input**: Clear error messages for non-numeric values.
- **Division by zero**: Prevents mathematical errors.
- **Syntax errors**: Validates mathematical expression syntax.
- **Unmatched parentheses**: Ensures proper expression structure.
- **Unknown functions**: Helpful suggestions for valid function names.
- **Factorial of negative numbers**: Mathematical domain validation.

## Visual Features:

- **Colorful ASCII art banner** on startup
- **Color-coded output**:
  - **Green**: Results and success messages.
  - **Red**: Error messages.
  - **Blue**: Section headers.
  - **Yellow**: Input prompts and warnings.
  - **Cyan**: Options and commands.

## Quick Start Guide:

1. **Start the calculator**: `python CalcPro.py`
2. **Try a simple calculation**: Enter `2 + 3`
3. **Explore scientific functions**: Enter `sqrt(25)`
4. **Check history**: Enter `h`
5. **Get help**: Enter `?`
6. **Try demo mode**: Enter `demo`

## Contributing:

This calculator is designed to be extensible. You can easily add new functions by:

1. Adding the function to the `allowed_names` dictionary in `evaluate_expression()`.
2. Adding documentation to the `suggestions` dictionary.
3. Implementing any custom mathematical functions as needed.

## License:

This project is open source and available under standard GNU General Public License v3.0 licensing terms.

## Support:

If you encounter any issues:
1. Check that you're using Python 3.6 (or) higher.
2. Ensure your terminal supports ANSI color codes.
3. Verify that mathematical expressions follow standard notation.
4. Use the `?` command for function help
5. Try the `demo` command to see example usage

---

**Happy Calculating!**
