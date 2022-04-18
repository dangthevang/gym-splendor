import gym
import gym_splendor
import os
import pandas as pd


def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn < 200:
        o, a, done, t = env.step(
            env.player[env.turn % env.amount_player].action(env.state))
        env.render()
        if done == True:
            break


if __name__ == '__main__':
    main()


# def create_train(link_folder):
#     list_stock = ['red', 'blue', 'green', 'white', 'black', 'auto_color']
#     file_train = pd.DataFrame({})
#     for type_stock in list_stock[:-1]:
#         for i in range(8):
#             list_score = [100]*90
#             file_train[f'{i}_{type_stock}_board'] = list_score
#         for i in range(8):
#             list_score = [100]*90
#             file_train[f'{i}_{type_stock}_player'] = list_score
#         for i in range(19):
#             list_score = [100]*90
#             file_train[f'{i}_{type_stock}_const'] = list_score
#     for i in range(6):
#         list_score = [100]*90
#         file_train[f'{i}_auto_color_board'] = list_score
#         file_train[f'{i}_auto_color_player'] = list_score
#     for card_id in range(1,101):
#         list_score = [100]*90
#         file_train[f'card_{card_id}_Y'] = list_score
#         file_train[f'card_{card_id}_N'] = list_score
#     file_train.to_csv(f'{link_folder}/file_train.csv', index=False)

#     print(file_train.shape)

# link_folder = './TRAIN_HIEU'
# try:
#     os.mkdir(link_folder)
# except:
#     pass
# create_train(link_folder)


# def check_winner(self, state):
#     name = ''
#     score_max = 14
#     player_win = None
#     if state['Turn']%4 == 0:
#         for player in list(state['Player']):
#             if player.score > score_max:
#                 score_max = player.score
#         if score_max > 14:

#             for player in list(state['Player']):
#                 if player.score >= score_max:
#                     score_max = player.score
#                     player_win = player
#                 elif player.score == score_max:
#                     if len(player.card_open) < len(player_win.card_open):
#                         player_win = player
#             if score_max > 14:
#                 print('Tap trung vao day nao')
#                 print(player_win.name, 'win với ', score_max, 'ở turn ',  state['Turn']/4)


