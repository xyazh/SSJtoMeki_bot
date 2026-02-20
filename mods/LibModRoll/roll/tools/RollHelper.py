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
    def foramtValue(value):
        if isinstance(value, float):
            return "%.4f" % value
        if isinstance(value, complex):
            return "%.4f+%.4fj" % (value.real, value.imag)
        return str(value)