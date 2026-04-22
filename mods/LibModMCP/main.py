import threading
from xyacqbot.Cqserver import Cqserver
from xyacqbot.packet.PacketBase import PacketBase
from xyacqbot.packet.PacketMsg import PacketMsg
from xyacqbot.modsLoader.Container import Container
from xyacqbot.xyazhServer.ConsoleMessage import ConsoleMessage

class Main:
    cqserver: Cqserver = None
    instance: "Main" = None

    @staticmethod
    def main(moudles: list[Container]):
        Main.cqserver = Cqserver.instance
        Main.instance = Main()
        Main.MCP = None
        try:
            from mods.LibModMCP.MCP import MCP
        except ImportError:
            ConsoleMessage.printError("未安装MCP库，无法启用MCP服务，请自行安装")
        Main.MCP = MCP()
    @staticmethod
    def postInit():
        if Main.MCP is None:
            return
        threading.Thread(target=Main.MCP.run,args=("sse",)).start()

       
    @staticmethod
    def onBotOtherEvent(packet: PacketBase):
        pass

    @staticmethod
    def onBotMsgEvent(packet: PacketMsg):
        pass

    def __init__(self):
        pass
