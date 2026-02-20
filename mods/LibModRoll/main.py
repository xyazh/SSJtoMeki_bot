from xyacqbot.Cqserver import Cqserver
from xyacqbot.packet.PacketBase import PacketBase
from xyacqbot.packet.PacketMsg import PacketMsg
from xyacqbot.modsLoader.Container import Container

from .rolldata.UserRollData import UserRollData

class Main:
    cqserver: Cqserver = None
    instance: "Main" = None

    @staticmethod
    def main(moudles: list[Container]):
        Main.cqserver = Cqserver.instance
        Main.instance = Main()
        data = UserRollData("114514")
        print(data.getBindingCard(True).setAttrFromDSL("力量40str40敏捷80dex80意志65pow65体质45con45外貌55app55教育55edu55体型40siz40智力80灵感80int80san65san值65理智65理智值65幸运75运气75mp魔法hp8体力8会计5人类学1估价5考古学1取悦15魅惑15攀爬70计算机5计算机使用5电脑5信用5信誉5信用评级5克苏鲁0克苏鲁神话0cm0乔装5闪避80汽车20驾驶20汽车驾驶20电气维修10电子学1话术5斗殴80手枪60急救80历史5恐吓15跳跃70母语55法律5图书馆40图书馆使用40聆听50开锁1撬锁1锁匠1机械维修10医学1博物学10自然学10领航10导航10神秘学5重型操作1重型机械1操作重型机械1重型1说服40精神分析1心理学10骑术5妙手10侦查55潜行20生存10游泳45投掷20追踪10驯兽5潜水1爆破1读唇1催眠1炮术1"))
    @staticmethod
    def onBotOtherEvent(packet: PacketBase):
        pass

    @staticmethod
    def onBotMsgEvent(packet: PacketMsg):
        pass

    def __init__(self):
        pass
