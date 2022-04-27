from base import player
import random
import math

player_04 = player.Player("KingOfDestruction", 0)
def action(board, arr_player):
    return turn(board, player_04)

def price_card(card, player):
    price = 0
    for typestock in list(card.stocks.keys()):
        price += card.stocks[typestock] - player.stocks_const[typestock]
    if price <= 0:
        return 0.1
    return price


def turn(board, player_04):
    thecothelay = list_card_can_buy(board, player_04)    
    nguyenlieucothelay2 = listnguyenlieulay2(board)
    nguyenlieucon = listnguyenlieucon(board)    
    #action

    #Lấy thẻ
    if len(thecothelay) > 0:
        list_card_value = []
        for card in thecothelay:
            #lấy thẻ có điểm
            if card.score > 1:
                card_value = card.score/price_card(card, player_04)
                list_card_value.append([card, card_value])
        if len(list_card_value) > 0:
            card_get = list_card_value[0][0]
            card_value = list_card_value[0][1]
            for item in list_card_value:
                if item[1] > card_value:
                    card_get = item[0]
                    card_value = item[1]
            return player_04.getCard(card_get, board)
        else:
            #lấy thẻ để lấy noble
            thecothelay = get_card_to_get_noble(board)
            if thecothelay != None:
                for card in thecothelay:
                    if card.score == 0:
                        card_value = math.sqrt(sum(list(card.stocks.values())) + 1.78)
                        list_card_value.append([card, card_value])
                    elif card.score > 0:
                        card_value = sum(list(card.stocks.values()))/card.score
                        list_card_value.append([card, card_value])
                # if len(list_card_value) > 0:
                card_get = list_card_value[0][0]
                card_value = list_card_value[0][1]
                for item in list_card_value:
                    if item[1] < card_value:
                        card_get = item[0]
                        card_value = item[1]
                
                return player_04.getCard(card_get, board)
            else:
                #lấy thẻ rẻ nhất còn lại, có thể cải thiện thành kiểu khác
                thecothelay = list_card_can_buy(board, player_04)
                for card in thecothelay:
                    if card.score == 0:
                        card_value = math.sqrt(sum(list(card.stocks.values())) + 1.78)
                        list_card_value.append([card, card_value])
                    else:
                        card_value = sum(list(card.stocks.values()))/card.score
                        list_card_value.append([card, card_value])
                card_get = list_card_value[0][0]
                card_value = list_card_value[0][1]
                for item in list_card_value:
                    if item[1] < card_value:
                        card_get = item[0]
                        card_value = item[1]
                return player_04.getCard(card_get, board)
      
    # không lấy được thẻ thì lấy token
    if sum(list(player_04.stocks.values())) <= 7:
        dict_token_important = get_important_token(board)
        # if len(dict_token_important) > 0:
            # for token in list(dict_token_important.keys()):
            #     if token not in nguyenlieucon:
            #         del dict_token_important[token]
        if len(dict_token_important) >= 3:
            return player_04.getThreeStocks(list(dict_token_important.keys())[0],
                                    list(dict_token_important.keys())[1],
                                    list(dict_token_important.keys())[2], board, {})
        elif len(dict_token_important) > 0 and len(nguyenlieucothelay2) > 0:

            for token in list(dict_token_important.keys()):
                if token not in nguyenlieucothelay2:
                    del dict_token_important[token]
            type_card = list(dict_token_important.keys())[0]
            value = list(dict_token_important.values())[0]
            for typecard in list(dict_token_important.keys()):
                # if dict_token_important[typecard] > value:
                #     value = dict_token_important[typecard]
                #     type_card = typecard
                if player_04.checkOneStock(board, typecard) == True:
                    return player_04.getOneStock(type_card, board, {})
        else:
            dict_token_choose = get_Three_Most_Token(board)
            for token in list(dict_token_choose.keys()):
                if token not in nguyenlieucon:
                    del dict_token_choose[token]

            if len(dict_token_choose) >= 3:
                return player_04.getThreeStocks(list(dict_token_choose.keys())[0],
                                        list(dict_token_choose.keys())[1],
                                        list(dict_token_choose.keys())[2], board, {})
            else:
                #có thể cải thiện đc
                if len(nguyenlieucothelay2) > 0:
                    #dict_token_choose = get_Three_Most_Token(board)
                    for token in list(dict_token_choose.keys()):
                        if token not in nguyenlieucothelay2:
                            del dict_token_choose[token]
                    # if len(dict_token_choose)
                    if len(dict_token_choose) > 0:
                        return player_04.getOneStock(list(dict_token_choose.keys())[0], board, {})    
                    else:
                        if player_04.checkUpsiteDown() == True:
                            return player_04.getUpsideDown(get_card_value(board), board, {})

    if sum(player_04.stocks.values()) > 7:
        #nếu có 8 token
        #khi chưa úp thẻ, ko có dict_important, nên bị pass turn # đã xong
        if sum(player_04.stocks.values()) < 9:
            dict_token_important = get_important_token(board)
            if len(dict_token_important) > 0:
                for token in list(dict_token_important.keys()):
                    if token not in nguyenlieucothelay2:
                        del dict_token_important[token]
            if len(dict_token_important) > 0:
                type_card = list(dict_token_important.keys())[0]
                value = list(dict_token_important.values())[0]
                for typecard in list(dict_token_important.keys()):
                    if player_04.checkOneStock(board, type_card) == True:
                        return player_04.getOneStock(type_card, board,{})
            #nếu ko lấy được 2token cùng loại thì sẽ auto úp thẻ
            if player_04.checkUpsiteDown() == True: 
                return player_04.getUpsideDown(get_card_value(board), board, {})
        #nếu có 9 token
        elif sum(player_04.stocks.values()) == 9:
            #nếu đã úp 3 thẻ, thì mình có thể đổi nguyên liệu trong bàn chơi, nếu ko bị pass turn
            if player_04.checkUpsiteDown() == True: 
                return player_04.getUpsideDown(get_card_value(board), board, {})
            else:
                dict_token_important = get_important_token(board)
                if len(dict_token_important) > 0 and len(nguyenlieucothelay2) > 0 :
                    for token in list(dict_token_important.keys()):
                        if token not in nguyenlieucothelay2:
                            del dict_token_important[token]
                    
                    if len(dict_token_important) > 0:
                        list_token = list(dict_token_important.keys())
                        bo = get_token_return(board, 1)
                        return player_04.getOneStock(list_token[0], board,{})
                    else:
                        dict_token_important = get_important_token(board)
                        for token in list(dict_token_important.keys()):
                            if token not in nguyenlieucon:
                                del dict_token_important[token]
                        if len(dict_token_important) > 2:
                            bo = get_token_return(board, 2)
                            return player_04.getThreeStocks(list(dict_token_important.keys())[0],
                                        list(dict_token_important.keys())[1],
                                        list(dict_token_important.keys())[2], board, {})
        else:

            bo = get_token_return(board, 1)
            # dict_token_not_important = get_token_return(board)
            # list_value = list(dict_token_not_important.values())
            # list_type_token = list(dict_token_not_important.keys())
            # list_token_return = []
            # count = 0
            # while count < len(dict_token_not_important):
            #     count += 1
            #     min_value = min(list_value)
            #     list_token_return.append(list_type_token[list_value.index(min_value)])
            #     list_type_token.remove(list_type_token[list_value.index(min_value)])
            #     list_value.remove(min_value)
                
            
            # for nguyenlieu in list_token_return:
            #     if player_04.stocks[nguyenlieu] > 0:
            #         bo[nguyenlieu] = 1
            #         break
           
            if player_04.checkUpsiteDown() == True: 
                return player_04.getUpsideDown(get_card_value(board), board, bo)
    return board





