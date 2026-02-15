import math
from .tools.RandomGen import RandomGen
from .RollDiceResult import RollDiceResult


class Dice:
    def __init__(self):
        self.max_count = 100
        self.rand: RandomGen = RandomGen()

    def setRandomGen(self, rand: RandomGen):
        self.rand = rand

    def dInt(self, count: int, faces: int) -> RollDiceResult:
        max_count = self.max_count
        outsum = 0
        outlen = 0
        if count > max_count:
            outlen = count - max_count
            count = max_count
            mu = outlen * (1 + faces) / 2
            sigma = math.sqrt(outlen * (faces**2 - 1) / 12)
            outsum = round(self.rand.gauss(mu, sigma))
            min_sum = outlen * 1
            max_sum = outlen * faces
            outsum = max(min_sum, min(outsum, max_sum))
        result = tuple(self.rand.nextInt(1, faces) for _ in range(count))
        return RollDiceResult(result, outsum, outlen)

    def dFloat(self, count: float, faces: float) -> RollDiceResult:
        max_count = self.max_count
        outsum = 0.0
        outlen = 0
        if count > max_count:
            outlen = count - max_count
            count = max_count
            mu = outlen * (faces / 2)
            sigma = math.sqrt(outlen * (faces**2 / 12))
            outsum = self.rand.gauss(mu, sigma)
            min_sum = 0.0
            max_sum = outlen * faces
            outsum = max(min_sum, min(outsum, max_sum))
        result = tuple(self.rand.nextFloat() * faces for _ in range(count))
        return RollDiceResult(result, outsum, outlen)

    def dComplex(self, count: complex, faces: complex) -> RollDiceResult:
        max_count = self.max_count
        outsum = 0.0 + 0.0j
        outlen = 0
        if count > max_count:
            outlen = count - max_count
            count = max_count
            mu = outlen * (faces / 2)
            sigma = math.sqrt(outlen * (faces**2 / 12))
            outsum_i = self.rand.gauss(mu, sigma)
            min_sum_i = 0.0
            max_sum_i = outlen * faces
            outsum_i = max(min_sum_i, min(outsum_i, max_sum_i))
            outsum = self.rand.gauss(mu, sigma)
            min_sum = 0.0
            max_sum = outlen * faces
            outsum = max(min_sum, min(outsum, max_sum))
            outsum = outsum + outsum_i * 1j
        result = tuple(self.rand.nextComplex * faces for _ in range(count))
        return RollDiceResult(result, outsum, outlen)

    def d(self, count: int | float | complex, faces: int | float | complex) -> RollDiceResult | None:
        if isinstance(count, complex) or isinstance(faces, complex):
            return self.dComplex(count, faces)
        elif isinstance(count, float) or isinstance(faces, float):
            return self.dFloat(count, faces)
        elif isinstance(count, int) and isinstance(faces, int):
            return self.dInt(count, faces)
        else:
            return None
