from ..base.player import Player
import random
import math
import json
#format state:
# 0 Nguyên liệu trên bàn
# 1 Nguyên liệu đang có
# 2 Nguyên liệu count đang có
# 3 thẻ trên bàn: 
#     0: thẻ upsidown, 
#     1: card_open,
# 4 thẻ mo trong tay
#     0: card_have
#     1: card_dont_have
# 5 the up trong tay:
#     0: card_have
#     1: card_dont_have
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
        list_ = ['-'.join(str(i) for i in list(board.stocks.values())),
                '-'.join(str(i) for i in list(self.stocks.values())),
                '-'.join(str(i) for i in list(self.stocks_const.values())),
                board_card_to_str(state)] + self_card_to_str(self)
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
def board_card_to_str(state):
    list_card_open = []
    for i in state['Board'].dict_Card_Stocks_Show.keys():
        for j in state['Board'].dict_Card_Stocks_Show[i]:
            list_card_open.append((convert_card_to_id(j.id)))
    list_card = []
    for i in range(1, 101):
        if i not in list_card_open:
            list_card.append(0)
        else:
            list_card.append(1)
    return '-'.join(str(i) for i in list_card)

def self_card_to_str(self):
    list_card_open = []
    list_card_upsidedown = []
    loaithe = ['I', 'II', 'III', 'Noble']
    for i in loaithe:
        for j in self.card_open + self.card_upside_down + self.card_noble:
            list_card_open.append((convert_card_to_id(j.id)))
        for j in self.card_upside_down:
            list_card_upsidedown.append((convert_card_to_id(j.id)))
    list_card = []
    list_card_down = []
    for i in range(1, 101):
        if i not in list_card_open:
            list_card.append(0)
        else:
            list_card.append(1)
    for i in range(1, 101):
        if i not in list_card_open:
            list_card_down.append(0)
        else:
            list_card_down.append(1)
    return ['-'.join(str(i) for i in list_card)] + ['-'.join(str(i) for i in list_card_down)]