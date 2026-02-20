import re
import random
import time
from dataclasses import dataclass, field
from typing import List, Optional, Union, Literal, Dict, Any


@dataclass
class UserData:
    id: int
    nickname: str
    card: Optional[str] = None
    sex: Optional[Literal["male", "female", "unknown"]] = None
    age: Optional[int] = None
    level: Optional[str] = None
    role: Optional[Literal["owner", "admin", "member"]] = None
    data: Dict[str, Any] = field(default_factory=dict)

    def getName(self) -> str:
        name = self.card
        if name == "" or name is None:
            name = self.nickname
        return name


class Template:
    def __init__(self, kw: dict = None):
        if kw is None:
            kw = {}
        self.__dict__["kw"] = kw  # 直接设置底层字典，避免触发 __setattr__

    def __setattr__(self, name, value):
        self.__dict__["kw"][name] = value

    def __getattr__(self, name):
        return self.__dict__["kw"].get(name, None)


class Random:
    def randint(self, a: int, b: int) -> int:
        return random.randint(a, b)

    def random(self) -> float:
        return random.random()

    def choice(self, *args) -> Any:
        return random.choice(args)

    def gauss(self, mu: float, sigma: float) -> float:
        return random.gauss(mu, sigma)


class Time:
    def dateTime(self) -> float:
        return time.time()

    def strTime(self, ft: str = "%Y-%m-%d %H:%M:%S") -> str:
        return time.strftime(ft, time.localtime())


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
    所以使用了{q:=data.user.inv.get(temp.name,0)}个{temp.name}，
    这{q}个{random.choice(1,2,3)}效果拔群
    """

    engine = TemplateEngine(template_text)
    result = engine.render(data=data, temp=temp, random=Random())
    print(result)
