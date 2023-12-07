from ..BaseGroup import BaseGroup
from .IBaseGroup import IBaseGroup
from ...Order import Order
from ...GroupHelper import GroupHelper
from ...GameSystem.PlayerSystem.Player import Player
from ...GameSystem.Helper import RollHelper
from ...IType import *

class ITTKGroup(IBaseGroup):
    @BaseGroup.register
    @BaseGroup.helpData(["roll"], "创建角色", "new_card", "new_card [name]", "创建一张新卡")
    def ttk(self, data: dict, order: Order):
        pass