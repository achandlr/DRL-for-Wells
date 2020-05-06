import numpy as np
##reads in the data to make an oil field
def readData(dims):
    a = np.loadtxt("gym_oilfield/smallStructure", delimiter=",")
    return a.reshape(dims,dims,dims,-1)
