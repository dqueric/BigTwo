from Players.Player import Player
from Players.RandomPlayer import RandomPlayer
from GameState import GameState
import numpy as np
from Deck import Deck
from Hand import Hand
from Card import Card
 
def game_over(won_dict):
    return(sum([i is not None for i in won_dict]) == 4)

def pass_reset_check(pass_dict, won_dict, last_player):
    pass_count = 0
    total_count = 0
    in_player = None
    for i in range(len(won_dict)):
        if won_dict[i] is None:
            total_count += 1
            if pass_dict[i] is True:
                pass_count += 1
            else:
                in_player = i
    return((total_count - pass_count == 1 and last_player == in_player) or (total_count == pass_count and won_dict[last_player] is not None))

class MontePlayer(Player):
    def __init__(self, n_sims=100):
        self.n_sims = n_sims

    def action(self, gamestate):
        possible_actions = self.action_list(gamestate)
        action_score = []
        for action_index in range(len(possible_actions)):
            action_score.append(0)
            for sample in range(self.n_sims):
                action_score[-1] += self.simulate(gamestate, action_index)
        return(possible_actions[np.argmin(action_score)])

    def simulate(self, gamestate, action_index):
        orig_player = gamestate.curr_turn
        last_play = gamestate.last_play
        pass_dict = gamestate.pass_dict.copy()
        hand_dict = gamestate.hand_dict.copy()
        played_cards = gamestate.played_cards.copy()
        won_dict = gamestate.won_dict.copy()
        last_player = gamestate.last_player
        curr_turn = gamestate.curr_turn
        player_list = [RandomPlayer() for i in range(4)]
        log = gamestate.log
        # randomly generate handlist
        hand = gamestate.hand
        deck = Deck()
        deck.remove(hand.hand + played_cards)
        deck.shuffle()
        hand_list = []
        for i in range(len(hand_dict)):
            if i == curr_turn:
                hand = Hand([Card(card.suit, card.rank) for card in gamestate.hand.hand])
                hand_list.append(hand)
            else:
                hand_list.append(Hand(deck.deck[:hand_dict[i]]))
                deck.deck = deck.deck[hand_dict[i]:]
        placement = sum([i is not None for i in won_dict]) + 1
        first_turn = True
        while True:
            gamestate = GameState(hand_list[curr_turn], last_play, last_player, pass_dict, hand_dict, played_cards, won_dict, curr_turn, log)
            if not first_turn:
                action = player_list[curr_turn].action(gamestate)
            else:
                action = self.action_list(gamestate)[action_index]
                first_turn = False
            if action == "PASS":
                pass_dict[curr_turn] = True
                log += "PLAYER " + str(curr_turn) + ": " + "Passed\n"
            else:
                last_player = curr_turn
                log += "PLAYER " + str(curr_turn) + ": " + str((action[0], [i.rank + i.suit for i in action[1]])) + "\n"
                last_play = action
                hand_dict[curr_turn] -= len(action[1])
                played_cards += list(action[1])
                for card in action[1]:
                    hand_list[curr_turn].play_card(card)
                if hand_dict[curr_turn] == 0:
                    won_dict[curr_turn] = placement
                    log += "PLAYER " + str(curr_turn) + " Placement: " + str(placement) + "\n"
                    placement += 1
                    if placement == 4:
                        for i in range(4):
                            if won_dict[i] is None:
                                won_dict[i] = 4
                                log += "PLAYER " + str(i) + " Placement: " + str(placement) + "\n"
                                break
                if game_over(won_dict):
                    break
            reset_check = pass_reset_check(pass_dict, won_dict, last_player)
            if reset_check:
                pass_dict = [False, False, False, False]
                last_play = None
                log += "RESET\n"
                curr_turn = last_player
                while won_dict[curr_turn] is not None:
                    curr_turn = (curr_turn + 1) % 4
                last_player = None
            else:
                for i in range(0, 3):
                    curr_turn = (curr_turn + 1) % 4
                    if (won_dict[curr_turn] is None and pass_dict[curr_turn] is False):
                        break
        return(won_dict[orig_player])