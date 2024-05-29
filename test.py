class Status:
    status_dict1 = {}
    status_dict2 = {}

    @staticmethod
    def getStatus(id:int):
        status = Status.status_dict1.get(id)
        if status is None:
            status = Status.status_dict2.get(id)
        return status

    def __init__(self,id1:int,id2:int):
        self.id1:int = id1
        self.id2:int = id2
        self.banId1 = False
        Status.status_dict1[id1] = self
        Status.status_dict2[id2] = self

    def id1IsBan(self)->bool:
        return self.banId1
    
    def id2IsBan(self)->bool:
        return not self.banId1
    
    def banning(self)->int:
        return self.id1 if self.id1IsBan() else self.id2
    

