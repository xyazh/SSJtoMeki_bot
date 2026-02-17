from .tools.Dice import Dice
from .result.RollResult import RollResult,RAResult
from .result.DiceResult import DiceResult
from .tools.Expression import Expression


class Roll:
    def __init__(self):
        self.dice = Dice()

    def r(self, exp_s: str, rule: bool = True) -> RollResult:
        exp = Expression(exp_s)
        exp_result = exp.eval()
        result = RollResult(exp_result[0], exp_s, exp_result[1])
        if rule:
            result.checkRaw()
        else:
            result.checkCus()
        return result

    def ra(self, attr_name: str, attr_val: int | float | complex, count: int = 1, rule: bool = True):
        values = self.dice.dInt(count, 100)
        return RAResult(values, attr_name, attr_val, rule)
