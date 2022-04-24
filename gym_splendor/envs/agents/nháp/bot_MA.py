from base import player

player_03 = player.Player("MINH", 0)


def action(board, arr_player, turn):
    dict_type_card_show = statistic_type_card(board)
    blue_green_white = dict_type_card_show['blue'] + dict_type_card_show['green'] + dict_type_card_show['white']
    black_red_white = dict_type_card_show['black'] + dict_type_card_show['red'] + dict_type_card_show['white']
    if blue_green_white > black_red_white:
        sub_color = ['blue', 'green', 'white']
    else:
        sub_color = ['white', 'black', 'red']
    # print('sub_color turn {} {}'.format(turn, sub_color))
    lst_theaim = []
    # turn < = 5
    dict_value = {}
    for key in board.dict_Card_Stocks_Show.keys():
        if key != 'Noble':
            # neu lay duoc the nao => lay luon
            for card_ in board.dict_Card_Stocks_Show[key]:
                if card_.score >=4:
                    if player_03.checkGetCard(card_):
                        # print('1. minh lay the ', card_.score, card_.stocks)
                        return player_03.getCard(card_, board)
                elif card_.score == 3:
                    if player_03.checkGetCard(card_):
                        # print('1. minh lay the ', card_.score, card_.stocks)
                        return player_03.getCard(card_, board)
                elif card_.score == 2:
                    if player_03.checkGetCard(card_):
                        # print('1. minh lay the ', card_.score, card_.stocks)
                        return player_03.getCard(card_, board)
                elif card_.score == 1:
                    if player_03.checkGetCard(card_):
                        # print('1. minh lay the ', card_.score, card_.stocks)
                        return player_03.getCard(card_, board)
                else:
                    if player_03.checkGetCard(card_):
                        return player_03.getCard(card_, board)

    # neu turn < 10 : chi aim the I
    for key in board.dict_Card_Stocks_Show.keys():
        if turn <= 17:
            # lay tai nguyen dua vao gia trị cua the
            if key == "I":
                for card in board.dict_Card_Stocks_Show[key]:
                    dict_value[card] = statistic_card_value(board, card, sub_color)
        else:
            if key != 'Noble':
                for card in board.dict_Card_Stocks_Show[key]:
                    dict_value[card] = statistic_card_value(board, card, sub_color)

    # lay the co value nho nhat
    card_aim = sorted_dict_n(dict_value, 5, descending=False)
    for card_aim_key in card_aim.keys():
        # print("card aim: ", key_.score, key_.type_stock, key_.stocks)
        if card_aim_key.score >= 2:
            # up the nay
            if player_03.checkUpsiteDown():
                # print('2. minh up the ', card_aim_key.score, card_aim_key.stocks)
                return player_03.getUpsideDown(card_aim_key, board, nlbo('auto_color'))
            else:
                lst_theaim.append(card_aim_key)
        else:
            # lay nguyen lieu cho the nayf
            # print('3. them the vao the aim ', card_aim_key.score, card_aim_key.stocks)
            lst_theaim.append(card_aim_key)
            # print('3.1 lst the aim ', lst_theaim)

    # lay tai nguyen minh dang co - so sanh voi tai nguyen can de lay the
    # suy ra tai nguyen can lay
    if len(player_03.card_upside_down) >= 1:
        theup_recent = player_03.card_upside_down[0]
    else:
        # print('out of index 6', lst_theaim, len(lst_theaim))
        theup_recent = lst_theaim[0]

    # print('3.2 the dang huong toi ', theup_recent.score, theup_recent.stocks)
    lst_nl_dangco = player_03.stocks
    for i, j in player_03.stocks_const.items():
        lst_nl_dangco[i] += j
    # print('4. nl dang co cua minh ', lst_nl_dangco)

    dict_nl_canlay = {}
    for stock_type, stock_num in theup_recent.stocks.items():
        if stock_type in lst_nl_dangco:
            if stock_num > lst_nl_dangco[stock_type]:
                dict_nl_canlay[stock_type] = stock_num - lst_nl_dangco[stock_type]
        else:
            dict_nl_canlay[stock_type] = stock_num

    # print('5. nl can lay cua minh ', dict_nl_canlay)

    ## check neu co > 3 loai nguyen lieu => lay
    lst_nl_canlay_keys = list(dict_nl_canlay.keys())
    # print('5.2 list nl key can lay ', lst_nl_canlay_keys)
    if len(lst_nl_canlay_keys) >= 3:
        if player_03.checkThreeStocks(board, lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]):
            # print('6. minh lay 3 nl ', lst_nl_canlay_keys[:4])
            return player_03.getThreeStocks(lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2], board,
                                            nlbo(lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]))
        else:
            lst_temp = []
            for nl_key, nl_value in board.stocks.items():
                if nl_key not in lst_nl_canlay_keys and nl_value != 0 and nl_key != 'auto_color':
                    lst_temp.append(nl_key)
            # print('6.1 nl con co the lay ', lst_temp)
            for nl in lst_temp:
                if nl not in lst_nl_canlay_keys:
                    lst_nl_canlay_keys.append(nl)
            for nl in lst_nl_canlay_keys:
                if board.stocks[nl] == 0:
                    lst_nl_canlay_keys.remove(nl)

            return player_03.getThreeStocks(lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2], board,
                                            nlbo(lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]))
    ## check neu co < 3 loai => pick random 1 cai tu nguyen lieu con it tren ban
    else:
        nl_hiem = tim_nl_hiem(board, n=5)
        lst_nl_se_lay = check_nl_can_lay(lst_nl_canlay_keys, nl_hiem)
        # print('7 list nl se lay ', lst_nl_se_lay)
        if len(lst_nl_se_lay) >= 3:
            if player_03.checkThreeStocks(board, lst_nl_se_lay[0], lst_nl_se_lay[1], lst_nl_se_lay[2]):
                # print('7.1. minh lay 3 nl ', lst_nl_se_lay[:4])
                return player_03.getThreeStocks(lst_nl_se_lay[0], lst_nl_se_lay[1], lst_nl_se_lay[2], board,
                                                nlbo(lst_nl_se_lay[0], lst_nl_se_lay[1], lst_nl_se_lay[2]))
            else:
                lst_temp = []
                for nl_key, nl_value in board.stocks.items():
                    if nl_key not in list(lst_nl_se_lay.keys()) and nl_value != 0 and nl_key != 'auto_color':
                        lst_temp.append(nl_key)
                # print('7.2 nl con co the lay ', lst_temp)
                for nl in lst_temp:
                    if nl not in lst_nl_se_lay:
                        lst_nl_se_lay.append(nl)
                for nl in lst_nl_se_lay:
                    if board.stocks[nl] == 0:
                        lst_nl_se_lay.remove(nl)
                return player_03.getThreeStocks(lst_nl_se_lay[0], lst_nl_se_lay[1], lst_nl_se_lay[2], board,
                                                nlbo((lst_nl_se_lay[0], lst_nl_se_lay[1], lst_nl_se_lay[2])))
        elif len(lst_nl_se_lay) >= 1:
            if player_03.checkOneStock(board, lst_nl_se_lay[0]):
                # print('8. minh lay 1 nl ', lst_nl_se_lay[0])
                return player_03.getOneStock(lst_nl_se_lay[0], board,
                                             nlbo(lst_nl_se_lay[0], lst_nl_se_lay[0]))
            else:
                # print('8.1. minh lay 3 nl')
                lst_temp = []
                for nl_key, nl_value in board.stocks.items():
                    if nl_key not in lst_nl_se_lay and nl_value != 0 and nl_key != 'auto_color':
                        lst_temp.append(nl_key)
                # print('8.2 nl con co the lay ', lst_temp)
                for nl in lst_temp:
                    if nl not in lst_nl_se_lay:
                        lst_nl_se_lay.append(nl)

                for nl in lst_nl_se_lay:
                    if board.stocks[nl] == 0:
                        lst_nl_se_lay.remove(nl)

                # print('8.3 minh lay 3 nl la ', lst_nl_se_lay[:4])
                if len(lst_nl_se_lay) >= 3:
                    return player_03.getThreeStocks(lst_nl_se_lay[0], lst_nl_se_lay[1], lst_nl_se_lay[2], board,
                                                    nlbo(lst_nl_se_lay[0], lst_nl_se_lay[1], lst_nl_se_lay[2]))
                if len(lay_1nl_co_the(board)) >= 1 and player_03.checkOneStock(board, lay_1nl_co_the(board)[0]):
                    return player_03.getOneStock(lay_1nl_co_the(board)[0], board,
                                                 nlbo(lay_1nl_co_the(board)[0], lay_1nl_co_the(board)[0]))
                elif len(lay_3nl_co_the(board)) >= 3 and player_03.checkThreeStocks(board, lay_3nl_co_the(board)[0],
                                                                                    lay_3nl_co_the(board)[1],
                                                                                    lay_3nl_co_the(board)[2]):
                    return player_03.getThreeStocks(lay_3nl_co_the(board)[0], lay_3nl_co_the(board)[1],
                                                    lay_3nl_co_the(board)[2], board,
                                                    nlbo(lay_3nl_co_the(board)[0], lay_3nl_co_the(board)[1],
                                                    lay_3nl_co_the(board)[2]))
                elif lay_duynhat_1nl(board) != None:
                    if player_03.checkOneTwoStock(board, lay_duynhat_1nl(board), 'Null'):
                        return player_03.getOneTwoStock(lay_duynhat_1nl(board), "Null", board, nlbo(lay_duynhat_1nl(board)))
                    else:
                        print('NO ACTION')
                        return board
                else:
                    print('NO ACTION')
                    return board
    if lay_duynhat_1nl(board) != None:
        if player_03.checkOneTwoStock(board, lay_duynhat_1nl(board), 'Null'):
            return player_03.getOneTwoStock(lay_duynhat_1nl(board, "Null", board, nlbo(lay_duynhat_1nl(board))))
        else:
            print('NO ACTION')
            return board

    print('NO ACTION')
    return board

