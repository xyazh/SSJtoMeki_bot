from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...PlayerSystem.Player import Player
import random
from .BaseItem import BaseItem

class FoodItem(BaseItem):
    def __init__(self):
        self.name = "food_item"
        self.desc = "普通的食物"
        self.atk = 0
        self.size = 1
        self.tizhong = 0.01

    def onEat(self,onwer:"Player"):
        tizhong = onwer.findGet("体重",random.randint(45,75))
        tizhong += self.tizhong
        onwer.set("体重",tizhong)