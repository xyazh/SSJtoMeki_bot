class IPlatyerBase:
    def __init__(self):
        self.data: dict

    def writeGet(self, key, dis=None):
        """
        返回属性的值，如果没有数据则写入默认值后返回
        """
        r = dis
        if key in self.data:
            r = self.data[key]
        else:
            self.data[key] = dis
        return r

    def getBindedCardName(self) -> str:
        """
        获取绑定的角色卡的名字
        """
        r = self.writeGet("binded_chara", "空白卡")
        return r

    def get(self, key):
        """
        返回属性的值
        """
        return self.data[key]

    def findGet(self, key, dis=None):
        """
        返回属性的值，如果没有则返回默认值
        """
        return self.data.get(key, dis)

    def set(self, key, val):
        """
        返回属性的值
        """
        self.data[key] = val

    def getSet(self,key,s):
        """
        获取属性的值后写入属性
        """
        r = self.data[key]
        self.data[key] = s
        return r
    
    def findGetSet(self,key,s):
        """
        获取属性的值后写入属性，如果不存在属性则返回要设置的属性
        """
        r = self.findGet(key,s)
        self.data[key] = s
        return r