def lay_duynhat_1nl(board):
    for stock_key, stock_value in board.stocks.items():
        if stock_value >= 1 and stock_key != 'auto_color':
            return stock_key
    return None

def lay_1nl_co_the(board):
    lay1stock = []
    for stock_key, stock_value in board.stocks.items():
        if stock_value > 3:
            lay1stock.append(stock_key)
    return lay1stock


def lay_3nl_co_the(board):
    lay3stocks = []
    for stock_key, stock_value in board.stocks.items():
        if stock_value >= 1:
            lay3stocks.append(stock_key)
    return lay3stocks


def bo_nl(lst_aim_card):
    lst_nl_dang_co = player_03.stocks.sopy()
    dict_co_the_bo = {}
    for key_stock, value_stock in lst_nl_dang_co.items():
        if key_stock not in list(lst_aim_card.keys()):
            dict_co_the_bo[key_stock] = value_stock
            if value_stock >= 3:
                return dict_co_the_bo

    for key_stock, value_stock in lst_nl_dang_co.items():
        if key_stock not in list(dict_co_the_bo.keys()):
            if value_stock > lst_nl_dang_co[key_stock]:
                dict_co_the_bo[key_stock] = value_stock - lst_nl_dang_co[key_stock]

    return dict_co_the_bo


