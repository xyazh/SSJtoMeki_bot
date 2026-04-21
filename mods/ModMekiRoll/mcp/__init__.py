import time
import random
from xyacqbot.packet.PacketMsg import PacketMsg
from xyacqbot.datamanager.UserDataManager import UserDataManager
from xyacqbot.helper.RollHelper import RollHelper
from xyacqbot.CommandDLS import CommandDLS
from xyacqbot.xyazhServer.ConsoleMessage import ConsoleMessage
from mcp.server.fastmcp import FastMCP

MCP = FastMCP()


@MCP.tool()
def sign(qq_id: int) -> str:
    """
    签到
    :param qq_id: qq号
    :return: 签到信息
    """
    user = UserDataManager(qq_id)
    last_time = user.data.get("last_time", 0)
    if (last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
        return "%.2f秒前签到过，今日已签到" % time.time()-last_time
    n = user.data.get("n", 1)
    p = user.data.get("point", 1)
    ap = random.randint(int(n//2), n)
    ap = 1 if ap <= 0 else ap
    user.data["n"] = n+1
    user.data["point"] = p+ap
    user.data["last_time"] = time.time()
    return "第%d天签到获得：%dP" % (n, ap)


@MCP.tool()
def jrrp(qq_id: int) -> str:
    """
    运势
    :param qq_id: qq号
    :return: 运势信息
    """
    user = UserDataManager(qq_id)
    last_time = user.data.get("ys_last_time", 0)
    ys = -1
    if (last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
        ys = user.data.get("ys", -1)
    flag = False
    if ys == -1:
        ys = RollHelper.presetSurpriseDistribution2()
        user.data["ys"] = ys
        user.data["ys_last_time"] = time.time()
        flag = True
    if ys <= 5:
        r = '大吉'
    elif ys <= 20:
        r = '吉'
    elif ys <= 35:
        r = '半吉'
    elif ys <= 50:
        r = '小吉'
    elif ys <= 65:
        r = '末小吉'
    elif ys <= 80:
        r = '末吉'
    elif ys <= 95:
        r = '凶'
    else:
        r = '大凶'
    if not flag:
        r += "，今天已经测过了"
    return "今日的幸运指数是%i %s" % (100-ys, r)

MCP.settings.host = "127.0.0.1"
MCP.settings.port = 37101
MCP.run("sse")

ConsoleMessage.print("MCP已加载", titles=["MEKIMOD"])
