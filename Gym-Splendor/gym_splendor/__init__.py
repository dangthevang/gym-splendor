from gym.envs.registration import register

register(
    id='gym_splendor-v0',
    max_episode_steps=200,
    
    entry_point='gym_splendor.envs:SplendporEnv',
)