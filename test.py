import gym
import gym_splendor

def main():
    env = gym.make('gym_splendor-v0')
    env.render()
    env.close()
if __name__ == '__main__':
    main()
