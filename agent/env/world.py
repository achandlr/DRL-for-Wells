import numpy as np

NOTHING = 0
PLAYER = 1
OIL = 0.5
WATER = -0.5
WALL = -1

mapper = {"_": NOTHING, "P": PLAYER, "O": OIL, "W": WATER}
mapperInv = {NOTHING: "_", PLAYER: "P", OIL: "O", WATER: "W", WALL: "|"}


##reads through a txt file and makes an array representing the oil field
def parseWorld():
    worldFile = open("env/world.txt", "r")
    totalField = None
    for line in worldFile.readlines():
        values = list(line)[:-1]
        fieldLine = np.array([list(map(lambda x: [mapper[x]], values))])
        if totalField is None:
            totalField = fieldLine
        else:
            totalField = np.append(totalField, fieldLine, axis=0)
    return totalField

##prints out the world with symbols representing a space instead of a number
def printWorld(world):
    final = ""
    for row in world:
        for el in row:
            print(mapperInv[el[0]], end="")
        print("")
