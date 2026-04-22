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
    from mods.LibModRoll.roll.Roll import Roll
except ImportError:
    Command = None
    Roll == None
try:
    from mods.LibModMCP.MCP import MCP
except ImportError:
    MCP = None


class Main:
    cqserver: Cqserver = None
    instance: "Main" = None

    @staticmethod
    def main(moudles: list[Container]):
        Main.cqserver = Cqserver.instance
        Main.instance = Main()
        if Command is None:
            ConsoleMessage.printError("ModSherry需要LibModCommand模块，该模块未安装")
            raise ImportError("ModSherry需要LibModCommand模块，该模块未安装")
        if Roll is None:
            ConsoleMessage.printError("ModSherry需要LibModRoll模块，该模块未安装")
            raise ImportError("ModSherry需要LibModRoll模块，该模块未安装")
        from . import commands
        if MCP is None:
            ConsoleMessage.printWarning("ModSherry需要LibModMCP模块，该模块未安装")
        else:
            from . import mcp



    @staticmethod
    def onBotOtherEvent(packet: PacketBase):
        pass

    @staticmethod
    def onBotMsgEvent(packet: PacketMsg):
        pass

    def __init__(self):
        pass
