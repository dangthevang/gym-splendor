from ..base.player import Player
import random
import math
import json
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        stocks = ['red']
        print(self.NL_board(state))
        print(self.score)
        return stocks, card, stock_return

    def NL_board(self, state):
        board = state['Board']
        list_card_open = []
        list_score = [player.score for player in state['Player']]
        
        for i in board.dict_Card_Stocks_Show.keys():
            for j in board.dict_Card_Stocks_Show[i]:
                list_card_open.append((convert_card_to_id(j.id)))
        list_all_card = []
        list_player_card = [convert_card_to_id(card.id) for card in self.card_open]
        list_player_noble = [convert_card_to_id(card.id) for card in self.card_noble]
        list_player_upside_down = [convert_card_to_id(card.id) for card in self.card_upside_down]
        list_player_card_test = [card.id for card in self.card_open]

        list_card_check = []
        for player in state['Player']:
            for card in player.card_open:
                if convert_card_to_id(card.id) <= 40:
                    list_card_check.append(card.id)

        # print('CHECK', len(list_card_check),list_player_card, list_player_noble, list_player_card_test)
        for i in range(1, 101):
            if i in list_card_open:
                list_all_card.append(1)
            elif i in list_player_card or i in list_player_noble:
                list_all_card.append(2)
            elif i in list_player_upside_down:
                list_all_card.append(3)
            else:
                list_all_card.append(0)

        list_ = ['-'.join(str(i) for i in list_score) +'/'+
                '-'.join(str(i) for i in list(board.stocks.values())) +'/'+
                '-'.join(str(i) for i in list(self.stocks.values())) +'/'+
                '-'.join(str(i) for i in list(self.stocks_const.values())) +'/'+
                '-'.join(str(i) for i in list_all_card)]

        return list_


def convert_card_to_id(id):
    if 'Noble_' in id:
        return int(id.replace('Noble_', '')) + 90
    elif 'III_' in id:
        return int(id.replace('III_', '')) + 70
    elif 'II_' in id:
        return int(id.replace('II_', '')) + 40
    elif 'I_' in id:
        return int(id.replace('I_', ''))