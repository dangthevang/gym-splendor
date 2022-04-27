from base import player
import random
player_02 = player.Player("QueenOfGame", 0)
    
def list_target_cards(board):
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
                    if check_any_card_5score_onhand() == False:
                        target_cards_rank.append(card)
                    else:
                        continue
                if card.score == 4:
                    if check_any_card_4score_onhand() == False:
                        target_cards_rank.append(card)
                    else:
                        continue
                if card.score == 3:
                    if check_any_card_3score_onhand() == False:
                        target_cards_rank.append(card)
                    else:
                        continue
                target_cards_rank.append(card)
    target_cards_rank_upgrade = []
    if len(player_02.card_upside_down) > 0:
        for item in player_02.card_upside_down:
            for card in target_cards_rank:
                if card.stocks[item.type_stock] > 0:
                    target_cards_rank_upgrade.append(card)
                if item.stocks[card.type_stock] > 0:
                    target_cards_rank_upgrade.append(card)
    else:
        target_cards_rank_upgrade = target_cards_rank.copy()
    return target_cards_rank_upgrade

def list_color_on_board(board):
    dict_start = {"red" : 0, "white": 0, "blue": 0, "green": 0,"black": 0}
    
    type = ["III", "II"]
    for i in type:
        for card in board.dict_Card_Stocks_Show[i]:
            if card in list_target_cards(board):
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

def list_holding_cards():
    A = []
    if len(player_02.card_upside_down) > 0:
        for item in player_02.card_upside_down:
            holding_cards = player_02.card_upside_down.copy()  
            holding_cards.remove(item)
            for card in holding_cards:
                if card.stocks[item.type_stock] > 0:
                    A.append(item)
        score = [3, 5, 4, 2, 1]
        for i in score:
            for item in player_02.card_upside_down:
                if item.score == i:
                    A.append(item)
    return A

def list_color_for_holdings(board):
    list_color_holding = []
    dict_start = {"red" : 0, "white": 0, "blue": 0, "green": 0,"black": 0}
    item = None
    if len(player_02.card_upside_down) > 0:
        item = list_holding_cards()[0]
        a = 0
        for color in list(item.stocks.keys()):
            if ( item.stocks[color] - player_02.stocks[color] - player_02.stocks_const[color] ) > a:
                if board.stocks[color] > 0: 
                    a = item.stocks[color] - player_02.stocks[color] - player_02.stocks_const[color]
                    if len(list_color_holding) > 0:                    
                        list_color_holding.insert(0,color)
                    else:
                        list_color_holding.append(color)
            if item.stocks[color] > 0:
                if board.stocks[color] > 0:
                    if color not in list_color_holding:
                        list_color_holding.append(color)
        if len(player_02.card_upside_down) > 1:
            list_cards = list_holding_cards().copy()
            list_cards.pop(0)
            for card in list_cards:
                for color in card.stocks.keys():
                    dict_start[color] += card.stocks[color] 
            for color in dict_start.keys():
                dict_start[color] -= ( player_02.stocks[color] + player_02.stocks_const[color] )
            list_values = sorted(list(dict_start.values()),reverse=True)
            for value in list_values:
                for color in dict_start.keys():
                    if dict_start[color] == value:
                        if value > 0:
                            if board.stocks[color] > 0:
                                if color not in list_color_holding:
                                    list_color_holding.append(color)
    return list_color_holding

def color_3(board):
    color3 = None
    if len(list_color_for_holdings(board)) == 2:
        for color in board.stocks.keys():
            if board.stocks[color] > 0 and color not in list_color_for_holdings(board):
                if color != "auto_color":
                    color3 = color
    return color3

def color_3_on_board(board):
    color3 = None
    if len(list_color_on_board(board)) == 2:
        for color in board.stocks.keys():
            if board.stocks[color] > 0 and color not in list_color_on_board(board):
                if color != "auto_color":
                    color3 = color
    return color3

def list_color_no_target(board):
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
                        if color not in list_color_for_holdings(board):
                            color_no_target.append(color)
    return color_no_target

