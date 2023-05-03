from Card import compare_card, RANK_VALUE, SUIT_VALUE
from functools import cmp_to_key
from itertools import combinations

class Hand:
    def __init__(self, hand, deck):
        # the deck being used
        self.deck = deck
        # sorts the hand into card value order
        self.hand = sorted(hand, key = cmp_to_key(compare_card))
        hand_set = set(self.hand)
        # dictionary of (score, play) for a given number of cards in the play
        self.plays = {1: [], 2: [], 3: [], 4: [], 5: []}

        for n in self.deck.plays:
            for play in self.deck.plays[n]:
                possible = True
                for card in play[1]:
                    if card not in hand_set:
                        possible = False
                        break
                if possible:
                    self.plays[n].append(play)
        

    def play_card(self, card):
        # removes card from hand, also removes available plays that have the card
        self.hand.remove(card)
        remove_plays = []
        for play_type in self.plays:
            for play in self.plays[play_type]:
                for c in play[1]:
                    if c.card_value == card.card_value:
                        remove_plays.append((play_type, play))
                        break
        for play in remove_plays:
            self.plays[play[0]].remove(play[1])

if __name__ == '__main__':
    from Deck import Deck
    deck = Deck()
    hand = Hand(deck.deck[:13], deck)