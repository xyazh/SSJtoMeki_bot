from .BasePlayer import BasePlayer

class Player(BasePlayer):
    def __init__(self, qq_id: int):
        super().__init__(qq_id)