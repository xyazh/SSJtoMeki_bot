from .Dice import Dice
from .result.RollCheckResult import RollCheckResult
from .result.RollDiceResult import RollDiceResult


class Roll:
    def __init__(self):
        self.dice = Dice()

    def r(self, count=1, faces=100) -> RollDiceResult:
        return self.dice.d(count, faces)
