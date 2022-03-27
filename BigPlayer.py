from Player import Player

class BigPlayer(Player):
    def action(self, gamestate):
        possible_actions = self.action_list(gamestate)
        return(possible_actions[-1])