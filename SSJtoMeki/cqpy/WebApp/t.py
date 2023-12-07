from .C import C
from .Api import Api
from ..xyazhServer.App import App
from ..xyazhServer.PageManager import PageManager
from ..xyazhServer.Server import Server
from ..xyazhServer.UrlHelper import UrlHelper


class MyWebApp(Api):
    def __init__(self):
        pass

    if __name__ == "__main__":
        def __init__(self):
            if C.H == "http":
                self.app = App("127.0.0.1", 80)
            elif C.H == "https":
                self.app = App("127.0.0.1", 443)

        def run(self):
            if C.H == "http":
                self.app.runHTTP()
            elif C.H == "https":
                self.app.runHTTPS(
                    ('cert/server.crt', 'cert/server_rsa_private.pem.unsecure'))

    def load(self):
        root = "./web/public"
        v_root = "/res"

        def vPath(s: Server):
            path = s.v_path.replace(v_root, root, 1)
            s.sendFile(path)
        PageManager.addFileTree(root, v_root, vPath)

    @PageManager.register("/res/*", "GET")
    def prPage(s: Server):
        token = s.getCookieToDict().get("token", "")
        if not C.user_data_manager.get("%s.json" % token):
            s.send_error(401, "Not found token")
            return
        fn = UrlHelper.pathSplit(s.v_path)[-2]
        s.sendFile("./web/" + fn)

    @PageManager.register("/", "GET")
    def dis(s: Server):
        s.sendFileBreakpoint(
            ".\\xya_data\\192d9a98d782d9c74c96f09db9378d93.mp4")

    @PageManager.register("/favicon.ico", "GET")
    def fav(s: Server):
        s.sendFileBreakpoint(".\\web\\images\\favicon.png")

    @PageManager.register("/index", "GET")
    @PageManager.register("/index.html", "GET")
    def reindex(s: Server):
        host = s.headers.get("Host")
        if host == None:
            s.send_error(404)
            return
        s.send_response(301, "Moved Permanently")
        s.send_header("Location", C.H +
                      "://" + host + "/res/index.html")
        s.end_headers()


if __name__ == "__main__":
    my_web_app = C()
    my_web_app.load()
    my_web_app.run()
