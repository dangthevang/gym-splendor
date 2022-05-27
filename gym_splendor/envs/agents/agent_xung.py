from ..base.player import Player
from ..base.board import Board
from ..base.card import Card
import random
import math
from collections import Counter
from copy import deepcopy

class Agent(Player, Card, Board):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        # gán
        board = state['Board']
        tn_target_final = self.tai_nguyen_target_func(state['Board'])
        the_lay_ngay = self.dict_card_mua_duoc_luon(board)  # dict
        #print("list the cho khong : ", the_lay_ngay)
        #print(the_lay_ngay.items(), the_lay_ngay.values())
        #chọn thẻ lấy ngay
        mau_the_vinh_vien_da_so_huu = {
            'red': 0, 'blue': 0, 'green': 0, 'white': 0, 'black': 0}
        for mau_the,ds_the in the_lay_ngay.items():
            if mau_the in tn_target_final :
                for car in ds_the:
                    if car.type_stock == mau_the and mau_the_vinh_vien_da_so_huu[mau_the] <=3:
                        card = car
                        mau_the_vinh_vien_da_so_huu[car.type_stock] +=1
                        return [], card,[]

        #tim nguyen lieu tra
        list_co_the_lay = self.card_can_get(state['Board'], tn_target_final)
        if list_co_the_lay.__len__() != 0:
            target = list_co_the_lay[0]
            mau_target_thieu = [mau for mau in target['nl_thieu'].keys() if
                                mau != 'auto_color' and target['nl_thieu'][mau] != 0]
            if mau_target_thieu.__len__() == 1:
                if target['nl_thieu'][mau_target_thieu[0]] >= 2 and state['Board'].stocks[mau_target_thieu[0]] >= 4:
                    stocks = [mau_target_thieu[0], mau_target_thieu[0]]
                    stocks_return = self.stock_return_(target['the'], stocks)
                    nl_trung_nhau = list(set(stocks) & set(stocks_return))
                    for i in nl_trung_nhau:
                        stocks.remove(i)
                        stocks_return.remove(i)
                    return stocks, None, stocks_return
            temp_list_ = []
            for ele in list_co_the_lay:
                for mau in ele['the'].stocks.keys():
                    if ele['nl_thieu'][mau] != 0 and mau not in temp_list_:
                        temp_list_.append(mau)
            if temp_list_.__len__() <= 3:
                stocks = deepcopy(temp_list_)
            else:
                while stocks.__len__() < 3:
                    sdg = random.choice(temp_list_)
                    stocks.append(sdg)
                    temp_list_.remove(sdg)
            if stocks.__len__() == 3:
                stocks_return = self.stock_return_(target['the'], stocks)
                nl_trung_nhau = list(set(stocks) & set(stocks_return))
                for i in nl_trung_nhau:
                    stocks.remove(i)
                    stocks_return.remove(i)
                return stocks, None, stocks_return
            nn = 3 - stocks.__len__()
            for i in range(nn):
                temp_list_mau = [mau for mau in state['Board'].stocks.keys() if
                                 mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
                if temp_list_mau.__len__() != 0:
                    mau_choice = random.choice(temp_list_mau)
                    stocks.append(mau_choice)
            stocks_return = self.stock_return_(target['the'], stocks)
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            return stocks, None, stocks_return
        if (state['Board'].stocks['auto_color'] > 0 and self.card_upside_down.__len__() < 3) or (
            self.card_upside_down.__len__() < 3 and sum(state['Board'].stocks.values()) ==
            state['Board'].stocks['auto_color']):
            card_up = self.find_card_upside_down(state['Board'], tn_target_final)
            if card_up != None:
                stocks_return = []
                if card_up != None:
                    stocks_return = self.stock_return_(card_up, ['auto_color'])
                return [], card_up, stocks_return
        stocks = []
        for i in range(min(3, 10 - sum(self.stocks.values()))):
            temp_list = [mau for mau in state['Board'].stocks.keys() if
                             mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))
        if stocks.__len__() > 0:
            return stocks, None, []
        for i in range(3):
            temp_list = [mau for mau in state['Board'].stocks.keys() if
                        mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))
        stocks_return = []
        nl_thua = max(sum(self.stocks.values()) + stocks.__len__() - 10, 0)
        pl_st = deepcopy(self.stocks)
        for i in range(nl_thua):
            temp_list = [mau for mau in pl_st.keys() if mau != 'auto_color' and pl_st[mau] > 0]
            abc = random.choice(temp_list)
            stocks_return.append(abc)
            pl_st[abc] -= 1
        return stocks, None, stocks_return

    def find_card_upside_down(self, board, color_card_target):
        list_card_check = []
        list_check_1 = []
        list_check_1_ = []
        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for car in board.dict_Card_Stocks_Show[type_card]:
                    if not self.check_get_card(car):
                        list_card_check.append(car)
        if len(color_card_target) > 0:
            for mau in color_card_target[0]:
                for car in list_card_check:
                    if car.type_stock == mau:
                        list_check_1.append(car)
        if len(color_card_target) >2:
            for mau in color_card_target[1]:
                for car in list_card_check:
                    if car.type_stock == mau:
                        list_check_1_.append(car)
        list_check_2 = [car for car in list_card_check if car not in (list_check_1 + list_check_1_)]
        list_check = [list_check_1, list_check_1_, list_check_2]
        for i in range(3):
            if list_check[i].__len__() != 0:
                value_cards = [car.score / sum(list(car.stocks.values())) for car in list_check[i]]
                max_value = max(value_cards)
                card = list_check[i][value_cards.index(max_value)]
                return card
        return None
    def dict_card_mua_duoc_luon(self, board):
        dict_ = {'red': [], 'blue': [], 'green': [], 'white': [], 'black': []}
        for card in self.card_upside_down:
            if self.check_get_card(card):
                dict_[card.type_stock].append(card)
        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in board.dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        dict_[card.type_stock].append(card)
        return dict_
    def tai_nguyen_target_func(self, board):# chưa xét trường hợp cụ thể noble_2_tn rỗng
        # lấy list tài nguyên target cho toàn trận từ hàng noble.
        noble_3_tn_tam = []
        noble_2_tn = {}  # các loại tài nguyên xuất hiện trong thẻ noble chỉ có 2 tài nguyên_và số thẻ mà nó nằm trong
        noble_3_tn = {'red': 0, 'blue': 0, 'green': 0, 'black': 0,
                      'white': 0}  # các loại tài nguyên xuất hiện trong thẻ noble chỉ có 3 tài nguyên
        # số thẻ mà nó nằm trong
        tn_target_final = []  # tài nguyên chọn để build thực sự.

        for type_card in board.dict_Card_Stocks_Show:
            if type_card == 'Noble':
                list_tn_target_ = []
                for card in board.dict_Card_Stocks_Show['Noble']:
                    # tìm các thẻ noble chứa 2 tn build
                    count_card_tn_eval_2 = 0
                    for k in card.stocks.keys():
                        if card.stocks[k] > 0:
                            count_card_tn_eval_2 += 1

                    if count_card_tn_eval_2 == 2:
                        for k in card.stocks.keys():
                            if card.stocks[k] > 0:
                                list_tn_target_.append(k)
                        noble_2_tn = dict((x, list_tn_target_.count(x)) for x in set(list_tn_target_))
                    else:
                        noble_3_tn_tam.append(card.stocks)
                # lưu tất cả loại tài nguyên của thẻ noble có 3 tài nguyên build vào noble_3_tn
                for tn_build_each_card_IV in noble_3_tn_tam:
                    if tn_build_each_card_IV['red'] > 0:
                        noble_3_tn['red'] += 1
                    if tn_build_each_card_IV['blue'] > 0:
                        noble_3_tn['blue'] += 1
                    if tn_build_each_card_IV['green'] > 0:
                        noble_3_tn['green'] += 1
                    if tn_build_each_card_IV['black'] > 0:
                        noble_3_tn['black'] += 1
                    if tn_build_each_card_IV['white'] > 0:
                        noble_3_tn['white'] += 1

                noble_2_tn = dict(sorted(noble_2_tn.items(), key=lambda x: x[1], reverse=True))
                noble_3_tn = dict(sorted(noble_3_tn.items(), key=lambda x: x[1], reverse=True))
                #print("noble_2_tn", noble_2_tn)  # loại thẻ noble chỉ có 2 tài nguyên
                #print("noble_3_tn", noble_3_tn)  # loại thẻ noble chỉ có 3 tài nguyên

                # ưu tiền target tài nguyên theo các thẻ noble chỉ có 2 loại tài nguyên build và có loại tài nguyên xuất hiện trong noble_3_tn

                if len(noble_2_tn) != 0:
                    if len(noble_2_tn) == 2:  # chỉ có 1 thẻ noble 2 tn build
                        for x in noble_2_tn.keys():
                            tn_target_final.append(x)
                    else:  # nếu len(noble_2_tn) > 2, tức có >= 2 thẻ noble 2 tn build
                        # nếu tất cả giá trị = 1 thì xét sang list kia
                        if list(noble_2_tn.values())[0] == 1:  # list chứa toàn value = 1
                            for k in noble_2_tn.keys():
                                if k in noble_3_tn.keys():
                                    if len(tn_target_final) < 3:
                                        tn_target_final.append(k)
                        else:
                            for m in noble_2_tn.keys():
                                if noble_2_tn[m] >= 2 and len(tn_target_final) < 3:
                                    tn_target_final.append(m)
                            if len(tn_target_final) < 3:
                                for k in noble_3_tn.keys():
                                    if k in tn_target_final:
                                        continue
                                    else:
                                        if len(tn_target_final) < 3:
                                            tn_target_final.append(k)
                #print("tn_target_final : ",
                     # tn_target_final)

                ####################cần tối ưu: giả sử noble_2_tn có value= [2,1,1,1]. Sau khi lấy key của value 2
                # ta cần truy cập đến thẻ chứa tài nguyên key=2 để lấy nốt cái tài nguyên còn lại
        return tn_target_final

    def stock_return_(self, card, stocks):
        nl_hien_tai = deepcopy(self.stocks)
        for i in stocks:
            nl_hien_tai[i] += 1
        snl = sum(list(nl_hien_tai.values()))
        if snl <= 10:
            return []
        list_stock_return = []
        nl_thua = snl - 10

        dict_nl_thua_temp = {}
        for mau in card.stocks.keys():
            if nl_hien_tai[mau] + self.stocks_const[mau] > card.stocks[mau]:
                dict_nl_thua_temp[mau] = nl_hien_tai[mau] + self.stocks_const[mau] - card.stocks[mau]
        dict_nl_thua = {k: v for k, v in sorted(dict_nl_thua_temp.items(), key=lambda item: item[1], reverse=True)}
        for i in range(nl_thua):
            for mau in dict_nl_thua.keys():
                if dict_nl_thua[mau] != 0:
                    dict_nl_thua[mau] -= 1
                    nl_hien_tai[mau] -= 1
                    dict_nl_thua_temp = deepcopy(dict_nl_thua)
                    dict_nl_thua = {k: v for k, v in
                                    sorted(dict_nl_thua_temp.items(), key=lambda item: item[1], reverse=True)}
                    list_stock_return.append(mau)
                    break
        if list_stock_return.__len__() != nl_thua:
            nl_hien_tai.pop('auto_color')
            nl_tra_them = nl_thua - list_stock_return.__len__()
            for i in range(nl_tra_them):
                a = max(nl_hien_tai.values())
                for mau in nl_hien_tai.keys():
                    if nl_hien_tai[mau] == a:
                        nl_hien_tai[mau] -= 1
                        list_stock_return.append(mau)
                        break
        return list_stock_return

    def card_can_get(self, board, mau_the_quan_trong):
        card_check = []
        list_check_1 = []
        list_check_1_ = []
        list_thu_nhat = []
        for car in self.card_upside_down:
            if not self.check_get_card(car):
                card_check.append(car)

        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for car in board.dict_Card_Stocks_Show[type_card]:
                    if not self.check_get_card(car):
                        card_check.append(car)
        if len(mau_the_quan_trong) > 0:
            for mau in mau_the_quan_trong[0]:
                for car in card_check:
                    if car.type_stock == mau:
                        list_check_1.append(car)
        if len(mau_the_quan_trong) >2 :
            for mau in mau_the_quan_trong[1]:
                for car in card_check:
                    if car.type_stock == mau:
                        list_check_1_.append(car)
        list_check_2 = [car for car in card_check if car not in (list_check_1 + list_check_1_)]
        temp = ["red", "blue", "green", "white", "black"]
        for car in (list_check_1 + list_check_1_ + list_check_2):
            nl_vc_thieu = {}
            for mau in temp:
                nl_vc_thieu[mau] = max(0, car.stocks[mau] - self.stocks_const[mau])

            if sum(nl_vc_thieu.values()) > 10:
                continue

            nl_thieu = {}
            nl_thieu['auto_color'] = 0
            for mau in temp:
                nl_thieu[mau] = max(0, car.stocks[mau] - self.stocks_const[mau] - self.stocks[mau])

            if self.stocks['auto_color'] != 0:
                a = self.stocks['auto_color']
                for i in range(a):
                    loai_nl_thieu = [mau for mau in temp if nl_thieu[mau] > 0]
                    dict_temp = {}
                    for mau in loai_nl_thieu:
                        if board.stocks[mau] == 0:
                            dict_temp[mau] = -10 - nl_thieu[mau]
                        else:
                            dict_temp[mau] = board.stocks[mau] - nl_thieu[mau]

                    dict_tempp = {k: v for k, v in sorted(
                        dict_temp.items(), key=lambda item: item[1], reverse=False
                    )}
                    nl_thieu[list(dict_tempp.keys())[0]] -= 1
            loai_mau_thieu = [mau for mau in temp if nl_thieu[mau] > 0]
            list_board_nl = [mau for mau in temp if board.stocks[mau] > 0]
            list_temp = list(set(loai_mau_thieu) & set(list_board_nl))
            if list_temp.__len__() > 0:
                list_thu_nhat.append({
                    'the': car,
                    'nl_thieu': nl_thieu
                })
        list_check_11 = [ele for ele in list_thu_nhat if ele['the'] in list_check_1]
        list_check_11_2 = [ele for ele in list_thu_nhat if ele['the'] in list_check_1_]
        list_check_22 = [ele for ele in list_thu_nhat if ele not in (list_check_11 + list_check_11_2)]
        list_check_11.sort(key=lambda a: sum(a['nl_thieu'].values()))
        list_check_11_2.sort(key=lambda a: sum(a['nl_thieu'].values()))
        list_check_22.sort(key=lambda a: sum(a['nl_thieu'].values()))
        list_thu_hai = list_check_11 + list_check_11_2 + list_check_22
        for ele in list_thu_hai:
            for mau in temp:
                if mau not in list_board_nl:
                    ele['nl_thieu'][mau] = 0
        return list_thu_hai

