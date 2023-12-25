from ..BaseGroup import BaseGroup
from .IBaseGroup import IBaseGroup
from ...Order import Order
from ...GroupHelper import GroupHelper
from ...GameSystem.PlayerSystem.Player import Player
from ...GameSystem.Helper import RollHelper
from ...GameSystem.ItemSystem.Items.BaseItem import BaseItem
from ...IType import *
from ...CQCode import CQCodeHelper
from ...I18n.I18n import I18n

class IItemGroup(IBaseGroup):
    @BaseGroup.register
    @BaseGroup.helpData(["item"], "使用物品", "use", "use [item_name] [number] (targets)...", "使用物品，或对target使用物品，target是被@的人。此指令会对每一个target都使用number个item（如果数量足够的话）")
    def use(self, data: dict, order: Order):
        if not order.checkOrder("use"):
            return
        item_name = order.getArg(1)
        number = order.getArg(2)
        if item_name == None or number == None:
            self.server.sendGroup(self.group_id,I18n.format("has_help"))
            return
        if not number.isdigit():
            self.server.sendGroup(self.group_id,"噫~不会数数的杂鱼大哥哥~kimo")
            return
        number = int(number)
        if number <= 0:
            self.server.sendGroup(self.group_id,"%s是在表示你那为%s的杂鱼智商吗~？"%(number,number))
            return
        msg = GroupHelper.getMsg(data)
        qq_id = GroupHelper.getId(data)
        cq_codes = CQCodeHelper.creatCQCodeFromMsg(msg)
        at_ids = set()
        for i in cq_codes:
            if i.t == "at":
                at_ids.add(i.data["qq"])
        at_ids = list(at_ids)
        n = len(at_ids)
        n = number if n <= 0 else n*number
        player_onwer = Player(qq_id)
        item_number = player_onwer.getItemNumberFromtBindedChara(item_name)
        if item_number < n:
            self.server.sendGroup(self.group_id,"物品不足")
            return
        item_stack = player_onwer.countItemFromBindedCharaToIter(item_name,n)
        if at_ids:
            for i in at_ids:
                player_targer = Player(i)
                for i in range(number):
                    item_stack.item.onUse(player_onwer,player_targer)
        else:
            for i in range(n):
                item_stack.item.onUse(player_onwer,None)
        self.server.sendGroup(self.group_id,"%s使用了%s个%s"%(GroupHelper.getName(data),n,item_name))

    @BaseGroup.register
    @BaseGroup.helpData(["item"], "物品列表", "item_list", "item_list (page) (chara|godown)", "获取物品列表，默认显示当前角色的物品，如果要查看仓库物品请在最后加上godown参数")
    def itemList(self, data: dict, order: Order):
        if not order.checkOrder("item_list"):
            return
        page,m = order.getArgs(1,2)
        flag = False
        if m == "godown":
            flag = True
        if page == None:
            page = "1"
        if not page.isdigit():
            if page == "godown":
                flag = True
                page = "1"
            elif page != "chara":
                self.server.sendGroup(self.group_id,"噫~不会数数的杂鱼大哥哥~kimo")
                return
        page = int(page)
        if page <= 0:
            self.server.sendGroup(self.group_id,"%s是在表示你那为%s的杂鱼智商吗~？"%(page,page))
            return
        limit = 16
        qq_id = GroupHelper.getId(data)
        player =  Player(qq_id)
        if flag:
            items = player.getGodownItems()
        else:
            items = player.getBindedCharaItems()
        item_names = list(items.keys())
        for i in item_names:
            if items[i] <= 0:
                items.pop(i)
        item_names = list(items.keys())
        l = len(item_names)
        max_page = int(l // limit) + 1
        if page > max_page:  
            self.server.sendGroup(self.group_id,"超出页数")
            return
        start_index = limit * (page - 1)
        end_index = limit * (page)
        item_names = item_names[start_index:end_index]
        n = 1
        for i in item_names:
            n = max(len(str(items[i])),n)
        msg = "你当前%s库存如下：\r\n(第%s页/共%s页)\r\n数量      物品名"%("仓库" if flag else "角色",page,max_page)
        for i in item_names:
            s = str(items[i])
            dn = n - len(s)
            s = "  "*dn + s
            msg = msg +"\r\n%s       %s"%(s,i)
        self.server.sendGroup(self.group_id,msg)