import inspect,random,time,threading
from ..CQCode import CQCodeHelper
from ..GameSystem.PlayerSystem.Player import Player
from ..Order import Order
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
from ..GameSystem.YxClass.UserStatus import UserStatus
from ..MsgHelper import MsgHelper

BOT_NAME_SELF = "三色堇"
BOT_NAME = "三色堇"

class YxBaseGroup(BaseGroup,IRollGroup,ISSJGroup,ITTKGroup,IItemGroup):
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
    
    #确认time_name今日有无使用，未使用返回True，否返回False；以及如果没有使用是否将本次确认保存为今日第一次使用
    def timeCheck(self,data,time_name:str,bool:bool = False):
        player = Player(GroupHelper.getId(data))
        last_time = player.findGet(time_name,0)
        if (last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
            return False
        elif bool:
            player.set(time_name,time.time())
        return True

    #更改属性数值，返回更改值
    def ARTChange(self,data,change__name:str,change_number:float):
        player = Player(GroupHelper.getId(data))
        n = player.findGet(change__name,0)
        player.set(change__name,n + change_number)
        return change_number
########################################################################################################################
    #指令帮助列表及其详情说明
    @register
    @helpData(["normal"],"获取帮助","help","help (name)|/page/","help指令用于查看一般常用指令列表，可以添加一个参数作为需要查找的指令名字，来获取此指令的详细信息。")
    def help(self,data,order:Order):
        if order.checkOrder("help") or GroupHelper.getMsg(data) in ["帮助","获取帮助"]:
            arg = order.getArg(1)
            if arg == None:
                msg = "#-----帮助列表-----#\r\n%s\r\n------------------"%((I18n.format("ord")))
                for i in BaseGroup.HELP_CLASS_DATA:
                    msg += "\r\n%s：/help %s"%(BaseGroup.HELP_CLASS_DATA[i],i)
            elif arg in BaseGroup.HELP_CLASS_DATA:
                msg = "#-----%s-----#\r\n%s\r\n------------------"%(BaseGroup.HELP_CLASS_DATA[arg],(I18n.format("ord")))
                for i in self.helps_class[arg]:
                    msg += "\r\n%s：/%s"%(i[0],i[1])
                msg += "\r\n------------------\r\ntip：可使用/help (指令名)查看指令详细说明。\r\n例：/help pack--->查看/pack指令详细说明。"
            elif arg in self.helps:
                tx, ord, usg, datdetails = tuple(self.helps[arg])
                msg = "#---『%s』---#\r\n用法：\r\n/%s"%(tx,(usg))
                msg += "\r\n------------------\r\n功能详解：%s"%datdetails
                msg += "\r\n------------------\r\n数据类型详解：\r\n(可选参数) ; [必须参数]\r\n/未完成参数/ ; *可选语法\r\n...可重复 ; |或"
            else:
                self.server.sendGroup(self.group_id,(I18n.format("prob")) + "\r\n（找不到这样的指令）")
                return
            self.server.sendGroup(self.group_id,msg)

    #手动让三色堇退群
    @register
    @helpData(["other"],"退出该群","bye","bye","让三色堇退出该群。")
    def bye(self,data:dict,order:Order):
        if order.checkOrder("bye") or order.checkOrder("exit"):
            if GroupHelper.checkOwnerOrAdmin(data):
                self.server.setGroupLeave(self.group_id)

    #测试机器人发送信息
    @register
    @helpData(["other"],"测试指令","test","test (msg)","发送一句test或者指定的参数。")
    def test(self,data,order:Order):
        if order.checkOrder("test"):
            arg = order.getArg(1)
            if arg:
                self.server.sendGroup(self.group_id,arg)
            else: 
                self.server.sendGroup(self.group_id,"test")

    #输出机器人开发信息
    @register
    @helpData(["other"],"开发信息","bot","bot","输出机器人信息。")
    def bot(self,data,order:Order):
        if order.checkOrder("bot"):
            self.server.sendGroup(self.group_id,"Multi functional dice rolling bot made with Python by Xyazh")

    @register
    @helpData(["other"],"网页绑定","web_bind","web_bind [uid]","在网站上绑定qq用（跑团可能需要）")
    def webBindQQ(self, data: dict, order: Order):
        if not order.checkOrder("web_bind"):
            return
        uid = order.getArg(1)
        if uid == None:
            self.server.sendGroup(self.group_id, I18n.format("prob") + "（需要help吗）")
            return
        token = BestXor.bestEncryptXor(uid.encode("utf8"),b"%d"%GroupHelper.getId(data))
        self.server.sendGroup(self.group_id, "你的token是：\r\n%s"%token)
########################################################################################################################
    #获取功能列表
    @register
    @helpData(["normal"],"功能列表","fun","fun","功能列表，面向给群友使用的功能。直接发送“功能”或指令的方式就可以使用。")
    def function(self,data,order:Order):
        if GroupHelper.getMsg(data) in ["功能","功能列表"] or order.checkOrder("fun"):
            msg = "#-----功能列表-----#\r\n"
            msg += "获取帮助；每日签到\r\n✧未来视✧；✧未来启✧\r\n魔素具现；查看好感\r\n好感归零；随机涩图\r\n动画资讯；g a l资讯"
            msg += "\r\n------------------\r\n%s"%((I18n.format("fun")))
            self.server.sendGroup(self.group_id,msg)

    #获取发送者魔素点数
    @register
    @helpData(["normal"],"魔素具现","point","point","查看自己当前魔素点数。")
    def point(self,data,order:Order):
        if order.checkOrder("point") or GroupHelper.getMsg(data) in ["魔素具现","魔素"]:
            player = Player(GroupHelper.getId(data))
            pt = player.findGet("point")
            if pt == None:
                player.set("point",1)
                self.server.sendGroup(self.group_id,I18n.format("pt_0")%GroupHelper.getName(data))
            elif pt > 0:
                if pt < 10:
                    self.server.sendGroup(self.group_id,(I18n.format("pt_1"))%(GroupHelper.getName(data),pt))
                elif pt < 20:
                    self.server.sendGroup(self.group_id,(I18n.format("pt_2"))%(GroupHelper.getName(data),pt))
                elif pt < 60:
                    self.server.sendGroup(self.group_id,(I18n.format("pt_3"))%(GroupHelper.getName(data),pt))
                elif pt < 240:
                    self.server.sendGroup(self.group_id,(I18n.format("pt_4"))%(GroupHelper.getName(data),pt))
                elif pt < 1200:
                    self.server.sendGroup(self.group_id,(I18n.format("pt_5"))%(GroupHelper.getName(data),pt))
                elif pt < 7200:
                    self.server.sendGroup(self.group_id,(I18n.format("pt_6"))%(GroupHelper.getName(data),pt))
                else:
                    self.server.sendGroup(self.group_id,(I18n.format("pt_7"))%(pt,GroupHelper.getName(data)))
            else:
                self.server.sendGroup(self.group_id,(I18n.format("pt_neg"))%(GroupHelper.getName(data),pt))

    #获取三色堇对发送者好感度
    @register
    @helpData(["normal"],"查看好感","emotion","emotion","查看自己当前好感点数。")
    def emotion(self,data,order:Order):
        if order.checkOrder("emotion") or GroupHelper.getMsg(data) in ["查看好感","好感"]:
            player = Player(GroupHelper.getId(data))
            e = player.get("emotion")
            if e == None:
                player.set("emotion",1)
                self.server.sendGroup(self.group_id,I18n.format("e_0")%GroupHelper.getName(data))
            elif e > 0:
                if e < 150:
                    self.server.sendGroup(self.group_id,(I18n.format("e_1"))%(GroupHelper.getName(data),e))
                elif e < 300:
                    self.server.sendGroup(self.group_id,(I18n.format("e_2"))%(GroupHelper.getName(data),e))
                elif e < 600:
                    self.server.sendGroup(self.group_id,(I18n.format("e_3"))%(GroupHelper.getName(data),e))
                elif e < 1200:
                    self.server.sendGroup(self.group_id,(I18n.format("e_4"))%(GroupHelper.getName(data),e))
                elif e < 2400:
                    self.server.sendGroup(self.group_id,(I18n.format("e_5"))%(GroupHelper.getName(data),e))
                else:
                    self.server.sendGroup(self.group_id,(I18n.format(random.choice["e_6","e_5"]))%(GroupHelper.getName(data),e))
            else:
                self.server.sendGroup(self.group_id,(I18n.format("e_neg"))%(GroupHelper.getName(data),e))

    #向三色堇道歉
    @register
    @helpData(["normal"],"好感归零","sorry","sorry","向三色堇道歉以让你为负数的可怜好感度归0。（所以说你干了什么要用这个指令？）")
    def sorry(self,data,order:Order):
        if order.checkOrder("sorry") or GroupHelper.getMsg(data) in ["好感归零","道歉"]:
            player = Player(GroupHelper.getId(data))
            e = player.get("emotion")
            if e == None:
                self.server.sendGroup(self.group_id,I18n.format("e_rst_0"))
            elif e < 0:
                player.set("emotion",1)
                self.server.sendGroup(self.group_id,I18n.format("e_rst_1")%(GroupHelper.getName(data)))
            else:
                self.server.sendGroup(self.group_id,I18n.format("e_rst_ng")%(GroupHelper.getName(data),e))

    #获取签到者签到天数，并加魔素与好感
    @register
    @helpData(["normal"],"每日签到","sign","sign","签到，签到计数所有群通用。直接发送签到或指令的方式就可以使用。")
    def sign(self,data,order:Order):
        if GroupHelper.getMsg(data) in ["每日签到","签到"] or order.checkOrder("sign"):
            player = Player(GroupHelper.getId(data))
            last_time = player.findGet("last_time")
            if last_time == None:
                player.set("last_time",time.time())
                player.set("day",1)
                pt = player.findGet("point",0)
                player.set("point",pt + 1)
                self.server.sendGroup(self.group_id,I18n.format("sign_0")%(GroupHelper.getName(data)))
                return
            if (last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
                self.server.sendGroup(self.group_id,I18n.format("sign_ng")%(GroupHelper.getName(data),time.time()-last_time))
            else:
                day = player.findGet("day",0)
                e = player.findGet("emotion",0)
                pt = player.findGet("point",0)
                day += 1
                add_e = random.randint(1,int(day//40) + 1) if int(day//40) < 10 else random.randint(10,20)
                add_pt = random.randint(int(day//4),day//2)                    
                player.set("last_time",time.time())
                player.set("day",day)
                player.set("emotion",e + add_e)
                player.set("point",pt + add_pt)
                self.server.sendGroup(self.group_id,I18n.format("sign_1")%(GroupHelper.getName(data),day,add_pt,add_e))

    #获取发送者占卜命运结果
    @register
    @helpData(["normal"],"✧未来视✧","fate","fate","吾が名はパンジー↑！随一の魔法使いにして身に魔神✦↑『デイアブロス』↑✦を封印されし、根源の力を↑引き継げり、そしていつか魔法の真理に辿り着きも↓の↑！\r\n")
    def meiunn(self,data,order:Order):
        if GroupHelper.getMsg(data) in ["占卜","未来视","✧未来视✧"] or order.checkOrder("fate"):
            player = Player(GroupHelper.getId(data))
            pt = player.findGet("point")
            def change_point(min,max):
                if (fate_last_time + 8 * 3600) // (24 * 3600) != (time.time() + 8 * 3600) // (24 * 3600):
                    change_pt = random.randint(min,max)
                    player.set("point",pt + change_pt)
                    player.set("fate_change_pt",change_pt)
                else:
                    change_pt = player.get("fate_change_pt")
                return change_pt
            msg = "请“%s”阁下，先去查看一下自己的『魔素』吧。"%GroupHelper.getName(data)
            if pt is not None:
                fate_last_time = player.findGet("fate_last_time",0)
                add_msg = "\r\n(获得魔素【+%g✧】)\r\n------------------\r\n"
                sub_msg = "\r\n(丢失魔素【%g✧】)\r\n------------------\r\n"
                end_msg = ""
                fate = int(random.randint(0,99))
                flag = True
                if fate_last_time and self.unnsei_once_a_day:
                    if (fate_last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
                        end_msg = "\r\n------------------\r\n“%s”阁下，那、那个…… 【%.2f】秒前已经占卜了的说……不满意的话要三色堇使用『✧未来启✧』吗？……"%(GroupHelper.getName(data),time.time() - fate_last_time)
                        _fate = player.findGet("fate",0)
                        if isinstance(_fate,int):
                            fate = _fate
                            flag = False
                if flag:
                    player.set("fate_last_time",time.time())
                    player.set("fate",fate)
                if fate < 1:
                    r_msg = "✧『⛧崩れし大地、破裂し蒼穹⛧』✧" + sub_msg % change_point(-100,-50)
                    r_msg += (I18n.format("fate_1")) + end_msg
                elif fate < 3:
                    r_msg = "✧『⛧破滅世界の結末⛧』✧" + sub_msg % change_point(-50,-40)
                    r_msg += (I18n.format("fate_2")) + end_msg
                elif fate < 6:
                    r_msg = "✧『⛧終焉の大厄災⛧』✧" + sub_msg % change_point(-40,-30)
                    r_msg += (I18n.format("fate_3")) + end_msg
                elif fate < 10:
                    r_msg = "✧『冥界不祥の角笛』✧" + sub_msg % change_point(-25,-20)
                    r_msg += (I18n.format("fate_4")) + end_msg
                elif fate < 15:
                    r_msg = "✧『呪いの指輪』✧" + sub_msg % change_point(-20,-15)
                    r_msg += (I18n.format("fate_5")) + end_msg
                elif fate < 21:
                    r_msg = "✧『深淵の凝視』✧" + sub_msg % change_point(-15,-10)
                    r_msg += (I18n.format("fate_6")) + end_msg
                elif fate < 28:
                    r_msg = "『悪魔の囁き』" + sub_msg % change_point(-10,-5)
                    r_msg += (I18n.format("fate_7")) + end_msg
                elif fate < 36:
                    r_msg = "『鬼の悪戯』" + sub_msg % change_point(-5,-1)
                    r_msg += (I18n.format("fate_8")) + end_msg
                elif fate < 45:
                    r_msg = "『尻尾切』\r\n------------------\r\n"
                    r_msg += (I18n.format("fate_9")) + end_msg
                elif fate < 55:
                    r_msg = "『無変の平日』\r\n------------------\r\n"#中间值
                    r_msg += (I18n.format("fate_10")) + end_msg
                elif fate < 64:
                    r_msg = "『些か運』\r\n------------------\r\n"
                    r_msg += (I18n.format("fate_11")) + end_msg
                elif fate < 72:
                    r_msg = "『聖域の水』" + add_msg%change_point(5,10)
                    r_msg += (I18n.format("fate_12")) + end_msg
                elif fate < 79:
                    r_msg = "『御守の光』" + add_msg%change_point(10,15)
                    r_msg += (I18n.format("fate_13")) + end_msg
                elif fate < 85:
                    r_msg = "✧『天使の歌声』✧" + add_msg%change_point(15,20)
                    r_msg += (I18n.format("fate_14")) + end_msg
                elif fate < 90:
                    r_msg = "✧『精霊の恵み』✧" + add_msg%change_point(20,25)
                    r_msg += (I18n.format("fate_15")) + end_msg
                elif fate < 94:
                    r_msg = "✧『世界祝福の加護』✧" + add_msg%change_point(25,30)
                    r_msg += (I18n.format("fate_16")) + end_msg
                elif fate < 97:
                    r_msg = "✧『✦神々守の強運✦』✧" + add_msg%change_point(40,60)
                    r_msg += (I18n.format("fate_17")) + end_msg
                elif fate < 99:
                    r_msg = "✧『✦素晴世界の初風✦』✧" + add_msg%change_point(60,80)
                    r_msg += (I18n.format("fate_18")) + end_msg
                else:
                    r_msg = "✧『✦咲き誇る花、舞い踊る瓣✦』✧" + add_msg%change_point(80,150)
                    r_msg += (I18n.format("fate_19")) + end_msg
                msg = "%s\r\n“%s”的预言之语是……\r\n------------------\r\n%s"%((I18n.format("mgc_fate")),GroupHelper.getName(data),r_msg)
            self.server.sendGroup(self.group_id,msg)

    #媒介转运
    @register
    @helpData(["normal"],"✧未来启✧","fate_change","fate_change","吾が名はパンジー↑！随一の魔法使いにして身に魔神✦↑『デイアブロス』↑✦を封印されし、根源の力を↑引き継げり、そしていつか魔法の真理に辿り着きも↓の↑！\r\n")
    def fateChange(self,data,order:Order):
        if GroupHelper.getMsg(data) in ["运转","未来启","✧未来启✧"] or order.checkOrder("fate_change"):
            player = Player(GroupHelper.getId(data))
            change_pt = player.findGet("fate_change_pt",0)
            add_msg = "\r\n(获得魔素【+%g✧】)\r\n------------------\r\n"
            sub_msg = "\r\n(丢失魔素【%g✧】)\r\n------------------\r\n"
            end_msg = "\r\n------------------\r\n『✧未来启✧』每日只作用一次的说……"
            if self.timeCheck(data,"fate_last_time"):
                msg = "阁下今天还没有让我使用过『✧未来视✧』呢……"
            else:
                msg = I18n.format("pass_text")
            self.server.sendGroup(self.group_id,msg)

# #test
#     @register
#     @helpData(["normal"],"✧裁判✧","saiban","saiban","开庭辩论")
#     def ccoTest(self,data,order:Order):
#         if qqid == UserStatus.:
#             self.server.groupBan(self.group_id,qqid,sec)
#         if GroupHelper.getMsg(data) in ["ccoTest"] or order.checkOrder("ccoTest"):
#             cqcodes = CQCodeHelper.creatCQCodeFromMsg(GroupHelper.getMsg(data))
#             at_ids = []
#             for i in cqcodes:
#                 if i.t == "at":
#                     at_ids.append(i.data["qq"])
#             if len(at_ids) != 2:
#                 return
#             else:
#                 UserStatus.useBan(at_ids[0],at_ids[1])
#             while True:
#                 self.server.groupBan(self.group_id,qqid,sec)
            
    #获取当日动漫资讯
    @register
    @helpData(["normal"],"动画资讯","anime_news","anime_news","获取当日动漫新闻。资讯来源于网络，每小时会尝试更新，直接发送动漫新闻、动画新闻、二次元新闻、anime新闻、动漫资讯、动画资讯、二次元资讯、anime资讯有同样效果。")
    def getAnimeNews(self,data,order:Order):
        if GroupHelper.getMsg(data) in ["动漫新闻","动画新闻","二次元新闻","anime新闻","动漫资讯","动画资讯","二次元资讯","anime资讯"]:
            order = GroupHelper.getOrderFromStr(ORDER_SPLIT_LIST[0] + "anime_news")
        if order.checkOrder("anime_news"):
            li = LoopEvent.today_anime_news
            if len(li)>0:
                self.server.sendGroup(self.group_id,li[random.randint(0,len(li)-1)])
                return
            self.server.sendGroup(self.group_id,"三色堇没有更多的信息了……不要再找三色堇了……")

    #获取当日gal新闻
    @register
    @helpData(["normal"],"g a l资讯","gal_news","gal_news (0-9*|all)","获取当日gal新闻。资讯来源于网络，每小时会尝试更新。参数为空随机，为all输出全部，数字输出当前条数，发送gal新闻、galgame新闻、gal资讯、galgame资讯也可随机获取一条。")
    def getGalNews(self,data,order:Order):
        if GroupHelper.getMsg(data) in ["gal新闻","galgame新闻","gal资讯","galgame资讯","g a l资讯"]:
            order = GroupHelper.getOrderFromStr(ORDER_SPLIT_LIST[0] + "gal_news")
        if order.checkOrder("gal_news"):
            li = LoopEvent.today_galgame_news
            arg = order.getArg(1)
            if len(li)<=0:
                self.server.sendGroup(self.group_id,"噶呜……三色堇知道的信息都已经说完了……")
                return
            if arg == None:
                self.server.sendGroup(self.group_id,li[random.randint(0,len(li)-1)])
                return
            if arg == "all":
                if len(li)>0:
                    msg = "今日gal:"
                    n = 0
                    for i in li:
                        n += 1
                        msg += "\r\n\r\n%d.%s"%(n,i)
                    self.server.sendGroup(self.group_id,msg)
                    return
            if arg.isdigit():
                i = int(arg)
                if i > 0 and i < len(li):
                    msg = "%d.%s"%(i,li[i-1])
                    self.server.sendGroup(self.group_id,msg)
                    return
                self.server.sendGroup(self.group_id,"那个……三色堇也找不到相关的信息的说……")
                return
            self.server.sendGroup(self.group_id,(I18n.format("prob")) + "\r\n（需要help吗）")

    #获取随机涩图
    @register
    @helpData(["normal"],"随机涩图","roll_img","roll_img","随机获取涩图。")
    def rollImg(self,data:dict,order:Order):
        if order.checkOrder("roll_img"):
            #self.s.sendImgToGroupFromUrl(self.group_id,"https://iw233.cn/api.php?sort=iw233")
            self.server.sendImgToGroupFromUrl(self.group_id,"https://www.dmoe.cc/random.php")

    @register
    @helpData(["normal"],"生成语音","vits","vits [text] (language)","发出真奈美的声音，可以自动识别语言和也可以指定语言，支持日本語、简体中文、English。")
    def vits(self,data:dict,order:Order):
        if not order.checkOrder("vits"):
            return
        def t(self:YxBaseGroup,data:dict,order:Order):
            text = order.getArg(1)
            l = order.getArg(2)
            if not text:
                self.server.sendGroup(self.group_id,(I18n.format("prob")) + "\r\n（未输入文字）")
                return
            if l in ("日本語","简体中文","English"):
                r = GenVoice.gen(text,l)
            else:
                r = GenVoice.genVioce(text)
            if not r:
                self.server.sendGroup(self.group_id,(I18n.format("prob") + "\r\n（语音生成失败）"))
                return
            r = r.replace("C:\\","C:\\\\")
            self.server.sendGroup(self.group_id,"[CQ:record,file=file:///%s]"%r)
        th = threading.Thread(target=t,args=(self,data,order))
        th.start()