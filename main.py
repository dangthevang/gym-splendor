
import gym
import gym_splendor
import pandas as pd
import time

env = gym.make('gym_splendor-v0')
def main():
    env.reset() 
    start_time = time.time()
    while env.turn <1000:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        # env.render()
        if done == True:
            break
    for i in range(4):
        # print(env.turn//4)
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
    print(env.pVictory)
    print(time.time()-start_time)
if __name__ == '__main__':
    main()