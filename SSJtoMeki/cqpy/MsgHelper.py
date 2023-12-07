ORDER_SPLIT_LIST =  [".","/","。","\\"]

class MsgHelper:
    @staticmethod
    def getId(data:dict)->int:
        if "sender" in data:
            if "user_id" in data["sender"]:
                return data["sender"]["user_id"]
        return -1

    @staticmethod
    def getMsg(data:dict)->str:
        if type(data)==dict: 
            if 'raw_message' in data:
                return data['raw_message']
        return ""

    @staticmethod
    def getNickname(data:dict)->str:
        if "sender" in data:
            if "nickname" in data["sender"]:
                return data["sender"]["nickname"]
        return ""