import re
import random
from .RollHelper import RollHelper
from .Dice import Dice

DICE = Dice()


class ExpressionError(Exception):
    pass


class Expression:
    def __init__(self, expression: str):
        self.operators = {"?": 0, "+": 1, "-": 1,
                          "*": 2, "/": 2, "^": 3,
                          "D": 4, "d": 4}
        self.expression = self.replace(expression)
        self.dice = DICE

    def _foramtValue(self, value):
        return RollHelper.formatValue(value)

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

    def count(self, output_queue, *args) -> tuple[complex | float | int, str]:
        operand_stack = []
        for token in output_queue:
            if isinstance(token, (float, int, complex)):
                operand_stack.append(
                    (token, RollHelper.formatValue(token), None))
            else:
                if token in ["D", "d"]:
                    n_val, n_str, n_op = operand_stack.pop()
                    m_val, m_str, m_op = operand_stack.pop()
                    rolls = self.dice.d(m_val, n_val)
                    total = rolls.sum()
                    left = m_str
                    right = n_str
                    if self.needParen(token, m_op, is_right=False):
                        left = f"({left})"
                    if self.needParen(token, n_op, is_right=True):
                        right = f"({right})"
                    step = f"{left}{token}{right}[{RollHelper.formatValue(total)}]"
                    operand_stack.append((total, step, "d"))
                else:
                    b_val, b_str, b_op = operand_stack.pop()
                    a_val, a_str, a_op = operand_stack.pop()
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
                    left = a_str
                    right = b_str
                    if self.needParen(token, a_op, is_right=False):
                        left = f"({left})"
                    if self.needParen(token, b_op, is_right=True):
                        right = f"({right})"
                    step = f"{left}{token}{right}"
                    operand_stack.append((result, step, token))
        final_val, step, _ = operand_stack.pop()
        return final_val, step

    def needParen(self, parent_op, child_op, is_right=False):
        if child_op is None:
            return False
        if self.operators[child_op] < self.operators[parent_op]:
            return True
        if self.operators[child_op] > self.operators[parent_op]:
            return False
        if parent_op == "^":
            return is_right
        if self.operators[child_op] == self.operators[parent_op]:
            if child_op not in ("+", "*"):
                return is_right
        return False

    def eval(self, *args) -> tuple[complex | float | int, str]:
        try:
            return self.count(self.toRpn())
        except (IndexError, SyntaxError):
            raise ExpressionError("Invalid expression syntax") from None
        except ZeroDivisionError:
            raise ExpressionError("Division by zero") from None
        except OverflowError:
            raise ExpressionError("Number too large") from None
        except Exception as e:
            raise ExpressionError(f"Unexpected error: {e}") from e
