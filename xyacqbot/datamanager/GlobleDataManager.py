from .DataManager import DataManager


class GlobalDataManager(DataManager):
    def __init__(self):
        super().__init__(file_path="global_data.json")

    def getEnbaleGroupList(self) -> list[str]:
        return self.data.get("enable_group_list",[])

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