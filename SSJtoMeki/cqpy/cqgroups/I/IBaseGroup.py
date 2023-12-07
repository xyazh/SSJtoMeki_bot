from ...DataManager import DataManager
from ...Cqserver import Cqserver

class IBaseGroup:
    def __init__(self):
        self.group_id:int
        self.data_manager:DataManager
        self.s: Cqserver
        self.unnsei_once_a_day:bool