def get_Three_Most_Token(board):
    token_can_get = list_token_can_get(board)
    dict_most_token = {}
    dict_most_token['red'] = 0
    dict_most_token['blue'] = 0
    dict_most_token['green'] = 0
    dict_most_token['white'] = 0
    dict_most_token['black'] = 0
    list_type = ['III', 'II', 'I']
    #xác định 3 nguyên liệu phổ biến nhất
    for i in list_type:
        for card in board.dict_Card_Stocks_Show[i]:
            dict_most_token['red'] += card.stocks['red'] - player_04.stocks_const['red']
            dict_most_token['blue'] += card.stocks['blue'] - player_04.stocks_const['blue']
            dict_most_token['green'] += card.stocks['green'] - player_04.stocks_const['green']
            dict_most_token['white'] += card.stocks['white'] - player_04.stocks_const['white']
            dict_most_token['black'] += card.stocks['black'] - player_04.stocks_const['black']

    list_token = list(dict_most_token.keys())
    list_number_token = list(dict_most_token.values())
    dict_token_choose = {}
    count = 0

    while count < len(list_token):
        count += 1
        # for token in list_token:
        # if list_token[list_number_token.index(max(list_number_token))] in token_can_get:
        dict_token_choose[list_token[list_number_token.index(max(list_number_token))]] = max(list_number_token)
        
        list_token.remove(list_token[list_number_token.index(max(list_number_token))])
        list_number_token.remove(max(list_number_token))
    return dict_token_choose

