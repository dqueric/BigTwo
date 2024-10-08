from Deck import Deck
from Players.Player import Player
from Players.SmallPlayer import SmallPlayer
from Players.BigPlayer import BigPlayer
from Players.RandomPlayer import RandomPlayer
from Players.HumanPlayer import HumanPlayer
from Players.MontePlayer import MontePlayer
from Hand import Hand
from GameState import GameState


class Game:
    def __init__(self, player_list):
        self.player_list = player_list

    def game_over(self):
        return(sum([i is not None for i in self.won_dict]) == 4)

    def pass_reset_check(self):
        pass_count = 0
        total_count = 0
        in_player = None
        for i in range(len(self.won_dict)):
            if self.won_dict[i] is None:
                total_count += 1
                if self.pass_dict[i] is True:
                    pass_count += 1
                else:
                    in_player = i
        return((total_count - pass_count == 1 and self.last_player == in_player) or (total_count == pass_count and self.won_dict[self.last_player] is not None))

    def play_game(self):
        deck = Deck()
        deck.shuffle()
        self.played_cards = []
        self.hand_list = []
        self.log = ""
        for i in range(len(self.player_list)):
            self.hand_list.append(Hand(deck.deck[i*13:(i+1)*13]))
        for i in range(len(self.hand_list)):
            if self.hand_list[i].hand[0].card_value == 12:
                self.curr_turn = i

        self.placement = 1
        self.pass_dict = [False, False, False, False]
        self.hand_dict = {0: 13, 1: 13, 2: 13, 3:13}
        self.won_dict = [None, None, None, None]
        self.played_cards = []
        self.last_play = None
        self.last_player = None
        while True:
            gamestate = GameState(self.hand_list[self.curr_turn], self.last_play, self.last_player, self.pass_dict, self.hand_dict, self.played_cards, self.won_dict, self.curr_turn, self.log)
            action = self.player_list[self.curr_turn].action(gamestate)
            if action == "PASS":
                self.pass_dict[self.curr_turn] = True
                self.log += "PLAYER " + str(self.curr_turn) + ": " + "Passed\n"
            else:
                self.last_player = self.curr_turn
                self.log += "PLAYER " + str(self.curr_turn) + ": " + str((action[0], [i.rank + i.suit for i in action[1]])) + "\n"
                self.last_play = action
                self.hand_dict[self.curr_turn] -= len(action[1])
                self.played_cards += list(action[1])
                for card in action[1]:
                    self.hand_list[self.curr_turn].play_card(card)
                if self.hand_dict[self.curr_turn] == 0:
                    self.won_dict[self.curr_turn] = self.placement
                    self.log += "PLAYER " + str(self.curr_turn) + " Placement: " + str(self.placement) + "\n"
                    self.placement += 1
                    if self.placement == 4:
                        for i in range(4):
                            if self.won_dict[i] is None:
                                self.won_dict[i] = 4
                                self.log += "PLAYER " + str(i) + " Placement: " + str(self.placement) + "\n"
                                break
                if self.game_over():
                    break
            reset_check = self.pass_reset_check()
            if reset_check:
                self.pass_dict = [False, False, False, False]
                self.last_play = None
                self.log += "RESET\n"
                self.curr_turn = self.last_player
                while self.won_dict[self.curr_turn] is not None:
                    self.curr_turn = (self.curr_turn + 1) % 4
                self.last_player = None
            else:
                for i in range(0, 3):
                    self.curr_turn = (self.curr_turn + 1) % 4
                    if (self.won_dict[self.curr_turn] is None and self.pass_dict[self.curr_turn] is False):
                        break
        return(self.won_dict)

if __name__ == '__main__':
    player_list = [HumanPlayer()] + [MontePlayer() for i in range(3)]
    game = Game(player_list)
    game.play_game()
