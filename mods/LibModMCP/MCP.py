import logging
import functools
from mcp.server.fastmcp import FastMCP
from xyacqbot.xyazhServer.ConsoleMessage import ConsoleMessage


class MCP(FastMCP):
    instance = None
    inited = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, *args, host: str = "127.0.0.1", port: int = 37101, **kwargs):
        if self.inited:
            return
        super().__init__(*args, **kwargs)
        self.settings.host = host
        self.settings.port = port
        self.initLogging()
        self.inited = True

    def initLogging(self):
        for logger in logging.Logger.manager.loggerDict.values():
            if not isinstance(logger, logging.Logger):
                continue
            if logger.name[:2] != "mcp":
                continue
            logger.info = lambda msg, * \
                args, **kw: ConsoleMessage.print(msg % args, titles=["MCP"])
            logger.warning = lambda msg, * \
                args, **kw: ConsoleMessage.printWarning(msg % args, titles=["MCP"])
            logger.error = lambda msg, * \
                args, **kw: ConsoleMessage.printError(msg % args, titles=["MCP"])
            logger.warn = lambda msg, * \
                args, **kw: ConsoleMessage.printWarning(msg % args, titles=["MCP"])
        for name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
            logger = logging.getLogger(name)
            logger.info = lambda msg, * \
                args, **kw: ConsoleMessage.print(msg % args, titles=["MCP"])
            logger.warning = lambda msg, * \
                args, **kw: ConsoleMessage.printWarning(msg % args, titles=["MCP"])
            logger.error = lambda msg, * \
                args, **kw: ConsoleMessage.printError(msg % args, titles=["MCP"])
            logger.warn = lambda msg, * \
                args, **kw: ConsoleMessage.printWarning(msg % args, titles=["MCP"])
        logging.getLogger("uvicorn.access").disabled = True

    def run(self, *args, **kwargs):
        ConsoleMessage.print("启动MCP服务", titles=["MCP"])
        tool_names = map(lambda tool: tool.name,
                         self._tool_manager.list_tools())
        ConsoleMessage.print("工具已加载:", list(tool_names), titles=["MCP"])
        super().run(*args, **kwargs)

    
    def add_tool(self, fn, *args, **kwargs):
        @functools.wraps(fn)
        def wrapper(*call_args, **call_kwargs):
            ConsoleMessage.print("MCP工具调用", fn.__name__,
                                call_args, call_kwargs, titles=["MCP"])
            result = fn(*call_args, **call_kwargs)
            ConsoleMessage.print("MCP工具返回", fn.__name__,
                                result, titles=["MCP"])
            return result
        return super().add_tool(wrapper, *args, **kwargs)




