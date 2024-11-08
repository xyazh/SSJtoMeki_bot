import re

if __name__ == "__main__":
    from IType import *
else:
    from .IType import *


class Order:
    def __init__(self, o_li: list, raw_msg: str):
        self.o_li = o_li
        self.raw_msg = raw_msg

    def getiGnorePrefixOLi(self) -> list[str]:
        if not self.o_li:
            r = []
            self.o_li = r
            if (len(self.raw_msg) >= 2) and (self.raw_msg[0] != " "):
                for i in self.raw_msg.split(" "):
                    if i != "" and i != " ":
                        r.append(i)
        return self.o_li

    def checkOrder(self, order: str, ignore_prefix: bool = False) -> bool:
        if not self.o_li and not ignore_prefix:
            return False
        if ignore_prefix:
            o_li = self.getiGnorePrefixOLi()
            if len(o_li) <= 0:
                return False
            true_order = o_li[0]
            if order == true_order:
                return True
        true_order = self.o_li[0][1:]
        return order == true_order

    def checkOrderRe(self, pattern: str, ignore_prefix: bool = False) -> bool:
        if not self.o_li and not ignore_prefix:
            return False
        if ignore_prefix:
            o_li = self.getiGnorePrefixOLi()
            if len(o_li) <= 0:
                return False
            order = o_li[0]
            if re.fullmatch(pattern, order) is not None:
                return True
        order = self.o_li[0][1:]
        return re.fullmatch(pattern, order) is not None

    def getArgCount(self) -> int:
        return len(self.o_li)-1

    def getOrderStr(self) -> str:
        if len(self.o_li) <= 0:
            return ""
        if len(self.o_li[0]) < 2:
            return ""
        return self.o_li[0][1:]


    def getArg(self, index: int, t: Callable[[T], T] = str) -> str | T | None: # type: ignore
        r = None
        if index >= 0 and index < len(self.o_li):
            r = self.o_li[index]
        if r == None or t == str:
            return r
        try:
            r = t(r)
            return r
        except BaseException as e:
            pass
        return None

    def getArgs(self, *args: tuple[int], t: Callable[[T], T] = str) -> tuple[str | T | None, ...]: # type: ignore
        return tuple(self.getArg(i, t=t) for i in args)


if __name__ == "__main__":
    order = Order(["/s", "1", "b"],"/s 1 b")
    print(order.getArg(1, int))
