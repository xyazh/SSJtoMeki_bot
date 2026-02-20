import re
import random
from .RollHelper import RollHelper
from .Dice import Dice

class ExpressionError(Exception):
    pass


class Expression:
    def __init__(self, expression: str):
        self.operators = {"?": 0, "+": 1, "-": 1,
                          "*": 2, "/": 2, "^": 3,
                          "D": 4, "d": 4}
        self.expression = self.replace(expression)
        self.dice = Dice()

    def _foramtValue(self, value):
        return RollHelper.foramtValue(value)

    def replace(self, s: str) -> str:
        s = s.replace("（", "(")
        s = s.replace("）", ")")
        s = s.replace("【", "(")
        s = s.replace("】", ")")
        s = s.replace("{", "(")
        s = s.replace("}", ")")
        s = s.replace("[", "(")
        s = s.replace("]", ")")
        s = s.replace("(-", "(0-")
        return s

    def toRpn(self, right_associative=None) -> list[str | complex | float | int]:
        precedence = self.operators
        tokens = re.findall(r"[-+*/^Ddij()\?]|\d+\.?\d*", self.expression)
        if right_associative is None:
            right_associative = set()
        operator_stack = []
        output_queue = []
        for token in tokens:
            if RollHelper.isNumber(token):
                token = float(token)
                if token.is_integer():
                    token = int(token)
                output_queue.append(token)
            elif token in ("i", "j"):
                output_queue.append(complex(0, 1))
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()
            else:
                while (
                    operator_stack
                    and operator_stack[-1] != "("
                    and (
                        (token not in right_associative and
                         precedence[operator_stack[-1]] >= precedence[token])
                        or
                        (token in right_associative and
                         precedence[operator_stack[-1]] > precedence[token])
                    )
                ):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
        while operator_stack:
            if operator_stack[-1] == "(":
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        return output_queue

    def count(self, output_queue, trace:bool=True) -> tuple[complex | float | int, list[tuple[str]] | None]:
        operand_stack = []
        steps = []
        for token in output_queue:
            if isinstance(token, (float, int, complex)):
                operand_stack.append(
                    (token, str(token if token == token else token)))
            else:
                if token in ["D", "d"]:
                    n_val, n_str = operand_stack.pop()
                    m_val, m_str = operand_stack.pop()
                    rolls = self.dice.d(m_val, n_val)
                    total = rolls.sum()
                    expr_str = f"({m_str})d{n_str}"
                    if trace:
                        steps.append(
                            (expr_str,
                             f"{expr_str}={RollHelper.foramtValue(total)}[{expr_str}={rolls.toStr(sep='+')}]")
                        )
                    operand_stack.append((total, str(total)))
                else:
                    b_val, b_str = operand_stack.pop()
                    a_val, a_str = operand_stack.pop()
                    if token == "+":
                        result = a_val + b_val
                    elif token == "-":
                        result = a_val - b_val
                    elif token == "*":
                        result = a_val * b_val
                    elif token == "/":
                        result = a_val / b_val
                    elif token == "^":
                        result = a_val ** b_val
                    expr_str = f"{a_str}{token}{b_str}"
                    operand_stack.append((result, expr_str))
        final_val, final_expr = operand_stack.pop()
        if trace:
            return final_val, steps
        return final_val, None

    def eval(self, trace:bool=True) -> tuple[complex | float | int, list[dict[str, str]] | None]:
        try:
            return self.count(self.toRpn(),trace)
        except (IndexError, SyntaxError):
            raise ExpressionError("Invalid expression syntax") from None
        except ZeroDivisionError:
            raise ExpressionError("Division by zero") from None
        except OverflowError:
            raise ExpressionError("Number too large") from None
        except Exception as e:
            raise ExpressionError(f"Unexpected error: {e}") from e
