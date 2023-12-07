from .Order import Order

ORDER_SPLIT_LIST = [".", "/", "。", "\\"]


class GroupHelper:
    @staticmethod
    def getNickname(data: dict) -> str:
        if "sender" in data:
            if "nickname" in data["sender"]:
                return data["sender"]["nickname"]
        return ""

    @staticmethod
    def getCardname(data: dict) -> str:
        if "sender" in data:
            if "card" in data["sender"]:
                return data["sender"]["card"]
        return ""

    @staticmethod
    def getName(data: dict) -> str:
        name = GroupHelper.getCardname(data)
        if name == "":
            name = GroupHelper.getNickname(data)
        return name

    @staticmethod
    def checkOwner(data) -> bool:
        if "sender" in data:
            return data["sender"]["role"] == "owner"
        return False

    @staticmethod
    def checkAdmin(data) -> bool:
        if "sender" in data:
            return data["sender"]["role"] == "admin"
        return False

    @staticmethod
    def checkOwnerOrAdmin(data) -> bool:
        return GroupHelper.checkAdmin(data) or GroupHelper.checkOwner(data)

    @staticmethod
    def getId(data: dict) -> int:
        if "sender" in data:
            if "user_id" in data["sender"]:
                return data["sender"]["user_id"]
        return -1

    @staticmethod
    def getMsg(data: dict) -> str:
        if type(data) == dict:
            if 'raw_message' in data:
                return data['raw_message']
        return ""

    @staticmethod
    def orderSplit(s: str) -> list[str]:
        r = []
        if len(s) < 2:
            return r
        if s[0] in ORDER_SPLIT_LIST and s[1] != " ":
            for i in s.split(" "):
                if i != "" and i != " ":
                    r.append(i)
        return r

    @staticmethod
    def getOrderFromData(data: dict) -> Order:
        return Order(GroupHelper.orderSplit(GroupHelper.getMsg(data)))

    @staticmethod
    def getOrderFromStr(msg: str) -> Order:
        return Order(GroupHelper.orderSplit(msg))
