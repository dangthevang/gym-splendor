
import gym
import gym_splendor
import pandas as pd
import time
import warnings
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

start_time = time.time()
def main():
    env = gym.make('gym_splendor-v0')
    env.reset() 
    while env.turn <1000:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        # env.render()
        if done == True:
            break
    for i in range(4):
        # print(env.turn//4)
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
    # print(env.pVictory)
    print(env.turn, env.pVictory.name, env.pVictory.score)
for i in range(15):
    if __name__ == '__main__':
        main()
print(time.time()-start_time)
