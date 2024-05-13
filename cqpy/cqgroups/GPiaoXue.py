from BaseGroupForHHZ import BaseGroupForHHZ
from BaseGroup import BaseGroup
from .I.IRollGroup import IRollGroup
from .I.IItemGroup import IItemGroup
from .I.ITTKGroup import ITTKGroup
from ..GroupHelper import GroupHelper
from ..LLMChat import *
import base64

class GPiaoXue(BaseGroupForHHZ, IRollGroup, IItemGroup, ITTKGroup):
    def __init__(self):
        super().__init__()
        self.group_id = int(base64.b64decode(b'NTUzMDY2MTM0').decode())
        self.clientArgs = {'api_key':None, 'base_url':'https://api.deepseek.com'}
        self.chatArgs = {'model':'deepseek-chat', 'max_tokens':4096, 'temperature':1, 'AI_role':'system', 'user_role':'user', 'AI_content':'You are a helpful assistant'}
        self.chatArgsType = {'model':str, 'max_tokens':int, 'temperature':float, 'AI_role':str, 'user_role':str, 'AI_content':str}
        self.debug_mode = False

    @BaseGroup.register
    @BaseGroup.helpData(["o"], "测试指令", "test", "test (msg)", "测试指令")
    def test(self,data,order):
        if order.checkOrder("test"):
            name = GroupHelper.getName(data)
            arg = order.getArg(1)
            self.server.sendGroup(self.group_id, "%s发送的指令test的第一个参数为%s"%(name,arg))

        @BaseGroup.register
        def chat(self, data, cmd):
            if cmd.checkOrder("chat"):
                if self.clientArgs['api_key'] is None:
                    self.server.sendGroup(self.group_id, "API key is not set, please set it first.")
                    return

                message = cmd.getArg(1)

                client = createClient(**self.clientArgs)
                response = get_response(client, message, **self.chatArgs)
                str = extract_response(response, self.debug_mode)

                self.server.sendGroup(self.group_id, str)

        @BaseGroup.register
        def setAPIKey(self, data, cmd):
            if cmd.checkOrder("setAPIKey"):
                encodedStr = cmd.getArg(1)

                try:
                    decodedStr = base64.b64decode(encodedStr).decode()
                except:
                    self.server.sendGroup(self.group_id, "Invalid encoded API key.")
                    return
                
                self.clientArgs['api_key'] = decodedStr
                self.server.sendGroup(self.group_id, "API key set.")

        @BaseGroup.register
        def setChatArgs(self, data, cmd):
            if cmd.checkOrder("setChatArgs"):
                arg1, arg2 = cmd.getArg(1), cmd.getArg(2)

                if (arg1 is None) or (arg2 is None):
                    self.server.sendGroup(self.group_id, "Invalid chat args.")
                    return
                
                if arg1 not in self.chatArgs:
                    self.server.sendGroup(self.group_id, "Invalid chat args.")
                    return

                self.chatArgs[arg1] = self.chatArgsType[arg1](arg2)

                self.server.sendGroup(self.group_id, f"Successfully set {arg1} to {arg2}.")
        
        @BaseGroup.register
        def showChatArgs(self, data, cmd):
            if cmd.checkOrder("showChatArgs"):
                self.server.sendGroup(self.group_id, str(self.chatArgs))
    