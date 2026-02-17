from dataclasses import dataclass
from itertools import islice
from typing import Iterator, Tuple
from ..tools.Comparator import Comparator
from ..tools.RollHelper import RollHelper
from .DiceResult import DiceResult

MSG = ["大成功", "极难成功", "困难成功", "普通成功", "失败", "大失败"]


@dataclass
class RollResult:
    value: int | float | complex
    exp: str
    steps: list[tuple[str, str]] | None = None
    level: int = -1
    ref: int | float | complex = 80
    ref_name: str = ""

    @property
    def msg(self) -> str:
        if 0 <= self.level < len(MSG):
            return MSG[self.level]
        return ""

    def checkRaw(self):
        value = Comparator(self.value)
        if value <= Comparator(1):
            self.level = 0
        elif value <= Comparator(self.ref / 5):
            self.level = 1
        elif value <= Comparator(self.ref / 2):
            self.level = 2
        elif value <= Comparator(self.ref):
            self.level = 3
        elif self.ref < Comparator(50) and Comparator(95) < value <= Comparator(100):
            self.level = 5
        elif value <= Comparator(99):
            self.level = 4
        else:
            self.level = 5
        return self

    def checkCus(self):
        value = Comparator(self.value)
        if value <= Comparator(5):
            self.level = 0
        elif value <= Comparator(self.ref / 5):
            self.level = 1
        elif value <= Comparator(self.ref / 2):
            self.level = 2
        elif value <= Comparator(self.ref):
            self.level = 3
        elif value <= Comparator(95):
            self.level = 4
        else:
            self.level = 5
        return self

    def __getitem__(self, index: int) -> int | str:
        if index == 0:
            return self.value
        elif index == 1:
            return self.exp
        elif index == 2:
            return self.steps
        elif index == 3:
            return self.level
        elif index == 4:
            return self.msg
        elif index == 5:
            return self.ref
        elif index == 6:
            return self.ref_name
        else:
            raise IndexError("Index out of range")

    def __iter__(self) -> Iterator[Tuple[int, str, list[tuple[str, str]], int, str]]:
        yield self.value
        yield self.exp
        yield self.steps
        yield self.level
        yield self.msg
        yield self.ref
        yield self.ref_name

    def __len__(self) -> int:
        return 7

    def __str__(self) -> str:
        return f"RollResult[value={self.value}, level={self.level}, msg={self.msg}]"


@dataclass
class RAResult:
    dice_result: DiceResult
    attr_name: str
    attr_val: int | float | complex
    rule: bool = True

    @property
    def limit(self) -> int:
        return self.dice_result.limit

    def size(self) -> int:
        return self.dice_result.size()

    def rollResults(self) -> Iterator[RollResult]:
        for value in self.dice_result:
            result = RollResult(
                value, "1d100", f"(1)d100={RollHelper.foramtValue(value)}[(1)d100={RollHelper.foramtValue(value)}]",
                ref=self.attr_val, ref_name=self.attr_name)
            if self.rule:
                yield result.checkRaw()
            else:
                yield result.checkCus()

    def rollTrueResult(self) -> Iterator[RollResult]:
        for value in self.dice_result.values:
            result = RollResult(
                value, "1d100", f"(1)d100={RollHelper.foramtValue(value)}[(1)d100={RollHelper.foramtValue(value)}]",
                ref=self.attr_val, ref_name=self.attr_name)
            if self.rule:
                yield result.checkRaw()
            else:
                yield result.checkCus()

    def __str__(self) -> str:
        limit = self.limit
        length = self.size()
        if length > limit:
            items = list(islice(self.rollResults(), limit))
            result_s = (
                f"{RollHelper.foramtValue(item.value)}|{item.msg}"
                for item in items)
            return f"RAResult[size={length}]<{', '.join(result_s)}, ...>"
        items = self.rollResults()
        result_s = (
            f"{RollHelper.foramtValue(item.value)}|{item.msg}"
            for item in items)
        return f"RAResult[size={length}]<{', '.join(result_s)}>"

    def toStr(self, sep: str = ", ") -> str:
        limit = self.limit
        length = self.size()
        if length > limit:
            items = list(islice(self.rollResults(), limit))
            result_s = (
                f"{RollHelper.foramtValue(item.value)}|{item.msg}"
                for item in items)
            return f"{sep.join(result_s)}{sep}..."
        items = self.rollResults()
        result_s = (
            f"{RollHelper.foramtValue(item.value)}|{item.msg}"
            for item in items)
        return f"{sep.join(result_s)}"

    def bonus(self):
        value = self.dice_result.max()
        result = RollResult(
            value, "1d100", f"(1)d100={RollHelper.foramtValue(value)}[(1)d100={RollHelper.foramtValue(value)}]",
            ref=self.attr_val, ref_name=self.attr_name)
        if self.rule:
            return result.checkRaw()
        else:
            return result.checkCus()

    def punishment(self):
        value = self.dice_result.min()
        result = RollResult(
            value, "1d100", f"(1)d100={RollHelper.foramtValue(value)}[(1)d100={RollHelper.foramtValue(value)}]",
            ref=self.attr_val, ref_name=self.attr_name)
        if self.rule:
            return result.checkRaw()
        else:
            return result.checkCus()

    def count(self) -> list[int]:
        result = [0] * 6
        true_dresult = self.rollTrueResult()
        for item in true_dresult:
            result[item.level] += 1
        comparison = []
        for i in range(100):
            if self.rule:
                comparison.append(RollResult(
                    i+1, "", "", ref=self.attr_val).checkRaw().level)
            else:
                comparison.append(RollResult(
                    i+1, "", "", ref=self.attr_val).checkCus().level)
        outlen = self.dice_result.outlen
        quo = int(outlen // 100)
        rem = int(outlen % 100)
        allocation1 = [quo for _ in range(50)]
        allocation2 = [quo for _ in range(50)]
        offset = 0
        while rem > 0:
            allocation1[offset] += 1
            rem -= 1
            if rem <= 0:
                break
            allocation2[offset] += 1
            rem -= 1
        allocation = allocation1[::-1] + allocation2
        for i in range(100):
            result[comparison[i]] += allocation[i]
        return result
