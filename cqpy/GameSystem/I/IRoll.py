from ..Helper import RollHelper
from ..Helper import DictHelper
from ..ToolClass.RollDict import RollDict
from .IPlatyerBase import IPlatyerBase

DIS_DATA = {"hp": 1, "san": 10, "mp": 1, "str": 10, "dex": 10, "con": 10,
            "siz": 10, "app": 10, "int": 10, "pow": 10, "edu": 10, "luk": 10}


class IRoll(IPlatyerBase):
    def getCards(self) -> dict[str, dict]:
        """
        获取此用户的所有角色卡为字典
        """
        return self.writeGet("chara_cards", {"空白卡": RollDict(DIS_DATA.copy())})

    def getCard(self, name) -> dict[str:int | float | complex | str | bool | None] | None:
        """
        传入角色卡的名字来获取此用户的某角色卡，返回一个字典

        若该角色卡不存在，则返回None
        """
        chara_cards = self.getCards()
        r = chara_cards.get(name, None)
        return r

    def getBindedCard(self) -> dict[str:int | float | complex | str | bool | None] | None:
        """
        获取此用户当前正在绑定的角色卡，返回一个字典

        角色卡不存在，则返回None
        """
        binded_card_name = self.getBindedCardName()
        binded_card = self.getCard(binded_card_name)
        return binded_card

    def getBindedCardNotNone(self) -> dict[str:int | float | complex | str | bool | None]:
        """
        传入角色卡的名字来获取此用户的某角色卡，返回一个字典

        没有则返回空白卡
        """
        r = self.getBindedCard()
        if r != None:
            return r
        self.data["binded_chara"] = "空白卡"
        chara_cards = self.getCards()
        if not self.data["binded_chara"] in chara_cards:
            chara_cards[self.data["binded_chara"]] = RollDict(DIS_DATA.copy())
        return chara_cards[self.data["binded_chara"]]

    def setCardArr(self, card_name: str, d: dict):
        """
        传入角色卡的名字与包含角色卡各属性的字典，重新设置角色卡的数据

        注意会清除已有数据
        """
        chara_cards = self.getCards()
        chara_cards[card_name] = RollDict(DIS_DATA.copy())
        for i in d:
            chara_cards[card_name][i] = d[i]

    def addCardArr(self, card_name: str, d: dict):
        """
        传入角色卡的名字，以及需要修改/添加的数据组成的字典，添加角色卡的数据

        重复的数据会被覆盖
        """
        chara_cards = self.getCards()
        chara_card = DictHelper.wirteGet(chara_cards,card_name,RollDict(DIS_DATA.copy()))
        for i in d:
            chara_card[i] = d[i]

    def setBindedCardArr(self, d: dict):
        """
        传入需要修改/添加的数据组成的字典，修改/添加绑定的角色卡的数据

        重复的数据会被覆盖
        """
        binded_card_name = self.getBindedCardName()
        self.addCardArr(binded_card_name, d)

    def creatCard(self, card_name: str, d: dict):
        """
        传入角色卡的名字与数据，创建新角色卡
        """
        self.setCardArr(card_name, d)

    def bindCard(self, card_name: str) -> bool:
        """
        传入角色卡的名称，绑定的角色卡
        
        绑定成功返回True，若角色卡不存在返回False
        """
        chara_cards = self.getCards()
        if card_name in chara_cards:
            self.data["binded_chara"] = card_name
            return True
        return False

    def creatBindedCardAsStr(self, s: str):
        """
        从录卡字符串重新设置绑定的卡

        注意会清除已有数据
        """
        card_name = self.getBindedCardName()
        d = RollHelper.decodeArrStr(s)
        self.setCardArr(card_name, d)

    def addBindedCardAsStr(self, s:str):
        """
        从录卡字符串添加绑定的角色卡的数据

        重复的数据会被覆盖
        """
        card_name = self.getBindedCardName()
        d = RollHelper.decodeArrStr(s)
        self.addCardArr(card_name, d)

    def creatCardAsStr(self, card_name: str, s: str):
        """
        从录卡字符串重新设置属性

        注意会清除已有数据
        """
        d = RollHelper.decodeArrStr(s)
        self.setCardArr(card_name, d)

    def delCard(self, card_name: str) -> bool:
        """
        传入角色卡的名字，删除卡角色卡
        """
        chara_cards = self.getCards()
        if card_name in chara_cards:
            chara_cards.pop(card_name)
            return True
        return False

    def getCardsList(self) -> list[str]:
        """
        获取角色卡列表
        """
        chara_cards = self.getCards()
        return list(chara_cards.keys())

    def getCardVal(self, card_name: str, key: str) -> str | int | float | complex | None:
        """
        传入角色卡名称和要获取的属性，获取该角色卡的这个属性的值

        如果角色卡和属性不存在则返回None
        """
        card = self.getCard(card_name)
        if card == None:
            return None
        return card.get(key, None)

    def getBindedCardVal(self, key: str) -> str | int | float | complex | None:
        """
        传入属性的名字，获取当前绑定的角色卡的这个属性的值

        如果属性不存在则返回None
        """
        binded_card = self.getBindedCardName()
        return self.getCardVal(binded_card, key)
    
    def isKp(self)->bool:
        """
        判断此用户是否是kp
        """
        return self.data.get("is_kp",False)
    
    def setKp(self,b:bool):
        """
        传入True设置此用户为kp，传入False设置此用户不为kp
        """
        self.data["is_kp"] = b