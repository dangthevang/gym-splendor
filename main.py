import gym
import gym_splendor
import time

def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn < 8:
        print("**********************************************************************************************************")
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        env.render()
        print("-----------------------------------------------------------------------------------------------------------")
        if done == True:
            break
        time.sleep(0.03)

if __name__ == '__main__':
    main()
