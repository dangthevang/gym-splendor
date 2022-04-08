import gym
import gym_splendor

def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn <120:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        env.render()
        print(env.state["Board"])
        if done == True:
            break

if __name__ == '__main__':
    main()
