from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from env.field_env import FieldEnv


env = DummyVecEnv([lambda: FieldEnv()])
#model = PPO2(MlpPolicy, env, learning_rate=0.001)

model = PPO2.load("field-env-1000000-a2c")

obs = env.reset()
sumRew = 0
episodeCount = 0
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    if dones:
        sumRew = 0
        print("Resetting reward")
        episodeCount += 1
        print(f"Episode ${episodeCount}")
    sumRew += rewards
    print(f"reward total = ${sumRew}")
    env.render()
    if dones:
        break
