from .Order import Order
from .GroupHelper import GroupHelper
from .MsgHelper import MsgHelper
from . import Cqserver
from .CQCode import CQCodeHelper

class Event:
    """事件系统

    被注册到事件总线的方法不做特殊说明的话是全局的，无论有没有在cqgroups里添加过这个群
    """
    class EventBus:
        #群聊消息事件(仅处理机器人自身收到或发送的消息)
        FUNC_GROUP_MSG_EVENT = 1
        #私聊消息事件
        PRIVATE_MSG_EVENT = 2
        #群方法注册事件
        GROUP_REGISTER_EVENT = 3
        "群@事件（已弃用，整合进了消息事件里）"
        GROUP_AT_EVENT = 4
        #消息撤回事件
        MAS_RECALL_EVENT = 5
        #群成员事件
        MENBER_GROUP_EVENT = 5
        #群自己事件
        SELF_GROUP_EVENT = 7
        #被邀请进群事件
        INVITED_TO_GROUP_EVENT = 8
        #群禁言事件
        GROUP_BAN_EVENT = 9
        #添加好友事件
        FRIEND_ADD_EVENT = 10
        #骰子结果事件
        ROLL_RESULT_EVENT = 11

        EVENT_BUS_MAP = {
            FUNC_GROUP_MSG_EVENT:[],
            PRIVATE_MSG_EVENT:[],
            GROUP_REGISTER_EVENT:[],
            GROUP_AT_EVENT:[],
            MAS_RECALL_EVENT:[],
            MENBER_GROUP_EVENT:[],
            SELF_GROUP_EVENT:[],
            INVITED_TO_GROUP_EVENT:[],
            GROUP_BAN_EVENT:[],
            FRIEND_ADD_EVENT:[],
            ROLL_RESULT_EVENT:[]

        }

        @staticmethod
        def hookFucGroupMsgEvent(data:dict,t:str,s:Cqserver):
            fuc_group_msg_event:Event.FucGroupMsgEvent = Event.FucGroupMsgEvent(data,t,s)
            for func in Event.EventBus.EVENT_BUS_MAP[Event.EventBus.FUNC_GROUP_MSG_EVENT]:
                func(fuc_group_msg_event)
            return fuc_group_msg_event

        @staticmethod
        def hookPrivateMsgEvent(data:dict,t:str,s:Cqserver):
            private_msg_event:Event.PrivateMsgEvent = Event.PrivateMsgEvent(data,t,s)
            for func in Event.EventBus.EVENT_BUS_MAP[Event.EventBus.PRIVATE_MSG_EVENT]:
                func(private_msg_event)
            return private_msg_event

        @staticmethod
        def hookGruopRegisterEvent(group_id:int,fucs:list[object],s:Cqserver):
            gruop_register_event:Event.GruopRegisterEvent = Event.GruopRegisterEvent(group_id,fucs,s)
            for func in Event.EventBus.EVENT_BUS_MAP[Event.EventBus.GROUP_REGISTER_EVENT]:
                func(gruop_register_event)
            return gruop_register_event
        
        @staticmethod
        def hookRollResultEvent(data:dict,t:str,result:float,s:Cqserver):
            roll_result_event:Event.RollResultEvent = Event.RollResultEvent(data,result,s)
            for func in Event.EventBus.EVENT_BUS_MAP[Event.EventBus.ROLL_RESULT_EVENT]:
                func(roll_result_event)
            return roll_result_event


        def register(t:int):
            def _r(fuc:object):
                if t in Event.EventBus.EVENT_BUS_MAP:
                    Event.EventBus.EVENT_BUS_MAP[t].append(fuc)
            return _r

    class BaseEvent:
        def __init__(self):
            self.__is_cancel = False

        def setCancel(self,b:bool):
            self.__is_cancel = b

        def getCancel(self)->bool:
            return self.__is_cancel

        def isCancel(self)->bool:
            return self.__is_cancel
        
    class MsgBaseEvent(BaseEvent):
        def __init__(self,data:dict,t:str,s:Cqserver):
            super().__init__()
            self.type:str = t
            self.data = data
            self.s = s

        def getOrder(self)->Order:
            return GroupHelper.getOrderFromData(self.data)

        def copyData(self)->dict:
            return self.data.copy()

        def checkSend(self)->bool:
            return self.type == "send"

        def checkRecv(self)->bool:
            return self.type == "recv"

    class FucGroupMsgEvent(MsgBaseEvent):
        def __init__(self,data:dict,t:str,s:Cqserver):
            super().__init__(data,t,s)
            self.msg = GroupHelper.getMsg(data)
            self.group_id = data["group_id"]
            self.cqcodes = CQCodeHelper.creatCQCodeFromMsg(self.msg)
            self.hasAt = False
            self.atIds = set()
            for i in self.cqcodes:
                if i.t == "at":
                    self.atIds.add(i.data["qq"])
                    self.hasAt = True
        
        def getMsg(self)->str:
            return self.msg

        def setMsg(self,msg:str)->None:
            self.msg = msg
    
        def getGroupId(self)->int:
            return self.group_id

        def setGroupId(self,group_id:int)->None:
            self.group_id = group_id

        def getName(self)->str:
            return GroupHelper.getName(self.data)

        def getId(self)->int:
            return GroupHelper.getId(self.data)

    class PrivateMsgEvent(MsgBaseEvent):
        def __init__(self,data:dict,t:str,s:Cqserver):
            super().__init__(data,t,s)
            self.msg = MsgHelper.getMsg(data)
            self.sub_type = data["sub_type"]
            self.cqcodes = CQCodeHelper.creatCQCodeFromMsg(self.msg)

        def getMsg(self)->str:
            return self.msg

        def setMsg(self,msg:str)->None:
            self.msg = msg

        def getId(self)->int:
            return MsgHelper.getId(self.data)

        def checkSubTypeGroup(self)->bool:
            return self.sub_type == "group"

        def checkSubTypeSelfGroup(self)->bool:
            return self.sub_type == "self_group"

        def checkSubTypeFriend(self)->bool:
            return self.sub_type == "friend"

        def checkSubTypeOther(self)->bool:
            return self.sub_type == "other"

    class GruopRegisterEvent(BaseEvent):
        def __init__(self,group_id:int,fucs:list[object],s:Cqserver):
            super().__init__()
            self.group_id = group_id
            self.fucs = fucs
            self.s = s

    class RollResultEvent(BaseEvent):
        def __init__(self,data:dict,result:float,s:Cqserver):
            super().__init__()
            self.data = data
            self.result = result
            self.s = s

        def getRollResult(self)->float:
            return self.result
        
        def setRollResult(self,result:float)->None:
            self.result = result