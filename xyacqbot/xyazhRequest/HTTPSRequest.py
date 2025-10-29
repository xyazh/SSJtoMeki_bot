import socket
import ssl
import logging
from ..xyazhServer.ConsoleMessage import ConsoleMessage

if __name__ == '__main__':
    from RequestData import RequestData
    from ResponseData import ResponseData
else:
    from .RequestData import RequestData
    from .ResponseData import ResponseData

class HTTPSRequest:
    def __init__(self, hostname, port=443):
        self.hostname = hostname
        self.port = port
        self.context = ssl.create_default_context()
        self.sock = None
        self.ssl_sock = None

    def _createConnection(self):
        self.sock = socket.create_connection((self.hostname, self.port))
        self.ssl_sock = self.context.wrap_socket(self.sock, server_hostname=self.hostname)

    def sendRequest(self, request_data:bytes|RequestData):
        if self.ssl_sock is None:
            self._createConnection()
        self.ssl_sock.sendall(request_data)

    def receiveResponse(self):
        response = b''
        while True:
            data = self.ssl_sock.recv(4096)
            if not data:
                break
            response += data
        return response

    def close(self):
        if self.ssl_sock:
            self.ssl_sock.close()

    def execute(self, request_data:bytes|RequestData)->ResponseData|None:
        data = None
        try:
            self.sendRequest(request_data)
            data = ResponseData(self.receiveResponse())
        except Exception as e:
            ConsoleMessage.printError(e)
            logging.exception(e)
        finally:
            self.close()
        return data