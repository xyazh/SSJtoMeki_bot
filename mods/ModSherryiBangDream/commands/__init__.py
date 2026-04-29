import random
import time
import base64
import threading
from mods.LibModCommand.command.Command import Command
from xyacqbot.Cqserver import Cqserver
from xyacqbot.packet.PacketMsg import PacketMsg
from xyacqbot.msg.MsgBuilder import MsgBuilder
from xyacqbot.datamanager.UserDataManager import UserDataManager
from xyacqbot.helper.RollHelper import RollHelper
from xyacqbot.CommandDLS import CommandDLS
from tsugu_api import *

BOT_NAME = "雪莉"

def threadWrapper(fn, *args, **kwargs):
    threading.Thread(target=fn, args=args, kwargs=kwargs).start()



@Command(
    "[e:emun('.','/','。')][e:emun('bg','bang','bgd','bangdream')][e:emun(' song','song ',' song ','song')][name:str]",
    sign="bg song [name:str]",
    desc="邦多利查歌",
    category="BGD"
)
def searchSong(msg: PacketMsg, name: str = "", **kw):
    if not name:
        return
    def _searchSong():
        result = search_song([3, 0], text=name)
        if not result:
            return
        song = result[0]
        if song.get("type") != "base64":
            return
        data = song.get("string")
        send_msg = MsgBuilder()
        send_msg.updateImage(f"base64://{data}")
        Cqserver.instance.sendGroupMsg(send_msg, msg.group_id)
    threadWrapper(_searchSong)


@Command(
    "[e:emun('.','/','。')][e:emun('bg','bang','bgd','bangdream')][e:emun(' card','card ',' card ','card')][name:str]",
    sign="bg card [name:str]",
    desc="邦多利查卡",
    category="BGD"
)
def searchCard(msg: PacketMsg, name: str = "", **kw):
    if not name:
        return
    def _searchCard():
        result = search_card([3, 0], text=name)
        if not result:
            return
        card = result[0]
        if card.get("type") != "base64":
            return
        data = card.get("string")
        send_msg = MsgBuilder()
        send_msg.updateImage(f"base64://{data}")
        Cqserver.instance.sendGroupMsg(send_msg, msg.group_id)
    threadWrapper(_searchCard)


@Command(
    "[e:emun('.','/','。')][e:emun('bg','bang','bgd','bangdream')][e:emun(' pop','pop ',' pop ','pop')][count:int] [id:int]",
    sign="bg pop [count:int] [id:int]",
    desc="邦多利模拟抽卡",
    category="BGD"
)
def gachaSimulate(msg: PacketMsg, count: int = 10,id: int = 1, **kw):
    def _gachaSimulated():
        result = gacha_simulate(3, times=count, gacha_id=id)
        if not result:
            return
        card = result[0]
        if card.get("type") != "base64":
            return
        data = card.get("string")
        send_msg = MsgBuilder()
        send_msg.updateImage(f"base64://{data}")
        Cqserver.instance.sendGroupMsg(send_msg, msg.group_id)
    threadWrapper(_gachaSimulated)