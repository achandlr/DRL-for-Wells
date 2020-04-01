from stable_baselines.a2c.utils import conv, linear, conv_to_fc
import sys
import tensorflow as tf
import numpy as np
from stable_baselines.common.policies import FeedForwardPolicy, MlpPolicy, MlpLstmPolicy, MlpLnLstmPolicy, CnnPolicy, CnnLstmPolicy, CnnLnLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv, VecNormalize
from stable_baselines.common import set_global_seeds
from stable_baselines import ACKTR, PPO2
from env.field_env import FieldEnv

def make_env(env_class, rank, seed=0):
    """
    Utility function for multiprocessed env.
    
    :param env_id: (str) the environment ID
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = env_class()
        # Important: use a different seed for each environment
        env.seed(seed + rank)
        return env
    set_global_seeds(seed)
    return _init

def run():
    print("Setting up env")

    n_procs = 8
    env = DummyVecEnv([make_env(FieldEnv, i+1) for i in range(n_procs)])
    env = VecNormalize(env, norm_obs=True, norm_reward=False, clip_obs=10.)

    print("Setting up model")

    model = PPO2.load("field-env-10000000-ppo2-MlpLnLstmPolicy.zip", seed=8)

    obs = env.reset()
    state = None

    #zero_completed_obs = np.zeros((n_procs,) + env.observation_space.shape)
    #zero_completed_obs[0, :] = obs

    total_rew_avg = [];
    total_rew = 0;
    for i in range(599):
        #action, state = model.predict(zero_completed_obs, state=state)
        action, state = model.predict(obs, state=state, deterministic=False)
        obs, reward , done, _ = env.step(action)
        #zero_completed_obs[0, :] = obs
        total_rew += reward
        if (i % 300 == 298):
            total_rew_avg.append(total_rew)
        #if (done):
            #state = None
            #obs = env.reset()
            #zero_completed_obs[0, :] = obs
    env.env_method('render')
    print(f"Total Reward: {total_rew}")
    print(f"Total Reward: {total_rew_avg}")


if __name__ == '__main__':
    run()
