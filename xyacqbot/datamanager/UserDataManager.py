from .DataManager import DataManager


class UserDataManager(DataManager):
    def __new__(cls, qq: str):
        file_path = f"./data/user/{qq}.json"
        return super().__new__(cls,file_path)

    def __init__(self, qq: str):
        self.qq = qq
        super().__init__(file_path=f"{qq}.json")

    def getLevel(self) -> int:
        return self.data.get("level", 0)

    def setLevel(self, level: int) -> None:
        self.data["level"] = level

    def getPoints(self) -> int:
        return self.data.get("points", 0)

    def setPoints(self, points: int) -> None:
        self.data["points"] = points

    def getData(self, key: str) -> dict:
        return self.data.get(key, {})

    def setData(self, key: str, value: dict) -> None:
        self.data[key] = value

    def getAttr(self, key: str, t=str):
        if t == str:
            return str(self.data.get(key, ""))
        elif t == int:
            return int(self.data.get(key, 0))
        elif t == float:
            return float(self.data.get(key, 0.0))
        elif t == bool:
            return bool(self.data.get(key, False))
        elif t == list:
            return list(self.data.get(key, []))
        elif t == dict:
            return dict(self.data.get(key, {}))
        else:
            return self.data.get(key, None)

    def setAttr(self, key: str, value):
        self.data[key] = value
