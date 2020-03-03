import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_field.envs.Field2D import Field

class FieldEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    
    def __init__(self):
        
        self.action_space = spaces.Discrete(4)
        self.reset()
        
        print("Initialized successfully");
        
    def hasVisited(self, x, y):
        if (self.visitField[y][x] == 1):
            return True
        else :
            return False
    
    def step(self, action):
        if (action < 0 or action >= 4):
            print("Invalid Action")
            return 0
        
        moved = True
        
        if (action == 0):
            ##Move North
            if (self.currentY - 1 < 0 or self.hasVisited(self.currentX,self.currentY - 1)):
                moved = False
            else :
                self.currentY = self.currentY - 1
            
        if (action == 1):
            ##Move East
            if (self.currentX + 1 >= 10 or self.hasVisited(self.currentX + 1,self.currentY)):
                moved = False
            else :
                self.currentX = self.currentX + 1
            
        if (action == 2):
            ##Move South
            if (self.currentY + 1 >= 10 or self.hasVisited(self.currentX,self.currentY + 1)):
                moved = False
            else :
                self.currentY = self.currentY + 1
            
        if (action == 3):
            if (self.currentX - 1 < 0 or self.hasVisited(self.currentX - 1,self.currentY)):
                moved = False
            else :
                self.currentX = self.currentX + 1
                
        if (moved):
            self.visitField[self.currentY][self.currentX] = 1
            
            newOil, newWater = self.Field.getRock(self.currentX,self.currentY).Drain(0,0,None)
            
            self.totalOil += newOil
            self.totalWater += newWater
            
            reward = (newOil - newWater - 1) * 1
            
            return self.Field.getLiquidField(), reward, False, {}
        else :
            return self.Field.getLiquidField(), -5, False, {}
    
    def reset(self):
        print("Reseting")
        
        FieldInput = [ [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]],
                       [[.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1], [.8,.1]] ]
        
        self.visitField = [ [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]
        
        self.Field = Field(FieldInput)
        
        self.currentX = 0
        self.currentY = 5
        self.visitField[5][0] = 1
        
        StartOil , startWater = self.Field.getRock(0,5).Drain(0,0,None)
        
        self.totalOil = 0
        self.totalOil += StartOil
        
        self.totalWater = 0
        self.totalWater += startWater
        
        return self.Field.getLiquidField()
    
    def render(self, mode='human'):
        file = open("render.txt", "a")
        file.write(" — — — — — — — — — — — — — — — — — — — — — -\n")
        file.write(f"Episode number {self.current_episode}\n")
        file.write(f"{self.success_episode[-1]} in {self.current_step} steps\n")
        file.close()

    
    ##def close(self):
    
    
