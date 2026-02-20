import random
import time

from xyacqbot.packet.PacketMsg import PacketMsg
from xyacqbot.helper.RollHelper import RollHelper as XRollHelper
from mods.LibModCommand.command.Command import Command
from mods.LibModRoll.roll.Roll import Roll
from mods.LibModRoll.rolldata.RollConfig import RollConfig
from mods.LibModRoll.rolldata.UserRollData import UserRollData
from mods.LibModRoll.roll.tools.RollHelper import RollHelper
from .msg import D, D0, D1, D2, D3, D4, D5, D6, D7, D8, D9


BOT_NAME = "Meki"

ROLL = Roll()


@Command(
    "[e:emun('.','/','。')]r[exp:str]",
    sign="r [exp:str]",
    desc="投骰子，支持延拓至复数域的运算，默认1d100",
    category="跑团"
)
def r(msg: PacketMsg, e: str, exp: str = ""):
    exp = exp.replace(" ", "")
    if not exp:
        exp = "1d100"
    if exp[0] in ("a", "b", "p"):
        return
    config = RollConfig()
    try:
        result = ROLL.r(exp, rule=config.getRules())
        value = RollHelper.foramtValue(result.value)
        step = [stp[1] for stp in result.steps]
        if len(step) > 10:
            step = step[:10]
            step.append("...")
        steps = "\r\n".join(step)
        return f"{msg.getName()}投了骰子: \r\n{exp}={value}\r\nstep: {steps}"
    except Exception as e:
        return f"哈？杂鱼大哥哥怎么骰子都不会骰？\r\n{e}"


@Command(
    "[e:emun('.','/','。')][ra:emun('ra','ra '][count:int]#[arr:str]",
    sign="ra [count:int]#[arr:str]",
    desc="检定一个属性, #前表示检定次数",
    category="跑团",
)
@Command(
    "[e:emun('.','/','。')][ra:emun('ra','ra '][arr:str]",
    sign="ra [arr:str]",
    desc="检定一个属性",
    category="跑团",
)
def ra(msg: PacketMsg, e: str, ra: str, count: int = 1, arr: str = ""):
    if not arr:
        return
    if "#" in arr:
        return
    if XRollHelper.reFind(r"(\D+\d+)", arr):
        key = ""
        value = ""
        for attribute in arr:
            if attribute.isdigit():
                value += attribute
                continue
            key += attribute
        arr = key
        val = int(value)
    else:
        data = UserRollData(msg.getId())
        card = data.getBindingCard(create=True)
        val = card.getAttr(arr, 0)
    config = RollConfig()
    result = ROLL.ra(arr, val, count, config.getRules())
    level = result.rollResults().__next__().level
    d: D = [D0, D1, D2, D3, D4, D5][level]
    if count == 1:
        return f"#命运之书为“{msg.getName()}”进行了“{arr}”检定，\r\n#字符精灵为你呈现出:#【{result.toStr()}】:\r\n# Meki：{d.choice()}"
    n = result.count()
    count_s = f"大成功:{n[0]}、极难成功:{n[1]}、困难成功:{n[2]}、普通成功:{n[3]}、失败:{n[4]}、大失败:{n[5]}"
    return f"#命运之书为“{msg.getName()}”进行了{count}次“{arr}”检定，\r\n#字符精灵为你呈现出:#【{result.toStr()}】:\r\n# Meki：让我看看都有些啥\r\n# {count_s}"


@Command(
    "[e:emun('.','/','。')][rb:emun('rb','rb '][count:int]#[arr:str]",
    sign="rb [count:int]#[arr:str]",
    desc="奖励骰, #前表示检定次数",
    category="跑团",
)
@Command(
    "[e:emun('.','/','。')][rb:emun('rb','rb '][arr:str]",
    sign="rb [arr:str]",
    desc="奖励骰，默认两次取最小",
    category="跑团",
)
def rb(msg: PacketMsg, e: str, rb: str, count: int = 2, arr: str = ""):
    if not arr:
        return
    if "#" in arr:
        return
    if XRollHelper.reFind(r"(\D+\d+)", arr):
        key = ""
        value = ""
        for attribute in arr:
            if attribute.isdigit():
                value += attribute
                continue
            key += attribute
        arr = key
        val = int(value)
    else:
        data = UserRollData(msg.getId())
        card = data.getBindingCard(create=True)
        val = card.getAttr(arr, 0)
    config = RollConfig()
    result = ROLL.ra(arr, val, count, config.getRules())
    b = result.bonus()
    if b.level < 4:
        meki_msg = D6.choice()
    else:
        meki_msg = D7.choice()
    return f"#福音之书为“{msg.getName()}”进行了“{arr}”祝福检定，\r\n#神圣精灵为你呈现出【{b.value}/{b.ref}】:\r\n#{result.toStr()}\r\nMeki：{meki_msg}\r\n"


