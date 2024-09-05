import inspect
import json
import urllib.parse
import threading
import logging
import typing
import os
import time

from .Event import Event
from .GroupHelper import GroupHelper
from .ServerHelper import ServerHelper
from .MsgData import MsgData
from .WebApp.MyWebApp import MyWebApp
from .MsgHelper import MsgHelper
from .CQCode import CQCode
from .xyazhServer import App
from .xyazhServer import PageManager
from .xyazhServer import Server
from .xyazhServer import ConsoleMessage
from .xyazhRequest import HTTPRequest, HTTPSRequest, RequestData, ResponseData
from .OpenQQ.OpenQQServer import OpenQQServer
from .DataManager import DataManager

from typing import Callable
from typing import BinaryIO
from urllib import request

if typing.TYPE_CHECKING:
    from . import cqgroups
    from .cqgroups.BaseGroup import BaseGroup


class Cqserver:
    @staticmethod
    def patch(fuc):
        def newFuc(*args, **kw):
            if (threading.current_thread() == threading.main_thread()):
                print(
                    "\r\n/*----------------------------------------------------------------")
                print(">> %s:" % fuc.__name__)
                for i in args:
                    print(">> %s" % i)
                for i in kw:
                    print(">> %s=%s" % (i, kw[i]))
                print(
                    "/*----------------------------------------------------------------\r\n")
                return
            return fuc(*args, **kw)
        return newFuc

    def __init__(self, ip: str, port: int, post_port: int):
        self.ip = ip
        self.port = port
        self.post_port = post_port
        self.reg_func: dict[int:list[Callable]] = {}
        self.ban_func: dict[int:list[Callable]] = {}
        self.data_manager: DataManager = DataManager("\\config\\")
        self.newWebAndListenApp(ip, post_port)
        self.register()

    def tryRunOpenQQ(self):
        if not self.data_manager.hasFile("opqq.json"):
            self.data_manager.craftFile("opqq.json", {
                "use_open_qq": False,
                "app_id": 114514,
                "client_secret": "xxxxxxxxxxxxxxx",
                "mandatory_use_group": False
            })
        if not self.data_manager.findGet("opqq.json", "use_open_qq", False):
            ConsoleMessage.printC("未启用OpenQQ")
            return
        app_id = self.data_manager.findGet("opqq.json", "app_id", None)
        client_secret = self.data_manager.findGet(
            "opqq.json", "client_secret", None)
        if app_id is None or client_secret is None:
            ConsoleMessage.printError("未配置OpenQQ")
            return
        self.openqq_server = OpenQQServer(self, app_id, client_secret)
        threading.Thread(target=self.openqq_server.run).start()

    def printTitleVison(self):
        print(" * ---------------------------------")
        print(" * Multi functional dice rolling bot made with Python by Xyazh")
        print(" * 在浏览器打开 http://%s:%s/res/index.html 进行可视化后台管理" %
              (self.ip, self.post_port))
        print(" * アトリは、高性能ですから!")
        print(" * ---------------------------------")

    def newWebAndListenApp(self, ip: str, post_port: int):
        self.web_and_listen: App = App(ip, post_port)
        self.web_and_listen.http_server.cqserver = self
        real_root = "./web/public"
        virtual_root = "/res"

        def virtualPath(server: Server):
            path = server.virtual_path.replace(virtual_root, real_root, 1)
            server.sendFile(path)
        PageManager.addFileTree(real_root, virtual_root, virtualPath)
        PageManager.addPath("/", self.cqhttpApiConnector, "POST")
        MyWebApp()

    def registerGObj(self, group_obj: "BaseGroup"):
        group_obj.setSender(self)
        func_list = []
        for fuc in inspect.getmembers(group_obj):
            if hasattr(fuc[1], "sign_reg"):
                func_list.append(fuc[1])
        event: Event.GruopRegisterEvent = Event.EventBus.hookGruopRegisterEvent(
            group_obj.group_id, func_list, self)
        if event.getCancel():
            return
        self.reg_func.update({event.group_id: event.fucs})

    def register(self):
        clazz = None
        from . import cqgroups
        from .cqgroups.BaseGroup import BaseGroup
        class_list = ServerHelper.getFullClassesFormModul(
            cqgroups, lambda clazz: issubclass(clazz, BaseGroup))
        for ClassGroup in class_list:
            try:
                clazz = ClassGroup
                group_obj: BaseGroup = None
                if clazz in GroupHelper.ACTIVE_GROUPS:
                    for group_id in GroupHelper.ACTIVE_GROUPS[ClassGroup]:
                        group_obj = ClassGroup()
                        group_obj.group_id = group_id
                        self.registerGObj(group_obj)
                        group_obj = None
                group_obj = ClassGroup()
                self.registerGObj(group_obj)
                group_obj = None
            except BaseException as e:
                log = "加载%s|%s时出错" % (
                    "初始化" if clazz == None else clazz.__name__, clazz)
                if group_obj != None:
                    log += "|当前群号：%s" % group_obj.group_id
                ConsoleMessage.printError(log)
                logging.exception(e)

    def cqhttpApiConnector(self, server: Server):
        data: bytes = server.readPostData(max_size=10240)
        try:
            cqhttp_data: dict = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            server.send_error(400, "json decoder error")
            return
        self.mainMsgHandler(cqhttp_data)
        server.sendTextPage("ok")

    def testMsg(self, group_id: int, msg: str):
        self.mainMsgHandler(MsgHelper.createMsg(group_id, msg))

    def mainMsgHandler(self, raw_data: dict):
        data = MsgData(raw_data)
        if not "message_type" in data:
            return
        message_type = data["message_type"]
        if message_type == "group":
            if not "group_id" in data:
                return
            if not 'raw_message' in data:
                return
            event: Event.FucGroupMsgEvent = Event.EventBus.hookFucGroupMsgEvent(
                data, "recv", self)
            if event.getCancel():
                return
            group_id = event.getGroupId()
            data['raw_message'] = event.getMsg()
            if group_id in self.reg_func:
                order = GroupHelper.getOrderFromData(data)
                for func in self.reg_func[data["group_id"]]:
                    if ServerHelper.checkFunsArgs(func, (data, order)):
                        func(data, order)
                    else:
                        func(data)
        if data["message_type"] == "private":
            Event.EventBus.hookPrivateMsgEvent(data, "recv", self)

    def initFunc(self):
        from .I18n.I18n import I18n
        I18n.data_loader.loadLang()

    def serverRun(self):
        self.printTitleVison()
        fuc = self.web_and_listen.runHTTP
        self.web_and_listen.runThead(fuc, (self.initFunc,))
        time.sleep(1)
        self.tryRunOpenQQ()

    def escapeMsg(self, msg: str) -> str:
        msg = urllib.parse.quote(msg)
        return msg

    def get(self, path: str) -> ResponseData | None:
        h_requse = HTTPRequest(self.ip, self.port)
        data = RequestData("GET", path)
        data.setJsonData({
            "Connection": "close",
            "Host": self.ip
        })
        result = h_requse.execute(data)
        if result is None:
            ConsoleMessage.printError(f"Cqserver request failed path: {path}")
            return None
        if result.status_code // 100 == 2:
            ConsoleMessage.printDebug(
                f"Cqserver report succescefully status:{result.status_code} message: {result.reason_phrase} for path: {path}")
        elif (result.status_code // 100 == 4) or (result.status_code // 100 == 5):
            ConsoleMessage.printError(
                f"Cqserver report failed status:{result.status_code} message: {result.reason_phrase} for path: {path}")
        else:
            ConsoleMessage.printWarning(
                f"Cqserver report error status:{result.status_code} message: {result.reason_phrase} for path: {path}")
        return result

    def _getImgRaw(self, img_cqcode: CQCode) -> dict | None:
        if "file" not in img_cqcode.data:
            return None
        path = self.get("/get_image?file=%s" % img_cqcode.data["file"])
        path_json: dict
        try:
            path_json = path.json()
        except json.decoder.JSONDecodeError as e:
            return None
        return path_json

    def _getImgPath(self, img_raw: dict) -> str:
        if img_raw is None:
            return ""
        if "data" in img_raw and "file" in img_raw["data"]:
            return img_raw["data"]["file"]
        return ""

    @patch
    def sendGroup(self, group_id: str | int, msg: str):
        fuc_group_msg_event: Event.FucGroupMsgEvent = Event.EventBus.hookFucGroupMsgEvent(
            {"raw_message": msg, "group_id": group_id}, "send", self)
        msg = fuc_group_msg_event.getMsg()
        group_id = fuc_group_msg_event.getGroupId()
        if not fuc_group_msg_event.getCancel():
            msg = self.escapeMsg(msg)
            self.get("/send_msg?message_type=group&group_id=%s&message=%s" %
                     (group_id, msg))

    @patch
    def sendPrivate(self, id: str | int, msg: str):
        private_msg_event: Event.PrivateMsgEvent = Event.EventBus.hookPrivateMsgEvent(
            {"raw_message": msg, "user_id": id, "sub_type": "sender"}, "send", self)
        msg = private_msg_event.getMsg()
        if not private_msg_event.getCancel():
            msg = self.escapeMsg(msg)
            self.get(
                "/send_msg?message_type=private&user_id=%s&message=%s" % (id, msg))

    @patch
    def setGroupLeave(self, group_id: str | int):
        self.get("/set_group_leave?group_id=%s" % (group_id))

    @patch
    def sendImgToGroupFromPath(self, group_id: str | int, path: str):
        cq = "[CQ:image,file=%s,cache=0]" % ("file:///" + path)
        self.get("/send_msg?message_type=group&group_id=%s&message=%s" %
                 (group_id, cq))

    @patch
    def sendImgToGroupFromUrl(self, group_id: str | int, url: str):
        cq = "[CQ:image,file=%s,cache=0]" % url
        self.get("/send_msg?message_type=group&group_id=%s&message=%s" %
                 (group_id, cq))

    @patch
    def getGroupList(self) -> ResponseData:
        return self.get("/get_group_list")

    @patch
    def getForwardMsg(self, msg_id: str | int) -> ResponseData:
        return self.get("/get_forward_msg?message_id=%s" % msg_id)

    @patch
    def groupBan(self, group_id: str | int, qqid: int, time: int):
        self.get("/set_group_ban?group_id=%s&user_id=%d&duration=%d" %
                 (group_id, qqid, time))

    @patch
    def getForwardMsg(self, msg_id: str | int) -> ResponseData:
        return self.get("/get_forward_msg?message_id=%s" % msg_id)

    @patch
    def groupBan(self, group_id: str | int, qqid: int, sec: int):
        self.get("/set_group_ban?group_id=%s&user_id=%d&duration=%d" %
                 (group_id, qqid, sec))

    @patch
    def getImgRaw(self, img_cqcode: CQCode) -> dict | None:
        return self._getImgRaw(img_cqcode)

    @patch
    def getImgPath(self, img_cqcode: CQCode) -> str:
        img_raw = self._getImgRaw(img_cqcode)
        return self._getImgPath(img_raw)

    @patch
    def getImgData(self, img_cqcode: CQCode) -> bytes:
        img_raw = self._getImgRaw(img_cqcode)
        img_path = self._getImgPath(img_raw)
        img_data = b""
        try:
            with open(img_path, "rb") as f:
                img_data = f.read()
        except BaseException as e:
            ConsoleMessage.printWarning("获取图片失败：%s" % e)
            logging.exception(e)
        return img_data
