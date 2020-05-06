import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding

from .Field2D import Field
from .world import parseWorld, printWorld
from .world import NOTHING, PLAYER, OIL, WATER, WALL


class FieldEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    """

    Represents an oil field environment

    Variables:
        action_space
            --Discrete variable which can take one of four options at a time
        observation_space
            --A box with identical bounds in each dimension
        size
            --Size of the start world
        reward_range
            --Descibes the potential range of a given reward
        current_episode
            --Store what episode the agent is on
        current_player
            --Stores a value describing the current agent/player
        current_step (int)
            --Stores what step in the episode the agent is on
        max_step (int)
            --Stores the limit for how many steps per episode
        world
            --A copy of the current world
        _movement_grid
            --Options that describe how the agent can move through the env
        _last_reward
            --Stores the last reward the agent collected
        _cum_rew
            --Stores the cumulative rewards the agent has acquired
        _oils
            --Stores the position of all the oil in the world
        _start_world
            --The world filled with initial values representing oil, water, empty
    """

    def __init__(self):

        self.action_space = spaces.Discrete(4)
        self._start_world = parseWorld()
        self.world = self._start_world.copy()
        self.size = np.shape(self._start_world)[0]
        self.observation_space = spaces.Box(low=-1, high=1, shape=(self.size + 0,self.size, 1), dtype=np.float32)
        self.reward_range = (-1,1)
        self.current_episode = 0
        self.current_step = 0
        self.max_step = 300
        self._cum_rew = 0
        self._seed = 0
        self._oils = np.transpose(np.where(self.world == OIL))

        self._movement_grid = {0: [[0], [-1], [0]], 1: [[1], [0], [0]], 2: [[0], [1], [0]], 3: [[-1], [0], [0]]}

        print("Initialized successfully");


    def reset(self):
        """
        Function that resets the episode and brings everything back to its
        original state
        """
        #print("Reseting")
        #print(f"Episode number {self.current_episode}")
        #print(f" in {self.current_step} steps\n")
        if (self.current_episode % 1000 == 0):
            print(f"On episode {self.current_episode}\n", flush=True)
            print(f"Last reward: {self._cum_rew}\n", flush=True)
            printWorld(self.world)
        self.current_player = PLAYER
        self.current_step = 0
        self._cum_rew = 0
        self.world = self._start_world.copy()
        self._oils = np.transpose(np.where(self.world == OIL))
        return self._next_observation()


        #FieldInput = [ [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       #[[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       #[[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       #[[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       #[[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       #[[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       #[[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       #[[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       #[[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       #[[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]] ]

        #self.visitField = [ [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]

        #self.Field = Field(FieldInput)

        #self.currentX = 0
        #self.currentY = 5
        #self.visitField[5][0] = 1

        #StartOil , startWater = self.Field.getRock(0,5).Drain(0,0,None)

        #self.totalOil = 0
        #self.totalOil += StartOil

        #self.totalWater = 0
        #self.totalWater += startWater

        #return self.Field.getLiquidField()

    def shift1(self, arr, num, fill_value=np.nan):
        """
        TODO
        """

        result = np.empty_like(arr)
        if num > 0:
            result[:num] = fill_value
            result[num:] = arr[:-num]
        elif num < 0:
            result[num:] = fill_value
            result[:num] = arr[-num:]
        else:
            result[:] = arr
        return result


    def shift2(self, arr, num, fill_value=np.nan):
        """
        TODO

        Parameters:
            arr (TODO) : TODO
            num (TODO) : TODO
            fill_value (TODO) : TODO
        """
        result = np.empty_like(arr)
        if num > 0:
            result[:,:num] = fill_value
            result[:,num:] = arr[:,:-num]
        elif num < 0:
            result[:,num:] = fill_value
            result[:,:num] = arr[:,-num:]
        else:
            result[:] = arr
        return result

    def _next_observation(self):
        """
        Updates the observation space based off the agent's movement

        Returns the new observation space
        """
        current_pos = np.where(self.world == [self.current_player])
        obs = self.shift2(self.shift1(self.world, self.size//2 - current_pos[0][0], WALL), self.size//2 - current_pos[1][0], WALL);
        #obs = np.append(obs, [[self.current_player, 0, 0, 0, 0, 0, 0, 0, 0]], axis=0)
        return obs

    # returns a reward
    def _take_action(self, action):
        """

        Parameters:
            -action (TODO): the action that the agent wants to _take_action

        Moves the agent in the desired direction (based off action param) and
        calculates the reward based off that movement

        Return: the reward for the action
        """

        current_pos = np.where(self.world == [self.current_player])
        new_pos = tuple(np.array(current_pos) + self._movement_grid[action])
        if new_pos[0][0] < 0 or new_pos[0][0] >= self.size or new_pos[1][0] < 0 or new_pos[1][0] >= self.size:
            return -100/100 # don't waste a turn

        # we know it will move to new_pos now
        new_pos_value = self.world[new_pos][0]
        self.world[new_pos] = self.current_player
        self.world[current_pos] = NOTHING#WATER # can't move backwards
        rewPart = 0
        q1 = int(new_pos[0])
        q2 = int(new_pos[1])
        o1 = int(current_pos[0])
        o2 = int(current_pos[1])
        closestDist = np.min(np.sum(np.abs(self._oils - [q1, q2, 0]), axis=1)) # taxicab dist
        oldClosestDist = np.min(np.sum(np.abs(self._oils - [o1, o2, 0]), axis=1)) # taxicab dist
        if new_pos_value == OIL:
            rewPart = 65/100
            self._oils = self._oils[~(self._oils==[q1, q2, 0]).all(axis=1)] # remove current position from oils list
        elif new_pos_value == WATER:
            rewPart = -35/100

        return rewPart + -(closestDist - oldClosestDist)/(closestDist + 2)-15/100 # go fast

    #def hasVisited(self, x, y):
        #if (self.visitField[y][x] == 1):
            #return True
        #else :
            #return False

    def step(self, action):
        """

        Parameter:
            action (TODO) - the action the agent performs during this step


        Tells the agent to actually take the action and increments values as a
        result of the step

        Return: A tuple containing the next observation, reward of the last
        action, and whether or not the episode is done
        """
        if (action < 0 or action >= 4):
            print("Invalid Action")
            return 0

        self._last_reward = self._take_action(action)
        self._cum_rew += self._last_reward
        self.current_step += 1
        done = self.current_step >= self.max_step
        if done: self.current_episode += 1
        return self._next_observation(), self._last_reward, done, {}


    def render(self, mode='human'):
        """
        (TODO confirm w Victor or Matthew)
        Renders the environment for visualization purposes

        Parameters:
            mode (str) : TOOD
        """

        if (mode is 'human'):
            if (self._seed == 1):
                printWorld(self.world)
        else:
            return np.repeat((self.world+1)*127, 3, axis=-1).astype(dtype=np.uint8)
        """
        file = open("render.txt", "a")
        file.write(" — — — — — — — — — — — — — — — — — — — — — -\n")
        file.write(f"Episode number {self.current_episode}")
        file.write(f" in {self.current_step} steps\n")
        file.write(f"Reward: {self._last_reward}\n")
        file.write("\n");
        file.write(str(self.world));
        file.write("\n");
        file.close()
        """


    ##def close(self):
    def seed(self, seed):
        self._seed = seed;
