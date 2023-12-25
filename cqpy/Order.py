if __name__ == "__main__":
    from IType import *
else:
    from .IType import *

class Order:
    def __init__(self,o_li:list):
        self.o_li = o_li
        
    def checkOrder(self,order:str):
        if len(self.o_li) <= 0:
            return False
        if order == self.o_li[0][1:]:
            return True
        return False
    
    def getOrderStr(self)->str:
        if len(self.o_li)<=0:
            return ""
        if len(self.o_li[0])<2:
            return ""
        return self.o_li[0][1:]

    def getArg(self,index:int,t:Callable[[T],T]=str)->str|T|None:
        r = None
        if index>=0 and index<len(self.o_li):
            r = self.o_li[index]
        if r == None or t == str:
            return  r
        try:
            r = t(r)
            return r
        except BaseException as e:
            pass
        return None
    
    def getArgs(self,*args:tuple[int],t:Callable[[T],T]=str)->tuple[str|T|None,...]:
        return tuple(self.getArg(i,t=t) for i in args)

if __name__ == "__main__":
    order = Order(["/s","1","b"])
    print(order.getArg(1,int))