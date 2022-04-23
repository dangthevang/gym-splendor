
import numpy as np
import itertools
import json
NL_board = {'red': 4, 'blue': 6, 'green': 5, 'white': 1, 'black': 3, 'auto_color': 2}
NL = {'red': 1, 'blue': 1, 'green': 2, 'white': 2, 'black': 1, 'auto_color': 0}
board_materials = []
hand_materials = []
for nl in NL.keys():
    if nl != "auto_color" and NL[nl] > 0:
        hand_materials.append(nl)
for nl in NL_board.keys():
    if nl != "auto_color" and NL_board[nl] > 0:
        board_materials.append(nl)
def get_st(NL_board, hand_materials):
    list_ = []
    stock_return = []
    for lay in range(1, 4):
        sonl = sum(NL.values()) + lay - 10
        if sonl <= 0:
            st_return = []
        else:
            st_return = [' '.join(i).split(' ') for i in itertools.combinations(hand_materials, sonl)]
        st_give = [' '.join(i).split(' ') for i in itertools.combinations(NL_board, lay)]
        for i in st_give:
            if st_return == []:
                hi = [i, []]
                list_.append(hi)
            for j in st_return:
                hi = [i, j]
                list_.append(hi)         
    return list_
import pandas as pd
import numpy as np

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

# print(dich_arr(['blue']))

import pandas as pd

state_player = [60, 15, np.array([1, 0, 2, 0, 1, 2]), np.array([5, 2, 0, 1, 0, 0]), np.array([3, 2, 3, 3, 6, 0]), [0, 2, 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2, 3, 2, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 2, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]]
D = state_player[1]
T = state_player[0]
Sd = state_player[3][0]
Sb =state_player[3][1]
Sg = state_player[3][2]
Sw =state_player[3][3]
Sbl =state_player[3][4]
Sa =state_player[3][5]

Scd = state_player[4][0]
Scb =state_player[4][1]
Scg = state_player[4][2]
Scw =state_player[4][3]
Scbl =state_player[4][4]
Sca =state_player[4][5]
# ct = 'D*5 + T +Sd+Sb+Sg+Sw+Sbl+Sa +Scd*2+Scb*2+Scg*2+Scw*2+Scbl*2+Sca*2'
# pd.DataFrame({'ct':[ct] }).to_csv('ct.csv',index = False)

a = [['red'], ['red']]
del a[0]
print(a)