def list_token_can_get(board):
    nguyenlieucon = []
    for nguyenlieu in board.stocks.keys():
        if board.stocks[nguyenlieu] > 0 and nguyenlieu != "auto_color":
            nguyenlieucon.append(nguyenlieu)
    return nguyenlieucon

def get_important_token(board):
    token_can_get = list_token_can_get(board)
    dict_important_token = {}
    dict_important_token['red'] = 0
    dict_important_token['blue'] = 0
    dict_important_token['green'] = 0
    dict_important_token['white'] = 0
    dict_important_token['black'] = 0
    for card in player_02.card_upside_down:
        dict_important_token['red'] += card.stocks['red'] - player_02.stocks_const['red'] - player_02.stocks['red']
        dict_important_token['blue'] += card.stocks['blue'] - player_02.stocks_const['blue'] - player_02.stocks['blue']
        dict_important_token['green'] += card.stocks['green'] - player_02.stocks_const['green'] - player_02.stocks['green']
        dict_important_token['white'] += card.stocks['white'] - player_02.stocks_const['white'] - player_02.stocks['white']
        dict_important_token['black'] += card.stocks['black'] - player_02.stocks_const['black'] - player_02.stocks['black']
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

def list_color_return_when_holding(board):
    color_return = []
    for color in player_02.stocks.keys():
        if player_02.stocks[color] > 0 and color != "auto_color":
            if color not in list_color_for_holdings(board):
                color_return.append(color)
    list = list_color_for_holdings(board).copy()
    list.reverse()
    for color in list:
        if player_02.stocks[color] > 0 and color not in color_return:
            color_return.append(color)
    return color_return

def Luachonbothe(board,*args):
    dict_bo = {
        "red":0,
        "blue":0,
        "white":0,
        "green":0,
        "black":0,
        "auto_color": 0
    }
    dict_bd = player_02.stocks.copy()
    for x in args:
        dict_bd[x] += 1
    danhsachcon = list_color_return_when_holding(board).copy()
    
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
    return dict_bo

def dict_return(board,*args):
    dict_bo = {
        "red":0,
        "blue":0,
        "white":0,
        "green":0,
        "black":0,
        "auto_color": 0
    }
    dict_bd = player_02.stocks.copy()
    for x in args:
        dict_bd[x] += 1
    color_list = list_color_no_target(board).copy()
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

def list_cards_target_can_buy(board):
    cards_target_can_buy = []
    for card in list_holding_cards():
        if player_02.checkGetCard(card):
            cards_target_can_buy.append(card)
    for card in list_target_cards(board):
        if player_02.checkGetCard(card):
            cards_target_can_buy.append(card)
    if target_support_cards(board) != None:
        if player_02.checkGetCard(card):
            cards_target_can_buy.append(card)
    return cards_target_can_buy

def list_cards_on_board_can_buy(board):
    cards_on_board_can_buy = []
    type = ["III", "II", "I"]
    for i in type:
        for card in board.dict_Card_Stocks_Show[i]:
            if player_02.checkGetCard(card):
                cards_on_board_can_buy.append(card)
    return cards_on_board_can_buy

def check_any_card_5score_onhand():
    for card in player_02.card_upside_down:
        if card.score == 5:
            return True
    for card in player_02.card_open:
        if card.score == 5:
            return True
    return False

def check_any_card_4score_onhand():
    for card in player_02.card_upside_down:
        if card.score == 4:
            return True
    for card in player_02.card_open:
        if card.score == 4:
            return True
    return False

def check_any_card_3score_onhand():
    for card in player_02.card_upside_down:
        if card.score == 3:
            return True
    for card in player_02.card_open:
        if card.score == 3:
            return True
    return False

def theup(board):
    NL = []
    for nguyenlieu in board.dict_Card_Stocks_Show["III"][0].stocks.keys():
        max = 0
        for the in player_02.card_upside_down:
            if the.stocks[nguyenlieu] > max:
                the.stocks[nguyenlieu] = max
        if max > player_02.stocks[nguyenlieu]:
            NL.append(nguyenlieu)
    for n in NL:
        for the1 in board.dict_Card_Stocks_Show["III"]:
            if the1.type_stock == n:
                return the1


