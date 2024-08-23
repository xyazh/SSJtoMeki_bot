import time
import json
import websocket
from .OpenQQStatue import OpenQQStatue
from .xyazhServer.ConsoleMessage import ConsoleMessage
from .IType import emptyFuc
from .xyazhRequest import RequestData, HTTPSRequest


class OpenQQServer:
    @staticmethod
    def checkStop(fuc):
        def wrapper(self: OpenQQServer, *args, **kwargs):
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
        def wrapper(self: OpenQQServer, *args, **kwargs):
            if self.is_ws_closed:
                ConsoleMessage.printError("由于websocket连接已关闭，无法执行该操作")
                return
            return fuc(self, *args, **kwargs)
        return wrapper

    def __init__(self, app_id: str, client_Secret: str):
        self.status = OpenQQStatue(app_id, client_Secret)
        self.max_time = 30
        t = 0
        while self.status.access_token == "":
            time.sleep(1)
            t += 1
            if t > self.max_time:
                ConsoleMessage.printError("连接超时")
                raise Exception("Connection timeout")
        if self.status.is_stop:
            ConsoleMessage.printError("连接失败")
            raise Exception("Connection failed")

        self.url = self.getWebSocketUrl()
        if self.url == "":
            raise Exception("Get WebSocket address failed")

        self.ws = websocket.WebSocketApp(self.url,
                                         on_open=self.wsOnOpen,
                                         on_message=self.wsOnMessage,
                                         on_error=self.wsOnError,
                                         on_close=self.wsOnClose)
        self.is_ws_closed = False
        self.ws.run_forever()

    def wsWatch(self):
        while True:
            time.sleep(1)
            if self.is_ws_closed:
                break

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
    def sendWs(self, msg: str|bytes):
        self.ws.send(msg)

    @checkWsClose
    def sendWsBytes(self, msg: bytes):
        self.ws.send_bytes(msg)

    @checkWsClose
    def sendWsStr(self, msg: str):
        self.ws.send_text(msg)

    def sendWsJson(self, data: dict):
        self.sendWs(json.dumps(data))

    def wsOnMessage(self, ws, message):
        pass

    def wsOnError(self, ws, error):
        ConsoleMessage.printError(f"Error occurred: {error}")
        self.is_ws_closed = True

    def wsOnClose(self, ws, close_status_code, close_msg):
        ConsoleMessage.printMsg(
            f"Connection closed with status code: {close_status_code}")
        self.is_ws_closed = True

    def wsOnOpen(self, ws):
        ConsoleMessage.printMsg("Connection opened")
