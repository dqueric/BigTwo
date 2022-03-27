from re import L
from Deck import Deck
from Player import Player
from Hand import Hand
from GameState import GameState

class Game:
    def __init__(self, player_list):
        self.player_list = player_list

    def game_over(self):
        return(sum([i is not None for i in self.won_dict]) == 4)

    def pass_reset_check(self):
        count = 0
        for i in range(len(self.won_dict)):
            if self.won_dict[i] is None and self.pass_dict[i] is False:
                count += 1
        return(count == 1)

    def play_game(self):
        deck = Deck()
        self.played_cards = []
        self.hand_list = []
        print("START GAME")
        for i in range(len(self.player_list)):
            self.hand_list.append(Hand(deck.deck[i*13:(i+1)*13]))
            print("PLAYER " + str(i) + ": " + str([i.rank + i.suit for i in self.hand_list[i].hand]), len(self.hand_list[i].hand))
        for i in range(len(self.hand_list)):
            if self.hand_list[i].hand[0].card_value == 12:
                self.curr_turn = i

        self.placement = 1
        self.pass_dict = [False, False, False, False]
        self.hand_dict = {0: 13, 1: 13, 2: 13, 3:13}
        self.won_dict = [None, None, None, None]
        self.played_cards = []
        self.last_play = None

        while not self.game_over():
            gamestate = GameState(self.hand_list[self.curr_turn], self.last_play, self.pass_dict, self.hand_dict, self.played_cards, self.won_dict, self.curr_turn)
            action = self.player_list[self.curr_turn].action(gamestate)
            if action == "PASS":
                self.pass_dict[self.curr_turn] = True
                print("PLAYER " + str(self.curr_turn) + ": " + "Passed")
            else:
                print("PLAYER " + str(self.curr_turn) + ": " + str((action[0], [i.rank + i.suit for i in action[1]])))
                self.last_play = action
                self.hand_dict[self.curr_turn] -= len(action[1])
                self.played_cards += list(action[1])
                for card in action[1]:
                    self.hand_list[self.curr_turn].play_card(card)
                if self.hand_dict[self.curr_turn] == 0:
                    self.won_dict[self.curr_turn] = self.placement
                    print("PLAYER " + str(self.curr_turn) + " Placement: " + str(self.placement))
                    self.placement += 1
                    if self.placement == 4:
                        for i in range(4):
                            if self.won_dict[i] is None:
                                self.won_dict[i] = 4
                                print("PLAYER " + str(i) + " Placement: " + str(self.placement))
                                break
            for i in range(0, 4):
                self.curr_turn = (self.curr_turn + 1) % 4
                if i == 3:
                    self.pass_dict = [False, False, False, False]
                    self.last_play = None
                    print("RESET")
                if (self.won_dict[self.curr_turn] is None and self.pass_dict[self.curr_turn] is False):
                    break
        print(self.won_dict)
        return(self.won_dict)

if __name__ == '__main__':
    player_list = [Player() for i in range(4)]
    game = Game(player_list)
    game.play_game()
