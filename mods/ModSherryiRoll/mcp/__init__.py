from mods.LibModRoll.roll.tools.RollHelper import RollHelper
from mods.LibModRoll.rolldata.UserRollData import UserRollData
from mods.LibModRoll.rolldata.RollConfig import RollConfig
from mods.LibModRoll.roll.Roll import Roll
from mods.LibModRoll.roll.result.RollResult import RAResult
from mods.LibModMCP.MCP import MCP
from mods.LibModRoll.roll.tools.Dice import Dice
from mods.LibModRoll.roll.tools.RandomGen import RandomGen
from ..coc7 import INSANE_TEMP, INSANE_UNCERTAIN, PHOBIA, MANIA


ROLL = Roll()
_MCP = MCP()


@_MCP.tool()
def roll(expression: str = "1d100") -> str:
    """
    掷骰子
    :param expression: 骰子表达式
    :return: 骰子结果，包含骰子结果和骰子计算步骤
    :desc: 支持+-*/等常用运算符以及d这个特殊运算符，如mdn，投掷m次面数为n的骰子；支持延拓至复数域的运算；默认表达式1d100
    :param_example: 1d100、(1+1)d23、1-(0.5*1d3)d(1+2j)/3
    :command_name: r
    """
    exp = expression.replace(" ", "")
    if not exp:
        exp = "1d100"
    config = RollConfig()
    result = ROLL.r(exp, rule=config.getRules())
    value = RollHelper.formatValue(result.value)
    step = [stp[1] for stp in result.steps]
    if len(step) > 10:
        step = step[:10]
        step.append("...")
    steps = "\r\n".join(step)
    return f"骰子结果: {exp}={value}step: {steps}"


@_MCP.tool()
def switchRule(rule: bool = None) -> str:
    """
    切换检定规则
    :param rule: True为标准规则，False为简易规则
    :return: 切换检定规则为标准规则或者简易规则
    """
    config = RollConfig()
    if rule is None:
        rule = config.getRules()
        config.setRules(not rule)
    else:
        config.setRules(rule)
    return f"#切换检定规则为{'标准' if rule else '简易'}规则"


def _rollAttribute(qq_id: int, attribute_name: str, count: int, value_or_expression: int | float | complex | str = None) -> RAResult:
    data = UserRollData(qq_id)
    card = data.getBindingCard(create=True)
    config = RollConfig()
    if isinstance(value_or_expression, (int, float, complex)):
        val = value_or_expression
    elif value_or_expression is None:
        val = card.getAttr(attribute_name, 1)
    else:
        val = ROLL.r(value_or_expression, rule=config.getRules()).value
    return ROLL.ra(attribute_name, val, count, config.getRules())


@_MCP.tool()
def rollAttribute(qq_id: int, attribute_name: str, count: int, value_or_expression: int | float | complex | str = None) -> str:
    """
    检定
    :param qq_id: 用户的qq号（5-11位的数字）
    :param attribute_name: 属性名称
    :param count: 检定次数
    :param display_value_or_expression: 值或者表达式，为None时使用用户角色卡储存的值
    :return: 检定结果
    :command_name: ra
    :desc: 检定一个属性，用户可能使用的语句（ra可能被省略）：ra 力量、ra 力量50、ra 力量1d100、ra 力量50d100、ra 力量3#50d100、ra 力量3#50d(100*2)}d(100+2j)；表达式支持+-*/等常用运算符以及d这个特殊运算符，如mdn，投掷m次面数为n的骰子；支持延拓至复数域的运算；默认表达式1d100；#前面的数字表示次数只能为int，#不是表达式的一部分
    """
    result = _rollAttribute(qq_id, attribute_name, count, value_or_expression)
    n = result.count()
    count_s = f"大成功:{n[0]}、极难成功:{n[1]}、困难成功:{n[2]}、普通成功:{n[3]}、失败:{n[4]}、大失败:{n[5]}"
    return f"进行了{count}次“{attribute_name}”检定，总结果：{result.toStr()}，统计结果：{count_s}"


@_MCP.tool()
def rollAttributeBonus(qq_id: int, attribute_name: str, count: int, value_or_expression: int | float | complex | str = None) -> str:
    """
    奖励检定
    :param qq_id: 用户的qq号（5-11位的数字）
    :param attribute_name: 属性名称
    :param count: 检定次数
    :param display_value_or_expression: 值或者表达式，为None时使用用户角色卡储存的值
    :return: 检定结果
    :command_name: rb
    :desc: 奖励检定检定一个属性，用户可能使用的语句（rb可能被省略）：rb 力量、rb 力量50、rb 力量1d100、rb 力量50d100、rb 力量3#50d100、rb 力量3#50d(100*2)}d(100+2j)；表达式支持+-*/等常用运算符以及d这个特殊运算符，如mdn，投掷m次面数为n的骰子；支持延拓至复数域的运算；默认表达式1d100；#前面的数字表示次数只能为int，#不是表达式的一部分
    """
    result = _rollAttribute(qq_id, attribute_name, count, value_or_expression)
    b = result.bonus()
    if b.level < 4:
        msg = "成功"
    else:
        msg = "失败"
    return f"进行了“{attribute_name}”奖励检定，{b.value}/{b.ref}】:{result.toStr()}|{msg}"