def token_of_player(board, player):
    token_of_player = []
    for token in list(player.stocks.keys()):
        if player.stocks[token] > 0:
            token_of_player.append(token)

    return token_of_player

def get_token_return(board, number_bo):
    '''
    #note: nếu đã úp thẻ thì trả token mà có ít tác dụng nhất trong việc lật thẻ, còn nếu chưa úp thẻ thì
    trả token kém phổ biến nhất trong các thẻ đang lật trên bàn chơi
    '''
    dict_token_not_important = {}
    token_can_return = token_of_player(board, player_04)
    count = 0
    bo = {}
    
    if len(player_04.card_upside_down) > 0:
        dict_important_token = {}
        dict_important_token['red'] = 0
        dict_important_token['blue'] = 0
        dict_important_token['green'] = 0
        dict_important_token['white'] = 0
        dict_important_token['black'] = 0
        for card in player_04.card_upside_down:
            dict_important_token['red'] += card.stocks['red'] - player_04.stocks_const['red'] - player_04.stocks['red']
            dict_important_token['blue'] += card.stocks['blue'] - player_04.stocks_const['blue'] - player_04.stocks['blue']
            dict_important_token['green'] += card.stocks['green'] - player_04.stocks_const['green'] - player_04.stocks['green']
            dict_important_token['white'] += card.stocks['white'] - player_04.stocks_const['white'] - player_04.stocks['white']
            dict_important_token['black'] += card.stocks['black'] - player_04.stocks_const['black'] - player_04.stocks['black']
        list_token = list(dict_important_token.keys())
        list_number_token = list(dict_important_token.values())
        
        while count < len(list_token):
            count += 1
            if list_token[list_number_token.index(min(list_number_token))] in token_can_return:
                dict_token_not_important[list_token[list_number_token.index(min(list_number_token))]] = min(list_number_token)
            list_token.remove(list_token[list_number_token.index(min(list_number_token))])
            list_number_token.remove(min(list_number_token))
    else:
        dict_most_token = get_Three_Most_Token(board)
        list_token = list(dict_most_token.keys())
        list_number_token = list(dict_most_token.values())
        while count < len(list_token):
            count += 1
            if list_token[list_number_token.index(min(list_number_token))] in token_can_return:
                dict_token_not_important[list_token[list_number_token.index(min(list_number_token))]] = min(list_number_token)
            list_token.remove(list_token[list_number_token.index(min(list_number_token))])
            list_number_token.remove(min(list_number_token))
    
    list_value = list(dict_token_not_important.values())
    list_type_token = list(dict_token_not_important.keys())
  
    list_token_return = []
    count = 0
    while count < len(dict_token_not_important):
        count += 1
        min_value = min(list_value)
        list_token_return.append(list_type_token[list_value.index(min_value)])
        list_type_token.remove(list_type_token[list_value.index(min_value)])
        list_value.remove(min_value)
    so_bo = 0
 
    index = 0
    while so_bo < number_bo:
        if player_04.stocks[list_token_return[index]] > 0:
            bo[list_token_return[index]] = 1
            so_bo += 1
        index += 1
    # for nguyenlieu in list_token_return:
    #     if player_04.stocks[nguyenlieu] > 0:
    #         bo[nguyenlieu] = 1
    #         break
    # return dict_token_not_important
    return bo

