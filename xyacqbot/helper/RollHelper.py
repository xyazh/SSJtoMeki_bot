import random
import re
import math


class RollHelper:
    @staticmethod
    def decodeArrStr(t: str) -> dict:
        """
        传入录卡字符串，将字符串处理为dict
        """
        t = t.replace("\r", "")
        t = t.replace("\n", "")
        li = re.split(r"([0-9]+)", t)
        li = [i for i in li if i != ""]
        li1 = li[::2]
        li2 = li[1::2]
        if len(li1) - len(li2) == 1:
            li2.append("0")
        d = {k: v for k, v in zip(li1, li2)}
        for i in d:
            if d[i].isdigit():
                d[i] = int(d[i])
            else:
                d[i] = float(d[i])
        if "mp魔法hp" in d:
            d["hp"] = d["mp魔法hp"]
            d["mp"] = 0
        if "幸运" in d:
            d["luk"] = d["幸运"]
        return d

    @staticmethod
    def isNumber(string):
        """
        传入一个字符串，判断该字符串是否为整数或浮点数
        """
        try:
            float(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def evaluateExpression(expression: str) -> float | int | complex:
        """
        传入一个roll点的表达式，如1d(1+3),计算该表达式并返回结果

        返回结果包含整数，浮点数，复数
        """
        operator_precedence = {"?": 0, "+": 1, "-": 1,
                               "*": 2, "/": 2, "^": 3, "D": 4, "d": 4}
        expression = expression.replace("（", "(")
        expression = expression.replace("）", ")")
        expression = expression.replace("(-", "(0-")
        tokens = re.findall(r"[-+*/^Ddij()\?]|\d+\.?\d*", expression)
        operator_stack = []
        output_queue = []
        for token in tokens:
            if RollHelper.isNumber(token):
                output_queue.append(float(token))
            elif token in ("i", "j"):
                output_queue.append(complex(0, 1))
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
            else:
                while operator_stack and operator_stack[-1] != "(" and operator_precedence[operator_stack[-1]] >= operator_precedence[token]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
        while operator_stack:
            output_queue.append(operator_stack.pop())
        operand_stack = []
        for token in output_queue:
            if isinstance(token, (float, int, complex)):
                operand_stack.append(token)
            else:
                if token in ["D", "d"]:
                    n = operand_stack.pop()
                    if len(operand_stack) <= 0:
                        raise SyntaxError("invalid syntax")
                    m = operand_stack.pop()
                    result = RollHelper.d(m, n)
                    operand_stack.append(result)
                else:
                    b = operand_stack.pop()
                    a = None
                    if len(operand_stack) > 0:
                        a = operand_stack.pop()
                    if token == "?":
                        if a == None:
                            raise SyntaxError("invalid syntax")
                        result = random.choice((a, b))
                    if token == "+":
                        result = a + b
                    elif token == "-":
                        if a == None:
                            a = 0
                        result = a - b
                    elif token == "*":
                        if a == None:
                            raise SyntaxError("invalid syntax")
                        result = a * b
                    elif token == "/":
                        if a == None:
                            raise SyntaxError("invalid syntax")
                        result = a / b
                    elif token == "^":
                        if a == None:
                            raise SyntaxError("invalid syntax")
                        result = a ** b
                    operand_stack.append(result)
        return operand_stack.pop()

    @staticmethod
    def reFind(r: str, s: str):
        if re.match(r, s):
            s = re.sub(r, "114514", s, count=1)
            if s == "114514":
                return True
        return False

    @staticmethod
    def findsStr(s: str, fs: list[str] | tuple[str]):
        flag = False
        for i in fs:
            if i in s:
                flag = True
                break
        return flag

    @staticmethod
    def compareComplex(complex1: complex, complex2: complex):
        """
        按照自定义的方式比较两个复数的大小

        复数1大于复数2返回1，复数1小于复数2返回-1，复数1等于复数2返回0
        """
        zero = complex(0, 0)
        one_plus_j = complex(1, 1)
        line = one_plus_j - zero
        proj_complex1 = (complex1 - zero).real * line.real + \
            (complex1 - zero).imag * line.imag
        proj_complex2 = (complex2 - zero).real * line.real + \
            (complex2 - zero).imag * line.imag
        if proj_complex1 > proj_complex2:
            return 1
        elif proj_complex1 < proj_complex2:
            return -1
        else:
            return 0

    @staticmethod
    def d(m: int | float | complex, n: int | float | complex) -> int | complex:
        """
        传入两个参数m、n————mdn，（如1d3就为m=1，n=3）

        计算投点结果
        """
        mi = 0
        if isinstance(m, complex):
            mi = m.imag
            m = m.real
        ni = 0
        if isinstance(n, complex):
            ni = n.imag
            n = n.real
        dm = int(m)
        fm = m - dm
        dmi = int(mi)
        fmi = mi - dmi
        dn = int(n)
        fn = n - dn
        dni = int(ni)
        fni = ni - dni
        x = -1 if m < 0 else 1
        xi = -1 if mi < 0 else 1
        y = -1 if n < 0 else 1
        yi = -1 if ni < 0 else 1
        dm += (1 if random.random() < abs(fm) else 0) * x
        dmi += (1 if random.random() < abs(fmi) else 0) * xi
        dn += (1 if random.random() < abs(fn) else 0) * y
        dni += (1 if random.random() < abs(fni) else 0) * yi
        dm = int(abs(dm))
        dmi = int(abs(dmi))
        adm = int(max(dm - 114, 0))
        admi = int(max(dmi - 114, 0))
        dm = int(min(dm, 114))
        dmi = int(min(dmi, 114))
        r = 0
        ri = 0
        if dn == 0:
            r += 0
        else:
            for _ in range(dm):
                r += (random.randint(min(dn, y), max(y, dn)))*x
            r += int(adm*(dn+0)/2*x)
        if mi == 0 and ni == 0:
            return r
        if dni == 0:
            ri += 0
        else:
            for _ in range(dm):
                ri += (random.randint(min(dni, yi), max(yi, dni)))*x
            ri += int(adm*(dni+0)/2*x)
        if dni == 0:
            r -= 0
        else:
            for _ in range(dmi):
                r -= (random.randint(min(dni, yi), max(yi, dni)))*xi
            r -= int(admi*(dni+0)/2*x)*xi
        if dn == 0:
            ri += 0
        else:
            for _ in range(dmi):
                ri += (random.randint(min(dn, y), max(y, dn)))*xi
            ri += int(admi*(dn+0)/2*x)*xi
        return r + ri*1j

    @staticmethod
    def findRealProjection(complex_number: complex | int | float) -> float:
        """
        获取复数在(1,1)上的投影大小
        """
        line = complex(1, 1)
        projected_complex = (complex_number * line.conjugate()
                             ).real / line.conjugate().real
        return projected_complex.real

    @staticmethod
    def evaluateExpressionToFloat(expression: str) -> float:
        """
        传入一个roll点的表达式，如1d(1+3),计算该表达式并返回结果

        返回结果包含整数，浮点数（不包含复数）
        """
        return RollHelper.findRealProjection(RollHelper.evaluateExpression(expression))

    @staticmethod
    def binomialDistributionProbability(p: float, n: int, k: int) -> float:
        """
        二项式分布概率
        """
        return math.comb(n, k) * p**k * (1-p)**(n-k)

    @staticmethod
    def bestRandomGuass(mu: float, sigma: float, n: float):
        """
        生成范围大小为n的高斯分布随机数
        """
        lower = mu - n
        upper = mu + n
        return RollHelper.bestRandomGuassRange(mu, sigma, lower, upper)

    def bestRandomGuassRange(mu: float, sigma: float, lower: float, upper: float):
        """
        生成在[lower, upper]范围内的高斯分布随机数
        """
        r = random.gauss(mu, sigma)
        lower, upper = min(lower, upper), max(lower, upper)
        while r < lower or r > upper:
            r = random.gauss(mu, sigma)
        return r

    @staticmethod
    def randomSplitInt(n: int, m: int, l: int) -> list[int]:
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
                index = random.randint(0, m-1)
                while True:
                    if result[index] + 1 <= l:
                        result[index] += 1
                        break
                    else:
                        index = int((index + 1) % m)
        return result

    @staticmethod
    def surpriseDistribution(p1: float, e1: float, p2: float, e2: float, p3: float, e3: float, lower: float, upper: float, weight1: float, weight2: float, weight3: float) -> float:
        """
        节目效果分布
        
        有三个峰的组合正态分布，可以实现中低高低中的概率分布
        """
        w = weight1 + weight2 + weight3
        weight1 /= w
        weight2 /= w
        weight3 /= w
        r = random.random()
        result = 0
        if r < weight1:
            result = RollHelper.bestRandomGuassRange(p1, e1, lower, upper)
        elif r < weight1 + weight2:
            result = RollHelper.bestRandomGuassRange(p2, e2, lower, upper)
        else:
            result = RollHelper.bestRandomGuassRange(p3, e3, lower, upper)
        return result

    def presetSurpriseDistribution1() -> float:
        """
        范围[0,100]

        0.0118-0.0080-0.0117-0.0080-0.0118

        两边几乎与中间一样高
        """
        return RollHelper.surpriseDistribution(0, 15, 49.5, 22, 100, 15, 0, 100, 1, 3, 1)

    def presetSurpriseDistribution2() -> float:
        """
        范围[0,100]

        0.0100-0.0082-0.0125-0.0082-0.0100

        两边略高中间高
        """
        return RollHelper.surpriseDistribution(0, 16, 49.5, 21, 100, 16, 0, 100, 9, 32, 9)

    def presetSurpriseDistribution3() -> float:
        """
        范围[1,100]

        0.0105-0.0082-0.0125-0.0082-0.0105

        两边略高中间高
        """
        return RollHelper.surpriseDistribution(0, 16, 51, 21, 100, 16, 1, 100, 9, 32, 9)
    

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from collections import Counter

    def plot_frequency_histogram(int_list):
        # 统计频率
        counter = Counter(int_list)
        
        # 拆分为 x 和 y
        numbers = list(counter.keys())
        frequencies = list(counter.values())
        
        # 绘制柱状图
        plt.bar(numbers, frequencies, width=0.6, edgecolor='black')
        
        # 设置标题和标签
        plt.title("Frequency Distribution Histogram")
        plt.xlabel("Number")
        plt.ylabel("Frequency")
        
        plt.show()


    # 示例
    l = [int(RollHelper.surpriseDistribution(0, 20, 39, 12, 100, 16, 1, 100, 9, 30, 2)) for _ in range(1000000)]
    plot_frequency_histogram(l)
