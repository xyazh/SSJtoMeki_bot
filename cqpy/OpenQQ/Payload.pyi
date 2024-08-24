from typing import overload


class Payload:
    @overload
    def __init__(self):
        ...

    @overload
    def __init__(self, data: str):
        ...

    @overload
    def __init__(self, data: dict):
        ...

    @overload
    def __init__(self, data: bytes):
        ...

    @property
    def op(self) -> int:
        ...

    @op.setter
    def op(self, value:int):
        ...

    @property
    def d(self) -> object:
        ...

    @d.setter
    def d(self, value:object):
        ...

    @property
    def s(self) -> int:
        ...

    @s.setter
    def s(self, value:int):
        ...

    @property
    def t(self) -> str:
        ...

    @t.setter
    def t(self, value:str):
        ...

    def getDict(self)->dict:
        ...