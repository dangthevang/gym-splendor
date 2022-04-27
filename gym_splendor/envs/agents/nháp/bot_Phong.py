from base import player
import random
import math
import operator
from operator import itemgetter
player_01    = player.Player("ChuaTeNgocLucBao", 0)
Loai_the = ["I", "II", "III"]
def action(board, arr_player):
    return HanhDongChinh(board, arr_player)
#loai nguyen lieu = lnl
def HanhDongChinh(board, arr_player):
    #lay the de du 15 diem
    if len(thecothemo(board)) > 0:
        x = []
        for the in thecothemo(board):
            if player_01.score + the.score >= 15:
                x.append(the)

        for diem in range(5, 0, -1):
            for card in x:
                if card.score == diem:
                    return player_01.getCard(card, board)
    #up the chien thang cua nguoi choi khac
    for i in thecothemocuanguoichoi(board, arr_player):
        id = 0
        if len(i) > 0:
            x = []
            for the in i:
                if arr_player[id].score + the.score >= 15:
                    x.append(the)
            for diem in range(5, 0, -1):
                for card in x:
                    if card.score == diem:
                        if player_01.checkUpsiteDown():
                            return player_01.getUpsideDown(card, board, Luachonbothe(board, "auto_color"))
        id += 1
        if id == 2:
            break
    #mo the up
    if len(latthedangup(board)) > 0:
        for diem in range(5, 0, -1):
            for card in latthedangup(board):
                if card.score == diem:
                    return player_01.getCard(card, board)

    #lay the noble neu co the
    if len(laythenoble(board)) > 0:
        return player_01.getCard(laythenoble(board)[0], board)

    #upthebandau
    if arr_player[0].score <= 13 and arr_player[1].score <= 13 and arr_player[2].score <= 13:
        if len(player_01.card_upside_down) == 0:
            if len(thecotheup(board)) > 0:
                if player_01.checkUpsiteDown() == True:
                    return player_01.getUpsideDown(thecotheup(board)[0], board,Luachonbothe(board, "auto_color"))

    #lay 1 nguyen lieu cho the up dau tien neu diem cac nguoi choi khac < 13
    if arr_player[0].score <= 13 and arr_player[1].score <= 13 and arr_player[2].score <= 13:
        if len(lay1NLtheup1(board)) > 0:
            color = lay1NLtheup1(board)
            if len(color) > 0:
                return player_01.getOneStock(color[0], board, Luachonbothe(board, color[0], color[0]))

    #lay 3 nguyen lieu cho the up dau tien neu diem cac nguoi choi khac < 13
    if arr_player[0].score <= 13 and arr_player[1].score <= 13 and arr_player[2].score <= 13:
        if sum(player_01.stocks.values()) <= 8:
            if len(Lay3NLtheup1(board)) >= 3:
                if player_01.checkThreeStocks(board, Lay3NLtheup1(board)[0], Lay3NLtheup1(board)[1], Lay3NLtheup1(board)[2]):
                    return player_01.getThreeStocks(Lay3NLtheup1(board)[0], Lay3NLtheup1(board)[1], Lay3NLtheup1(board)[2], board, Luachonbothe(board, Lay3NLtheup1(board)[0], Lay3NLtheup1(board)[1], Lay3NLtheup1(board)[2]))
    
    #lay 3 nguyen lieu
    if arr_player[0].score <= 12 and arr_player[1].score <= 12 and arr_player[2].score <= 12:
        if sum(player_01.stocks.values()) <= 8:
            if len(layBaNguyenlieu(board)) >= 3:
                if player_01.checkThreeStocks(board, layBaNguyenlieu(board)[0], layBaNguyenlieu(board)[1], layBaNguyenlieu(board)[2]):
                    return player_01.getThreeStocks(layBaNguyenlieu(board)[0], layBaNguyenlieu(board)[1], layBaNguyenlieu(board)[2], board, Luachonbothe(board, layBaNguyenlieu(board)[0], layBaNguyenlieu(board)[1], layBaNguyenlieu(board)[2]))

    #lay 1 nguyen lieu
    if arr_player[0].score <= 12 and arr_player[1].score <= 12 and arr_player[2].score <= 12:
        if sum(player_01.stocks.values()) <= 9:
            color = laymotnguyenlieu(board)
            if len(color) > 0:
                return player_01.getOneStock(color[0], board, Luachonbothe(board, color[0], color[0]))

    #lay the de nhat
    if arr_player[0].score <=12 and arr_player[1].score <=12 and arr_player[2].score <=12 < 12:
        if SXthecothemo(board) != None:
            print("x")
            return player_01.getCard(SXthecothemo(board), board)

    #mo the co diem tren ban
    if len(thecothemo(board)) > 0:
        for diem in range(5, 0, -1):
            for card in thecothemo(board):
                if card.score == diem:
                    return player_01.getCard(card, board)

    #lay 1 nguyen lieu cho the up dau tien
    if len(lay1NLtheup1(board)) > 0:
        if sum(player_01.stocks.values()) <= 9:
            color = lay1NLtheup1(board)
            if len(color) > 0:
                return player_01.getOneStock(color[0], board, Luachonbothe(board, color[0], color[0]))

    #lay 3 nguyen lieu cho the up dau tien
    if sum(player_01.stocks.values()) <= 8:
        if len(Lay3NLtheup1(board)) >= 3:
            if player_01.checkThreeStocks(board, Lay3NLtheup1(board)[0], Lay3NLtheup1(board)[1], Lay3NLtheup1(board)[2]):
                return player_01.getThreeStocks(Lay3NLtheup1(board)[0], Lay3NLtheup1(board)[1], Lay3NLtheup1(board)[2], board, Luachonbothe(board, Lay3NLtheup1(board)[0], Lay3NLtheup1(board)[1], Lay3NLtheup1(board)[2]))


    #lay 3 nguyen lieu
    if sum(player_01.stocks.values()) <= 8:
        if len(layBaNguyenlieu(board)) >= 3:
            if player_01.checkThreeStocks(board, layBaNguyenlieu(board)[0], layBaNguyenlieu(board)[1], layBaNguyenlieu(board)[2]):
                return player_01.getThreeStocks(layBaNguyenlieu(board)[0], layBaNguyenlieu(board)[1], layBaNguyenlieu(board)[2], board, Luachonbothe(board, layBaNguyenlieu(board)[0], layBaNguyenlieu(board)[1], layBaNguyenlieu(board)[2]))

    #lay 1 nguyen lieu
    if sum(player_01.stocks.values()) <= 9:
        color = laymotnguyenlieu(board)
        if len(color) > 0:
            return player_01.getOneStock(color[0], board, Luachonbothe(board, color[0], color[0]))

    #Mo the ho tro
    if len(Laythehotro(board)) > 0:
        return player_01.getCard(Laythehotro(board)[0], board)
    
    # lay 3 nguyen lieu trong do co 2 nguyen lieu can
    if sum(player_01.stocks.values()) <= 8:
        if len(L3NLtrong2(board)) >= 3:
            if player_01.checkThreeStocks(board, L3NLtrong2(board)[0], L3NLtrong2(board)[1], L3NLtrong2(board)[2]):
                return player_01.getThreeStocks(L3NLtrong2(board)[0], L3NLtrong2(board)[1], L3NLtrong2(board)[2], board, Luachonbothe(board, L3NLtrong2(board)[0], L3NLtrong2(board)[1], L3NLtrong2(board)[2]))
    
    #Up the khi khong lay duoc nguyen lieu can
    if len(thecotheup(board)) > 0:
        if arr_player[0].score <=12 and arr_player[1].score <=12 and arr_player[2].score <=12:
            if player_01.checkUpsiteDown() == True:
                return player_01.getUpsideDown(thecotheup(board)[0], board,Luachonbothe(board, "auto_color"))

    #lay 3 nguyen lieu trong do co 1 nguyen lieu
    if sum(player_01.stocks.values()) <= 9:
        if len(L3NLtrong1(board)) >= 3:
            if player_01.checkThreeStocks(board, L3NLtrong1(board)[0], L3NLtrong1(board)[1], L3NLtrong1(board)[2]):
                return player_01.getThreeStocks(L3NLtrong1(board)[0], L3NLtrong1(board)[1], L3NLtrong1(board)[2], board, Luachonbothe(board, L3NLtrong1(board)[0], L3NLtrong1(board)[1], L3NLtrong1(board)[2]))

    # lay 3 nguyen lieu bat ky
    if sum(player_01.stocks.values()) <= 7:
        if len(SXNLtrenban(board)) >= 3:
            if player_01.checkThreeStocks(board, SXNLtrenban(board)[0], SXNLtrenban(board)[1], SXNLtrenban(board)[2]):
                return player_01.getThreeStocks(SXNLtrenban(board)[0], SXNLtrenban(board)[1], SXNLtrenban(board)[2], board, Tranguyenlieu(board))
    
    # Lay 1 loai nguyen lieu bat ky
    if sum(player_01.stocks.values()) <=8:
        if len(Lay1NLbatky(board)) > 0:
            player_01.getOneStock(Lay1NLbatky(board)[0], board, Luachonbothe(board, Lay1NLbatky(board)[0], Lay1NLbatky(board)[0]))

    #Mo the binh thuong khi khong lam duoc gi
    if arr_player[0].score <=12 and arr_player[1].score <=12 and arr_player[2].score <=12:
        if len(thecothemo(board)) > 0:
            if Laythebinhthuong(board) != None:
                return player_01.getCard(Laythebinhthuong(board), board)
    return board

