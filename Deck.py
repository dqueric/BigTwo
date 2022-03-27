import random
from Card import Card
class Deck:
    def __init__(self):
        self.deck = []
        for suit in ["H", "C", "S", "D"]:
            for rank in [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]:
                self.deck.append(Card(suit, rank))
        random.shuffle(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)
