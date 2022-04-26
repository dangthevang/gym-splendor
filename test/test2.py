
import numpy as np
import itertools
import json
NL_board = {'red': 7, 'blue': 7, 'green': 7, 'black': 7, 'white': 7, 'auto_color': 5}
NL = {'red': 2, 'blue': 2, 'green': 2, 'black': 2, 'white': 2, 'auto_color': 0}
board_materials = []
hand_materials = []
for nl in NL.keys():
    if nl != "auto_color" and NL[nl] > 0:
        hand_materials.append(nl)
for nl in NL_board.keys():
    if nl != "auto_color" and NL_board[nl] > 0:
        board_materials.append(nl)

def get_st(NL_board, board_materials, hand_materials):
    list_ = []
    stock_return = []
    for so_NL in range(7, 11):
        for lay in range(1, 4):
            sonl = so_NL + lay - 10
            if sonl <= 0:
                st_return = []
            else:
                st_return = [' '.join(i).split(' ') for i in itertools.combinations(hand_materials, sonl)]
            st_give = [' '.join(i).split(' ') for i in itertools.combinations(board_materials, lay)]
            if lay == 2:
                for cl in board_materials:
                    if NL_board[cl] >=4:
                        st_give.append([cl, cl])
            for i in st_give:
                if st_return == []:
                    hi = [i, []]
                    list_.append(hi)
                else:
                    for j in st_return:
                        # print(i, j)
                        check = True
                        for cl_rt in j:
                            if cl_rt in i:
                                check = False
                        if check == True:
                            hi = [i, j]
                            list_.append(hi)
        list2 = []
        if len(list_)> 0:
            for i in range(len(list_)):
                if list_[i][0] != list_[i][1]:
                    list2.append(list_[i])
    return list2
list_save = []
list2 = get_st(NL_board, board_materials, hand_materials)
for i2 in list2:
    list_save += [[i2[0], [], i2[1]]]
# for i in list_save:

# print(list_save)
# print(len(list_save))
# for i in list_save:
#     print(i)

list_card = ["I_1", "I_2", "I_3", "I_4", "I_5", "I_6", "I_7", "I_8", "I_9", "I_10", "I_11", "I_12", "I_13", "I_14", "I_15", "I_16", "I_17", "I_18", "I_19", "I_20", "I_21", "I_22", "I_23", "I_24", "I_25", "I_26", "I_27", "I_28", "I_29", "I_30", "I_31", "I_32", "I_33", "I_34", "I_35", "I_36", "I_37", "I_38", "I_39", "I_40", "II_1", "II_2", "II_3", "II_4", "II_5", "II_6", "II_7", "II_8", "II_9", "II_10", "II_11", "II_12", "II_13", "II_14", "II_15", "II_16", "II_17", "II_18", "II_19", "II_20", "II_21", "II_22", "II_23", "II_24", "II_25", "II_26", "II_27", "II_28", "II_29", "II_30", "III_1", "III_2", "III_3", "III_4", "III_5", "III_6", "III_7", "III_8", "III_9", "III_10", "III_11", "III_12", "III_13", "III_14", "III_15", "III_16", "III_17", "III_18", "III_19", "III_20"]
List_cl = [[],['red'], ['blue'], ['green'], ['white'], ['black']]
for cl in List_cl:
    for card in list_card:
        list_save.append([[], card, cl])
import pandas as pd
import numpy as np
pd.DataFrame({'action':list_save}).to_csv('C:/Users/ADMIN/Máy tính/gym-splendor/data_act.csv', index = False)
pd.read_csv('C:/Users/ADMIN/Máy tính/gym-splendor/data_act.csv').drop_duplicates().reset_index(drop = True).to_csv('C:/Users/ADMIN/Máy tính/gym-splendor/data_act.csv', index = False)

df_act = pd.read_csv('C:/Users/ADMIN/Máy tính/gym-splendor/data_act.csv')
list_ = [[[], [], []]]
import ast
for i in df_act.index:
    res = ast.literal_eval(df_act['action'].iloc[i])
    list_.append(res)
print(len(list_))
pd.DataFrame({'action':[list_]}).to_csv('C:/Users/ADMIN/Máy tính/gym-splendor/data_act.csv', index = False)
pd.read_csv('C:/Users/ADMIN/Máy tính/gym-splendor/data_act.csv')