def thecotheup(board):
    listthecotheup = []
    for Loaithe in board.dict_Card_Stocks_Show.keys():
        for card in board.dict_Card_Stocks_Show[Loaithe]:
            if card.score == 3 and sum(card.stocks.values()) == 6:
                listthecotheup.append(card)
            if card.score == 4 and sum(card.stocks.values()) == 7:
                listthecotheup.append(card)
            if card.score == 2 and sum(card.stocks.values()) == 5:
                listthecotheup.append(card)
            if card.score == 5 and sum(card.stocks.values()) == 10:
                listthecotheup.append(card)            
            if card.score == 1 and sum(card.stocks.values()) == 4:
                listthecotheup.append(card)
            if card.score == 2 and sum(card.stocks.values()) == 7:
                listthecotheup.append(card)
            if card.score == 2 and sum(card.stocks.values()) == 8:
                listthecotheup.append(card)
    return listthecotheup

def latthedangup(board):
    listthecothemuadangup = []
    if len(player_01.card_upside_down) > 0:
        for card in player_01.card_upside_down:
            if player_01.checkGetCard(card) == True:
                listthecothemuadangup.append(card)
    return listthecothemuadangup

def thecothemo(board):
    listthecothemo = []
    if len(player_01.card_upside_down) > 0:
        for card in player_01.card_upside_down:
            if player_01.checkGetCard(card):
                listthecothemo.append(card)
    for Loaithe in board.dict_Card_Stocks_Show.keys():
        if Loaithe != "Noble":
            for card in board.dict_Card_Stocks_Show[Loaithe]:
                    if player_01.checkGetCard(card) == True:
                        listthecothemo.append(card)
    return listthecothemo

