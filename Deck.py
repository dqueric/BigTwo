import random
from Card import Card
class Deck:
    def __init__(self):
        self.deck = []
        for suit in ["H", "C", "S", "D"]:
            for rank in [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)
    
    def remove(self, card_list):
        index = 0
        remove_list = []
        for card in self.deck:
            if card.card_value == card_list[index].card_value:
                index += 1
                remove_list.append(card)
        for card in remove_list:
            self.deck.remove(card)

