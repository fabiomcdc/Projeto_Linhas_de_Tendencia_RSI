import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Função para calcular o RSI
def compute_rsi(data, window):
    delta = data.diff()
    delta_df = pd.DataFrame(delta)

    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    gain_df = pd.DataFrame(gain)
    loss_df = pd.DataFrame(loss)
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi