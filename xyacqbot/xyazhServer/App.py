import ssl
import threading

from .ihttp import server
from .Server import Server
from .PageManager import PageManager
from typing import Callable, Type


class PacketHTTPServer(server.ThreadingHTTPServer):
    def __init__(self, server_address, RequestHandlerClass: Type[Server], app: "App"):
        self.RequestHandlerClass: Type[Server]
        super().__init__(server_address, RequestHandlerClass)
        self.app: "App" = app

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, self.app)


class App:
    def __init__(self, host: str, port: int):
        self.page_manager = PageManager()
        self.host = host
        self.port = port
        self.http_server = PacketHTTPServer((self.host, port), Server, self)
        self.http_server.socket.settimeout(5)
        self.context = None
        self.ready = False

    def pTitleVison(self, t: str):
        print(f" * ---------------------------------")
        print(f" * xyazhServer {Server.server_version}")
        print(f" * Server is runing on {self.host}:{self.port}")
        print(f" * HTTP url is {t}://{self.host}:{self.port}/")
        print(f" * (Press CTRL+C to quit)")
        print(f" * ---------------------------------")

    def runThead(self, func: Callable = None, args: tuple = ()):
        if func == self.runHTTP:
            self.pTitleVison("http")
        elif func == self.runHTTPS:
            self.pTitleVison("https")
        else:
            raise Exception("Please use runHTTP or runHTTPS")
        thread = threading.Thread(target=func, args=args)
        thread.start()

    def runHTTP(self, func: Callable = None):
        if func is not None:
            func()
        self.ready = True
        self.http_server.serve_forever()

    def runHTTPS(self, cert_chain: tuple[str], func: Callable = None):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(*cert_chain)
        self.http_server.socket = self.context.wrap_socket(
            self.http_server.socket, server_side=True)
        if func is not None:
            func()
        self.ready = True
        self.http_server.serve_forever()
