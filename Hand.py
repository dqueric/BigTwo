from Card import compare_card, RANK_VALUE, SUIT_VALUE
from functools import cmp_to_key
from itertools import combinations

class Hand:
    def __init__(self, hand):
        # sorts the hand into card value order
        self.hand = sorted(hand, key = cmp_to_key(compare_card))
        # dictionary of (score, play) for a given number of cards in the play
        self.plays = {1: [], 2: [], 3: [], 4: [], 5: []}

        # dictionary of card organised into rank and suit
        rank_dict = {}
        suit_dict = {}
        for card in self.hand:
            if RANK_VALUE[card.rank] not in rank_dict:
                rank_dict[RANK_VALUE[card.rank]] = []
            if card.suit not in suit_dict:
                suit_dict[card.suit] = []
            rank_dict[RANK_VALUE[card.rank]].append(card)
            suit_dict[card.suit].append(card)

        # singles
        for play in self.hand:
            self.plays[1].append(tuple([play.card_value, tuple([play])]))

        # doubles, triples, quadruples
        for rank in rank_dict:
            plays_2 = combinations(rank_dict[rank], 2)
            plays_3 = combinations(rank_dict[rank], 3)
            plays_4 = combinations(rank_dict[rank], 4)
            for play in plays_2:
                self.plays[2].append((play[-1].card_value, play))
            for play in plays_3:
                self.plays[3].append((play[-1].card_value, play))
            for play in plays_4:
                self.plays[4].append((play[-1].card_value, play))

        # straight and straight flush
        continuous = None
        prev = None
        hand_ranks = list(rank_dict.keys())
        for i in range(len(rank_dict)):
            rank = list(rank_dict)[i]
            if prev is None:
                prev = hand_ranks[i]
                continuous = 1
            elif prev + 1 == rank:
                continuous = min(5, continuous + 1)
            elif prev + 1 != rank:
                continuous = 1
            prev = hand_ranks[i]

            if continuous == 5:
                for card_1 in rank_dict[hand_ranks[i-4]]:
                    for card_2 in rank_dict[hand_ranks[i-3]]:
                        for card_3 in rank_dict[hand_ranks[i-2]]:
                            for card_4 in rank_dict[hand_ranks[i-1]]: 
                                for card_5 in rank_dict[hand_ranks[i]]:
                                    if card_1.suit == card_2.suit and card_2.suit == card_3.suit and card_3.suit == card_4.suit and card_4.suit == card_5.suit:
                                        self.plays[5].append((card_5.card_value+64*4, (card_1, card_2, card_3, card_4, card_5)))
                                    else:
                                        self.plays[5].append((card_5.card_value, (card_1, card_2, card_3, card_4, card_5)))

        # flush, no straight flush
        for suit in suit_dict:
            plays_flush = combinations(suit_dict[suit], 5)
            for play in plays_flush:
                if RANK_VALUE[play[4].rank] - RANK_VALUE[play[0].rank] != 4 :
                    self.plays[5].append((RANK_VALUE[play[4].rank]+SUIT_VALUE[play[4].suit]*16+64, play))

        # full house
        for triple_play in self.plays[3]:
            for double_play in self.plays[2]:
                if triple_play[1][0].rank != double_play[1][0].rank:
                    self.plays[5].append((triple_play[1][2].card_value+64*2, tuple(list(triple_play[1]) + list(double_play[1]))))

        # four of a kind + 1
        for quadruple_play in self.plays[4]:
            for single_play in self.plays[1]:
                if quadruple_play[1][0].rank != single_play[1][0].rank:
                    self.plays[5].append((quadruple_play[1][3].card_value+64*3, tuple(list(quadruple_play[1]) + list(single_play[1]))))
        self.plays[5] = sorted(self.plays[5], key=lambda x: x[0])

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