from GameState import GameState

class Player:
    def __init__(self):
        pass

    def action_list(self, gamestate):
        hand = gamestate.hand
        last_play = gamestate.last_play
        pass_dict = gamestate.pass_dict
        hand_dict = gamestate.hand_dict
        won_dict = gamestate.won_dict
        curr_turn = gamestate.curr_turn
        played_cards = gamestate.played_cards
        if len(gamestate.played_cards) == 0:
            possible_actions = []
            for i in hand.plays:
                for play in hand.plays[i]:
                    for card in play[1]:
                        if card.rank + card.suit == "3D":
                            possible_actions.append(play)
                            break
        else:
            possible_actions = ["PASS"]
            if last_play == None:
                for i in hand.plays:
                    for play in hand.plays[i]:
                        possible_actions.append(play)
            else:
                for play in hand.plays[len(last_play[1])]:
                    if play[0] > last_play[0]:
                        possible_actions.append(play)
        return(possible_actions)

    def action(self, gamestate):
        possible_actions = self.action_list(gamestate)
        return(possible_actions[-1])