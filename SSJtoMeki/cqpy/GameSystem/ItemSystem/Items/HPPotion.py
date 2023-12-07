from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...PlayerSystem.Player import Player
from .BaseItem import BaseItem

class HPPotion(BaseItem):
    def __init__(self):
        super().__init__()
        self.name = "HP药水"
        self.desc = "恢复5点生命值"
        self.atk = 0

    def onUse(self,onwer:"Player",target:"Player|None"=None,*args,**kw):
        if target != None:
            target.healHp(5)
            return super().onUse(onwer, target, *args, **kw)
        onwer.healHp(5)
        return super().onUse(onwer, target, *args, **kw)