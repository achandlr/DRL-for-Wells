from stable_baselines.a2c.utils import conv, linear, conv_to_fc
import sys
import tensorflow as tf
import numpy as np
import subprocess as sp
from stable_baselines.common.policies import FeedForwardPolicy, MlpPolicy, MlpLstmPolicy, MlpLnLstmPolicy, CnnPolicy, CnnLstmPolicy, CnnLnLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv
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
    env = DummyVecEnv([make_env(FieldEnv, i+1) for i in range(1)])

    print("Setting up model")

    model = PPO2.load("field-env-10000000-ppo2-MlpLnLstmPolicy.zip", seed=15346)

    obs = env.reset()
    state = None

    zero_completed_obs = np.zeros((n_procs,) + env.observation_space.shape)
    zero_completed_obs[0, :] = obs

    rew = 0
    for _ in range(1000):
        action, state = model.predict(zero_completed_obs, state=state)
        obs, reward , done, _ = env.step(action)
        zero_completed_obs[0, :] = obs
        sp.call('clear',shell=True);
        env.render()
        rew += reward
        input(f"Reward: {rew}")


if __name__ == '__main__':
    run()
