from .DataManager import DataManager


class GlobalDataManager(DataManager):
    def __new__(cls, file_path="./data/global_data.json"):
        return super().__new__(cls, file_path)

    def __init__(self, file_path="./data/global_data.json"):
        super().__init__(file_path)

    def getEnbaleGroupList(self) -> list[str]:
        return self.data.get("enable_group_list", [])

    def setEnbaleGroupList(self, li: list[str]) -> None:
        self.data["enable_group_list"] = li

    def appendEnbaleGroup(self, group_id: str) -> None:
        groups = set(self.data.get("enable_group_list", []))
        group_id = str(group_id)
        groups.add(group_id)
        self.data["enable_group_list"] = list(groups)

    def removeEnbaleGroup(self, group_id: str) -> None:
        groups = set(self.data.get("enable_group_list", []))
        group_id = str(group_id)
        if group_id not in groups:
            return
        groups.remove(group_id)
        self.data["enable_group_list"] = list(groups)

    def appendAutoReplyRules(self, trigger: str, reply: str, mode: str = 'exact', enabled: bool = False) -> None:
        rules: dict[dict] = self.data.get("auto_reply_rules", {})
        rules[trigger] = {
            "trigger": trigger,
            "reply": reply,
            "mode": mode,
            "enabled": enabled
        }
        self.data["auto_reply_rules"] = rules

    def getAutoReplyRules(self) -> dict[str, dict]:
        return self.data.get("auto_reply_rules", {})

    def removeAutoReplyRules(self, trigger: str | list) -> None:
        rules: dict[dict] = self.data.get("auto_reply_rules", {})
        if isinstance(trigger, str):
            if trigger in rules:
                del rules[trigger]
        elif isinstance(trigger, list):
            for t in trigger:
                if t in rules:
                    del rules[t]
        self.data["auto_reply_rules"] = rules

    def getWebappToken(self)->str|None:
        return self.data.get("webapp_token")
    
    def setWebappToken(self, token:str)->None:
        self.data["webapp_token"] = token
