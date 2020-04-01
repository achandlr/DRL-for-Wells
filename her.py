from stable_baselines.a2c.utils import conv, linear, conv_to_fc
import sys
import tensorflow as tf
import numpy as np
from stable_baselines.common.policies import FeedForwardPolicy, MlpPolicy, MlpLstmPolicy, MlpLnLstmPolicy, CnnPolicy, CnnLstmPolicy, CnnLnLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv, VecNormalize
from stable_baselines.common import set_global_seeds
from stable_baselines import ACKTR, PPO2, HER, SAC
from env.field_env import FieldEnv

print("Setting up env")


#n_procs = 8
#env = SubprocVecEnv([make_env(FieldEnv, i) for i in range(n_procs)], start_method='spawn')
#env = DummyVecEnv([lambda: FieldEnv(1)])
env = FieldEnv(1)
env.seed(1)
set_global_seeds(1)

#env = VecNormalize(env, norm_obs=True, norm_reward=False, clip_obs=10.)

print("Setting up model")
print("Policy = HER")

model = HER('MlpPolicy', env, SAC, n_sampled_goal=4, goal_selection_strategy='future', buffer_size=int(1e6), learning_rate=1e-3, gamma=0.95, batch_size=256, policy_kwargs=dict(layers=[256,256,256]), verbose=1, tensorboard_log="./tensey/")
print("About to start");
#stepsToLearn = int(2e5)
stepsToLearn = int(10)
model.learn(stepsToLearn)

# Save the agent
model.save("field-env-" + str(stepsToLearn) + "-her-MlpPolicy")

