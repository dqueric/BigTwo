class GameState:
    def __init__(self, hand, last_play, pass_dict, hand_dict, played_cards, won_dict, curr_turn):
        self.hand = hand
        self.last_play = last_play
        self.pass_dict = pass_dict
        self.hand_dict = hand_dict
        self.played_cards = played_cards
        self.won_dict = won_dict
        self.curr_turn = curr_turn