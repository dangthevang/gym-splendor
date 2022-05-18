
import gym
import gym_splendor
import pandas as pd
import time
import warnings
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

def check_winner(state):
    name = ''
    score_max = 14
    player_win = None
    if (state['Turn']+1)%4 == 0:
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
        return player_win.name, score_max, state['Turn']+1
    else:
        return "None"

def main():
    env = gym.make('gym_splendor-v0')
    pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []}).to_csv('State_tam_1.csv', index = False)
    pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []}).to_csv('State_tam_2.csv', index = False)
    pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []}).to_csv('State_tam_3.csv', index = False)
    pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []}).to_csv('State_tam_4.csv', index = False)
    try:
        state_save = pd.read_csv('state.csv')
    except:
        state_save = pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []})


    env.reset()
    while env.turn <1000:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(state = env.state))
        # env.render()
        if done == True:
            break
    for i in range(4):
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(state = env.state))

    state = env.state

    print(check_winner(state))
    for player in list(state['Player']):
        df_tam = pd.read_csv(f'State_tam_{player.name}.csv')
        state_save = pd.concat([state_save, df_tam])
    if check_winner(state) != "NA0":
        df_tam = pd.read_csv(f'State_tam_{player.name}.csv')
        state_save.to_csv('state.csv', index = False)
if __name__ == '__main__':
    main()


