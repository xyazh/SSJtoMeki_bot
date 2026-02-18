from typing import Callable, TYPE_CHECKING
from ..xyazhServer.PageManager import Token
from ..datamanager.GlobleDataManager import GlobalDataManager
if TYPE_CHECKING:
    from ..xyazhServer.App import App

    class _MCallable(Callable):
        _pagefuc: tuple[str, str]


class BaseWebApp:
    @staticmethod
    def page(path: str, t: str = "GET", token: bool = True):
        def fuc(f: "_MCallable") -> Callable:
            f._pagefuc = (path, t, token)
            return f
        return fuc

    def __init__(self, app: "App"):
        self.app: "App" = app
        global_data = GlobalDataManager()
        token_val = global_data.getWebappToken()
        if token_val is None:
            token_val = input("请输入webapp的token用于web后台管理:")
            global_data.setWebappToken(token_val)
        self.token = Token(token_val, "/login")

        for name in dir(self):
            m: "_MCallable" = getattr(self, name)
            if callable(m) and hasattr(m, "_pagefuc"):
                path, t,has_token = m._pagefuc
                if has_token:
                    app.page_manager.addPath(path, m, t, token=self.token)
                else:
                    app.page_manager.addPath(path, m, t)
