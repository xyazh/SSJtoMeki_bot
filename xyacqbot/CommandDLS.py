import re


class emun:
    def __init__(self, *args):
        self.args = tuple(sorted(args, key=len, reverse=True))

    def values(self):
        return sorted(self.args, key=len, reverse=True)


class regex:
    def __init__(self, pattern):
        self.regex = re.compile(pattern)


class Template:

    def __init__(self, text):
        self.raw = text
        name, type_expr = text.split(":", 1)
        self.variable = name.rstrip("?")
        self.optional = name.endswith("?")
        type_expr = type_expr.strip()
        if type_expr == "str":
            self.type = str
        elif type_expr == "int":
            self.type = int
        elif type_expr == "float":
            self.type = float
        elif type_expr.startswith("emun("):
            inner = type_expr[5:-1]
            args = []
            buf = []
            quote = None
            for ch in inner:
                if quote:
                    if ch == quote:
                        quote = None
                    else:
                        buf.append(ch)
                    continue
                if ch in ("'", '"'):
                    quote = ch
                    continue
                if ch == ",":
                    args.append("".join(buf))
                    buf = []
                    continue
                buf.append(ch)
            if buf:
                args.append("".join(buf))
            self.type = emun(*args)
        elif type_expr.startswith("regex("):
            inner = type_expr[6:-1]
            self.type = regex(inner)
        else:
            raise ValueError(type_expr)


class CommandDLS:

    def __init__(self, dsl):
        self.dsl = dsl
        self.compiled_dsl = self.compileDLS(dsl)
        self.memo = {}

    def compileDLS(self, dsl):
        result = []
        i = 0
        n = len(dsl)
        literal = []
        while i < n:
            if dsl[i] != "[":
                literal.append(dsl[i])
                i += 1
                continue
            if literal:
                result.append("".join(literal))
                literal = []
            depth = 1
            paren = 0
            j = i + 1
            while j < n:
                c = dsl[j]
                if c == "(":
                    paren += 1
                elif c == ")":
                    paren -= 1
                elif c == "[" and paren == 0:
                    depth += 1
                elif c == "]" and paren == 0:
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if j >= n:
                raise ValueError("missing ]")
            result.append(
                Template(dsl[i + 1:j])
            )
            i = j + 1
        if literal:
            result.append("".join(literal))
        return result

    def template(self, text):
        self.memo.clear()
        return self._match(
            token_idx=0,
            pos=0,
            text=text,
            result={}
        )

    def _match(self, token_idx, pos, text, result):
        key = (token_idx, pos, tuple(sorted(result.items())))
        if key in self.memo:
            return None
        if token_idx >= len(self.compiled_dsl):
            if pos == len(text):
                return result
            return None
        token = self.compiled_dsl[token_idx]
        if isinstance(token, str):
            if text.startswith(token, pos):
                return self._match(
                    token_idx + 1,
                    pos + len(token),
                    text,
                    result.copy()
                )
            self.memo[key] = True
            return None
        if token.type is float:
            m = re.match(
                r"-?\d+(?:\.\d+)?",
                text[pos:]
            )
            if m:
                nr = result.copy()
                nr[token.variable] = float(
                    m.group()
                )
                r = self._match(
                    token_idx + 1,
                    pos + len(m.group()),
                    text,
                    nr
                )
                if r:
                    return r
        if token.type is int:
            m = re.match(
                r"-?\d+",
                text[pos:]
            )
            if m:
                nr = result.copy()
                nr[token.variable] = int(
                    m.group()
                )
                r = self._match(
                    token_idx + 1,
                    pos + len(m.group()),
                    text,
                    nr
                )
                if r:
                    return r
        if isinstance(token.type, emun):
            for candidate in token.type.values():
                if text.startswith(candidate, pos):
                    nr = result.copy()
                    nr[token.variable] = candidate
                    r = self._match(
                        token_idx + 1,
                        pos + len(candidate),
                        text,
                        nr
                    )
                    if r:
                        return r
        if isinstance(token.type, regex):
            m = token.type.regex.match(
                text,
                pos
            )
            if m:
                nr = result.copy()
                nr[token.variable] = m.group()
                r = self._match(
                    token_idx + 1,
                    m.end(),
                    text,
                    nr
                )
                if r:
                    return r
        if token.type is str:
            if token_idx == len(self.compiled_dsl) - 1:
                nr = result.copy()
                nr[token.variable] = text[pos:]
                return nr
            for end in range(pos, len(text) + 1):
                nr = result.copy()
                nr[token.variable] = text[pos:end]
                r = self._match(
                    token_idx + 1,
                    end,
                    text,
                    nr
                )
                if r:
                    return r
        self.memo[key] = True
        return None


if __name__ == "__main__":
    TEST_CASES = [
        (
            "[a:str][r:regex([a-z]+)][i:int]",
            "123abc456"
        ),
        (
            "[e:emun('.','/')][e1:emun('coc7','coc7 ')][i:int]",
            "/coc7123"
        ),
    ]

    for idx, (dsl, text) in enumerate(TEST_CASES, 1):
        print(f"\n========== CASE {idx} ==========")
        print("DSL :", dsl)
        print("TEXT:", text)

        try:
            d = CommandDLS(dsl)
            result = d.template(text)
            print("RESULT:", result)
        except Exception as e:
            print("ERROR :", e)