def target_support_cards(board):
    target_support_cards = []
    cardx = None
    type = ["II", "I"]
    if len(list_color_for_holdings(board)) > 0:
        for color in list_color_for_holdings(board):
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

def color_card_support(board):
    dict = {}
    color_support = []
    if target_support_cards(board) != None:
        dict = target_support_cards(board).stocks.copy()
        list_values = sorted(list(dict.values()),reverse=True)
        for value in list_values:
            for color in dict.keys():
                if dict[color] == value:
                    if value > 0:
                        if board.stocks[color] > 0:
                            color_support.append(color)
    return color_support

def color_3_support(board):
    color3_support = None
    for color in board.stocks.keys():
        if board.stocks[color] > 0:
            if color not in color_card_support(board):
                color3_support = color
    return color3_support

def action(board, arr_player):

    if len(list_cards_target_can_buy(board)) > 0:
        return player_02.getCard(list_cards_target_can_buy(board)[0],board)
    
    if len(list_target_cards(board)) > 0:
        if player_02.checkUpsiteDown():
            return player_02.getUpsideDown(list_target_cards(board)[0],board, Luachonbothe(board,"auto_color"))

    if len(player_02.card_upside_down) > 0:
        if sum(player_02.stocks.values()) <= 8:            
            if len(list_color_for_holdings(board)) > 0:
                if player_02.checkOneStock(board,list_color_for_holdings(board)[0]):
                    return player_02.getOneStock(list_color_for_holdings(board)[0],board,Luachonbothe(board,list_color_for_holdings(board)[0],list_color_for_holdings(board)[0]))
            
            if len(list_color_for_holdings(board)) > 2:
                if player_02.checkThreeStocks(board,list_color_for_holdings(board)[0],list_color_for_holdings(board)[1],list_color_for_holdings(board)[2]):
                    return player_02.getThreeStocks(list_color_for_holdings(board)[0],list_color_for_holdings(board)[1],list_color_for_holdings(board)[2],
                                                    board,
                                                    Luachonbothe(board,list_color_for_holdings(board)[0],list_color_for_holdings(board)[1],list_color_for_holdings(board)[2]))
            if len(list_color_for_holdings(board)) == 2 :               
                if player_02.checkOneStock(board,list_color_for_holdings(board)[1]):
                    return player_02.getOneStock(list_color_for_holdings(board)[1],board,Luachonbothe(board,list_color_for_holdings(board)[1],list_color_for_holdings(board)[1]))
                if color_3(board) != None:
                    return player_02.getThreeStocks(list_color_for_holdings(board)[0],list_color_for_holdings(board)[1],color_3(board),
                                                    board,
                                                    Luachonbothe(board,
                                                    list_color_for_holdings(board)[0],list_color_for_holdings(board)[1],color_3(board)))
                                            
            if len(list_color_for_holdings(board)) == 1 :
                if len(list_color_no_target(board)) >= 2:
                    if player_02.checkThreeStocks(board,list_color_for_holdings(board)[0],list_color_no_target(board)[0],list_color_no_target(board)[1]):                     
                        return player_02.getThreeStocks(list_color_for_holdings(board)[0],list_color_no_target(board)[0],list_color_no_target(board)[1],
                                                    board,
                                                    Luachonbothe(board,list_color_for_holdings(board)[0],list_color_no_target(board)[0],list_color_no_target(board)[1]))
                if target_support_cards(board) != None:
                    if len(color_card_support(board)) > 2:
                        if player_02.checkThreeStocks(board,color_card_support(board)[0],color_card_support(board)[1],color_card_support(board)[2]):
                            return player_02.getThreeStocks(color_card_support(board)[0],color_card_support(board)[1],color_card_support(board)[2],board,
                                                        Luachonbothe(board,color_card_support(board)[0],color_card_support(board)[1],color_card_support(board)[2]))                                            
                    for color in color_card_support(board):
                        if player_02.checkOneStock(board,color):
                            return player_02.getOneStock(color,board,Luachonbothe(board,color,color))
                    if len(color_card_support(board)) == 2:
                        if color_3_support(board) != None:
                            if player_02.checkThreeStocks(board,color_card_support(board)[0],color_card_support(board)[1],color_3_support(board)):
                                return player_02.getThreeStocks(color_card_support(board)[0],color_card_support(board)[1],color_3_support(board),board,
                                                                Luachonbothe(board,color_card_support(board)[0],color_card_support(board)[1],color_3_support(board)))
                        for color in color_card_support(board):
                            if player_02.checkOneStock(board,color):
                                return player_02.getOneStock(color,board,Luachonbothe(board,color,color))                
                    if player_02.checkUpsiteDown():
                        return player_02.getUpsideDown(target_support_cards(board),board,{})
                if theup(board) != None:
                    if player_02.checkUpsiteDown():                  
                        return player_02.getUpsideDown(theup(board),board,Luachonbothe(board,"auto_color"))
                if target_support_cards(board) != None:
                    if player_02.checkGetCard(target_support_cards(board)):
                        return player_02.getCard(target_support_cards(board),board)
                if theup(board) != None:                
                    if player_02.checkGetCard(theup(board)):
                        return player_02.getCard(theup(board),board)
                if len(list_color_no_target(board)) >= 3:
                    if player_02.checkThreeStocks(board,list_color_no_target(board)[0],list_color_no_target(board)[1],list_color_no_target(board)[2]):
                        return player_02.getThreeStocks(list_color_no_target(board)[0],list_color_no_target(board)[1],list_color_no_target(board)[2],
                                                        board,
                                                        Luachonbothe(board,list_color_no_target(board)[0],list_color_no_target(board)[1],list_color_no_target(board)[2]))
                if len(list_color_no_target(board)) > 0:
                    for color in list_color_no_target(board):
                        if player_02.checkOneStock(board,color):
                            return player_02.getOneStock(color,board,{})            

        if sum(player_02.stocks.values()) == 9:
            for color in list_color_for_holdings(board):
                if player_02.checkOneStock(board,color):
                    return player_02.getOneStock(color,board,Luachonbothe(board,color,color))
            if player_02.checkUpsiteDown():
                if len(list_target_cards(board)) > 0:
                    return player_02.getUpsideDown(list_target_cards(board)[0],board, Luachonbothe(board,"auto_color"))
                if target_support_cards(board) != None:
                    return player_02.getUpsideDown(target_support_cards(board),board,{})
                if theup(board) != None:
                    return player_02.getUpsideDown(theup(board),board,Luachonbothe(board,"auto_color"))                                 
            if len(list_color_for_holdings(board)) == 2:
                if color_3_on_board(board) != None:
                    return player_02.getThreeStocks(list_color_for_holdings(board)[0],list_color_for_holdings(board)[1],color_3_on_board(board),
                                                board,
                                                Luachonbothe(board,list_color_for_holdings(board)[0],list_color_for_holdings(board)[1],color_3_on_board(board)))        
            if target_support_cards(board) != None:
                if player_02.checkGetCard(target_support_cards(board)):
                    return player_02.getCard(target_support_cards(board),board)
            if theup(board) != None:
                if player_02.checkGetCard(theup(board)):
                    return player_02.getCard(theup(board),board)
        if sum(player_02.stocks.values()) == 10:
            if target_support_cards(board) != None:
                if player_02.checkUpsiteDown():
                    return player_02.getUpsideDown(target_support_cards(board),board,Luachonbothe(board,"auto_color"))
            if theup(board) != None:
                if player_02.checkUpsiteDown():
                    return player_02.getUpsideDown(theup(board),board,Luachonbothe(board,"auto_color"))            
            if target_support_cards(board) != None:
                if player_02.checkGetCard(target_support_cards(board)):
                    return player_02.getCard(target_support_cards(board),board)
            if theup(board) != None:
                if player_02.checkGetCard(theup(board)):
                    return player_02.getCard(theup(board),board)
            if len(list_color_for_holdings(board)) > 0:
                for color in list_color_for_holdings(board):
                    if player_02.checkOneStock(board,color):
                        return player_02.getOneStock(color,board,Luachonbothe(board,color,color))
            if len(list_color_for_holdings(board)) == 2:
                if color_3_on_board(board) != None:
                    if player_02.checkThreeStocks(board,list_color_for_holdings(board)[0],list_color_for_holdings(board)[1],color_3_on_board(board)):               
                        return player_02.getThreeStocks(list_color_for_holdings(board)[0],list_color_for_holdings(board)[1],color_3_on_board(board),
                                                    board,
                                                    Luachonbothe(board,list_color_for_holdings(board)[0],list_color_for_holdings(board)[1],color_3_on_board(board)))                      
        
        if len(list_cards_on_board_can_buy(board)) > 0:
            for card in list_cards_on_board_can_buy(board):
                if card.score > 0:
                    if player_02.checkGetCard(list_cards_on_board_can_buy(board)[0]):
                        return player_02.getCard(card,board)
            for card in list_cards_on_board_can_buy(board):
                if player_02.checkGetCard(card):
                    return player_02.getCard(card,board)
        if len(list_color_on_board(board)) > 0:
            for color in list_color_on_board(board):
                if player_02.checkOneStock(board, color):
                    return player_02.getOneStock(color,board,Luachonbothe(board,color,color))
            if len(list_color_on_board(board)) > 2:
                if player_02.checkThreeStocks(board,list_color_on_board(board)[0],list_color_on_board(board)[1],list_color_on_board(board)[2]):
                    return player_02.getThreeStocks(list_color_on_board(board)[0],list_color_on_board(board)[1],list_color_on_board(board)[2],
                                                    board,
                                                    Luachonbothe(board,
                                                    list_color_on_board(board)[0],list_color_on_board(board)[1],list_color_on_board(board)[2]))

    if len(player_02.card_upside_down) == 0:

        if len(list_color_on_board(board)) > 0:
            for color in list_color_on_board(board):
                if player_02.checkOneStock(board, color):
                    return player_02.getOneStock(color,board,dict_return(board,color,color))
            if len(list_color_on_board(board)) > 2:
                if player_02.checkThreeStocks(board,list_color_on_board(board)[0],list_color_on_board(board)[1],list_color_on_board(board)[2]):
                    return player_02.getThreeStocks(list_color_on_board(board)[0],list_color_on_board(board)[1],list_color_on_board(board)[2],
                                                    board,
                                                    dict_return(board,
                                                    list_color_on_board(board)[0],list_color_on_board(board)[1],list_color_on_board(board)[2]))
            if len(list_color_on_board(board)) == 2:
                if color_3(board) != None:
                    return player_02.getThreeStocks(list_color_on_board(board)[0],list_color_on_board(board)[1],color_3_on_board(board),
                                                    board,
                                                    dict_return(board,
                                                    list_color_on_board(board)[0],list_color_on_board(board)[1],color_3_on_board(board)))      

        if sum(player_02.stocks.values()) <= 8:
            for color in list_color_no_target(board):
                if player_02.checkOneStock(board,color):
                    return player_02.getOneStock(color,board,{})
            if len(list_color_no_target(board)) >= 3:
                return player_02.getThreeStocks(list_color_no_target(board)[0],list_color_no_target(board)[1],list_color_no_target(board)[2],
                                                board,
                                                dict_return(board,list_color_no_target(board)[0],list_color_no_target(board)[1],list_color_no_target(board)[2]))
        
        if sum(player_02.stocks.values()) == 9:
            for color in list_color_no_target(board):
                if player_02.checkOneStock(board,color):
                    return player_02.getOneStock(color,board,dict_return(board,color,color))
    
    if theup(board) != None:
        if player_02.checkGetCard(theup(board)):
            return player_02.getCard(theup(board),board)
    
    if len(list_cards_on_board_can_buy(board)) > 0:
        for card in list_cards_on_board_can_buy(board):
            if card.score > 0:
                return player_02.getCard(card,board)
        return player_02.getCard(card,board)
    return board  