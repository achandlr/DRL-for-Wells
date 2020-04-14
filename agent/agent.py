import sys
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv, VecNormalize
from stable_baselines.common import set_global_seeds
from env.field_env import FieldEnv
from model import Model

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

ENV = FieldEnv
SEED = 49
N_PROCS = 8
NUM_STEPS = int(1e4)

def run():
    resume = sys.argv[1] == "r" if len(sys.argv) > 1 else False
    evaluate = sys.argv[1] == "e" if len(sys.argv) > 1 else False
    loadpath = sys.argv[2] if resume or evaluate else ""
    print("Setting up env")
    env = SubprocVecEnv([make_env(ENV, i) for i in range(N_PROCS)], start_method='spawn')

    eval_env = DummyVecEnv([make_env(ENV, i) for i in range(N_PROCS)])
    eval_env = VecNormalize(eval_env, norm_obs=True, norm_reward=False, clip_obs=10.)

    print("Setting up model")

    if not (resume or evaluate):
        env = VecNormalize(env, norm_obs=True, norm_reward=False, clip_obs=10.)
        model = Model(env=env, eval_env=eval_env, env_name="FieldEnv", seed=SEED, n_procs=N_PROCS, num_steps=NUM_STEPS)
    else:
        model = Model.load(loadpath, env, eval_env=eval_env, env_name="FieldEnv", seed=SEED, n_procs=N_PROCS, num_steps=NUM_STEPS)
        #model = Model(env=None, eval_env=eval_env, env_name="FieldEnv", seed=SEED, n_procs=N_PROCS, num_steps=NUM_STEPS)


    if not evaluate:
        model.trainAndSave()
    else:
        model.evaluate()

if __name__ == '__main__':
    run()

