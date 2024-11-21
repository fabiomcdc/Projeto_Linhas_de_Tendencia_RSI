import pandas as pd
import numpy as np

# Checa Topos locais de ordem "order"
def checa_tops(data: np.array, curr_index: int, order: int) -> bool:
    if curr_index + 1 < order:
        return False
    top = True
    k = curr_index
    v = data.iloc[k]
    for i in range(-order, order + 1):
        if data.iloc[k + i] > v:
            top = False
            break
    
    return top

# Checa Fundos locais
def checa_bottoms(data: np.array, curr_index: int, order: int) -> bool:
    if curr_index +1 < order:
        return False

    bottom = True
    k = curr_index
    v = data.iloc[k]
    for i in range(-order, order + 1):
        if data.iloc[k + i] < v:
            bottom = False
            break

    return bottom
