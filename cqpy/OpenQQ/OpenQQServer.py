import time
import json
from types import UnionType
import logging
import threading
import os
import subprocess
import sys
from .OpenQQStatue import OpenQQStatue
from .Payload import Payload
from ..xyazhServer.ConsoleMessage import ConsoleMessage
from ..IType import emptyFuc
from ..xyazhRequest import RequestData, HTTPSRequest
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..Cqserver import Cqserver

try:
    import websocket
except ImportError:
    ConsoleMessage.printWarning("websocket 模块未安装，正在安装...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websocket-client"])
    import websocket


class OpenQQServer:
    @staticmethod
    def checkStop(fuc):
        def wrapper(self: "OpenQQServer", *args, **kwargs):
            if self.status.is_stop:
                ConsoleMessage.printError("由于程序已经冻结，无法执行该操作")
                return
            if self.status.access_token == "":
                ConsoleMessage.printWarning("等待获取令牌或连接建立，此操作已跳过")
                return
            return fuc(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def checkWsClose(fuc):
        def wrapper(self: "OpenQQServer", *args, **kwargs):
            if self.is_ws_closed:
                ConsoleMessage.printError("由于websocket连接已关闭，无法执行该操作")
                return
            return fuc(self, *args, **kwargs)
        return wrapper

    def __init__(self,cqserver:"Cqserver",app_id: str, client_secret: str):
        self.max_time = 30
        self.cqserver = cqserver
        self.app_id = app_id
        self.client_Secret = client_secret

    def run(self):
        t = 0
        ConsoleMessage.printC("正在启动...")
        ConsoleMessage.printC("正在获取令牌...")
        ConsoleMessage.printC(f"App id: {self.app_id}")
        ConsoleMessage.printC(f"Client Secret: {self.client_Secret}")
        self.status = OpenQQStatue(self.app_id, self.client_Secret)
        while self.status.access_token == "":
            time.sleep(1)
            t += 1
            if t > self.max_time:
                ConsoleMessage.printError("连接超时")
                raise Exception("Connection timeout")
        if self.status.is_stop:
            ConsoleMessage.printError("连接失败")
            raise Exception("Connection failed")
        ConsoleMessage.printC("正在获取WebSocket地址...")
        self.url = self.getWebSocketUrl()
        if self.url == "":
            raise Exception("Get WebSocket address failed")
        ConsoleMessage.printC(f"WebSocket地址: {self.url}")
        ConsoleMessage.printC("正在启动websocket...")
        self.doWsWatch()
        self.createWs()

    def createWs(self):
        while True:
            self.ws = websocket.WebSocketApp(self.url,
                                             on_open=self.wsOnOpen,
                                             on_message=self.wsOnMessage,
                                             on_error=self.wsOnError,
                                             on_close=self.wsOnClose)
            self.is_ws_closed = True
            self.heartbeat_time = -1
            self.new_s = None
            self.heartbeat_timer = 0
            flag = self.ws.run_forever(reconnect=5)
            if not flag:
                break

    def doWsWatch(self):
        threading.Thread(target=self.wsWatch).start()

    def wsWatch(self):
        while True:
            time.sleep(1)
            if self.is_ws_closed == True:
                continue
            if self.heartbeat_time != -1:
                self.heartbeat_timer += 1
                if self.heartbeat_timer > self.heartbeat_time:
                    self.heartbeat_timer = 0
                    self.sendHeartbeat()

    def sendHeartbeat(self):
        payload = Payload()
        payload.op = 1
        payload.d = self.new_s
        ConsoleMessage.printDebug(f"发送心跳包: {payload.getDict()}")
        self.sendWsJson(payload.getDict())

    @checkStop
    def getWebSocketUrl(self) -> str:
        request_data = RequestData("GET", "/gateway")
        request_data.addBodys({
            "Host": "api.sgroup.qq.com",
            "Connection": "close",
            "Authorization": "QQBot %s" % self.status.access_token
        })
        https = HTTPSRequest("api.sgroup.qq.com")
        data = https.execute(request_data)
        if data.status_code != 200:
            ConsoleMessage.printError("获取WebSocket地址失败")
            print(data)
            return ""
        return data.json()["url"]

    @checkWsClose
    def sendWs(self, msg: str | bytes):
        self.ws.send(msg)

    @checkWsClose
    def sendWsBytes(self, msg: bytes):
        self.ws.send_bytes(msg)

    @checkWsClose
    def sendWsStr(self, msg: str):
        self.ws.send_text(msg)

    def sendWsJson(self, data: dict):
        self.sendWs(json.dumps(data))

    def onOpCode10Hello(self, ws: websocket.WebSocketApp, payload: Payload):
        if isinstance(payload.d, dict):
            self.heartbeat_time = payload.d["heartbeat_interval"] / 1000
        else:
            self.heartbeat_time = 45
        self.sendWsJson({
            "op": 2,
            "d": {
                "token": "QQBot %s" % self.status.access_token,
                "intents":  0 | 513 | (1 << 25) | (1 << 0) | (1 << 1),
                "shard": [0, 1],
                "properties": {
                    "$os": os.name,
                    "$browser": "",
                    "$device": "xyazhServer"
                }
            }
        })

    def onOpCode0Ready(self, ws: websocket.WebSocketApp, payload: Payload):
        #print(payload)
        if payload.t == "GROUP_AT_MESSAGE_CREATE":
            pass


    def onOpCode1Heartbeat(self, ws: websocket.WebSocketApp, payload: Payload):
        self.sendWsJson({
            "op": 11
        })

    def onOpCode7Reconnect(self, ws: websocket.WebSocketApp, payload: Payload):
        pass

    def onOpCode9InvalidSession(self, ws: websocket.WebSocketApp, payload: Payload):
        ConsoleMessage.printWarning(f"Invalid session: {payload}")


    def onOpCode11HeartbeatACK(self, ws: websocket.WebSocketApp, payload: Payload):
        ConsoleMessage.printDebug(f"收到心跳ACK回包: {payload}")

    def onPayload(self, ws: websocket.WebSocketApp, payload: Payload):
        if payload.op == 0:
            self.onOpCode0Ready(ws, payload)
        elif payload.op == 1:
            self.onOpCode1Heartbeat(ws, payload)
        elif payload.op == 7:
            self.onOpCode7Reconnect(ws, payload)
        elif payload.op == 9:
            self.onOpCode9InvalidSession(ws, payload)
        elif payload.op == 11:
            self.onOpCode11HeartbeatACK(ws, payload)
        elif payload.op == 10:
            self.onOpCode10Hello(ws, payload)

    def wsOnMessage(self, ws, message):
        try:
            payload = Payload(message)
            if payload.s != None:
                self.new_s = payload.s
            self.onPayload(ws, payload)
        except Exception as e:
            ConsoleMessage.printError(f"WebSocket解析服务器消息失败: {message}")
            logging.exception(e)

    def wsOnError(self, ws, error):
        ConsoleMessage.printError(f"WebSocket error occurred: {error}")
        self.is_ws_closed = True

    def wsOnClose(self, ws, close_status_code, close_msg):
        ConsoleMessage.printC(
            f"WebSocket connection closed with status code: {close_status_code}")
        ConsoleMessage.printC(
            f"WebSocket connection closed with message: {close_msg}")
        self.is_ws_closed = True

    def wsOnOpen(self, ws):
        ConsoleMessage.printC("WebSocket connection opened")
        self.is_ws_closed = False
