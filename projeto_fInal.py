import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Library for plotting candles
# pip install mplfinance
import mplfinance as mpf 
# https://github.com/matplotlib/mplfinance/blob/master/examples/using_lines.ipynb

# from trendlines import check_trend_line
# from trendlines import optimize_slope
from import fit_trendlines_single
# from trendlines import fit_trendlines_high_low
from trendlines import get_line_points
from trendlines import eh_similar
from calcula_RSI import compute_rsi

# Carregando os dados
data = pd.read_csv('BTCUSDT86400.csv', parse_dates=['date'])
data = data.set_index('date')

# Take natural log of data to resolve price scaling issues
data_log = np.log(data)

# Cálculo do RSI
janela_rsi = 42
data['RSI'] = compute_rsi(data_log['close'],janela_rsi)
rsi_values = compute_rsi(data_log['close'], janela_rsi)

close_df = pd.DataFrame(data_log['close'])
close_df.to_csv('log_close.csv', index=True)

close_df = pd.DataFrame(data['close'])
close_df.to_csv('close.csv', index=True)

rsi_df = pd.DataFrame(data['RSI'])
rsi_df.to_csv('rsi_values.csv', index=True)

# Parâmetro
lookback = 300

# Inicializar DataFrames
support_slope = [np.nan] * len(rsi_values)
resist_slope = [np.nan] * len(rsi_values)
colunas_suporte = ['indice', 'indice_original_lower_pivot', 'support_slope', 'support_intercept']
colunas_resistencia = ['indice', 'indice_original_upper_pivot', 'resist_slope', 'resist_intercept']
trendlines_suporte_df = pd.DataFrame(columns=colunas_suporte)
trendlines_resistencia_df = pd.DataFrame(columns=colunas_resistencia)

for i in range(lookback - 1 + janela_rsi, len(rsi_values)):
    # Chamar a função fit_trendlines_single para a janela sendo avaliada
    lower_pivot, support_coefs, upper_pivot, resist_coefs = fit_trendlines_single(rsi_values[i-lookback+1:i+1])

    # Adicionar dados ao DataFrame
    nova_linha_suporte = {
        'indice': i - lookback -  janela_rsi + 1,
        'indice_original_lower_pivot': lower_pivot + i - lookback + 1,
        'support_slope': support_coefs[0],
        'support_intercept': support_coefs[1],
    }
    nova_linha_resistencia = {
        'indice': i - lookback -  janela_rsi + 1,
        'indice_original_upper_pivot': lower_pivot + i - lookback + 1,
        'resist_slope': resist_coefs[0],
        'resist_intercept': resist_coefs[1]
    }

    trendlines_suporte_df = trendlines_suporte_df._append(nova_linha_suporte, ignore_index=True)
    trendlines_resistencia_df = trendlines_resistencia_df._append(nova_linha_resistencia, ignore_index=True)


trendlines_suporte_df.to_csv('trendlines_suporte.csv', index=True)
trendlines_resistencia_df.to_csv('trendlines_resistencia.csv', index=True)

# Preparando o DataFrame para os resultados consolidados
cons_trendlines_suporte_df = pd.DataFrame(columns=['indice', 'indice_original_lower_pivot', 'support_slope', 'support_intercept'])

# Variáveis provisórias para armazenar os valores acumulados
prov_slope = 0
prov_intercept = 0
prov_indice = 0
prov_lower_pivot = 0
count = 1  # Contador para calcular a média

for i in range(len(trendlines_suporte_df)):
    row = trendlines_suporte_df.iloc[i]
    if i < len(trendlines_suporte_df) - 1:
        next_row = trendlines_suporte_df.iloc[i + 1]
        if (row['indice_original_lower_pivot'] == next_row['indice_original_lower_pivot'] and
            abs(row['support_slope'] - next_row['support_slope']) <= 0.001 and
            abs(row['support_intercept'] - next_row['support_intercept']) <= 2):
            # Acumular os valores para média
            prov_slope += row['support_slope']
            prov_intercept += row['support_intercept']
            prov_indice = row['indice']
            prov_lower_pivot = row['indice_original_lower_pivot']
            count += 1
        else:
            # Adicionar a média dos valores acumulados ao novo DataFrame
            cons_trendlines_suporte_df = cons_trendlines_suporte_df._append({
                'indice': prov_indice,
                'indice_original_lower_pivot': prov_lower_pivot,
                'support_slope': prov_slope / count,
                'support_intercept': prov_intercept / count
            }, ignore_index=True)
            # Resetar as variáveis provisórias
            prov_slope = row['support_slope']
            prov_intercept = row['support_intercept']
            prov_indice = row['indice']
            prov_lower_pivot = row['indice_original_lower_pivot']
            count = 1
    else:
        cons_trendlines_suporte_df = cons_trendlines_suporte_df._append({
            'indice': prov_indice,
            'indice_original_lower_pivot': prov_lower_pivot,
            'support_slope': prov_slope / count,
            'support_intercept': prov_intercept / count
        }, ignore_index=True)

