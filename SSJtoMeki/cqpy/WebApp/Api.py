from ..cqevent.DisEvent import DisEvent
from ..GameSystem.PlayerSystem.Player import Player
from .login_and_register import LoggingData
from .login_and_register import RegisterData
from .msg import MsgData
from .C import C
from ..xyazhServer.ConsoleMessage import ConsoleMessage
from ..xyazhServer.HtmlStr import HtmlStr
from ..xyazhServer.PageManager import PageManager
from ..xyazhServer.Server import Server
from ..xyazhServer.BestXor import BestXor
import time
import json
import re
import html
import os
import uuid

class Api:
    @PageManager.register("/api/send_mail_code", "POST")
    def mailCheckCodeApi(s: Server):
        user_ip = s.address_string()
        t = time.time()
        if user_ip in C.IP_CHECK_MAIL_TIMER:
            if t - C.IP_CHECK_MAIL_TIMER[user_ip] > 55:
                C.IP_CHECK_MAIL_TIMER[user_ip] = t
            else:
                s.send_error(403, "resetting time")
                return
        else:
            C.IP_CHECK_MAIL_TIMER[user_ip] = t
        r_data: bytes = s.readPostDataTimeout()
        try:
            user_mail = str(r_data, encoding="utf8")
        except UnicodeDecodeError:
            s.send_error(400, "Not mail")
            return
        if not re.match(r"^\w+([\.\-]\w+)*\@\w+([\.\-]\w+)*\.\w+$", user_mail):
            s.send_error(400, "Not mail")
            return
        check_code = s.randomIntStr(6)
        tmp = C.user_data_manager.get("user_list.json", user_mail)
        if tmp != None:
            s.send_error(409, "hased mail")
            return
        C.temp_mail_data_manager.setMenbers(
            user_mail+".json", {"check_code": check_code, "time": t})
        ConsoleMessage.printDebug("生成验证码：%s" % check_code)
        try:
            C.mail_helper.sendMail(
                user_mail, "你的验证码是：%s, 请勿泄露给他人（十分钟有效）" % check_code)
        except C.mail_helper.ERROR as e:
            s.send_response(500, "Send mail error")
            s.end_headers()
            ConsoleMessage.printError(str(e))
        s.send_response(204, "No Content")
        s.end_headers()

    @PageManager.register("/api/register", "POST")
    def registerApi(s: Server):
        r_data: bytes = s.readPostDataTimeout()
        try:
            user_data: dict = json.loads(r_data)
        except json.decoder.JSONDecodeError as e:
            s.send_error(400, "json decoder error")
            return
        register_data = RegisterData(user_data)
        if not register_data.check():
            s.send_error(400, "incomplete data")
            return
        m = C.temp_mail_data_manager.getMenbers(
            register_data.user_mail+".json", ("check_code", "time"), lambda x: 0)
        t = time.time()
        if len(register_data.user_name) > 20:
            s.send_error(413, "username too long")
            return
        if t - m["time"] > 600:
            s.send_error(403, "code timeout")
            return
        if register_data.check_code != m["check_code"]:
            s.send_error(401, "code error")
            return
        tmp = C.user_data_manager.get(
            "user_mail_list.json", register_data.user_mail)
        if tmp != None:
            s.send_error(409, "hased mail")
            return
        C.user_data_manager.set(
            "user_mail_list.json", register_data.user_mail, 1)
        tmp = C.user_data_manager.get(
            "user_name_list.json", register_data.user_name)
        if tmp != None:
            s.send_error(409, "hased username")
            return
        C.user_data_manager.set(
            "user_name_list.json", register_data.user_name, 1)
        sl = s.randomIntStr(16)
        token = s.safeHash(sl, register_data.password)
        uid = str(uuid.uuid4())
        C.user_data_manager.set(
            "user_token.json", register_data.user_mail, token)
        C.user_data_manager.setMenbers(token+".json", {
            "user_name": register_data.user_name,
            "password": register_data.password,
            "token": token,
            "sl": sl,
            "email": register_data.user_mail,
            "uid": uid,
            "level": 0,
            "qq_id": -1
        })
        s.setCookie("token", token, path="/")
        s.setCookie("level", 0, path="/")
        s.setCookie("uid", uid, path="/")
        s.setCookie("user_name",  register_data.user_name, path="/")
        s.setCookie("qq_id", -1, path="/")
        s.sendTextPage(json.dumps({"token": token, "level": 0, "uid": uid,
                       "user_name": register_data.user_name, "qq_id": -1}, ensure_ascii=False).encode("utf8"))

    @PageManager.register("/api/logging", "POST")
    def loggingApi(s: Server):
        r_data: bytes = s.readPostDataTimeout()
        try:
            user_data: dict = json.loads(r_data)
        except json.decoder.JSONDecodeError as e:
            s.send_error(400, "json decoder error")
            return
        logging_data = LoggingData(user_data)
        if not logging_data.check():
            s.send_error(400, "incomplete data")
            return
        token = C.user_data_manager.get(
            "user_token.json", logging_data.user_mail)
        if token == None:
            s.send_error(404, "not found user")
            return
        l_data = C.user_data_manager.getMenbers(
            token+".json", ["level", "uid", "user_name", "password", "qq_id"])
        if l_data["password"] != logging_data.password:
            s.send_error(401, "password error")
            return
        s.setCookie("token", token, path="/")
        s.setCookie("level", l_data["level"], path="/")
        s.setCookie("uid", l_data["uid"], path="/")
        s.setCookie("user_name", l_data["user_name"], path="/")
        s.setCookie("qq_id", l_data["qq_id"], path="/")
        s.sendTextPage(json.dumps(
            {"token": token, "level": l_data["level"], "uid": l_data["uid"], "user_name": l_data["user_name"], "qq_id": l_data["qq_id"]}, ensure_ascii=False).encode("utf8"))

    @PageManager.register("/api/msg_send", "POST")
    def msgSendApi(s: Server):
        user_ip = s.address_string()
        t = time.time()
        if user_ip in C.IP_CHECK_MAIL_TIMER:
            if t - C.IP_CHECK_MAIL_TIMER[user_ip] > 5:
                C.IP_CHECK_MAIL_TIMER[user_ip] = t
            else:
                s.send_error(403, "resetting time")
                return
        else:
            C.IP_CHECK_MAIL_TIMER[user_ip] = t
        C.IP_CHECK_MAIL_TIMER
        r_data: bytes = s.readPostDataTimeout()
        try:
            msg_data: dict = json.loads(r_data)
        except json.decoder.JSONDecodeError as e:
            s.send_error(400, "json decoder error")
            return
        msg = MsgData(msg_data)
        if not msg.check():
            s.send_error(400, "incomplete data")
            return
        user_name = msg.name
        if msg.token:
            user_name = C.user_data_manager.get(
                msg.token+".json", "user_name")
            if not user_name:
                s.send_error(404, "not found user")
                return
        else:
            if 9 > time.localtime().tm_hour > 0:
                s.send_error(403, "curfew")
                return
        mid = C.msg_data_manager.findGet("max_id.json", "max_id", 0) + 1
        C.msg_data_manager.set("max_id.json", "max_id", mid)
        r_msg = {"msg_id": mid, "title": msg.title,
                 "user_name": user_name, "msg": msg.text, "token": msg.token}
        C.msg_data_manager.set("msgs.json", str(mid), r_msg)
        s.sendTextPage(json.dumps(r_msg, ensure_ascii=False).encode("utf8"))

    @PageManager.register("/api/msg_get", "GET")
    def msgGetApi(s: Server):
        m: dict = C.msg_data_manager.get("msgs.json")
        msgs = list(m.values())
        s.sendTextPage(json.dumps(msgs, ensure_ascii=False).encode("utf8"))

    @PageManager.register("/api/group_manager", "POST")
    def groupGetApi(s: Server):
        r_data: bytes = s.readPostDataTimeout()
        try:
            rev_data: dict = json.loads(r_data)
        except json.decoder.JSONDecodeError as e:
            s.send_error(400, "json decoder error")
            return
        if False and not "token" in rev_data:
            s.send_error(401, "Unauthorized")
            return
        if not "type" in rev_data:
            s.send_error(400, "incomplete data")
            return
        rev_type = rev_data["type"]
        match rev_type:
            case "fuc_off":
                if not ("group" in rev_data and "fuc_name" in rev_data):
                    s.send_error(404, "not fount gruop")
                    return
                group = rev_data["group"]
                fuc_name = rev_data["fuc_name"]
                if not group in s.cqserver.register_list:
                    s.send_error(404, "not fount fuc")
                    return
                fuc_list: list = s.cqserver.register_list[group]
                for i in range(len(fuc_list)):
                    if fuc_list[i].__name__ == fuc_name:
                        fuc = fuc_list.pop(i)
                        if group in s.cqserver.dis_register_list:
                            s.cqserver.dis_register_list[group].append(fuc)
                        else:
                            s.cqserver.dis_register_list[group] = [fuc]
                        dis_register_fuc = DisEvent.data_manager.findGet(
                            "dis_register_fuc.json", str(group), [])
                        dis_register_fuc.append(fuc_name)
                        DisEvent.data_manager.set(
                            "dis_register_fuc.json", str(group), dis_register_fuc)
                        break
            case "fuc_on":
                if not ("group" in rev_data and "fuc_name" in rev_data):
                    s.send_error(404, "not fount gruop")
                    return
                group = rev_data["group"]
                fuc_name = rev_data["fuc_name"]
                if not group in s.cqserver.dis_register_list:
                    s.send_error(404, "not fount fuc")
                    return
                fuc_list: list = s.cqserver.dis_register_list[group]
                for i in range(len(fuc_list)):
                    if fuc_list[i].__name__ == fuc_name:
                        fuc = fuc_list.pop(i)
                        if group in s.cqserver.register_list:
                            s.cqserver.register_list[group].append(fuc)
                        else:
                            s.cqserver.register_list[group] = [fuc]
                        dis_register_fuc = DisEvent.data_manager.findGet(
                            "dis_register_fuc.json", str(group), [])
                        if fuc_name in dis_register_fuc:
                            dis_register_fuc.remove(fuc_name)
                        DisEvent.data_manager.set(
                            "dis_register_fuc.json", str(group), dis_register_fuc)
                        break
        r = []
        for group_id in s.cqserver.register_list:
            fucs = s.cqserver.register_list[group_id]
            for fuc in fucs:
                fuc_data = ""
                if hasattr(fuc, "help_data"):
                    fuc_data = fuc.help_data[1]
                r.append({"group": group_id,
                          "fuc_name": HtmlStr(fuc.__name__).escapeHtml(),
                          "fuc_data": HtmlStr(html.escape(fuc_data)).escapeHtml(),
                          "fuc_on": HtmlStr("on").setColor("green")
                          })
        for group_id in s.cqserver.dis_register_list:
            fucs = s.cqserver.dis_register_list[group_id]
            for fuc in fucs:
                fuc_data = ""
                if hasattr(fuc, "help_data"):
                    fuc_data = fuc.help_data[1]
                r.append({"group": group_id,
                          "fuc_name": HtmlStr(fuc.__name__).escapeHtml(),
                          "fuc_data": HtmlStr(html.escape(fuc_data)).escapeHtml(),
                          "fuc_on": HtmlStr("off").setColor("red")
                          })
        r.sort(key=lambda x: x["group"])
        s.sendTextPage(json.dumps(r, ensure_ascii=False).encode("utf8"))

    @PageManager.register("/api/data_manager", "POST")
    def dataManagerApi(s: Server):
        r_data: bytes = s.readPostDataTimeout()
        r = []
        for dirpath, dirnames, filenames in os.walk("./cqpy_data"):
            for filename in filenames:
                path = dirpath+"/"+filename
                r.append({"file_name": filename, "file_path": path})
        s.sendTextPage(json.dumps(r))

    @PageManager.register("/api/data_manager/file", "POST")
    def dataManagerFile(s: Server):
        r_data: bytes = s.readPostDataTimeout()
        data = json.loads(r_data)
        file_name = data["file_name"]
        s.sendFile("./cqpy_data/"+file_name)

    @PageManager.register("/api/get_check_qq_code", "POST")
    def bindQQCode(s: Server):
        token = s.getCookieToDict().get("token", "")
        f = "%s.json" % token
        if not C.user_data_manager.hasFile(f):
            s.send_error(401, "Not found token")
            return
        dtok = s.readPostDataTimeout().decode("utf8")
        uid = C.user_data_manager.get(f,"uid").encode("utf8")
        qq_id = BestXor.bestDecryptXor(uid,dtok)
        C.user_data_manager.set(f,"qq_id",qq_id.decode("utf8"))
        s.sendTextPage(qq_id)

    @PageManager.register("/api/get_roll_menber","GET")
    def getRollMenber(s: Server):
        token = s.getCookieToDict().get("token", "")
        f = "%s.json" % token
        if not C.user_data_manager.hasFile(f):
            s.send_error(401, "Not found token")
            return
        qq_id = C.user_data_manager.get(f,"qq_id")
        if not qq_id or int(qq_id) < 0:
            s.send_error(404, "Not qq")
            return
        kp_qq = Player(qq_id)
        pls = kp_qq.get("pls")
        rd = {}
        for i in pls:
            pl_player = Player(i)
            i += "-" + pl_player.getBindedCardName()
            items = pl_player.getBindedCharaItems()
            attr = pl_player.getBindedCardNotNone()
            rd[i] = []
            for k in items:
                rd[i].append({"name":k,'val':items[k],"type":"物品"})
            for j in attr:
                rd[i].append({"name":j,'val':attr[j],"type":"属性"})
        s.sendTextPage(json.dumps(rd,ensure_ascii=False))

    @PageManager.register("/api/set_roll_menber","POST")
    def setRollMenber(s: Server):
        token = s.getCookieToDict().get("token", "")
        f = "%s.json" % token
        if not C.user_data_manager.hasFile(f):
            s.send_error(401, "Not found token")
            return
        r_data: bytes = s.readPostDataTimeout()
        try:
            rev_data: dict = json.loads(r_data)
        except json.decoder.JSONDecodeError as e:
            s.send_error(400, "json decoder error")
            return
        for qq_id in rev_data:
            pl_player = Player(int(qq_id))
            arr_data = rev_data[qq_id]
            if arr_data["type"] == "物品":
                print(arr_data["name"],arr_data["val"])
                pl_player.setItemNumberTotBindedChara(arr_data["name"],arr_data["val"])
            elif arr_data["type"] == "属性":
                pl_player.setBindedCardArr({arr_data["name"]:arr_data["val"]})
        s.send_error(200, "OK")