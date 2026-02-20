from typing import Literal
from typing import Callable
from typing import TYPE_CHECKING
from xyacqbot.Cqserver import Cqserver
from xyacqbot.packet.PacketBase import PacketBase
from xyacqbot.packet.PacketMsg import PacketMsg
from xyacqbot.modsLoader.Container import Container
from xyacqbot.xyazhServer.ConsoleMessage import ConsoleMessage

try:
    from mods.LibModCommand.command.Command import Command
except ImportError:
    Command = None

class Main:
    cqserver: Cqserver = None
    instance: "Main" = None

    @staticmethod
    def main(moudles: list[Container]):
        Main.cqserver = Cqserver.instance
        Main.instance = Main()
        if Command is None:
            ConsoleMessage.printError("ModMeki需要LibModCommand模块，该模块未安装")
            raise ImportError("ModMeki需要LibModCommand模块，该模块未安装")
        from . import commands


    @staticmethod
    def onBotOtherEvent(packet: PacketBase):
        pass

    @staticmethod
    def onBotMsgEvent(packet: PacketMsg):
        pass

    def __init__(self):
        pass
