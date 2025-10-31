import re

class TemplateEngine:
    """
    支持：
    - 普通占位符 {expr}
    - 海象运算符 {var:=expr}，可在模板中后续引用
    - TemplateEngine将会尝试执行模板中的表达式并替换为结果。
    - 请确保模板中的表达式的来源可信任，防止远程执行。
    """
    ASSIGN_RE = re.compile(r"\{([a-zA-Z_]\w*):=(.+?)\}")  # 匹配 {n:=...}

    def __init__(self, template: str):
        self.template = template

    def render(self, **env):
        local_env = dict(env)
        global_env = {}

        code = self.template
        def assign_replacer(match):
            var, expr = match.groups()
            try:
                local_env[var] = eval(expr, global_env, local_env)
                return str(local_env[var])
            except Exception as e:
                return f"<格式化错误:{e}>"
        code = self.ASSIGN_RE.sub(assign_replacer, code)
        try:
            fcode = f'f"""{code}"""'
            exec(f"_result = {fcode}", global_env, local_env)
            return local_env["_result"]
        except Exception as e:
            return f"<格式化错误:{e}>"
        


if __name__ == "__main__":
    class User:
        def __init__(self):
            self.name = "Alice"
            self.inv = {"apple": 2, "banana": 5}

        def find(self, item):
            return self.inv.get(item, 0)

        def count(self, item, default=0):
            return self.inv.get(item, default)

    class Data:
        user = User()

    class Temp:
        count = 3
        name = "apple"

    data = Data()
    temp = Temp()

    # ==== 示例模板 ====
    template_text = """
    {data.user.name}尝试使用{temp.count}个{temp.name}，
    但是库存只有{data.user.inv.get(temp.name,0)}个{temp.name}，
    所以使用了{n:=data.user.inv.get(temp.name,0)}个{temp.name}，
    这{n}个{temp.name}效果拔群
    """

    engine = TemplateEngine(template_text)
    result = engine.render(data=data, temp=temp)
    print(result)
