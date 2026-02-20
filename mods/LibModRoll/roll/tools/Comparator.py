class Comparator:
    def __init__(self, value: int | float | complex):
        self.value: int | float | complex = value

    def eqComplex(self, v1: complex, v2: complex) -> int:
        v1r = v1.real
        v2r = v2.real
        if v1r < v2r:
            return -1
        elif v1r > v2r:
            return 1
        v1i = abs(v1.imag)
        v2i = abs(v2.imag)
        if v1i < v2i:
            return -1
        elif v1i > v2i:
            return 1
        return 0

    def __eq__(self, other):
        v1 = self.value
        v2 = other
        if isinstance(v2, Comparator):
            v2 = v2.value
        v1 = complex(v1)
        v2 = complex(v2)
        return self.eqComplex(v1, v2) == 0

    def __lt__(self, other):
        v1 = self.value
        v2 = other
        if isinstance(v2, Comparator):
            v2 = v2.value
        v1 = complex(v1)
        v2 = complex(v2)
        return self.eqComplex(v1, v2) == -1

    def __gt__(self, other):
        v1 = self.value
        v2 = other
        if isinstance(v2, Comparator):
            v2 = v2.value
        v1 = complex(v1)
        v2 = complex(v2)
        return self.eqComplex(v1, v2) == 1

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other


if __name__ == "__main__":
    print(Comparator(1j) > Comparator(2j))
    print(Comparator(1j) > Comparator(0))