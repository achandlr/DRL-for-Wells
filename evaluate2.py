from CustomEvalCallback import evaluate_policy
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv, VecNormalize
from stable_baselines import ACKTR, PPO2
from stable_baselines.common import set_global_seeds
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

n_procs=8
eval_env = DummyVecEnv([make_env(FieldEnv, i) for i in range(n_procs)])
#eval_env = VecNormalize(eval_env, norm_obs=True, norm_reward=False, clip_obs=10.)
eval_env = VecNormalize.load("agent/results/FieldEnv-PPO2-MlpLnLstmPolicy-8-4-10000-49.env", eval_env)
model = PPO2.load("agent/results/FieldEnv-PPO2-MlpLnLstmPolicy-8-4-10000-49.zip")
n_eval_episodes=5
render = False;
deterministic=True;
episode_rewards, episode_lengths = evaluate_policy(model, eval_env,
					       n_eval_episodes=n_eval_episodes,
					       render=render,
					       deterministic=deterministic,
					       return_episode_rewards=True)


print(episode_rewards)
print(episode_lengths)
