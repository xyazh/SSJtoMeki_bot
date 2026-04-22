from mods.LibModRoll.roll.tools.RollHelper import RollHelper
from mods.LibModRoll.rolldata.UserRollData import UserRollData
from mods.LibModRoll.rolldata.RollConfig import RollConfig
from mods.LibModRoll.roll.Roll import Roll
from mods.LibModCommand.command.Command import Command
from xyacqbot.helper.RollHelper import RollHelper as XRollHelper
import time
import random
from xyacqbot.datamanager.UserDataManager import UserDataManager
from xyacqbot.CommandDLS import CommandDLS
from xyacqbot.xyazhServer.ConsoleMessage import ConsoleMessage
from mods.LibModMCP.MCP import MCP


import random
import time


BOT_NAME = "Meki"

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


@_MCP.tool()
def rollAttribute(qq_id: int, attribute_name: str, count: int, value_or_expression: int | float | complex | str = None) -> str:
    """
    检定
    :param qq_id: QQ号
    :param attribute_name: 属性名称
    :param count: 检定次数
    :param display_value_or_expression: 值或者表达式，为None时使用用户角色卡储存的值
    :return: 检定结果
    :command_name: ra
    :desc: 检定一个属性，用户可能使用的语句（ra可能被省略）：ra 力量、ra 力量50、ra 力量1d100、ra 力量50d100、ra 力量3#50d100、ra 力量3#50d(100*2)}d(100+2j)；表达式支持+-*/等常用运算符以及d这个特殊运算符，如mdn，投掷m次面数为n的骰子；支持延拓至复数域的运算；默认表达式1d100；#前面的数字表示次数只能为int，#不是表达式的一部分
    """
    data = UserRollData(qq_id)
    card = data.getBindingCard(create=True)
    config = RollConfig()
    if isinstance(value_or_expression, (int, float, complex)):
        val = value_or_expression
    elif value_or_expression is None:
        val = card.getAttr(attribute_name, 1)
    else:
        val = ROLL.r(value_or_expression, rule=config.getRules()).value
    result = ROLL.ra(attribute_name, val, count, config.getRules())
    n = result.count()
    count_s = f"大成功:{n[0]}、极难成功:{n[1]}、困难成功:{n[2]}、普通成功:{n[3]}、失败:{n[4]}、大失败:{n[5]}"
    return f"进行了{count}次“{attribute_name}”检定，总结果：{result.toStr()}，统计结果：{count_s}"