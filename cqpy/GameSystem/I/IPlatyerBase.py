class IPlatyerBase:
    def __init__(self):
        self.data: dict

    def writeGet(self, key, dis=None):
        """
        传入需要获取的属性的名字返回对应的值
        
        若该属性不存在则在玩家数据中写入默认值并返回默认值
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
        传入需要获取的属性的名字返回对应的值

        若该属性不存在则抛出错误
        """
        return self.data[key]

    def findGet(self, key, dis=None):
        """
        传入需要获取的属性的名字返回对应的值
        
        若该属性不存在则返回默认值（不更改玩家数据）
        """
        return self.data.get(key, dis)

    def set(self, key, val):
        """
        传入属性的名字与需要修改的值来更改玩家对应属性的值
        """
        self.data[key] = val

    def getSet(self,key,s):
        """
        传入一个属性的名字以及一个值，用于获取该属性当前的值后设置为一个新的值

        若该属性不存在则抛出错误
        """
        r = self.data[key]
        self.data[key] = s
        return r
    
    def findGetSet(self,key,s):
        """
        传入一个属性的名字以及一个值，用于获取该属性当前的值后设置为一个新的值

        若属性不存在则添加这个属性并返回要设置的新的值
        """
        r = self.findGet(key,s)
        self.data[key] = s
        return r