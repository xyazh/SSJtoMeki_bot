from .IPlatyerBase import IPlatyerBase
from ..Helper import DictHelper
from ..ItemSystem.Items.BaseItem import BaseItem
from ..ItemSystem import ITEMS_LIST
from ..ToolClass.ItemStack import ItemStack


class IItemSystem(IPlatyerBase):
    def findItemFromItemName(self, item_name: str) -> BaseItem | None:
        return ITEMS_LIST.get(item_name, None)

    def findItemFromItemNameNotNone(self, item_name: str) -> BaseItem:
        item = self.findItemFromItemName(item_name)
        if item == None:
            item = BaseItem()
            item.name = item_name
        return item
    
    def getGodownItems(self) -> dict:
        items = self.writeGet("godown_items", {})
        return items

    def setItemNumberToGodown(self, item: str | BaseItem, n: int):
        n = 0 if n <= 0 else int(n)
        if isinstance(item, BaseItem):
            item = item.name
        items = self.getGodownItems()
        items[item] = n

    def getItemNumberFromGodown(self, item: str | BaseItem) -> int:
        if isinstance(item, BaseItem):
            item = item.name
        items = self.getGodownItems()
        return items.get(item, 0)

    def countItemFromGodown(self, item_name: str, count: int) -> int:
        count = 0 if count <= 0 else int(count)
        n = self.getItemNumberFromGodown(item_name)
        real_count = min(count, n)
        n -= real_count
        self.setItemNumberToGodown(item_name,n)
        return real_count

    def countItemFromGodownToIter(self, item_name: str, count: int) -> ItemStack:
        return ItemStack(self.findItemFromItemNameNotNone(item_name), self.countItemFromGodown(item_name, count))
    
    def getCharaItems(self, chara_name: str) -> dict[str:int]:
        charas_items = self.writeGet("charas_items", {"空白卡": {}})
        chara_items = DictHelper.wirteGet(charas_items,chara_name,{})
        return chara_items

    def getBindedCharaItems(self) -> dict[str:int]:
        chara_name = self.getBindedCardName()
        return self.getCharaItems(chara_name)
    
    def setItemNumberTotBindedChara(self, item: str | BaseItem, n: int):
        n = 0 if n <= 0 else int(n)
        if isinstance(item, BaseItem):
            item = item.name
        items = self.getBindedCharaItems()
        items[item] = n

    def getItemNumberFromtBindedChara(self, item: str | BaseItem) -> int:
        if isinstance(item, BaseItem):
            item = item.name
        items = self.getBindedCharaItems()
        return items.get(item, 0)

    def countItemFromtBindedChara(self, item_name: str, count: int) -> int:
        count = 0 if count <= 0 else int(count)
        n = self.getItemNumberFromtBindedChara(item_name)
        real_count = min(count, n)
        n -= real_count
        self.setItemNumberTotBindedChara(item_name,n)
        return real_count
    
    def countItemFromBindedCharaToIter(self, item_name: str, count: int) -> ItemStack:
        return ItemStack(self.findItemFromItemNameNotNone(item_name), self.countItemFromtBindedChara(item_name, count))