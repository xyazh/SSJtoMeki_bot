import inspect
from ..Cqserver import Cqserver
from ..DataManager import DataManager

HELP_CLASS_DATA = {"normal":"常用命令","roll":"跑团命令","other":"其他命令","item":"RPG系统"}
BOT_NAME_SELF = "Meki"


class BaseGroup:
    HELP_CLASS_DATA = HELP_CLASS_DATA
    BOT_NAME_SELF = BOT_NAME_SELF

    @staticmethod
    def register(fuc):
        fuc.sign_reg = True
        return fuc

    @staticmethod
    def helpData(clazz: list[str], tx: str, ord: str, usg: str, datdetails: str):
        def r(fuc):
            fuc.help_data = [clazz, tx, ord, usg, datdetails]
            return fuc
        return r

    def __init__(self):
        self.group_id = -1
        self.unnsei_once_a_day = True
        self.data_manager = DataManager()
        self._getHelpsData()

    def setSender(self,s):
        self.s:Cqserver = s
    
    def _getHelpsData(self):
        self.helps_class: dict[str:list[str]] = {i:[] for i in HELP_CLASS_DATA}
        self.helps: dict[str:list[str]] = {}
        for fuc in inspect.getmembers(self):
            if hasattr(fuc[1], "help_data"):
                help_data: list = fuc[1].help_data
                ord_classes, tx, ord, usg, datdetails = tuple(help_data)
                li = [tx, ord, usg, datdetails]
                for i in ord_classes:
                    i = i if i in HELP_CLASS_DATA else "o"
                    if i in self.helps_class:
                        self.helps_class[i].append(li)
                    else:
                        self.helps_class.update({i: [li]})
                self.helps.update({ord: li})