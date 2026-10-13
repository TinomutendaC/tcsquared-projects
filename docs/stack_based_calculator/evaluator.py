"""
evaluator.py
------------
Group 6 - Expression Evaluator (Stack-Based Calculator)
CUITM205 Mini Project

This module implements the two core ALGORITHMS of the project:

    1. Shunting-Yard Algorithm  -> converts a normal ("infix")
       mathematical expression into postfix (Reverse Polish)
       notation, correctly handling operator precedence,
       associativity and parentheses. Uses a Stack for operators
       and a Queue for the output token stream.

    2. Postfix Evaluation Algorithm -> evaluates a postfix
       expression using a Stack of operands.

Together with data_structures.py (Stack, Queue) this satisfies the
assignment requirement of at least TWO data structures and at least
TWO algorithms.

The module is deliberately independent of the GUI (gui.py) so it can
be tested/reused on its own -- this is the "modular programming"
requirement in practice.
"""

import re
from data_structures import Stack, Queue


class ExpressionError(Exception):
    """Raised for any invalid expression (bad syntax, mismatched
    parentheses, division by zero, unknown token, etc.)."""
    pass


# Operator precedence: higher number = binds tighter.
PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3,
}

# '^' is right-associative in standard maths convention; the rest are
# left-associative.
RIGHT_ASSOCIATIVE = {"^"}

TOKEN_PATTERN = re.compile(r"\d+\.\d+|\d+|[+\-*/%^()]")


def tokenize(expression):
    """
    Convert a raw expression string into a list of tokens
    (numbers, operators, parentheses).

    Also performs basic input validation: rejects empty input and
    any character that is not a digit, a decimal point, a
    recognised operator, or a parenthesis.
    """
    if expression is None or expression.strip() == "":
        raise ExpressionError("Expression is empty.")

    # Strip whitespace so tokens can be matched cleanly.
    cleaned = expression.replace(" ", "")

    tokens = []
    pos = 0
    while pos < len(cleaned):
        match = TOKEN_PATTERN.match(cleaned, pos)
        if not match:
            raise ExpressionError(
                f"Invalid character '{cleaned[pos]}' in expression."
            )
        tokens.append(match.group())
        pos = match.end()

    if not tokens:
        raise ExpressionError("No valid tokens found in expression.")

    _handle_unary_minus(tokens)
    return tokens


def _handle_unary_minus(tokens):
    """
    Rewrite unary '-' (e.g. the leading minus in '-5+3' or '(-5+3)')
    as a binary subtraction from zero, so the rest of the algorithm
    only ever has to deal with binary operators.
    Modifies the token list in place.
    """
    i = 0
    while i < len(tokens):
        if tokens[i] == "-":
            is_start = i == 0
            prev_is_operator_or_open = (
                i > 0 and (tokens[i - 1] in PRECEDENCE or tokens[i - 1] == "(")
            )
            if is_start or prev_is_operator_or_open:
                tokens.insert(i, "0")
                i += 1
        i += 1


def infix_to_postfix(tokens):
    """
    ALGORITHM 1: Shunting-Yard Algorithm.

    Converts a list of infix tokens into a Queue of postfix tokens,
    using a Stack to hold operators temporarily.
    """
    operator_stack = Stack()
    output_queue = Queue()

    for token in tokens:
        if _is_number(token):
            output_queue.enqueue(token)

        elif token in PRECEDENCE:
            while (
                not operator_stack.is_empty()
                and operator_stack.peek() != "("
                and (
                    PRECEDENCE[operator_stack.peek()] > PRECEDENCE[token]
                    or (
                        PRECEDENCE[operator_stack.peek()] == PRECEDENCE[token]
                        and token not in RIGHT_ASSOCIATIVE
                    )
                )
            ):
                output_queue.enqueue(operator_stack.pop())
            operator_stack.push(token)

        elif token == "(":
            operator_stack.push(token)

        elif token == ")":
            found_matching = False
            while not operator_stack.is_empty():
                top = operator_stack.pop()
                if top == "(":
                    found_matching = True
                    break
                output_queue.enqueue(top)
            if not found_matching:
                raise ExpressionError("Mismatched parentheses.")

        else:
            raise ExpressionError(f"Unknown token '{token}'.")

    while not operator_stack.is_empty():
        top = operator_stack.pop()
        if top == "(":
            raise ExpressionError("Mismatched parentheses.")
        output_queue.enqueue(top)

    return output_queue


def evaluate_postfix(postfix_queue):
    """
    ALGORITHM 2: Postfix (Reverse Polish Notation) Evaluation.

    Evaluates a Queue of postfix tokens using a Stack of operands.
    """
    operand_stack = Stack()

    for token in postfix_queue.to_list():
        if _is_number(token):
            operand_stack.push(float(token))
        else:
            if operand_stack.size() < 2:
                raise ExpressionError("Invalid expression: not enough operands.")
            right = operand_stack.pop()
            left = operand_stack.pop()
            operand_stack.push(_apply_operator(token, left, right))

    if operand_stack.size() != 1:
        raise ExpressionError("Invalid expression: too many operands.")

    return operand_stack.pop()


def _apply_operator(operator, left, right):
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        if right == 0:
            raise ExpressionError("Division by zero.")
        return left / right
    if operator == "%":
        if right == 0:
            raise ExpressionError("Division by zero (modulo).")
        return left % right
    if operator == "^":
        return left ** right
    raise ExpressionError(f"Unsupported operator '{operator}'.")


def _is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def evaluate_expression(expression):
    """
    Convenience wrapper tying both algorithms together:
    infix string -> tokens -> postfix (Shunting-Yard) -> result.

    Returns (result, postfix_string) so the GUI can optionally show
    the postfix form as well as the final answer.
    """
    tokens = tokenize(expression)
    postfix_queue = infix_to_postfix(tokens)
    postfix_tokens = postfix_queue.to_list()
    result = evaluate_postfix(postfix_queue)
    return result, " ".join(postfix_tokens)
