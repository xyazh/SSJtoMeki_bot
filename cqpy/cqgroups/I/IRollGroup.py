from ..BaseGroup import BaseGroup
from .IBaseGroup import IBaseGroup
import random
from ...Order import Order
from ...GroupHelper import GroupHelper
from ...GameSystem.PlayerSystem.Player import Player
from ...GameSystem.Helper import RollHelper
from ...IType import *
from ...I18n.I18n import I18n
from ...CQCode import CQCodeHelper


class IRollGroup(IBaseGroup):
    vanilla_ra_rule: bool = True
    daiseikou: int = 5
    daishippai: int = 96

    @staticmethod
    def safeRoll(base_group: BaseGroup, fuc: Callable, arg: str) -> int | float | complex | None:
        result = None
        try:
            result = fuc(arg)
        except ZeroDivisionError:
            base_group.server.sendGroup(
                base_group.group_id, I18n.format("safeRoll_1"))
        except OverflowError:
            base_group.server.sendGroup(
                base_group.group_id, I18n.format("safeRoll_2"))
        except BaseException:
            base_group.server.sendGroup(
                base_group.group_id, I18n.format("safeRoll_3"))
        return result

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "创建角色", "new_card", "new_card [name]", "创建一张新卡")
    def nc(self, data: dict, order: Order):
        if order.checkOrder("new_card"):
            card_name = order.getArg(1)
            if not card_name:
                card_name = "空白卡"
            if len(card_name) > 30:
                self.server.sendGroup(
                    self.group_id, "名字太长了，%s记不住的" % (BaseGroup.BOT_NAME_SELF))
                return
            qq_id = GroupHelper.getId(data)
            player = Player(qq_id)
            player.creatCard(card_name, {})
            self.server.sendGroup(self.group_id, "是叫%s吧，%s知道了" % (
                card_name, BaseGroup.BOT_NAME_SELF))

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "绑定角色", "bind_card", "bind_card [name]", "绑定角色卡")
    def bindCard(self, data: dict, order: Order):
        if order.checkOrder("bind_card"):
            card_name = order.getArg(1)
            if not card_name:
                card_name = "空白卡"
            qq_id = GroupHelper.getId(data)
            player = Player(qq_id)
            if player.bindCard(card_name):
                self.server.sendGroup(self.group_id, "%s已绑定" % card_name)
            else:
                self.server.sendGroup(self.group_id, "我找找，我找找...咦？怎么没有")

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "角色列表", "list_card", "list_card", "获取角色卡列表")
    def cardList(self, data: dict, order: Order):
        if order.checkOrder("list_card"):
            qq_id = GroupHelper.getId(data)
            player = Player(qq_id)
            chara_cards = player.getCardsList()
            msg = "%s当前拥有角色卡：" % GroupHelper.getName(data)
            for i in chara_cards:
                msg += "\r\n%s" % i
            self.server.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "删除角色", "del_card", "del_card [name]", "删除角色卡，如果删除的角色卡正被绑定则会绑定空白卡")
    def delCard(self, data: dict, order: Order):
        if order.checkOrder("del_card"):
            card_name = order.getArg(1)
            msg = "好像没有这张卡呢"
            if card_name == "空白卡":
                msg = "空白卡无法被删除"
            elif card_name:
                qq_id = GroupHelper.getId(data)
                player = Player(qq_id)
                if player.delCard(card_name):
                    msg = "已删除%s" % card_name
            self.server.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "角色管理", "pc", "pc (new|tag|bind|list|del|rm)", "pc指令用于管理角色卡\r\n没有参数时输出当前角色卡,各项参数说明：\r\n创建角色：new [name]\r\n绑定角色：bind|tag [name]\r\n角色列表：list\r\n删除角色：del|rm [name]\r\n")
    def pc(self, data: dict, order: Order):
        if order.checkOrder("pc"):
            operate = order.getArg(1)
            card_name = order.getArg(2)
            card_name = card_name if card_name else ""
            if operate == None:
                qq_id = GroupHelper.getId(data)
                player = Player(qq_id)
                binded_chara = player.getBindedCardName()
                self.server.sendGroup(
                    self.group_id, "当前绑定的角色卡是%s" % binded_chara)
            elif operate == "new":
                order2 = GroupHelper.getOrderFromStr(
                    GroupHelper.ORDER_SPLIT_LIST[0] + "new_card %s" % card_name)
                self.nc(data, order2)
            elif operate in ("tag", "bind"):
                order2 = GroupHelper.getOrderFromStr(
                    GroupHelper.ORDER_SPLIT_LIST[0] + "bind_card %s" % card_name)
                self.bindCard(data, order2)
            elif operate == "list":
                order2 = GroupHelper.getOrderFromStr(
                    GroupHelper.ORDER_SPLIT_LIST[0] + "list_card")
                self.cardList(data, order2)
            elif operate in ("del", "rm"):
                order2 = GroupHelper.getOrderFromStr(
                    GroupHelper.ORDER_SPLIT_LIST[0] + "del_card %s" % card_name)
                self.delCard(data, order2)
            else:
                pass

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "设置属性", "st", "st [ATTRnumber...] (target)", "st指令用于设置计算角色属性，支持算数运算")
    def st(self, data: dict, order: Order):
        if order.checkOrder("st"):
            attribute_text = order.getArg(1)
            if not attribute_text:
                self.server.sendGroup(self.group_id, I18n.format("has_help"))
                return
            qq_id = GroupHelper.getId(data)
            qq_msg = GroupHelper.getMsg(data)
            cq_codes = CQCodeHelper.creatCQCodeFromMsg(qq_msg)
            at_id_set = set()
            for cq_code in cq_codes:
                if cq_code.t == "at":
                    at_id_set.add(cq_code.data["qq"])
            at_id_list = list(at_id_set)
            if len(at_id_list) > 0:
                qq_id = at_id_list[0]
            player = Player(qq_id)
            if RollHelper.findsStr(attribute_text, ["+", "-", "*", "/", "%", "^", "(", ")", "|"]):
                card = player.getBindedCardNotNone()
                key = ""
                for attribute in card:
                    if attribute_text.startswith(attribute):
                        key = attribute
                if key == "":
                    self.server.sendGroup(
                        self.group_id, I18n.format("has_help"))
                    return
                for attribute in card:
                    attribute_text = attribute_text.replace(
                        attribute, str(card[attribute]))
                flag = ""
                for attribute in attribute_text:
                    if not attribute in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "%", "^", "d", "D", "(", ")", ".", "i", "j", "|"]:
                        flag += attribute
                if flag != "":
                    self.server.sendGroup(self.group_id, "没有找到属性:%s" % flag)
                    return
                roll_result = IRollGroup.safeRoll(
                    self, RollHelper.evaluateExpressionToFloat, attribute_text)
                if roll_result == None:
                    return
                roll_result = int(roll_result)
                player.setBindedCardArr({key: roll_result})
                self.server.sendGroup(self.group_id, "%s设置%s=%s=%d" % (
                    GroupHelper.getName(data), key, attribute_text, roll_result))
            else:
                player.addBindedCardAsStr(attribute_text)
                self.server.sendGroup(self.group_id, "%s记住了" %
                                      BaseGroup.BOT_NAME_SELF)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "属性检定", "ra", "ra [ARR]", "ra指令用于检定")
    def ra(self, data: dict, order: Order):
        if order.checkOrder("ra"):
            attributes_or_value: str = order.getArg(1)
            if attributes_or_value == None:
                self.server.sendGroup(self.group_id, I18n.format("has_help"))
                return
            elif attributes_or_value.isdigit():
                key = ""
                value = int(attributes_or_value)
            elif RollHelper.reFind(r"(\D+\d+)", attributes_or_value):
                key = ""
                value = ""
                for attribute in attributes_or_value:
                    if attribute.isdigit():
                        value += attribute
                        continue
                    key += attribute
                value = int(value)
            else:
                key = attributes_or_value
                qq_id = GroupHelper.getId(data)
                player = Player(qq_id)
                value = player.getBindedCardVal(key)
                if value == None:
                    self.server.sendGroup(self.group_id, "好像没有%s这个属性" % key)
                    return
            roll_result = random.randint(1, 100)
            msg = I18n.format("ra_kantei") % (
                GroupHelper.getName(data), key, roll_result, value)
            if self.vanilla_ra_rule:
                if roll_result == 1:
                    msg += I18n.format("ra_meki_daiseiko")
                elif roll_result <= value/5:
                    msg += I18n.format("ra_meki_kyokunan")
                elif roll_result <= value/2:
                    msg += I18n.format("ra_meki_konnan")
                elif roll_result <= value:
                    msg += I18n.format("ra_meki_huutsuu")
                elif roll_result <= 95:
                    msg += I18n.format("ra_meki_shippai")
                elif roll_result <= 99:
                    if value >= 50:
                        msg += I18n.format("ra_meki_shippai")
                    else:
                        msg += I18n.format("ra_meki_daishippai")
                else:
                    msg += I18n.format("ra_meki_daishippai")
            else:
                if roll_result <= value:
                    if roll_result <= self.daiseikou:
                        msg += I18n.format("ra_meki_daiseiko")
                    elif roll_result <= value/5:
                        msg += I18n.format("ra_meki_kyokunan")
                    elif roll_result <= value/2:
                        msg += I18n.format("ra_meki_konnan")
                    else:
                        msg += I18n.format("ra_meki_huutsuu")
                else:
                    if roll_result >= self.daishippai:
                        msg += I18n.format("ra_meki_daishippai")
                    else:
                        msg += I18n.format("ra_meki_shippai")
            self.server.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "检定规则", "ra_rule", "ra_rule [vanilla|true|custom|false|daiseikou|daishippai|dsk|dsp] (number)", "ra_rule指令用于检定")
    def raRule(self, data: dict, order: Order):
        if order.checkOrder("ra_rule"):
            rule_option = order.getArg(1)
            if rule_option in ("vanilla", "true"):
                self.vanilla_ra_rule = True
                self.server.sendGroup(self.group_id, "ra将使用原版规则")
            elif rule_option in ("custom", "false"):
                self.vanilla_ra_rule = False
                self.server.sendGroup(self.group_id, "ra将使用自定义规则")
            elif rule_option in ("daiseikou", "dsk"):
                value = order.getArg(2)
                if not value.isdigit():
                    self.server.sendGroup(
                        self.group_id, I18n.format("has_help"))
                    return
                value = int(value)
                if value > 50 or value < 1:
                    self.server.sendGroup(self.group_id, "大成功值应该在0以上50及以下")
                    return
                self.daiseikou = value
                self.server.sendGroup(self.group_id, "ra结果%d以下将为大成功" % value)
            elif rule_option in ("daishippai", "dsp"):
                value = order.getArg(2)
                if not value.isdigit():
                    self.server.sendGroup(
                        self.group_id, I18n.format("has_help"))
                    return
                value = int(value)
                if value > 100 or value < 51:
                    self.server.sendGroup(self.group_id, "大失败值应该在50以上100及以下")
                    return
                self.daishippai = value
                self.server.sendGroup(self.group_id, "ra结果%d以上将为大失败" % value)
            else:
                self.server.sendGroup(self.group_id, I18n.format("has_help"))

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "骰个骰子", "r", "r [xdy*...]", "r指令用于roll点，支持复数域的算数运算 ，默认1d100")
    def r(self, data: dict, order: Order):
        if order.checkOrder("r"):
            expression = order.getArg(1)
            if not expression:
                expression = "1d100"
            roll_result = IRollGroup.safeRoll(
                self, RollHelper.evaluateExpression, expression)
            if roll_result == None:
                return
            self.server.sendGroup(self.group_id, "%s投了骰子：\r\n%s=%s" %
                                  (GroupHelper.getName(data), expression, roll_result))

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "coc7作成", "coc", "coc (number) (point)", "coc指令用于自动角色卡作成，number代表需要作成多少张卡（默认1张，最多5张），point表示设置的最大点数（默认随机400-500高斯分布）")
    def coc(self, data: dict, order: Order):
        if not order.checkOrder("coc"):
            return
        number, point = order.getArgs(1, 2)
        number = 1
        if isinstance(number, str) and number.isdigit():
            number = min(int(number), 5)
        card_list = []
        for card in range(number):
            min_point = 8 * 20
            point = 0
            if isinstance(point, str) and point.isdigit():
                point = int(point)
            else:
                roll_result = int(RollHelper.bestRandomGuass(450, 25, 2))
                roll_result -= int(roll_result % 5)
                point = roll_result
            if point < min_point:
                n = int(point // 5)
                card_list.append(
                    tuple(map(lambda x: x*5, RollHelper.randomSplitInt(n, 8, 15))))
            else:
                lost_point = point - min_point
                n = int(lost_point // 5)
                card_list.append(
                    tuple(map(lambda x: x*5 + 20, RollHelper.randomSplitInt(n, 8, 15))))
        msg = "%s的角色卡作成：" % GroupHelper.getName(data)
        for card in card_list:
            roll_result = int(RollHelper.bestRandomGuass(50, 25, 2))
            roll_result -= int(roll_result % 5)
            total = sum(card)
            msg += " \r\n\r\n力量%s体质%s体型%s敏捷%s外貌%s智力%s意志%s教育%s" % card + \
                "幸运%s 共计[%s/%s]" % (roll_result, total, total + roll_result)
        self.server.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "主持管理", "kp", "kp [set|ban] (target)", "设置kp")
    def setKp(self, data: dict, order: Order):
        if not order.checkOrder("kp"):
            return
        if not GroupHelper.checkOwnerOrAdmin(data):
            self.server.sendGroup(self.group_id, "只有群主或管理员可以指定kp")
            return
        arg1 = order.getArg(1)
        msg = GroupHelper.getMsg(data)
        qq_id = GroupHelper.getId(data)
        cq_codes = CQCodeHelper.creatCQCodeFromMsg(msg)
        at_ids = set()
        for i in cq_codes:
            if i.t == "at":
                at_ids.add(i.data["qq"])
        at_ids = list(at_ids)
        if len(at_ids) <= 0:
            at_ids.append(qq_id)
        print(arg1)
        if arg1 == "set":
            for i in at_ids:
                player = Player(i)
                player.setKp(True)
                self.server.sendGroup(self.group_id, "成功指定kp")
        elif arg1 == "ban":
            for i in at_ids:
                player = Player(i)
                player.setKp(False)
                self.server.sendGroup(self.group_id, "成功取消kp")
        else:
            self.server.sendGroup(self.group_id, I18n.format("has_help"))

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "玩家管理", "pl", "pl [join|leave|clear] [targets]...", "设置pl")
    def kpSetPl(self, data: dict, order: Order):
        if not order.checkOrder("pl"):
            return
        qq_id = GroupHelper.getId(data)
        kp_player = Player(qq_id)
        if not kp_player.isKp():
            self.server.sendGroup(self.group_id, "只有kp可以用此命令")
            return
        arg = order.getArg(1)
        if not arg in ("join", "leave", "clear"):
            self.server.sendGroup(self.group_id, I18n.format("has_help"))
            return
        msg = GroupHelper.getMsg(data)
        cq_codes = CQCodeHelper.creatCQCodeFromMsg(msg)
        at_ids = set()
        for i in cq_codes:
            if i.t == "at":
                at_ids.add(i.data["qq"])
        at_ids = list(at_ids)
        if len(at_ids) <= 0:
            at_ids.append(qq_id)
        pls: dict = kp_player.writeGet("pls", {})
        if arg == "join":
            for i in at_ids:
                pls[i] = 1
            self.server.sendGroup(self.group_id, "已添加玩家")
        elif arg == "leave":
            for i in at_ids:
                if i in pls:
                    pls.pop(i)
            self.server.sendGroup(self.group_id, "已退出玩家")
        elif arg == "clear":
            pls.clear()
            self.server.sendGroup(self.group_id, "已清空玩家")

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "设置物品", "set_item", "set_item [ItemNumber...] (targets)...", "kp设置物品")
    def kpSetItem(self, data: dict, order: Order):
        if not order.checkOrder("set_item"):
            return
        qq_id = GroupHelper.getId(data)
        kp_player = Player(qq_id)
        if not kp_player.isKp():
            self.server.sendGroup(self.group_id, "只有kp可以用此命令")
            return
        arg = order.getArg(1)
        if not arg:
            self.server.sendGroup(self.group_id, I18n.format("has_help"))
            return
        d = RollHelper.decodeArrStr(arg)
        msg = GroupHelper.getMsg(data)
        cq_codes = CQCodeHelper.creatCQCodeFromMsg(msg)
        at_ids = set()
        for i in cq_codes:
            if i.t == "at":
                at_ids.add(i.data["qq"])
        at_ids = list(at_ids)
        if len(at_ids) <= 0:
            at_ids.append(qq_id)
        for p in at_ids:
            player = Player(p)
            for i in d:
                player.setItemNumberTotBindedChara(i, int(d[i]))
        self.server.sendGroup(self.group_id, "物品设置完毕")

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "检定变更", "[ARR]", "[ARR] [xdy*...|xdy*...]", "对属性进行检定，若成功执行|左边的内容，失败则执行|右边的内容")
    def rollCheck(self, data: dict, order: Order):
        qq_id = GroupHelper.getId(data)
        player = Player(qq_id)
        card = player.getBindedCardNotNone()
        order_str = order.getOrderStr()
        if order_str not in card:
            return
        arg = order.getArg(1)
        xdys = arg.split("|")
        if len(xdys) == 1:
            xdys = ["1", xdys[0]]
        elif len(xdys) < 2:
            self.server.sendGroup(self.group_id, I18n.format("has_help"))
            return
        val = card[order_str]
        rc = random.randint(1, 100)
        msg = I18n.format("ra_kantei") % (
            GroupHelper.getName(data), order_str, rc, val)
        if rc <= val:
            r = IRollGroup.safeRoll(
                self, RollHelper.evaluateExpression, xdys[0])
            if r == None:
                return
            r = int(r)
            msg += I18n.format("ra_meki_huutsuu")
            msg += "\r\n（你的“%s”变更为【%s%s=%s】）" % (
                order_str, val, "+%s" % r if r >= 0 else "%s" % r, val+r)
            player.setBindedCardArr({order_str: val+r})
        else:
            r = IRollGroup.safeRoll(
                self, RollHelper.evaluateExpression, xdys[1])
            if r == None:
                return
            r = int(r)
            msg += I18n.format("ra_meki_shippai")
            msg += "\r\n（你的“%s”变更为【%s%s=%s】）" % (
                order_str, val, "+%s" % r if r >= 0 else "%s" % r, val+r)
            player.setBindedCardArr({order_str: val+r})
        self.server.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "奖励骰子", "rb", "rb [ARR](number)", "对属性进行奖励骰检定，可设定投骰子次数取最小值，默认骰两次。")
    def rollBenefits(self, data: dict, order: Order):
        if order.checkOrder("rb"):
            player = Player(GroupHelper.getId(data))
            arg_1 = order.getArg(1)
            value = player.getBindedCardVal(arg_1)
            if value is not None:
                arg_2 = order.getArg(2)
                arg_2 = int(arg_2) if arg_2 != None else 2
                rc_list = (random.randint(1, 100) for _ in range(arg_2))
                rc = min(rc_list)
                if rc <= value:
                    msg = I18n.format("rb_meki_seikou")
                else:
                    msg = I18n.format("rb_meki_shippai")
            else:
                return
            msg = I18n.format("rb_kantei") % (
                GroupHelper.getName(data), arg_1, rc, value) + msg
            self.server.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "惩罚骰子", "rp", "rp [ARR](number)", "对属性进行惩罚骰检定，可设定投骰子次数取最大值，默认骰两次。")
    def rollPunish(self, data: dict, order: Order):
        if order.checkOrder("rp"):
            player = Player(GroupHelper.getId(data))
            arg_1 = order.getArg(1)
            value = player.getBindedCardVal(arg_1)
            if value is not None:
                arg_2 = order.getArg(2)
                arg_2 = int(arg_2) if arg_2 != None else 2
                rc_list = (random.randint(1, 100) for _ in range(arg_2))
                rc = max(rc_list)
                if rc >= value:
                    msg = I18n.format("rp_meki_shippai")
                else:
                    msg = I18n.format("rp_meki_seikou")
            else:
                return
            msg = I18n.format("rp_kantei") % (
                GroupHelper.getName(data), arg_1, rc, value) + msg
            self.server.sendGroup(self.group_id, msg)
