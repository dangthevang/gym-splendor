
import gym
import gym_splendor
import pandas as pd
import time

def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    start_time = time.time()
    while env.turn <1000:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        # env.render()
        if done == True:
            break
    print(env.pVictory.name)
    # for i in range(4):
    #     o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
    print(time.time()-start_time)
if __name__ == '__main__':
    main()