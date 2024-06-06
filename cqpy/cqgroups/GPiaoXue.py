from .BaseGroupForHHZ import BaseGroupForHHZ
from .BaseGroup import BaseGroup
from .I.IRollGroup import IRollGroup
from .I.IItemGroup import IItemGroup
from .I.ITTKGroup import ITTKGroup
from ..GroupHelper import GroupHelper
from ..DataManager import DataManager
from ..LLMChat import LLMAPI, DeepseekAPI, ERNIEAPI, QwenAPI
import base64
import pickle
import threading


class GPiaoXue(BaseGroupForHHZ, IRollGroup, IItemGroup, ITTKGroup):
    def __init__(self):
        super().__init__()
        self.group_id = int(base64.b64decode(b'NTUzMDY2MTM0').decode())
        self.debug_mode = False

        try:
            self.data_manager: DataManager = DataManager("\\PiaoXue\\")
            with self.data_manager.openFile('key.pkl', 'rb') as f:
                key_dict = pickle.load(f)

                
                self.API_dict = {
                    "DeepseekAPI": DeepseekAPI(key_dict['deepseek']),
                    "ERNIEApi": ERNIEAPI(key_dict['ERNIE']['api_key'], key_dict['ERNIE']['secret_key']),
                    "QwenAPI": QwenAPI(key_dict['Qwen'])}

            self.activeAPI: LLMAPI = self.API_dict["QwenAPI"]
        except BaseException:
            pass

    @BaseGroup.register
    @BaseGroup.helpData(["o"], "测试指令", "test", "test (msg)", "测试指令")
    def test(self, data, order):
        if order.checkOrder("test"):
            name = GroupHelper.getName(data)
            arg = order.getArg(1)
            self.server.sendGroup(
                self.group_id, "%s发送的指令test的第一个参数为%s" % (name, arg))

    @BaseGroup.register
    def chat(self, data, cmd):
        if not cmd.checkOrder("chat"):
            return
        
        # 拼接消息
        # message = " ".join(cmd.o_li[1:])

        # 使用GroupHelper.getMsg(data)获取原消息
        message = GroupHelper.getMsg(data)
        # 截去指令/chat 开头部分
        message = message[6:]
        def sendMsg():
            # 调用API
            response = self.activeAPI.chat(message, debug_mode=self.debug_mode)

            self.server.sendGroup(self.group_id, response)

        threading.Thread(target=sendMsg).start()



    @BaseGroup.register
    def changeAPI(self, data, cmd):
        if cmd.checkOrder("changeAPI"):
            arg1 = cmd.getArg(1)

            if arg1 in self.API_dict:
                self.activeAPI = self.API_dict[arg1]
                self.server.sendGroup(self.group_id, f"API已切换为{arg1}")
            else:
                self.server.sendGroup(self.group_id, f"API {arg1} 不存在")
                self.server.sendGroup(
                    self.group_id, f"可用API有{', '.join(self.API_dict.keys())}")

    @BaseGroup.register
    def showAPIList(self, data, cmd):
        if cmd.checkOrder("showAPIList"):
            self.server.sendGroup(self.group_id, f"当前API为{self.activeAPI}")
            self.server.sendGroup(
                self.group_id, f"可用API有{', '.join(self.API_dict.keys())}")
            message = "API介绍：\nDeepseekAPI：由deepseek公司开发的开源模型deepseek v2，性能优秀，推理成本低\nERNIEApi：由百度开发的ERNIE系列模型，4和3.5性能不错，但是API贵。免费的speed和lite模型有点憨憨。\nQwenAPI：由阿里开发的Qwen模型，分闭源的qwen系列和开源的qwen1.5系列，性能优秀，送了一大堆免费额度，建议用这个\n"
            self.server.sendGroup(self.group_id, message)

    @BaseGroup.register
    def changeModel(self, data, cmd):
        if cmd.checkOrder("changeModel"):
            arg1 = cmd.getArg(1)

            if arg1 in self.activeAPI.model_list:
                self.activeAPI.model = arg1
                self.server.sendGroup(self.group_id, f"模型已切换为{arg1}")
            else:
                self.server.sendGroup(self.group_id, f"模型{arg1}不存在")
                self.server.sendGroup(
                    self.group_id, f"可用模型有{', '.join(self.activeAPI.model_list)}")

    @BaseGroup.register
    def showModelList(self, data, cmd):
        if cmd.checkOrder("showModelList"):
            self.server.sendGroup(
                self.group_id, f"当前模型为{self.activeAPI.model}")
            self.server.sendGroup(
                self.group_id, f"可用模型有{', '.join(self.activeAPI.model_list)}")

    @BaseGroup.register
    def debugMode(self, data, cmd):
        if cmd.checkOrder("debugMode"):
            self.debug_mode = not self.debug_mode
            self.server.sendGroup(
                self.group_id, f"debug模式已切换为{self.debug_mode}")
