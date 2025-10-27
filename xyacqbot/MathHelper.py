class MathHelper:
    @staticmethod
    def A(m: int, n: int):
        """
        排列数
        """
        return MathHelper.factorial(n)/MathHelper.factorial(n-m)

    def C(a: int, b: int):
        """
        组合数
        """
        fz = 1
        n = b-a
        while n < b:
            fz = fz * (n + 1)
            n = n + 1
        fm = MathHelper.factorial(a)
        return fz / fm

    @staticmethod
    def decreasesTechnique(m, n):
        """
        更相减损术
        """
        if m == n:
            return n
        while m % 2 == 0 and n % 2 == 0:
            m = m/2
            n = n/2
        n = (max(m, n), min(m, n))
        d = n[0]-n[1]
        while d != n[1]:
            n[0] = max(d, n[1])
            n[1] = min(d, n[1])
            d = n[0]-n[1]
        return d

    @staticmethod
    def factorial(n: int):
        """
        计算n的阶乘
        """
        """
        if n > 0:
            return n*MathHelper.factorial(n-1)
        else:
            return 1
        """
        result = 1
        for i in range(1, n+1):
            result = result*i
        return result


    class Fraction:
        """
        高精度浮点数
        """

        def __add__(self, other):
            if isinstance(other, MathHelper.Fraction):
                numerator = self.signBit*self.numerator*other.denominator + \
                    other.signBit*other.numerator*self.denominator
                denominator = self.denominator*other.denominator
                signBit = 1
                if numerator < 0:
                    signBit = signBit*-1
                if denominator < 0:
                    signBit = signBit*-1
                self.signBit = signBit
                self.numerator = abs(numerator)
                self.denominator = abs(denominator)
                return self

        def __init__(self, a):
            if isinstance(a, str):
                a = self._strToFraction(s=a)
            self.numerator = abs(a[0])
            self.denominator = abs(a[1])
            if (a[0]/a[1] == 0):
                self.numerator = 0
                self.denominator = 1
            self.signBit = 1
            if a[0] < 0:
                self.signBit = self.signBit*-1
            if a[1] < 0:
                self.signBit = self.signBit*-1

        def __str__(self):
            if self.numerator == 0:
                return "0"
            s1 = str(int(self.signBit*self.numerator))
            s2 = str(int(self.denominator))
            return s1+"/"+s2

        def __sub__(self, other):
            if isinstance(other, MathHelper.Fraction):
                other.signBit = -other.signBit
            return self.__add__(other)

        def _strToFraction(self=None, s=""):
            li = s.split("/")
            return (int(li[0]), int(li[1]))

        def getFloat(self):
            return self.signBit * self.numerator / self.denominator

        def reduction(self):
            if self.numerator == 0:
                self.numerator = 0
                self.denominator = 1
            else:
                l = MathHelper.decreasesTechnique(
                    self.numerator, self.denominator)
                self.numerator = int(self.numerator/l)
                self.denominator = int(self.denominator/l)
            return self.__str__()
