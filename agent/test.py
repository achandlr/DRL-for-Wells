#from stable_baselines.a2c.utils import conv, linear, conv_to_fc
#import tensorflow as tf
#import numpy as np
#from stable_baselines.common.policies import FeedForwardPolicy, CnnPolicy
#from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common import env_checker
import stable_baselines
#from stable_baselines import ACKTR
from gym_oilfield.oilfield_env import OilFieldEnv
from gym_oilfield.readData import readData


print("Setting up env")
env = OilFieldEnv()#DummyVecEnv([lambda: FieldEnv()])
env.initData([0,0,0],11,11,11,readData(11))

env.render()
