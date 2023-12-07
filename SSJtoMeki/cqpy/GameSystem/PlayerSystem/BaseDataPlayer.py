import weakref
from ..DataManager import DataManager
from ..ToolClass.RollDict import RollDict

class BaseDataPlayer:
    data_manager = DataManager()
    instances = {}

    def __hash__(self) -> int:
        return hash(self.qq_id)

    def __new__(cls,qq_id:int):
        if qq_id in BaseDataPlayer.instances:
            r:BaseDataPlayer = BaseDataPlayer.instances[qq_id]()
            if r != None and r.deteled == False:
                return r
        self = super().__new__(cls)
        BaseDataPlayer.instances[qq_id] = weakref.ref(self)
        self.inited = False
        return self

    def __init__(self,qq_id:int):
        if not self.inited:
            self.qq_id:int = qq_id
            self.deteled:bool = False
            self.data:dict = {}
            self.load()
        self.inited = True

    def __del__(self):
        if self.deteled:
            return
        self.save()
        self.deteled = True

    def __delete__(self,instance):
        if self.deteled:
            return
        self.save()
        self.deteled = True

    def load(self):
        self.data = BaseDataPlayer.data_manager.get(str(self.qq_id)+".json")
        if "chara_cards" in self.data:
            for i in self.data["chara_cards"]:
                self.data["chara_cards"][i] = RollDict(self.data["chara_cards"][i])

    def save(self):
        BaseDataPlayer.data_manager.setMenbers(str(self.qq_id)+".json",self.data)