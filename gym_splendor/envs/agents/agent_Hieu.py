from ..base.player import Player
import random
import math
import json
import pandas as pd
import os
import itertools
'''
format state:
0 Scores
1 board.stock
2 player.stock
3 player.stock_const
4 list_card:
    -chưa xuất hiện: 0
    -trên bàn chơi: 1
    -mình đã lấy: 2
    -mình đang úp: 3
'''
file_train = pd.read_csv('./TRAIN_HIEU/file_train.csv')


class Agent(Player):

    def __init__(self, name):
        self.file_train = file_train
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        print(self.str_state(state))
        list_action_possible = self.action_possible(state)
        print('ALL ACTION', list_action_possible)
        
        
        id = random.randint(0, len(list_action_possible) -1)
        action = list(list_action_possible[id])
        action[0]  = []
        print("TOANG", action[0], action[1], action[2])
        return action[0], action[1], action[2]
        return stocks, card, stock_return

    def action_possible(self, state):
        list_all_action = list(file_train['action'])
        list_check = [False]*len(file_train)
        board = state['Board']
        card_can_get = self.list_card_can_buy(board)
        card_can_action = [convert_card_to_id(card.id) for card in
                     board.dict_Card_Stocks_Show['I'] +
                     board.dict_Card_Stocks_Show['II']
                     + board.dict_Card_Stocks_Show['III']
                     + self.card_upside_down]
        card_upside_down = [convert_card_to_id(card.id) for card in self.card_upside_down]
        stock_2_get, stock_3_get = self.stock_board(board)
        card_can_action_other = []
        card_check = card_upside_down + card_can_get
        
        for card in card_can_action:
            if card not in card_check:
                card_can_action_other.append(card)

        list_action = self.create_list_action(stock_2_get, stock_3_get, card_can_get, card_can_action_other)
        list_str_action = [str(item) for item in list_action]
        for i in range(len(list_all_action)):
            if list_all_action[i] in list_str_action:
                list_check[i] = True
        file_train['CHECK'] = list_check
        df = file_train[file_train['CHECK'] == True].reset_index(drop=True)
  
        
        return list_action

    def reference_file(self, state):
        list_stock = ['red', 'blue', 'green', 'white', 'black', 'auto_color']
        list_columns_reference = []
        list_str_state = [item.split('-') for item in self.str_state(state).split('/')]
        for id in range(len(list_str_state[1])):
            list_columns_reference.append(f'{int(list_str_state[id])}_{list_stock[id]}_board')
        for id in range(len(list_str_state[2])):
            list_columns_reference.append(f'{int(list_str_state[id])}_{list_stock[id]}_player')
        for id in range(len(list_str_state[3])):
            list_columns_reference.append(f'{int(list_str_state[id])}_{list_stock[id]}_const')
        for id in range(len(list_str_state[4])):
            if int(list_str_state[id]) != 0:
                list_columns_reference.append(f'card_{id+1}_Y')
        return list_columns_reference




    def create_list_action(self, stock_2_get, stock_3_get, card_can_get, card_can_action_other):
        #get_stock
        get_3 = list(itertools.combinations(stock_3_get,3))          
        get_2 = [(i,i) for i in stock_2_get]                         
        #stock return
        stock_return_1, stock_return_2, stock_return_3 = self.stock_player()
        return_3 = list(itertools.combinations_with_replacement(stock_return_3,3))
        return_2 = list(itertools.combinations_with_replacement(stock_return_2,2))
        return_1 = stock_return_1
        #card
        list_action = []
        for get in get_3:
            for return_stock in return_3 + return_2 + return_1:
                list_action.append((get, None, return_stock))       #lấy 2 stock trả lại stock dư
        for get in get_2:
            for return_stock in return_2 + return_1:
                list_action.append((get, None, return_stock))       #lấy 2 stock trả lại stock dư
        for card in card_can_get:
            list_action.append(([], card, []))                      #lấy thẻ
            for return_stock in return_1:
                list_action.append((['auto_color'], card, [return_stock])) #úp thẻ trả nguyên liệu
        for card in card_can_action_other:
            list_action.append((['auto_color'], card, []))          #úp thẻ
            for return_stock in return_1:
                list_action.append((['auto_color'], card, [return_stock])) #úp thẻ trả nguyên liệu

        return list_action

    
    def str_state(self, state):
        board = state['Board']
        list_card_open = []
        list_score = [player.score for player in state['Player']]

        for i in board.dict_Card_Stocks_Show.keys():
            for j in board.dict_Card_Stocks_Show[i]:
                list_card_open.append((convert_card_to_id(j.id)))
        list_all_card = []
        list_player_card = [convert_card_to_id(
            card.id) for card in self.card_open]
        list_player_noble = [convert_card_to_id(
            card.id) for card in self.card_noble]
        list_player_upside_down = [convert_card_to_id(
            card.id) for card in self.card_upside_down]

        list_card_check = []
        for player in state['Player']:
            for card in player.card_open:
                if convert_card_to_id(card.id) <= 40:
                    list_card_check.append(card.id)
        for i in range(1, 101):
            if i in list_card_open:
                list_all_card.append(1)
            elif i in list_player_card or i in list_player_noble:
                list_all_card.append(2)
            elif i in list_player_upside_down:
                list_all_card.append(3)
            else:
                list_all_card.append(0)
        list_ = ['-'.join(str(i) for i in list_score) + '/' +
                 '-'.join(str(i) for i in list(board.stocks.values())) + '/' +
                 '-'.join(str(i) for i in list(self.stocks.values())) + '/' +
                 '-'.join(str(i) for i in list(self.stocks_const.values())) + '/' +
                 '-'.join(str(i) for i in list_all_card)]
        return list_[0]


    def stock_player(self):
        stock_3 = []
        stock_2 = []
        stock_1 = []
        for stock in self.stocks.keys():
            if self.stocks[stock] > 0:
                stock_1.append(stock)
            elif self.stocks[stock] > 1:
                stock_2.append(stock)
            elif self.stocks[stock] > 2:
                stock_3.append(stock)
        return stock_1, stock_2, stock_3

    def stock_board(self, board):
        stock_3 = []
        stock_2 = []
        for stock in board.stocks.keys():
            if stock != "auto_color":
                if board.stocks[stock] > 0:
                    stock_3.append(stock)
                elif board.stocks[stock] > 3:
                    stock_2.append(stock)
        
        return stock_2, stock_3

    def list_card_can_buy(self, board):
        card_can_get = []
        list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + \
            board.dict_Card_Stocks_Show['III'] + self.card_upside_down
        for card in list_card_show:
            if self.check_get_card(card) == True:
                card_can_get.append(convert_card_to_id(card.id))
        return card_can_get



def convert_card_to_id(id):
    if 'Noble_' in id:
        return int(id.replace('Noble_', '')) + 90
    elif 'III_' in id:
        return int(id.replace('III_', '')) + 70
    elif 'II_' in id:
        return int(id.replace('II_', '')) + 40
    elif 'I_' in id:
        return int(id.replace('I_', ''))
