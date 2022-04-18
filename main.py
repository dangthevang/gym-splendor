import gym
import gym_splendor
import os
import pandas as pd


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
        return player_win.name, score_max, 'ở turn ' + str(int(state['Turn']/4))
    else:
        return "NA0"

def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn <150:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        env.render()
        if done == True:
            break
    state = env.state
    print(check_winner(state))

if __name__ == '__main__':
    main()


