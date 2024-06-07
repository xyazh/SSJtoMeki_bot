class MsgData(dict):
    def getNickname(self) -> str:
        if "sender" in self:
            if "nickname" in self["sender"]:
                return self["sender"]["nickname"]
        return ""

    def getCardname(self) -> str:
        if "sender" in self:
            if "card" in self["sender"]:
                return self["sender"]["card"]
        return ""

    def getName(self) -> str:
        name = self.getCardname()
        if name == "":
            name = self.getNickname()
        return name

    def checkOwner(self) -> bool:
        if "sender" in self:
            return self["sender"]["role"] == "owner"
        return False

    def checkAdmin(self) -> bool:
        if "sender" in self:
            return self["sender"]["role"] == "admin"
        return False

    def checkOwnerOrAdmin(self) -> bool:
        return self.checkAdmin() or self.checkOwner()

    def getId(self) -> int:
        if "sender" in self:
            if "user_id" in self["sender"]:
                return self["sender"]["user_id"]
        return -1

    def getMsg(self) -> str:
        if 'raw_message' in self:
            return self['raw_message']
        return ""