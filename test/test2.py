
import numpy as np
import itertools
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
