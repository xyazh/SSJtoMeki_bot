import random
import re
import math


class RollHelper:
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
    def formatValue(value):
        def fmt(x):
            x = round(x, 2)
            s = f"{x:.2f}"
            s = s.rstrip("0").rstrip(".")
            return s if s else "0"
        if isinstance(value, int):
            return str(value)
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return fmt(value)
        if isinstance(value, complex):
            r = value.real
            i = value.imag
            r = round(r, 2)
            i = round(i, 2)
            if i == 0:
                if r.is_integer():
                    return str(int(r))
                return fmt(r)
            r_str = "0" if r == 0 else fmt(r)
            i_str = fmt(abs(i)) + "j"
            if r == 0:
                return ("-" if i < 0 else "") + i_str
            sign = "+" if i >= 0 else "-"
            return f"{r_str}{sign}{i_str}"
        return str(value)