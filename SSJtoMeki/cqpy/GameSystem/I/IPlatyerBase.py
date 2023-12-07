class IPlatyerBase:
    def __init__(self):
        self.data: dict

    def writeGet(self, key, dis=None):
        r = dis
        if key in self.data:
            r = self.data[key]
        else:
            self.data[key] = dis
        return r

    def getBindedCardName(self) -> str:
        r = self.writeGet("binded_chara", "空白卡")
        return r

    def get(self, key):
        return self.data[key]

    def findGet(self, key, dis=None):
        return self.data.get(key, dis)

    def set(self, key, val):
        self.data[key] = val
