import numpy as np
def readData(dims):
    a = np.loadtxt("gym_oilfield/smallStructure", delimiter=",")
    return a.reshape(dims,dims,dims,-1)
