import math
from .RandomGen import RandomGen
from ..result.DiceResult import DiceResult


class Dice:
    def __init__(self):
        self.max_count = 500
        self.rand: RandomGen = RandomGen()

    def setRandomGen(self, rand: RandomGen):
        self.rand = rand

    def dInt(self, r_count: int, r_faces: int) -> DiceResult:
        if not (isinstance(r_count, int) and isinstance(r_faces, int)):
            raise TypeError("Invalid type")
        sub = 1
        count = r_count
        faces = r_faces
        if r_count < 0:
            count = -r_count
            sub *= -1
        if r_faces < 0:
            faces = -r_faces
            sub *= -1
        max_count = self.max_count
        outsum = 0
        outlen = 0
        if count > max_count:
            outlen = count - max_count
            count = max_count
            mu = outlen * (1 + faces) / 2
            sigma = (outlen * (faces**2 - 1) / 12)**0.5
            outsum = round(self.rand.gauss(mu, sigma))
            min_sum = outlen * 1
            max_sum = outlen * faces
            outsum = max(min_sum, min(outsum, max_sum)) * sub
        result = tuple(self.rand.nextInt(1, faces) * sub for _ in range(count))
        return DiceResult(result, outsum, outlen)

    def dFloat(self, r_count: int | float, r_faces: float) -> DiceResult:
        sub = 1
        count = r_count
        faces = r_faces
        if r_count < 0:
            count = -r_count
            sub *= -1
        if r_faces < 0:
            faces = -r_faces
            sub *= -1
        if isinstance(count, int) or (isinstance(count, float) and count.is_integer()):
            count = int(count)
            max_count = self.max_count
            outsum = 0.0
            outlen = 0
            if count > max_count:
                outlen = count - max_count
                count = max_count
                mu = outlen * (faces / 2)
                sigma = (outlen * (faces**2 / 12))**0.5
                outsum = self.rand.gauss(mu, sigma)
                min_sum = 0.0
                max_sum = outlen * faces
                outsum = max(min_sum, min(outsum, max_sum)) * sub
            result = tuple(self.rand.nextFloat() * sub *
                           faces for _ in range(count))
            return DiceResult(result, outsum, outlen)
        elif isinstance(count, float):
            mu = count * (faces / 2)
            sigma = (count * (faces**2 / 12))**0.5
            outsum = self.rand.gauss(mu, sigma)
            min_sum = 0.0
            max_sum = count * faces
            outsum = max(min_sum, min(outsum, max_sum)) * sub
            return DiceResult(None, outsum)
        else:
            raise TypeError("Invalid type")

    def dComplex(self, r_count: complex | float | int, r_faces: complex) -> DiceResult:
        if not isinstance(r_faces, complex):
            r_faces = complex(r_faces)
        sub_i = 1 + 1j
        faces = r_faces.real
        faces_i = r_faces.imag
        if faces < 0:
            faces = -faces
            sub_i = -sub_i.real + 1j * sub_i.imag
        if faces_i < 0:
            faces_i = -faces_i
            sub_i = sub_i.real - 1j * sub_i.imag
        if isinstance(r_count, int) or (isinstance(r_count, float) and r_count.is_integer()):
            count = r_count
            sub = 1
            if count < 0:
                count = -r_count
                sub *= -1
            count = int(count)
            max_count = self.max_count
            outsum = 0.0
            outlen = 0
            if count > max_count:
                outlen = count - max_count
                count = max_count
                mu = outlen * (faces / 2)
                sigma = (outlen * (faces**2 / 12))**0.5
                outsum = self.rand.gauss(mu, sigma) * sub
            result = tuple(self.rand.nextComplex(
                sub_i.real * faces.real, sub_i.imag * faces.imag) * sub for _ in range(count))
            return DiceResult(result, outsum, outlen)
        elif isinstance(r_count, complex) or isinstance(r_count, float):
            count = complex(r_count)
            mu = count * (faces / 2)
            sigma = (count * (faces**2 / 12))**0.5
            outsum = self.rand.gauss(mu, sigma)
            return DiceResult(None, outsum)
        else:
            raise TypeError("Invalid type")

    def d(self, count: int | float | complex, faces: int | float | complex) -> DiceResult:
        if isinstance(count, complex) and count .imag == 0:
            count = count.real
        if isinstance(faces, complex) and faces.imag == 0:
            faces = faces.real
        if isinstance(count, float) and count.is_integer():
            count = int(count)
        if isinstance(faces, float) and faces.is_integer():
            faces = int(faces)
        if isinstance(count, complex) or isinstance(faces, complex):
            return self.dComplex(count, faces)
        elif isinstance(count, float) or isinstance(faces, float):
            return self.dFloat(count, faces)
        elif isinstance(count, int) and isinstance(faces, int):
            return self.dInt(count, faces)
        else:
            raise TypeError("Invalid type")
