import json
import threading
import time
import random
from collections import deque
from ..xyazhServer.Server import Server
from .BaseWebApp import BaseWebApp
from typing import TYPE_CHECKING
from ..packet.PacketBase import PacketBase
from ..packet.PacketMsg import PacketMsg, ImageSegment
from ..datamanager.GlobleDataManager import GlobalDataManager
from ..msg.MsgBuilder import MsgBuilder
from ..xyazhServer.ConsoleMessage import ConsoleMessage
if TYPE_CHECKING:
    from ..xyazhServer.App import App
    from ..Cqserver import Cqserver


class WebApp(BaseWebApp):
    def __init__(self, app: "App", cq_server: "Cqserver"):
        super().__init__(app)
        self.cq_server = cq_server
        self._real_root = "./web/public"
        self._virtual_root = "/res"
        self.app.page_manager.addFileTree(
            self._real_root, self._virtual_root, self._virtualPath)
        cq_server.onEvent(self.onEvent)
        self.__init_other__()

    def __init_other__(self):
        self.msg_count = 0
        self.message_queue: deque[PacketMsg] = deque(maxlen=10000)

    def _virtualPath(self, server: Server):
        path = server.virtual_path.replace(
            self._virtual_root, self._real_root, 1)
        server.sendFile(path)

    def onEvent(self, p: PacketBase):
        if isinstance(p, PacketMsg):
            self.msg_count += 1
            self.message_queue.append(p)

    @BaseWebApp.page("/favicon.ico", "GET")
    def fav(self, s: Server):
        s.sendFile(".\\web\\images\\favicon.png")

    @BaseWebApp.page("/index", "GET")
    @BaseWebApp.page("/index.html", "GET")
    def reindex(self, s: Server):
        host = s.headers.get("Host")
        if host == None:
            s.send_error(404)
            return
        s.send_response(301, "Moved Permanently")
        s.send_header("Location", "http://" + host + "/res/index.html")
        s.end_headers()

    @BaseWebApp.page("/api/stats", "GET")
    def stats(self, s: Server):
        status = self.cq_server.getStatus()
        s.sendTextPage(json.dumps({
            "status": status["status"],
            "recode": status["recode"],
            "online": status["online"],
            "good": status["good"],
            "total": self.msg_count
        }), "application/json;charset=utf-8")

    @BaseWebApp.page("/api/messages", "GET")
    def messages(self, s: "Server"):
        keyword = s.urlVals(s.path).get("q", "")
        keywords = s.splitKeyword(keyword)
        msgs = []
        for msg in self.message_queue:
            real_msgs = msg.message
            urls = []
            for real_msg in real_msgs:
                if isinstance(real_msg, ImageSegment):
                    print(real_msg.getUrl())
                    urls.append(real_msg.getUrl())
            data = {
                "id": str(msg.getId()),
                "user": msg.getName(),
                "text": msg.getMsg(),
                "time": msg.time,
                "weight": 0,
                "urls": urls
            }
            if keyword == "":
                msgs.append(data)
                continue
            for kw in keywords:
                if kw in data["text"]:
                    data["weight"] += 1
                if kw in data["user"]:
                    data["weight"] += 2
                if kw in data["id"]:
                    data["weight"] += 2
            if data["weight"] > 0:
                msgs.append(data)
        msgs.sort(key=lambda x: x["weight"], reverse=True)
        s.sendTextPage(json.dumps(msgs), "application/json;charset=utf-8")

    @BaseWebApp.page("/api/groups", "GET")
    def groups(self, s: "Server"):
        groups = self.cq_server.getGroupList()
        if groups == None:
            s.send_error(500)
            return
        datas = []
        enble_groups = GlobalDataManager().getEnbaleGroupList()
        for group in groups:
            group_id = group.get("group_id")
            data = {
                "id": group_id,
                "name": group.get("group_name"),
                "count": group.get("member_count"),
                "enabled": str(group_id) in enble_groups
            }
            datas.append(data)
        s.sendTextPage(json.dumps(datas), "application/json;charset=utf-8")

    @BaseWebApp.page("/api/groups/leave", "POST")
    def leaveGroup(self, s: "Server"):
        data = s.readPostData(-1)
        try:
            data: dict = json.loads(data)
        except Exception as e:
            s.send_error(400, json.dumps({"success": False, "error": str(e)}))
            return
        group_ids = data.get("group_ids", [])
        for group_id in group_ids:
            self.cq_server.leaveGroup(group_id)
        s.sendTextPage(json.dumps({"success": True}),
                       "application/json;charset=utf-8")

    @BaseWebApp.page("/api/groups/data", "GET")
    def getGroupData(self, s: "Server"):
        group_id = s.urlVals(s.path).get("g")
        if group_id == None or group_id == "":
            s.send_error(400)
            return
        s.sendTextPage(json.dumps({"id": group_id, "enabled": group_id in GlobalDataManager().getEnbaleGroupList()}),
                       "application/json;charset=utf-8")

    @BaseWebApp.page("/api/groups/update", "POST")
    def updateGroup(self, s: "Server"):
        data = s.readPostData(-1)
        try:
            data: dict = json.loads(data)
        except Exception as e:
            s.send_error(400, json.dumps({"success": False, "error": str(e)}))
            return
        global_data_manager = GlobalDataManager()
        if data.get("enabled", False):
            global_data_manager.appendEnbaleGroup(data.get("id"))
        else:
            global_data_manager.removeEnbaleGroup(data.get("id"))
        s.sendTextPage(json.dumps({"success": True}),
                       "application/json;charset=utf-8")

    @BaseWebApp.page("/api/send", "POST")
    def sendGroup(self, s: "Server"):
        data = s.readPostData(-1)
        try:
            data: dict = json.loads(data)
        except Exception as e:
            s.send_error(400, json.dumps({"success": False, "error": str(e)}))
            return
        group_id = data.get("target")
        msg = data.get("message")
        file_base64 = data.get("file")
        file_type = data.get("file_type")
        send_mode = data.get("send_mode")
        if group_id == None:
            s.send_error(400)
            return
        if msg == None and file_base64 == None:
            s.send_error(400)
            return
        msg_builder = MsgBuilder()
        msg_builder.updateText(msg)
        if file_base64 != None:
            if send_mode == "image_sticker":
                msg_builder.updateImage(file_base64)
            elif send_mode == "audio_voice":
                msg_builder.updateRecord(file_base64)
            elif send_mode == "video_video":
                msg_builder.updateVideo(file_base64)
            else:
                s.sendTextPage(json.dumps({"success": False, "error": "暂不支持发送文件"}),
                               "application/json;charset=utf-8")
                return
        if group_id == "all":
            def _broadcastTask(self: WebApp, msg_builder):
                """后台线程执行群发任务"""
                enable_groups = GlobalDataManager().getEnbaleGroupList()
                total = len(enable_groups)
                ConsoleMessage.printC(f"[Broadcast] 开始群发，共 {total} 个群")
                for i, gid in enumerate(enable_groups, start=1):
                    try:
                        self.cq_server.sendGroupMsg(msg_builder, gid)
                        ConsoleMessage.printC(
                            f"[Broadcast] ({i}/{total}) 已发送到群 {gid}")
                    except Exception as e:
                        print(f"[Broadcast] 发送到群 {gid} 失败: {e}")
                    if i < total:
                        delay = random.uniform(1.0, 2.0)
                        time.sleep(delay)
            threading.Thread(target=_broadcastTask,
                             args=(self, msg_builder)).start()
        else:
            self.cq_server.sendGroupMsg(msg_builder, group_id)
        s.sendTextPage(json.dumps({"success": True, "error": ""}),
                       "application/json;charset=utf-8")

    @BaseWebApp.page("/api/rules/save", "POST")
    def rulesSave(self, s: "Server"):
        data = s.readPostData(-1)
        try:
            data: dict = json.loads(data)
        except Exception as e:
            s.send_error(400, json.dumps({"success": False, "error": str(e)}))
            return
        trigger = data.get("trigger")
        reply = data.get("reply")
        mode = data.get("mode", "exact")
        enabled = data.get("enabled", False)
        if trigger == None or trigger == "":
            s.sendTextPage(json.dumps(
                {"success": False, "error": "触发词不能为空"}),
                "application/json;charset=utf-8", 400)
            return
        if reply == None or reply == "":
            s.sendTextPage(json.dumps(
                {"success": False, "error": "回复不能为空"}),
                "application/json;charset=utf-8", 400)
            return
        global_data_manager = GlobalDataManager()
        global_data_manager.appendAutoReplyRules(trigger, reply, mode, enabled)
        s.sendTextPage(json.dumps({"success": True, "error": ""}),
                       "application/json;charset=utf-8")

    @BaseWebApp.page("/api/rules", "GET")
    def rulesGet(self, s: "Server"):
        global_data_manager = GlobalDataManager()
        rules = global_data_manager.getAutoReplyRules()
        rules = [{"trigger": k, "reply": v["reply"], "mode": v["mode"], "enabled": v["enabled"]} for k, v in rules.items()]
        s.sendTextPage(json.dumps(rules), "application/json;charset=utf-8")

    @BaseWebApp.page("/api/rules/delete", "POST")
    def rulesDelete(self, s: "Server"):
        data = s.readPostData(-1)
        try:
            data: dict = json.loads(data)
        except Exception as e:
            s.send_error(400, json.dumps({"success": False, "error": str(e)}))
            return
        triggers = data.get("triggers",[])
        GlobalDataManager().removeAutoReplyRules(triggers)
        s.sendTextPage(json.dumps({"success": True, "error": ""}),
                       "application/json;charset=utf-8")
