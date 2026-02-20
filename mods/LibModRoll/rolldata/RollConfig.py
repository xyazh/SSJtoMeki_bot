from xyacqbot.datamanager.DataManager import DataManager

class RollConfig(DataManager):
    def __new__(cls, file_path="./data/roll_config.json"):
        return super().__new__(cls, file_path)

    def __init__(self, file_path="./data/roll_config.json"):
        super().__init__(file_path)

    def getRules(self) -> bool:
        return self.data.get("rule",True)
    
    def setRules(self, rule:bool) -> None:
        self.data["rule"] = rule