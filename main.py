import gym
import gym_splendor
import os
import pandas as pd
import itertools

def check_winner(state):
    score_max = 14
    player_win = None
    if state['Turn']%4 == 0:
        for player in list(state['Player']):
            if player.score > score_max:
                score_max = player.score
        if score_max > 14:

            for player in list(state['Player']):
                if player.score >= score_max:
                    score_max = player.score
                    player_win = player
                elif player.score == score_max:
                    if len(player.card_open) < len(player_win.card_open):
                        player_win = player
            if score_max > 14:
                print('Tap trung vao day nao')
                print(player_win.name, 'win với ', score_max, 'ở turn ',  state['Turn']/4)

def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn < 200:
        o, a, done, t = env.step(
            env.player[env.turn % env.amount_player].action(env.state))
        env.render()
        if done == True:
            break
    check_winner(env.state)

if __name__ == '__main__':
    main()

# def create_list_action():
#     list_stock = ['red', 'blue', 'green', 'white', 'black']
#     list_stock_full = ['red', 'blue', 'green', 'white', 'black', 'auto_color']
#     #get_stock
#     get_3 = list(itertools.combinations(list_stock,3))          #length = 10
#     get_2 = [(i,i) for i in list_stock]                         #length = 5
#     #stock return
#     return_3 = list(itertools.combinations_with_replacement(list_stock_full,3))
#     return_2 = list(itertools.combinations_with_replacement(list_stock_full,2))
#     return_1 = list_stock_full.copy()
#     #card
#     list_card = [i for i in range(1,91)]
#     list_action = []
#     for get in get_3:
#         for return_stock in return_3 + return_2 + return_1:
#             list_action.append((get, None, return_stock))
#     for get in get_2:
#         for return_stock in return_2 + return_1:
#             list_action.append((get, None, return_stock))
    
#     for card in list_card:
#         list_action.append(([], card, []))                      #lấy thẻ
#         list_action.append((['auto_color'], card, []))          #úp thẻ
#         for return_stock in return_1:
#             list_action.append((['auto_color'], card, [return_stock])) #úp thẻ trả nguyên liệu

#     return list_action

# def create_train(link_folder):
#     list_stock = ['red', 'blue', 'green', 'white', 'black', 'auto_color']
#     list_action = create_list_action()
#     file_train = pd.DataFrame({'action': list_action})
#     for type_stock in list_stock[:-1]:
#         for i in range(8):
#             list_score = [100]*len(list_action)
#             file_train[f'{i}_{type_stock}_board'] = list_score
#         for i in range(8):
#             list_score = [100]*len(list_action)
#             file_train[f'{i}_{type_stock}_player'] = list_score
#         for i in range(18):
#             list_score = [100]*len(list_action)
#             file_train[f'{i}_{type_stock}_const'] = list_score
#     for i in range(6):
#         list_score = [100]*len(list_action)
#         file_train[f'{i}_auto_color_board'] = list_score
#         file_train[f'{i}_auto_color_player'] = list_score
#     for card_id in range(1,101):
#         list_score = [100]*len(list_action)
#         file_train[f'card_{card_id}_Y'] = list_score
#         # file_train[f'card_{card_id}_N'] = list_score
#     file_train.to_csv(f'{link_folder}/file_train.csv', index=False)

#     print(file_train.shape)

# link_folder = './TRAIN_HIEU'
# try:
#     os.mkdir(link_folder)
# except:
#     pass
# create_train(link_folder)

