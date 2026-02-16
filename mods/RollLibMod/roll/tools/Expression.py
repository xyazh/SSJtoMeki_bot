import re
import random
from .RollHelper import RollHelper


class Expression:
    def __init__(self, expression: str):
        self.operators = {"?": 0, "+": 1, "-": 1,
                          "*": 2, "/": 2, "^": 3,
                          "D": 4, "d": 4}
        self.expression = self.replace(expression)

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

    def toRpn(self, right_associative=None):
        precedence = self.operators
        tokens = re.findall(r"[-+*/^Ddij()\?]|\d+\.?\d*", self.expression)
        if right_associative is None:
            right_associative = set()
        operator_stack = []
        output_queue = []
        for token in tokens:
            if RollHelper.isNumber(token):
                output_queue.append(float(token))
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

    def count(self, output_queue, trace: bool = True):
        operand_stack = []
        steps = []
        for token in output_queue:
            if isinstance(token, (float, int, complex)):
                operand_stack.append(token)
            else:
                if token in ["D", "d"]:
                    n = operand_stack.pop()
                    m = operand_stack.pop()
                    result = RollHelper.d(m, n)
                    if trace:
                        steps.append(f"{m}d{n} -> {result}")
                    operand_stack.append(result)
                else:
                    b = operand_stack.pop()
                    a = operand_stack.pop() if operand_stack else None
                    if token == "+":
                        result = a + b
                    elif token == "-":
                        result = (a if a is not None else 0) - b
                    elif token == "*":
                        result = a * b
                    elif token == "/":
                        result = a / b
                    elif token == "^":
                        result = a ** b
                    elif token == "?":
                        result = random.choice((a, b))
                    if trace:
                        steps.append(f"{a} {token} {b} -> {result}")
                    operand_stack.append(result)
        final = operand_stack.pop()
        if trace:
            return final, steps
        return final

    
    def eval(self) -> complex | float | int:
        return self.count(self.toRpn())