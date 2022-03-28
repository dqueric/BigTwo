from Players.Player import Player
from Players.RandomPlayer import RandomPlayer
from GameState import GameState
import numpy as np
from Deck import Deck

def game_over(won_dict):
    return(sum([i is not None for i in won_dict]) == 4)

def pass_reset_check(pass_dict, won_dict):
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
    return(total_count - pass_count == 1, in_player)

class MontePlayer(Player):
    def __init__(self):
        pass

    def action(self, gamestate):
        possible_actions = self.action_list(gamestate)
        action_score = []
        for action in possible_actions:
            action_score.append(0)
            for sample in range(100):
                action_score[-1] += self.simulate(gamestate, action)
        
        return(possible_actions[np.argmax(action_score)])

    def simulate(self, gamestate, action):
        orig_player = gamestate.curr_turn
        last_play = gamestate.last_play
        pass_dict = gamestate.pass_dict
        hand_dict = gamestate.hand_dict
        played_cards = gamestate.played_cards
        won_dict = gamestate.won_dict
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
                hand_list.append(gamestate.hand)
            else:
                hand_list.append(deck.deck[:hand_dict[i]])
                deck.deck = deck.deck[hand_dict[i]:]

        first_turn = True
        while not game_over(won_dict):
            gamestate = GameState(hand_list[curr_turn], last_play, pass_dict, hand_dict, played_cards, won_dict, curr_turn, log)
            if not first_turn:
                action = player_list[curr_turn].action(gamestate)
            else:
                first_turn = False
            if action == "PASS":
                pass_dict[curr_turn] = True
                log += "PLAYER " + str(curr_turn) + ": " + "Passed\n"
            else:
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
            for i in range(0, 4):
                curr_turn = (curr_turn + 1) % 4
                reset_check = pass_reset_check(pass_dict, won_dict)
                if reset_check[0]:
                    pass_dict = [False, False, False, False]
                    last_play = None
                    log += "RESET\n"
                    curr_turn = reset_check[1]
                    break
                if (won_dict[curr_turn] is None and pass_dict[curr_turn] is False):
                    break
        return(won_dict[orig_player])