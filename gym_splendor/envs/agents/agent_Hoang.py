from os import stat
from turtle import st
from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    # Trả lại 1 dict các nguyên liệu còn thiếu để mua thẻ target
    def lack_of_stocks(self, _card):
        price = _card.stocks # dict, 5 keys
        my_stocks = {}
        for key in self.stocks_const.keys():
            my_stocks[key] = self.stocks[key] + self.stocks_const[key]

        my_stocks['auto_color'] = self.stocks['auto_color']

        lack_of_stocks = {}
        for key in price.keys():
            lack_of_stocks[key] = max(0, price[key] - my_stocks[key])

        n = my_stocks['auto_color']

        for i in range(n):
            if sum(lack_of_stocks.values()) == 0:
                break

            for key in lack_of_stocks.keys():   #########
                if lack_of_stocks[key] != 0:
                    lack_of_stocks[key] -= 1
                    break
        
        return lack_of_stocks

    #Trả về danh sách là một list các thẻ có thể mua (thẻ mở trên bàn hoặc thẻ mà người chơi đã úp)
    def available_card(self, _card):
        list = []
        card_open = _card.dict_Card_Stocks_Show
        for key in card_open.keys():
            if key != 'Noble':
                for card in card_open[key]:
                    if self.check_get_card(card):
                        list.append(card)

        card_upside_down = self.card_upside_down
        for card in card_upside_down:
                if self.check_get_card(card):
                    list.append(card)
            
        return list

    # Xử lý trả nguyên liệu khi thừa      
    def return_stocks(self, stocks_get):
        stocks_return = []

        my_stocks = self.stocks
        for key in stocks_get:
            my_stocks[key] += 1   
            
        if sum(my_stocks.values()) > 10:
            n = sum(my_stocks.values())-10
            for i in range(n):
                for key in my_stocks.keys():
                    if my_stocks[key] == max(my_stocks.values()):
                        stocks_return += [key]
                        my_stocks[key] -= 1
                        break
        else:
            stocks_return = []
        return stocks_return

    def priority_dict(self,type_card,list_card):
        priority_dict = {
            'red': 0,
            'blue': 0,
            'green': 0,
            'black': 0,
            'white': 0
        }
        for _card in list_card.dict_Card_Stocks_Show[type_card]:
            for stock in _card.stocks.keys():
                if _card.stocks[stock] > 0:
                    if stock == 'red':
                        priority_dict['red'] += 1
                    if stock == 'blue':
                        priority_dict['blue'] += 1
                    if stock == 'green':
                        priority_dict['green'] += 1
                    if stock == 'black':
                        priority_dict['black'] += 1
                    if stock == 'white':
                        priority_dict['white'] += 1

        return priority_dict

    def action(self, state):
        stocks = []
        stocks_return = [] 
        card = None
        available_card_list = [] # danh sách các thẻ có thể mua

        if state['Turn'] <= 8:
            priority = self.priority_dict('I',state['Board'])
            priority_list = list(priority.values())
            # print(priority)
            # print(priority_list)
            for stock in priority:
                if priority[stock] == max(list(priority_list)):
                    if len(stocks) < 3:
                     if state['Board'].stocks[stock] > 0:
                        stocks += [stock]
                        for _key in priority:
                            if state['Board'].stocks[_key] > 0 and _key != stock and self.stocks[_key] < 1:
                                    if len(stocks) < 3:
                                        stocks += [_key]
                     else:
                        for _key in state['Board'].stocks:
                            if state['Board'].stocks[_key] > 0 and _key != 'auto_color':
                                    if len(stocks) < 3:
                                        stocks += [_key]
        else:   
            available_card_list = self.available_card(state['Board'])
            target_list = []

            if len(available_card_list) != 0:
                # for _card in available_card_list:
                    # print(_card.id)
                #Tìm ra điểm số cao nhất trong tât cả các thẻ có thể mua
                max_score = 0
                for _card in available_card_list:
                   if _card.score > max_score:
                        max_score = _card.score

                #Tìm ra các thẻ có điểm = điểm cao nhât       
                for _card in available_card_list:
                    if _card.score == max_score:
                        target_list.append(_card)

                #Tìm ra số nguyên liệu cần mua ít nhất trong các thẻ có điểm cao nhất
                min_stocks = 15        
                for _card in target_list:                  
                    if sum(_card.stocks.values()) < min_stocks:
                        min_stocks = sum(_card.stocks.values())
                
                #Tìm ra thẻ có số nguyên liệu ít nhất và điểm cao nhất
                for _card in target_list:
                    if sum(_card.stocks.values()) == min_stocks:
                            return [], _card, []

            else:
                count = 0
                
                for stock in state['Board'].stocks:
                    if state['Board'].stocks[stock] > 0 and stock != 'auto_color':
                        count += 1
                        
                # print(count, 'abc')
                if count == 0:
                    if len(self.card_upside_down) >= 3:
                        return [],None,[]
                    else:
                        lacks_list = []   
                        for type_card in state['Board'].dict_Card_Stocks_Show:
                            if type_card != 'Noble':  
                                for _card in state['Board'].dict_Card_Stocks_Show[type_card]:
                                    lacks = sum(self.lack_of_stocks(_card).values())
                                    lacks_list.append(lacks)
                        min_value = min(lacks_list)
                        for type_card in state['Board'].dict_Card_Stocks_Show:
                             if type_card != 'Noble': 
                                for _card in state['Board'].dict_Card_Stocks_Show[type_card]:
                                    if sum(self.lack_of_stocks(_card).values()) == min_value:
                                        if sum(self.stocks.values()) <= 9:
                                            return [],_card,[]
                                        if sum(self.stocks.values()) > 9:
                                            for stock in self.stocks:
                                                if self.stocks[stock] == max(self.stocks.values()):
                                                    stocks_return += [stock]
                                                    break
                                            return [],_card,stocks_return
                if count == 1:
                    if sum(self.stocks.values()) > 8:
                    #    print('Nhiều hơn 8 nguyên liệu thường trên tay')
                       if len(self.card_upside_down) < 3:
                         lacks_list = []   
                         for type_card in state['Board'].dict_Card_Stocks_Show:
                            if type_card != 'Noble':  
                                for _card in state['Board'].dict_Card_Stocks_Show[type_card]:
                                    lacks = sum(self.lack_of_stocks(_card).values())
                                    lacks_list.append(lacks)
                         min_value = min(lacks_list)
                         for type_card in state['Board'].dict_Card_Stocks_Show:
                            if type_card != 'Noble': 
                                for _card in state['Board'].dict_Card_Stocks_Show[type_card]:
                                    if sum(self.lack_of_stocks(_card).values()) == min_value:
                                        # print(_card)
                                        if sum(self.stocks.values()) == 9:
                                            return [],_card,[]
                                        if sum(self.stocks.values()) == 10:
                                            for stock in self.stocks:
                                                if self.stocks[stock] == max(self.stocks.values()):
                                                    stocks_return += [stock]
                                                    break
                                            return [],_card,stocks_return
                       else:
                           for stock in state['Board'].stocks:
                            if stock != 'auto_color':
                                if state['Board'].stocks[stock] > 0:
                                    stocks += [stock]
                                    stocks_return = self.return_stocks(stocks)
                                    return stocks, None, stocks_return
                    else:
                        # print('ít hơn 9 nguyên liệu thường trên tay')
                        for stock in state['Board'].stocks:
                            if stock != 'auto_color':
                                if state['Board'].stocks[stock] > 3:
                                        # print(f'lấy 2 nguyên liệu {stock}')
                                        stocks += [stock,stock]
                                        stocks_return = self.return_stocks(stocks)
                                        return stocks, None, stocks_return

                        # print('Không lấy được 2 nl cùng loại')
                        if len(self.card_upside_down) < 3:
                            lacks_list = []   
                            for type_card in state['Board'].dict_Card_Stocks_Show:
                                if type_card != 'Noble':  
                                    for _card in state['Board'].dict_Card_Stocks_Show[type_card]:
                                            lacks = sum(self.lack_of_stocks(_card).values())
                                            lacks_list.append(lacks)
                            min_value = min(lacks_list)
                            for type_card in state['Board'].dict_Card_Stocks_Show:
                                if type_card != 'Noble': 
                                    for _card in state['Board'].dict_Card_Stocks_Show[type_card]:
                                        if sum(self.lack_of_stocks(_card).values()) == min_value:
                                                # print(_card)
                                                return [], _card, []
                                else:
                                    for stock in state['Board'].stocks:
                                        if stock != 'auto_color':
                                            if state['Board'].stocks[stock] > 0:
                                                stocks += [stock]
                                                stocks_return = self.return_stocks(stocks)      

                if count == 2:
                    for stock in state['Board'].stocks:
                        if state['Board'].stocks[stock] > 0 and stock != 'auto_color':
                            if len(stocks) < 2:
                                # print('abacabac')
                                stocks += [stock]
                                stocks_return = self.return_stocks(stocks)
                
                if count >= 3:
                    if state['Turn'] <= 80:
                        priority = self.priority_dict('I',state['Board'])
                        priority_list = list(priority.values())
                        # print(priority)
                        # print(priority_list)
                        for stock in priority:
                            if priority[stock] == max(list(priority_list)):
                                if len(stocks) < 3:
                                    if state['Board'].stocks[stock] > 0:
                                        stocks += [stock]
                                        for _key in priority:
                                            if state['Board'].stocks[_key] > 0 and _key != stock:
                                                if len(stocks) < 3:
                                                    stocks += [_key]
                                        stocks_return = self.return_stocks(stocks)
                                    else:
                                        for _key in state['Board'].stocks:
                                            if state['Board'].stocks[_key] > 0 and _key != 'auto_color':
                                                if len(stocks) < 3:
                                                    stocks += [_key]
                                        stocks_return = self.return_stocks(stocks)
                    else:
                        priority = self.priority_dict('II',state['Board'])
                        priority_list = list(priority.values())
                        # print(priority)
                        # print(priority_list)
                        for stock in priority:
                            if priority[stock] == max(list(priority_list)):
                                if len(stocks) < 3:
                                    if state['Board'].stocks[stock] > 0:
                                        stocks += [stock]
                                        for _key in priority:
                                            if state['Board'].stocks[_key] > 0 and _key != stock:
                                                if len(stocks) < 3:
                                                    stocks += [_key]
                                        stocks_return = self.return_stocks(stocks)
                                    else:
                                        for _key in state['Board'].stocks:
                                            if state['Board'].stocks[_key] > 0 and _key != 'auto_color':
                                                if len(stocks) < 3:
                                                    stocks += [_key]
                                        stocks_return = self.return_stocks(stocks)                    
        return stocks,card,stocks_return
    
