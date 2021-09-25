from gym.envs.registration import register

register(
    id='gymXplane-v2',
    entry_point='gym_xplane.envs:XplaneEnv',
    kwargs={'target_values': [180, 1000], 'tolerance': [2, 20],  'max_episode_steps':2000}
)
