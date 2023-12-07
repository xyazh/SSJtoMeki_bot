from typing import Any
from .Config import Config
from ..xyazhServer.ConsoleMessage import ConsoleMessage
import os

class Lang:
    args = {}
    def __setattr__(self, key: str, val: Any) -> None:
        self.args[key] = val

    def __getattr__(self, key: str):
        if key not in self.args:
            self.args[key] = Texts()
        return self.args[key]
    
class Texts:
    def __setattr__(self, key: str, val: Any) -> None:
        if key == "args":
            return super().__setattr__(key, val)
        if not hasattr(self,"args"):
            self.args = {}
        self.args[key] = val

class DataLoader:
    data_loader = None
    def __new__(cls):
        if isinstance(cls.data_loader,cls):
            return cls.data_loader
        cls.data_loader = super().__new__(cls)
        cls.data_loader.is_loaded = False
        return cls.data_loader

    def __init__(self):
        if self.is_loaded:
            return
        self.makePath()
        self.loadLang()
        self.is_loaded = True

    def makePath(self):
        self.path = os.getcwd() + "\\cqpy_lang\\"
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def executeCode(self,code:str|bytes)->dict:
        variables = {"lang":Lang()}
        exec(code, {}, variables)
        lang = variables["lang"]
        result_dict = {}
        for i in lang.args:
            v = lang.args[i]
            if isinstance(v,Texts):
                v = list(v.args.values())
            result_dict[i] = v
        return result_dict

    def loadLang(self):
        self.lang_data = {}
        file_name = Config.LANG + "_lang.py"
        try:
            with open(self.path + file_name,"rb") as f:
                data = f.read()
        except FileNotFoundError:
            ConsoleMessage.printWarning("语言文件%s未找到"%file_name)
            return
        self.lang_data = self.executeCode(data)
    
