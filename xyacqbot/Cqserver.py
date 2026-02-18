import urllib.parse
import typing
import json
import os
import re
from .xyazhServer import ConsoleMessage, App, Server
from .xyazhRequest import HTTPRequest, HTTPSRequest, RequestData, ResponseData
from .packet.PacketMsg import PacketMsg
from .packet.PacketBase import PacketBase
from .msg.MsgBuilder import MsgBuilder
from .modsLoader.ModsLoader import ModLoader
from .modsLoader.Container import Container
from .webApp.WebApp import WebApp
from .datamanager.GlobleDataManager import GlobalDataManager
from .datamanager.UserDataManager import UserDataManager
from .CommandDLS import CommandDLS
from .TemplateEngine import TemplateEngine, UserData, Template, Random, Time

if typing.TYPE_CHECKING:
    class Mod:
        class Main:
            @staticmethod
            def main(moudles: list[Container]):
                ...

            @staticmethod
            def onBotOtherEvent(packet: PacketBase):
                ...

            @staticmethod
            def onBotMsgEvent(packet: PacketMsg):
                ...


class Cqserver:
    instance = None

    def __init__(self, ip: str, send_port: int, lisent_port: int, web_port: int):
        self.ip = ip
        self.send_port = send_port
        self.lisent_port = lisent_port
        self.web_port = web_port
        self.on_event_fuctions: list[typing.Callable] = []
        Cqserver.instance = self

    def onEvent(self, fuction: typing.Callable):
        self.on_event_fuctions.append(fuction)

    def loadMods(self):
        self.mod_loader = ModLoader(os.getcwd()+"\\mods")
        self.mod_loader.loadAll()
        self.mods = self.mod_loader.getMods()
        mod: "Mod"
        for mod in self.mods.values():
            containers = [
                Container("cqserver", self, "object")
            ]
            mod.Main.main(containers)

    def modOnEvent(self, p: PacketBase):
        mods = self.mod_loader.getMods()
        mod: "Mod"
        for mod in mods.values():
            if isinstance(p, PacketMsg):
                if p.shouldIgnore():
                    return
                mod.Main.onBotMsgEvent(p)
            elif isinstance(p, PacketBase):
                mod.Main.onBotOtherEvent(p)

    def printTitleVison(self):
        print(f" * ---------------------------------")
        print(f" * Multi functional dice rolling bot made with Python by Xyazh")
        print(f" * Http发送地址 {self.ip}:{self.send_port}")
        print(f" * Http接收上报地址 http://{self.ip}:{self.lisent_port}/")
        print(f" * 后台管理地址 http://{self.ip}:{self.web_port}/res/index.html")
        print(f" * アトリは、高性能ですから!")
        print(f" * ---------------------------------")

    def initLisentFunc(self):
        pass

    def initWebFunc(self):
        pass

    def initFuc(self):
        self.loadMods()
        self.onEvent(self.modOnEvent)
        self.onEvent(self.onMsgEvent)

    def autoReply(self, p: PacketMsg):
        msg = p.getMsg()
        global_data_manager = GlobalDataManager()
        reply_rules = global_data_manager.getAutoReplyRules()
        user = UserData(p.getId(), p.getNickname(), p.getCardname(
        ), p.sender.sex, p.sender.age, p.sender.level, p.sender.role)
        user_data = UserDataManager(p.getId())
        random = Random()
        time = Time()
        for rule in reply_rules.values():
            if not rule["enabled"]:
                continue
            trigger = rule["trigger"]
            reply = TemplateEngine(rule["reply"])
            mode = rule["mode"]
            if mode == "exact":
                if msg == trigger:
                    result = reply.render(
                        user=user, user_data=user_data, random=random, time=time)
                    self.sendGroupMsg(result, p.group_id)
            elif mode == "fuzzy":
                result = re.match(trigger, msg)
                if result is not None:
                    result = reply.render(
                        user=user, user_data=user_data, random=random, time=time)
                    self.sendGroupMsg(result, p.group_id)
            elif mode == "dsltp":
                dsl = CommandDLS(trigger)
                t_data = dsl.template(msg)
                if t_data is None:
                    continue
                template = Template(t_data)
                result = reply.render(
                    user=user, template=template, user_data=user_data, random=random, time=time)
                self.sendGroupMsg(result, p.group_id)

    def onMsgEvent(self, p: PacketBase):
        if not isinstance(p, PacketMsg):
            return
        if p.message_type == "group":
            if p.shouldIgnore():
                ConsoleMessage.printC(
                    f"忽略群{p.group_id}{p.getName()}({p.getId()})的消息：{p.getMsg()}")
                return
            ConsoleMessage.printC(
                f"来自群{p.group_id}{p.getName()}({p.getId()})的消息：{p.getMsg()}")
            self.autoReply(p)

    def serverRun(self):
        self.printTitleVison()
        self.newLisentApp(self.ip, self.lisent_port)
        self.newWebApp(self.ip, self.web_port)
        print("\r\n\r\n")
        self.initFuc()

    def newWebApp(self, ip: str, port: int):
        self.web_app: App = App(ip, port)
        self.web_app_page = WebApp(self.web_app, self)
        fun = self.web_app.runHTTP
        self.web_app.runThead(fun, (self.initWebFunc,))

    def newLisentApp(self, ip: str, post_port: int):
        self.lisent_server: App = App(ip, post_port)
        self.lisent_server.page_manager.addPath(
            "/", self.cqhttpApiConnector, "POST")
        fuc = self.lisent_server.runHTTP
        self.lisent_server.runThead(fuc, (self.initLisentFunc,))

    def cqhttpApiConnector(self, server: Server):
        data: bytes = server.readPostData(max_size=10240)
        try:
            cqhttp_data: dict = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            server.send_error(400, "json decoder error")
            return
        self.mainEventHandler(cqhttp_data)
        server.sendTextPage("ok")

    def mainEventHandler(self, raw_data: dict):
        if PacketMsg.like(raw_data):
            p = PacketMsg(raw_data)
        else:
            p = PacketBase(raw_data)
        for f in self.on_event_fuctions:
            f(p)

    def send(self, h_path: str, data: dict = None, ignore: bool = False) -> ResponseData | None:
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
        result = h_requse.execute(h_data, ignore=ignore)
        if result is None:
            if ignore:
                return None
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

    def uploadGroupFile(self, group_id: int, file: str, name: str = None, folder_id: str = None) -> ResponseData | None:
        data = {"group_id": group_id, "file": file}
        if name is not None:
            data["name"] = name
        if folder_id is not None:
            data["folder_id"] = folder_id
        return self.send("/upload_group_file", data)

    def leaveGroup(self, group_id: int) -> ResponseData | None:
        data = {"group_id": group_id}
        return self.send("/set_group_leave", data)

    def setGroupBan(self, group_id: int, user_id: int, duration: int = 0) -> ResponseData | None:
        data = {"group_id": group_id, "user_id": user_id, "duration": duration}
        return self.send("/set_group_ban", data)

    def _getGroupList(self, no_cache: bool = False) -> ResponseData | None:
        data = {
            "no_cache": no_cache
        }
        return self.send("/get_group_list", data)

    def getGroupList(self, no_cache: bool = False) -> list[dict] | None:
        """
        data: [{"group_id": 123456,"group_name": "群名称","group_memo": "","group_create_time": 1234567890,"member_count": 123,"max_member_count": 200,"remark_name": ""}]
        """
        result = self._getGroupList(no_cache)
        if result is None:
            return None
        data = result.json()
        if data is None:
            return None
        status = data.get("status", "error")
        if status != "ok":
            return None
        data = data.get("data", [])
        return data

    def _getStatus(self) -> ResponseData | None:
        return self.send("/get_status", {}, ignore=True)

    def getStatus(self) -> dict:
        """
        data: {"status": "ok","retcode":0,"online": true,"good": true}
        """
        result = self._getStatus()
        if result is None:
            return {"status": "error", "recode": -1, "online": False, "good": False}
        data = result.json()
        if data is None:
            return {"status": "error", "recode": -1, "online": False, "good": False}
        status = data.get("status", "error")
        recode = data.get("retcode", -1)
        data_data: dict = data.get("data", {})
        online = data_data.get("online", False)
        good = data_data.get("good", False)
        return {"status": status, "recode": recode, "online": online, "good": good}

    def escapeMsg(self, msg: str) -> str:
        msg = urllib.parse.quote(msg)
        return msg
