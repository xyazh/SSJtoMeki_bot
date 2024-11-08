import queue

from ..PlayerSystem.Player import Player
from ..Helper.RollHelper import RollHelper


class RollPool:
    ROLL_POOL: dict[int, 'RollPool'] = {}
    MAX_SIZE = 100

    def __new__(cls, group_id: int):
        if group_id not in cls.ROLL_POOL:
            cls.ROLL_POOL[group_id] = super().__new__(cls)
            cls.ROLL_POOL[group_id].is_inited = False
        return cls.ROLL_POOL[group_id]

    def __init__(self, group_id: int):
        if self.is_inited:
            return
        self.is_inited = True
        self.group_id: int = group_id
        self.players: dict[int, RollPool.TempPlayer] = {}

    def addPlayer(self, player: int | Player):
        if isinstance(player, int):
            self.players[player] = RollPool.TempPlayer(player)
        elif isinstance(player, Player):
            self.addPlayer(player.qq_id)

    def getPlayer(self, qq_id: int|str) -> "RollPool.TempPlayer|None":
        if isinstance(qq_id, str):
            qq_id = int(qq_id)
        return self.players.get(qq_id)

    class TempPlayer:
        def __init__(self, user_id: int):
            self.user_id: int = user_id
            self.roll_points = queue.Queue(maxsize=RollPool.MAX_SIZE)
            self.dis_roll_fuc = self.disRollFuc
            self.roll_points
            self.flush()

        def putRoll(self, roll: int | float):
            self.roll_points.put(roll, block=False)

        def getRoll(self) -> int | float:
            if self.roll_points.empty():
                self.flush()
            r = self.roll_points.get()
            self.putRoll(self.dis_roll_fuc(RollPool.MAX_SIZE-1))
            return r

        def readRoll(self, index: int) -> int | float:
            return self.roll_points.queue[index]
        
        def writeRoll(self, index: int, v: int | float):
            self.roll_points.queue[index] = v

        def disRollFuc(self, index: int) -> int | float:
            return RollHelper.d(1, 100)

        def flush(self, fuc=None):
            if fuc is None:
                fuc = self.dis_roll_fuc
            self.roll_points.queue.clear()
            for i in range(RollPool.MAX_SIZE):
                self.roll_points.put(fuc(i))

        def getPlayer(self) -> Player:
            return Player(self.user_id)
