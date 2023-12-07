from ..ItemSystem.Items.BaseItem import BaseItem

class ItemStack:
    def __init__(self,item:BaseItem,n:int):
        self.item = item
        self.n = n

    def __iter__(self):
        return (self.item for _ in range(self.n))
    
    def __bool__(self):
        return self.n > 0
    
    def __len__(self):
        return self.n
    
    def copy(self)->"ItemStack":
        return ItemStack(self.item,self.n)