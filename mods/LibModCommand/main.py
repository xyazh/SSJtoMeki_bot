from xyacqbot.Cqserver import Cqserver
from xyacqbot.packet.PacketBase import PacketBase
from xyacqbot.packet.PacketMsg import PacketMsg
from xyacqbot.modsLoader.Container import Container

from mods.LibModCommand.command.Command import Command


class Main:
    cqserver: Cqserver = None
    instance: "Main" = None

    @staticmethod
    def main(moudles: list[Container]):
        Main.cqserver = Cqserver.instance
        Main.instance = Main()

    @staticmethod
    def onBotOtherEvent(packet: PacketBase):
        pass

    @staticmethod
    def onBotMsgEvent(packet: PacketMsg):
        if packet.message_type != "group" or not packet.group_id:
            return
        text = packet.getMsg()
        send_list = Command.dispatch(text, packet)
        for i in send_list:
            if i:
                Main.cqserver.sendGroupMsg(i, packet.group_id)

    def __init__(self):
        pass
