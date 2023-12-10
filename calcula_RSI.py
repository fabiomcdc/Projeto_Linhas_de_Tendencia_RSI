import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Função para calcular o RSI
def compute_rsi(data, window):
    delta = data.diff()
    delta_df = pd.DataFrame(delta)
    delta_df.to_csv('delta_values.csv', index=True)

    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    gain_df = pd.DataFrame(gain)
    gain_df.to_csv('gain_values.csv', index=True)

    loss_df = pd.DataFrame(loss)
    loss_df.to_csv('loss_values.csv', index=True)

    print(loss)
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi