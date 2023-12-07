from ...GroupHelper import GroupHelper
from .IBaseGroup import IBaseGroup
from ..BaseGroup import BaseGroup
from ...Order import Order
from ...GameSystem.PlayerSystem.Player import Player
from ...GameSystem.ItemSystem.Items.FoodItem import FoodItem

class ISSJGroup(IBaseGroup):
    @BaseGroup.register
    def weiShi(self,data,order:Order):
        if not order.checkOrder("weishi"):
            return
        food_name = order.getArg(1)
        if not food_name:
            self.s.sendGroup(self.group_id,"无食物名")
            return
        SSJ_player = Player(3556009251)
        SSJ_player.writeGet("体重",84)
        qq_id = GroupHelper.getId(data)
        player = Player(qq_id)
        n = player.countItemFromGodownToIter(food_name,1)
        if len(n) <= 0:
            self.s.sendGroup(self.group_id,"无数量")
            return
        for item in n:
            if not isinstance(item,FoodItem):
                self.s.sendGroup(self.group_id,"不是食物")
                return
            item:FoodItem
            item.onEat(SSJ_player)