import re


class emun:
    def __init__(self, *args):
        self.args = args

    def __call__(self, text: str):
        for a in self.args:
            if text.startswith(a):
                return a, text[len(a):]
        return None, text


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
            args = [a.strip().strip("'\"")
                    for a in args_str.split(",") if a.strip()]
            self.type = SAFE_TYPES["emun"](*args)
        elif type_expr in SAFE_TYPES:
            self.type = SAFE_TYPES[type_expr]
        else:
            raise ValueError(f"Unknown or unsafe type: {type_expr}")

    def extract(self, data: str, end_delimiter=None):
        data = data.lstrip()
        
        if self.type is str:
            if end_delimiter:
                idx = data.find(end_delimiter)
                if idx == -1:
                    return data, ""
                return data[:idx], data[idx:]
            else:
                return data, ""
        
        elif self.type is int:
            m = re.match(r"(\d+)", data)
            if m:
                return int(m.group(1)), data[m.end():]
        
        elif self.type is float:
            m = re.match(r"(\d+(?:\.\d+)?)", data)
            if m:
                return float(m.group(1)), data[m.end():]
        
        elif callable(self.type):
            val, rest = self.type(data)
            if val is not None:
                return val, rest
        
        return (None, data) if self.optional else (None, None)



class DSL:
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

    def template(self, text: str):
        result = {}
        offset = 0
        parts = self.compiled_dsl

        for i, s in enumerate(parts):
            if isinstance(s, str):
                idx = text.find(s, offset)
                if idx == -1:
                    return None
                offset = idx + len(s)
            else:
                # 找下一个固定字符串
                next_fixed = None
                for j in range(i + 1, len(parts)):
                    if isinstance(parts[j], str):
                        next_fixed = parts[j]
                        break
                segment = text[offset:]
                val, _ = s.extract(segment, end_delimiter=next_fixed)
                if val is not None:
                    result[s.variable] = val
                    if next_fixed:
                        offset += len(str(val))
                    else:
                        offset = len(str(text))
                elif not s.optional:
                    return None

        return result


if __name__ == "__main__":
    # 示例
    d = DSL("[e:emun('.','/')]use [count:int] [item:str] [do:str] [damege:float]")
    text = "/use 1 apple eat 1.1"
    print("RESULT:", d.template(text))
    text = ".use 1 apple eat 1.1"
    print("RESULT:", d.template(text))
