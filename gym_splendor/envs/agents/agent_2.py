from ..base.player import Player
import random
import math
import json
import numpy as np
import itertools
import pandas as pd
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    def Value_function(self, state_player):
        D = state_player[1]
        T = state_player[0]
        Sd = state_player[3][0]
        Sb =state_player[3][1]
        Sg = state_player[3][2]
        Sw =state_player[3][3]
        Sbl =state_player[3][4]
        Sa =state_player[3][5]

        Scd = state_player[4][0]
        Scb =state_player[4][1]
        Scg = state_player[4][2]
        Scw =state_player[4][3]
        Scbl =state_player[4][4]
        Sca =state_player[4][5]
        ct = np.nan_to_num(eval(pd.read_csv('ct.csv')['ct'].iloc[0]))
        return ct
    def act_to_values(self, state_player, list_act_can):
        list_values = []
        if len(list_act_can) > 0:
            for act in list_act_can:
                state_player_tam = np.array(state_player)
                if type(act) != type([]):
                    stocks = []
                    card_get = act
                    state_player_tam[0] += act.score
                    state_player_tam[2] += np.array(list(act.stocks.values())+[0])
                    state_player_tam[3] -= np.array(list(act.stocks.values())+[0])
                    state_player_tam[4] += np.array((dich_arr([act.type_stock])[0]))
                    list_values.append(self.Value_function(state_player_tam))
                else:
                    stocks = np.array(dich_arr(act)[0])
                    stock_return = np.array(dich_arr(act)[1])
                    if len(stock_return) == 0:
                        stock_return = np.array([0,0,0,0,0,0])
                    if len(stock_return) == 0:
                        state_player_tam[2] -= stocks
                        state_player_tam[3] += stocks
                    else:
                        state_player_tam[2] -= (stocks - stock_return)
                        state_player_tam[3] += (stocks - stock_return)
                    list_values.append(self.Value_function(state_player_tam))
        if len(list_values) == 0:
            act_save = [[], [], []]
            return [], None, [], act_save
        act = list_act_can[list_values.index(max(list_values))]
        # print(act)
        if type(act) != type([]):
            act_save = [[], [act.score, list(act.stocks.values()), act.type_stock], []]
            return [], act, [], act_save
        else:
            act_save = [act[0], [], act[1]]
            return act[0], None, act[1], act_save
    def action(self, state):
        stocks = []
        card_get = None
        stock_return = []

        state_player = self.NL_board(state)
        # print(state_player)
        NL_board = np.array(state_player[2])
        NL = np.array(state_player[3])
        NL_count = np.array(state_player[4])
        state_card = state_player[5]

        list_act_can = []

        for type_card in state['Board'].dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    # print(card.type_stock)
                    card_st = np.array(list(card.stocks.values())+[0])
                    if min(NL + NL_count - card_st) >= 0:
                        list_act_can.append(card)
        
        board_materials = []
        hand_materials = []
        for nl in self.stocks.keys():
            if nl != "auto_color" and self.stocks[nl] > 0:
                hand_materials.append(nl)
        for nl in state["Board"].stocks.keys():
            if nl != "auto_color" and state["Board"].stocks[nl] > 0:
                board_materials.append(nl)
        list_act_can += get_st(board_materials, hand_materials, self.stocks)

        stocks, card_get, stock_return, act_save = self.act_to_values(state_player, list_act_can)
        # if card_get == 'None':
        #     card_get = None
        try:
            state_luu = pd.read_csv('State_tam_2.csv')
        except:
            state_luu = [state_player, act_save, np.nan]
        state_luu.loc[len(state_luu.index)] = [state_player, act_save, np.nan]
        state_luu.to_csv('State_tam_2.csv', index = False)
        return stocks, card_get, stock_return

    def NL_board(self, state):
        board = state['Board']
        list_card_open = []
        
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

        for i in range(1, 101):
            if i in list_card_open:
                list_all_card.append(1)
            elif i in list_player_card or i in list_player_noble:
                list_all_card.append(2)
            elif i in list_player_upside_down:
                list_all_card.append(3)
            else:
                list_all_card.append(0)

        list_ = [(int(state['Turn']/4)),
                int(self.score),
                list(board.stocks.values()),
                list(self.stocks.values()),
                list(self.stocks_const.values())+[0],
                list_all_card]
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

def dich_arr(arr):
    cl = ['red', 'blue', 'green', 'white', 'black', 'auto_color']
    str_stock = []
    if len(arr) >1:
        for i in arr:
            stock = [0,0,0,0,0,0]
            for sl in i:
                stock[cl.index(sl)] += 1
            str_stock.append(stock)
    else:
        stock = [0,0,0,0,0,0]
        for sl in arr:
            stock[cl.index(sl)] += 1
            str_stock.append(stock)
    return str_stock

def get_st(board_materials, hand_materials, NL):
    list_ = []
    stock_return = []
    for lay in range(1, 4):
        sonl = sum(NL.values()) + lay - 10
        if sonl <= 0:
            st_return = []
        else:
            st_return = [' '.join(i).split(' ') for i in itertools.combinations(hand_materials, sonl)]
        st_give = [' '.join(i).split(' ') for i in itertools.combinations(board_materials, lay)]
        for i in st_give:
            if st_return == []:
                hi = [i, []]
                list_.append(hi)
            for j in st_return:
                hi = [i, j]
                list_.append(hi)
    list2 = []
    if len(list_)> 0:
        for i in range(len(list_)):
            if list_[i][0] != list_[i][1]:
                list2.append(list_[i])
    return list_

