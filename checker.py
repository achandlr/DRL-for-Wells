#from stable_baselines.a2c.utils import conv, linear, conv_to_fc
#import tensorflow as tf
#import numpy as np
#from stable_baselines.common.policies import FeedForwardPolicy, CnnPolicy
#from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common import env_checker
import stable_baselines
#from stable_baselines import ACKTR
from env.field_env import FieldEnv


print("Setting up env")
env = FieldEnv()#DummyVecEnv([lambda: FieldEnv()])

stable_baselines.common.env_checker.check_env(env, warn=True)
