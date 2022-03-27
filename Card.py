SUIT_VALUE = {"S": 3, "H": 2, "C": 1, "D": 0}
RANK_VALUE = {}
for i in range(3, 11):
    RANK_VALUE[(str(i))] = i
RANK_VALUE["J"] = 11
RANK_VALUE["Q"] = 12
RANK_VALUE["K"] = 13
RANK_VALUE["A"] = 14
RANK_VALUE["2"] = 15

class Card:
    def __init__(self, suit :str, rank :str):
        self.suit = suit
        self.rank = rank
        self.card_value = SUIT_VALUE[self.suit] + RANK_VALUE[self.rank]*4

def compare_card(card_1, card_2):
    if card_1.card_value < card_2.card_value:
        return -1
    elif card_1.card_value > card_2.card_value:
        return 1
    else:
        return 0