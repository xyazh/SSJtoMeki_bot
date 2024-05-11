# SSJtoMeki_bot
work work
# 开发
## 如何接收消息
### 基于群的处理
如果你希望针对每个群来实现特定的功能，你可以在cqpy.cqgroups个目录新建.py文件，在文件里创建BaseGruop的子类。程序将会自动导入这个目录下的文件，并获取其中所有BaseGruop的子类。

    class G114514(BaseGroup):
        def __init__(self):
            super().__init__()
            self.group_id = 114514

在构造函数中指定需要处理的群号。

    @BaseGroup.register
    def test(self, data: dict, order: Order):
        if order.checkOrder("test"):
            name = GroupHelper.getName(data)
            arg = order.getArg(1)
            self.server.sendGroup(self.group_id, "%s发送的指令test的第一个参数为%s"%(name,arg))

使用@BaseGroup.register装饰的方法会被加入消息回调，在每次收到消息时会被触发。

被装饰的方法接受两个参数data: dict, order: Order

data包含消息原始数据，可通过GroupHelper里的一些静态封装方法来获取聚体数据

order是一个内置的指令解析器，用于解析诸如"/test 你是一个一个一个"这样的指令

BaseGroup类中带有一个Cqserver的实例，为self.server。通过调用sendGroup方法往群里发送消息

### 基于消息的处理
此功能还未完善

## 如何发送消息

### 发送群消息
获取Cqserver的实例，调用其中的sendGroup(self, group_id:str|int, msg:str)方法可发送消息。

在BaseGroup类中Cqserver的实例为self.server。

在部分Event中Cqserver的实例为self.s。
### 发送私聊消息
