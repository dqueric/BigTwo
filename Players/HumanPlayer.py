from Players.Player import Player

class HumanPlayer(Player):
    def __init__(self):
        self.log = ""

    def action(self, gamestate):
        possible_actions = self.action_list(gamestate)
        print(gamestate.log[len(self.log):])
        self.log = gamestate.log
        print("You are player " + str(gamestate.curr_turn))
        print("Hand sizes: " + str(gamestate.hand_dict))
        filter_pass_dict = {}
        for i in range(len(gamestate.pass_dict)):
            if gamestate.won_dict[i] is None:
                filter_pass_dict[i] = gamestate.pass_dict[i]
        print("Passed: " + str(filter_pass_dict))
        print("Hand: " + str([card.rank + card.suit for card in gamestate.hand.hand]))

        if gamestate.last_play is not None:
            print("Action 0", "PASS")
            for i in range(1, len(possible_actions)):
                print("Action " + str(i), [card.rank + card.suit for card in possible_actions[i][1]])
        else:
            for i in range(len(possible_actions)):
                print("Action " + str(i), [card.rank + card.suit for card in possible_actions[i][1]])
        valid = False
        while not valid:
            try:
                play = int(input("Action number here: "))
                assert(play >= 0 and play < len(possible_actions))
                valid = True
            except:
                print("Action is not valid")
        print("\n")
        return(possible_actions[play])