def target_card(board, player):
    list_card23 = board.dict_Card_Stocks_Show['III'] + board.dict_Card_Stocks_Show['II']
    list_target_card = []

    for card in list_card23:
        sum = 0
        for token in list(card.stocks.keys()):
            sum += max(card.stocks[token] - player.stocks[token] - player.stocks_const[token], 0)
        
        if sum < 2:
            list_target_card.append(card)

    return list_target_card

def get_important_token(board):
    token_can_get = list_token_can_get(board)
    dict_important_token = {}
    dict_important_token['red'] = 0
    dict_important_token['blue'] = 0
    dict_important_token['green'] = 0
    dict_important_token['white'] = 0
    dict_important_token['black'] = 0
    for card in list(player_04.card_upside_down + target_card(board, player_04)):
        dict_important_token['red'] += card.stocks['red'] - player_04.stocks_const['red'] - player_04.stocks['red']
        dict_important_token['blue'] += card.stocks['blue'] - player_04.stocks_const['blue'] - player_04.stocks['blue']
        dict_important_token['green'] += card.stocks['green'] - player_04.stocks_const['green'] - player_04.stocks['green']
        dict_important_token['white'] += card.stocks['white'] - player_04.stocks_const['white'] - player_04.stocks['white']
        dict_important_token['black'] += card.stocks['black'] - player_04.stocks_const['black'] - player_04.stocks['black']
    list_token = list(dict_important_token.keys())
    list_number_token = list(dict_important_token.values())
    dict_token_important = {}
    count = 0
    while count < len(list_token):
        if list_token[list_number_token.index(max(list_number_token))] in token_can_get:
            dict_token_important[list_token[list_number_token.index(max(list_number_token))]] = max(list_number_token)
        list_token.remove(list_token[list_number_token.index(max(list_number_token))])
        list_number_token.remove(max(list_number_token))
    return dict_token_important
    
def get_card_to_get_noble(board):
    dict_important_card = {}
    dict_important_card['red'] = 0
    dict_important_card['blue'] = 0
    dict_important_card['green'] = 0
    dict_important_card['white'] = 0
    dict_important_card['black'] = 0
    dict_card_value = {}
    thecothelay = list_card_can_buy(board, player_04)
    target_noble = []
    #tính xem với các thẻ noble thì cần mua thêm bao nhiêu thẻ các loại để lấy được thẻ noble
    for card in board.dict_Card_Stocks_UpsiteDown['Noble']:
        dict_card_to_get = {}
        for type_card in card.stocks.keys():
            dict_card_to_get[type_card] = max(card.stocks[type_card] - player_04.stocks_const[type_card] , 0)
        if sum(list(dict_card_to_get.values())) > 2:
            continue
        else:
            dict_card_value[card] = dict_card_to_get
            target_noble.append(sum(list(dict_card_to_get.values())))
    #chỉ hướng đến các thẻ noble còn thiếu dưới 3 thẻ
    list_card_noble = list(dict_card_value.keys())
    noble_should_get = []
    while len(target_noble) > 0:
        index_card = target_noble.index(min(target_noble))
        noble_should_get.append(list_card_noble[index_card])
        target_noble.remove(min(target_noble))
        list_card_noble.remove(list_card_noble[index_card])
    if len(noble_should_get) > 0:
        list_card_should_get = []
        for the in thecothelay:
            if the.type_stock in list(dict_card_value[noble_should_get[0]].keys()):
                list_card_should_get.append(the)

        return list_card_should_get

