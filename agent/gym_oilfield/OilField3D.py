import numpy as np



class oilField():

    """
    Class that represents a three dimensional oil field

    Parameters:
        length (float) : Value representing the length of the oil field
        width (float) : Value representing the width of the oil field
        depth (float) : Value representing the depth of the oil field
        liquidField (array) : Represents the liquid (oil and water) within
                              each rock object in an oil field
    """

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
                    porosity = max(1-oilPercent-waterPercent, 0)
                    newRock = Rock(x,y,z,oilPercent,waterPercent,porosity,self)

                    rockField[z][y][x] = newRock

        self.rockField = rockField

    """
    Returns the rock at a x, y, z position in the oil field

    Parameters:
        x (int) - x position of a rock object
        y (int) - y position of a rock object
        z (int) - z position of a rock object
    """
    def getRock(self,x,y,z):
        return self.rockField[z][y][x]

    """
        Creates and returns a list holding th values for oil and water at every
        position in the oil field

    """
    def getCurrentLiquidLevels(self):
        liquidField = np.empty([self.depth,self.length,self.width,2], dtype = np.float64)

        #Get the liquid values at each position
        for z in range(0, self.depth):
            for y in range(0, self.width):
                for x in range (0, self.length):
                    currentRock = self.rockField[z][y][x]

                    liquidLevels = []

                    liquidLevels.append(currentRock.getOilPercent())
                    liquidLevels.append(currentRock.getWaterPercent())

                    liquidField[z][y][x] = liquidLevels

        return liquidField

    """
        Prints out the liquid values at each position in the oil field
    
    """
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

    """
    Returns list of SINGLE-STEP neighbors

    Parameters:
        x (int) - x position of a rock object
        y (int) - y position of a rock object
        z (int) - z position of a rock object
    """
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

    """
        Calculates initial porosity value

    """
    def calculateInitialPorosity(oilPercent, waterPercent):
        return max(0, 1 - (oilPercent + waterPercent))

    PorosityFactor = 1

    """
        Determines by how much the porosity should be affected
        by a constant porosity factor
        
        Parameters:
            porosity (float) - the porosity of a rock

    """
    def incimentPorosityFactor(porosity):
        return porosity * PorosityFactor

    """
    Calculates how much liquid can be drawn based off the distance from the drill
    and the amount in the rock
    
    Parameters:
        porosity (float) : indicates the amount of porosity in a rock object
        distance (float) : the distance the current rock is from the drill
        zFactor (TODO) : TODO - Ask VICTOR
    """
    def drawCalculation(porosity, distance, zFactor):
        return max((1 - (distance/distanceLimit)) * (1 - (porosity/porosityLimit)) * (1 + (zFactor/100)),0)

    distanceLimit = 2
    porosityLimit = 2

    distanceFactor = .1

    class Rock:

        """
        Class stores the properties of a rock object within an oil field

        Parameters:
            x (int) : the x-positon of the rock in the oil field
            y (int) : the y-position of the rock in the oil field
            z (int) : the z-position of the rock in the oil field
            oilPercent (float) : the amount of oil in a rock as a percentage
            waterPercent (float) : the amount of water in a rock as a percentage
            porosity (float) : the porosity of a rock object

        """
        def __init__(self, x, y, z, oilPercent, waterPercent, porosity, parentField):
            self.x = x
            self.y = y
            self.z = z
            self.oilPercent = oilPercent
            self.waterPercent = waterPercent

            #self.porosity = calculateInitialPorosity(oilPercent,waterPercent)
            self.porosity = porosity

            self.parentField = parentField

        """
            Returns the oil percentage of a rock object
        """
        def getOilPercent(self):
            return self.oilPercent

        """
            Returns the water percentage of a rockField object
        """
        def getWaterPercent(self):
            return self.waterPercent

        """
            Returns the porosity of a rock object
        """
        def getPorosity(self):
            return self.porosity

        """
            Updates the liquid within a rock object (oil and water)
            
            Parameters:
                newOil (float) - new value to set current oil to
                newWater (float) - new value to set current water to
        """
        def updateLiquid(self, newOil, newWater):
            self.oilPercent = newOil
            self.waterPercent = newWater

        """
            Returns the x, y, z coordinates of a rock object
        """
        def getLocation(self):
            coordinates = [self.x, self.y, self.z]
            return coordinates

        """
            Updates the porosity of a rock object
            
            Parameter:
                newPorosity (float) - the updated porosity of the rock object
        """
        def setPorosity(self, newPorosity):
            self.porosity = newPorosity

        """
            Gets the field in which this rock object is located
        """
        def getParentField(self):
            return self.parentField

        """
            Removes liquid from the current rock based on the amount to be drawn
            
            Parameter:
                drawAmmount (float) - the amount of liquid to be drawn 
        """
        def drawLiquid(self, drawAmmount):

            # empty all liquid if draw amount is more than what is in rock
            if (drawAmmount > (self.oilPercent + self.waterPercent)):
                dOil = self.oilPercent
                dWat = self.waterPercent

                self.updateLiquid(0,0)
                return dOil,dWat

            dOil = 0
            dWat = 0


            drawAmmount = drawAmmount/2

            # draw water
            if (drawAmmount > self.waterPercent):
                dWat = self.waterPercent
                self.updateLiquid(self.oilPercent,0)
            else :
                dWat = drawAmmount
                self.updateLiquid(self.oilPercent, self.waterPercent - drawAmmount)

            # draw oil
            if (drawAmmount > self.oilPercent):
                dOil = self.oilPercent
                self.updateLiquid(0,self.waterPercent)
            else:
                dOil = drawAmmount
                self.updateLiquid(self.oilPercent - drawAmmount, self.waterPercent)

            return dOil,dWat

        """
        Based off the distance from the drill, this updates the rock's liquid
        and porosity values
    
        Paramters:
            cummulativePorosity (float) : total porosity of rocks traversed 
            cummulativeDistance (float) : total distance of rocks traversed
            Parent (TODO) : rock object draining current rock object
            drainList (TODO) : list of rocks that have been visited during this drain step
        """
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