cons_trendlines_suporte_df.to_csv('cons_trendlines_suporte.csv', index=True)



plt.style.use('dark_background')
fig, (ax1, ax3) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [2, 1]})

# Obter as datas associadas aos valores do RSI
datas = data.index[len(data.index) - len(rsi_values):]

linhas_df = pd.DataFrame(columns=['indice', 'x_vals', 'y_vals'])

# Plotar as linhas de tendência no RSI
for i in range(len(cons_trendlines_suporte_df)):
    row = cons_trendlines_suporte_df.iloc[i]
    if int(row['indice_original_lower_pivot']) == 362:
        x_vals = np.arange(len(rsi_values))
        y_vals = row['support_slope'] * (x_vals-int(row['indice_original_lower_pivot'])) + row['support_intercept']
        filtered_x_vals = datas[(y_vals >= 0) & (y_vals <= 100)]  # Usar datas em vez de números
        filtered_y_vals = y_vals[(y_vals >= 0) & (y_vals <= 100)]
        ax3.plot(filtered_x_vals, filtered_y_vals, color='r')  # Usar datas como eixo x

# Plotando o preço de fechamento
data['close'].plot(ax=ax1, color='blue', label='BTC-USDT Close Price')

# Plotando o RSI
data['RSI'].plot(ax=ax3, color='purple', label='RSI')
ax3.axhline(70, color='red', linestyle='--')  # Linha de sobrecompra
ax3.axhline(30, color='green', linestyle='--')  # Linha de sobrevenda

plt.legend()
ax1.set_title("BTC-USDT Price and RSI")
ax1.legend(loc='upper left')
ax3.legend(loc='upper left')
ax3.set_ylim([0, 100])  # O RSI varia de 0 a 100

plt.show()



'''
# Plot Trendlines on candles 



candles = data.iloc[-30:] # Last 30 candles in data
support_coefs_c, resist_coefs_c = fit_trendlines_single(candles['close'])
support_coefs, resist_coefs = fit_trendlines_high_low(candles['high'], candles['low'], candles['close'])

support_line_c = support_coefs_c[0] * np.arange(len(candles)) + support_coefs_c[1]
resist_line_c = resist_coefs_c[0] * np.arange(len(candles)) + resist_coefs_c[1]

support_line = support_coefs[0] * np.arange(len(candles)) + support_coefs[1]
resist_line = resist_coefs[0] * np.arange(len(candles)) + resist_coefs[1]

plt.style.use('dark_background')
ax = plt.gca()

def get_line_points(candles, line_points):
    idx = candles.index
    line_i = len(candles) - len(line_points)
    assert(line_i >= 0)
    points = []
    for i in range(line_i, len(candles)):
        points.append((idx[i], line_points[i - line_i]))
    return points

s_seq = get_line_points(candles, support_line)
r_seq = get_line_points(candles, resist_line)
s_seq2 = get_line_points(candles, support_line_c)
r_seq2 = get_line_points(candles, resist_line_c)
mpf.plot(candles, alines=dict(alines=[s_seq, r_seq, s_seq2, r_seq2], colors=['w', 'w', 'b', 'b']), type='candle', style='charles', ax=ax)
plt.show()

'''

'''
plt.style.use('dark_background')
fig, (ax1, ax3) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [2, 1]})
ax2 = ax1.twinx()

# Plotando o preço de fechamento
data['close'].plot(ax=ax1, color='blue', label='BTC-USDT Close Price')

# Plotando o RSI
data['RSI'].plot(ax=ax3, color='purple', label='RSI')

#data['support_slope'].plot(ax=ax2, label='Support Slope', color='green')
#data['resist_slope'].plot(ax=ax2, label='Resistance Slope', color='red')
plt.legend()
ax1.set_title("BTC-USDT Price and RSI")
ax1.legend(loc='upper left')
ax3.legend(loc='upper left')
ax3.set_ylim([0, 100])  # O RSI varia de 0 a 100
ax3.axhline(70, color='red', linestyle='--')  # Linha de sobrecompra
ax3.axhline(30, color='green', linestyle='--')  # Linha de sobrevenda
mpf.plot(rsi_values, alines=dict(alines=[s_seq], colors=['w']), type='line', style='charles', ax=ax3)
plt.show()

'''