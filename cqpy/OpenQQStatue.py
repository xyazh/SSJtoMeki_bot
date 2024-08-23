import time
import threading

from .xyazhRequest.HTTPSRequest import HTTPSRequest
from .xyazhRequest.RequestData import RequestData
from .xyazhServer.ConsoleMessage import ConsoleMessage


class OpenQQStatue:
    def __init__(self, app_id: str, client_Secret: str, max_try: int = 3, hostname: str = "bots.qq.com", path: str = "/app/getAppAccessToken"):
        self.app_id: str = app_id
        self.client_Secret: str = client_Secret
        self.max_try: int = max_try
        self.hostname: str = hostname
        self.path: str = path

        self.access_token: str = ""
        self.expires_in: int = -1
        self.re_req_time: int = -1

        self.is_stop: bool = False

        self.request_data = None
        self.runAccessToken()

    def createRequestData(self):
        request_data = RequestData("POST", self.path)
        request_data.addBodys({
            "Host": self.hostname,
            "Content-Type": "application/json",
            "Connection": "close",
        })
        request_data.setJsonData({
            "appId": self.app_id,
            "clientSecret": self.client_Secret
        })
        self.request_data = request_data


    def _getAccessToken(self):
        while True:
            if self.re_req_time == -1 or time.time() > self.re_req_time:
                self.re_req_time == -2
                if self.request_data is None:
                    self.createRequestData()
                for i in range(self.max_try):
                    request = HTTPSRequest(self.hostname)
                    response = request.execute(self.request_data)
                    data = None
                    if response.status_code == 200 and (data := response.json()) is not None and "access_token" in data and "expires_in" in data:
                        self.access_token = data["access_token"]
                        self.expires_in = float(data["expires_in"])
                        self.re_req_time = time.time() + self.expires_in - 60
                        break
                    elif i == self.max_try - 1:
                        ConsoleMessage.printError("获取access_token失败，程序将被冻结")
                        self.is_stop = True
                        return
                    ConsoleMessage.printWarning(
                        "获取access_token失败，重试次数%d" % (i + 1))
                    time.sleep(1)
            time.sleep(30)
        

    def runAccessToken(self):
        threading.Thread(target=self._getAccessToken).start()