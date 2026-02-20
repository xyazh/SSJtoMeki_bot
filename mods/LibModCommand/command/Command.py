import logging
from xyacqbot.CommandDLS import CommandDLS
from xyacqbot.xyazhServer.ConsoleMessage import ConsoleMessage


class CommandInfo:
    def __init__(self, func, template_str, sign, desc, category, hidden=False):
        self.func = func
        self.template_str = template_str
        self.sign = sign
        self.desc = desc
        self.category = category
        self.hidden = hidden
        self.parser = CommandDLS(template_str)


class Command:
    registry: dict[str, list[CommandInfo]] = {}

    def __init__(self, template: str, sign: str = "", desc: str = "", category: str = "default", hidden=False):
        self.template = template
        self.sign = sign
        self.desc = desc
        self.category = category
        self.hidden = hidden

    def __call__(self, func):
        info = CommandInfo(
            func=func,
            template_str=self.template,
            sign=self.sign,
            desc=self.desc,
            category=self.category,
            hidden=self.hidden
        )
        regs = Command.registry.get(self.category, [])
        regs.append(info)
        Command.registry[self.category] = regs
        return func

    @classmethod
    def dispatch(cls, text: str, *arg) -> list[str]:
        r_text = []
        for cmds in cls.registry.values():
            for cmd in cmds:
                result = cmd.parser.template(text, True)
                if not result:
                    continue
                try:
                    r_text.append(cmd.func(*arg, **result))
                except Exception as e:
                    ConsoleMessage.printError(
                        f"{cmd.func}|{cmd.template_str}|{e}")
                    logging.error(e)
        return r_text

    @classmethod
    def help(cls, arg: str | None = None, page: int = 1) -> str:
        if arg is None:
            categories = list(cls.registry.keys())
            help_arg = ",".join(
                [f"'{cat}'" for i, cat in enumerate(categories)])
            help1 = f"help [e:emun({help_arg})]"
            help2 = f"help [e:emun({help_arg})] [page:int]"
            help_text = ""
            help_text += f"{help1}\n描述: 获取命令列表以及关于命令的提示\n\n"
            help_text += f"{help2}\n描述: 命令列表翻页\n"
            return help_text
        category_commands = cls.registry.get(arg, None)
        if category_commands is None:
            return f"没有找到类别: {arg}"
        start = (page - 1) * 20
        end = start + 20
        paged_commands = category_commands[start:end]
        if not paged_commands:
            return f"页 {page} 中没有更多命令了。"
        help_text = f"=== {arg} (第 {page} 页) ===\n"
        for cmd in paged_commands:
            if cmd.hidden:
                continue
            help_text += f"{cmd.sign}\n描述: {cmd.desc}\n\n"
        if len(category_commands) > end:
            help_text += f"更多命令，请查看下一页: {page + 1}"
        return help_text
