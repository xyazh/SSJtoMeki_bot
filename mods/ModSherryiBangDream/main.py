from xyacqbot.Cqserver import Cqserver
from xyacqbot.packet.PacketBase import PacketBase
from xyacqbot.packet.PacketMsg import PacketMsg
from xyacqbot.modsLoader.Container import Container
from xyacqbot.xyazhServer.ConsoleMessage import ConsoleMessage

try:
    from mods.LibModCommand.command.Command import Command
except ImportError:
    Command = None
try:
    from .Client import Client
except ImportError:
    Client = None

class Main:
    cqserver: Cqserver = None
    instance: "Main" = None

    @staticmethod
    def main(moudles: list[Container]):
        Main.cqserver = Cqserver.instance
        Main.instance = Main()
        if Command is None:
            ConsoleMessage.printError("ModSherryBangDream需要LibModCommand模块，该模块未安装")
            raise ImportError("ModSherryBangDream需要LibModCommand模块，该模块未安装")
        if Client is None:
            ConsoleMessage.printError("ModSherryBangDream需要tsugu_api库，请自行安装")
            raise ImportError("ModSherryBangDream需要tsugu_api库，请自行安装")
        Client.register()
        from . import commands



    @staticmethod
    def onBotOtherEvent(packet: PacketBase):
        pass

    @staticmethod
    def onBotMsgEvent(packet: PacketMsg):
        pass

    def __init__(self):
        pass
