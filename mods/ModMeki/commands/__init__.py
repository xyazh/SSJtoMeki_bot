import random
import time
from mods.LibModCommand.command.Command import Command
from xyacqbot.Cqserver import Cqserver
from xyacqbot.packet.PacketMsg import PacketMsg
from xyacqbot.datamanager.UserDataManager import UserDataManager
from xyacqbot.helper.RollHelper import RollHelper
from xyacqbot.CommandDLS import CommandDLS


BOT_NAME = "Meki"


@Command(
    "[e:emun('.','/','。')]help",
    sign="help",
    desc="查看帮助",
    category="常用"
)
@Command(
    "[e:emun('.','/','。')]help [sub:str]",
    sign="help",
    desc="",
    category="常用",
    hidden=True
)
def help(msg: PacketMsg, e: str, sub: str = None):
    msg = "#------帮助------\r\nMulti functional bot made with Python by Xyazh\r\n\r\nmeki酱在这里哟~\r\n"
    if sub is None:
        msg += Command.help()
    else:
        help_arg = ",".join(
            [f"'{cat}'" for i, cat in enumerate(list(Command.registry.keys()))])
        help1 = CommandDLS(f"[category:emun({help_arg})]")
        help2 = CommandDLS(f"[category:emun({help_arg})] [page:int]")
        sub1 = help1.template(sub, True)
        sub2 = help2.template(sub, True)
        if sub1:
            category = sub1.get("category")
            msg += Command.help(category, 1)
        elif sub2:
            category = sub2.get("category")
            page = sub2.get("page", 1)
            msg += Command.help(category, page)
    msg += "\r\n\r\n用命令要注意不要忘了参数，参数前一定要加空格；可以用help命令加上具体命令来查看具体命令用法"
    return msg


@Command(
    "[e:emun('.','/','。')]test",
    sign="test",
    desc="发送一条test",
    category="其他"
)
def test1(msg: PacketMsg, e: str):
    return "test"


@Command(
    "[e:emun('.','/','。')]test [r:str]",
    sign="test [r:str]",
    desc="让机器人发送一条消息",
    category="其他"
)
def test2(msg: PacketMsg, e: str, r: str):
    return r


@Command(
    "[e:emun('.','/','。')]bot",
    sign="bot",
    desc="输出机器人信息",
    category="其他"
)
def bot(msg: PacketMsg, e: str):
    return f"{BOT_NAME} is a Python-based chatbot built on the OneBot protocol, developed by xyazh for modular and extensible command-driven automation."


@Command(
    "[e:emun('.','/','。')]e:emun('bye','exit')]",
    sign="bye",
    desc=f"让{BOT_NAME}离开群聊",
    category="常用"
)
def bye(msg: PacketMsg, e: str):
    if msg.checkOwnerOrAdmin() and msg.group_id:
        Cqserver.instance.leaveGroup(msg.group_id)


@Command(
    "[e:emun('.','/','。')]sign",
    sign="sign",
    desc="签到，签到计数所有群通用。直接发送签到或/sign的方式就可以使用",
    category="常用"
)
@Command(
    "[e:emun('签到')]",
    sign="",
    desc="",
    category="常用",
    hidden=True
)
def sign(msg: PacketMsg, **kw):
    qq_id = msg.getId()
    user = UserDataManager(qq_id)
    last_time = user.data.get("last_time", 0)
    if (last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
        return "%s，%.2f秒前才签到过。这么快就忘了" % (msg.getName(), time.time()-last_time)
    n = user.data.get("n", 1)
    p = user.data.get("point", 1)
    ap = random.randint(int(n//2), n)
    ap = 1 if ap <= 0 else ap
    user.data["n"] = n+1
    user.data["point"] = p+ap
    user.data["last_time"] = time.time()
    return "%s，今天已签到。第%d天签到获得：%dP，今天也来见了%s呢" % (msg.getName(), n, ap, BOT_NAME)


@Command(
    "[e:emun('.','/','。')]jrrp",
    sign="jrrp",
    desc="查询当前运势，图一乐。直接发送运势或/jrrp的方式就可以使用",
    category="常用"
)
@Command(
    "[e:emun('今日人品')]",
    sign="",
    desc="",
    category="常用",
    hidden=True
)
@Command(
    "[e:emun('运势')]",
    sign="",
    desc="",
    category="常用",
    hidden=True
)
def jrrp(msg: PacketMsg, **kw):
    qq_id = msg.getId()
    user = UserDataManager(qq_id)
    last_time = user.data.get("ys_last_time", 0)
    ys = -1
    if (last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
        ys = user.data.get("ys", -1)
    flag = False
    if ys == -1:
        ys = RollHelper.presetSurpriseDistribution2()
        user.data["ys"] = ys
        user.data["ys_last_time"] = time.time()
        flag = True
    if ys <= 5:
        r = '大吉，'
        r += "今天已经测过运势了" if not flag else random.choice(
            ["在好运的帮助下不断努力吧", "运气真好", "今天运气一定非常好"])
    elif ys <= 20:
        r = '吉，'
        r += "今天已经测过运势了" if not flag else random.choice(
            ["运气不错", "今天或许能做出一些改变"])
    elif ys <= 35:
        r = '半吉，'
        r += "今天已经测过运势了" if not flag else random.choice(
            ["运气还行", "在外面转转也许不错"])
    elif ys <= 50:
        r = '小吉，'
        r += "今天已经测过运势了" if not flag else random.choice(["普通的运气", "所谓日常"])
    elif ys <= 65:
        r = '末小吉，'
        r += "今天已经测过运势了" if not flag else random.choice(["有些糟糕", "问题不大"])
    elif ys <= 80:
        r = '末吉，'
        r += "今天已经测过运势了" if not flag else random.choice(
            ["小心一点就没有问题了吧", "可能不适合出去吧", "可能不适合待在家里吧"])
    elif ys <= 95:
        r = '凶，'
        r += "今天已经测过运势了" if not flag else random.choice(["悲", "好像不太妙呢"])
    else:
        r = '大凶，'
        r += "今天已经测过运势了" if not flag else random.choice(["街上好安静啊", "大哥哥......", "打完这场仗我就会老家结婚", "听好，在我回来之前不要乱走", "已经没什么好怕的了",
                                                         "你们先走我马上就来", "身体好轻", "因为我不再是一个人了", "什么声音，我去看看", "完了，这次真的完了", "没关系，问题不大（", "嗯？是错觉吗"])
    return "%s今日的幸运指数是%i %s" % (msg.getName(), 100-ys, r)


@Command(
    "[e:emun('.','/','。')]point",
    sign="point",
    desc="查看当前点数",
    category="常用",
)
def point(msg: PacketMsg, **kw):
    qq_id = msg.getId()
    user = UserDataManager(qq_id)
    return "%s，当前拥有点数：%d" % (msg.getName(), user.data.get("point", 1))
