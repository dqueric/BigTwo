from Players.Player import Player

class BigPlayer(Player):
    def __init__(self):
        pass

    def action(self, gamestate):
        possible_actions = self.action_list(gamestate)
        return(possible_actions[-1])