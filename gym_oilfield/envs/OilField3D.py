import numpy as np


class oilField():
        
    def __init__(self, length, width, depth, liquidField):
        # passed in x - length, y - width, z - depth
        # liquidField - 3D np array of [oil%, water%]
        
        self.length = length
        self.width = width
        self.depth = depth
        
        rockField = np.empty([depth,length,width], dtype = Rock)
        
        for z in range(0, depth):
            for y in range(0, width):
                for x in range(0, length):
                    oilPercent = liquidField[z][y][x][0]
                    waterPercent = liquidField[z][y][x][1]
                    newRock = Rock(x,y,z,oilPercent,waterPercent,self)
                    
                    rockField[z][y][x] = newRock
                    
        self.rockField = rockField
        
    def getRock(self,x,y,z):
        return self.rockField[z][y][x]
    
    def getCurrentLiquidLevels(self):
        liquidField = np.empty([self.depth,self.length,self.width,2], dtype = np.float64)
        
        for z in range(0, self.depth):
            for y in range(0, self.width):
                for x in range (0, self.length):
                    currentRock = self.rockField[z][y][x]
                    
                    liquidLevels = []
                    
                    liquidLevels.append(currentRock.getOilPercent())
                    liquidLevels.append(currentRock.getWaterPercent())
                    
                    liquidField[z][y][x] = liquidLevels
                    
        return liquidField
    
    def __str__(self):
        
        returnString = ""
        
        returnString += "--------------------\n"
        
        for z in range (0, self.depth):
            
            for y in range (0, self.width):
                
                for x in range (0, self.length):
                    currentRock = self.rockField[z][y][x]
                    
                    returnString += "["
                    returnString += str("%0.3f" % currentRock.getOilPercent())
                    returnString += ","
                    returnString += str("%0.3f" % currentRock.getWaterPercent())
                    returnString += "] "
                    
                returnString += "\n"
            
            returnString += "\n--------------------\n"
        
        return returnString
    
    ##Currently returns list of SINGLE-STEP neighbors
    def getRockNeighbors(self,x,y,z):
        returnList = []
        
        neighborOffsets = [
                   [0, 1 , 0,],
            [0, 0, -1],   [0, 0, 1],
                   [0, -1, 0],
            
            [-1,0,0], [1,0,0]
        ]
        
        for offset in neighborOffsets:
            ndepth = z + offset[0]
            nwidth =  y + offset[1]
            nlength = x + offset[2]
            
            if ( ndepth >= 0 and ndepth < self.depth and nwidth >= 0 and nwidth < self.width and
                 nlength >= 0 and nlength < self.length):
                returnList.append(self.getRock(ndepth,nwidth,nlength))
                
        return returnList
        
        
def calculateInitialPorosity(oilPercent, waterPercent):
        return 1 - (oilPercent + waterPercent)
    
    
PorosityFactor = 1

def incimentPorosityFactor(porosity):
    return porosity * PorosityFactor

def drawCalculation(porosity, distance, zFactor):
    return (1 - distance) * (1 - porosity) * (1 + (zFactor/100)) 

distanceLimit = 2
porosityLimit = 2

distanceFactor = .1

class Rock:
    
    def __init__(self, x, y, z, oilPercent, waterPercent, parentField):
        self.x = x
        self.y = y
        self.z = z
        self.oilPercent = oilPercent
        self.waterPercent = waterPercent
        
        self.porosity = calculateInitialPorosity(oilPercent,waterPercent)
        
        self.parentField = parentField
        
    def getOilPercent(self):
        return self.oilPercent
    
    def getWaterPercent(self):
        return self.waterPercent

    def getPorosity(self):
        return self.porosity
    
    def updateLiquid(self, newOil, newWater):
        self.oilPercent = newOil
        self.waterPercent = newWater
    
    def getLocation(self):
        coordinates = [self.x, self.y, self.z]
        return coordinates
    
    def setPorosity(self, newPorosity):
        self.porosity = newPorosity
    
    def getParentField(self):
        return self.parentField
    

    def drawLiquid(self, drawAmmount):

        if (drawAmmount > (self.oilPercent + self.waterPercent)):
            dOil = self.oilPercent
            dWat = self.waterPercent

            self.updateLiquid(0,0)
            return dOil,dWat

        dOil = 0
        dWat = 0
        
        drawAmmount = drawAmmount/2

        if (drawAmmount > self.waterPercent):
            dWat = self.waterPercent
            self.updateLiquid(self.oilPercent,0)
        else :
            dWat = drawAmmount
            self.updateLiquid(self.oilPercent, self.waterPercent - drawAmmount)

        if (drawAmmount > self.oilPercent):
            dOil = self.oilPercent
            self.updateLiquid(0,self.waterPercent)
        else:
            dOil = drawAmmount
            self.updateLiquid(self.oilPercent - drawAmmount, self.waterPercent)

        return dOil,dWat

    
    def drain(self, cummulativePorosity, cummulativeDistance, Parent, drainList):


        cummulativePorosity += incimentPorosityFactor(self.porosity)
        
        if (cummulativeDistance >= distanceLimit or cummulativePorosity >= porosityLimit):
            return 0,0

        oilDrawn = 0
        waterDrawn = 0

        ##Self

        if (self.oilPercent > 0 or self.waterPercent > 0):

            drawAmmount = 0

            zFactor = 0

            if (Parent != None):
                zFactor = (Parent.z - self.z)

            drawAmmount = drawCalculation(cummulativePorosity, cummulativeDistance, zFactor)

            oilD, waterD = self.drawLiquid(drawAmmount)

            oilDrawn += oilD
            waterDrawn += waterD

        drainList.append(self)


        ##Neighbors
        
        for Rock in self.parentField.getRockNeighbors(self.x,self.y,self.z):
            if (not(Rock in drainList)):
                childOil, childWater = Rock.drain(cummulativePorosity, cummulativeDistance + distanceFactor, self, drainList)
                oilDrawn += childOil
                waterDrawn += childWater
                
        return oilDrawn,waterDrawn

