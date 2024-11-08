from .BasePlayer import BasePlayer
from ...GroupHelper import GroupHelper

class Player(BasePlayer):

    @staticmethod
    def getPlayerFromData(data:dict)->"Player":
        return Player(GroupHelper.getId(data))

    def __init__(self, qq_id: int):
        super().__init__(qq_id)