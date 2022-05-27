from ..base.player import Player
from copy import deepcopy
import random

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        the_co_the_lay = self.list_card_can_buy(state['Board'])
        # print('1111', the_co_the_lay)
        pick_token = self.value_function2(state['Board'])
        if type(pick_token) == list:
            pick_token = [x for x in pick_token if abs(x[1] - 0.0) > 1e-12]
        # print('2222, pick_token', pick_token)
        pick_gold = self.value_function3(state['Board'])
        # print('3333, pick_gold', pick_gold)
        dict_value_stock_const = self.value_function1(state['Board'])
        # print('4444, dict_value_stock_const', dict_value_stock_const)
        value_get_card = [-1000000, -1]
        if len(the_co_the_lay) > 0:
            value_get_card = [self.Q_function(state['Board'], 'get_card', the_co_the_lay[0], [], dict_value_stock_const), the_co_the_lay[0]]
            for card in the_co_the_lay[1:]:
                val_get_card = self.Q_function(state['Board'], 'get_card', card, [], dict_value_stock_const)
                if val_get_card > value_get_card[0]:
                    value_get_card = [val_get_card, card]
        
        dict_action = {'pick_gold':pick_gold[1] if pick_gold != None else -1000000, 'pick_token':sum(item[1] for item in pick_token), 'get_card':value_get_card[0]}
        sort_action = sorted(dict_action.items(),reverse= True, key = lambda x : x[1])
        # print(sort_action[0][0], 'sadfdgfdhfjgfhdgfsfdfnm')
        if sort_action[0][0] == 'pick_gold':
            
            stocks_return = []
            dict_bo = self.create_dict_return(state['Board'], sum(self.stocks.values()) + 1 - 10)
            for mau in dict_bo.keys():
                if dict_bo[mau] > 0:
                    for i in range(dict_bo[mau]):
                        stocks_return.append(mau)

            return [], pick_gold[0], stocks_return

        elif sort_action[0][0] == 'get_card':
            
            return [], value_get_card[1], []

        else:
            if pick_token.__len__() > 2:
                stocks = [pick_token[0][0], pick_token[1][0], pick_token[2][0]]
                dict_bo = self.create_dict_return(state['Board'], sum(self.stocks.values()) + 3 - 10)
                stocks_return = []
                for mau in dict_bo.keys():
                    if dict_bo[mau] > 0:
                        for i in range(dict_bo[mau]):
                            stocks_return.append(mau)
                
                # print(stocks, stocks_return)
                # print(stocks, stocks_return, '1111')
                return stocks, None, stocks_return
                
            elif pick_token.__len__() > 0:
                stocks = [pick_token[0][0], pick_token[0][0]]
                dict_bo = self.create_dict_return(state['Board'], sum(self.stocks.values()) + 2 - 10)
                stocks_return = []
                for mau in dict_bo.keys():
                    if dict_bo[mau] > 0:
                        for i in range(dict_bo[mau]):
                            stocks_return.append(mau)

                # print(stocks, stocks_return)
                # print(stocks, stocks_return, '2222')
                return stocks, None, stocks_return

        stocks = []
        for i in range(min(3, 10-sum(self.stocks.values()))):
            temp_list = [mau for mau in state['Board'].stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))
        
        if stocks.__len__() > 0:
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
        
        return stocks, None, stocks_return

    def create_dict_return(self, board, number_bo):
        dict_value_stock1 = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
        dict_value_stock2 = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
        list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III'] + self.card_upside_down
        for card in list_card_show:
            A = sum(card.stocks.values())/2
            B = card.score
            D = B**(1/A)
            C = 0
            for type_stock in dict_value_stock1.keys():
                C += min(self.stocks_const[type_stock] + self.stocks[type_stock], card.stocks[type_stock])
            for type_stock in dict_value_stock1.keys():
                if D > 0:
                    if card.stocks[type_stock] > 0 and self.stocks[type_stock] > 0:
                        dict_value_stock1[type_stock] = dict_value_stock1[type_stock] + D**(C-A) - D**(C - 1 - A) 
                    if card.stocks[type_stock] > 0 and self.stocks[type_stock] > 1:
                        dict_value_stock2[type_stock] = dict_value_stock2[type_stock] + D**(C-A) - D**(C - 2 - A)
        for type_stock in dict_value_stock1.keys():
            if self.stocks[type_stock] == 0:
                dict_value_stock1[type_stock] = 100
        id = 0
        pick_return = sorted(dict_value_stock1.items(), key = lambda x : x[1])
        dict_bo = {}
        while number_bo > 0:
            dict_bo[pick_return[id][0]] = 1
            id += 1
            number_bo -= 1
        return dict_bo

    def value_function1(self, board):
        dict_value_stock_const = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
        for card in board.dict_Card_Stocks_Show['Noble']:
            A = sum(card.stocks.values())/2
            B = 3
            D = B**(1/A)
            C = 0
            for type_stock in dict_value_stock_const.keys():
                C += min(self.stocks_const[type_stock], card.stocks[type_stock])
            for type_stock in dict_value_stock_const.keys():
                if card.stocks[type_stock] > 0:
                    dict_value_stock_const[type_stock] = dict_value_stock_const[type_stock] + D**(C + 1 - A)*C/(2*A)
        
        return dict_value_stock_const

    def value_function2(self, board):
        dict_value_stock1 = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
        dict_value_stock2 = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
        dict_number_card_stock = {'red':1, 'blue':1, 'green':1, 'white':1, 'black':1}
        list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III'] + self.card_upside_down
        for card in list_card_show:
            C1 = 0
            for type_stock in dict_value_stock1.keys():
                C1 += min(self.stocks[type_stock] + self.stocks_const[type_stock], card.stocks[type_stock])
            A = sum(card.stocks.values())/2
            B = card.score*C1/sum(card.stocks.values())
            D = B**(1/A)
            
            for type_stock in dict_value_stock1.keys():
                if card.stocks[type_stock] > 0 and board.stocks[type_stock] > 0:
                    dict_number_card_stock[type_stock] = dict_number_card_stock[type_stock] + 1
                    if B > 0:
                        dict_value_stock1[type_stock] = dict_value_stock1[type_stock] + D**(C1 + 1 - A)
                        if board.stocks[type_stock] > 3:
                            dict_value_stock2[type_stock] = dict_value_stock2[type_stock] + D**(C1+ 2 - A)

        for type_stock in dict_value_stock1.keys():
            dict_value_stock1[type_stock] /= dict_number_card_stock[type_stock]
            dict_value_stock2[type_stock] /= dict_number_card_stock[type_stock]
        pick3 = sorted(dict_value_stock1.items(),reverse= True, key = lambda x : x[1])[:3]
        pick2 = sorted(dict_value_stock2.items(), reverse= True, key = lambda x : x[1])[0]
        
        if pick2[1] > sum(item[1] for item in pick3):
            return [pick2]
        else:
            if board.stocks[pick3[2][0]] > 0:
                return pick3
            else:
                return {}

    def value_function3(self, board):
        list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III']
        dict_value_stock1 = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
        if list_card_show.__len__() == 0:
            return None

        choice = [list_card_show[0], -100]
        if len(self.card_upside_down) == 3:
            return choice
        gold = min(1,board.stocks['auto_color'])
        for card in list_card_show:
            C1 = 0
            for type_stock in dict_value_stock1.keys():
                C1 += min(self.stocks[type_stock] + self.stocks_const[type_stock], card.stocks[type_stock])
            A = sum(card.stocks.values())/2
            B = card.score*C1/sum(card.stocks.values())
            if B > 0:
                D = B**(1/A)
                val = D**(C1+gold-A) 
                
                try:
                    if val > choice[1]:
                        choice = [card, val]
                except:
                    choice = [card, val]

        return choice

    def Q_function(self, board, action, card, pick_token, dict_value_stock_const):
        Q_value = 0
        if action == 'get_card':
            Q_value = self.score +  sum(self.stocks_const.values()) + dict_value_stock_const[card.type_stock] + 2 + 2*card.score
            
            
        elif action == 'get_token':
            Q_value = self.score +  sum(self.stocks_const.values()) + sum(item[1] for item in pick_token)
        return Q_value

    def list_card_can_buy(self, board):
        thecothelay = []
        list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III'] + self.card_upside_down
        for the in list_card_show:
            if self.check_get_card(the) == True:
                thecothelay.append(the)
        return thecothelay