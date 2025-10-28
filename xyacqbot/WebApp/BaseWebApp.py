from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from ..xyazhServer.App import App

    class _MCallable(Callable):
        _pagefuc: tuple[str, str]


class BaseWebApp:
    @staticmethod
    def page(path: str, t: str = "GET"):
        def fuc(f: "_MCallable") -> Callable:
            f._pagefuc = (path, t)
            return f
        return fuc

    def __init__(self, app: "App"):
        self.app: "App" = app
        for name in dir(self):
            m: "_MCallable" = getattr(self, name)
            if callable(m) and hasattr(m, "_pagefuc"):
                path, t = m._pagefuc
                app.page_manager.addPath(path, m, t)