@_MCP.tool()
def rollAttributePunishment(qq_id: int, attribute_name: str, count: int, value_or_expression: int | float | complex | str = None) -> str:
    """
    惩罚检定
    :param qq_id: 用户的qq号（5-11位的数字）
    :param attribute_name: 属性名称
    :param count: 检定次数
    :param display_value_or_expression: 值或者表达式，为None时使用用户角色卡储存的值
    :return: 检定结果
    :command_name: rp
    :desc: 惩罚检定检定一个属性，用户可能使用的语句（rp可能被省略）：rp 力量、rp 力量50、rp 力量1d100、rp 力量50d100、rp 力量3#50d100、rp 力量3#50d(100*2)}d(100+2j)；表达式支持+-*/等常用运算符以及d这个特殊运算符，如mdn，投掷m次面数为n的骰子；支持延拓至复数域的运算；默认表达式1d100；#前面的数字表示次数只能为int，#不是表达式的一部分
    """
    result = _rollAttribute(qq_id, attribute_name, count, value_or_expression)
    p = result.punishment()
    if p.level < 4:
        msg = "成功"
    else:
        msg = "失败"
    return f"进行了“{attribute_name}”惩罚检定，{p.value}/{p.ref}】:{result.toStr()}|{msg}"


@_MCP.tool()
def setAttribute(qq_id: int, data: dict[str, int | float | complex | str]) -> str:
    """
    设置属性
    :param qq_id: 用户的qq号（5-11位的数字）
    :param data: 属性数据{属性名称:值或表达式, ...}
    :return: 设置结果
    :command_name: st
    :desc: 设置属性，用户可能使用的语句（st可能被省略）：st 力量50、st 力量50d100、st 力量50d(100*2)}d(100+2j)；表达式支持+-*/等常用运算符以及d这个特殊运算符，如mdn，投掷m次面数为n的骰子；支持延拓至复数域的运算；默认表达式1d100；用户可以同时设置多个属性
    """
    user_data = UserRollData(qq_id)
    card = user_data.getBindingCard(create=True)
    result = []
    for k, v in data.items():
        if isinstance(v, (int, float, complex)):
            v = v
        else:
            v = ROLL.r(v).value
        card.setAttr(k, v)
        result.append(f"{k}:{card.getAttr(k)}")
    if len(result) > 10:
        result = result[:10]
        result.append("...")
    return f"已设置{card.name}的属性: {', '.join(result)}"


@_MCP.tool()
def showAttribute(qq_id: int, attribute_names: list[str]) -> dict[str, str]:
    """
    显示属性
    :param qq_id: 用户的qq号（5-11位的数字）
    :param *attribute_names: 属性名称
    :return: 属性数据
    :command_name: show
    :desc: 显示最多100条属性，用户可能使用的语句（show可能被省略）：show 力量；用户可同时获取多个属性
    """
    data = UserRollData(qq_id)
    card = data.getBindingCard(create=True)
    result = {}
    count = 0
    for arr in attribute_names:
        val = card.getAttr(arr)
        if val is None:
            continue
        result[arr] = str(val)
        count += 1
        if count > 100:
            break
    return result


@_MCP.tool()
def playerCardNew(qq_id: int, card_name: str = "空白卡") -> str:
    """
    创建角色卡
    :param qq_id: 用户的qq号（5-11位的数字）
    :param card_name: 角色卡名称
    :return: 创建结果
    :command_name: pc new
    :desc: 创建角色卡，用户可能使用的语句（pc new可能被省略）：pc new 角色卡名称
    """
    data = UserRollData(qq_id)
    if len(data.cardsList()) >= 25:
        return "已超过25张角色卡，请删除后再创建"
    card = data.createCard(card_name)
    return f"已创建角色卡：{card.name}"


@_MCP.tool()
def playerCardBind(qq_id: int, card_name: str = "空白卡") -> str:
    """
    绑定角色卡
    :param qq_id: 用户的qq号（5-11位的数字）
    :param card_name: 角色卡名称
    :return: 绑定结果
    :command_name: pc bind
    :desc: 绑定角色卡，用户可能使用的语句（pc bind可能被省略）：pc bind 角色卡名称
    """
    data = UserRollData(qq_id)
    card = data.getCard(card_name)
    if not card:
        return f"未找到角色卡: {card_name}"
    data.bindCard(card)
    return f"已绑定到角色卡: {card.name}"


