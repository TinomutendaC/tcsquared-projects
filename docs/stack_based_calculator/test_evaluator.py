"""
test_evaluator.py
------------------
Quick sanity tests for the Shunting-Yard + Postfix-Evaluation logic.
Run with:  python test_evaluator.py
"""

from evaluator import evaluate_expression, ExpressionError

CASES = [
    ("3+4*2", 11),
    ("(1+2)*(3+4)", 21),
    ("10/2-3", 2),
    ("2^3^2", 512),        # ^ is right-associative
    ("-5+3", -2),
    ("(-5+3)*2", -4),
    ("7%3", 1),
]

ERROR_CASES = ["10/0", "((2+3)", "4+*2", ""]


def main():
    passed = 0
    for expression, expected in CASES:
        result, postfix = evaluate_expression(expression)
        ok = abs(result - expected) < 1e-9
        status = "PASS" if ok else "FAIL"
        passed += ok
        print(f"[{status}] {expression:15} -> {result} (postfix: {postfix})")

    for expression in ERROR_CASES:
        try:
            evaluate_expression(expression)
            print(f"[FAIL] {expression!r:15} -> expected an error, got a result")
        except ExpressionError as e:
            print(f"[PASS] {expression!r:15} -> correctly raised: {e}")

    print(f"\n{passed}/{len(CASES)} value tests passed.")


if __name__ == "__main__":
    main()
