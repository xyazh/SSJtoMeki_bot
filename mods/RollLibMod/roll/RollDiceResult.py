from dataclasses import dataclass
from typing import Iterator
from itertools import islice
from .Comparator import Comparator


@dataclass
class RollDiceResult:
    values: tuple[int | float | complex]
    outsum: int | float | complex = 0
    outlen: int = 0
    limit: int = 10

    def __getitem__(self, index: int) -> int | float | complex:
        total_len = len(self.values) + self.outlen
        if index < 0:
            index += total_len
        if not 0 <= index < total_len:
            raise IndexError("Index out of range")
        if index < len(self.values):
            return self.values[index]
        if self.outlen == 0:
            raise IndexError("Index out of range")
        avg = self.outsum / self.outlen
        if isinstance(avg, float) and avg.is_integer():
            avg = int(avg)
        return avg

    def __iter__(self) -> Iterator[int | float | complex]:
        yield from self.values
        if self.outlen:
            avg = self.outsum / self.outlen
            if isinstance(avg, float) and avg.is_integer():
                avg = int(avg)
            for _ in range(self.outlen):
                yield avg

    def __len__(self) -> int:
        return len(self.values) + self.outlen

    def __str__(self) -> str:
        limit = self.limit
        length = len(self)
        if length > limit:
            items = list(islice(self, limit))
            return f"RollResult<{', '.join(map(str, items))}, ...>"
        return f"RollResult<{', '.join(map(str, self))}>"

    def __repr__(self):
        return self.__str__()

    def toStr(self) -> str:
        limit = self.limit
        length = len(self)
        if length > limit:
            items = list(islice(self, limit))
            return f"{', '.join(map(str, items))}, ..."
        return f"{', '.join(map(str, self))}"

    def max(self) -> int | float | complex:
        values = (Comparator(i) for i in self.values)
        if self.outlen == 0:
            return max(values).value
        return max(max(values), Comparator(self.outsum / self.outlen)).value

    def min(self) -> int | float | complex:
        values = (Comparator(i) for i in self.values)
        if self.outlen == 0:
            return min(values).value
        return min(min(values), Comparator(self.outsum / self.outlen)).value

    def sum(self) -> int | float | complex:
        return sum(self.values) + self.outsum

    def avg(self) -> int | float | complex:
        return self.sum() / (len(self.values) + self.outlen)

    def count(self, a: int | float | complex, b: int | float | complex) -> list[int | float | complex]:
        a = Comparator(a)
        b = Comparator(b)
        return [i for i in self.values if a <= Comparator(i) <= b]
