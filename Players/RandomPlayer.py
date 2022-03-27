from Players.Player import Player
from random import randint
class RandomPlayer(Player):
    def action(self, gamestate):
        possible_actions = self.action_list(gamestate)
        return(possible_actions[randint(0, len(possible_actions) - 1)])