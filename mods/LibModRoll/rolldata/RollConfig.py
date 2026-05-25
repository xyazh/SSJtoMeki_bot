from xyacqbot.datamanager.DataManager import DataManager

class RollConfig(DataManager):
    def __new__(cls, file_path="./data/roll_config.json"):
        return super().__new__(cls, file_path)

    def __init__(self, file_path="./data/roll_config.json"):
        super().__init__(file_path)

    def getRules(self, session_id: int) -> bool:
        return self.data.get(str(session_id), {}).get("rule", True)

    def setRules(self, session_id: int, rule: bool) -> None:
        if str(session_id) not in self.data:
            self.data[str(session_id)] = {}
        self.data[str(session_id)]["rule"] = rule