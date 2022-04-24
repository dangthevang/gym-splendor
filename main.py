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

def check_winner(state):
    name = ''
    score_max = 14
    player_win = None
    if state['Turn']%4 == 0:
        for player in list(state['Player']):
            if player.score > score_max:
                score_max = player.score 
        if score_max > 14:

            list_ten = []
            list_diem = []

            for player in list(state['Player']):
                list_ten.append(player.name)
                list_diem.append(player.score)
                if player.score >= score_max:
                    score_max = player.score 
                    player_win = player
                elif player.score == score_max:
                    if len(player.card_open) < len(player_win.card_open):
                        player_win = player
            if score_max > 14:
                winner(str(player_win.name) + ' win với ' + str(score_max) + ' ở turn ' + str(state['Turn']/4))
            
                for i in range(list_ten.__len__()):
                    Thongbao('Người chơi ' + str(list_ten[i]) + ' có ' + str(list_diem[i]) + ' điểm ')

    return list_ten, list_diem, state['Turn']/4


def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn <200:
        #print(env.turn)
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        env.render()
        if done == True:
            break

    # return check_winner(env.state)

if __name__ == '__main__':
    main()

