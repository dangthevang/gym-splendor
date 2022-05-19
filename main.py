
import gym
import gym_splendor
import pandas as pd
import time
import warnings
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn <1000:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(state = env.state))
        # env.render()
        if done == True:
            break
    # for i in range(4):
    #     o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(state = env.state))
    print(env.turn, env.pVictory.name, env.pVictory.score)

if __name__ == '__main__':
    main()
