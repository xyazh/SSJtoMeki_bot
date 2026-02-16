class Comparator:
    def __init__(self, value: int | float | complex):
        self.value: int | float | complex = value

    def __eq__(self, other):
        if isinstance(self.value, complex) and isinstance(other, complex):
            return abs(self.value) == abs(other)
        return self.value == other

    def __lt__(self, other):
        if isinstance(self.value, complex) and isinstance(other, complex):
            return abs(self.value) < abs(other)
        return self.value < other

    def __gt__(self, other):
        if isinstance(self.value, complex) and isinstance(other, complex):
            return abs(self.value) > abs(other)
        return self.value > other

    def __le__(self, other):
        return self == other or self < other
        
    def __ge__(self, other):
        return self == other or self > other

