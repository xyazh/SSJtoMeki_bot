import re
from .AttrEnum import AttrEnum
from ..roll.tools.Expression import Expression


VALID_EXPR_PATTERN = re.compile(r"[0-9+\-*/^Ddij()?.]")
_PROTECT_MAP = {"i": "\uE000", "j": "\uE001", "d": "\uE002", "D": "\uE003"}
_RESTORE_MAP = {v: k for k, v in _PROTECT_MAP.items()}


def splitKeepAlias(word: str, pattern: str) -> list[str]:
    """Split `word` by alias regex and keep matched aliases in result."""
    parts = re.split(f"({pattern})", word)
    return [part for part in parts if part]


def _buildAliasData() -> tuple[dict[str, AttrEnum], str]:
    alias_map: dict[str, AttrEnum] = {}
    for attr in AttrEnum:
        for name in attr.names:
            alias_map[name] = attr

    sorted_aliases = sorted(alias_map.keys(), key=len, reverse=True)
    alias_pattern = "|".join(map(re.escape, sorted_aliases))
    return alias_map, alias_pattern


def _protectPlainWordLetters(exp: str) -> str:
    chars = list(exp)
    n = len(chars)
    for i, ch in enumerate(chars):
        replacement = _PROTECT_MAP.get(ch)
        if replacement is None:
            continue
        if i <= 0 or i >= n - 1:
            continue
        if VALID_EXPR_PATTERN.fullmatch(chars[i - 1]) and VALID_EXPR_PATTERN.fullmatch(chars[i + 1]):
            continue
        chars[i] = replacement
    return "".join(chars)


def _restoreProtectedLetters(word: str) -> str:
    for protected, original in _RESTORE_MAP.items():
        word = word.replace(protected, original)
    return word


class PlCard:
    @staticmethod
    def fromData(data: dict) -> "PlCard|None":
        if data is None:
            return None
        return PlCard(data)

    @staticmethod
    def fromDataList(data: dict) -> list["PlCard"]:
        return [PlCard(d) for d in data]

    def __init__(self, data: dict):
        self.name: str = data.get("name", "空白卡")
        self.builtin_attrs: dict[AttrEnum, int | float | complex] = {
            i: i.dis_val for i in AttrEnum}
        builtin_attrs_data: dict[str, int | float |
                                 str] = data.get("builtin_attrs", {})
        for i in builtin_attrs_data:
            attr_enum = AttrEnum[i]
            if attr_enum is None:
                continue
            val = builtin_attrs_data[i]
            if isinstance(val, str):
                try:
                    val = complex(val)
                except Exception:
                    continue
            self.builtin_attrs[attr_enum] = val
        self.other_attrs: dict[str, int | float | complex] = {}
        other_attrs = data.get("other_attrs", {})
        for i in other_attrs:
            val = other_attrs[i]
            if isinstance(val, str):
                try:
                    val = complex(val)
                except Exception:
                    continue
            self.other_attrs[i] = val

    def toData(self) -> dict:
        return {
            "name": self.name,
            "builtin_attrs": {i.name: str(self.builtin_attrs[i]) if isinstance(self.builtin_attrs[i], complex) else self.builtin_attrs[i]
                              for i in self.builtin_attrs},
            "other_attrs": {i: str(self.other_attrs[i]) if isinstance(self.other_attrs[i], complex) else self.other_attrs[i]
                            for i in self.other_attrs}
        }

    def getAttr(self, key: str, dis: int | float | complex | None = None) -> int | float | complex | None:
        key_enum = AttrEnum[key]
        val = self.builtin_attrs.get(key_enum, dis)
        if val is None:
            val = self.other_attrs.get(key, dis)
        return val

    def setAttr(self, key: str, val: int | float | complex) -> None:
        key_enum = AttrEnum[key]
        if key_enum in self.builtin_attrs:
            self.builtin_attrs[key_enum] = val
            return
        self.other_attrs[key] = val

    def setAttrFromDSL(self,dsl:str) -> None:
        for key, expr in self.parseDSL(dsl).items():
            try: 
                val = Expression(expr).eval()[0]
                self.setAttr(key, val)
            except Exception:
                continue

    def parseDSL(self, exp: str) -> dict[str, str]:
        _, alias_pattern = _buildAliasData()
        normalized = _protectPlainWordLetters(exp)
        result: dict[str, str] = {}
        i = 0
        n = len(normalized)
        while i < n:
            start = i
            while i < n and not VALID_EXPR_PATTERN.fullmatch(normalized[i]):
                i += 1
            if start == i:
                i += 1
                continue
            word = _restoreProtectedLetters(normalized[start:i])
            aliases = splitKeepAlias(word, alias_pattern)
            if aliases:
                word = aliases[-1]
                for alias in aliases[:-1]:
                    result[alias] = "0"
            expr_chars: list[str] = []
            while i < n and VALID_EXPR_PATTERN.fullmatch(normalized[i]):
                expr_chars.append(normalized[i])
                i += 1
            expr = "".join(expr_chars).strip() or "0"
            result[word] = expr
        return result
