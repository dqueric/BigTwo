from GameState import GameState

class Player:
    def __init__(self, deck):
        self.deck = deck
        self.log = ""

    def action_list(self, gamestate):
        hand = gamestate.hand
        last_play = gamestate.last_play
        if len(gamestate.played_cards) == 0:
            possible_actions = []
            for i in hand.plays:
                for play in hand.plays[i]:
                    if hand.deck.start_card in play[1]:
                        possible_actions.append(play)
        else:
            if last_play == None:
                possible_actions = []
                for i in hand.plays:
                    for play in hand.plays[i]:
                        possible_actions.append(play)
            else:
                possible_actions = ["PASS"]
                for play in hand.plays[len(last_play[1])]:
                    if play[0] > last_play[0]:
                        possible_actions.append(play)
        return(possible_actions)

    def action(self, gamestate):
        pass