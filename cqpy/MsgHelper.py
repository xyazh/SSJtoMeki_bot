import time

ORDER_SPLIT_LIST =  [".","/","。","\\"]

class MsgHelper:
    @staticmethod
    def getId(data:dict)->int:
        """
        传入数据，获取qq号
        """
        if "sender" in data:
            if "user_id" in data["sender"]:
                return data["sender"]["user_id"]
        return -1

    @staticmethod
    def getMsg(data:dict)->str:
        """
        传入数据，获取消息
        """
        if isinstance(data,dict): 
            if 'raw_message' in data:
                return data['raw_message']
        return ""

    @staticmethod
    def getNickname(data:dict)->str:
        """
        传入数据，获取昵称
        """
        if "sender" in data:
            if "nickname" in data["sender"]:
                return data["sender"]["nickname"]
        return ""
    
    @staticmethod
    def createMsg(group_id:int, msg:str,self_id:int=-1,user_id:int=-1)->dict:
        data = {
            'self_id': self_id,
            'user_id': user_id,
            'time': int(time.time()),
            'message_id': -1,
            'real_id': -1,
            'message_seq': -1,
            'message_type': 'group',
            'sender': {
                'user_id': -1,
                'nickname': 'consle_test',
                'card': '控制台测试',
                'role': 'test'
            },
            'raw_message': msg,
            'font': 14,
            'sub_type': 'normal',
            'message': [
                {
                    'data': {'text': msg},
                    'type': 'text'
                }
            ],
            'message_format': 'array',
            'post_type': 'message',
            'group_id': group_id
        }
        return data
