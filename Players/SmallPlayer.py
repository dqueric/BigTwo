from Players.Player import Player

class SmallPlayer(Player):
    def action(self, gamestate):
        possible_actions = self.action_list(gamestate)
        if len(possible_actions) == 1:
            return(possible_actions[0])
        else:
            return(possible_actions[1])