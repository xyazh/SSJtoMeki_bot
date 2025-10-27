from .Api import Api
from ..xyazhServer.PageManager import PageManager
from ..xyazhServer.Server import Server


class MyWebApp(Api):
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
        s.send_header("Location","http://" + host + "/res/index.html")
        s.end_headers()
