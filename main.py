import gym
import gym_splendor
import os
import pandas as pd
from colorama import Fore, Back, Style

def winner(message):
    print(Fore.MAGENTA + message, end='')
    print(Style.RESET_ALL)
    pass

def Thongbao(message):
    print(Fore.GREEN + message, end='')
    print(Style.RESET_ALL)
    pass

def main(data):
    
    
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn <200:
        env.render()
        # o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state, data))
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        if done == True:
            break

    print(Fore.LIGHTGREEN_EX, 'Win, name:', Fore.LIGHTMAGENTA_EX, env.pVictory.name, Fore.LIGHTCYAN_EX, env.pVictory.score, end='   ')
    for p in env.player:
        if p.name != env.pVictory.name:
            print(Fore.RED, 'Lose, name:', Fore.MAGENTA, p.name, Fore.CYAN, p.score, end='   ')
    
    print(Fore.YELLOW, '   ROUND:', Fore.LIGHTYELLOW_EX, (env.turn+1)//4, end='')
    
    print(Style.RESET_ALL)

    # learning(env, data)

def learning(env, training_data):
    for p in env.player:
        pass

if __name__ == '__main__':
    data = pd.read_csv('gym_splendor/envs/agents/agent_Ann_policy/Ann_policy_training_data.csv', index_col='state_element')
    for i in range(1):
        print('Game', i, end='      ')
        main(data)

