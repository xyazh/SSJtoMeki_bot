import datetime,random,time
from ..GameSystem.PlayerSystem.Player import Player
from ..I18n.I18n import I18n
from .YxBaseGroup import YxBaseGroup
from ..GroupHelper import GroupHelper

class G558335813(YxBaseGroup):
    def __init__(self):
        super().__init__()
        self.group_id = 558335813

    #对于【当前时间】的回复
    @YxBaseGroup.register
    def nowTime(self,data):
        get_msg = GroupHelper.getMsg(data)
        if get_msg in ("当前时间","时间"):
            t = datetime.datetime.now()
            all_dict = {#回复总目录
            #平常
            "a":"现在是？……【%Y-%m-%d，%H:%M:%S】的说……嗯……应该没搞错吧……",
            "b":"【%Y-%m-%d，%H:%M:%S】的说……自己也可以看为什么要来问像我这样的人呢……",
            "c":"【%Y-%m-%d，%H:%M:%S】……希望不会发生什么不好的事就好了……",
            "d":"【%Y-%m-%d，%H:%M:%S】了呢，感觉好闲呢……吖呜（打哈欠），都不知道该干什么了……(￣▽￣)",
            "e":"【%Y-%m-%d，%H:%M:%S】的说，这个时间段大家在做什么呢？Ciallo～(∠·ω< )⌒☆",
            #凌晨 00.00-05.00
            "f":"啊~~~哈~~~呜~~~【%Y-%m-%d，%H:%M:%S】，都这么晚了……大家都不睡觉嘛……(´·ω·`)？",
            "g":"【%Y-%m-%d，%H:%M:%S】，嗷~~~好困的说……嗯嗯呃呃……",
            "h":"喵呜~~~【%Y-%m-%d，%H:%M:%S】，该睡觉了的说……",
            #早晨 05.00-08.00
            "i":"【%Y-%m-%d，%H:%M:%S】？好困啊……起床……不要……",
            "j":"(＠￣￢￣＠)zzZ，现在是……【%Y-%m-%d，%H:%M:%S】的说……呼呼……哈……zzZ",
            "k":"嗯呃……额……啊嗯……吃……真的吃不下了……嘿嘿……（【%Y-%m-%d，%H:%M:%S】）",
            "i1":"【%Y-%m-%d，%H:%M:%S】？怎么回事……啊呜……不要起床……不要……",
            #上午 08.00-11.00
            "l":"太阳……好烦……（把头埋进被子）嗯呃……（【%Y-%m-%d，%H:%M:%S】)",
            "m":"【%Y-%m-%d，%H:%M:%S】？还有点困呢，再睡一觉的说……(～￣▽￣)～",
            "n":"呼……哈……嗯嗯~？【%Y-%m-%d，%H:%M:%S】？等……等等再起床啦……",
            #中午 11.00-13.00
            "o":"【%Y-%m-%d，%H:%M:%S】，果然还是起来早点吃早饭比较好麻……",
            "p":"早上果然就应该一股脑地睡过去的说！啊，不是……我的意思是……都【%Y-%m-%d，%H:%M:%S】了呢，大家一定要养成早睡早起的好习惯，嗯……",
            "q":"糟！？都【%Y-%m-%d，%H:%M:%S】这个时间段了，再不去吃饭就要被骂了的说……(っ°Д°;)っ",
            "o1":"（啪哒）啊呜……（从床上滚到地板）磕到脚趾母了，脚好痛的说……（看向时钟）原来已经%Y-%m-%d，%H:%M:%S了吗……脚还是好痛的说……啊呜……",
            #下午 13.00-16.00
            "r":"【%Y-%m-%d，%H:%M:%S】……我能做些什么呢……果然什么都做不好的样子呢……",
            "s":"下午【%Y-%m-%d，%H:%M:%S】的说……还要多久这一天才能过去呢？",
            "t":"加把劲……哦……呃嗯……果然还是提不起劲的说，好想睡觉……（【%Y-%m-%d，%H:%M:%S】）",
            #傍晚 16.00-19.00
            "u":"【%Y-%m-%d，%H:%M:%S】……特地来问我……我也不会有什么特别的想法的说……",
            "v":"今天有没有夕阳呢？现在是(*°▽°*)【%Y-%m-%d，%H:%M:%S】的说",
            "w":"晚饭的香味？……肚子有点饿了的说……（【%Y-%m-%d，%H:%M:%S】）",
            #晚上 19.00-00.00
            "x":"都到【%Y-%m-%d，%H:%M:%S】了，不会还有什么没有做完的事情吧……",
            "y":"【%Y-%m-%d，%H:%M:%S】的说，有点晚了呢……不知道今天夜晚的星星有多少颗呢？",
            "z":"【%Y-%m-%d，%H:%M:%S】，已经到这个时间了，总感觉晚上好兴奋呢*★,°*:.☆\(￣▽￣)/$:*.°★*"
            }
            msg_dict = {#基于总目录的文本根据时间以此分类回复
            "lingchen":all_dict[random.choice(["f","g","h"])],
            "zaochen":all_dict[random.choice(["i","j","k"])],
            "shangwu":all_dict[random.choice(["l","m","n"])],
            "zhongwu":all_dict[random.choice(["o","p","q","a","b","c","d","e","o1"])],
            "xiawu":all_dict[random.choice(["r","s","t","a","b","c","d","e"])],
            "bangwan":all_dict[random.choice(["u","v","w","a","b","c","d","e"])],
            "wanshang":all_dict[random.choice(["x","y","z","a","b","c","d","e"])]
            }
            now_hour = int(datetime.datetime.now().strftime("%H"))
            match {0:0,1:0,2:0,3:0,4:0,5:1,6:1,7:1,8:2,9:2,10:2,11:3,12:3,13:4,14:4,15:4,16:5,17:5,18:5,19:6,20:6,21:6,22:6,23:6}[now_hour]:
                case 0:
                    self.server.sendGroup(self.group_id,t.strftime(msg_dict["lingchen"]))
                case 1:
                    self.server.sendGroup(self.group_id,t.strftime(msg_dict["zaochen"]))
                case 2:
                    self.server.sendGroup(self.group_id,t.strftime(msg_dict["shangwu"]))
                case 3:
                    self.server.sendGroup(self.group_id,t.strftime(msg_dict["zhongwu"]))
                case 4:
                    self.server.sendGroup(self.group_id,t.strftime(msg_dict["xiawu"]))
                case 5:
                    self.server.sendGroup(self.group_id,t.strftime(msg_dict["bangwan"]))
                case 6:
                    self.server.sendGroup(self.group_id,t.strftime(msg_dict["wanshang"]))

    # #三色堇的各种回复
    # @YxBaseGroup.register
    # def strSSJ(self,data):
    #     get_msg = GroupHelper.getMsg(data)
    #     msg_list = None
    #     #对于"三色堇抱抱"的回复
    #     if get_msg == "三色堇抱抱":
    #         player = Player(GroupHelper.getId(data))
    #         if self.timeCheck(data,"SSJBaobao_last_time"):
    #             n = 1
    #         else:
    #             n =  player.findGet("SSJBaobao_n",0)
    #             n += 1
    #         player.set("SSJBaobao_n",n)
    #         if n <= 5:
    #             msg_list = [
    #                 "阁下还真是爱撒娇呢，真是拿阁下没有办法呢，只……只限这一次的说哦。",
    #                 "睡在怀里的阁下真可爱呢，这件事可不要告诉大家哦。",
    #                 "怀里的阁下睡得真熟呢，就像小宝宝一样的说，今天一定是累坏了吧……",
    #                 "只要阁下不嫌弃三色堇的话……三色堇会静静安抚阁下的。",
    #                 "阁下一定累了吧，嘘~~~，没关系的哦，三色堇都知道的……",
    #                 "至少现在，请阁下放轻松……在我的膝上静静地休息吧……",
    #                 "没关系的，我不会像别人一样忘记阁下的，我会【永远】地记住阁下的……",
    #                 "阁下,我还在意着你的说，请不要这么难过……这样子…这样子三色堇也会伤心的……",
    #                 "都会没事的说，三色堇永远都会在这里等着阁下哦……"
    #                 "就让三色堇来施展一个消除伤心的魔法，把阁下的烦恼都放飞吧。"]
    #         elif n > 5:
    #             msg_list = ["今天的阁下…怎么这么爱撒娇呢……",
    #                 "阁下这是在是在戏弄三色堇吗…？",
    #                 "请阁下不要这样子捉弄三色堇的说……",
    #                 "阁下怎么这么爱撒娇……"]
    #     #对于【三色堇|跳楼】的回复
    #     elif "三色堇" in get_msg and "跳楼" in get_msg:
    #         player = Player(GroupHelper.getId(data))
    #         e =  player.getet("emotion")
    #         sub_e = random.randint(-5,0)
    #         player.set("emotion",e + sub_e)
    #         msg_list = [
    #             "嗯……感觉不是什么有意思的话题呢……（好感下降【%g◈】）"%sub_e,
    #             "那个……三色堇不是很想听这些的说……（好感下降【%g◈】）"%sub_e,
    #             "可以不要这样子嘛……突然感觉好难受的说……（好感下降【-%g◈】）"%sub_e,
    #             "突然有点想吐了……（好感下降【%g◈】）"%sub_e,
    #             "……嗯额……（好感下降【%g◈】）"%sub_e,
    #             "#三色堇扭扭捏捏的，看起来好像不太舒服。（好感下降【%g◈】）"%sub_e,
    #             "脚好痛……像被子弹打中了一样……为什么会痛的说……（好感下降【%g◈】）"%sub_e,
    #             "好冷的说……是我衣服穿少了吗……（好感下降【%g◈】）"%sub_e,
    #             "啊……那个……不是……（好感下降【%g◈】）"%sub_e,
    #             "人死之后才能变得幸福吗…………。嘿哈……开玩笑的说……（好感下降【%g◈】）"%sub_e,
    #             "三色堇感觉身体不是很舒服的说……（好感下降【%g◈】）"%sub_e]
    #     #对于【三色堇】的回复
    #     elif "三色堇" in get_msg:
    #         msg_list = [
    #             "嗯额……那个……\r\n找三色堇有什么事吗……",
    #             "嗯……额……要找三色堇吗？",
    #             "三色堇一直呆在这里的说……",
    #             "欸……在叫三色堇吗？",
    #             "Ciallo～(∠·ω< )⌒☆\r\n三色堇在这里。"]
    #     #对于【灰茉莉】的回复
    #     elif "灰茉莉" in get_msg:
    #         msg_list = [
    #             "灰茉莉……那是谁？",
    #             "灰茉莉……我不认识的说……",
    #             "……",
    #             "欸？什么？",
    #             "",]#如果没有那样的幼年，或许一切都会不一样的吧……
    #     elif "行" in get_msg or "彳亍" in get_msg or "可以" in get_msg:
    #         msg_list = [
    #             "还好啦……",
    #             "真的要这样子吗……",
    #             "这样子好吗……",
    #             "这样子可以吗？…",
    #             "……",
    #             "没有问题……"]
    #     elif  "是不是" in get_msg:
    #         msg_list = [
    #         "三色堇觉得应该……是……",
    #         "三色堇觉得不应该……是……"]
    #     elif ("三色堇" in get_msg and "是" in get_msg) or "三色堇是不是" in get_msg:
    #         msg_list = [
    #         "请不要评价三色堇……",
    #         "咦？",
    #         "额嗯？",
    #         "……"]
    #     if msg_list is not None:
    #         self.server.sendGroup(self.group_id,random.choice(msg_list))
        
    # #对于【三色堇】的肢体互动
    # @YxBaseGroup.register
    # def SSJTouch(self,data):
    #     player = Player(GroupHelper.getId(data))
    #     e = player.findGet("emotion",0)
    #     get_msg = GroupHelper.getMsg(data)
    #     msg,add_e_list = None,""
    #     def msgChoice(low,mid,high):
    #         lim_e,add_lim_e,low_up_lim,mid_up_lim,add_e = 50,50,90,99,0
    #         if e <= 0:
    #             return "",-1
    #         while True:
    #             if e < lim_e:
    #                 n = random.randint(0,99)
    #                 if n < low_up_lim:
    #                     msg = low
    #                 elif n < mid_up_lim:
    #                     msg = mid
    #                 else:
    #                     msg = high
    #                     if self.timeCheck(data,"SSJTouch_last_time",True):
    #                         add_e = e // 24 if e < 2400 else 100
    #                         player.set("emotion",e + add_e)
    #                 return I18n.format(msg),add_e
    #             add_lim_e += 50
    #             lim_e += add_lim_e
    #             low_up_lim = low_up_lim - 15 if low_up_lim > 15 else 1
    #             mid_up_lim = mid_up_lim - 10 if mid_up_lim > 9 else 9
    #     if   get_msg in ("捏三色堇脸","捏捏脸"):
    #         msg = msgChoice("kao_low","kao_mid","kao_high")
    #     elif get_msg in ("摸三色堇头","摸摸头",):
    #         msg = msgChoice("atama_low","atama_mid","atama_high")
    #     elif get_msg in ("摸三色堇毒牙","摸摸毒牙","摸毒牙"):
    #         msg = msgChoice("dokuga_low","dokuga_mid","dokuga_high")
    #     elif get_msg in ("摸三色堇尾巴","摸摸尾巴","摸尾巴"):
    #         msg = msgChoice("shippo_low","shippo_mid","shippo_high")
    #     if msg is not None:
    #         if msg[1] < 0:
    #             self.server.sendGroup(self.group_id,"咿呀！你是谁！？不要碰三色堇！？（你的手被警惕的三色堇弹开了）")
    #         elif msg[1] > 0:
    #             add_e_list = "（好感上升【+%g◈】）"%msg[1]
    #         self.server.sendGroup(self.group_id,msg[0] + add_e_list)

#三色堇未来功能预定：
    #1.三色堇属性系统，对于群友的互动的反馈系统（投喂次数-体重，……）。
    #2.三色堇每天随机挑选一位群友进行【出行(晒太阳，爬山，吃饭，游乐园，看电影……)、读书、魔法研究、森林聆听妖精的歌声】（计数器记录一周内触发三色堇发言的人从中选择）。
    #3.举行活动到三色堇这里报名【魔法切磋（……）、】。
#魔法体系：
    #1.魔素是生命力量人人皆有，但能通过魔素经络来操控魔素的人全世界不过一二,一般来说这种人在太古时期被人称之为【原初者】。
    #2.消耗魔素使用魔法。
    #3.魔素容量（天生决定），用了部分魔素可以自行回复，过度使用到极限值会对身体造成负担虚弱很长一段时间甚至死亡。
    #4.已知太古时期所改造出来的亚人是人类人工创造魔素经络的唯一方法，但是为了创造亚人很多人沦为了牺牲品和实验品。