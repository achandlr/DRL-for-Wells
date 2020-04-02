import numpy as np
import pandas as pd

# required for rendering
import plotly.express as px

import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_oilfield.envs.OilField3D import oilField

class OilFieldEnv(gym.Env):
    metadata = {'render.modes':['human']}
    
    def __init__(self):
        ##Still need to initialize with info
        self.action_space = spaces.Discrete(6)
        ##Must call initData to give full data
        print("Initialized successfully")
        print("Call initData( drillStartInfo, length, width, depth, liquidField)")
        print("drillStartInfo - [x,y,z] of starting drill locations\n
               liquidField - 3D numpyarray of [oil%,water%] lists")
        
    
    def initData(self,drillStartInfo, length, width, depth, liquidField):
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
        
    def resetDrillInfo():
        self.drillx = self.drillStartx
        self.drilly = self.drillStarty
        self.drillz = self.drillStartz
        
    def getCurrentState(self):
        return self.oilField.getCurrentLiquidLevels()
    
    
    ##Determine best way to transfer actions
    actionSpace = [1,2,3,4,5,6]
    
    ## Current action Space
    # 0 - move down directly
    # 1 - move north directly
    # 2 - move east directly
    # 3 - move south directly
    # 4 - move west directly
    # 5 - move up directly
    
    
    def getActionRequirements(self, action):
        if (action == 0):
            return (self.drillz + 1 < self.depth)
        elif (action == 1):
            return (self.drilly - 1 >= 0)
        elif (action == 2):
            return (self.drillx + 1 < self.length)
        elif (action == 3):
            return (self.drilly + 1 < self.width)
        elif (action == 4):
            return (self.drillx - 1 >= 0)
        elif (action == 5):
            return (self.drillz - 1 >= 0)
        
    def moveDrill(self,x,y,z):
        self.drillx = x
        self.drilly = y
        self.drillz = z
        
        Rock = self.oilField.getRock(x,y,z)
        
        Rock.setPorosity(0)
        
        oilDrawn, waterDrawn = Rock.drain(0,0,None);
        
        self.storedReward = calulateReward(oilDrawn, waterDrawn)
        
        
    def calculateReward(self,oilDrawn,waterDrawn):
        return (oilDrawn - waterDrawn)
    
    def performAction(self, action):
        if(action == actionSpace[0] and self.getActionRequirements(actionSpace[0])):
            self.moveDrill(self.drillx,self.drilly,self.drillz - 1)
            
        elif (action == actionSpace[1] and self.getActionRequirements(1)):
            self.moveDrill(self.drillx,self.drilly - 1,self.drillz)
            
        elif (action == actionSpace[2] and self.getActionRequirements(2)):
            self.moveDrill(self.drillx+1,self.drilly,self.drillz)
            
        elif (action == actionSpace[3] and self.getActionRequirements(3)):
            self.moveDrill(self.drillx,self.drilly+1,self.drillz)
            
        elif (action == actionSpace[4] and self.getActionRequirements(4)):
            self.moveDrill(self.drillx-1,self.drilly,self.drillz)
            
        elif (action == actionSpace[5] and self.getActionRequirements(5)):
            self.moveDrill(self.drillx,self.drilly,self.drillz+1)
            
        
        
    def step(self, action):
        
        self.storedReward = 0;
        
        if (not(action in actionSpace)):
            print("Invalid Action")
            return 0
        
        self.performAction(action)
        
        return self.getCurrentState(), self.storedReward, False, {}
        
        
    def reset(self):
        self.oilField = oilField(self.length,self.width,self.depth,self.originalField)
        
        
    def render(self, mode='human'):
        '''
        file = open("render.txt", "a")
        file.write(" — — — — — — — — — — — — — — — — — — — — — -\n")
        file.write(f"Episode number {self.current_episode}\n")
        file.write(f"{self.success_episode[-1]} in {self.current_step} steps\n")
        file.close()
        '''
        
        data = []

        for x in range(0, oilField.length):
            for y in range(0, oilField.width):
                for z in range(0, oilField.depth):
                    rock = oilField.getRock(x, y, z)
                    data.append([x, y, z, 1 - rock.getOilPercent() - rock.getWaterPercent(), rock.getOilPercent(), rock.getWaterPercent()])

        df = pd.DataFrame(data, columns = ['x', 'y', 'z', 'rock %', 'oil %', 'water %'])
        
        new_df = df.loc[df['x'] == self.drillx]
        fig = px.scatter_3d(new_df, x='x', y='y', z='z', color='oil %')
        fig.show(renderer = 'browser')
        
    ##def close(self):