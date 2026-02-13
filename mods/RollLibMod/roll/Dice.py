import math
from .tools.RandomGen import RandomGen
from .RollResult import RollResult


class Dice:
    def __init__(self):
        self.rand: RandomGen = RandomGen()

    def dInt(self, count: int, faces: int) -> RollResult:
        max_count = 1000
        out_count = 0
        flag = count > max_count
        if flag:
            out_count = count - max_count
            count = max_count
        base_number = math.floor(out_count * (1 + faces) / 2)
        result = tuple(self.rand.nextInt(1, faces) for _ in range(count))
        number = sum(result)
        return RollResult(-1, number+base_number, result, not flag)

    def dFloat(self, count: float, faces: float) -> RollResult:
        result = count * faces / 2
        return RollResult(-1, result, (result,), True)

    def dComplex(self, count: complex, faces: complex) -> RollResult:
        counti = 0
        facesi = 0
        if isinstance(count, complex):
            counti = count.imag
            count = count.real
        if isinstance(faces, complex):
            facesi = faces.imag
            faces = faces.real
        result = count * faces / 2
        resulti = counti * facesi / 2
        result = result + resulti * 1j
        return RollResult(-1, result, (result,), True)

    def d(self, count: int | float | complex, faces: int | float | complex) -> RollResult | None:
        if isinstance(count, complex) or isinstance(faces, complex):
            return self.dComplex(count, faces)
        elif isinstance(count, float) or isinstance(faces, float):
            return self.dFloat(count, faces)
        elif isinstance(count, int) and isinstance(faces, int):
            return self.dInt(count, faces)
        else:
            return None