@Command(
    "[e:emun('.','/','。')][rp:emun('rp','rp '][count:int]#[arr:str]",
    sign="rp [count:int]#[arr:str]",
    desc="惩罚骰, #前表示检定次数",
    category="跑团",
)
@Command(
    "[e:emun('.','/','。')][rp:emun('rp','rp '][arr:str]",
    sign="rp [arr:str]",
    desc="惩罚骰，默认两次取最大",
    category="跑团",
)
def rp(msg: PacketMsg, e: str, rp: str, count: int = 2, arr: str = ""):
    if not arr:
        return
    if "#" in arr:
        return
    if XRollHelper.reFind(r"(\D+\d+)", arr):
        key = ""
        value = ""
        for attribute in arr:
            if attribute.isdigit():
                value += attribute
                continue
            key += attribute
        arr = key
        val = int(value)
    else:
        data = UserRollData(msg.getId())
        card = data.getBindingCard(create=True)
        val = card.getAttr(arr, 0)

    config = RollConfig()
    result = ROLL.ra(arr, val, count, config.getRules())
    config = RollConfig()
    result = ROLL.ra(arr, val, count, config.getRules())
    b = result.punishment()
    if b.level < 4:
        meki_msg = D8.choice()
    else:
        meki_msg = D9.choice()
    return f"#灾厄之书为“{msg.getName()}”进行了“{arr}”诅咒检定，\r\n#黯殇精灵为你呈现出【{b.value}/{b.ref}】:\r\n#{result.toStr()}\r\nMeki：{meki_msg}\r\n"


@Command(
    "[e:emun('.','/','。')][st:emun('st','st '][arr:str]",
    sign="st [arr:str]",
    desc="设置角色卡的属性",
    category="跑团",
)
def st(msg: PacketMsg, e: str, st: str, arr: str = ""):
    if not arr:
        return
    data = UserRollData(msg.getId())
    card = data.getBindingCard(create=True)
    result = card.setAttrFromDSL(arr)[1]
    if len(result) > 10:
        result = result[:10]
        result.append("...")
    return f"已设置{card.name}的属性: \r\n{', '.join(result)}"


@Command(
    "[e:emun('.','/','。')][show:emun('show','show '][arr:str]",
    sign="show [arr:str]",
    desc="查看属性值",
    category="跑团",
)
def show(msg: PacketMsg, e: str, show: str, arr: str):
    data = UserRollData(msg.getId())
    card = data.getBindingCard(create=True)
    return f"{card.name}: {arr}{card.getAttr(arr)}"


@Command(
    "[e:emun('.','/','。')][pc:emun('pc','pc ')][new:emun('new','new ')][name:str]",
    sign="pc new [name:str]",
    desc="创建一张默认角色卡，最多25张",
    category="跑团",
)
def pcnew(msg: PacketMsg, name: str = "", **kw):
    if not name:
        name = "空白卡"
    data = UserRollData(msg.getId())
    if len(data.cardsList()) >= 25:
        return "已超过25张角色卡，请删除后再创建"
    card = data.createCard(name)
    return f"已创建角色卡：{card.name}"


@Command(
    "[e:emun('.','/','。')][pc:emun('pc','pc ')][bind:emun('bind','bind ','tag','tag ')][name:str]",
    sign="pc bind [name:str]",
    desc="设置为当前使用的角色卡",
    category="跑团",
)
def pcbind(msg: PacketMsg, name: str = "", **kw):
    if not name:
        name = "空白卡"
    data = UserRollData(msg.getId())
    card = data.getCard(name)
    if not card:
        return f"未找到角色卡: {name}"
    data.bindCard(card)
    return f"已绑定到角色卡: {card.name}"


@Command(
    "[e:emun('.','/','。')][pc:emun('pc','pc ')][list:emun('list','list ','grp','grp ')]",
    sign="pc list",
    desc="拥有的角色卡列表",
    category="跑团",
)
def pclist(msg: PacketMsg, **kw):
    data = UserRollData(msg.getId())
    li = "\r\n".join([card.name for card in data.cardsList()])
    return f"当前拥有的角色卡: \r\n{li}"


@Command(
    "[e:emun('.','/','。')][pc:emun('pc','pc ')][del:emun('del','del ')][name:str]",
    sign="pc del [name:str]",
    desc="删除角色卡",
    category="跑团",
)
def pcdel(msg: PacketMsg, name: str = "", **kw):
    data = UserRollData(msg.getId())
    card = data.getCard(name)
    if not card:
        return f"未找到角色卡: {name}"
    data.removeCard(name)
    return f"已删除角色卡: {card.name}"


@Command(
    "[e:emun('.','/','。')][pc:emun('pc','pc ')][nn:emun('nn','nn ')][name:str]",
    sign="pc nn [name:str]",
    desc="重命名当前角色卡",
    category="跑团",
)
def pcnn(msg: PacketMsg, name: str = "", **kw):
    data = UserRollData(msg.getId())
    card = data.getBindingCard(create=True)
    card.name = name
    return f"角色卡已重命名为: {card.name}"


@Command(
    "[e:emun('.','/','。')][pc:emun('pc','pc ')][copy:emun('copy','copy ','cpy','cpy ')][name1:str]=[name2:str]",
    sign="pc copy [name1:str]=[name2:str]",
    desc="将角色卡2的属性赋值到角色卡1",
    category="跑团",
)
def pccopy(msg: PacketMsg, name1: str = "", name2: str = "", **kw):
    data = UserRollData(msg.getId())
    card1 = data.getCard(name1)
    card2 = data.getCard(name2)
    if not card2:
        return f"未找到角色卡: {name2}"
    if not card1:
        card1 = data.createCard(name1)
    card1.copyFrom(card2)
    return f"已复制角色卡: {card2.name}到{card1.name}"


@Command(
    "[e:emun('.','/','。')][pc:emun('pc','pc ')][show:emun('show','show ')][name:str]",
    sign="pc show [name:str]",
    desc="查看角色卡数据",
    category="跑团",
)
def pcshow(msg: PacketMsg, name: str = "", **kw):
    data = UserRollData(msg.getId())

    if not name:
        card = data.getBindingCard(create=True)
    else:
        card = data.getCard(name)
    if not card:
        return f"未找到角色卡: {name}"
    card.toData()
    return f"当前角色卡: \r\n{card.toData()}"