def thecothemocuanguoichoi(board, arr_player):
    listnguoichoi = []
    for nguoichoi in range(len(arr_player)):
        listthecothemo = []
        for Loaithe in board.dict_Card_Stocks_Show.keys():
            if Loaithe != "Noble":
                for card in board.dict_Card_Stocks_Show[Loaithe]:
                        if arr_player[nguoichoi].checkGetCard(card) == True:
                            listthecothemo.append(card)
        listnguoichoi.append(listthecothemo)
    return listnguoichoi

#sap xep cac the co the mo va co diem
def SXthecothemo(board):
    x = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4]
    soluongnguyenlieucan = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
    for danhgia in x:
        for the in thecothemo(board):
            if the.score > 0:
                sumNL = 0
                for lnl in soluongnguyenlieucan.keys():
                    sumNL += the.stocks[lnl] - player_01.stocks_const[lnl]
                    if sumNL / the.score < danhgia:
                        return the    
    return None                               

def NLtheup1(board):
    soluongnguyenlieucan = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
    for lnl in soluongnguyenlieucan.keys():
        if len(player_01.card_upside_down) > 0:
            the = player_01.card_upside_down[0]
            soluongnguyenlieucan[lnl] += the.stocks[lnl] 
            soluongnguyenlieucan[lnl] -= player_01.stocks[lnl] + player_01.stocks_const[lnl]
    SXNL = dict(sorted(soluongnguyenlieucan.items(), key=lambda x:x[1], reverse=True))
    return SXNL 

