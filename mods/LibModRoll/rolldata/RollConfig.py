from xyacqbot.datamanager.DataManager import DataManager

class RollConfig(DataManager):
    # 全局默认规则的存储键，供没有会话上下文的调用方（如 MCP 工具）使用
    DEFAULT_KEY = "default"

    def __new__(cls, file_path="./data/roll_config.json"):
        return super().__new__(cls, file_path)

    def __init__(self, file_path="./data/roll_config.json"):
        super().__init__(file_path)

    @classmethod
    def _sessionKey(cls, session_id: int | str | None) -> str:
        """将会话id转换为存储键，None表示全局默认规则"""
        if session_id is None:
            return cls.DEFAULT_KEY
        return str(session_id)

    def getRules(self, session_id: int | str | None = None) -> bool:
        """获取检定规则，session_id为None时取全局默认规则"""
        return self.data.get(self._sessionKey(session_id), {}).get("rule", True)

    def setRules(self, session_id: int | str | None = None, rule: bool = True) -> None:
        """设置检定规则，session_id为None时设置全局默认规则"""
        key = self._sessionKey(session_id)
        if key not in self.data:
            self.data[key] = {}
        self.data[key]["rule"] = rule