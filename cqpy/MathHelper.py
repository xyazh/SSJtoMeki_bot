class MathHelper:
    def A(m:int,n:int):
        return MathHelper.factorial(n)/MathHelper.factorial(n-m)

    def C(a:int,b:int):
        fz = 1
        n = b-a
        while n < b:
            fz = fz * (n + 1)
            n = n + 1
        fm = MathHelper.factorial(a)
        return fz / fm

    def decreasesTechnique(m,n):
        if m==n:
            return n
        while m%2==0 and n%2==0:
            m=m/2
            n=n/2
        li=[max(m,n),min(m,n)]
        d=li[0]-li[1]
        while d!=li[1]:
            li[0]=max(d,li[1])
            li[1]=min(d,li[1])
            d=li[0]-li[1]
        return d

    def factorial(n:int):
        if n>0:
            return n*MathHelper.factorial(n-1)
        else:
            return 1

    class Fraction:
        def __add__(self, other):
            if isinstance(other,MathHelper.Fraction):
                numerator=self.signBit*self.numerator*other.denominator+other.signBit*other.numerator*self.denominator
                denominator=self.denominator*other.denominator
                signBit=1
                if numerator<0:
                    signBit=signBit*-1
                if denominator<0:
                    signBit=signBit*-1
                self.signBit = signBit
                self.numerator = abs(numerator)
                self.denominator = abs(denominator)
                return self
        
        def __init__(self,a):
            if type(a)==str:
                a=self._strToFraction(s=a)
            self.numerator=abs(a[0])
            self.denominator=abs(a[1])
            if(a[0]/a[1]==0):
                self.numerator=0
                self.denominator=1
            self.signBit=1
            if a[0]<0:
                self.signBit=self.signBit*-1
            if a[1]<0:
                self.signBit=self.signBit*-1


        def __str__(self):
            if self.numerator==0:
                return "0"
            s1=str(int(self.signBit*self.numerator))
            s2=str(int(self.denominator))
            return s1+"/"+s2

        def __sub__(self,other):
            if isinstance(other,MathHelper.Fraction):
                other.signBit = -other.signBit
            return self.__add__(other)
            
        
        def _strToFraction(self=None,s=""):
            li=s.split("/")
            return (int(li[0]),int(li[1]))  

        def getFloat(self):
            return self.signBit * self.numerator / self.denominator

        def reduction(self):
            if self.numerator==0:
                self.numerator=0
                self.denominator=1
            else:
                l=MathHelper.decreasesTechnique(self.numerator,self.denominator)
                self.numerator=int(self.numerator/l)
                self.denominator=int(self.denominator/l)
            return self.__str__()