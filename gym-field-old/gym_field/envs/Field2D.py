distanceFactor = .1

porosityFactor = 1


class Field:

    ## Initalizes Field class from list of liquid quantities
    def __init__(self, liquidField):

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

    ## Return rock at given x,y coordinates
    def getRock(self, x, y):
        return self.field[y][x]

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
                
    
    def printField(self):

        for row in self.field:

            rowString = "| "
            for rock in row:
                rowString += str("%0.3f" % rock.getLiquid())
                rowString += " "
            rowString += "|"

            print(rowString)

    ## Returns all neighbors to given x,y Rock
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

    ## Initializes rock
    def __init__(self, x, y, oil, water, Field):
        self.x = x
        self.y = y
        self.oil = oil
        self.water = water
        self.liquid = (oil + water)
        self.porosity = (1 - self.liquid)
        self.field = Field

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getOil(self):
        return self.oil

    def getWater(self):
        return self.water

    def getLiquid(self):
        return self.liquid

    ## Sets liquid to updated ammount
    def updateLiquids(newOil, newWater):
        self.oil = newOil
        self.water = newWater
        self.liquid = (newOil + newWater)

    def getPorosity(self):
        return self.porosity

    def getField(self):
        return self.field

    def setLiquid(self, ammount):
        self.liquid = ammount

    ## Important
    def FlowCalculation(self, Distance, porosityTotal):
        return (1 - Distance) * (1 - porosityTotal) * self.liquid

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

    ## Drains liquid from this rock and neighboring rocks
    def Drain(self, porosityTotal, Distance, Parent):

        ##Need to experiment with best function here
        porosityTotal += (self.porosity * porosityFactor)

        if (Distance > 1 or porosityTotal > 1):
            return 0, 0

        totalOil = 0
        totalWater = 0

        if (self.liquid > 0):
            ##Second important function we need to decide on
            flowCalc = self.FlowCalculation(Distance, porosityTotal)

            oilDrawn, waterDrawn = self.DrawLiquid(flowCalc)

            totalOil += oilDrawn
            totalWater += waterDrawn

        for Rock in self.field.getNeighbors(self.x, self.y):
            if (not (Rock is Parent)):
                childOil, childWater = Rock.Drain(porosityTotal, Distance + distanceFactor, self)
                totalOil += childOil
                totalWater += childWater

        return totalOil, totalWater