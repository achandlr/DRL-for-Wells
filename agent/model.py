from stable_baselines.common.policies import MlpLnLstmPolicy
from stable_baselines.common.vec_env import VecNormalize
from stable_baselines.common.callbacks import CheckpointCallback
from CustomEvalCallback import CustomEvalCallback, evaluate_policy
from stable_baselines import PPO2

ALGO = PPO2
ALGO_STR = "PPO2"
POLICY = MlpLnLstmPolicy
POLICY_STR = "MlpLnLstmPolicy"
CP_COUNT = 100
NMINIBATCHES = 4
N_EVAL_EPISODES = 5

"""
Class that sets up model, and automates model saving as well as tensorboard output.
"""

class Model(ALGO):
    def __init__(self, env, eval_env, env_name, seed, n_procs, num_steps):
        """
        Initializes a model.
        :param env: (Environment) the environment / environment ID
        :param eval_env: (Environment) the environment to evaluate models on
        :param env_name: (str) the name used for saving models
        :param seed: (int) seed for randomization
        :param n_procs: (int) the number of processes used in training
        :param num_steps: (int) the number of steps to train / retrain for
        """
        super().__init__(POLICY, env, verbose=1, tensorboard_log="./tensorboard/", seed=seed, nminibatches=NMINIBATCHES)
        self.n_procs = n_procs
        self.num_steps = num_steps
        self.seed = seed;
        self.eval_env = eval_env
        self.loaded = False
        self.env_name = env_name
    def save(self, basepath):
        """
        Saves model (overrides base method)
        :param basepath: (str) the base path to save to
        """
        name = basepath + self.getName()
        super().save(name)
        super().get_env().save(name + ".env")
    @staticmethod
    def load(path, env, eval_env, env_name, seed, n_procs, num_steps):
        """
        Load a model from a folder (overrides base method)
        :param env: (Environment) the environment / environment ID
        :param eval_env: (Environment) the environment to evaluate models on
        :param env_name: (str) the name used for saving models
        :param seed: (int) seed for randomization
        :param n_procs: (int) the number of processes used in training
        :param num_steps: (int) the number of steps to train / retrain for
        """
        env = VecNormalize.load(path + ".env", env)
        ret = ALGO.load(path, env=env, verbose=1, tensorboard_log="./tensorboard/", seed=seed, nminibatches=NMINIBATCHES)
        ret.__class__ = Model;
        ret.n_procs = n_procs
        ret.num_steps = num_steps
        ret.seed = seed;
        ret.eval_env = eval_env
        ret.loaded = True
        ret.env_name = env_name
        return ret
    def trainAndSave(self):
        """
        Trains the model and saves it once done, as well as saving checkpoints and best results along the way
        """
        cps = CheckpointCallback(save_freq=self.num_steps//(CP_COUNT*self.n_procs), save_path="./checkpoints/", name_prefix="")
        bestcb = CustomEvalCallback(self.eval_env, best_model_save_path="./bests/", log_path="./logs/", eval_freq=self.num_steps//(CP_COUNT*self.n_procs), deterministic=True, render=False, verbose=1)
        cb = [cps, bestcb]
        super().learn(self.num_steps, callback=cb, reset_num_timesteps=not self.loaded)
        self.save("./results/")
    def evaluate(self, visualize):
        """
        Evaluates a model.
        :param visualize: (boolean) whether or not you want to call render on each step.
        """
        episode_rewards, episode_lengths = evaluate_policy(self, self.eval_env,
					       n_eval_episodes=N_EVAL_EPISODES,
					       render=visualize,
					       deterministic=True,
					       return_episode_rewards=True)
        print(episode_rewards)

    def getName(self):
        """
        Gets the unique name for this model
        """
        return "-".join(list(map(str,filter(None.__ne__, [self.env_name, ALGO_STR, POLICY_STR, self.n_procs, NMINIBATCHES, self.num_steps, self.seed, "resume" if self.loaded else None]))))
