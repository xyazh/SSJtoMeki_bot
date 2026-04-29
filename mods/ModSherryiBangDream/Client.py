from typing import Any
from typing_extensions import override
from urllib.parse import urlparse
from xyacqbot.xyazhRequest import HTTPRequest, HTTPSRequest, RequestData
from tsugu_api import *
from tsugu_api_core import register_client
from tsugu_api_core.client import Client as _Client
from tsugu_api_core.client import Request, Response

class Client(_Client):
    @classmethod
    def register(cls):
        register_client(cls)

    @override
    def __enter__(self) -> 'Client':
        return self
    
    @override
    async def __aenter__(self) -> 'Client':
        raise RuntimeError(
            'REQUESTS client is not asynchronous, please use sync context manager')

    @override
    def __exit__(self, *args: Any) -> None:
        pass

    @override
    async def __aexit__(self, *args: Any) -> None:
        pass

    @override
    def request(self, request: Request) -> Response:
        parsed_url = urlparse(request.url)
        host = parsed_url.hostname
        port = parsed_url.port
        path = parsed_url.path
        if "https" in request.url:
            if port is None:
                port = 443
            h_request = HTTPSRequest(host, port)
        else:
            if port is None:
                port = 80
            h_request = HTTPRequest(host, port)
        h_request_data = RequestData(request.method.upper(), path)
        h_request_data.addBodys(request.headers)
        h_request_data.addBody("Host", f"{host}:{port}")
        h_request_data.addBody("Connection", f"close")
        h_request_data.setJsonData(request.data)
        h_response = h_request.execute(h_request_data)
        return Response(
            h_response.un_chunks_body,
            h_response.status_code
        )

    @override
    async def arequest(self, request: Request) -> Response:
        raise RuntimeError(
            'REQUESTS client is not asynchronous, please use sync request method.')