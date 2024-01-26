from ..Event import Event
from ..xyazhServer.ConsoleMessage import ConsoleMessage
from ..GroupHelper import GroupHelper
from ..MsgHelper import MsgHelper
from ..DataManager import DataManager

MSG_LEN = 400

class DisEvent:
    data_manager = DataManager()
    @staticmethod
    @Event.EventBus.register(Event.EventBus.FUNC_GROUP_MSG_EVENT)
    def disFucGroupMsgEvent(event:Event.FucGroupMsgEvent):
        if event.checkRecv():
            group_id = event.getGroupId()
            name = GroupHelper.getName(event.data)
            uid = GroupHelper.getId(event.data)
            msg = event.getMsg()
            msg = msg.replace("\r","")
            msg = msg.replace("\n","")
            if len(msg) > MSG_LEN:
                msg = msg[:MSG_LEN]+"..."
            if event.hasAt:
                owner_uid = uid
                takers_uid = " ".join(map(str,event.atIds))
                ConsoleMessage.printC("来自群%d%s(%d)@了%s：%s"%(group_id,name,owner_uid,takers_uid,msg))
            else:
                ConsoleMessage.printC("来自群%d%s(%d)的消息：%s"%(group_id,name,uid,msg))
        if event.checkSend():
            group_id = event.getGroupId()
            msg = event.getMsg()
            msg = msg.replace("\r","")
            msg = msg.replace("\n","")
            if len(msg) > MSG_LEN:
                msg = msg[:MSG_LEN]+"..."
            ConsoleMessage.printC("发送到群%d的消息：%s"%(group_id,msg))
    
    @staticmethod
    @Event.EventBus.register(Event.EventBus.PRIVATE_MSG_EVENT)
    def disPrivateMsgEvent(event:Event.PrivateMsgEvent):
        if event.checkRecv():
            uid = event.getId()
            name = MsgHelper.getNickname(event.data)
            msg = event.getMsg()
            msg = msg.replace("\r","")
            msg = msg.replace("\n","")
            if len(msg) > MSG_LEN:
                msg = msg[:MSG_LEN]+"..."
            ConsoleMessage.printC("来自%d(%s)的私聊消息：%s"%(uid,name,msg))

    @staticmethod
    @Event.EventBus.register(Event.EventBus.GROUP_REGISTER_EVENT)
    def disGroupRegister(event:Event.GruopRegisterEvent):
        if event.group_id < 0:
            event.setCancel(True)
            return
        dis_register_fuc_name:dict = DisEvent.data_manager.findGet("dis_register_fuc.json")
        group_id = str(event.group_id)
        if group_id in dis_register_fuc_name:
            fun_name_list = dis_register_fuc_name[group_id]
            l = len(event.fucs)
            for i in (l-1-j for j in range(l)):
                if event.fucs[i].__name__ in fun_name_list:
                    if event.group_id in event.s.dis_register_list:
                        event.s.dis_register_list[event.group_id].append(event.fucs.pop(i))
                    else:
                        event.s.dis_register_list[event.group_id] = [event.fucs.pop(i)]        

    @staticmethod
    @Event.EventBus.register(Event.EventBus.ROLL_RESULT_EVENT)
    def disGroupRegister(event:Event.RollResultEvent):
        event.setRollResult(6)