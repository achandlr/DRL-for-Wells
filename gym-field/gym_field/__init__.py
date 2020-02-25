from gym.envs.registration import register

register(
    id='field-v0',
    entry_point='gym_field.envs:FieldEnv',
)