def lay1NLtheup1(board):
    OneNguyenlieucothelay = []
    for lnl in NLtheup1(board):
        if NLtheup1(board)[lnl] >= 2:
            if player_01.checkOneStock(board, lnl):
                OneNguyenlieucothelay.append(lnl)
    return OneNguyenlieucothelay

def Lay3NLtheup1(board):
    listcacNLnenlay = []
    for lnl in NLtheup1(board):
        if NLtheup1(board)[lnl] > 0 and board.stocks[lnl] > 0:
            listcacNLnenlay.append(lnl)
    return listcacNLnenlay

def Nguyenlieucan(board):
    soluongnguyenlieucan = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
    for lnl in soluongnguyenlieucan.keys():
        for the in player_01.card_upside_down:
            soluongnguyenlieucan[lnl] += the.stocks[lnl] 
        soluongnguyenlieucan[lnl] -= player_01.stocks[lnl] + player_01.stocks_const[lnl] 
    return soluongnguyenlieucan

def dictsapxepnguyenlieu(board):
    return dict(sorted(Nguyenlieucan(board).items(), key=lambda x:x[1], reverse=True))

def laymotnguyenlieu(board):
    OneNguyenlieucothelay = []
    if sum(player_01.stocks.values()) <= 8:
        for lnl in dictsapxepnguyenlieu(board):
            if dictsapxepnguyenlieu(board)[lnl] >= 2:
                if player_01.checkOneStock(board, lnl):
                    OneNguyenlieucothelay.append(lnl)
    return OneNguyenlieucothelay

def layBaNguyenlieu(board):
    listcacNLnenlay = []
    for lnl in dictsapxepnguyenlieu(board):
        if dictsapxepnguyenlieu(board)[lnl] > 0 and board.stocks[lnl] > 0:
            listcacNLnenlay.append(lnl)
    return listcacNLnenlay

def Laythehotro(board):
    listNLcan = []
    listthehotro = []
    listthehotrolay = []
    for lnl in dictsapxepnguyenlieu(board):
        if dictsapxepnguyenlieu(board)[lnl] > 0:
            listNLcan.append(lnl)
    for the in thecothemo(board):
        if the.type_stock in listNLcan:
            listthehotro.append(the)
    for the in listthehotro:
        if player_01.checkGetCard(the) == True:
            listthehotrolay.append(the)
    return listthehotrolay

def Laythebinhthuong(board):
    a = []
    if len(thecothemo(board)) > 0:
        the = thecothemo(board)[0]
        for card in thecothemo(board):
            NLcanmo1the = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
            for lnl in NLcanmo1the.keys():
                NLcanmo1the[lnl] = card.stocks[lnl] - player_01.stocks_const[lnl]
            a.append(sum(NLcanmo1the.values()))
        x = min(a)
        for card in thecothemo(board):
            NLcanmo1the = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
            for lnl in NLcanmo1the.keys():
                NLcanmo1the[lnl] = card.stocks[lnl] - player_01.stocks_const[lnl]
            if a == sum(NLcanmo1the.values()):
                return card
    return None
    
def SXNLtrenban(board):
    listNLcan = layBaNguyenlieu(board)
    NLtrenban = board.stocks.copy()
    for lnl in (dict(sorted(NLtrenban.items(), key=lambda x:x[1], reverse=False))).keys():
        if lnl != "auto_color":
            if board.stocks[lnl] > 0 and (lnl not in layBaNguyenlieu(board)):
                listNLcan.append(lnl)
    return listNLcan
