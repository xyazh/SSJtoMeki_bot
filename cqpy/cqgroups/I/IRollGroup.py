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
    def safeRoll(s: BaseGroup, fuc: Callable, arg: str) -> int | float | complex | None:
        r = None
        try:
            r = fuc(arg)
        except ZeroDivisionError:
            s.s.sendGroup(s.group_id, I18n.format("safeRoll_1"))
        except OverflowError:
            s.s.sendGroup(s.group_id, I18n.format("safeRoll_2"))
        except BaseException:
            s.s.sendGroup(s.group_id, I18n.format("safeRoll_3"))
        return r

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "创建角色", "new_card", "new_card [name]", "创建一张新卡")
    def nc(self, data: dict, order: Order):
        if order.checkOrder("new_card"):
            arg = order.getArg(1)
            if not arg:
                arg = "空白卡"
            if len(arg) > 30:
                self.s.sendGroup(self.group_id, "名字太长了，%s记不住的"%(BaseGroup.BOT_NAME_SELF))
                return
            qq_id = GroupHelper.getId(data)
            player = Player(qq_id)
            player.creatCard(arg, {})
            self.s.sendGroup(self.group_id, "是叫%s吧，%s知道了"%(arg, BaseGroup.BOT_NAME_SELF))

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "绑定角色", "bind_card", "bind_card [name]", "绑定角色卡")
    def bindCard(self, data: dict, order: Order):
        if order.checkOrder("bind_card"):
            arg = order.getArg(1)
            if not arg:
                arg = "空白卡"
            qq_id = GroupHelper.getId(data)
            player = Player(qq_id)
            if player.bindCard(arg):
                self.s.sendGroup(self.group_id, "%s已绑定" % arg)
            else:
                self.s.sendGroup(self.group_id, "我找找，我找找...咦？怎么没有")

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
            self.s.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "删除角色", "del_card", "del_card [name]", "删除角色卡，如果删除的角色卡正被绑定则会绑定空白卡")
    def delCard(self, data: dict, order: Order):
        if order.checkOrder("del_card"):
            arg = order.getArg(1)
            msg = "好像没有这张卡呢"
            if arg == "空白卡":
                msg = "空白卡无法被删除"
            elif arg:
                qq_id = GroupHelper.getId(data)
                player = Player(qq_id)
                if player.delCard(arg):
                    msg = "已删除%s" % arg
            self.s.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "角色管理", "pc", "pc (new|tag|bind|list|del|rm)", "pc指令用于管理角色卡\r\n没有参数时输出当前角色卡,各项参数说明：\r\n创建角色：new [name]\r\n绑定角色：bind|tag [name]\r\n角色列表：list\r\n删除角色：del|rm [name]\r\n")
    def pc(self, data: dict, order: Order):
        if order.checkOrder("pc"):
            arg1 = order.getArg(1)
            arg2 = order.getArg(2)
            arg2 = arg2 if arg2 else ""
            if arg1 == None:
                qq_id = GroupHelper.getId(data)
                player = Player(qq_id)
                binded_chara = player.getBindedCardName()
                self.s.sendGroup(self.group_id, "当前绑定的角色卡是%s" % binded_chara)
            elif arg1 == "new":
                order2 = GroupHelper.getOrderFromStr(
                    BaseGroup.ORDER_SPLIT_LIST[0] + "new_card %s" % (arg2))
                self.nc(data, order2)
            elif arg1 in ("tag", "bind"):
                order2 = GroupHelper.getOrderFromStr(
                    BaseGroup.ORDER_SPLIT_LIST[0] + "bind_card %s" % (arg2))
                self.bindCard(data, order2)
            elif arg1 == "list":
                order2 = GroupHelper.getOrderFromStr(
                    BaseGroup.ORDER_SPLIT_LIST[0] + "list_card")
                self.cardList(data, order2)
            elif arg1 in ("del", "rm"):
                order2 = GroupHelper.getOrderFromStr(
                    BaseGroup.ORDER_SPLIT_LIST[0] + "del_card %s" % (arg2))
                self.delCard(data, order2)
            else:
                pass

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "设置属性", "st", "st [ARRnumber...] (target)", "st指令用于设置计算角色属性，支持算数运算")
    def st(self, data: dict, order: Order):
        if order.checkOrder("st"):
            arg = order.getArg(1)
            if not arg:
                self.s.sendGroup(self.group_id, I18n.format("has_help"))
                return
            qq_id = GroupHelper.getId(data)
            msg = GroupHelper.getMsg(data)
            cq_codes = CQCodeHelper.creatCQCodeFromMsg(msg)
            at_ids = set()
            for i in cq_codes:
                if i.t == "at":
                    at_ids.add(i.data["qq"])
            at_ids = list(at_ids)
            if len(at_ids) > 0:
                qq_id = at_ids[0]
            player = Player(qq_id)
            if RollHelper.findsStr(arg, ["+", "-", "*", "/", "%", "^", "(", ")","|"]):
                card = player.getBindedCardNotNone()
                key = ""
                for i in card:
                    if arg.startswith(i):
                        key = i
                if key == "":
                    self.s.sendGroup(self.group_id, I18n.format("has_help"))
                    return
                for i in card:
                    arg = arg.replace(i, str(card[i]))
                flag = ""
                for i in arg:
                    if not i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "%", "^", "d", "D", "(", ")", ".", "i", "j", "|"]:
                        flag += i
                if flag != "":
                    self.s.sendGroup(self.group_id, "没有找到属性:%s" % flag)
                    return
                n = IRollGroup.safeRoll(
                    self, RollHelper.evaluateExpressionToFloat, arg)
                if n == None:
                    return
                n = int(n)
                player.setBindedCardArr({key: n})
                self.s.sendGroup(self.group_id, "%s设置%s=%s=%d" %(GroupHelper.getName(data), key, arg, n))
            else:
                player.addBindedCardAsStr(arg)
                self.s.sendGroup(self.group_id, "%s记住了" %BaseGroup.BOT_NAME_SELF)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "属性检定", "ra", "ra [ARR]", "ra指令用于检定")
    def ra(self, data: dict, order: Order):
        if order.checkOrder("ra"):
            arg: str = order.getArg(1)
            if arg == None:
                self.s.sendGroup(self.group_id,I18n.format("has_help"))
                return v
            elif arg.isdigit():
                k = ""
                v = int(arg)
            elif RollHelper.reFind(r"(\D+\d+)", arg):
                k = ""
                v = ""
                for i in arg:
                    if i.isdigit():
                        v += i
                        continue
                    k += i
                v = int(v)
            else:
                k = arg
                qq_id = GroupHelper.getId(data)
                player = Player(qq_id)
                v = player.getBindedCardVal(k)
                if v == None:
                    self.s.sendGroup(self.group_id, "好像没有%s这个属性" % k)
                    return
            r = random.randint(1, 100)
            msg = I18n.format("ra_meki_kantei") % (GroupHelper.getName(data), k, r, v)
            if self.vanilla_ra_rule:
                if r == 1:
                    msg += I18n.format("ra_meki_daiseiko")
                elif r <= v/5:
                    msg += I18n.format("ra_meki_kyokunan")
                elif r <= v/2:
                    msg += I18n.format("ra_meki_konnan")
                elif r <= v:
                    msg += I18n.format("ra_meki_huutsuu")
                elif r <= 95:
                    msg += I18n.format("ra_meki_shippai")
                elif r <= 99:
                    if v >= 50:
                        msg += I18n.format("ra_meki_shippai")
                    else:
                        msg += I18n.format("ra_meki_daishippai")
                else:
                    msg += I18n.format("ra_meki_daishippai")
            else:
                if r <= v:
                    if r <= self.daiseikou:
                        msg += I18n.format("ra_meki_daiseiko")
                    elif r <= v/5:
                        msg += I18n.format("ra_meki_kyokunan")
                    elif r <= v/2:
                        msg += I18n.format("ra_meki_konnan")
                    else:
                        msg += I18n.format("ra_meki_huutsuu")
                else:
                    if r >= self.daishippai:
                        msg += I18n.format("ra_meki_daishippai")
                    else:
                        msg += I18n.format("ra_meki_shippai")
            self.s.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "检定规则", "ra_rule", "ra_rule [vanilla|true|custom|false|daiseikou|daishippai|dsk|dsp] (number)", "ra_rule指令用于检定")
    def raRule(self, data: dict, order: Order):
        if order.checkOrder("ra_rule"):
            arg = order.getArg(1)
            if arg in ("vanilla", "true"):
                self.vanilla_ra_rule = True
                self.s.sendGroup(self.group_id, "ra将使用原版规则")
            elif arg in ("custom", "false"):
                self.vanilla_ra_rule = False
                self.s.sendGroup(self.group_id, "ra将使用自定义规则")
            elif arg in ("daiseikou", "dsk"):
                arg2 = order.getArg(2)
                if not arg2.isdigit():
                    self.s.sendGroup(self.group_id, I18n.format("has_help"))
                    return
                arg2 = int(arg2)
                if arg2 > 50 or arg2 < 1:
                    self.s.sendGroup(self.group_id, "大成功值应该在0以上50及以下")
                    return
                self.daiseikou = arg2
                self.s.sendGroup(self.group_id, "ra结果%d以下将为大成功" % arg2)
            elif arg in ("daishippai", "dsp"):
                arg2 = order.getArg(2)
                if not arg2.isdigit():
                    self.s.sendGroup(self.group_id, I18n.format("has_help"))
                    return
                arg2 = int(arg2)
                if arg2 > 100 or arg2 < 51:
                    self.s.sendGroup(self.group_id, "大失败值应该在50以上100及以下")
                    return
                self.daishippai = arg2
                self.s.sendGroup(self.group_id, "ra结果%d以上将为大失败" % arg2)
            else:
                self.s.sendGroup(self.group_id, I18n.format("has_help"))

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "骰个骰子", "r", "r [xdy*...]", "r指令用于roll点，支持复数域的算数运算 ，默认1d100")
    def r(self, data: dict, order: Order):
        if order.checkOrder("r"):
            arg = order.getArg(1)
            if not arg:
                arg = "1d100"
            r = IRollGroup.safeRoll(
                self, RollHelper.evaluateExpression, arg)
            if r == None:
                return
            self.s.sendGroup(self.group_id, "%s投了骰子：\r\n%s=%s" %
                             (GroupHelper.getName(data), arg, r))

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "coc7作成", "coc", "coc (number) (point)", "coc指令用于自动角色卡作成，number代表需要作成多少张卡（默认1张，最多5张），point表示设置的最大点数（默认随机400-500高斯分布）")
    def coc(self, data: dict, order: Order):
        if not order.checkOrder("coc"):
            return
        arg1, arg2 = order.getArgs(1, 2)
        number = 1
        if isinstance(arg1, str) and arg1.isdigit():
            number = min(int(arg1), 5)
        card_list = []
        for i in range(number):
            min_point = 8 * 20
            point = 0
            if isinstance(arg2, str) and arg2.isdigit():
                point = int(arg2)
            else:
                r = int(RollHelper.bestRandomGuass(450, 25, 2))
                r -= int(r % 5)
                point = r
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
        for i in card_list:
            y = int(RollHelper.bestRandomGuass(50, 25, 2))
            y -= int(y % 5)
            si = sum(i)
            msg += " \r\n\r\n力量%s体质%s体型%s敏捷%s外貌%s智力%s意志%s教育%s" % i + \
                "幸运%s 共计[%s/%s]" % (y, si, si + y)
        self.s.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "主持管理", "kp", "kp [set|ban] (target)", "设置kp")
    def setKp(self, data: dict, order: Order):
        if not order.checkOrder("kp"):
            return
        if not GroupHelper.checkOwnerOrAdmin(data):
            self.s.sendGroup(self.group_id, "只有群主或管理员可以指定kp")
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
                self.s.sendGroup(self.group_id, "成功指定kp")
        elif arg1 == "ban":
            for i in at_ids:
                player = Player(i)
                player.setKp(False)
                self.s.sendGroup(self.group_id, "成功取消kp")
        else:
            self.s.sendGroup(self.group_id, I18n.format("has_help"))

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "玩家管理", "pl", "pl [join|leave|clear] [targets]...", "设置pl")
    def kpSetPl(self, data: dict, order: Order):
        if not order.checkOrder("pl"):
            return
        qq_id = GroupHelper.getId(data)
        kp_player = Player(qq_id)
        if not kp_player.isKp():
            self.s.sendGroup(self.group_id, "只有kp可以用此命令")
            return
        arg = order.getArg(1)
        if not arg in ("join","leave","clear"):
            self.s.sendGroup(self.group_id, I18n.format("has_help"))
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
        pls:dict = kp_player.writeGet("pls",{})
        if arg == "join":
            for i in at_ids:
                pls[i] = 1
            self.s.sendGroup(self.group_id, "已添加玩家")
        elif arg == "leave":
            for i in at_ids:
                if i in pls:
                    pls.pop(i)
            self.s.sendGroup(self.group_id, "已退出玩家")
        elif arg == "clear":
            pls.clear()
            self.s.sendGroup(self.group_id, "已清空玩家")

    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "设置物品", "set_item", "set_item [ItemNumber...] (targets)...", "kp设置物品")
    def kpSetItem(self, data: dict, order: Order):
        if not order.checkOrder("set_item"):
            return
        qq_id = GroupHelper.getId(data)
        kp_player = Player(qq_id)
        if not kp_player.isKp():
            self.s.sendGroup(self.group_id, "只有kp可以用此命令")
            return
        arg = order.getArg(1)
        if not arg:
            self.s.sendGroup(self.group_id, I18n.format("has_help"))
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
        self.s.sendGroup(self.group_id, "物品设置完毕")

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
        if len(xdys)==1:
            xdys = ["1",xdys[0]]
        elif len(xdys)<2:
            self.s.sendGroup(self.group_id,I18n.format("has_help"))
            return
        val = card[order_str]
        rc = random.randint(1, 100)
        msg = I18n.format("ra_meki_kantei") % (GroupHelper.getName(data), order_str, rc, val)
        if rc<=val:
            r = IRollGroup.safeRoll(
                self, RollHelper.evaluateExpression, xdys[0])
            if r == None:
                return
            r = int(r)
            msg += I18n.format("ra_meki_huutsuu")
            msg += "\r\n你的%s变更为%s"%(order_str,"+%s"%r if r>=0 else "%s"%r)
            player.setBindedCardArr({order_str:val+r})
        else:
            r = IRollGroup.safeRoll(
                self, RollHelper.evaluateExpression, xdys[1])
            if r == None:
                return
            r = int(r)
            msg += I18n.format("ra_meki_shippai")
            msg += "\r\n你的%s变更为%s"%(order_str,"+%s"%r if r>=0 else "%s"%r)
            player.setBindedCardArr({order_str:val+r})
        self.s.sendGroup(self.group_id, msg)