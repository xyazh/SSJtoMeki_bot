import sys
from dataclasses import dataclass
from typing import Iterator
from itertools import islice
from ..tools.RollHelper import RollHelper
from ..tools.Comparator import Comparator


@dataclass
class DiceResult:
    values: tuple[int | float | complex] | None
    outsum: int | float | complex = 0
    outlen: int = 0
    limit: int = 10

    def lenValues(self) -> int:
        if self.values is None:
            return 0
        return len(self.values)

    def __getitem__(self, index: int) -> int | float | complex:
        total_len = self.lenValues() + self.outlen
        if index < 0:
            index += total_len
        if not 0 <= index < total_len:
            raise IndexError("Index out of range")
        if index < self.lenValues():
            return self.values[index]
        if self.outlen == 0:
            raise IndexError("Index out of range")
        avg = self.outsum / self.outlen
        if isinstance(avg, float) and avg.is_integer():
            avg = int(avg)
        return avg

    def __iter__(self) -> Iterator[int | float | complex]:
        if self.values is not None:
            yield from self.values
        if self.outlen:
            avg = self.outsum / self.outlen
            if isinstance(avg, float) and avg.is_integer():
                avg = int(avg)
            for _ in range(self.outlen):
                yield avg

    def __len__(self) -> int:
        s = self.size()
        if s < sys.maxsize:
            return s
        raise OverflowError("Result len is too large, use size() instead")

    def __str__(self) -> str:
        limit = self.limit
        length = self.size()
        if length > limit:
            items = list(islice(self, limit))
            return f"RollResult[size={length}, sum={self.sum()}]<{', '.join(map(RollHelper.foramtValue, items))}, ...>"
        return f"RollResult[size={length}, sum={self.sum()}]<{', '.join(map(RollHelper.foramtValue, self))}>"

    def __repr__(self):
        return self.__str__()
    
    def toStr(self,sep:str = ", ") -> str:
        limit = self.limit
        length = self.size()
        if length == 0:
            items = [RollHelper.foramtValue(self.outsum)]
        elif length > limit:
            items = list(map(RollHelper.foramtValue,islice(self, limit)))
            items.append(RollHelper.foramtValue("..."))
        else:
            items = map(RollHelper.foramtValue,self)
        return sep.join(items)


    def size(self) -> int:
        return self.lenValues() + self.outlen

    def max(self) -> int | float | complex:
        if self.values is not None and len(self.values) > 0:
            values = (Comparator(i) for i in self.values)
            if self.outlen == 0:
                return max(values).value
            return max(max(values), Comparator(self.outsum / self.outlen)).value
        if self.outlen == 0:
            return 0
        return self.outsum / self.outlen

    def min(self) -> int | float | complex:
        if self.values is not None and len(self.values) > 0:
            values = (Comparator(i) for i in self.values)
            if self.outlen == 0:
                return min(values).value
            return min(min(values), Comparator(self.outsum / self.outlen)).value
        if self.outlen == 0:
            return 0
        return self.outsum / self.outlen

    def sum(self) -> int | float | complex:
        if self.values is None:
            return self.outsum
        return sum(self.values) + self.outsum

    def avg(self) -> int | float | complex:
        return self.sum() / (self.lenValues() + self.outlen)

    def count(self, a: int | float | complex, b: int | float | complex) -> list[int | float | complex]:
        a = Comparator(a)
        b = Comparator(b)
        return [i for i in ([] if self.values is None else self.values) if a <= Comparator(i) <= b]
