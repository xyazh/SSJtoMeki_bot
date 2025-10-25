import time
from .Cqserver import Cqserver
from .GroupHelper import GroupHelper
from .Order import Order

REGISTER_FUC = []
COMMON_TYPES = [
    "群聊模式",
    "控制台指令模式"
]


class CommonTest:

    @staticmethod
    def register(fuc):
        REGISTER_FUC.append(fuc)
        return fuc

    def __init__(self, server: Cqserver):
        self.server = server
        self.select_group_id = 114514
        self.do_send_group = False
        self.common_type = 0
        self.common_desc = "使用/cq_change切换"

    def loop(self):
        while not self.server.web_and_listen.ready:
            time.sleep(0.1)
        print(COMMON_TYPES[int(self.common_type %
              len(COMMON_TYPES))] + "(%s)" % self.common_desc)
        while True:
            msg = input(">>")
            order = GroupHelper.getOrderFromStr(msg)
            for fuc in REGISTER_FUC:
                fuc(self, msg, order)

    @register
    def change(self, msg: str, order: Order):
        if not order.checkOrder("cq_change"):
            return
        self.common_type += 1
        print(COMMON_TYPES[int(self.common_type %
              len(COMMON_TYPES))] + "(%s)" % self.common_desc)

    @register
    def select(self, msg: str, order: Order):
        if not order.checkOrder("cq_group"):
            return
        arg = order.getArg(1, int)
        arg = -1 if arg is None else arg
        self.select_group_id = arg
        print("当前选择群聊：%s" % self.select_group_id)

    @register
    def sendGroup(self, msg: str, order: Order):
        if order.checkOrder("cq_change") or int(self.common_type % len(COMMON_TYPES)) != 0:
            return
        self.server.testMsg(self.select_group_id, msg)

    @register
    def sendAudio(self, msg: str, order: Order):
        if not order.checkOrder("send_a") and not order.checkOrder("send_audio"):
            return
        group_id = order.getArg(1, int)
        r = order.getArg(2)
        if r is None or group_id is None:
            print("参数错误")
            return
        print(self.server.sendGroup(group_id, "[CQ:record,file=file://%s]" % r))
