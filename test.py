import numpy as np
def shift5(arr, num, fill_value=np.nan):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
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
        result[:] = arr
    return result


a = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(shift5(a, 1, 0));
print(shift2(a, 2, 0));
