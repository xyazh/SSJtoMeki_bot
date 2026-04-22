from typing import Literal
from typing import Callable
from typing import TYPE_CHECKING
from xyacqbot.Cqserver import Cqserver
from xyacqbot.packet.PacketBase import PacketBase
from xyacqbot.packet.PacketMsg import PacketMsg
from xyacqbot.modsLoader.Container import Container
from xyacqbot.xyazhServer.ConsoleMessage import ConsoleMessage
from xyacqbot.timer.Timer import Timer

try:
    from mods.LibModCommand.command.Command import Command
except ImportError:
    Command = None
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
            ConsoleMessage.printError("ModMeki需要LibModCommand模块，该模块未安装")
        else:
            from . import commands
        if MCP is None:
            ConsoleMessage.printWarning("ModMeki需要LibModMCP模块，该模块未安装")
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
