from xyacqbot.datamanager.UserDataManager import UserDataManager
from .PlCard import PlCard


class UserRollData(UserDataManager):

    def __new__(cls, qq: str):
        return super().__new__(cls, qq)

    def __init__(self, qq: str):
        super().__init__(qq)

    def _load(self):
        super()._load()
        data = self.getData("roll_data") or {}
        cards: list[PlCard] = PlCard.fromDataList(data.get("cards", []))
        self.cards: dict[str, PlCard] = {
            card.name: card for card in cards
        }
        bindind_card_name: str = data.get("bindind_card", "空白卡")
        self.bindind_card: PlCard | None = self.cards.get(
            bindind_card_name, None
        )

    def save(self):
        roll_data = {
            "bindind_card": self.bindind_card.name if self.bindind_card else None,
            "cards": [card.toData() for card in self.cards.values()]
        }
        self.setData("roll_data", roll_data)
        super().save()

    def createCard(self, name: str) -> PlCard:
        card = PlCard({"name": name})
        self.cards[card.name] = card
        return card
    
    def bindCard(self, card: PlCard):
        self.bindind_card = card

    def getCard(self, name: str) -> PlCard | None:
        return self.cards.get(name, None)
    
    def getBindingCard(self,create:bool=False) -> PlCard | None:
        if create and self.bindind_card is None:
            self.bindind_card = self.createCard("空白卡")
        return self.bindind_card
    
    def removeCard(self, name: str):
        card = self.getCard(name)
        if card is not None:
            del self.cards[name]
            if self.bindind_card == card:
                self.bindind_card = None

    def cardsList(self) -> list[PlCard]:
        return list(self.cards.values())
