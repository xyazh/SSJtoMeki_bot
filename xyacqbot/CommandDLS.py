import re


class emun:
    def __init__(self, *args):
        self.args = args

    def __call__(self, text: str):
        for a in self.args:
            if text.startswith(a):
                return a, len(a)
        return None, 0


SAFE_TYPES = {
    "int": int,
    "str": str,
    "float": float,
    "emun": lambda *args: emun(*args),
}


class Template:
    def __init__(self, template: str):
        self.template = template
        self.exec()

    def __repr__(self):
        return f"Template<{self.template}>"

    def exec(self):
        vt = self.template.split(":", 1)
        self.variable = vt[0].rstrip("?")
        self.optional = vt[0].endswith("?")
        type_expr = vt[1].strip()
        if type_expr.startswith("emun("):
            args_str = type_expr[len("emun("):-1]
            args = [
                a.strip().strip("'\"")
                for a in args_str.split(",")
                if a.strip()
            ]
            self.type = SAFE_TYPES["emun"](*args)
        elif type_expr in SAFE_TYPES:
            self.type = SAFE_TYPES[type_expr]
        else:
            raise ValueError(f"Unknown or unsafe type: {type_expr}")

    def extract(self, data: str, end_delimiter=None):
        original_len = len(data)
        data = data.lstrip()
        lstrip_len = original_len - len(data)
        if self.type is str:
            if end_delimiter:
                idx = data.find(end_delimiter)
                if idx == -1:
                    value = data
                    consumed = len(data)
                else:
                    value = data[:idx]
                    consumed = idx
            else:
                value = data
                consumed = len(data)
            return value, consumed + lstrip_len
        elif self.type is int:
            m = re.match(r"(\d+)", data)
            if m:
                value = int(m.group(1))
                consumed = m.end()
                return value, consumed + lstrip_len
        elif self.type is float:
            m = re.match(r"(\d+(?:\.\d+)?)", data)
            if m:
                value = float(m.group(1))
                consumed = m.end()
                return value, consumed + lstrip_len
        elif callable(self.type):
            val, consumed = self.type(data)
            if val is not None:
                return val, consumed + lstrip_len
        if self.optional:
            return None, 0

        return None, None


class CommandDLS:
    def __init__(self, dsl: str):
        self.dsl = dsl
        self.compileDsl(dsl)

    def compileDsl(self, dsl: str):
        over_stack = []
        stack = []
        l = len(dsl)
        dsl = dsl + " "
        i = 0
        while i < l:
            if dsl[i] == "[" and dsl[i + 1] != "[":
                if stack:
                    over_stack.append("".join(stack))
                stack = []
                i += 1
                continue

            if dsl[i] == "]" and dsl[i + 1] != "]":
                over_stack.append(Template("".join(stack)))
                stack = []
                i += 1
                continue

            if dsl[i] == "[" and dsl[i + 1] == "[":
                stack.append("[")
                i += 2
                continue

            if dsl[i] == "]" and dsl[i + 1] == "]":
                stack.append("]")
                i += 2
                continue

            stack.append(dsl[i])
            i += 1

        if stack:
            over_stack.append("".join(stack))

        over_stack = [x for x in over_stack if x != ""]
        self.compiled_dsl = over_stack

    def template(self, text: str, full_match: bool = False):
        result = {}
        offset = 0
        parts = self.compiled_dsl
        for i, s in enumerate(parts):
            if isinstance(s, str):
                if not text.startswith(s, offset):
                    return None
                offset += len(s)
                continue
            next_fixed = None
            for j in range(i + 1, len(parts)):
                if isinstance(parts[j], str):
                    next_fixed = parts[j]
                    break
            segment = text[offset:]
            val, consumed = s.extract(segment, end_delimiter=next_fixed)
            if val is None:
                if not s.optional:
                    return None
                continue

            result[s.variable] = val
            offset += consumed
        if full_match:
            remaining = text[offset:].strip()
            if remaining:
                return None

        return result


if __name__ == "__main__":
    d = CommandDLS(
        "[e:emun('.','/')]use [do:str]"
    )
    print("CASE1:", d.template("/1 apple use eat"))
    print("CASE2:", d.template("/use eat"))