@_MCP.tool()
def playerCardList(qq_id: int) -> str:
    """
    列出角色卡
    :param qq_id: 用户的qq号（5-11位的数字）
    :return: 角色卡列表
    :command_name: pc list
    :desc: 列出角色卡，用户可能使用的语句：pc list
    """
    data = UserRollData(qq_id)
    li = ",".join([card.name for card in data.cardsList()])
    return f"当前拥有的角色卡: {li}"


@_MCP.tool()
def playerCardDelte(qq_id: int, card_name: str) -> str:
    """
    删除角色卡
    :param qq_id: 用户的qq号（5-11位的数字）
    :param card_name: 角色卡名称
    :return: 删除结果
    :command_name: pc del
    :desc: 删除角色卡，用户可能使用的语句（pc del可能被省略）：pc del 角色卡名称
    """
    data = UserRollData(qq_id)
    card = data.getCard(card_name)
    if not card:
        return f"未找到角色卡: {card_name}"
    data.removeCard(card_name)
    return f"已删除角色卡: {card.name}"


@_MCP.tool()
def playerCardNewName(qq_id: int, new_card_name: str) -> str:
    """
    重命名角色卡
    :param qq_id: 用户的qq号（5-11位的数字）
    :param new_card_name: 新的角色卡名称
    :return: 重命名结果
    :command_name: pc nn
    :desc: 重命名角色卡，用户可能使用的语句（pc nn可能被省略）：pc nn 新的角色卡名称
    """
    data = UserRollData(qq_id)
    card = data.getBindingCard(create=True)
    card.name = new_card_name
    return f"角色卡已重命名为: {card.name}"


@_MCP.tool()
def playerCardCopy(qq_id: int, card_name1: str = "", card_name2: str = "") -> str:
    """
    复制角色卡
    :param qq_id: 用户的qq号（5-11位的数字）
    :param card_name1: 目标角色卡名称
    :param card_name2: 源角色卡名称
    :return: 复制结果
    :command_name: pc copy
    :desc: 将角色卡2的属性赋值到角色卡1，用户可能使用的语句（pc copy可能被省略）：pc copy 目标角色卡名称 源角色卡名称
    """
    data = UserRollData(qq_id)
    card1 = data.getCard(card_name1)
    card2 = data.getCard(card_name2)
    if not card2:
        return f"未找到角色卡: {card_name2}"
    if not card1:
        if len(data.cardsList()) >= 25:
            return f"未找到{card_name1}，且已超过25张角色卡，无法创建"
        card1 = data.createCard(card_name1)
    card1.copyFrom(card2)
    return f"已复制角色卡: {card2.name}到{card1.name}"


@_MCP.tool()
def playerCardShow(qq_id: int, card_name: str) -> str:
    """
    显示角色卡属性
    :param qq_id: 用户的qq号（5-11位的数字）
    :param card_name: 角色卡名称
    :return: 角色卡数据
    :command_name: pc show
    :desc: 显示角色卡，用户可能使用的语句（pc show可能被省略）：pc show 角色卡名称
    """
    data = UserRollData(qq_id)
    if not card_name:
        card = data.getBindingCard(create=True)
    else:
        card = data.getCard(card_name)
    if not card:
        return f"未找到角色卡: {card_name}"
    return f"当前角色卡: {card.toData()}"


@_MCP.tool()
def tempMadness() -> str:
    """
    临时疯狂
    :return: 临时疯狂描述
    :command_name: ti
    :desc: 临时疯狂描述，用户可能使用的语句：ti
    """
    rand = RandomGen()
    name, desc = rand.choice(*INSANE_TEMP)
    return f"临时疯狂-{name}：{desc}"


@_MCP.tool()
def summarizeMadness() -> str:
    """
    总结疯狂
    :return: 总结疯狂描述
    :command_name: li
    :desc: 总结疯狂描述，用户可能使用的语句：li
    """
    rand = RandomGen()
    name, desc = rand.choice(*INSANE_UNCERTAIN)
    return f"总结疯狂-{name}：{desc}"


@_MCP.tool()
def phobia() -> str:
    """
    恐惧症
    :return: 恐惧症描述
    :command_name: ph
    :desc: 恐惧症描述，用户可能使用的语句：ph
    """
    rand = RandomGen()
    result = rand.choice(*PHOBIA)
    name, desc = result
    dice = Dice()
    duration = dice.dInt(1, 10).values[0]
    return f"恐惧症-{name}: {desc} 持续1d10={duration}小时"


@_MCP.tool()
def mania() -> str:
    """
    狂躁症
    :return: 狂躁症描述
    :command_name: ma
    :desc: 狂躁症描述，用户可能使用的语句：ma
    """
    rand = RandomGen()
    result = rand.choice(*MANIA)
    name, desc = result
    dice = Dice()
    duration = dice.dInt(1, 10).values[0]
    return f"狂躁症-{name}: {desc} 持续1d10={duration}小时"
