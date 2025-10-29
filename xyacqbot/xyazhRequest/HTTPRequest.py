import socket
import logging
from ..xyazhServer.ConsoleMessage import ConsoleMessage

if __name__ == '__main__':
    from RequestData import RequestData
    from ResponseData import ResponseData
else:
    from .RequestData import RequestData
    from .ResponseData import ResponseData

class HTTPRequest:
    def __init__(self, hostname, port=80):
        self.hostname = hostname
        self.port = port
        self.sock = None

    def _createConnection(self):
        self.sock = socket.create_connection((self.hostname, self.port))

    def sendRequest(self, request_data:bytes|RequestData):
        if self.sock is None:
            self._createConnection()
        self.sock.sendall(request_data)

    def receiveResponse(self):
        response = b''
        while True:
            data = self.sock.recv(4096)
            if not data:
                break
            response += data
        return response

    def close(self):
        if self.sock:
            self.sock.close()

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