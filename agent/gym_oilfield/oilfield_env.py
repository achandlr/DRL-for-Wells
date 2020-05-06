import gym
import numpy as np
import pandas as pd
from gym import error, spaces, utils
from gym.utils import seeding

# required for rendering
import plotly.express as px
from .OilField3D import oilField

"""

Represents an oil field through which the agent navigates and drills through

"""

class OilFieldEnv(gym.Env):
    metadata = {'render.modes':['human']}

    def __init__(self):
        ##Still need to initialize with info
        self.action_space = spaces.Discrete(6)

        self.reward_range = (-1,1)
        self.current_episode = 0
        self.current_step = 0
        self.max_step = 300
        self.cum_rew = 0

        ##Must call initData to give full data
        print("Initialized successfully")
        print("Call initData( drillStartInfo, length, width, depth, liquidField)")
        print("drillStartInfo - [x,y,z] of starting drill locations")
        print("liquidField - 3D numpyarray of [oil%,water%] lists")

    """

    Initializes starting values for the oil well

    Parameters:
        drillStartInfo (array) : Contains the starting x, y, z values for drill
        length (float) : the length of the oil field
        width (float) : the width of the oil field
        depth (float) : the depth of the oil field
        liquidField (array) : contains the liquid values for each rock in the field

    """
    def initData(self,drillStartInfo, length, width, depth, liquidField):
        self.observation_space = spaces.Box(low=-1, high=2, shape=(length, width, depth, 2), dtype=np.float64)

        self.oilField = oilField(length, width, depth, liquidField)

        self.length = length
        self.width = width
        self.depth = depth

        self.originalField = liquidField

        self.drillStartx = drillStartInfo[0]
        self.drillStarty = drillStartInfo[1]
        self.drillStartz = drillStartInfo[2]

        self.resetDrillInfo()

        return self.getCurrentState()

    ##Repositions the drill at the starting x, y, z values
    def resetDrillInfo(self):
        self.drillx = self.drillStartx
        self.drilly = self.drillStarty
        self.drillz = self.drillStartz

    ##Returns the current liquid values within the oil field
    def getCurrentState(self):
        return self.oilField.getCurrentLiquidLevels()

    """
    Calculates the reward for the previous action based off how successful
    the agent drilled oil

    Parameters:
        oilDrawn (float) : the amount oil drawn on the last step
        waterDrawn (float) : the amount of water drawn on the last step
    """
    def calculateReward(self,oilDrawn,waterDrawn):
        return (oilDrawn - waterDrawn)

    ##Determine best way to transfer actions
    actionSpace = {0: [0,0,-1], 1: [0,-1,0],
                   2: [1,0,0],  3: [0,1,0],
                   4: [-1,0,0], 5: [0,0,1]}

    ## Current action Space
    # 0 - move up directly
    # 1 - move north directly
    # 2 - move east directly
    # 3 - move south directly
    # 4 - move west directly
    # 5 - move down directly

    ##Returns the current x, y, z position of the drill
    def getLocationVector(self):
        return [self.drillx,self.drilly,self.drillz]

    ##Checks to see if the drill is inbounds and can actually drill something
    ##locationVector (array) - the location of the drill's current position
    def validLocation(self,locationVector):
        return  ((0 <= locationVector[0] and locationVector[0] < self.length ) and
                 (0 <= locationVector[1] and locationVector[1] < self.width ) and
                 (0 <= locationVector[2] and locationVector[2] < self.depth ))

    """
    Update the drill's x, y, z position based off the positions in the parameters

    Parameters:
        x (int) : new x position of the drill
        y (int) : new y position of the drill
        z (int) : new z position of the drill
    """
    def moveDrill(self,x,y,z):
        self.drillx = x
        self.drilly = y
        self.drillz = z

        Rock = self.oilField.getRock(x,y,z)

        Rock.setPorosity(0)

        emptyList = []

        oilDrawn, waterDrawn = Rock.drain(0,0,None, emptyList)

        self.storedReward = self.calculateReward(oilDrawn, waterDrawn)


    ##Updates the drill's position based off the agent's action
    ##action (int) - the move the agent is supposed to perform
    def performAction(self, action):
        currentLocation = self.getLocationVector()
        movementVector = self.actionSpace[action]

        currentLocation = np.add(currentLocation, movementVector)

        if (not self.validLocation(currentLocation)): return -100/100

        self.moveDrill(currentLocation[0],currentLocation[1],currentLocation[2])

    """
    A single move that the agent takes. Updates the reward and the location
    of the drill based of the agent's action

    Parameter:
        action (int) - plugged into the action space in order to acquire the
                       move the agent is supposed to make
    """
    def step(self, action):

        self.storedReward = 0

        if (not(action in self.actionSpace)):
            print("Invalid Action")
            return 0

        self.performAction(action)

        self.cum_rew += self.storedReward
        self.current_step += 1

        done = self.current_step >= self.max_step

        if done: self.current_episode += 1

        return self.getCurrentState(), self.storedReward, done, {}

    ##Reassigns variables to starting values
    def reset(self):
        ##print results before reset
        if (self.current_episode % 1000 == 0):
            print(f"On episode {self.current_episode}\n",flush=True)
            print(f"Last reward: {self.cum_rew}\n", flush=True)

        self.current_step = 0
        self.cum_rew = 0

        self.oilField = oilField(self.length,self.width,self.depth,self.originalField)

        self.resetDrillInfo()

        return self.getCurrentState()

    ##Creates a figure to visualize the oil field
    def render(self, mode='human'):
        '''
        file = open("render.txt", "a")
        file.write(" — — — — — — — — — — — — — — — — — — — — — -\n")
        file.write(f"Episode number {self.current_episode}\n")
        file.write(f"{self.success_episode[-1]} in {self.current_step} steps\n")
        file.close()
        '''

        data = []

        #fill in DataFrame with each rock's values
        for x in range(0, self.oilField.length):
            for y in range(0, self.oilField.width):
                for z in range(0, self.oilField.depth):
                    rock = self.oilField.getRock(x, y, z)
                    data.append([x, y, z, 1 - rock.getOilPercent() - rock.getWaterPercent(), rock.getOilPercent(), rock.getWaterPercent()])

        df = pd.DataFrame(data, columns = ['x', 'y', 'z', 'rock %', 'oil %', 'water %'])

        new_df = df.loc[df['x'] == self.drillx]
        fig = px.scatter_3d(new_df, x='x', y='y', z='z', color='oil %')
        fig.show(renderer = 'browser')

    ##def close(self):
