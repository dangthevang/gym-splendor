from ..base.player import Player
import random
from copy import deepcopy

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state, training_data):
        board = state['Board']
        list_cards_target_can_buy = self.list_cards_target_can_buy(board)
        if len(list_cards_target_can_buy) > 0:
            card = list_cards_target_can_buy[0]
            return [], card, []

        list_target_cards = self.list_target_cards(board)
        if len(list_target_cards) > 0:
            card = list_target_cards[0]
            if self.check_upsite_down(card):
                stocks_return = []
                if board.stocks['auto_color'] > 0:
                    stocks_return = self.Luachonbothe(board, ['auto_color'])
                
                return [], card, stocks_return, 3
        
        if len(self.card_upside_down) > 0:
            if sum(self.stocks.values()) <= 8:
                list_color_for_holdings = self.list_color_for_holdings(board)
                if len(list_color_for_holdings) > 0:
                    color = list_color_for_holdings[0]
                    if board.stocks[color] > 3:
                        stocks_get = [color, color]
                        stocks_return = self.Luachonbothe(board, stocks_get)
                        # print(stocks_get, stocks_return, '1111')
                        return stocks_get, None, stocks_return

                if len(list_color_for_holdings) > 2:
                    stocks_get = [mau for mau in list_color_for_holdings[0:3] if board.stocks[mau] > 0]
                    if stocks_get.__len__() == 3:
                        stocks_return = self.Luachonbothe(board, stocks_get)
                        # print(stocks_get, stocks_return, '2222')
                        return stocks_get, None, stocks_return
                
                if len(list_color_for_holdings) == 2:
                    color = list_color_for_holdings[1]
                    if board.stocks[color] > 3:
                        stocks_get = [color, color]
                        stocks_return = self.Luachonbothe(board, stocks_get)
                        # print(stocks_get, stocks_return, '3333')
                        return stocks_get, None, stocks_return

                    color_3 = self.color_3(board)
                    if color_3 != None:
                        stocks_get = [mau for mau in (list_color_for_holdings[0:2] + [color_3]) if board.stocks[mau] > 0]
                        if stocks_get.__len__() == 3:
                            stocks_return = self.Luachonbothe(board, stocks_get)
                            # print(stocks_get, stocks_return, '4444')
                            return stocks_get, None, stocks_return

                if len(list_color_for_holdings) == 1:
                    list_color_no_target = self.list_color_no_target(board)
                    if len(list_color_no_target) >= 2:
                        stocks_get = [mau for mau in (list_color_no_target[0:2] + [list_color_for_holdings[0]]) if board.stocks[mau] > 0]
                        if stocks_get.__len__() == 3:
                            stocks_return = self.Luachonbothe(board, stocks_get)
                            # print(stocks_get, stocks_return, '5555')
                            return stocks_get, None, stocks_return

                    target_support_cards = self.target_support_cards(board)
                    if target_support_cards != None:
                        color_card_support = self.color_card_support(board)
                        if len(color_card_support) > 2:
                            stocks_get = [mau for mau in (color_card_support[0:3]) if board.stocks[mau] > 0 if mau not in stocks_get]
                            if stocks_get.__len__() == 3:
                                stocks_return = self.Luachonbothe(board, stocks_get)
                                # print(stocks_get, stocks_return, '6666')
                                return stocks_get, None, stocks_return

                        for color in color_card_support:
                            if board.stocks[color] > 3:
                                stocks_get = [color, color]
                                stocks_return = self.Luachonbothe(board, stocks_get)
                                # print(stocks_get, stocks_return, '7777')
                                return stocks_get, None, stocks_return

                        if len(color_card_support) == 2:
                            color_3_support = self.color_3_support(board)
                            if color_3_support != None:
                                stocks_get = [mau for mau in (color_card_support[0:2] + [color_3_support]) if board.stocks[mau] > 0]
                                if stocks_get.__len__() == 3:
                                    stocks_return = self.Luachonbothe(board, stocks_get)
                                    # print(stocks_get, stocks_return, '8888')
                                    return stocks_get, None, stocks_return

                            for color in color_card_support:
                                if board.stocks[color] > 3:
                                    stocks_get = [color, color]
                                    stocks_return = self.Luachonbothe(board, stocks_get)
                                    # print(stocks_get, stocks_return, '9999')
                                    return stocks_get, None, stocks_return

                        card = target_support_cards
                        if self.check_upsite_down(card):
                            stocks_return = []
                            if board.stocks['auto_color'] > 0:
                                stocks_return = self.Luachonbothe(board, ['auto_color'])
                        
                            return [], card, stocks_return, 3

                    theup = self.theup(board)
                    if theup != None:
                        card = theup
                        if self.check_upsite_down(card):
                            stocks_return = []
                            if board.stocks['auto_color'] > 0:
                                stocks_return = self.Luachonbothe(board, ['auto_color'])
                        
                            return [], card, stocks_return, 3

                    if target_support_cards != None:
                        card = target_support_cards
                        if self.check_get_card(card):
                            return [], card, []
                    
                    if theup != None:
                        card = theup
                        if self.check_get_card(card):
                            return [], card, []

                    if list_color_no_target.__len__() >= 3:
                        stocks_get = [mau for mau in (list_color_no_target[0:3]) if board.stocks[mau] > 0]
                        if stocks_get.__len__() == 3:
                            stocks_return = self.Luachonbothe(board, ['auto_color'])
                            # print(stocks_get, stocks_return, '0000')
                            return stocks_get, None, stocks_return
                    
                    if list_color_no_target.__len__() > 0:
                        for color in list_color_no_target:
                            if board.stocks[color] > 3:
                                stocks_get = [color, color]
                                stocks_return = self.Luachonbothe(board, stocks_get)
                                # print(stocks_get, stocks_return, 'aaaa')
                                return stocks_get, None, stocks_return

            if sum(self.stocks.values()) == 9:
                list_color_for_holdings = self.list_color_for_holdings(board)
                for color in list_color_for_holdings:
                    if board.stocks[color] > 3:
                        stocks_get = [color, color]
                        stocks_return = self.Luachonbothe(board, stocks_get)
                        # print(stocks_get, stocks_return, 'bbbb')
                        return stocks_get, None, stocks_return

                if self.card_upside_down.__len__() < 3:
                    if len(list_target_cards) > 0:
                        stocks_return = []
                        if board.stocks['auto_color'] > 0:
                            stocks_return = self.Luachonbothe(board, ['auto_color'])
                        
                        card = list_target_cards[0]
                        return [], card, stocks_return, 3

                    target_support_cards = self.target_support_cards(board)
                    if target_support_cards != None:
                        stocks_return = []
                        if board.stocks['auto_color'] > 0:
                            stocks_return = self.Luachonbothe(board, ['auto_color'])
                        
                        card = target_support_cards
                        return [], card, stocks_return, 3

                    theup = self.theup(board)
                    if theup != None:
                        stocks_return = []
                        if board.stocks['auto_color'] > 0:
                            stocks_return = self.Luachonbothe(board, ['auto_color'])
                        
                        card = theup
                        return [], card, stocks_return, 3

                if len(list_color_for_holdings) == 2:
                    color_3_on_board = self.color_3_on_board(board)
                    if color_3_on_board != None:
                        stocks_get = [mau for mau in (list_color_for_holdings[0:2] + [color_3_on_board]) if board.stocks[mau] > 0]
                        if stocks_get.__len__() == 3:
                            stocks_return = self.Luachonbothe(board, stocks_get)
                            # print(stocks_get, stocks_return, 'cccc')
                            return stocks_get, None, stocks_return

                target_support_cards = self.target_support_cards(board)
                if target_support_cards != None:
                    if self.check_get_card(target_support_cards):
                        card = target_support_cards
                        return [], card, []
                
                theup = self.theup(board)
                if theup != None:
                    if self.check_get_card(theup):
                        card = theup
                        return [], card, []

            if sum(self.stocks.values()) == 10:
                target_support_cards = self.target_support_cards(board)
                if target_support_cards != None:
                    if self.check_upsite_down(target_support_cards):
                        stocks_return = []
                        if board.stocks['auto_color'] > 0:
                            stocks_return = self.Luachonbothe(board, ['auto_color'])
                        
                        card = target_support_cards
                        return [], card, stocks_return, 3

                theup = self.theup(board)
                if theup != None:
                    if self.check_upsite_down(theup):
                        stocks_return = []
                        if board.stocks['auto_color'] > 0:
                            stocks_return = self.Luachonbothe(board, ['auto_color'])
                        
                        card = theup
                        return [], card, stocks_return, 3

                if target_support_cards != None:
                    if self.check_get_card(target_support_cards):
                        card = target_support_cards
                        return [], card, []

                if theup != None:
                    if self.check_get_card(theup):
                        card = theup
                        return [], card, []

                list_color_for_holdings = self.list_color_for_holdings(board)
                if len(list_color_for_holdings) > 0:
                    for color in list_color_for_holdings:
                        if board.stocks[color] > 3:
                            stocks_get = [color, color]
                            stocks_return = self.Luachonbothe(board, stocks_get)
                            # print(stocks_get, stocks_return, 'dddd')
                            return stocks_get, None, stocks_return

                if len(list_color_for_holdings) == 2:
                    color_3_on_board = self.color_3_on_board(board)
                    if color_3_on_board != None:
                        stocks_get = [mau for mau in (list_color_for_holdings[0:2] + [color_3_on_board]) if board.stocks[mau] > 0]
                        if stocks_get.__len__() == 3:
                            stocks_return = self.Luachonbothe(board, stocks_get)
                            # print(stocks_get, stocks_return, 'eeee')
                            return stocks_get, None, stocks_return
        
            list_cards_on_board_can_buy = self.list_cards_on_board_can_buy(board)
            if len(list_cards_on_board_can_buy) > 0:
                for card in list_cards_on_board_can_buy:
                    if card.score > 0:
                        if self.check_get_card(card):
                            return [], card, []
                
                for card in list_cards_on_board_can_buy:
                    if self.check_get_card(card):
                        return [], card, []

            list_color_on_board = self.list_color_on_board(board)
            if len(list_color_on_board) > 0:
                for color in list_color_on_board:
                    if board.stocks[color] > 3:
                        stocks_get = [color, color]
                        stocks_return = self.Luachonbothe(board, stocks_get)
                        # print(stocks_get, stocks_return, 'ffff')
                        return stocks_get, None, stocks_return
                
                if len(list_color_on_board) > 2:
                    stocks_get = [mau for mau in (list_color_on_board[0:3]) if board.stocks[mau] > 0]
                    if stocks_get.__len__() == 3:
                        stocks_return = self.Luachonbothe(board, stocks_get)
                        # print(stocks_get, stocks_return, 'gggg')
                        return stocks_get, None, stocks_return
        
        if len(self.card_upside_down) == 0:
            list_color_on_board = self.list_color_on_board(board)
            if len(list_color_on_board) > 0:
                for color in list_color_on_board:
                    if board.stocks[color] > 3:
                        stocks_get = [color, color]
                        stocks_return = self.Luachonbothe(board, stocks_get)
                        # print(stocks_get, stocks_return, 'hhhh')
                        return stocks_get, None, stocks_return

                if len(list_color_on_board) > 2:
                    stocks_get = [mau for mau in (list_color_on_board[0:3]) if board.stocks[mau] > 0]
                    if stocks_get.__len__() == 3:
                        stocks_return = self.Luachonbothe(board, stocks_get)
                        # print(stocks_get, stocks_return, 'iiii')
                        return stocks_get, None, stocks_return

                if len(list_color_on_board) == 2:
                    color_3 = self.color_3(board)
                    if color_3 != None:
                        stocks_get = [mau for mau in (list_color_on_board[0:2] + [color_3]) if board.stocks[mau] > 0]
                        if stocks_get.__len__() == 3:
                            stocks_return = self.Luachonbothe(board, stocks_get)
                            # print(stocks_get, stocks_return, 'kkkk')
                            return stocks_get, None, stocks_return
            
            if sum(self.stocks.values()) <= 8:
                list_color_no_target = self.list_color_no_target(board)
                if list_color_no_target.__len__() > 0:
                    for color in list_color_no_target:
                        if board.stocks[color] > 3:
                            stocks_get = [color, color]
                            stocks_return = self.Luachonbothe(board, stocks_get)
                            # print(stocks_get, stocks_return, 'llll')
                            return stocks_get, None, stocks_return

                    if len(list_color_no_target) >= 3:
                        stocks_get = [mau for mau in (list_color_no_target[0:3]) if board.stocks[mau] > 0]
                        if stocks_get.__len__() == 3:
                            stocks_return = self.Luachonbothe(board, ['auto_color'])
                            # print(stocks_get, stocks_return, 'mmmm')
                            return stocks_get, None, stocks_return
            
            theup = self.theup(board)
            if theup != None:
                if self.check_get_card(theup):
                    card = theup
                    return [], card, []

            list_cards_on_board_can_buy = self.list_cards_on_board_can_buy(board)
            if len(list_cards_on_board_can_buy) > 0:
                for card in list_cards_on_board_can_buy:
                    if card.score > 0:
                        if self.check_get_card(theup):
                            return [], card, []
            
        stocks = []
        for i in range(min(3, 10-sum(self.stocks.values()))):
            temp_list = [mau for mau in state['Board'].stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))
        
        if stocks.__len__() > 0:
            # print(stocks, 'mmmm')
            return stocks, None, []

        for i in range(3):
            temp_list = [mau for mau in state['Board'].stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))

        stocks_return = []
        nl_thua = max(sum(self.stocks.values()) + stocks.__len__() - 10, 0)
        pl_st = deepcopy(self.stocks)
        for i in range(nl_thua):
            temp_list = [mau for mau in pl_st.keys() if mau != 'auto_color' and pl_st[mau] > 0]
            mau_choice = random.choice(temp_list)
            stocks_return.append(mau_choice)
            pl_st[mau_choice] -= 1
        
        if stocks.__len__() > 0:
            # print(stocks, stocks_return, 'nnnn')
            return stocks, None, stocks_return

        card = self.Tim_the_up(state['Board'])
        if card != None:
            stocks_return = []
            if state['Board'].stocks['auto_color'] > 0:
                stocks_return = self.Luachonbothe(state['Board'], ['auto_color'])
            
            # print(card.stocks, card.score, stocks_return, 'oooo')
            return [], card, stocks_return, 3
        


        # print(self.card_upside_down.__len__(), 'pppp')
        return [], None, []

    def Tim_the_up(self, board):
        list_card_can_check = []
        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for car in board.dict_Card_Stocks_Show[type_card]:
                    list_card_can_check.append(car)

        if len(list_card_can_check) != 0:
            card = self.chon_the_gia_tri_cao(list_card_can_check)
            return card
        
        return None

    def chon_the_gia_tri_cao(self, list_the):
        value_cards = [car.score / sum(list(car.stocks.values())) for car in list_the]
        max_value = max(value_cards)

        return list_the[value_cards.index(max_value)]

    def check_any_card_5score_onhand(self):
        for card in self.card_upside_down:
            if card.score == 5:
                return True
        for card in self.card_open:
            if card.score == 5:
                return True
        return False

    def list_cards_on_board_can_buy(self, board):
        cards_on_board_can_buy = []
        type = ["III", "II", "I"]
        for i in type:
            for card in board.dict_Card_Stocks_Show[i]:
                if self.check_get_card(card):
                    cards_on_board_can_buy.append(card)
        return cards_on_board_can_buy

    def check_any_card_4score_onhand(self):
        for card in self.card_upside_down:
            if card.score == 4:
                return True
        for card in self.card_open:
            if card.score == 4:
                return True
        return False

    def check_any_card_3score_onhand(self):
        for card in self.card_upside_down:
            if card.score == 3:
                return True
        for card in self.card_open:
            if card.score == 3:
                return True
        return False

    def theup(self, board):
        NL = []
        for nguyenlieu in board.dict_Card_Stocks_Show["III"][0].stocks.keys():
            max = 0
            for the in self.card_upside_down:
                if the.stocks[nguyenlieu] > max:
                    the.stocks[nguyenlieu] = max
            if max > self.stocks[nguyenlieu]:
                NL.append(nguyenlieu)
        for n in NL:
            for the1 in board.dict_Card_Stocks_Show["III"]:
                if the1.type_stock == n:
                    return the1

    def list_holding_cards(self):
        A = []
        if len(self.card_upside_down) > 0:
            for item in self.card_upside_down:
                holding_cards = self.card_upside_down.copy()  
                holding_cards.remove(item)
                for card in holding_cards:
                    if card.stocks[item.type_stock] > 0:
                        A.append(item)
            score = [3, 5, 4, 2, 1]
            for i in score:
                for item in self.card_upside_down:
                    if item.score == i:
                        A.append(item)
        return A

    def list_color_for_holdings(self, board):
        list_color_holding = []
        dict_start = {"red" : 0, "white": 0, "blue": 0, "green": 0,"black": 0}
        item = None
        if len(self.card_upside_down) > 0:
            item = self.list_holding_cards()[0]
            a = 0
            for color in list(item.stocks.keys()):
                if (item.stocks[color] - self.stocks[color] - self.stocks_const[color]) > a:
                    if board.stocks[color] > 0: 
                        a = item.stocks[color] - self.stocks[color] - self.stocks_const[color]
                        if len(list_color_holding) > 0:                    
                            list_color_holding.insert(0,color)
                        else:
                            list_color_holding.append(color)
                if item.stocks[color] > 0:
                    if board.stocks[color] > 0:
                        if color not in list_color_holding:
                            list_color_holding.append(color)
            if len(self.card_upside_down) > 1:
                list_cards = self.list_holding_cards().copy()
                list_cards.pop(0)
                for card in list_cards:
                    for color in card.stocks.keys():
                        dict_start[color] += card.stocks[color] 
                for color in dict_start.keys():
                    dict_start[color] -= ( self.stocks[color] + self.stocks_const[color] )
                list_values = sorted(list(dict_start.values()),reverse=True)
                for value in list_values:
                    for color in dict_start.keys():
                        if dict_start[color] == value:
                            if value > 0:
                                if board.stocks[color] > 0:
                                    if color not in list_color_holding:
                                        list_color_holding.append(color)
        return list_color_holding

    def list_token_can_get(self, board):
        nguyenlieucon = []
        for nguyenlieu in board.stocks.keys():
            if board.stocks[nguyenlieu] > 0 and nguyenlieu != "auto_color":
                nguyenlieucon.append(nguyenlieu)
        return nguyenlieucon

    def get_important_token(self, board):
        token_can_get = self.list_token_can_get(board)
        dict_important_token = {}
        dict_important_token['red'] = 0
        dict_important_token['blue'] = 0
        dict_important_token['green'] = 0
        dict_important_token['white'] = 0
        dict_important_token['black'] = 0
        for card in self.card_upside_down:
            dict_important_token['red'] += card.stocks['red'] - self.stocks_const['red'] - self.stocks['red']
            dict_important_token['blue'] += card.stocks['blue'] - self.stocks_const['blue'] - self.stocks['blue']
            dict_important_token['green'] += card.stocks['green'] - self.stocks_const['green'] - self.stocks['green']
            dict_important_token['white'] += card.stocks['white'] - self.stocks_const['white'] - self.stocks['white']
            dict_important_token['black'] += card.stocks['black'] - self.stocks_const['black'] - self.stocks['black']
        list_token = list(dict_important_token.keys())
        list_number_token = list(dict_important_token.values())
        dict_token_important = {}
        count = 0
        while count < len(list_token):
            if list_token[list_number_token.index(max(list_number_token))] in token_can_get:
                dict_token_important[list_token[list_number_token.index(max(list_number_token))]] = max(list_number_token)
            list_token.remove(list_token[list_number_token.index(max(list_number_token))])
            list_number_token.remove(max(list_number_token))
        {k: v for k, v in sorted(dict_token_important.items(), key=lambda item: item[1],reverse=True)}
        return list(dict_token_important.keys())

    def list_color_return_when_holding(self, board):
        color_return = []
        for color in self.stocks.keys():
            if self.stocks[color] > 0 and color != "auto_color":
                if color not in self.list_color_for_holdings(board):
                    color_return.append(color)
        list = self.list_color_for_holdings(board).copy()
        list.reverse()
        for color in list:
            if self.stocks[color] > 0 and color not in color_return:
                color_return.append(color)
        return color_return

    def Luachonbothe(self, board, args):
        dict_bo = {
            "red":0,
            "blue":0,
            "white":0,
            "green":0,
            "black":0,
            "auto_color": 0
        }
        dict_bd = self.stocks.copy()
        for x in args:
            dict_bd[x] += 1
        danhsachcon = self.list_color_return_when_holding(board).copy()
        
        if sum(dict_bd.values()) > 10:
            n = sum(dict_bd.values()) - 10
            i = 0
            while n != 0:
                if dict_bd[danhsachcon[i]] != 0:
                    dict_bo[danhsachcon[i]] +=1
                    dict_bd[danhsachcon[i]] -=1
                    n -= 1
                else:
                    i += 1
        
        list_bo = []
        for key in dict_bo.keys():
            while dict_bo[key] > 0:
                list_bo.append(key)
                dict_bo[key] -= 1
        return list_bo

    def target_support_cards(self, board):
        target_support_cards = []
        cardx = None
        type = ["II", "I"]
        list_color_for_holdings = self.list_color_for_holdings(board)
        if len(list_color_for_holdings) > 0:
            for color in list_color_for_holdings:
                for i in type:
                    for card in board.dict_Card_Stocks_Show[i]:
                        if card.type_stock == color:
                            target_support_cards.append(card)
        valuation = 0
        for card in target_support_cards:
            if card.score / sum(card.stocks.values()) > valuation:
                valuation = card.score / sum(card.stocks.values())
                cardx = card
        return cardx

    def color_card_support(self, board):
        dict = {}
        color_support = []
        target_support_cards = self.target_support_cards(board)
        if target_support_cards != None:
            dict = target_support_cards.stocks.copy()
            list_values = sorted(list(dict.values()),reverse=True)
            for value in list_values:
                for color in dict.keys():
                    if dict[color] == value and color not in color_support:
                        if value > 0:
                            if board.stocks[color] > 0:
                                color_support.append(color)
        return color_support

    def color_3_support(self, board):
        color3_support = None
        for color in board.stocks.keys():
            if board.stocks[color] > 0 and color != 'auto_color':
                if color not in self.color_card_support(board):
                    color3_support = color
        return color3_support

    def list_cards_target_can_buy(self, board):
        cards_target_can_buy = []
        for card in self.list_holding_cards():
            if self.check_get_card(card):
                cards_target_can_buy.append(card)
        for card in self.list_target_cards(board):
            if self.check_get_card(card):
                cards_target_can_buy.append(card)
        if self.target_support_cards(board) != None:
            if self.check_get_card(card):
                cards_target_can_buy.append(card)
        return cards_target_can_buy

    def list_target_cards(self, board):
        target_cards = []
        type = ["III", "II", "I"]
        for i in type:
            for card in board.dict_Card_Stocks_Show[i]:
                if card.score == 5 and sum(card.stocks.values()) == 10:
                    target_cards.append(card)
                if card.score == 4 and sum(card.stocks.values()) == 7:
                    target_cards.append(card)
                if card.score == 3 and sum(card.stocks.values()) == 6:
                    target_cards.append(card)
                if card.score == 2 and sum(card.stocks.values()) == 2:
                    target_cards.append(card)
                if card.score == 1 and sum(card.stocks.values()) == 4:
                    target_cards.append(card)
        target_cards_rank = []
        score = [3, 5, 4, 3, 2, 1]

        for i in score:
            for card in target_cards:
                if card.score == i:
                    if card.score == 5:
                        if self.check_any_card_5score_onhand() == False:
                            target_cards_rank.append(card)
                        else:
                            continue
                    if card.score == 4:
                        if self.check_any_card_4score_onhand() == False:
                            target_cards_rank.append(card)
                        else:
                            continue
                    if card.score == 3:
                        if self.check_any_card_3score_onhand() == False:
                            target_cards_rank.append(card)
                        else:
                            continue
                    target_cards_rank.append(card)
        target_cards_rank_upgrade = []
        if len(self.card_upside_down) > 0:
            for item in self.card_upside_down:
                for card in target_cards_rank:
                    if card.stocks[item.type_stock] > 0:
                        target_cards_rank_upgrade.append(card)
                    if item.stocks[card.type_stock] > 0:
                        target_cards_rank_upgrade.append(card)
        else:
            target_cards_rank_upgrade = target_cards_rank.copy()
        return target_cards_rank_upgrade

    def list_color_on_board(self, board):
        dict_start = {"red" : 0, "white": 0, "blue": 0, "green": 0,"black": 0}
        
        type = ["III", "II"]
        for i in type:
            for card in board.dict_Card_Stocks_Show[i]:
                list_target_cards = self.list_target_cards(board)
                if card in list_target_cards:
                    for color in dict_start.keys():
                        dict_start[color] += card.stocks[color]
        list_color = []
        sort_list = sorted(list(dict_start.values()), reverse=True)
        for value in sort_list:
            for color in list(dict_start.keys()):
                if dict_start[color] == value:
                    if color not in list_color:
                        list_color.append(color)
        list_color_onboard = []
        for color in list_color:
            if board.stocks[color] > 0:
                list_color_onboard.append(color)
        return list_color_onboard

    def color_3(self, board):
        color3 = None
        list_color_for_holdings = self.list_color_for_holdings(board)
        if len(list_color_for_holdings) == 2:
            for color in board.stocks.keys():
                if board.stocks[color] > 0 and color not in list_color_for_holdings and color != 'auto_color':
                    if color != "auto_color":
                        color3 = color
        return color3

    def color_3_on_board(self, board):
        color3 = None
        list_color_on_board = self.list_color_on_board(board)
        if len(list_color_on_board) == 2:
            for color in board.stocks.keys():
                if board.stocks[color] > 0 and color not in list_color_on_board and color != 'auto_color':
                    if color != "auto_color":
                        color3 = color
        return color3

    def list_color_no_target(self, board):
        color_no_target = []
        dict_start = {"red" : 0, "white": 0, "blue": 0, "green": 0,"black": 0}
        type = ["III", "II", "I"]
        for i in type:
            for card in board.dict_Card_Stocks_Show[i]:
                for color in card.stocks.keys():
                    dict_start[color] += card.stocks[color]
        list_value = sorted(list(dict_start.values()),reverse=True)
        for value in list_value:
            for color in dict_start.keys():
                if dict_start[color] == value:
                    if board.stocks[color] > 0:
                        if color not in color_no_target:
                            list_color_for_holdings = self.list_color_for_holdings(board)
                            if color not in list_color_for_holdings:
                                color_no_target.append(color)
        return color_no_target

    def dict_return(self, board,args):
        dict_bo = {
            "red":0,
            "blue":0,
            "white":0,
            "green":0,
            "black":0,
            "auto_color": 0
        }
        dict_bd = self.stocks.copy()
        for x in args:
            dict_bd[x] += 1
        color_list = self.list_color_no_target(board).copy()
        color_list.reverse()
        if sum(dict_bd.values()) > 10:
            n = sum(dict_bd.values()) - 10
            i = 0
            while n != 0:
                if dict_bd[color_list[i]] != 0:
                    dict_bo[color_list[i]] +=1
                    dict_bd[color_list[i]] -=1
                    n -= 1
                else:
                    i += 1
        return dict_bo

    def check_get_card(self, Card):
        if Card == None:
            # input()
            return False
        auto_color = self.stocks["auto_color"]
        for i in Card.stocks.keys():
            if self.stocks[i] + self.stocks_const[i] < Card.stocks[i]:
                if self.stocks[i] + self.stocks_const[i] + auto_color >= Card.stocks[i]:
                    auto_color = self.stocks[i] + self.stocks_const[i] + auto_color - Card.stocks[i]
                else:
                    return False
        return True