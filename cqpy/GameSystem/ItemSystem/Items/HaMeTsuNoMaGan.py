from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...PlayerSystem.Player import Player
import random
from .BaseItem import BaseItem

class HaMeTsuNoMaGan(BaseItem):
    def __init__(self):
        self.name = ""
        self.desc = ""
        self.atk = 0
        self.size = 1
        self.tizhong = 0.01