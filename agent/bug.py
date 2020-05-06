from gym_oilfield.oilfield_env import OilFieldEnv
from gym_oilfield.readData import readData
import numpy as np

env = OilFieldEnv()
env.initData([0,0,0],11,11,11, readData(11))

print(np.max(env.step(5)[0]))
print(np.max(env.step(2)[0]))
print(np.max(env.step(2)[0]))
print(np.max(env.step(2)[0]))
