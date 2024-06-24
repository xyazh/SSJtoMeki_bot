import inspect
import random
import time
import threading
import datetime
from ..CQCode import CQCodeHelper
from ..GameSystem.PlayerSystem.Player import Player
from ..Order import Order
from ..Cqserver import Cqserver
from ..DataManager import DataManager
from ..LoopEvent import LoopEvent
from ..GroupHelper import GroupHelper
from ..GroupHelper import ORDER_SPLIT_LIST
from ..GenVoice import GenVoice
from ..xyazhServer.BestXor import BestXor
from ..I18n.I18n import I18n
from .BaseGroup import BaseGroup
from .I.ISSJGroup import ISSJGroup
from .I.IRollGroup import IRollGroup
from .I.ITTKGroup import ITTKGroup
from .I.IItemGroup import IItemGroup

BOT_NAME_SELF = "三色堇"
BOT_NAME = "三色堇"


@GroupHelper.addActiveGroups(582897932, 558335813)
class YxBaseGroup(BaseGroup, IRollGroup, ISSJGroup, ITTKGroup, IItemGroup):
    BOT_NAME_SELF = BOT_NAME_SELF
    BOT_NAME = BOT_NAME

    @staticmethod
    def register(fuc):
        fuc.sign_reg = True
        return fuc

    @staticmethod
    def helpData(clazz: list[str], tx: str, ord: str, usg: str, datdetails: str):
        def r(fuc):
            fuc.help_data = [clazz, tx, ord, usg, datdetails]
            return fuc
        return r

    # 确认time_name今日有无使用，未使用返回True，否返回False；以及如果没有使用是否将本次确认保存为今日第一次使用
    def timeCheck(self, data, time_name: str, bool: bool = False):
        player = Player(GroupHelper.getId(data))
        last_time = player.findGet(time_name, 0)
        if (last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
            return False
        elif bool:
            player.set(time_name, time.time())
        return True

    # 更改属性数值，返回更改值
    def ARTChange(self, data, change__name: str, change_number: float):
        player = Player(GroupHelper.getId(data))
        n = player.findGet(change__name, 0)
        player.set(change__name, n + change_number)
        return change_number
########################################################################################################################
    # 指令帮助列表及其详情说明

    @register
    @helpData(["normal"], "获取帮助", "help", "help (name)|/page/", "help指令用于查看一般常用指令列表，可以添加一个参数作为需要查找的指令名字，来获取此指令的详细信息。")
    def help(self, data, order: Order):
        if order.checkOrder("help") or GroupHelper.getMsg(data) in ["帮助", "获取帮助"]:
            arg = order.getArg(1)
            if arg == None:
                msg = "#-----帮助列表-----#\r\n%s\r\n------------------" % (
                    (I18n.format("ord")))
                for i in BaseGroup.HELP_CLASS_DATA:
                    msg += "\r\n%s：/help %s" % (
                        BaseGroup.HELP_CLASS_DATA[i], i)
            elif arg in BaseGroup.HELP_CLASS_DATA:
                msg = "#-----%s-----#\r\n%s\r\n------------------" % (
                    BaseGroup.HELP_CLASS_DATA[arg], (I18n.format("ord")))
                for i in self.helps_class[arg]:
                    msg += "\r\n%s：/%s" % (i[0], i[1])
                msg += "\r\n------------------\r\ntip：可使用/help (指令名)查看指令详细说明。\r\n例：/help pack--->查看/pack指令详细说明。"
            elif arg in self.helps:
                tx, ord, usg, datdetails = tuple(self.helps[arg])
                msg = "#---『%s』---#\r\n用法：\r\n/%s" % (tx, (usg))
                msg += "\r\n------------------\r\n功能详解：%s" % datdetails
                msg += "\r\n------------------\r\n数据类型详解：\r\n(可选参数) ; [必须参数]\r\n/未完成参数/ ; *可选语法\r\n...可重复 ; |或"
            else:
                self.server.sendGroup(
                    self.group_id, (I18n.format("prob")) + "\r\n（找不到这样的指令）")
                return
            self.server.sendGroup(self.group_id, msg)

    # 手动让三色堇退群
    @register
    @helpData(["other"], "退出该群", "bye", "bye", "让三色堇退出该群。")
    def bye(self, data: dict, order: Order):
        if order.checkOrder("bye") or order.checkOrder("exit"):
            if GroupHelper.checkOwnerOrAdmin(data):
                self.server.setGroupLeave(self.group_id)

    # 测试机器人发送信息
    @register
    @helpData(["other"], "测试指令", "test", "test (msg)", "发送一句test或者指定的参数。")
    def test(self, data, order: Order):
        if order.checkOrder("test"):
            arg = order.getArg(1)
            if arg:
                self.server.sendGroup(self.group_id, arg)
            else:
                self.server.sendGroup(self.group_id, "test")

    # 输出机器人开发信息
    @register
    @helpData(["other"], "开发信息", "bot", "bot", "输出机器人信息。")
    def bot(self, data, order: Order):
        if order.checkOrder("bot"):
            self.server.sendGroup(
                self.group_id, "Multi functional dice rolling bot made with Python by Xyazh")

    @register
    @helpData(["other"], "网页绑定", "web_bind", "web_bind [uid]", "在网站上绑定qq用（跑团可能需要）")
    def webBindQQ(self, data: dict, order: Order):
        if not order.checkOrder("web_bind"):
            return
        uid = order.getArg(1)
        if uid == None:
            self.server.sendGroup(
                self.group_id, I18n.format("prob") + "（需要help吗）")
            return
        token = BestXor.bestEncryptXor(uid.encode(
            "utf8"), b"%d" % GroupHelper.getId(data))
        self.server.sendGroup(self.group_id, "你的token是：\r\n%s" % token)
########################################################################################################################
    # 获取功能列表

    @register
    @helpData(["normal"], "功能列表", "fun", "fun", "功能列表，面向给群友使用的功能。直接发送“功能”或指令的方式就可以使用。")
    def function(self, data, order: Order):
        if GroupHelper.getMsg(data) in ["功能", "功能列表"] or order.checkOrder("fun"):
            msg = "#-----功能列表-----#\r\n"
            msg += "获取帮助；每日签到\r\n✧未来视✧；✧未来启✧\r\n魔素具现；查看好感\r\n好感归零；随机涩图\r\n动画资讯；g a l资讯"
            msg += "\r\n------------------\r\n%s" % ((I18n.format("fun")))
            self.server.sendGroup(self.group_id, msg)

    # 获取发送者魔素点数
    @register
    @helpData(["normal"], "魔素具现", "point", "point", "查看自己当前魔素点数。")
    def point(self, data, order: Order):
        if order.checkOrder("point") or GroupHelper.getMsg(data) in ["魔素具现", "魔素"]:
            player = Player(GroupHelper.getId(data))
            pt = player.findGet("point")
            if pt == None:
                player.set("point", 1)
                self.server.sendGroup(self.group_id, I18n.format(
                    "pt_0") % GroupHelper.getName(data))
            elif pt > 0:
                if pt < 10:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "pt_1")) % (GroupHelper.getName(data), pt))
                elif pt < 20:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "pt_2")) % (GroupHelper.getName(data), pt))
                elif pt < 60:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "pt_3")) % (GroupHelper.getName(data), pt))
                elif pt < 240:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "pt_4")) % (GroupHelper.getName(data), pt))
                elif pt < 1200:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "pt_5")) % (GroupHelper.getName(data), pt))
                elif pt < 7200:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "pt_6")) % (GroupHelper.getName(data), pt))
                else:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "pt_7")) % (pt, GroupHelper.getName(data)))
            else:
                self.server.sendGroup(self.group_id, (I18n.format(
                    "pt_neg")) % (GroupHelper.getName(data), pt))

    # 获取三色堇对发送者好感度
    @register
    @helpData(["normal"], "查看好感", "emotion", "emotion", "查看自己当前好感点数。")
    def emotion(self, data, order: Order):
        if order.checkOrder("emotion") or GroupHelper.getMsg(data) in ["查看好感", "好感"]:
            player = Player(GroupHelper.getId(data))
            e = player.get("emotion")
            if e == None:
                player.set("emotion", 1)
                self.server.sendGroup(self.group_id, I18n.format(
                    "e_0") % GroupHelper.getName(data))
            elif e > 0:
                if e < 150:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "e_1")) % (GroupHelper.getName(data), e))
                elif e < 300:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "e_2")) % (GroupHelper.getName(data), e))
                elif e < 600:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "e_3")) % (GroupHelper.getName(data), e))
                elif e < 1200:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "e_4")) % (GroupHelper.getName(data), e))
                elif e < 2400:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        "e_5")) % (GroupHelper.getName(data), e))
                else:
                    self.server.sendGroup(self.group_id, (I18n.format(
                        random.choice["e_6", "e_5"])) % (GroupHelper.getName(data), e))
            else:
                self.server.sendGroup(self.group_id, (I18n.format(
                    "e_neg")) % (GroupHelper.getName(data), e))

    # 向三色堇道歉
    @register
    @helpData(["normal"], "好感归零", "sorry", "sorry", "向三色堇道歉以让你为负数的可怜好感度归0。（所以说你干了什么要用这个指令？）")
    def sorry(self, data, order: Order):
        if order.checkOrder("sorry") or GroupHelper.getMsg(data) in ["好感归零", "道歉"]:
            player = Player(GroupHelper.getId(data))
            e = player.get("emotion")
            if e == None:
                self.server.sendGroup(self.group_id, I18n.format("e_rst_0"))
            elif e < 0:
                player.set("emotion", 1)
                self.server.sendGroup(self.group_id, I18n.format(
                    "e_rst_1") % (GroupHelper.getName(data)))
            else:
                self.server.sendGroup(self.group_id, I18n.format(
                    "e_rst_ng") % (GroupHelper.getName(data), e))

    # 获取签到者签到天数，并加魔素与好感
    @register
    @helpData(["normal"], "每日签到", "sign", "sign", "签到，签到计数所有群通用。直接发送签到或指令的方式就可以使用。")
    def sign(self, data, order: Order):
        if GroupHelper.getMsg(data) in ["每日签到", "签到"] or order.checkOrder("sign"):
            player = Player(GroupHelper.getId(data))
            last_time = player.findGet("last_time")
            if last_time == None:
                player.set("last_time", time.time())
                player.set("day", 1)
                pt = player.findGet("point", 0)
                player.set("point", pt + 1)
                self.server.sendGroup(self.group_id, I18n.format(
                    "sign_0") % (GroupHelper.getName(data)))
                return
            if (last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
                self.server.sendGroup(self.group_id, I18n.format("sign_ng") % (
                    GroupHelper.getName(data), time.time()-last_time))
            else:
                day = player.findGet("day", 0)
                e = player.findGet("emotion", 0)
                pt = player.findGet("point", 0)
                day += 1
                add_e = random.randint(
                    1, int(day//40) + 1) if int(day//40) < 10 else random.randint(10, 20)
                add_pt = random.randint(int(day//4), day//2)
                player.set("last_time", time.time())
                player.set("day", day)
                player.set("emotion", e + add_e)
                player.set("point", pt + add_pt)
                self.server.sendGroup(self.group_id, I18n.format("sign_1") % (
                    GroupHelper.getName(data), day, add_pt, add_e))

    # 获取发送者占卜命运结果
    @register
    @helpData(["normal"], "✧未来视✧", "fate", "fate", "吾が名はパンジー↑！随一の魔法使いにして身に魔神✦↑『デイアブロス』↑✦を封印されし、根源の力を↑引き継げり、そしていつか魔法の真理に辿り着きも↓の↑！\r\n")
    def meiunn(self, data, order: Order):
        if GroupHelper.getMsg(data) in ["占卜", "未来视", "✧未来视✧"] or order.checkOrder("fate"):
            player = Player(GroupHelper.getId(data))
            pt = player.findGet("point")

            def change_point(min, max):
                if (fate_last_time + 8 * 3600) // (24 * 3600) != (time.time() + 8 * 3600) // (24 * 3600):
                    change_pt = random.randint(min, max)
                    player.set("point", pt + change_pt)
                    player.set("fate_change_pt", change_pt)
                else:
                    change_pt = player.get("fate_change_pt")
                return change_pt
            msg = "请“%s”阁下，先去查看一下自己的『魔素』吧。" % GroupHelper.getName(data)
            if pt is not None:
                fate_last_time = player.findGet("fate_last_time", 0)
                add_msg = "\r\n(获得魔素【+%g✧】)\r\n------------------\r\n"
                sub_msg = "\r\n(丢失魔素【%g✧】)\r\n------------------\r\n"
                end_msg = ""
                fate = int(random.randint(0, 99))
                flag = True
                if fate_last_time and self.unnsei_once_a_day:
                    if (fate_last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
                        end_msg = "\r\n------------------\r\n“%s”阁下，那、那个…… 【%.2f】秒前已经占卜了的说……不满意的话要三色堇使用『✧未来启✧』吗？……" % (
                            GroupHelper.getName(data), time.time() - fate_last_time)
                        _fate = player.findGet("fate", 0)
                        if type(_fate) == int:
                            fate = _fate
                            flag = False
                if flag:
                    player.set("fate_last_time", time.time())
                    player.set("fate", fate)
                if fate < 1:
                    r_msg = "✧『⛧崩れし大地、破裂し蒼穹⛧』✧" + \
                        sub_msg % change_point(-100, -50)
                    r_msg += (I18n.format("fate_1")) + end_msg
                elif fate < 3:
                    r_msg = "✧『⛧破滅世界の結末⛧』✧" + sub_msg % change_point(-50, -40)
                    r_msg += (I18n.format("fate_2")) + end_msg
                elif fate < 6:
                    r_msg = "✧『⛧終焉の大厄災⛧』✧" + sub_msg % change_point(-40, -30)
                    r_msg += (I18n.format("fate_3")) + end_msg
                elif fate < 10:
                    r_msg = "✧『冥界不祥の角笛』✧" + sub_msg % change_point(-25, -20)
                    r_msg += (I18n.format("fate_4")) + end_msg
                elif fate < 15:
                    r_msg = "✧『呪いの指輪』✧" + sub_msg % change_point(-20, -15)
                    r_msg += (I18n.format("fate_5")) + end_msg
                elif fate < 21:
                    r_msg = "✧『深淵の凝視』✧" + sub_msg % change_point(-15, -10)
                    r_msg += (I18n.format("fate_6")) + end_msg
                elif fate < 28:
                    r_msg = "『悪魔の囁き』" + sub_msg % change_point(-10, -5)
                    r_msg += (I18n.format("fate_7")) + end_msg
                elif fate < 36:
                    r_msg = "『鬼の悪戯』" + sub_msg % change_point(-5, -1)
                    r_msg += (I18n.format("fate_8")) + end_msg
                elif fate < 45:
                    r_msg = "『尻尾切』\r\n------------------\r\n"
                    r_msg += (I18n.format("fate_9")) + end_msg
                elif fate < 55:
                    r_msg = "『無変の平日』\r\n------------------\r\n"  # 中间值
                    r_msg += (I18n.format("fate_10")) + end_msg
                elif fate < 64:
                    r_msg = "『些か運』\r\n------------------\r\n"
                    r_msg += (I18n.format("fate_11")) + end_msg
                elif fate < 72:
                    r_msg = "『聖域の水』" + add_msg % change_point(5, 10)
                    r_msg += (I18n.format("fate_12")) + end_msg
                elif fate < 79:
                    r_msg = "『御守の光』" + add_msg % change_point(10, 15)
                    r_msg += (I18n.format("fate_13")) + end_msg
                elif fate < 85:
                    r_msg = "✧『天使の歌声』✧" + add_msg % change_point(15, 20)
                    r_msg += (I18n.format("fate_14")) + end_msg
                elif fate < 90:
                    r_msg = "✧『精霊の恵み』✧" + add_msg % change_point(20, 25)
                    r_msg += (I18n.format("fate_15")) + end_msg
                elif fate < 94:
                    r_msg = "✧『世界祝福の加護』✧" + add_msg % change_point(25, 30)
                    r_msg += (I18n.format("fate_16")) + end_msg
                elif fate < 97:
                    r_msg = "✧『✦神々守の強運✦』✧" + add_msg % change_point(40, 60)
                    r_msg += (I18n.format("fate_17")) + end_msg
                elif fate < 99:
                    r_msg = "✧『✦素晴世界の初風✦』✧" + add_msg % change_point(60, 80)
                    r_msg += (I18n.format("fate_18")) + end_msg
                else:
                    r_msg = "✧『✦咲き誇る花、舞い踊る瓣✦』✧" + \
                        add_msg % change_point(80, 150)
                    r_msg += (I18n.format("fate_19")) + end_msg
                msg = "%s\r\n“%s”的预言之语是……\r\n------------------\r\n%s" % (
                    (I18n.format("mgc_fate")), GroupHelper.getName(data), r_msg)
            self.server.sendGroup(self.group_id, msg)

    # 媒介转运
    @register
    @helpData(["normal"], "✧未来启✧", "fate_change", "fate_change", "吾が名はパンジー↑！随一の魔法使いにして身に魔神✦↑『デイアブロス』↑✦を封印されし、根源の力を↑引き継げり、そしていつか魔法の真理に辿り着きも↓の↑！\r\n")
    def fateChange(self, data, order: Order):
        if GroupHelper.getMsg(data) in ["运转", "未来启", "✧未来启✧"] or order.checkOrder("fate_change"):
            player = Player(GroupHelper.getId(data))
            change_pt = player.findGet("fate_change_pt", 0)
            add_msg = "\r\n(获得魔素【+%g✧】)\r\n------------------\r\n"
            sub_msg = "\r\n(丢失魔素【%g✧】)\r\n------------------\r\n"
            end_msg = "\r\n------------------\r\n『✧未来启✧』每日只作用一次的说……"
            if self.timeCheck(data, "fate_last_time"):
                msg = "阁下今天还没有让我使用过『✧未来视✧』呢……"
            else:
                msg = I18n.format("pass_text")
            self.server.sendGroup(self.group_id, msg)

# #test
#     @register
#     @helpData(["normal"],"✧未来启✧","fate_change","fate_change","")
#     def ccoTest(self,data,order:Order):
#          if GroupHelper.getMsg(data) in ["ccoTest"] or order.checkOrder("ccoTest"):
#             cqcodes = CQCodeHelper.creatCQCodeFromMsg(GroupHelper.getMsg(data))
#             at_ids = []
#             for i in cqcodes:
#                 if i.t == "at":
#                     at_ids.append(i.data["qq"])
#             if len(at_ids) != 2:
#                 return
#             else:
#                 return at_ids
#             qqid = at_ids[0] #qqid1
#             qqid = at_ids[1] #qqid2
#             sec = 300 #禁言
#             sec = 0 #解禁
#             while True:
#                 self.server.groupBan(self.group_id,qqid,sec)

    # 获取当日动漫资讯
    @register
    @helpData(["normal"], "动画资讯", "anime_news", "anime_news", "获取当日动漫新闻。资讯来源于网络，每小时会尝试更新，直接发送动漫新闻、动画新闻、二次元新闻、anime新闻、动漫资讯、动画资讯、二次元资讯、anime资讯有同样效果。")
    def getAnimeNews(self, data, order: Order):
        if GroupHelper.getMsg(data) in ["动漫新闻", "动画新闻", "二次元新闻", "anime新闻", "动漫资讯", "动画资讯", "二次元资讯", "anime资讯"]:
            order = GroupHelper.getOrderFromStr(
                ORDER_SPLIT_LIST[0] + "anime_news")
        if order.checkOrder("anime_news"):
            li = LoopEvent.today_anime_news
            if len(li) > 0:
                self.server.sendGroup(
                    self.group_id, li[random.randint(0, len(li)-1)])
                return
            self.server.sendGroup(self.group_id, "三色堇没有更多的信息了……不要再找三色堇了……")

    # 获取当日gal新闻
    @register
    @helpData(["normal"], "g a l资讯", "gal_news", "gal_news (0-9*|all)", "获取当日gal新闻。资讯来源于网络，每小时会尝试更新。参数为空随机，为all输出全部，数字输出当前条数，发送gal新闻、galgame新闻、gal资讯、galgame资讯也可随机获取一条。")
    def getGalNews(self, data, order: Order):
        if GroupHelper.getMsg(data) in ["gal新闻", "galgame新闻", "gal资讯", "galgame资讯", "g a l资讯"]:
            order = GroupHelper.getOrderFromStr(
                ORDER_SPLIT_LIST[0] + "gal_news")
        if order.checkOrder("gal_news"):
            li = LoopEvent.today_galgame_news
            arg = order.getArg(1)
            if len(li) <= 0:
                self.server.sendGroup(self.group_id, "噶呜……三色堇知道的信息都已经说完了……")
                return
            if arg == None:
                self.server.sendGroup(
                    self.group_id, li[random.randint(0, len(li)-1)])
                return
            if arg == "all":
                if len(li) > 0:
                    msg = "今日gal:"
                    n = 0
                    for i in li:
                        n += 1
                        msg += "\r\n\r\n%d.%s" % (n, i)
                    self.server.sendGroup(self.group_id, msg)
                    return
            if arg.isdigit():
                i = int(arg)
                if i > 0 and i < len(li):
                    msg = "%d.%s" % (i, li[i-1])
                    self.server.sendGroup(self.group_id, msg)
                    return
                self.server.sendGroup(self.group_id, "那个……三色堇也找不到相关的信息的说……")
                return
            self.server.sendGroup(
                self.group_id, (I18n.format("prob")) + "\r\n（需要help吗）")

    # 获取随机涩图
    @register
    @helpData(["normal"], "随机涩图", "roll_img", "roll_img", "随机获取涩图。")
    def rollImg(self, data: dict, order: Order):
        if order.checkOrder("roll_img") or GroupHelper.getMsg(data) in ["涩图","色图","随机涩图"]:
            # self.s.sendImgToGroupFromUrl(self.group_id,"https://iw233.cn/api.php?sort=iw233")
            self.server.sendImgToGroupFromUrl(
                self.group_id, "https://www.dmoe.cc/random.php")

    @register
    @helpData(["normal"], "生成语音", "vits", "vits [text] (language)", "发出真奈美的声音，可以自动识别语言和也可以指定语言，支持日本語、简体中文、English。")
    def vits(self, data: dict, order: Order):
        if not order.checkOrder("vits"):
            return

        def t(self: YxBaseGroup, data: dict, order: Order):
            text = order.getArg(1)
            l = order.getArg(2)
            if not text:
                self.server.sendGroup(
                    self.group_id, (I18n.format("prob")) + "\r\n（未输入文字）")
                return
            if l in ("日本語", "简体中文", "English"):
                r = GenVoice.gen(text, l)
            else:
                r = GenVoice.genVioce(text)
            if not r:
                self.server.sendGroup(
                    self.group_id, (I18n.format("prob") + "\r\n（语音生成失败）"))
                return
            r = r.replace("C:\\", "C:\\\\")
            self.server.sendGroup(
                self.group_id, "[CQ:record,file=file:///%s]" % r)
        th = threading.Thread(target=t, args=(self, data, order))
        th.start()

    # 对于【当前时间】的回复
    @register
    def nowTime(self, data):
        get_msg = GroupHelper.getMsg(data)
        if get_msg in ("当前时间", "时间"):
            now_time = datetime.datetime.now()
            # 平常
            a = "现在是？……【%Y-%m-%d，%H:%M:%S】的说……嗯……应该没搞错吧……"
            b = "【%Y-%m-%d，%H:%M:%S】的说……自己也可以看为什么要来问像我这样的人呢……"
            c = "【%Y-%m-%d，%H:%M:%S】……希望不会发生什么不好的事就好了……"
            d = "【%Y-%m-%d，%H:%M:%S】了呢，感觉好闲呢……吖呜（打哈欠），都不知道该干什么了……(￣▽￣)"
            e = "【%Y-%m-%d，%H:%M:%S】的说，这个时间段大家在做什么呢？Ciallo～(∠·ω< )⌒☆"
            # 凌晨 00.00-05.00
            f = "啊~~~哈~~~呜~~~【%Y-%m-%d，%H:%M:%S】，都这么晚了……大家都不睡觉嘛……(´·ω·`)？"
            g = "【%Y-%m-%d，%H:%M:%S】，嗷~~~好困的说……嗯嗯呃呃……"
            h = "喵呜~~~【%Y-%m-%d，%H:%M:%S】，该睡觉了的说……"
            # 早晨 05.00-08.00
            i = "【%Y-%m-%d，%H:%M:%S】？好困啊……起床……不要……"
            j = "(＠￣￢￣＠)zzZ，现在是……【%Y-%m-%d，%H:%M:%S】的说……呼呼……哈……zzZ"
            k = "嗯呃……额……啊嗯……吃……真的吃不下了……嘿嘿……（【%Y-%m-%d，%H:%M:%S】）"
            i1 = "【%Y-%m-%d，%H:%M:%S】？怎么回事……啊呜……不要起床……不要……"
            # 上午 08.00-11.00
            l = "太阳……好烦……（把头埋进被子）嗯呃……（【%Y-%m-%d，%H:%M:%S】)"
            m = "【%Y-%m-%d，%H:%M:%S】？还有点困呢，再睡一觉的说……(～￣▽￣)～"
            n = "呼……哈……嗯嗯~？【%Y-%m-%d，%H:%M:%S】？等……等等再起床啦……"
            # 中午 11.00-13.00
            o = "【%Y-%m-%d，%H:%M:%S】，果然还是起来早点吃早饭比较好麻……",
            p = "早上果然就应该一股脑地睡过去的说！啊，不是……我的意思是……都【%Y-%m-%d，%H:%M:%S】了呢，大家一定要养成早睡早起的好习惯，嗯……"
            q = "糟！？都【%Y-%m-%d，%H:%M:%S】这个时间段了，再不去吃饭就要被骂了的说……(っ°Д°;)っ"
            o1 = "（啪哒）啊呜……（从床上滚到地板）磕到脚趾母了，脚好痛的说……（看向时钟）原来已经%Y-%m-%d，%H:%M:%S了吗……脚还是好痛的说……啊呜……"
            # 下午 13.00-16.00
            r = "【%Y-%m-%d，%H:%M:%S】……我能做些什么呢……果然什么都做不好的样子呢……"
            s = "下午【%Y-%m-%d，%H:%M:%S】的说……还要多久这一天才能过去呢？"
            t = "加把劲……哦……呃嗯……果然还是提不起劲的说，好想睡觉……（【%Y-%m-%d，%H:%M:%S】）"
            # 傍晚 16.00-19.00
            u = "【%Y-%m-%d，%H:%M:%S】……特地来问我……我也不会有什么特别的想法的说……"
            v = "今天有没有夕阳呢？现在是(*°▽°*)【%Y-%m-%d，%H:%M:%S】的说"
            w = "晚饭的香味？……肚子有点饿了的说……（【%Y-%m-%d，%H:%M:%S】）"
            # 晚上 19.00-00.00
            x = "都到【%Y-%m-%d，%H:%M:%S】了，不会还有什么没有做完的事情吧……"
            y = "【%Y-%m-%d，%H:%M:%S】的说，有点晚了呢……不知道今天夜晚的星星有多少颗呢？"
            z = "【%Y-%m-%d，%H:%M:%S】，已经到这个时间了，总感觉晚上好兴奋呢*★,°*:.☆\(￣▽￣)/$:*.°★*"
            msg_dict = {  # 基于总目录的文本根据时间以此分类回复
            "lingchen":random.choice([f, g, h,i1]),
            "zaochen":random.choice([i, j, k]),
            "shangwu":random.choice([l, m, n]),
            "zhongwu":random.choice([o, p, q, a, b, c, d, e, o1]),
            "xiawu":random.choice([r, s, t, a, b, c, d, e]),
            "bangwan":random.choice([u, v, w, a, b, c, d, e]),
            "wanshang":random.choice([x, y, z, a, b, c, d, e])
            }
            now_hour = int(now_time.strftime("%H"))
            match {0:0,1:0,2:0,3:0,4:0,
                   5:1,6:1,7:1,
                   8:2,9:2,10:2,
                   11:3,12:3,
                   13:4,14:4,15:4,
                   16:5,17:5,18:5,
                   19:6,20:6,21:6,22:6,23:6
                   }[now_hour]:
                case 0:
                    send_msg = "lincheng"
                case 1:
                    send_msg = "zaochen"
                case 2:
                    send_msg = "shangwu"
                case 3:
                    send_msg = "zhongwu"
                case 4:
                    send_msg = "xiawu"
                case 5:
                    send_msg = "bangwan"
                case 6:
                    send_msg = "wanshang"
            self.server.sendGroup(self.group_id, now_time.strftime(msg_dict[send_msg]))

    # 三色堇的各种回复
    @register
    def strSSJ(self, data):
        get_msg = GroupHelper.getMsg(data)
        msg_list = None
        # 对于"三色堇抱抱"的回复
        if get_msg == "三色堇抱抱":
            player = Player(GroupHelper.getId(data))
            if self.timeCheck(data, "SSJBaobao_last_time"):
                n = 1
            else:
                n = player.findGet("SSJBaobao_n", 0)
                n += 1
            player.set("SSJBaobao_n", n)
            if n <= 5:
                msg_list = [
                    "阁下还真是爱撒娇呢，真是拿阁下没有办法呢，只……只限这一次的说哦。",
                    "睡在怀里的阁下真可爱呢，这件事可不要告诉大家哦。",
                    "怀里的阁下睡得真熟呢，就像小宝宝一样的说，今天一定是累坏了吧……",
                    "只要阁下不嫌弃三色堇的话……三色堇会静静安抚阁下的。",
                    "阁下一定累了吧，嘘~~~，没关系的哦，三色堇都知道的……",
                    "至少现在，请阁下放轻松……在我的膝上静静地休息吧……",
                    "没关系的，我不会像别人一样忘记阁下的，我会【永远】地记住阁下的……",
                    "阁下,我还在意着你的说，请不要这么难过……这样子…这样子三色堇也会伤心的……",
                    "都会没事的说，三色堇永远都会在这里等着阁下哦……"
                    "就让三色堇来施展一个消除伤心的魔法，把阁下的烦恼都放飞吧。"]
            elif n > 5:
                msg_list = ["今天的阁下…怎么这么爱撒娇呢……",
                            "阁下这是在是在戏弄三色堇吗…？",
                            "请阁下不要这样子捉弄三色堇的说……",
                            "阁下怎么这么爱撒娇……"]
        # 对于【三色堇|跳楼】的回复
        elif "三色堇" in get_msg and "跳楼" in get_msg:
            player = Player(GroupHelper.getId(data))
            e = player.getet("emotion")
            sub_e = random.randint(-5, 0)
            player.set("emotion", e + sub_e)
            msg_list = [
                "嗯……感觉不是什么有意思的话题呢……（好感下降【%g◈】）" % sub_e,
                "那个……三色堇不是很想听这些的说……（好感下降【%g◈】）" % sub_e,
                "可以不要这样子嘛……突然感觉好难受的说……（好感下降【-%g◈】）" % sub_e,
                "突然有点想吐了……（好感下降【%g◈】）" % sub_e,
                "……嗯额……（好感下降【%g◈】）" % sub_e,
                "#三色堇扭扭捏捏的，看起来好像不太舒服。（好感下降【%g◈】）" % sub_e,
                "脚好痛……像被子弹打中了一样……为什么会痛的说……（好感下降【%g◈】）" % sub_e,
                "好冷的说……是我衣服穿少了吗……（好感下降【%g◈】）" % sub_e,
                "啊……那个……不是……（好感下降【%g◈】）" % sub_e,
                "人死之后才能变得幸福吗…………。嘿哈……开玩笑的说……（好感下降【%g◈】）" % sub_e,
                "三色堇感觉身体不是很舒服的说……（好感下降【%g◈】）" % sub_e]
        # 对于【三色堇】的回复
        elif "三色堇" in get_msg:
            msg_list = [
                "嗯额……那个……\r\n找三色堇有什么事吗……",
                "嗯……额……要找三色堇吗？",
                "三色堇一直呆在这里的说……",
                "欸……在叫三色堇吗？",
                "Ciallo～(∠·ω< )⌒☆\r\n三色堇在这里。"]
        # 对于【灰茉莉】的回复
        elif "灰茉莉" in get_msg:
            msg_list = [
                "灰茉莉……那是谁？",
                "灰茉莉……我不认识的说……",
                "……",
                "欸？什么？",
                "",]  # 如果没有那样的幼年，或许一切都会不一样的吧……
        # elif "行" in get_msg or "彳亍" in get_msg or "可以" in get_msg:
        #     msg_list = [
        #         "还好啦……",
        #         "真的要这样子吗……",
        #         "这样子好吗……",
        #         "这样子可以吗？…",
        #         "……",
        #         "没有问题……"]
        # elif  "是不是" in get_msg:
        #     msg_list = [
        #     "三色堇觉得应该……是……",
        #     "三色堇觉得不应该……是……"]
        # elif ("三色堇" in get_msg and "是" in get_msg) or "三色堇是不是" in get_msg:
        #     msg_list = [
        #     "请不要评价三色堇……",
        #     "咦？",
        #     "额嗯？",
        #     "……"]
        if msg_list is not None:
            self.server.sendGroup(self.group_id, random.choice(msg_list))

    # 对于【三色堇】的肢体互动
    @register
    def SSJTouch(self, data):
        player = Player(GroupHelper.getId(data))
        e = player.findGet("emotion", 0)
        get_msg = GroupHelper.getMsg(data)
        msg, add_e_list = None, ""

        def msgChoice(low, mid, high):
            lim_e, add_lim_e, low_up_lim, mid_up_lim, add_e = 50, 50, 90, 99, 0
            if e <= 0:
                return "", -1
            while True:
                if e < lim_e:
                    n = random.randint(0, 99)
                    if n < low_up_lim:
                        msg = low
                    elif n < mid_up_lim:
                        msg = mid
                    else:
                        msg = high
                        if self.timeCheck(data, "SSJTouch_last_time", True):
                            add_e = e // 24 if e < 2400 else 100
                            player.set("emotion", e + add_e)
                    return I18n.format(msg), add_e
                add_lim_e += 50
                lim_e += add_lim_e
                low_up_lim = low_up_lim - 15 if low_up_lim > 15 else 1
                mid_up_lim = mid_up_lim - 10 if mid_up_lim > 9 else 9
        if get_msg in ("捏三色堇脸", "捏捏脸"):
            msg = msgChoice("kao_low", "kao_mid", "kao_high")
        elif get_msg in ("摸三色堇头", "摸摸头",):
            msg = msgChoice("atama_low", "atama_mid", "atama_high")
        elif get_msg in ("摸三色堇毒牙", "摸摸毒牙", "摸毒牙"):
            msg = msgChoice("dokuga_low", "dokuga_mid", "dokuga_high")
        elif get_msg in ("摸三色堇尾巴", "摸摸尾巴", "摸尾巴"):
            msg = msgChoice("shippo_low", "shippo_mid", "shippo_high")
        if msg is not None:
            if msg[1] < 0:
                self.server.sendGroup(
                    self.group_id, "咿呀！你是谁！？不要碰三色堇！？（你的手被警惕的三色堇弹开了）")
            elif msg[1] > 0:
                add_e_list = "（好感上升【+%g◈】）" % msg[1]
            self.server.sendGroup(self.group_id, msg[0] + add_e_list)

# 三色堇未来功能预定：
#     1.三色堇属性系统，对于群友的互动的反馈系统（投喂次数-体重，……）。
#     2.三色堇每天随机挑选一位群友进行【出行(晒太阳，爬山，吃饭，游乐园，看电影……)、读书、魔法研究、森林聆听妖精的歌声】（计数器记录一周内触发三色堇发言的人从中选择）。
#     3.举行活动到三色堇这里报名【魔法切磋（……）、】。
# 魔法体系：
#     1.魔素是生命力量人人皆有，但能通过魔素经络来操控魔素的人全世界不过一二,一般来说这种人在太古时期被人称之为【原初者】。
#     2.消耗魔素使用魔法。
#     3.魔素容量（天生决定），用了部分魔素可以自行回复，过度使用到极限值会对身体造成负担虚弱很长一段时间甚至死亡。
#     4.已知太古时期所改造出来的亚人是人类人工创造魔素经络的唯一方法，但是为了创造亚人很多人沦为牺牲品和实验品。