def Lay1NLbatky(board):
    ln = []
    NLtrenban = board.stocks.copy()
    for lnl in NLtrenban.keys():
        if lnl != "auto_color":
            if NLtrenban[lnl] >=4:
                if player_01.checkOneStock(board, lnl):
                    ln.append(lnl)
    return ln
def L3NLtrong2(board):
    listNLcan = layBaNguyenlieu(board)
    if len(layBaNguyenlieu(board)) == 2:
        NLtrenban = board.stocks.copy()
        for lnl in (dict(sorted(NLtrenban.items(), key=lambda x:x[1], reverse=False))).keys():
            if lnl != "auto_color":
                if board.stocks[lnl] > 0 and (lnl not in layBaNguyenlieu(board)):
                    listNLcan.append(lnl)
    return listNLcan

def L3NLtrong1(board):
    listNLcan = layBaNguyenlieu(board)
    if len(layBaNguyenlieu(board)) == 1:
        NLtrenban = board.stocks.copy()
        for lnl in (dict(sorted(NLtrenban.items(), key=lambda x:x[1], reverse=False))).keys():
            if lnl != "auto_color":
                if board.stocks[lnl] > 0 and (lnl not in layBaNguyenlieu(board)):
                    listNLcan.append(lnl)
    return listNLcan 

#Nguyen lieu can cua the up tru cho stocks count
def NLcan(board):
    NL_the_up = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
    NL_can = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
    for lnl in player_01.stocks.keys():
        if lnl != "auto_color":
            for the in player_01.card_upside_down:
                NL_the_up[lnl] += the.stocks[lnl]
            NL_can[lnl] = NL_the_up[lnl] - player_01.stocks_const[lnl]
    return NL_can

def Tranguyenlieu(board):
    listthebo = []
    dictnguyenlieuthua = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
    nguyen_lieu_the_up = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}

    for lnl in dictnguyenlieuthua.keys():
        if player_01.stocks[lnl] > 0:
            dictnguyenlieuthua[lnl] = player_01.stocks[lnl] - NLcan(board)[lnl]

    SXNL_thua= dict(sorted(dictnguyenlieuthua.items(), key=lambda x:x[1], reverse=True))
    for lnl in SXNL_thua.keys():
        listthebo.append(lnl)
    SXNLcan = dict(sorted(NLcan(board).items(), key=lambda x:x[1], reverse=False))
    for lnl in SXNLcan.keys():
        if player_01.stocks[lnl] > 0  and (lnl not in list(SXNL_thua.keys())):
            listthebo.append(lnl)
    return listthebo

def Luachonbothe(board, *args):
    dict_bo = {
        "red": 0,
        "blue": 0,
        "white": 0,
        "green": 0,
        "black": 0,
        "auto_color": 0
    }
    dict_bd = player_01.stocks.copy()
    for x in args:
        dict_bd[x] += 1
    danhsachcon = Tranguyenlieu(board)
    if sum(dict_bd.values()) > 10:
        n = sum(dict_bd.values()) - 10
        i = 0
        while n != 0:
            if dict_bd[danhsachcon[i]] != 0:
                dict_bo[danhsachcon[i]] += 1
                dict_bd[danhsachcon[i]] -= 1
                n -= 1
            else:
                i += 1
    return dict_bo

def laythenoble(board):
    theNoblenenlay = []
    NLcanchotheNoble = []
    for the in board.dict_Card_Stocks_Show["Noble"]:
        x = 0
        for lnl in the.stocks.keys():
            if the.stocks[lnl] > 0:
                x += the.stocks[lnl] - player_01.stocks_const[lnl]
        if x <= 1:
            theNoblenenlay.append(the)
    for the in theNoblenenlay:
        for lnl in the.stocks.keys():
            if (the.stocks[lnl] - player_01.stocks_const[lnl]) > 0:
                NLcanchotheNoble.append(lnl)
    the_taget_noble = []
    for the in thecothemo(board):
        if the.type_stock in NLcanchotheNoble:
            the_taget_noble.append(the)
    return the_taget_noble