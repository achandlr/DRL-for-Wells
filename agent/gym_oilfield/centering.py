import numpy as np
def shift1(arr, num, fill_value=np.nan):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result = arr
    return result


def shift2(arr, num, fill_value=np.nan):
    result = np.empty_like(arr)
    if num > 0:
        result[:,:num] = fill_value
        result[:,num:] = arr[:,:-num]
    elif num < 0:
        result[:,num:] = fill_value
        result[:,:num] = arr[:,-num:]
    else:
        result = arr
    return result

def shift3(arr, num, fill_value=np.nan):
    result = np.empty_like(arr)
    if num > 0:
        result[:,:,:num] = fill_value
        result[:,:,num:] = arr[:,:,:-num]
    elif num < 0:
        result[:,:,num:] = fill_value
        result[:,:,:num] = arr[:,:,-num:]
    else:
        result = arr
    return result

def center(field, x, y, z, size):
    return shift3(shift2(shift1(field, size//2 - z, 0), size//2 - y, 0), size//2 - x, 0)