def check_nl_can_lay(nl_can_lay, nl_hiem):
    final_list_nl = []
    for nl_hime_ in nl_hiem:
        if nl_hime_ in nl_can_lay and nl_hime_ != 'auto_color':
            final_list_nl.append(nl_hime_)

    for key in nl_can_lay:
        if key != 'auto_color' and key not in nl_can_lay:
            nl_can_lay.append(key)

    remove_dup = []
    for nl in nl_can_lay:
        if nl not in remove_dup and nl != 'auto_color':
            remove_dup.append(nl)
    return remove_dup


def tim_nl_hiem(board, n):
    dict_board_stock_remove_autocolor = {}
    for stock_key, stock_value in board.stocks.items():
        if stock_key != 'auto_color':
            dict_board_stock_remove_autocolor[stock_key] = stock_value
    # print('5.1 nl hiem bo auto color ', dict_board_stock_remove_autocolor)
    lst = list(sorted_dict_n(dict_board_stock_remove_autocolor, n=n, descending=False).keys())
    return lst


def statistic_card_value(board, card, sub_color):
    # note : giá trị / giá cả ( số điểm / số nguyên liệu cần - số nl const stocks)
    const_stocks = player_03.stocks_const.copy()
    count_soluongnl = 0
    real_value = {}
    if card.type_stock in sub_color:
        for key, value in card.stocks.items():
            if key in list(const_stocks.keys()):
                if const_stocks[key] < value:
                    real_value[key] = value - const_stocks[key]
            else:
                real_value[key] = value
    tong_nl_thuc = sum(real_value.values())

    if card.type_stock in sub_color:
        for key, value in real_value.items():
            if value > 0:
                count_soluongnl += 1
    # index 1 = tong so nguyen lieu can / so luong nguyen lieu ( can nho )
    index1 = tong_nl_thuc / (count_soluongnl + 1)

    # index2 = tong so tai nguyen / tong so diem ( can nho )
    index2 = tong_nl_thuc / (card.score + 1)

    # index3 = ty le tai nguyen tren ban
    # index3.1 = so luong tai nguyen 1 can tren the / so luong tai nguyen 1 dang co tren ban ( can nho )
    lst_index3 = []
    for key_stock, number_stock in card.stocks.items():
        num_stock_avai_board = board.stocks[key_stock]
        if num_stock_avai_board > 0:
            lst_index3.append(number_stock / num_stock_avai_board)
    index3 = sum(lst_index3) / len(lst_index3)

    # index = trung binh 3 index
    index = (0.95 * index1 + 0.05 * index2 + 0.05 * index3)
    return index