def get_card_value(board):
    dict_card_value = {}
    list_card_process = []
    list_card_get = []
    list_type_card = ['III', 'II', 'I']
    for type_card in list_type_card:
        for card in list(board.dict_Card_Stocks_Show[type_card]):
            if card.score == 0:
                list_card_process.append(card)
                sum = 1
                for token in list(card.stocks.keys()):
                    if card.stocks[token] - player_04.stocks[token] - player_04.stocks_const[token]  > 0:
                        sum += card.stocks[token] - player_04.stocks[token] - player_04.stocks_const[token]
                    else:
                        sum += 0
                
                dict_card_value[card.id] = math.sqrt(sum+3)
            else:
                sum = 1
                list_card_process.append(card)
                for token in card.stocks.keys():
                    if card.stocks[token] - player_04.stocks[token] - player_04.stocks_const[token] > 0:
                        sum += card.stocks[token]- player_04.stocks[token] - player_04.stocks_const[token]
                    else:
                        sum += 0
                dict_card_value[card] = sum/card.score
    dict_card_process = {}
    values = list(dict_card_value.values())
    count = 0
    list_card = list_card_process
    while count < len(list_card_process):
        count += 1
        list_card_get.append(list_card_process[values.index(min(values))])
        list_card.remove(list_card[values.index(min(values))])
        values.remove(min(values))    
    return list_card_get[0]

def list_card_can_buy(board, player):
    thecothelay = []
    if len(player.card_upside_down) > 0:
        for the in player.card_upside_down:
            if player.checkGetCard(the) == True:
                thecothelay.append(the)
    for the in board.dict_Card_Stocks_Show["III"]:
        if player.checkGetCard(the) == True:
            thecothelay.append(the)
    for the in board.dict_Card_Stocks_Show["II"]:
        if player.checkGetCard(the) == True:
            thecothelay.append(the)
    for the in board.dict_Card_Stocks_Show["I"]:
        if player.checkGetCard(the) == True:
            thecothelay.append(the)
    return thecothelay

def listnguyenlieulay2(board):
    nguyenlieucothelay2 = []
    for nguyenlieu in board.stocks.keys():
        if nguyenlieu != "auto_color" and player_04.checkOneStock(board,nguyenlieu) == True:
            nguyenlieucothelay2.append(nguyenlieu)
    return nguyenlieucothelay2

def listnguyenlieucon(board):
    nguyenlieucon = []
    for nguyenlieu in board.stocks.keys():
        if board.stocks[nguyenlieu] > 0 and nguyenlieu != "auto_color":
            nguyenlieucon.append(nguyenlieu)
    return nguyenlieucon

def target_noble_card(board, player_04):
    list_noble_card = board.dict_Card_Stocks_Show['Noble']
    dict_card_value = {}
    for card in list_noble_card:
        dict_thieu = {}
        for type_card in card.stocks.keys():
            if player_04.stocks_const[type_card] > card.stocks.keys():
                dict_thieu[type_card] = 0
            else:
                dict_thieu[type_card] = card.stocks.keys() - player_04.stocks_const[type_card]
        dict_card_value[card] = sum(list(dict_thieu.values()))

def virtual_player(board, player_04):
    player_virtual = player_04
    thecothelay = list_card_can_buy(board)    
    nguyenlieucothelay2 = listnguyenlieulay2(board)
    nguyenlieucon = listnguyenlieucon(board)     

#hàm list_token_can_get ngon
def list_token_can_get(board):
    nguyenlieucon = []
    for nguyenlieu in board.stocks.keys():
        if board.stocks[nguyenlieu] > 0 and nguyenlieu != "auto_color":
            nguyenlieucon.append(nguyenlieu)
    return nguyenlieucon