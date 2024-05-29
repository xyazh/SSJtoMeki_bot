from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...PlayerSystem.Player import Player
from .FoodItem import FoodItem

class Apple(FoodItem):
    def __init__(self):
        super().__init__()
        self.name = "苹果"
        self.tizhong = 0.05

apple1 = Apple()
apple1.tizhong = 10