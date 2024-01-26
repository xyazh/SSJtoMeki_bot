import inspect
import json
import urllib.parse

from .Event import Event
from .GroupHelper import GroupHelper
from .ServerHelper import ServerHelper
from .WebApp.MyWebApp import MyWebApp
from .xyazhServer import App
from .xyazhServer import PageManager
from .xyazhServer import Server
from typing import Callable
from typing import BinaryIO
from urllib import request


class Cqserver:
    def __init__(self, ip: str, port: int, post_port: int):
        self.ip = ip
        self.port = port
        self.post_port = post_port
        self.reg_func: dict[int:list[Callable]] = {}
        self.ban_func: dict[int:list[Callable]] = {}
        self.newWebAndListenApp(ip,post_port)
        self.register()

    def printTitleVison(self):
        print(" * ---------------------------------")
        print(" * Multi functional dice rolling bot made with Python by Xyazh")
        print(" * 在浏览器打开 http://%s:%s/res/index.html 进行可视化后台管理" %(self.ip, self.post_port))
        print(" * アトリは、高性能ですから!")
        print(" * ---------------------------------")

    def newWebAndListenApp(self,ip: str, post_port: int):
        self.web_and_listen:App = App(ip,post_port)
        self.web_and_listen.http_server.cqserver = self
        real_root = "./web/public"
        virtual_root = "/res"
        def virtualPath(server: Server):
            path = server.virtual_path.replace(virtual_root, real_root, 1)
            server.sendFile(path)
        PageManager.addFileTree(real_root, virtual_root, virtualPath)
        PageManager.addPath("/", self.cqhttpApiConnector, "POST")
        MyWebApp()


    def register(self):
        from . import cqgroups
        from .cqgroups.BaseGroup import BaseGroup
        class_list = ServerHelper.getFullClassesFormModul(
            cqgroups, lambda clazz: issubclass(clazz, BaseGroup))
        for ClassGroup in class_list:
            group_obj: BaseGroup = ClassGroup()
            group_obj.setSender(self)
            func_list = []
            for fuc in inspect.getmembers(group_obj):
                if hasattr(fuc[1], "sign_reg"):
                    func_list.append(fuc[1])
            event: Event.GruopRegisterEvent = Event.EventBus.hookGruopRegisterEvent(
                group_obj.group_id, func_list, self)
            if event.getCancel():
                continue
            self.reg_func.update({event.group_id: event.fucs})

    def cqhttpApiConnector(self, server: Server):
        data: bytes = server.readPostData(max_size=10240)
        try:
            cqhttp_data: dict = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            server.send_error(400, "json decoder error")
            return
        self.mainMsgHandler(cqhttp_data)
        server.sendTextPage("ok")

    def mainMsgHandler(self,data:dict):
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
        self.web_and_listen.runHTTP(self.initFunc)

    def get(self, path:str) -> bytes:
        result = b""
        f:BinaryIO
        with request.urlopen("http://%s:%s%s"%(self.ip,self.port,path)) as f:
            result = f.read()
        return result


    def sendGroup(self, group_id:str|int, msg:str):
        fuc_group_msg_event: Event.FucGroupMsgEvent = Event.EventBus.hookFucGroupMsgEvent(
            {"raw_message": msg, "group_id": group_id}, "send", self)
        msg = fuc_group_msg_event.getMsg()
        group_id = fuc_group_msg_event.getGroupId()
        if not fuc_group_msg_event.getCancel():
            msg = self.escapeMsg(msg)
            self.get("/send_msg?message_type=group&group_id=%s&message=%s" %
                     (group_id, msg))

    def sendPrivate(self, id:str|int, msg:str):
        private_msg_event: Event.PrivateMsgEvent = Event.EventBus.hookPrivateMsgEvent(
            {"raw_message": msg, "user_id": id, "sub_type": "sender"}, "send", self)
        msg = private_msg_event.getMsg()
        if not private_msg_event.getCancel():
            msg = self.escapeMsg(msg)
            self.get(
                "/send_msg?message_type=private&user_id=%s&message=%s" % (id, msg))

    def escapeMsg(self, msg: str) -> str:
        msg = urllib.parse.quote(msg)
        return msg

    def setGroupLeave(self, group_id:str|int):
        self.get("/set_group_leave?group_id=%s" % (group_id))

    def sendImgToGroupFromPath(self, group_id:str|int, path:str):
        cq = "[CQ:image,file=%s,cache=0]" % ("file:///" + path)
        self.get("/send_msg?message_type=group&group_id=%s&message=%s" %
                 (group_id, cq))

    def sendImgToGroupFromUrl(self, group_id:str|int, url:str):
        cq = "[CQ:image,file=%s,cache=0]" % url
        self.get("/send_msg?message_type=group&group_id=%s&message=%s" %
                 (group_id, cq))

    def getGroupList(self):
        return self.get("/get_group_list")
    
    def getForwardMsg(self,msg_id:str|int)->bytes:
        return self.get("/get_forward_msg?message_id=%s"%msg_id)