import datetime
import re
import random
import time
import html
import logging
import threading
import json
import inspect
from ..CQCode import CQCodeHelper, CQCode
from ..GameSystem.PlayerSystem.Player import Player
from ..Order import Order
from ..LoopEvent import LoopEvent
from ..GroupHelper import GroupHelper
from ..GroupHelper import ORDER_SPLIT_LIST
from ..GenVoice import GenVoice
from ..I18n.I18n import I18n
from ..MsgData import MsgData
from ..xyazhServer.BestXor import BestXor
from ..GameSystem.Helper import RollHelper
from ..GameSystem.ToolClass.BaseData import BaseData
from .BaseGroup import BaseGroup


BOT_NAME = "meki酱"
BOT_NAME_SELF = "meki"
HELP_CLASS_DATA = {"n": "常用命令", "r": "跑团命令", "o": "其他命令", "i": "RPG系统"}
ALIAS = {"normal": "n", "roll": "r", "other": "o", "item": "i"}


@GroupHelper.addActiveGroups(114514)
class BaseGroupPreset(BaseGroup):
    BOT_NAME = BOT_NAME
    BOT_NAME_SELF = BOT_NAME_SELF

    ai_chating = False

    def _getHelpsData(self):
        self.helps_class: dict[str:list[str]] = {
            i: [] for i in HELP_CLASS_DATA}
        self.helps: dict[str:list[str]] = {}
        for fuc in inspect.getmembers(self):
            if hasattr(fuc[1], "help_data"):
                help_data: list = fuc[1].help_data
                ord_classes, tx, ord, usg, datdetails = tuple(help_data)
                ord_classes = [ALIAS.get(i, i) for i in ord_classes]
                li = [tx, ord, usg, datdetails]
                for i in ord_classes:
                    i = i if i in HELP_CLASS_DATA else "o"
                    if i in self.helps_class:
                        self.helps_class[i].append(li)
                    else:
                        self.helps_class.update({i: [li]})
                self.helps.update({ord: li})

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "获取帮助", "help", "help (name)|/page/", "help指令用于查看一般常用指令列表，可以添加一个参数作为需要查找的指令名字，来获取此指令的详细信息")
    def help(self, data: dict, order: Order):
        if order.checkOrder("help"):
            msg = "#------帮助------\r\nMulti functional dice rolling bot made with Python by Xyazh\r\n\r\nmeki酱在这里哟~\r\n"
            arg = order.getArg(1)
            if arg == None:
                msg += "命令："
                for i in HELP_CLASS_DATA:
                    msg += "\r\n%s：help %s" % (HELP_CLASS_DATA[i], i)
                msg += I18n.format("help_exit_group_msg") % (
                    BOT_NAME_SELF, BOT_NAME)
            elif arg in HELP_CLASS_DATA:
                msg += "%s：" % HELP_CLASS_DATA[arg]
                for i in self.helps_class[arg]:
                    msg += "\r\n%s：%s" % (i[0], i[1])
            elif arg in self.helps:
                tx, ord, usg, datdetails = tuple(self.helps[arg])
                msg += "%s：" % tx
                msg += "\r\n%s     %s" % (ord, usg)
                msg += "\r\n%s" % datdetails
                msg += I18n.format("help_1")
            else:
                self.server.sendGroup(self.group_id, I18n.format(
                    "help_not_found") % BOT_NAME)
                return
            msg += I18n.format("help_2")
            self.server.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["o"], "测试指令", "test", "test (msg)", "发送一句test或者指定的参数")
    def test(self, data: dict, order: Order):
        if order.checkOrder("test"):
            arg = order.getArg(1)
            if arg:
                self.server.sendGroup(self.group_id, arg)
            else:
                self.server.sendGroup(self.group_id, "test")

    @BaseGroup.register
    def testImg(self, data: MsgData, order: Order):
        cq_codes = CQCodeHelper.creatCQCodeFromMsg(data.getMsg())
        for cq_code in cq_codes:
            if cq_code.t != "image":
                continue

    @BaseGroup.register
    @BaseGroup.helpData(["o"], "退出该群", "bye", "bye", "让机器人退出该群")
    def bye(self, data: dict, order: Order):
        if order.checkOrder("bye") or order.checkOrder("exit"):
            if GroupHelper.checkOwnerOrAdmin(data):
                self.server.setGroupLeave(self.group_id)

    @BaseGroup.register
    @BaseGroup.helpData(["n", "o"], "开发信息", "bot", "bot", "输出机器人信息")
    def bot(self, data: dict, order: Order):
        if order.checkOrder("bot"):
            self.server.sendGroup(
                self.group_id, I18n.format("bot_desc"))

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "每日签到", "sign", "sign", "签到，签到计数所有群通用。直接发送签到或指令的方式就可以使用")
    def sign(self, data: dict, order: Order):
        if not (GroupHelper.getMsg(data) in ["签到", "sign"] or order.checkOrder("sign") or order.checkOrder("签到")):
            return
        qq_id = GroupHelper.getId(data)
        player = Player(qq_id)
        last_time = player.findGet("last_time", 0)
        if last_time//(24*3600) == time.time()//(24*3600):
            self.server.sendGroup(self.group_id, "%s，%.2f秒前才签到过。这么快就忘了" % (
                GroupHelper.getName(data), time.time()-last_time))
        else:
            n = player.findGet("n", 1)
            p = player.findGet("point", 1)
            ap = random.randint(int(n//2), n)
            ap = 1 if ap <= 0 else ap
            self.server.sendGroup(self.group_id, "%s，今天已签到。第%d天签到获得：%dP，今天也来见%s了呢" % (
                GroupHelper.getName(data), n, ap, BOT_NAME))
            player.set("n", n+1)
            player.set("point", p+ap)
            player.set("last_time", time.time())

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "今日运势", "jrrp", "jrrp", "查询当前运势，图一乐。直接发送运势或指令的方式就可以使用")
    def meiunn(self, data: dict, order: Order):
        if not (GroupHelper.getMsg(data) == "运势" or order.checkOrder("运势") or order.checkOrder("jrrp")):
            return
        qq_id = GroupHelper.getId(data)
        player = Player(qq_id)
        ys_last_time = player.findGet("ys_last_time", 0)
        ys = RollHelper.bestRandomGuassRange(50, 35, 0, 100)
        ys = int(round(ys))
        flag = True
        if ys_last_time and self.unnsei_once_a_day:
            if ys_last_time//(24*3600) == time.time()//(24*3600):
                _ys = player.findGet("ys")
                if _ys != None:
                    ys = _ys
                    flag = False
        if flag:
            player.set("ys_last_time", time.time())
            player.set("ys", ys)
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
        msg = "%s今日的幸运指数是%i %s" % (GroupHelper.getName(data), 100-ys, r)
        self.server.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "动漫资讯", "anime_news", "anime_news", "获取当日动漫新闻。资讯来源于网络，每小时会尝试更新，直接发送动漫新闻、动画新闻、二次元新闻、anime新闻、动漫资讯、动画资讯、二次元资讯、anime资讯有同样效果")
    def getAnimeNews(self, data: dict, order: Order):
        if GroupHelper.getMsg(data) in ("动漫新闻", "动画新闻", "anime新闻", "动漫资讯", "动画资讯", "anime资讯", "anime", "动漫", "动画"):
            order = GroupHelper.getOrderFromStr(
                ORDER_SPLIT_LIST[0] + "anime_news")
        if order.checkOrder("anime_news"):
            li = LoopEvent.today_anime_news
            if len(li) > 0:
                self.server.sendGroup(
                    self.group_id, li[random.randint(0, len(li)-1)])
                return
            self.server.sendGroup(self.group_id, "当前没有资讯力")

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "游戏资讯", "gal_news", "gal_news (0-9*|all|msg) (hour)", "获取当日gal新闻。资讯来源于网络，每小时会尝试更新，也可自行添加新闻，第一个参数为新闻内容，第二个参数为新闻存在的小时数。参数为空随机，为all输出全部，数字输出当前条数，发送gal新闻、galgame新闻、gal资讯、galgame资讯也可随机获取一条")
    def getGalNews(self, data: dict, order: Order):
        if order.checkOrderRe(r"^(gal_news|gal新闻|galgame新闻|gal资讯|galgame资讯|旮旯|gal|galgame)$", True):
            group_data = BaseData(self.group_id)
            saved_news: dict[str:int] = group_data.data.get("gal_news", {})
            date_time = time.time()
            for i in [del_key for del_key in saved_news if saved_news[del_key] < date_time]:
                del saved_news[i]
            li = LoopEvent.today_galgame_news[:]
            li.extend(saved_news.keys())
            arg = order.getArg(1)
            if len(li) <= 0:
                self.server.sendGroup(self.group_id, "当前没有资讯力")
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
                if i > 0 and i <= len(li):
                    msg = "%d.%s" % (i, li[i-1])
                    self.server.sendGroup(self.group_id, msg)
                    return
                self.server.sendGroup(self.group_id, "好像没有这条资讯")
                return
            hour = order.getArg(2, float)
            if hour is not None:
                saved_news[arg] = date_time + hour*3600
                group_data.data["gal_news"] = saved_news
                self.server.sendGroup(self.group_id, I18n.format("已经添加资讯"))
                return
            self.server.sendGroup(self.group_id, I18n.format("has_help"))

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "添加回复", "ppp", "ppp [msg] [{dosomething}*t1|...]", "ppp(push posted plus)指令是add指令的升级版。ppp设置参数1为关键词。参数2为机器人随机回复的语料组，{dosomething}表示当机器人随机选中当前这条语料后额外执行的操作（仅群主或管理员可用）\r\n\r\n操作列表：\r\n增加点数：p_add([number])\r\n减少点数：p_sub([number])\r\n设置禁言：p_ban([number])")
    def ppp(self, data: dict, order: Order):
        if order.checkOrder("ppp"):
            a1 = order.getArg(1)
            a2 = order.getArg(2)
            if not (a1 and a2):
                self.server.sendGroup(self.group_id, I18n.format("has_help"))
                return
            a_list = [i for i in a2.split("|") if i != ""]
            is_owner_or_admin = GroupHelper.checkOwnerOrAdmin(data)
            p_li = []
            for a in a_list:
                ra = re.match(r"\{.*\}", a)
                if ra:
                    tx = a[ra.end():]
                    if not is_owner_or_admin:
                        self.server.sendGroup(
                            self.group_id, "只有群主或管理员才能使用{dosomething}操作")
                        return
                    o = ORDER_SPLIT_LIST[0] + "%s" % ra.group()[1:-1]
                    o = o.replace("(", " ")
                    o = o.replace(")", " ")
                    o = o.replace("（", " ")
                    o = o.replace("）", " ")
                    m_order = GroupHelper.getOrderFromStr(o)
                    if m_order.checkOrder("p_add"):
                        arg = m_order.getArg(1)
                        if arg and arg.isdigit():
                            p_li.append([tx, "p_add", int(arg)])
                        else:
                            self.server.sendGroup(self.group_id, "操作用法好像不对")
                            return
                    elif m_order.checkOrder("p_sub"):
                        arg = m_order.getArg(1)
                        if arg and arg.isdigit():
                            p_li.append([tx, "p_sub", int(arg)])
                        else:
                            self.server.sendGroup(self.group_id, "操作用法好像不对")
                            return
                    elif m_order.checkOrder("p_ban"):
                        arg = m_order.getArg(1)
                        if arg and arg.isdigit():
                            p_li.append([tx, "p_ban", int(arg)])
                        else:
                            self.server.sendGroup(self.group_id, "操作用法好像不对")
                            return
                    else:
                        self.server.sendGroup(
                            self.group_id, "嗯，不支持%s操作呢（需要help吗）" % m_order.getArg(0)[1:])
                        return
                else:
                    p_li.append([a, "", 0])
            dp: dict = self.data_manager.get(
                str(self.group_id) + ".json", "ppp")
            da: dict = self.data_manager.get(
                str(self.group_id) + ".json", "add")
            if isinstance(da, dict):
                if a1 in da:
                    da.pop(a1)
                    self.data_manager.set(
                        str(self.group_id) + ".json", "add", da)
            if isinstance(dp, dict):
                dp.update({a1: p_li})
                self.data_manager.set(str(self.group_id) + ".json", "ppp", dp)
                self.server.sendGroup(
                    self.group_id, "嗯，%s记住了！" % BOT_NAME_SELF)
            else:
                dp = {a1: p_li}
                self.data_manager.set(str(self.group_id) + ".json", "ppp", dp)
                self.server.sendGroup(
                    self.group_id, "嗯，%s记住了！" % BOT_NAME_SELF)

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "添加回复", "add", "add [msg1] [msg2]", "当机器人收到msg1时回复msg2")
    def add(self, data: dict, order: Order):
        if order.checkOrder("add"):
            a1 = order.getArg(1)
            a2 = order.getArg(2)
            if not (a1 and a2):
                self.server.sendGroup(self.group_id, I18n.format("has_help"))
                return
            dp: dict = self.data_manager.get(
                str(self.group_id) + ".json", "ppp")
            if isinstance(dp, dict):
                if a1 in dp:
                    dp.pop(a1)
                    self.data_manager.set(
                        str(self.group_id) + ".json", "ppp", dp)
            da: dict = self.data_manager.get(
                str(self.group_id) + ".json", "add")
            if isinstance(da, dict):
                da.update({a1: a2})
                self.data_manager.set(str(self.group_id) + ".json", "add", da)
                self.server.sendGroup(
                    self.group_id, "嗯，%s记住了！" % BOT_NAME_SELF)
            else:
                da = {a1: a2}
                self.data_manager.set(str(self.group_id) + ".json", "add", da)
                self.server.sendGroup(
                    self.group_id, "嗯，%s记住了！" % BOT_NAME_SELF)

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "删除回复", "del", "del [del]", "删除add和ppp设置的自动回复")
    def delt(self, data: dict, order: Order):
        if order.checkOrder("del"):
            a1 = order.getArg(1)
            if not a1:
                self.server.sendGroup(self.group_id, I18n.format("has_help"))
                return
            flag = True
            dp: dict = self.data_manager.get(
                str(self.group_id) + ".json", "ppp")
            if isinstance(dp, dict):
                if a1 in dp:
                    dp.pop(a1)
                    self.data_manager.set(
                        str(self.group_id) + ".json", "ppp", dp)
                    self.server.sendGroup(
                        self.group_id, "%s不会再这样子说了" % BOT_NAME_SELF)
                    flag = False
            da: dict = self.data_manager.get(
                str(self.group_id) + ".json", "add")
            if isinstance(da, dict):
                if a1 in da:
                    da.pop(a1)
                    self.data_manager.set(
                        str(self.group_id) + ".json", "add", da)
                    self.server.sendGroup(
                        self.group_id, "%s不会再这样子说了" % BOT_NAME_SELF)
                    flag = False
            if flag:
                self.server.sendGroup(
                    self.group_id, "%s好像没有这样过" % BOT_NAME_SELF)

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "查看点数", "point", "point", "查看当前点数")
    def point(self, data: dict, order: Order):
        if order.checkOrder("point"):
            player = Player(GroupHelper.getId(data))
            point = player.findGet("point", 1)
            self.server.sendGroup(self.group_id, "%s当前拥有点数：%s" %
                                  (GroupHelper.getName(data), point))

    @BaseGroup.register
    def autoMsg(self, data: dict):
        msg = GroupHelper.getMsg(data)
        da: dict = self.data_manager.get(str(self.group_id) + ".json", "add")
        if isinstance(da, dict):
            if msg in da:
                self.server.sendGroup(self.group_id, da[msg])
                return
        dp: dict = self.data_manager.get(str(self.group_id) + ".json", "ppp")
        if isinstance(dp, dict):
            if msg in dp:
                li = dp[msg]
                r_m = li[random.randint(0, len(li)-1)]
                msg = r_m[0]
                o = r_m[1]
                n = r_m[2]
                if o == "p_add":
                    p = self.data_manager.get(
                        str(GroupHelper.getId(data))+".json", "point")
                    p = p if p else 1
                    self.data_manager.set(
                        str(GroupHelper.getId(data))+".json", "point", p + n)
                elif o == "p_sub":
                    p = self.data_manager.get(
                        str(GroupHelper.getId(data))+".json", "point")
                    p = p if p else 1
                    self.data_manager.set(
                        str(GroupHelper.getId(data))+".json", "point", p - n)
                elif o == "p_ban":
                    self.server.groupBan(
                        self.group_id, GroupHelper.getId(data), n)
                self.server.sendGroup(self.group_id, msg)

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "随机图片", "roll_img", "roll_img", "随机获取涩图")
    def rollImg(self, data: dict, order: Order):
        if order.checkOrder("roll_img"):
            # self.s.sendImgToGroupFromUrl(self.group_id,"https://iw233.cn/api.php?sort=iw233")
            self.server.sendImgToGroupFromUrl(
                self.group_id, "https://www.dmoe.cc/random.php")

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "生成语音", "vits", "vits [text] (language)", "发出真奈美的声音，可以自动识别语言和也可以指定语言，支持日本語、简体中文、English")
    def vits(self, data: dict, order: Order):
        if not order.checkOrder("vits"):
            return

        def t(self: BaseGroup, data: dict, order: Order):
            text = order.getArg(1)
            l = order.getArg(2)
            if not text:
                self.server.sendGroup(self.group_id, I18n.format("has_help"))
                return
            if l in ("日本語", "简体中文", "English"):
                r = GenVoice.gen(text, l)
            else:
                r = GenVoice.genVioce(text)
            if not r:
                self.server.sendGroup(self.group_id, I18n.format("gen_loss"))
                return
            r = r.replace("C:\\", "C:\\\\")
            self.server.sendGroup(
                self.group_id, "[CQ:record,file=file:///%s]" % r)
        th = threading.Thread(target=t, args=(self, data, order))
        th.start()

    @BaseGroup.register
    @BaseGroup.helpData(["o"], "网页绑定", "web_bind", "web_bind [uid]", "在网站上绑定qq用（跑团可能需要）")
    def webBindQQ(self, data: dict, order: Order):
        if not order.checkOrder("web_bind"):
            return
        uid = order.getArg(1)
        if uid == None:
            self.server.sendGroup(self.group_id, I18n.format("has_help"))
            return
        token = BestXor.bestEncryptXor(uid.encode(
            "utf8"), b"%d" % GroupHelper.getId(data))
        self.server.sendGroup(self.group_id, "你的token是：\r\n%s" % token)

    @BaseGroup.register
    @BaseGroup.helpData(["o"], "执行语句", "exec", "exec [code]", "执行一段代码，仅限机器人所有者可用")
    def sExec(self, data: dict, order: Order):
        if order.checkOrder("exec") and GroupHelper.getId(data) in (330237917, 2132196134, 629233064):
            try:
                msg = GroupHelper.getMsg(data)
                arg = msg[6:]
                if not arg:
                    return
                co = html.unescape(arg)
                exec(co)
            except BaseException as e:
                logging.exception(e)
                self.server.sendGroup(self.group_id, str(e))

    @BaseGroup.register
    @BaseGroup.helpData(["n"], "随机食物", "/what_do_eat", "what_do_eat", "看看吃什么")
    def whatDoEatT(self, data: dict, order: Order):
        if not order.checkOrder("what_do_eat") and GroupHelper.getMsg(data) not in ("吃什么", "今天吃什么", "吃什么好", "看看吃什么"):
            return
        today = datetime.date.today()
        m_d = "%s-%s" % (today.month, today.day)
        if random.randint(1, 100) == 50:
            foods = ("纵连", "交互")
            msgs = ("请您吃%s", "%s，请")
        elif m_d in ("1-14", "5-14", "8-10", "11-4"):
            foods = ("雪", "〇堡肉", "林檎", "红茶", "布丁", "秘制酱料",
                     "极霸矛", "蔬菜棒", "迎宾酒", "爱心便当", "金液", "秘制酱拌面")
            msgs = ("那你就吃%s罢", "吃%s挺适合你的", "吃%s完了有奖励，吃不完有惩罚")
        else:
            foods = ("东坡肉", "冷锅鱼", "豆花", "甜皮鸭", "卤鸭子", "鱼香肉丝", "回锅肉", "麻婆豆腐", "炝炒大白菜", "金沙玉米",
                     "辣子鸡", "酸菜鱼", "水煮鱼", "毛血旺", "夫妻肺片", "火锅", "红烧排骨", "烧烤脑花", "锅巴肉片", "蒸鱼",
                     "糖醋鲤鱼", "葱烧海参", "九转大肠", "油爆双脆", "油焖大虾", "醋椒鱼", "糟熘鱼片", "苦瓜烘蛋", "小煎兔",
                     "温炝鳜鱼片", "芫爆鱿鱼卷", "清汤银耳", "糖醋里脊", "红烧大虾", "招远蒸丸", "清蒸加吉鱼", "把子肉",
                     "葱椒鱼片", "糖酱鸡块",  "乌鱼蛋汤", "锅烧鸭", "香酥鸡",  "黄焖鸡", "烧鸡", "长寿面", "香肠", "红烧狮子头",
                     "奶汤鲫鱼", "虾饺", "烧卖", "糯米鸡", "叉烧包", "鸡蛋卷", "肠粉", "炒河粉", "凤爪", "卤牛杂", "薄脆",
                     "煎饼", "烤鸭", "老鸭汤", "盐水鸭", "板鸭", "松鼠鳜鱼", "叫花鸡", "卤鸡", "清炖甲鱼", "糖醋鳜鱼", "文思豆腐",
                           "粉蒸肉", "烧白", "辣椒炒肉", "剁椒鱼头", "泡椒鳝段", "花椒鸡", "红烧牛肉", "肝腰合炒", "宫保鸡丁", "干煸四季豆",
                           "番茄炒蛋", "青椒肉丝", "蛋炒饭", "兰州拉面", "泡椒腰花", "小炒肉", "羊肉串", "石锅拌饭", "冬瓜排骨", "美蛙鱼头",
                           "惠灵顿牛排", "意大利面", "春卷", "寿司", "照烧鸡", "墨西哥卷", "仰望星空", "炸鸡", "秋葵鸡", "沙拉", "三明治", "苹果派",
                           "面包", "蛋糕", "汉堡", "披萨")
            msgs = ("我觉得%s还不错", "那就尝尝%s吧", "试试%s如何")
        msg = random.choice(msgs) % random.choice(foods)
        self.server.sendGroup(self.group_id, msg)

    # @BaseGroup.register
    def fireStar(self, data: dict, order: Order):
        msg = GroupHelper.getMsg(data)
        cqs = CQCodeHelper.creatCQCodeFromMsg(msg)
        cq = None
        for i in cqs:
            if i.t == "json":
                cq = i
        if cq is None:
            return
        data = json.loads(html.unescape(cq.data["data"]))
        if data["app"] != "com.tencent.multimsg":
            return
        msg_id = data["meta"]["detail"]["resid"]
        f_msg = self.server.getForwardMsg(msg_id)
        j_f_msg: dict = json.loads(f_msg)
        d = j_f_msg["data"]["messages"]
        for i in d:
            t = None
            t = i.get("time")
            break
        if t is not None:
            dt_object = datetime.datetime.fromtimestamp(float(t))
            year = dt_object.year
            month = dt_object.month
            day = dt_object.day
            self.server.sendGroup(
                self.group_id, "此聊天记录记录于%s-%s-%s" % (year, month, day))
