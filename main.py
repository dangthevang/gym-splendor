import gym
import gym_splendor
import os
import pandas as pd
import json
import numpy as np

def check_winner(state):
    name = ''
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
    if player_win != None:
        return player_win.name
    else:
        return "NA0"

def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn <1500:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        # env.render()
        if done == True:
            break
    state = env.state
    win = check_winner(state)
    print(win,env.turn)
    f = open("/content/gym-splendor/gym_splendor/envs/agents/mind.json")
    mind = json.load(f)
    f = open("/content/gym-splendor/gym_splendor/envs/agents/data.json")
    act_possible = json.load(f)
    new_mind = {}
    for player in list(state['Player']):
        if player.name == win:
            last_act = player.s_a_pair[-1][1]
            score = len(player.s_a_pair)
            if player.act_possible[last_act][0][0] != "I":
                last_act = player.s_a_pair[-2][1]
                score = len(player.s_a_pair) -1
            point = player.point_act
            # print("học action",player.act_possible[last_act])
            if score > point[last_act]:
                point[last_act] = score
            with open('/content/gym-splendor/gym_splendor/envs/agents/point_act.json', 'w') as f:
                json.dump(point, f)

        #     step = -1
        # else:
        #     step = 1
        # for id_pair in range(len(player.s_a_pair)):
        #     pair = player.s_a_pair[id_pair]
        #     s = pair[0]
        #     a = pair[1]
        #     for id_state in s:
        #         name = str(id_state) + "_" +str(s[id_state])
        #         if name not in mind:
        #             mind[name] = list(np.ones(len(act_possible))*100)
        #         mind[name][a] += step + id_pair*(step>0)
        #         mind[name][a] *= (mind[name][a]>0)
                
    # with open('/content/gym-splendor/gym_splendor/envs/agents/mind.json', 'w') as f:
    #     json.dump(mind, f)



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


















