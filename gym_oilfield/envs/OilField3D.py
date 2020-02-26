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
        currentLiquidField = self.getCurrentLiquidLevels()
        
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
            ndepth = offset[0]
            nwidth = offset[1]
            nlength = offset[2]
            
            if ( ndepth >= 0 and ndepth < self.depth and nwidth >= 0 and nwidth < self.width and
                 nlength >= 0 and nlength < self.length):
                returnList.append(self.getRock(ndepth,nwidth,nlength))
                
        return returnList
        
        
def calculateInitialPorosity(oilPercent, waterPercent):
        return 1 - (oilPercent + waterPercent)
    
    
PorosityFactor = 1
def calculatePorosityFactor(porosity):
    return porosity * PorosityFactor

def flowCalculation(Distance, porosityTotal,totalLiquidPercent):
    return (1 - Distance) * (1 - porosityTotal) * totalLiquidPercent

distanceLimit = 1
porosityLimit = 1
    
distanceFactor = .1

class Rock:
    
    def __init__(self, x, y, z, oilPercent, waterPercent, parentField):
        self.x = x;
        self.y = y;
        self.z = z;
        self.oilPercent = oilPercent;
        self.waterPercent = waterPercent;
        
        self.totalLiquidPercent = oilPercent + waterPercent;
        
        self.porosity = calculateInitialPorosity(oilPercent,waterPercent)
        
        self.parentField = parentField
        
    def getOilPercent(self):
        return self.oilPercent
    
    def getWaterPercent(self):
        return self.waterPercent
    
    def updateLiquid(self, newOil, newWater):
        self.oilPercent = newOil
        self.waterPercent = newWater
    
    def getLocation(self):
        coordinates = [self.x, self.y, self.z]
        return coordinates
    
    def getTotalLiquidPercent(self):
        return self.totalLiquidPercent
    
    def getPorosity(self):
        return self.porosity
    
    def setPorosity(self, newPorosity):
        self.porosity = newPorosity
    
    def getParentField(self):
        return self.parentField
    
    def drawLiquid(self, ammountDrawn):
        return 0
    
    def flowCalculation(self, Distance, porosityTotal):
        return (1 - Distance) * (1 - porosityTotal) * self.totalLiquidPercent
    
    def drawLiquid(self, flowCalc):
        percentOil = 0
        if (self.oilPercent > 0):
            percentOil = self.oilPercent/self.totalLiquidPercent
            
        percentWater = 0
        if (self.waterPercent > 0):
            percentWater = self.waterPercent/self.totalLiquidPercent
            
        intendDrawOil = percentOil * flowCalc
        intendDrawWater = percentWater * flowCalc
        
        if (intendDrawOil > self.oilPercent):
            intendDrawOil = self.oilPercent
        if (intendDrawWater > self.waterPercent):
            intendDrawWater = self.waterPercent
            
        self.oilPercent = max(0, self.oilPercent - intendDrawOil)
        self.waterPercent = max(0, self.waterPercent - intendDrawWater)
        
        self.totalLiquidPercent = self.oilPercent + self.waterPercent
        
        return intendDrawOil,intendDrawWater
    
    def drain(self, porosityTotal, Distance, Parent):
        
        porosityTotal += calculatePorosityFactor(self.porosity)
        
        if (Distance >= distanceLimit or porosityTotal >= porosityLimit):
            return 0,0
        
        oilDrawn = 0
        waterDrawn = 0
        
        ##Get self
        if (self.totalLiquidPercent > 0):
            flowCalc = flowCalculation(Distance, porosityTotal, self.totalLiquidPercent)
            
            oilD, waterD = self.drawLiquid(flowCalc)
            
            oilDrawn += oilD
            waterDrawn += waterD
        
        ##Get Neighbors
        
        for Rock in self.parentField.getRockNeighbors(self.x,self.y,self.z):
            if (not(Rock is Parent)):
                childOil, childWater = Rock.drain(porosityTotal, Distance + distanceFactor, self)
                oilDrawn += childOil
                waterDrawn += childWater
                
        return oilDrawn,waterDrawn

