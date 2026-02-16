import random
import time
from typing import Iterable, TypeVar, Callable, Any
_T = TypeVar("_T")


class RandomGen:
    def __init__(self, seed=time.time()):
        self.seed = seed
        self.rand = random.Random(seed)

    def nextInt(self, a: int, b: int) -> int:
        return self.rand.randint(a, b)

    def nextFloat(self,scal = 1) -> float:
        return self.rand.random() * scal

    def nextBool(self) -> bool:
        return self.rand.randint(0, 1) == 0

    def nextBytes(self, n: int) -> bytes:
        return self.rand.randbytes(n)
    
    def nextComplex(self,scal_real = 1,scal_imag = 1) -> complex:
        return self.rand.random() * scal_real + self.rand.random() * 1j * scal_imag

    def choice(self, *args: object) -> object:
        return self.rand.choice(args)

    def randListFromI(self, len, ran: Iterable[_T] = range(10)) -> list[_T]:
        return [self.choice(*ran) for _ in range(len)]
    
    def gauss(self, mu, sigma):
        return self.rand.gauss(mu, sigma)

    def randListFronF(self, len, fuc: Callable[[Any], _T] = random.random, args: tuple[Any] = None) -> list[_T]:
        if args is None:
            return [fuc() for _ in range(len)]
        return [fuc(*args) for _ in range(len)]

    def bestRandomGauss(self, mu: float, sigma: float, n: float):
        """
        生成范围大小为n的高斯分布随机数
        """
        lower = mu - n
        upper = mu + n
        return self.bestRandomGaussRange(mu, sigma, lower, upper)

    def bestRandomGaussRange(self, mu: float, sigma: float, lower: float, upper: float):
        """
        生成在[lower, upper]范围内的高斯分布随机数
        """
        r = self.gauss(mu, sigma)
        lower, upper = min(lower, upper), max(lower, upper)
        while r < lower or r > upper:
            r = self.gauss(mu, sigma)
        return r

    def randomSplitInt(self, n: int, m: int, l: int) -> list[int]:
        """
        随机分割一个整数 
        """
        l = int(l)
        m = int(m)
        n = int(n)
        if n/m >= l:
            result = [l] * m
        else:
            result = [0] * m
            for _ in range(n):
                index = self.rand.randint(0, m-1)
                while True:
                    if result[index] + 1 <= l:
                        result[index] += 1
                        break
                    else:
                        index = int((index + 1) % m)
        return result


if __name__ == "__main__":
    r = RandomGen()
    print(r.randListFromI(10))
