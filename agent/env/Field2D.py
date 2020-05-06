distanceFactor = .1

porosityFactor = 1


class Field:

    """
    Class that describes the properties of values within a well fieldLine

    """

    def __init__(self, liquidField):

        """

       Initalizes Field class from list of liquid quantities

       Parameter:
            liquidField (array) : Represents the amount of liquid (oil and water)
                                  at each position in the field

        """

        rockField = []

        for row in range(0, len(liquidField)):

            currentRow = []

            liquidRow = liquidField[row]

            for column in range(0, len(liquidRow)):
                currentRockLiquid = liquidField[row][column]

                newRock = Rock(column, row, currentRockLiquid[0], currentRockLiquid[1], self)

                currentRow.append(newRock)

            rockField.append(currentRow)

        self.field = rockField


    """
    Return rock at given x,y coordinates

    Parameters:
        x (int) : x position of a rock object
        y (int) : y position of a rock object
    """
    def getRock(self, x, y):
        return self.field[y][x]

    ## Returns the field with values indicating the amount of oil and water
    ## at each position
    def getLiquidField(self):
        liquidField = []

        rockField = self.field

        for row in rockField:
            for Rock in row:
                x = Rock.getX()
                y = Rock.getY()
                Oil = Rock.getOil()
                Water = Rock.getWater()

                liquidField.append([x,y,Oil,Water])

        return liquidField

    ## prints the field and displays the amount of oil/water at each position
    def printField(self):

        for row in self.field:

            rowString = "| "
            for rock in row:
                rowString += str("%0.3f" % rock.getLiquid())
                rowString += " "
            rowString += "|"

            print(rowString)

    """
    Returns all neighbors to given x,y Rock

    Parameters:
        x (int) : x position of a rock object
        y (int) : y position of a rock object
    """
    def getNeighbors(self, x, y):
        returnList = []

        ## Theres a better way to do this
        if (x - 1 >= 0):
            returnList.append(self.field[y][x - 1])
        if (x + 1 < len(self.field[y])):
            returnList.append(self.field[y][x + 1])

        if (y - 1 >= 0):
            returnList.append(self.field[y - 1][x])
        if (y + 1 < len(self.field)):
            returnList.append(self.field[y + 1][x])

        return returnList


class Rock:

    """

    Rock class that describe a rock's properties and how they change based
    off an action (such as being drilled)

    """

    """
    Initializes rock

    Parameters:
        x (int) : x position of the rock object
        y (int) : y position of the rock object
        oil (float TODO check?) : the amount of oil in the rock object
        water (float TODO check?) : the amount of water in the rock object
        Field (TODO) : TODO
    """
    def __init__(self, x, y, oil, water, Field):
        self.x = x
        self.y = y
        self.oil = oil
        self.water = water
        self.liquid = (oil + water)
        self.porosity = (1 - self.liquid)
        self.field = Field

    ##Returns the x position of the current rock object
    def getX(self):
        return self.x

    ##Returns the x position of the current rock object
    def getY(self):
        return self.y

    ##Returns the amount of oil within the rock object
    def getOil(self):
        return self.oil

    ##Returns the amount of water within the rock object
    def getWater(self):
        return self.water

    ##Returns the amount of liquid (oil and water) within a rock object
    def getLiquid(self):
        return self.liquid

    """
    Sets liquid to updated ammount

    Parameters:
        newOil (float) : updated oil value of rock object
        newWater (float) : updated water value of rock object
    """
    def updateLiquids(newOil, newWater):
        self.oil = newOil
        self.water = newWater
        self.liquid = (newOil + newWater)

    ## Returns the porosity of a rock object
    def getPorosity(self):
        return self.porosity

    ## Returns the field
    def getField(self):
        return self.field

    ## Updates the total liquid within a rock object to the param amount
    def setLiquid(self, ammount):
        self.liquid = ammount

    ## Calculates how much a given rock object's liquid will flow out of rock
    def FlowCalculation(self, Distance, porosityTotal):
        return (1 - Distance) * (1 - porosityTotal) * self.liquid

    ## Removes liquid from a given rock object. Amount drawn is based on the
    ## parameter liquidDrawn (float TODO check?)
    def DrawLiquid(self, liquidDrawn):
        percentOil = 0
        if (self.oil > 0):
            percentOil = self.oil / self.liquid

        percentWater = 0
        if (self.water > 0):
            percentWater = self.water / self.liquid

        intendDrawOil = liquidDrawn * percentOil
        intendDrawWater = liquidDrawn * percentWater

        if (intendDrawOil > self.oil):
            intendDrawOil = self.oil
        if (intendDrawWater > self.water):
            intendDrawWater = self.water

        self.oil = max(0, self.oil - intendDrawOil)
        self.water = max(0, self.water - intendDrawWater)
        self.liquid = self.oil + self.water

        return intendDrawOil, intendDrawWater

    """
    Drains liquid from this rock and neighboring rocks

    Parameters:
        porosityTotal (float) : TODO
        Distance (TODO) : The distance the current rock object is from the drill
        Parent (TODO) : TODO
    """
    def Drain(self, porosityTotal, Distance, Parent):

        ##Need to experiment with best function here
        porosityTotal += (self.porosity * porosityFactor)

        if (Distance > 1 or porosityTotal > 1):
            return 0, 0

        totalOil = 0
        totalWater = 0

        ## drain current rock object
        if (self.liquid > 0):
            ##Second important function we need to decide on
            flowCalc = self.FlowCalculation(Distance, porosityTotal)

            oilDrawn, waterDrawn = self.DrawLiquid(flowCalc)

            totalOil += oilDrawn
            totalWater += waterDrawn

        ## drain neighbors
        for Rock in self.field.getNeighbors(self.x, self.y):
            if (not (Rock is Parent)):
                childOil, childWater = Rock.Drain(porosityTotal, Distance + distanceFactor, self)
                totalOil += childOil
                totalWater += childWater

        return totalOil, totalWater
