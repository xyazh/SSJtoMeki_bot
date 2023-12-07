import socket
import json
import time
import random
import inspect
from .DataManager import DataManager
from .Event import Event
from .GroupHelper import GroupHelper
from . import cqgroups
from .cqgroups import BaseGroup
from .xyazhServer import Server
from .xyazhServer import PageManager
from .xyazhServer import App
from .xyazhServer import ConsoleMessage
from .WebApp import t


class Cqserver(t.MyWebApp):
    @staticmethod
    def getFullClassesFormModul(o: object, filter=None, found_modules=None) -> list:
        r = []
        if found_modules == None:
            found_modules = set()
        if not hasattr(o, "__dict__"):
            return r
        for i in o.__dict__:
            if inspect.isclass(o.__dict__[i]):
                if inspect.isfunction(filter):
                    if not filter(o.__dict__[i]):
                        continue
                r.append(o.__dict__[i])
            elif inspect.ismodule(o.__dict__[i]):
                if o.__dict__[i] in found_modules:
                    continue
                found_modules.add(o.__dict__[i])
                r += Cqserver.getFullClassesFormModul(
                    o.__dict__[i], filter=filter, found_modules=found_modules)
        return r

    @staticmethod
    def checkFunsArgs(fuc: object, args: list | tuple) -> bool:
        i = inspect.signature(fuc)
        try:
            i.bind(*args)
        except TypeError:
            return False
        return True

    def __init__(self, ip_str: str, port_int: int, post_port_int: int):
        super().__init__()
        self.register_list: dict[int:list[object]] = {}
        self.dis_register_list: dict[int:list[object]] = {}
        self.ip = ip_str
        self.port = port_int
        self.post_port = post_port_int
        self.msg_data_manager = DataManager("//cqpy_msg_data//")
        self.register()

    def saveGroupMsg(self, data: dict):
        msg_id: int = data["message_id"]
        group_id: int = data["group_id"]
        msg: str = data["raw_message"]
        self.msg_data_manager.set("G%d.json" % group_id, str(msg_id), msg)

    def mainMsgProcess(self, data):
        if not "message_type" in data:
            return
        message_type = data["message_type"]
        if message_type == "group":
            if not "group_id" in data:
                return
            if not 'raw_message' in data:
                return
            self.saveGroupMsg(data)
            fuc_group_msg_event: Event.FucGroupMsgEvent = Event.EventBus.hookFucGroupMsgEvent(
                data, "recv", self)
            if fuc_group_msg_event.getCancel():
                return
            group_id = fuc_group_msg_event.getGroupId()
            data['raw_message'] = fuc_group_msg_event.getMsg()
            if group_id in self.register_list:
                order = GroupHelper.getOrderFromData(data)
                for i in self.register_list[data["group_id"]]:
                    if Cqserver.checkFunsArgs(i, (data, order)):
                        i(data, order)
                    else:
                        i(data)
        if data["message_type"] == "private":
            Event.EventBus.hookPrivateMsgEvent(data, "recv", self)

    def register(self):
        class_list = Cqserver.getFullClassesFormModul(
            cqgroups, lambda clazz: issubclass(clazz, BaseGroup.BaseGroup))
        for ClassGroup in class_list:
            class_group_obj: BaseGroup.BaseGroup = ClassGroup()
            class_group_obj.setSender(self)
            fuc_list = []
            for fuc in inspect.getmembers(class_group_obj):
                if hasattr(fuc[1], "sign_reg"):
                    fuc_list.append(fuc[1])
            gruop_register_event: Event.GruopRegisterEvent = Event.EventBus.hookGruopRegisterEvent(
                class_group_obj.group_id, fuc_list, self)
            if gruop_register_event.getCancel():
                continue
            self.register_list.update(
                {gruop_register_event.group_id: gruop_register_event.fucs})

    def connetCqHttpApi(self, s: Server):
        r_data: bytes = s.readPostData(max_size=10240)
        try:
            s_data: dict = json.loads(r_data)
        except json.decoder.JSONDecodeError as e:
            s.send_error(400, "json decoder error")
            return
        self.mainMsgProcess(s_data)
        # 并不是错误，因为这里没必要返回什么具体的数据
        s.send_error(200)

    def serverRun(self):
        ConsoleMessage.DEBUG_LEVEL = 2
        self.load()
        self.app = App(self.ip, self.post_port)
        self.app.httpd.cqserver = self
        PageManager.addPath("/", self.connetCqHttpApi, "POST")
        self.pTitleVison()
        self.app.runHTTP()

    def pTitleVison(self):
        print(" * ---------------------------------")
        print(" * Multi functional dice rolling bot made with Python by Xyazh")
        print(" * 在浏览器打开 http://%s:%s/res/index.html 进行可视化后台管理" %
              (self.ip, self.post_port))
        print(" * アトリは、高性能ですから!")
        print(" * ---------------------------------")

    def get(self, path) -> bytes:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        s.send(b"GET %b HTTP/1.1\r\n" % (bytes(path, "utf8")))
        s.send(b"Host: %b\r\n" % (bytes(self.ip, "utf8")))
        s.send(b"Connection: close\r\n")
        s.send(b"\r\n")
        data_list = []
        while True:
            data_recv = s.recv(1)
            data_list.append(data_recv)
            if (len(data_list) >= 4 and b"\r" == data_list[-4] and b"\n" == data_list[-3] and b"\r" == data_list[-2] and b"\n" == data_list[-1]) or len(data_recv) == 0:
                break
        s.close()
        return b"".join(data_list)

    def sendGroup(self, group_id, msg):
        time.sleep(0.7 + random.random()/2)
        fuc_group_msg_event: Event.FucGroupMsgEvent = Event.EventBus.hookFucGroupMsgEvent(
            {"raw_message": msg, "group_id": group_id}, "send", self)
        msg = fuc_group_msg_event.getMsg()
        group_id = fuc_group_msg_event.getGroupId()
        if not fuc_group_msg_event.getCancel():
            msg = self.escapeMsg(msg)
            self.get("/send_msg?message_type=group&group_id=%s&message=%s" %
                     (group_id, msg))

    def sendPrivate(self, id, msg):
        private_msg_event: Event.PrivateMsgEvent = Event.EventBus.hookPrivateMsgEvent(
            {"raw_message": msg, "user_id": id, "sub_type": "sender"}, "send", self)
        msg = private_msg_event.getMsg()
        if not private_msg_event.getCancel():
            msg = self.escapeMsg(msg)
            self.get(
                "/send_msg?message_type=private&user_id=%s&message=%s" % (id, msg))

    def escapeMsg(self, msg: str) -> str:
        msg = (msg
               .replace("%", "%25")
               .replace(" ", "%20")
               .replace("\r", "%0d")
               .replace("\n", "%0a")
               .replace("/", "%2f")
               .replace("?", "%3f")
               .replace("#", "%23")
               .replace("&amp;", "%26")
               .replace("&", "&amp;")
               .replace("&amp;", "%26")
               .replace("<", "%3c")
               .replace("=", "%3d")
               .replace(">", "%3e")
               .replace("+", "%2b")
               .replace("|", "%7c")
               .replace("(", "%28")
               .replace(")", "%29")
               .replace("]", "%5d")
               .replace("[", "%5b")
               .replace(":", "%3a")
               .replace(";", "%3b"))
        return msg

    def setGroupLeave(self, group_id):
        self.get("/set_group_leave?group_id=%s" % (group_id))

    def sendImgToGroupFromPath(self, group_id, path):
        cq = "[CQ:image,file=%s,cache=0]" % ("file:///" + path)
        self.get("/send_msg?message_type=group&group_id=%s&message=%s" %
                 (group_id, cq))

    def sendImgToGroupFromUrl(self, group_id, url):
        cq = "[CQ:image,file=%s,cache=0]" % url
        self.get("/send_msg?message_type=group&group_id=%s&message=%s" %
                 (group_id, cq))

    def getGroupList(self):
        self.get("/get_group_list")
