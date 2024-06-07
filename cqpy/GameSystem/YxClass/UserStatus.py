class UserStatus:
    qqid1_status = {}
    qqid2_status = {}

    def __init__(self,qqid1:int,qqid2:int):
        self.qqid1 = qqid1
        self.qqid2 = qqid2
        self.ban = False
    
#     @staticmethod
#     def useBan(self,qqid1:int,qqid2:int):
#         UserStatus.qqid1_status = qqid1
#         UserStatus.qqid2_status = qqid2
#         return False
    
# userstatus = UserStatus()