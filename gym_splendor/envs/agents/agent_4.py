from ..base.player import Player
import random
import math
import json
import numpy as np
import itertools
import pandas as pd
import ast
import random
import os

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    def act_to_values(self, list_act_can):
        if len(list_act_can) == 0:
            act_save = [[], [], []]
            return [], None, [], act_save
        act = random.choice(list_act_can)
        if len(act[1]) != 0 :
            act_save = [[], [act[1][0].id], act[2]]
            return [], act[1][0], act[2], act_save
        else:
            act_save = [act[0], [], act[1]]
            return act[0], None, act[1], act_save
    def action(self, state):
        state_player = self.NL_board(state)
        NL = np.array(state_player[3])
        NL_count = np.array(state_player[4])

        list_act_can = []
        list_act_up = []
        for card in self.card_upside_down:
            card_st = np.array(list(card.stocks.values())+[0])
            yellow_need = 0
            NL_can = NL + NL_count - card_st
            for yellow in NL_can:
                if yellow < 0:
                    yellow_need -= yellow
            if NL[5] >= yellow_need:
                list_act_can.append([[], [card], []])
        for type_card in state['Board'].dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    card_st = np.array(list(card.stocks.values())+[0])
                    yellow_need = 0
                    NL_can = NL + NL_count - card_st
                    for yellow in NL_can:
                        if yellow < 0:
                            yellow_need -= yellow
                    if NL[5] >= yellow_need:
                        list_act_can.append([[], [card], []])
                    else:
                        list_act_up.append(card)
        board_materials = []
        hand_materials = []
        for nl in self.stocks.keys():
            if nl != "auto_color" and self.stocks[nl] > 0:
                hand_materials.append(nl)
            if nl != "auto_color" and state["Board"].stocks[nl] > 0:
                board_materials.append(nl)
        list_act_can += get_st(state['Board'].stocks, board_materials, hand_materials, self.stocks)
        if len(self.card_upside_down) <3:
            list_act_can += get_usd(list_act_up, self.stocks, hand_materials)
        stocks, card_get, stock_return, act_save = self.act_to_values(list_act_can)
        act_save_index = ast.literal_eval(pd.read_csv('data_act.csv')['action'].iloc[0]).index(act_save)
        try:
            state_luu = pd.read_csv('State_tam_4.csv')
        except:
            state_luu = [state_player, act_save_index, np.nan]
        state_luu.loc[len(state_luu.index)] = [state_player, act_save_index, np.nan]
        state_luu.to_csv('State_tam_4.csv', index = False)

        if (os.path.exists('model_1.h5') == True):
            from keras.models import load_model
            action_id = pred(state_player, act_save)
            action = ast.literal_eval(pd.read_csv('data_act.csv')['action'].iloc[0])[action_id]
            if len(action[1]) > 0:
                for type_card in state["Board"].dict_Card_Stocks_Show.keys():
                    for card in state["Board"].dict_Card_Stocks_Show[type_card]:
                        if card.id == action[1][0]:
                            card_get = card
                for card in self.card_upside_down:
                    if card.id == action[1][0]:
                        card_get = card
            else:
                card_get = None
            return action[0], card_get, action[2]
        else:
            return stocks, card_get, stock_return

    def NL_board(self, state):
        board = state['Board']
        list_card_open = []
        list_all_card = []
        list_all_card_2 = []
        
        for i in board.dict_Card_Stocks_Show.keys():
            for j in board.dict_Card_Stocks_Show[i]:
                list_card_open.append((convert_card_to_id(j.id)))
        list_player_upside_down = [convert_card_to_id(card.id) for card in self.card_upside_down]

        for i in range(1, 101):
            if i in list_card_open:
                list_all_card.append(1)
            else:
                list_all_card.append(0)
            if i in list_player_upside_down:
                list_all_card_2.append(1)
            else:
                list_all_card_2.append(0)

        list_ = [(int(state['Turn']/4)+1),
                int(self.score),
                list(board.stocks.values()),
                list(self.stocks.values()),
                list(self.stocks_const.values())+[0],
                list_all_card, 
                list_all_card_2]
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

def get_st(NL_board, board_materials, hand_materials, NL):
    list_ = []
    stock_return = []
    for lay in range(1, 4):
        sonl = sum(NL.values()) + lay - 10
        if sonl <= 0:
            st_return = []
        else:
            st_return = [' '.join(i).split(' ') for i in itertools.product(hand_materials, repeat =sonl)]
        st_give = [' '.join(i).split(' ') for i in itertools.combinations(board_materials, lay)]
        if lay == 2:
            for cl in board_materials:
                if NL_board[cl] >=4:
                    st_give.append([cl, cl])
        for i in st_give:
            if st_return == []:
                hi = [i, []]
                list_.append(hi)
            else:
                for j in st_return:
                    # print(i, j)
                    check = True
                    for cl_rt in j:
                        if cl_rt in i:
                            check = False
                    if check == True:
                        hi = [i, j]
                        list_.append(hi)
    list2 = []
    if len(list_)> 0:
        for i in range(len(list_)):
            if list_[i][0] != list_[i][1]:
                list2.append(list_[i])
    list_save = []
    for i2 in list2:
        list_save += [[i2[0], [], i2[1]]]
    return list_save

def get_usd(list_act_up, NL, hand_materials):
    list_act = []
    for act in list_act_up:
        if sum(NL.values()) == 10:
            for cl in hand_materials:
                list_act.append([[], [act], [cl]])
        else:
            list_act.append([[], [act], []])
    return list_act


def prepar_data(df):
    df_state1 = df.copy()
    df_state1 = df_state1.astype(str)

    df_state1["state"] = df_state1["state"].apply(lambda x: x.replace("], [", ","))
    df_state1["state"] = df_state1["state"].apply(lambda x: x.replace(", [" , ","))
    df_state1["state"] = df_state1["state"].apply(lambda x: x.replace("["   ,""))
    df_state1["state"] = df_state1["state"].apply(lambda x: x.replace("]]"  , ""))
    df_state1 = df_state1["state"].str.split(pat=',',expand=True).astype(int)

    return df_state1

def pred(state_player, act_save):
    act_save_index = ast.literal_eval(pd.read_csv('data_act.csv')['action'].iloc[0]).index(act_save)
    df_act = pd.DataFrame({'state':[]})
    df_act.loc[len(df_act.index)] = [state_player]
    new_df = prepar_data(df_act)
    num_classes = 951
    labels = [int(i) for i in range(num_classes)]
    x_test = new_df
    model= load_model('model_1.h5')
    y_predict = model.predict(x_test)
    action = labels[np.argmax(y_predict)]
    return action