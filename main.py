from django.shortcuts import render
import gym
import gym_splendor
import os
import pandas as pd

def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn <1000:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(state = env.state))
        # env.render()
        if done == True:
            break
    for i in range(4):
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(state = env.state))
if __name__ == '__main__':
    main()

