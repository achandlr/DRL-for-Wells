from gym.envs.registration import register

register(
    id='oilfield-v1',
    entry_point='gym_oilfield.envs:OilFieldEnv',
)