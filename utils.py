import numpy as np

def preprocess(data):
    arr = np.array(data).reshape(1, -1)
    arr = (arr - np.mean(arr)) / (np.std(arr) + 1e-8)
    return arr.reshape(1, arr.shape[1], 1)