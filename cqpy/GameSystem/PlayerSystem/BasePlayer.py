from ..I import IRoll
from ..I import IItemSystem
from ..ToolClass.BaseData import BaseData
from ..Helper import DictHelper


class BasePlayer(BaseData, IRoll, IItemSystem):
    def __init__(self, qq_id: int):
        super().__init__(qq_id)

    def getName(self)->str:
        """
        获取绑定的角色卡的名字
        """
        return self.getBindedCardName()

    def getHp(self)->int:
        """
        获取绑定的角色卡的hp
        """
        card = self.getBindedCardNotNone()
        hp = DictHelper.wirteGet(card,"hp",1)
        return hp
    
    def getMaxHp(self)->int:
        """
        获取绑定的角色卡最大hp
        """
        card = self.getBindedCardNotNone()
        con = DictHelper.wirteGet(card,"con",10)
        siz = DictHelper.wirteGet(card,"siz",10)
        mhp = max(int((con+siz)/10),1)
        return mhp

    def setHp(self,hp:int|float):
        """
        传入要设置的hp，设置绑定的角色卡的hp
        """
        hp = int(hp)
        card = self.getBindedCardNotNone()
        card["hp"] = hp

    def countHp(self,count_hp:int|float)->int:
        """
        传入要扣去的hp，扣去绑定的角色卡的hp，并返回真实扣去的hp
        """
        count_hp = 0 if count_hp<=0 else int(count_hp)
        hp = self.getHp()
        real_count_hp = min(count_hp,hp)
        hp -= real_count_hp
        self.setHp(hp)
        return real_count_hp
    
    def healHp(self,heal_hp:int|float)->int:
        """
        传入要回复的hp，回复绑定的角色卡的hp，并返回真实回复的hp
        """
        heal_hp = 0 if heal_hp<=0 else int(heal_hp)
        hp = self.getHp()
        mhp = self.getMaxHp()
        print(mhp)
        dhp = mhp - hp
        real_heal_hp = min(dhp,heal_hp)
        hp += real_heal_hp
        self.setHp(hp)
        return real_heal_hp

    def getMp(self)->int:
        card = self.getBindedCardNotNone()
        mp = DictHelper.wirteGet(card,"mp",1)
        return mp
    
    def getMaxMp(self)->int:
        card = self.getBindedCardNotNone()
        pow = DictHelper.wirteGet(card,"pow",10)
        mmp = max(int(pow/5),0)
        return mmp

    def setMp(self,mp:int|float):
        mp = int(mp)
        card = self.getBindedCardNotNone()
        card["mp"] = mp

    def countMp(self,count_mp:int|float)->int:
        count_mp = 0 if count_mp<=0 else int(count_mp)
        mp = self.getMp()
        real_count_mp = min(count_mp,mp)
        mp -= real_count_mp
        self.setMp(mp)
        return real_count_mp
    
    def healMp(self,heal_mp:int|float)->int:
        heal_mp = 0 if heal_mp<=0 else int(heal_mp)
        mp = self.getMp()
        mmp = self.getMaxMp()
        dmp = mmp - mp
        real_heal_mp = min(dmp,heal_mp)
        mp += real_heal_mp
        self.set(mp)
        return real_heal_mp