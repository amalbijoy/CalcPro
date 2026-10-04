# CalcPro

> A command-line scientific calculator with basic, expression, and scientific modes, plus guarded mathematical-expression evaluation.

## Features

- Basic arithmetic: addition, subtraction, multiplication, division, exponentiation
- Expression mode for direct mathematical input
- Scientific functions including trigonometry, logarithms, roots, hyperbolic functions, rounding, and factorial
- Degree/radian toggle for trigonometric functions
- Scientific-notation display toggle
- Calculation history
- Built-in help and demo mode
- Colorized terminal interface

## Expression syntax

Examples:

```text
3 + 5 * 2
sqrt(16) + 2^3
sin(90)
log10(1000)
pi * 2
(sqrt(16) + 2^3) / factorial(3)
```

`^` is converted to Python exponentiation for expression evaluation, and `x` is accepted as a multiplication symbol.

## Safety and validation

Expression evaluation is guarded by AST validation rather than unrestricted `eval`.

The current evaluator also applies:

- Maximum expression length: `500` characters
- Maximum AST node count: `200`
- Maximum AST nesting depth: `50`
- Numeric constants only
- Named functions/constants must come from the allowlist
- Function calls are limited to positional arguments and at most two arguments
- Python built-ins are disabled in the final evaluation environment

These controls reduce the risk of pathological or unintended expressions, but the application should still be treated as a local calculator rather than a security sandbox.

## Installation

Python 3.8+ is recommended.

Run directly:

```bash
python CalcPro.py
```

## Main commands

| Command | Action |
|---|---|
| `1`–`5` | Basic arithmetic |
| `6` | Basic mode |
| `7` | Expression mode |
| `8` | Scientific mode |
| `h` | Show history |
| `c` | Clear history |
| `cl` | Clear screen |
| `?` | Help |
| `m` | Toggle degree/radian mode |
| `s` | Toggle scientific notation |
| `demo` | Run demo |
| `x` | Exit |

## Development

The repository includes focused unit tests for the expression evaluator's safety behavior:

```bash
python -m unittest discover -s tests
```

GitHub Actions also runs the test suite.

## License

See [LICENSE](LICENSE).
