from dataclasses import dataclass
from typing import Iterator, Tuple

MSG = ["大成功", "极难成功", "困难成功", "普通成功", "失败", "大失败"]


@dataclass
class RollDiceResult:
    level: int
    value: int | float | complex

    @property
    def msg(self) -> str:
        if 0 <= self.level < len(MSG):
            return MSG[self.level]
        return ""

    def __getitem__(self, index: int) -> int | str:
        return (self.value, self.level, self.msg)[index]

    def __iter__(self) -> Iterator[Tuple[int, int, str]]:
        yield self.value
        yield self.level
        yield self.msg

    def __len__(self) -> int:
        return 3

    def __str__(self) -> str:
        return f"RollResult<level: {self.level},value: {self.value}"
