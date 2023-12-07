from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...PlayerSystem.Player import Player

class BaseItem:
    name = "base item"
    desc = "item"
    akt = 0
    size = 1

    def __init__(self):
        self.name = "base item"
        self.desc = "item"
        self.atk = 0
        self.size = 1

    def onUse(self,onwer:"Player",target:"Player"=None,*args,**kw):
        pass