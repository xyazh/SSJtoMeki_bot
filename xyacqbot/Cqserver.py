import urllib.parse
import typing
import json
import os
from .xyazhServer import ConsoleMessage, App, PageManager, Server
from .xyazhRequest import HTTPRequest, HTTPSRequest, RequestData, ResponseData
from .Packet.PacketMsg import PacketMsg
from .Packet.PacketBase import PacketBase
from .msg.MsgBuilder import MsgBuilder
from .ModsLoader.ModsLoader import ModLoader
from .ModsLoader.Container import Container
from .Order import Order

if typing.TYPE_CHECKING:
    pass


class Cqserver:
    def __init__(self, ip: str, send_port: int, lisent_port: int):
        self.ip = ip
        self.send_port = send_port
        self.lisent_port = lisent_port
        

    def loadMods(self):
        self.mod_loader = ModLoader(os.getcwd()+"\\mods")
        self.mod_loader.loadAll()
        self.mods = self.mod_loader.getMods()
        for mod in self.mods.values():
            containers = [
                Container("cqserver", self, "object")
            ]
            mod.Main.main(containers)

    def printTitleVison(self):
        print(" * ---------------------------------")
        print(" * Multi functional dice rolling bot made with Python by Xyazh")
        print(" * 在浏览器打开 http://%s:%s/res/index.html 进行可视化后台管理" %
              (self.ip, self.lisent_port))
        print(" * アトリは、高性能ですから!")
        print(" * ---------------------------------")

    def initFunc(self):
        self.loadMods()

    def serverRun(self):
        self.printTitleVison()
        self.newLisentApp(self.ip, self.lisent_port)
        fuc = self.lisent_server.runHTTP
        self.lisent_server.runThead(fuc, (self.initFunc,))

    def newLisentApp(self, ip: str, post_port: int):
        self.lisent_server: App = App(ip, post_port)
        PageManager.addPath("/", self.cqhttpApiConnector, "POST")

    def cqhttpApiConnector(self, server: Server):
        data: bytes = server.readPostData(max_size=10240)
        try:
            cqhttp_data: dict = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            server.send_error(400, "json decoder error")
            return
        self.mainMsgHandler(cqhttp_data)
        server.sendTextPage("ok")

    def mainMsgHandler(self, raw_data: dict):
        mods = self.mod_loader.getMods()
        for mod in mods.values():
            if PacketMsg.like(raw_data):
                p = PacketMsg(raw_data)
                mod.Main.onBotMsgEvent(p)
            else:
                p = PacketBase(raw_data)
                mod.Main.onBotOtherEvent(p)

    def send(self, h_path: str, data: dict = None) -> ResponseData | None:
        h_requse = HTTPRequest(self.ip, self.send_port)
        h_type = "GET"
        if data is not None:
            h_type = "POST"
        h_data = RequestData(h_type, h_path)
        h_data.addBodys({
            "Connection": "close",
            "Host": self.ip
        })
        h_data.setJsonData(data)
        result = h_requse.execute(h_data)
        if result is None:
            ConsoleMessage.printError(
                f"Cqserver request failed path: {h_path}")
            return None
        if result.status_code // 100 == 2:
            ConsoleMessage.printDebug(
                f"Cqserver report succescefully status:{result.status_code} message: {result.reason_phrase} for path: {h_path}")
        elif (result.status_code // 100 == 4) or (result.status_code // 100 == 5):
            ConsoleMessage.printError(
                f"Cqserver report failed status:{result.status_code} message: {result.reason_phrase} for path: {h_path}")
        else:
            ConsoleMessage.printWarning(
                f"Cqserver report error status:{result.status_code} message: {result.reason_phrase} for path: {h_path}")
        return result

    def sendGroupMsg(self, msg: str | MsgBuilder, group_id: int) -> ResponseData | None:
        if isinstance(msg, str):
            message = [{"type": "text", "data": {"text": msg}}]
        else:
            message = msg.msg
        data = {"group_id": group_id, "message": message}
        return self.send("/send_group_msg", data)

    def sendPrivateMsg(self, msg: str | MsgBuilder, user_id: int) -> ResponseData | None:
        if isinstance(msg, str):
            message = [{"type": "text", "data": {"text": msg}}]
        else:
            message = msg.msg
        data = {"user_id": user_id, "message": message}
        return self.send("/send_private_msg", data)

    def leaveGroup(self, group_id: int) -> ResponseData | None:
        data = {"group_id": group_id}
        return self.send("/set_group_leave", data)

    def setGroupBan(self, group_id: int, user_id: int, duration: int = 0) -> ResponseData | None:
        data = {"group_id": group_id, "user_id": user_id, "duration": duration}
        return self.send("/set_group_ban", data)

    def escapeMsg(self, msg: str) -> str:
        msg = urllib.parse.quote(msg)
        return msg
