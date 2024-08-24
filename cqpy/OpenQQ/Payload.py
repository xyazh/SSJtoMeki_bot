import json

class Payload(dict):
    def __init__(self, *args, **kw):
        self._op: int = -1
        self._d:object = None
        self._s: int = None
        self._t: str = None

        if len(args) == 0:
            self.__init1()
        elif isinstance(args[0], str):
            self.__init2(args[0])
        elif isinstance(args[0], dict):
            self.__init3(args[0])
        elif isinstance(args[0], bytes):
            self.__init4(args[0])
        else:
            raise TypeError(
                f"Expected arguments of type str, dict, or bytes, but got {type(args[0])} instead."
            )

        super().__init__({
            "op": self._op,
            "d": self._d,
            "s": self._s,
            "t": self._t
        })

    @property
    def op(self):
        return self._op

    @op.setter
    def op(self, value):
        self._op = value
        self["op"] = value

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        self._d = value
        self["d"] = value

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, value):
        self._s = value
        self["s"] = value

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        self._t = value
        self["t"] = value

    def __init1(self):
        pass

    def __init2(self, data: str):
        try:
            json_data = json.loads(data)
            self.__init3(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {data}") from e

    def __init3(self, data: dict):
        self.op = data.get("op", -1)
        self.d = data.get("d", None)
        self.s = data.get("s", -1)
        self.t = data.get("t", "")

    def __init4(self, data: bytes):
        try:
            json_data = json.loads(data)
            self.__init3(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON bytes: {data}") from e
        
    def getDict(self)->dict:
        d = {}
        d["d"] = self._d
        d["op"] = self._op
        if self._s is not None:
            d["s"] = self._s
        if self._t is not None:
            d["t"] = self._t
        return d