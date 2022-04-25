import gym
import gym_splendor
import os
import pandas as pd
import warnings
import numpy as np
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
# warnings.filterwarnings("ignore", category=DeprecationWarning) 

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
        pd.read_csv(f'State_tam_{player_win.name}.csv').assign(win = 1).to_csv(f'State_tam_{player_win.name}.csv', index = False)
        return player_win.name, score_max, str(int(state['Turn']/4))
    else:
        return "NA0"

def main():
    env = gym.make('gym_splendor-v0')
    pd.DataFrame({'state':[], 'action':[],'win': []}).to_csv('State_tam_1.csv', index = False)
    pd.DataFrame({'state':[], 'action':[],'win': []}).to_csv('State_tam_2.csv', index = False)
    pd.DataFrame({'state':[], 'action':[],'win': []}).to_csv('State_tam_3.csv', index = False)
    pd.DataFrame({'state':[], 'action':[],'win': []}).to_csv('State_tam_4.csv', index = False)
    try:
        state_save = pd.read_csv('state.csv')
    except:
        state_save = pd.DataFrame({'state':[], 'action':[],'win': []})

    try:
        state_save_chi_MA = pd.read_csv('state_MA.csv')
    except:
        state_save_chi_MA = pd.DataFrame({'state':[], 'action':[],'win': []})

    env.reset()
    while env.turn <280:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        # env.render()
        if done == True:
            break
    state = env.state
    print(check_winner(state))
    for player in list(state['Player']):
        df_tam = pd.read_csv(f'State_tam_{player.name}.csv')
        state_save = pd.concat([state_save, df_tam])
    if check_winner(state) != "NA0":
        df_tam = pd.read_csv(f'State_tam_{player.name}.csv')
        state_save_chi_MA = pd.concat([state_save_chi_MA, df_tam])
        state_save_chi_MA.to_csv('state_MA.csv', index = False)
        state_save.to_csv('state.csv', index = False)

if __name__ == '__main__':
    main()


