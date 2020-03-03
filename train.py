from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import ACKTR
from env.field_env import FieldEnv


print("Setting up env");
env = DummyVecEnv([lambda: FieldEnv()])
model = ACKTR(MlpPolicy, env, verbose=1, tensorboard_log="./tensey/")
#model.learn(50000)
print("About to start");
model.learn(10000000)



# Save the agent
model.save("field-env-10000000-acktr")

