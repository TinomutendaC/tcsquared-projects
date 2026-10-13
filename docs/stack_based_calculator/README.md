# Group 6 – Expression Evaluator (Stack-Based Calculator)
CUITM205 – Data Structures and Algorithms – Mini Project

## What it does
A Tkinter GUI calculator that evaluates mathematical expressions
(including parentheses and correct operator precedence) using classic
stack-based algorithms instead of Python's `eval()`.

## Requirements checklist
| Requirement | How it's met |
|---|---|
| Written in Python | 100% Python 3, standard library only |
| Functional GUI | `gui.py` — Tkinter calculator UI with display, buttons, history |
| ≥ 2 data structures | `Stack` and `Queue` (`data_structures.py`) |
| ≥ 2 algorithms | Shunting-Yard (infix→postfix) and Postfix Evaluation (`evaluator.py`) |
| Modular programming | Separate modules: data structures / algorithms / GUI / entry point |
| Input validation & error handling | `ExpressionError` — empty input, invalid characters, mismatched parentheses, division by zero, malformed expressions |

## Files
- `data_structures.py` – `Stack` (LIFO) and `Queue` (FIFO), built from scratch.
- `evaluator.py` – tokenizer, unary-minus handling, Shunting-Yard algorithm, postfix evaluation, and `evaluate_expression()` convenience function.
- `gui.py` – Tkinter interface: number/operator buttons, live display, postfix trace, calculation history panel, keyboard shortcuts (Enter = `=`, Backspace, Esc = clear).
- `main.py` – entry point (`python main.py`).
- `test_evaluator.py` – standalone tests for the algorithm logic (no GUI needed): `python test_evaluator.py`.

## How the two algorithms work together
1. **Shunting-Yard Algorithm** (Dijkstra) walks the token list left to
   right. Numbers go straight to the output **Queue**. Operators are
   pushed onto an operator **Stack**, popping off any operators of
   higher-or-equal precedence first (respecting `^`'s
   right-associativity) so they land in the output queue in the
   correct order. Parentheses push/pop matching operator groups.
2. **Postfix Evaluation** then scans the resulting queue: numbers are
   pushed onto an operand **Stack**; each operator pops the top two
   operands, applies itself, and pushes the result back. The single
   value left on the stack at the end is the answer.

This mirrors exactly how a real calculator (or a compiler's
expression parser) handles precedence and parentheses without needing
nested function calls or `eval`.

## Running it
Requires Python 3 with Tkinter (included by default on Windows/most
Linux desktop installs; on some Linux distros install with
`sudo apt install python3-tk`).

```bash
python main.py
```

## Supported operators
`+  -  *  /  %  ^` (power), plus parentheses `( )` and decimal numbers.
Leading unary minus is supported, e.g. `-5+3` and `(-5+3)*2`.

## Example expressions to demo
| Expression | Result | Postfix |
|---|---|---|
| `3+4*2` | 11 | `3 4 2 * +` |
| `(1+2)*(3+4)` | 21 | `1 2 + 3 4 + *` |
| `2^3^2` | 512 | `2 3 2 ^ ^` (right-associative) |
| `10/0` | Error: Division by zero | — |