def statistic_stock_in_card_show(board):
    dict_nl = {
        "red": 0,
        "blue": 0,
        "green": 0,
        "white": 0,
        "black": 0,
    }
    for key in board.dict_Card_Stocks_Show.keys():
        for card in board.dict_Card_Stocks_Show[key]:
            for nl in dict_nl.keys():
                dict_nl[nl] += card.stocks[nl]
    return dict_nl


def statistic_type_card(board):
    dict_nl = {
        "red": 0,
        "blue": 0,
        "green": 0,
        "white": 0,
        "black": 0,
    }
    for key in board.dict_Card_Stocks_Show.keys():
        if key != "Noble":
            for card in board.dict_Card_Stocks_Show[key]:
                dict_nl[card.type_stock] += 1
    return dict_nl


def sorted_dict_n(dictionary, n, descending=None):
    final = {}
    ilistofTuples = sorted(dictionary.items(), key=lambda x: x[1])

    if descending == True:
        lst = ilistofTuples[:n]
        for elem in lst:
            final[elem[0]] = elem[1]
    elif descending == False:
        lst = ilistofTuples[::-1][:n]
        for elem in lst:
            final[elem[0]] = elem[1]
    return final



def nlbo(*args):
    dict_nl_ht = player_03.stocks
    # print('dict_nl_ht: ', dict_nl_ht)
    for color in args:
        dict_nl_ht[color] += 1
    snl = sum(list(dict_nl_ht.values()))
    # print('snl ', snl)
    dict_bo = {
        "red": 0,
        "blue": 0,
        "green" : 0,
        "black": 0,
        "white": 0,
        "auto_color": 0
    }
    if snl <= 10 :
        return dict_bo
    else:
        snllcb = snl-10
        dict_nl_theup = {}
        if len(player_03.card_upside_down) >= 1:
            theup = player_03.card_upside_down[0]
            nl_can_cho_theup = theup.stocks
            for key_stock, value_stock in dict_nl_ht.items():
                if key_stock in list(dict_nl_theup.keys()):
                    if value_stock > dict_nl_theup[key_stock]:
                        dict_bo[key_stock] += 1
                        if sum(dict_bo.values()) == snllcb:
                            return dict_bo
                elif key_stock not in list(dict_nl_theup.keys()):
                    if dict_nl_ht[key_stock] != 0 :
                        dict_bo += 1
                        if sum(dict_bo.values()) == snllcb:
                            return dict_bo

        if sum(dict_bo.values()) < snllcb:
            # print('slnlb ', snllcb)
            # print('sorted in snllcb', sorted_dict_n(dict_nl_ht, n=snllcb, descending=False))
            for nl_key in list(sorted_dict_n(dict_nl_ht, n = snllcb, descending=False).keys()):
                dict_bo[nl_key] += 1
                if sum(dict_bo.values()) == snllcb:
                    return dict_bo
        return dict_bo