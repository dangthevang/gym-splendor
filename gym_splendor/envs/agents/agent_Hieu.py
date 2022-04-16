from ..base.player import Player
import random
import math
import json
import os
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


class Agent(Player):
    def __init__(self, name):
        try:
            os.mkdir('./TRAIN_HIEU')

        except:
            pass
        super().__init__(name)



    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        print(self.NL_board(state))
        # self.check_winner(state)
        
        card = self.Checklatthe(state["Board"])
        nlnhamtoi = list(self.check_board_nl(state["Board"]).keys())
        if card != None:
            return stocks,card,stock_return
        if len(nlnhamtoi) >= 3:
            stocks = nlnhamtoi[:3]
        stock_return = list(self.TimNguyenLieuTra(stocks))

        return stocks, card, stock_return
    
    def board_nl(self,board):
        x = board.stocks
        y = self.stocks_const
        x.pop("auto_color")
        dic_nl = {}
        for i in x.keys():
            nl = x[i] - y[i]
            dic_nl[i] = nl
        dict_nl = {k: v for k, v in sorted(
            dic_nl.items(), key=lambda item: item[1], reverse=True)}
        return dict_nl
    
    def check_board_nl(self,board):
        dict_check_nl = {}
        for i in self.board_nl(board):
            if self.board_nl(board)[i] > 0:
                dict_check_nl[i] = self.board_nl(board)[i]
        return dict_check_nl

    def Checklatthe(self,board):
        list_card = []
        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != "Noble":
                for card in board.dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        list_card.append(card)
        ti_so = []
        for i in list_card:
            x = i.score
            y = sum(list(i.stocks.values()))
            dinh_gia = x/y
            ti_so.append(dinh_gia)
        dinh_gia_max = 0
        for i in ti_so:
            if dinh_gia_max < i:
                dinh_gia_max = i
        for i in range(len(ti_so)):
            if ti_so[i] == dinh_gia_max:
                return list_card[i]
    
    def TimNguyenLieuTra(self,arr):
        dict_hien_tai = self.stocks.copy()
        for i in arr:
            dict_hien_tai[i] += 1
        snl = sum(list(dict_hien_tai.values()))
        dict_tra = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "white": 0,
            "black": 0,
            "auto_color": 0,
        }
        if snl <= 10:
            return dict_tra
        else:
            for i in range(snl - 10):
                x = self.NLTTvaNLC(self.stocks_const, dict_hien_tai)
                dict_hien_tai[x] -= 1
                dict_tra[x] += 1
        for key,value in dict_tra.items():
            for i in range(value):
                yield key

    def NLTTvaNLC(self,const_stock, stock):
        x = const_stock
        y = stock
        dict_nl_can_bo = {}
        for i in x.keys():
            if y[i] > 0:
                nl_can_bo = x[i] - y[i]
            else:
                nl_can_bo = -10
            dict_nl_can_bo[i] = nl_can_bo
        dict_nl_can_bo = {k: v for k, v in sorted(
            dict_nl_can_bo.items(), key=lambda item: item[1], reverse=True)}
        return list(dict_nl_can_bo.keys())[0]   

    def NL_board(self, state):
        board = state['Board']
        list_ = ['-'.join(str(i) for i in list(board.stocks.values())) +'/'+
                '-'.join(str(i) for i in list(self.stocks.values())) +'/'+
                '-'.join(str(i) for i in list(self.stocks_const.values())) +'/'+
                self.board_card_to_str(state)]
                #  + self_card_to_str(self)
        return list_


    def board_card_to_str(self, state):
        list_card_open = []
        for i in state['Board'].dict_Card_Stocks_Show.keys():
            for j in state['Board'].dict_Card_Stocks_Show[i]:
                list_card_open.append((convert_card_to_id(j.id)))
        list_card = []
        for i in range(1, 101):
            if i in list_card_open:
                list_card.append(1)
            elif i in self.card_open or i in self.card_noble:
                list_card.append(2)
            elif i in self.card_upside_down:
                list_card.append(3)
            else:
                list_card.append(0)
        return '-'.join(str(i) for i in list_card)
    
    # def check_winner(self, state):
    #     name = ''
    #     score_max = 14
    #     player_win = None
    #     if state['Turn']%4 == 0:
    #         for player in list(state['Player']):
    #             if player.score > score_max:
    #                 score_max = player.score 
    #         if score_max > 14:

    #             for player in list(state['Player']):
    #                 if player.score >= score_max:
    #                     score_max = player.score 
    #                     player_win = player
    #                 elif player.score == score_max:
    #                     if len(player.card_open) < len(player_win.card_open):
    #                         player_win = player
    #             if score_max > 14:
    #                 print('Tap trung vao day nao')
    #                 print(player_win.name, 'win với ', score_max, 'ở turn ',  state['Turn']/4)


            




def convert_card_to_id(id):
    if 'Noble_' in id:
        return int(id.replace('Noble_', '')) + 90
    elif 'III_' in id:
        return int(id.replace('III_', '')) + 70
    elif 'II_' in id:
        return int(id.replace('II_', '')) + 40
    elif 'I_' in id:
        return int(id.replace('I_', ''))


# def self_card_to_str(self):
#     list_card_open = []
#     list_card_upsidedown = []
#     loaithe = ['I', 'II', 'III', 'Noble']
#     for i in loaithe:
#         for j in self.card_open + self.card_upside_down + self.card_noble:
#             list_card_open.append((convert_card_to_id(j.id)))
#         for j in self.card_upside_down:
#             list_card_upsidedown.append((convert_card_to_id(j.id)))
#     list_card = []
#     list_card_down = []
#     for i in range(1, 101):
#         if i not in list_card_open:
#             list_card.append(0)
#         else:
#             list_card.append(1)
#     for i in range(1, 101):
#         if i not in list_card_open:
#             list_card_down.append(0)
#         else:
#             list_card_down.append(1)
#     return ['-'.join(str(i) for i in list_card)] + ['-'.join(str(i) for i in list_card_down)]