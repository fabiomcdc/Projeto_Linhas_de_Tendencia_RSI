# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from backtesting import Backtest, Strategy

# ---------------------------------------------------------------------
#  Eliminando warnings indesejados 
# ---------------------------------------------------------------------

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

# ---------------------------------------------------------------------
#  Importando rotinas
# ---------------------------------------------------------------------

from trendlines import ajustar_linha_de_tendencia
from trendlines import mapear_retas_com_bottoms
from trendlines import mapear_retas_com_tops
from trendlines import identificar_retas_similares_suporte
from trendlines import identificar_retas_similares_resistencia
from trendlines import checar_cruzou_para_baixo
from trendlines import checar_cruzou_para_cima
from tops_e_bottoms import checa_tops
from tops_e_bottoms import checa_bottoms
from calcula_RSI import compute_rsi



# ---------------------------------------------------------------------
#  Definindo parâmetros
# ---------------------------------------------------------------------

# janela_rsi determina o número de amostras sobre os quais o RSI é calculado
janela_rsi = 28

# ordem determina quantos pontos à direita e à esquerda examinamos para determina pontos de máximo (tops) e mínimos (bottoms) locais
ordem = 4

# lookback determina o tamanho da janela de inspeção que será usada para encontrar as linhas de tendências
lookback1 = 50
lookback2 = 90
lookback3 = 120
lookback4 = 300

# distancia_maxima determina a distancia máxima na vertical que uma linha deve passar para considerar que passou pelo ponto
distancia_maxima = 3

# num_pontos determina quantos pontos queremos na linha de tendência no mínimo
num_pontos = 3

# break_min determina a distãncia mínima na vertical do ropomimento para uma reta ser considerada rompida
break_min = 3

# pontos_para_tras determina quantos pontos para trás eu checo o rompimento
pontos_para_tras = 6

# sl = stop loss e pt = profit taking
sl_val = 0.02
pt_val = 0.04

# datas do intervalo sendo avaliado
start_date = "2000-01-01"
end_date = "2004-12-31"

# ---------------------------------------------------------------------
#  Carregando os dados
# ---------------------------------------------------------------------

# datas do intervalo sendo avaliado

start_date = "2000-01-01"
end_date = "2004-12-31"

# Escolha do ativo (ind_indice determina quais variáveis vamos usar para fazer o estudo)
# 1 = bitcoin
# 2 = ibov
# 3 = S&P 500
# 4 = FTSE All Share
# 5  = DAX
# 6 = Nikkei 225

ind_indice = 5

indices = {
    1: "BTC-USD",    # Ticker para Bitcoin
    2: "^BVSP",      # Ticker para Ibovespa
    3: "^GSPC",      # Ticker para S&P 500
    4: "AAPL",      # Ticker para AAPL
    5: "JPY=X",     # Ticker para YEN
    6: "BRL=X"       # Ticker para BRL
}

aplicar_log = False

ticker = indices.get(ind_indice)

if ticker:
    # Importa os dados do Yahoo Finace
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Remove caracteres inválidos para nome de arquivo (como "^" no caso de tickers)
    ticker_clean = ticker.replace("^", "")
    
    # Gera o nome do arquivo com base no índice escolhido
    file_name = f'dados_csv_produzidos/dados_originais/data_{ticker_clean}.csv'

else:
    print("Índice inválido")

# Carregando o arquivo CSV
# data = pd.read_csv('dados_csv_produzidos/dados_originais/data_BVSP.csv')

# Converter colunas numéricas (exceto 'Date', que é uma string)
colunas_numericas = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# Converter as colunas para tipo numérico (ignorar erros caso já esteja no formato correto)
data[colunas_numericas] = data[colunas_numericas].apply(pd.to_numeric, errors='coerce')

# Salvando os dados em arquivo para verificação eventual
data.to_csv(file_name, index=True)



# ---------------------------------------------------------------------
# Calculando o RSI
# ---------------------------------------------------------------------

# Preparando base para o RSI, dependendo se vai usar log ou não

if aplicar_log:
    colunas_numericas_para_log = ['Open', 'High', 'Low', 'Close', 'Adj Close']
    data_log = np.log(data[colunas_numericas_para_log]) # Aplicando logaritmo nas colunas numéricas exceto volume
    data['RSI'] = compute_rsi(data_log['Close'],janela_rsi)
    rsi_values = compute_rsi(data_log['Close'], janela_rsi)
else:
    data['RSI'] = compute_rsi(data['Close'],janela_rsi)
    rsi_values = compute_rsi(data['Close'], janela_rsi)

rsi_df = pd.DataFrame(data['RSI'])



file_name = f'dados_csv_produzidos/dados_rsi/rsi_values_{ticker_clean}.csv'
rsi_df.to_csv(file_name, index=True)



# ---------------------------------------------------------------------
# Criando os mínimos e máximos locais
# ---------------------------------------------------------------------

tops = []
bottoms = []

for i in range(janela_rsi + ordem - 1, len(data['RSI']) - ordem - 1):
    if checa_tops(data['RSI'], i, ordem):
        top = [i, data['RSI'].iloc[i]]
        tops.append(top)

for i in range(janela_rsi + ordem - 1, len(data['RSI']) - ordem - 1):
    if checa_bottoms(data['RSI'], i, ordem):
        bottom = [i, data['RSI'].iloc[i]]
        bottoms.append(bottom)

tops_df = pd.DataFrame(tops, columns=['top_bottom_idx', 'top_bottom_value'])
tops_df = tops_df.dropna(subset=['top_bottom_value'])
file_name = f'dados_csv_produzidos/minimos_maximos_locais/maximos_locais_{ticker_clean}.csv'
tops_df.to_csv(file_name, index=True)

bottoms_df = pd.DataFrame(bottoms, columns=['top_bottom_idx', 'top_bottom_value'])
bottoms_df = bottoms_df.dropna(subset=['top_bottom_value'])
file_name = f'dados_csv_produzidos/minimos_maximos_locais/minimos_locais_{ticker_clean}.csv'
bottoms_df.to_csv(file_name, index=True)

idx = data.index



# ---------------------- Início de código para geração de gráfico auxiliar, comentado para performance ----------------------

#-----------------------------------------------------------------------   
# Plotando o as linhas de sobrecompra (RSI = 70) e sobrevenda (RSI = 30)
#-----------------------------------------------------------------------   

plt.style.use('default')
fig, (ax1, ax3) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [2, 1]})

#----------------------------------------------------------------   
# Plotando o preço de fechamento
#----------------------------------------------------------------   

data['Close'].plot(ax=ax1, color='blue', label=ticker_clean + ' Close Price', linewidth = 0.4)

#----------------------------------------------------------------   
# Plotando o RSI
#----------------------------------------------------------------   

data['RSI'].plot(ax=ax3, color='purple', label='RSI', linewidth = 0.5)

#-----------------------------------------------------------------------   
# Plotando o as linhas de sobrecompra (RSI = 70) e sobrevenda (RSI = 30)
#-----------------------------------------------------------------------
   
ax3.axhline(70, color='gray', linestyle='--', linewidth = 0.4)  # Linha de sobrecompra
ax3.axhline(30, color='gray', linestyle='--', linewidth = 0.4)  # Linha de sobrevenda

plt.legend()
ax1.set_title(ticker_clean + " and RSI", color='black', fontsize=8)
ax1.legend(loc='upper left', fontsize=6)
ax3.legend(loc='upper left', fontsize=6)
ax3.set_ylim([0, 100])  # O RSI varia de 0 a 100

# ----------------------------------------------------------------   
# Plotar os topos e fundos no gráfico
# ----------------------------------------------------------------

for top in tops_df.itertuples():
    # Plotar cada topo no gráfico RSI usando a data correspondente
    ax3.plot(idx[top.top_bottom_idx], data['RSI'][top.top_bottom_idx], marker='o', color='green', markersize=1)

for bottom in bottoms_df.itertuples():
    # Plotar cada fundo no gráfico RSI usando a data correspondente
    ax3.plot(idx[bottom.top_bottom_idx], data['RSI'][bottom.top_bottom_idx], marker='o', color='red', markersize=1)

# ----------------------------------------------------------------
# Ajustando o título e diminuir o tamanho da fonte
# ----------------------------------------------------------------

ax1.set_title(ticker_clean + " and RSI", color='black', fontsize=8)

# ----------------------------------------------------------------
# Reduzindo o tamanho da fonte dos valores da escala
# ----------------------------------------------------------------

ax1.tick_params(axis='both', which='major', labelsize=6)  # Tamanho da fonte dos ticks de ax1
ax3.tick_params(axis='both', which='major', labelsize=6)  # Tamanho da fonte dos ticks de ax3

# ----------------------------------------------------------------
# Salvando e plotando
# ----------------------------------------------------------------

file_name = f'graficos_gerados/mínimos_máximos_{ticker_clean}.png'
fig.savefig(file_name, dpi=300)  # Salva a figura como um arquivo PNG com alta resolução

plt.show()

# ---------------------- Fim de código para geração de gráfico auxiliar, comentado para performance ----------------------

# ---------------------------------------------------------------------
# Construção das retas de suporte para as janelas de observação
# ---------------------------------------------------------------------

# Estabelecendo contador e ponto inicial

contador_janela = 0
borda_esquerda = bottoms_df['top_bottom_idx'].iloc[0]

# Inicializando DataFrames

support_slope = [np.nan] * len(rsi_values)
colunas_resistencia = ['indice', 'indice_original_upper_pivot','valor_rsi', 'resist_slope', 'resist_intercept', 'inicio_janela', 'fim_janela']
colunas_suporte     = ['indice', 'indice_original_lower_pivot', 'valor_rsi', 'support_slope', 'support_intercept', 'inicio_janela', 'fim_janela']

trendlines_suporte_df = pd.DataFrame(columns=colunas_suporte)

for x in [lookback1, lookback2, lookback3]:
# for x in [lookback1]:
    lookback = x
    borda_esquerda = bottoms_df['top_bottom_idx'].iloc[0]-ordem
    while borda_esquerda + lookback < len(rsi_values):
    
        subset_tops_df = bottoms_df[(bottoms_df['top_bottom_idx'] >= borda_esquerda) & (bottoms_df['top_bottom_idx'] <= borda_esquerda+lookback-ordem)]

        if not subset_tops_df.empty:
            # Chamar a função ajustar_linha_de_tendencia para a janela sendo avaliada
            lower_pivot, lower_pivot_y, suport_slope_1, suport_slope_2 = ajustar_linha_de_tendencia(rsi_values[borda_esquerda:borda_esquerda+lookback], borda_esquerda, subset_tops_df, True)
            
            if suport_slope_1 != None:   
                nova_linha_suporte_1 = {
                    'indice': contador_janela,
                    'indice_original_lower_pivot': lower_pivot,
                    'valor_rsi': lower_pivot_y,
                    'support_slope': suport_slope_1,
                    'support_intercept':lower_pivot_y - lower_pivot * suport_slope_1,
                    'inicio_janela': borda_esquerda,
                    'fim_janela':borda_esquerda + lookback - 1
                }
                trendlines_suporte_df = trendlines_suporte_df._append(nova_linha_suporte_1, ignore_index=True)      
                contador_janela += 1

            if suport_slope_2 != None:
                nova_linha_suporte_2 = {
                    'indice': contador_janela,
                    'indice_original_lower_pivot': lower_pivot,
                    'valor_rsi': lower_pivot_y,
                    'support_slope': suport_slope_2,
                    'support_intercept':lower_pivot_y - lower_pivot * suport_slope_2,
                    'inicio_janela': borda_esquerda,
                    'fim_janela':borda_esquerda + lookback - 1
                }
                trendlines_suporte_df = trendlines_suporte_df._append(nova_linha_suporte_2, ignore_index=True)        
                contador_janela += 1     
        
        try:
            proximo_esquerda = bottoms_df.loc[bottoms_df['top_bottom_idx'].gt(borda_esquerda), 'top_bottom_idx'].min()
            rolagem_1 = proximo_esquerda - borda_esquerda
        except IndexError:
            proximo_esquerda = None  # Ou qualquer valor padrão que você queira usar

        try:
            proximo_direita = bottoms_df.loc[bottoms_df['top_bottom_idx'].gt(borda_esquerda+lookback), 'top_bottom_idx'].min()
            rolagem_2 = proximo_direita - (borda_esquerda + lookback)
        except IndexError:
            proximo_direita = None  # Ou qualquer valor padrão que você queira usar

        if proximo_esquerda == None:
            if proximo_direita == None:
                break
            else:
                rolagem = rolagem_2
        else:
            if proximo_direita == None:
                rolagem = rolagem_1
            else:
                rolagem = min(rolagem_1,rolagem_2)
                
        borda_esquerda = borda_esquerda + rolagem

    trendlines_suporte_df.to_csv('dados_csv_produzidos/trendlines_iniciais/trendlines_suporte.csv', index=True)


# ---------------------------------------------------------------------
# Construção das retas de resistência para as janelas de observação
# ---------------------------------------------------------------------

# Estabelecendo contador e ponto inicial

contador_janela = 0
borda_esquerda = tops_df['top_bottom_idx'].iloc[0]

# Inicializando DataFrames
resist_slope = [np.nan] * len(rsi_values)
colunas_resistencia = ['indice', 'indice_original_upper_pivot','valor_rsi', 'resist_slope', 'resist_intercept', 'inicio_janela', 'fim_janela']
trendlines_resistencia_df = pd.DataFrame(columns=colunas_resistencia)

for x in [lookback1, lookback2, lookback3]:
# for x in [lookback1]:
    lookback = x
    borda_esquerda = tops_df['top_bottom_idx'].iloc[0] - ordem # Começa no primeiro máximo local
    while borda_esquerda + lookback < len(rsi_values):
    
        # Fatia os tops e mínimos locais conforme a janela
        subset_tops_df = tops_df[(tops_df['top_bottom_idx'] >= borda_esquerda) & (tops_df['top_bottom_idx'] <= borda_esquerda+lookback)]

        if not subset_tops_df.empty:
            
            # Chamar a função ajustar_linha_de_tendencia para a janela sendo avaliada
            upper_pivot, upper_pivot_y, resist_slope_1, resist_slope_2 = ajustar_linha_de_tendencia(rsi_values[borda_esquerda:borda_esquerda+lookback], borda_esquerda, subset_tops_df, False)
            
            if resist_slope_1 != None:
                
                nova_linha_resistencia_1 = {
                    'indice': contador_janela,
                    'indice_original_upper_pivot': upper_pivot,
                    'valor_rsi': upper_pivot_y,
                    'resist_slope': resist_slope_1,
                    'resist_intercept':upper_pivot_y - upper_pivot * resist_slope_1,
                    'inicio_janela': borda_esquerda,
                    'fim_janela':borda_esquerda + lookback - 1
                }
                trendlines_resistencia_df = trendlines_resistencia_df._append(nova_linha_resistencia_1, ignore_index=True)

                
                contador_janela += 1

            if resist_slope_2 != None:    
                nova_linha_resistencia_2 = {
                    'indice': contador_janela,
                    'indice_original_upper_pivot': upper_pivot,
                    'valor_rsi': upper_pivot_y,
                    'resist_slope': resist_slope_2,
                    'resist_intercept':upper_pivot_y - upper_pivot * resist_slope_2,
                    'inicio_janela': borda_esquerda,
                    'fim_janela':borda_esquerda + lookback - 1
                }
                trendlines_resistencia_df = trendlines_resistencia_df._append(nova_linha_resistencia_2, ignore_index=True)

                contador_janela += 1

            # 5Rola a janela a maior distância possível até pegar o próximo máximo

        try:
            proximo_esquerda = tops_df.loc[tops_df['top_bottom_idx'].gt(borda_esquerda), 'top_bottom_idx'].min()
            rolagem_1 = proximo_esquerda - borda_esquerda
        except IndexError:
            proximo_esquerda = None  # Ou qualquer valor padrão que você queira usar

        try:
            proximo_direita = tops_df.loc[tops_df['top_bottom_idx'].gt(borda_esquerda+lookback), 'top_bottom_idx'].min()
            rolagem_2 = proximo_direita - (borda_esquerda + lookback)
        except IndexError:
            proximo_direita = None  # Ou qualquer valor padrão que você queira usar

        if proximo_esquerda == None:
            if proximo_direita == None:
                break
            else:
                rolagem = rolagem_2
        else:
            if proximo_direita == None:
                rolagem = rolagem_1
            else:
                rolagem = min(rolagem_1,rolagem_2)
        
        borda_esquerda = borda_esquerda + rolagem
    
trendlines_resistencia_df.to_csv('dados_csv_produzidos/trendlines_iniciais/trendlines_resistencia.csv', index=True)

# ---------------------- Início de código para geração de gráfico auxiliar, comentado para performance ----------------------

plt.style.use('default')
fig, (ax1, ax3) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [2, 1]})

# ----------------------------------------------------------------   
# Plotando o preço de fechamento
# ----------------------------------------------------------------   

data['Close'].plot(ax=ax1, color='blue', label=ticker_clean + ' Close Price', linewidth = 0.4)

# ----------------------------------------------------------------   
# Plotando o RSI
# ----------------------------------------------------------------   

data['RSI'].plot(ax=ax3, color='purple', label='RSI', linewidth = 0.5)

# ----------------------------------------------------------------   
# Plotando o as linhas de sobrecompra (RSI = 70) e sobrevenda (RSI = 30)
# ----------------------------------------------------------------   
ax3.axhline(70, color='gray', linestyle='--', linewidth = 0.4)  # Linha de sobrecompra
ax3.axhline(30, color='gray', linestyle='--', linewidth = 0.4)  # Linha de sobrevenda

plt.legend()
ax1.set_title(ticker_clean + " and RSI", color='black', fontsize=8)
ax1.legend(loc='upper left', fontsize=6)
ax3.legend(loc='upper left', fontsize=6)
ax3.set_ylim([0, 100])  # O RSI varia de 0 a 100

# ----------------------------------------------------------------   
# Plotando os topos e fundos no gráfico
# ----------------------------------------------------------------   

for top in tops_df.itertuples():
    # Plotar cada topo no gráfico RSI usando a data correspondente
    ax3.plot(idx[top.top_bottom_idx], data['RSI'][top.top_bottom_idx], marker='o', color='green', markersize=0.5)

for bottom in bottoms_df.itertuples():
    # Plotar cada fundo no gráfico RSI usando a data correspondente
    ax3.plot(idx[bottom.top_bottom_idx], data['RSI'][bottom.top_bottom_idx], marker='o', color='red', markersize=0.5)

# ----------------------------------------------------------------
# Ajustando o título e diminuir o tamanho da fonte
# ----------------------------------------------------------------
ax1.set_title(ticker_clean + " and RSI", color='black', fontsize=8)

# ----------------------------------------------------------------
# Reduzindo o tamanho da fonte dos valores da escala
# ----------------------------------------------------------------
ax1.tick_params(axis='both', which='major', labelsize=6)  # Tamanho da fonte dos ticks de ax1
ax3.tick_params(axis='both', which='major', labelsize=6)  # Tamanho da fonte dos ticks de ax3


# Obtendo as datas associadas aos valores do RSI
datas = data.index[len(data.index) - len(rsi_values):]

# ----------------------------------------------------------------   
# Plotando as retas de suporte do RSI
# ----------------------------------------------------------------   

for i in range(len(trendlines_suporte_df)):
    row = trendlines_suporte_df.iloc[i]

    x_start = int(row['inicio_janela'])
    y_start = row['support_slope'] * x_start + row['support_intercept']

    # Ajustar y_start se necessário
    if y_start < 0:
        x_start = max(0, min(len(datas) - 1, int(-row['support_intercept'] / row['support_slope'])))
        y_start = row['support_slope'] * x_start + row['support_intercept']

    x_end = int(row['fim_janela'])
    y_end = row['support_slope'] * x_end + row['support_intercept']

    # Ajustar y_end se necessário
    if y_end < 0:
        x_end = max(0, min(len(datas) - 1, int(-row['support_intercept'] / row['support_slope'])))
        y_end = row['support_slope'] * x_end + row['support_intercept']

    # Obter datas de início e fim
    data_start = datas[x_start]
    data_end = datas[x_end]

    # Desenhar o segmento de reta
    ax3.plot([data_start, data_end], [y_start, y_end], color='r', linewidth=0.4)


# Obtendo as datas associadas aos valores do RSI
datas = data.index[len(data.index) - len(rsi_values):]

# ----------------------------------------------------------------   
# Plotando as retas de suporte do RSI
# ----------------------------------------------------------------   

for i in range(len(trendlines_resistencia_df)):
    row = trendlines_resistencia_df.iloc[i]

    x_start = int(row['inicio_janela'])
    y_start = row['resist_slope'] * x_start + row['resist_intercept']

    # Ajustar y_start se necessário
    if y_start < 0:
        x_start = max(0, min(len(datas) - 1, int(-row['resist_intercept'] / row['resist_slope'])))
        y_start = row['resist_slope'] * x_start + row['resist_intercept']

    x_end = int(row['fim_janela'])
    y_end = row['resist_slope'] * x_end + row['resist_intercept']

    # Ajustar y_end se necessário
    if y_end < 0:
        x_end = max(0, min(len(datas) - 1, int(-row['resist_intercept'] / row['resist_slope'])))
        y_end = row['resist_slope'] * x_end + row['resist_intercept']

    # Obter datas de início e fim
    data_start = datas[x_start]
    data_end = datas[x_end]

    # Desenhar o segmento de reta
    ax3.plot([data_start, data_end], [y_start, y_end], color='green', linewidth=0.4)

# ----------------------------------------------------------------
# Salvando e plotando
# ----------------------------------------------------------------

file_name = f'graficos_gerados/primeiras_retas_{ticker_clean}.png'
fig.savefig(file_name, dpi=300)  # Salva a figura como um arquivo PNG com alta resolução

plt.show()

# ---------------------- Fim de código para geração de gráfico auxiliar, comentado para performance ----------------------

# --------------------------------------------------------------------------------------------
# Eliminando as retas de suporte e resistência que não passam por pelo menos três pontos 
# --------------------------------------------------------------------------------------------

# Mapeando as retas suporte para encontrar as que passaram por três bottoms até o fim da janela que criou a reta

mapeados_trendlines_suporte_df = mapear_retas_com_bottoms(bottoms_df, trendlines_suporte_df, distancia_maxima, num_pontos)

mapeados_trendlines_suporte_df.to_csv('dados_csv_produzidos/mapeados_trendlines_suporte.csv', index=True)

# Eliminando as retas suporte que não foram mapeadas

expurgado_trendlines_suporte_df = mapeados_trendlines_suporte_df[mapeados_trendlines_suporte_df['mapeado'] != 0]

# expurgado_trendlines_suporte_df.to_csv('dados_csv_produzidos/expurgado_trendlines_suporte.csv', index=True)


# Mapeando as retas resistência para encontrar as que passaram por três tops até o fim da janela que criou a reta

mapeados_trendlines_resistencia_df = mapear_retas_com_tops(tops_df, trendlines_resistencia_df, distancia_maxima, num_pontos)

mapeados_trendlines_resistencia_df.to_csv('dados_csv_produzidos/mapeados_trendlines_suporte.csv', index=True)

# Eliminando as retas resistência que não foram mapeadas

expurgado_trendlines_resistencia_df = mapeados_trendlines_resistencia_df[mapeados_trendlines_resistencia_df['mapeado'] != 0]

expurgado_trendlines_resistencia_df.to_csv('dados_csv_produzidos/expurgado_trendlines_resistencia.csv', index=True)

# ---------------------- Início de código para geração de gráfico auxiliar, comentado para performance ----------------------

plt.style.use('default')
fig, (ax1, ax3) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [2, 1]})

# ----------------------------------------------------------------   
# Plotando o preço de fechamento
# ----------------------------------------------------------------   

data['Close'].plot(ax=ax1, color='blue', label=ticker_clean + ' Close Price', linewidth = 0.4)

# ----------------------------------------------------------------   
# Plotando o RSI
# ----------------------------------------------------------------   

data['RSI'].plot(ax=ax3, color='purple', label='RSI', linewidth = 0.5)

# ----------------------------------------------------------------   
# Plotando o as linhas de sobrecompra (RSI = 70) e sobrevenda (RSI = 30)
# ----------------------------------------------------------------   
ax3.axhline(70, color='gray', linestyle='--', linewidth = 0.4)  # Linha de sobrecompra
ax3.axhline(30, color='gray', linestyle='--', linewidth = 0.4)  # Linha de sobrevenda

plt.legend()
ax1.set_title(ticker_clean + " and RSI", color='black', fontsize=8)
ax1.legend(loc='upper left', fontsize=6)
ax3.legend(loc='upper left', fontsize=6)
ax3.set_ylim([0, 100])  # O RSI varia de 0 a 100

# ----------------------------------------------------------------   
# Plotando os topos e fundos no gráfico
# ----------------------------------------------------------------   

for top in tops_df.itertuples():
    # Plotar cada topo no gráfico RSI usando a data correspondente
    ax3.plot(idx[top.top_bottom_idx], data['RSI'][top.top_bottom_idx], marker='o', color='green', markersize=0.3)

for bottom in bottoms_df.itertuples():
    # Plotar cada fundo no gráfico RSI usando a data correspondente
    ax3.plot(idx[bottom.top_bottom_idx], data['RSI'][bottom.top_bottom_idx], marker='o', color='red', markersize=0.3)

# ----------------------------------------------------------------
# Ajustando o título e diminuir o tamanho da fonte
# ----------------------------------------------------------------
ax1.set_title(ticker_clean + " and RSI", color='black', fontsize=8)

# ----------------------------------------------------------------
# Reduzindo o tamanho da fonte dos valores da escala
# ----------------------------------------------------------------
ax1.tick_params(axis='both', which='major', labelsize=6)  # Tamanho da fonte dos ticks de ax1
ax3.tick_params(axis='both', which='major', labelsize=6)  # Tamanho da fonte dos ticks de ax3


# Obter as datas associadas aos valores do RSI
datas = data.index[len(data.index) - len(rsi_values):]

# ----------------------------------------------------------------   
# Plotando as retas de suporte do RSI
# ----------------------------------------------------------------   

for i in range(len(expurgado_trendlines_suporte_df)):
    row = expurgado_trendlines_suporte_df.iloc[i]

    x_start = int(row['inicio_janela'])
    y_start = row['support_slope'] * x_start + row['support_intercept']

    # Ajustar y_start se necessário
    if y_start < 0:
        x_start = max(0, min(len(datas) - 1, int(-row['support_intercept'] / row['support_slope'])))
        y_start = row['support_slope'] * x_start + row['support_intercept']

    x_end = min(len(datas)-1, int(row['x_max']))
    y_end = row['support_slope'] * x_end + row['support_intercept']

    # Ajustar y_end se necessário
    if y_end < 0:
        x_end = max(0, min(len(datas) - 1, int(-row['support_intercept'] / row['support_slope'])))
        y_end = row['support_slope'] * x_end + row['support_intercept']

    # Obter datas de início e fim
    data_start = datas[x_start]
    data_end = datas[x_end]

    # Desenhar o segmento de reta
    ax3.plot([data_start, data_end], [y_start, y_end], color='r', linewidth=0.4)

# ----------------------------------------------------------------   
# Plotando as retas de rsistencia  do RSI
# ----------------------------------------------------------------   

for i in range(len(expurgado_trendlines_resistencia_df)):
    row = expurgado_trendlines_resistencia_df.iloc[i]

    x_start = int(row['inicio_janela'])
    y_start = row['resist_slope'] * x_start + row['resist_intercept']

    # Ajustar y_start se necessário
    if y_start < 0:
        x_start = max(0, min(len(datas) - 1, int(-row['resist_intercept'] / row['resist_slope'])))
        y_start = row['resist_slope'] * x_start + row['resist_intercept']

    x_end = min(len(datas)-1, int(row['fim_janela']))
    y_end = row['resist_slope'] * x_end + row['resist_intercept']

    # Ajustar y_end se necessário
    if y_end < 0:
        x_end = max(0, min(len(datas) - 1, int(-row['resist_intercept'] / row['resist_slope'])))
        y_end = row['resist_slope'] * x_end + row['resist_intercept']

    # Obter datas de início e fim
    data_start = datas[x_start]
    data_end = datas[x_end]

    # Desenhar o segmento de reta
    ax3.plot([data_start, data_end], [y_start, y_end], color='green', linewidth=0.4)

# ----------------------------------------------------------------
# Salvando e plotando
# ----------------------------------------------------------------

file_name = f'graficos_gerados/retas_com_expurgo_{ticker_clean}.png'
fig.savefig(file_name, dpi=300)  # Salva a figura como um arquivo PNG com alta resolução

plt.show()

# ---------------------- Fim de código para geração de gráfico auxiliar, comentado para performance ----------------------



# ----------------------------------------------------------------
# Eliminando as retas similares de suporte e resistência
# ----------------------------------------------------------------

# Eliminando as retasde suporte

eliminado_trendlines_suporte_df = identificar_retas_similares_suporte(expurgado_trendlines_suporte_df)

expurgado_trendlines_suporte_df['support_slope_rounded'] = expurgado_trendlines_suporte_df['support_slope'].round(3)

eliminado_trendlines_suporte_df = expurgado_trendlines_suporte_df.groupby(['indice_original_lower_pivot', 'support_slope_rounded']).agg({
    'inicio_janela': 'min',
    'fim_janela': 'min',
    'support_intercept': 'first',
    'num_zeros': 'min'}).reset_index()
eliminado_trendlines_suporte_df.to_csv('dados_csv_produzidos/eliminado_trendlines_suporte.csv', index=True)

# Eliminando as retas de resistência

eliminado_trendlines_resistencia_df = identificar_retas_similares_resistencia(expurgado_trendlines_resistencia_df)


eliminado_trendlines_resistencia_df.to_csv('dados_csv_produzidos/eliminado_trendlines_resistencia.csv', index=True)

expurgado_trendlines_resistencia_df['resist_slope_rounded'] = expurgado_trendlines_resistencia_df['resist_slope'].round(3)
eliminado_trendlines_resistencia_df = expurgado_trendlines_resistencia_df.groupby(['indice_original_upper_pivot', 'resist_slope_rounded']).agg({
    'inicio_janela': 'min',
    'fim_janela': 'min',
    'resist_intercept': 'first',
    'num_zeros': 'min'}).reset_index()
eliminado_trendlines_resistencia_df.to_csv('dados_csv_produzidos/eliminado_trendlines_resistencia.csv', index=True)



# ------------------------------------------------------------------------
# Encontrando breaks para baixo nas retas suporte
# ------------------------------------------------------------------------

# Criando DataFrame para armazenar os breaks para baixo

breaks_down_df = pd.DataFrame(columns=['ponto', 'evento', 'reta' ,'x_rompimento', 'y_rompimento', 'inicio_janela', 'fim_janela'])

# Percorrendo o gráfico para encontrar os breaks

for i in range(pontos_para_tras, len(rsi_df)):

    # Criando a lista de pontos
    pontos = [(i - pontos_para_tras, rsi_df.iloc[i - pontos_para_tras]['RSI']), 
          (i, rsi_df.iloc[i]['RSI'])]
    
    # Percorrendo as linhas de tendência de suporte
    for idx, linha in eliminado_trendlines_suporte_df.iterrows():
        # Extraindo os valores da reta e a fim_janela para armazenar
        fim_janela = linha['fim_janela']
        inicio_janela = linha['inicio_janela']

        # Verificando se i é maior do que fim_janela + ordem
        if i > fim_janela + ordem*0:
            slope = linha['support_slope_rounded']
            intercept = linha['support_intercept']
            # Verificando se o cruzamento ocorreu e salvando o cruzamento
            cruzou, x_rompimento, y_rompimento = checar_cruzou_para_baixo( pontos, slope, intercept, break_min, rsi_df)
            if cruzou:
                    breaks_down_df = breaks_down_df._append({'ponto': int(i),
                                                    'evento': 2,
                                                    'reta': idx,
                                                    'x_rompimento': x_rompimento,
                                                    'y_rompimento': y_rompimento,
                                                    'inicio_janela':inicio_janela,
                                                    'fim_janela': fim_janela}, ignore_index=True)
                    
breaks_down_df.to_csv('dados_csv_produzidos/breaks_down_sem_eliminacao.csv', index=True)

primeiros_breaks_down_df = breaks_down_df.loc[breaks_down_df.groupby('reta')['x_rompimento'].idxmin()]
primeiros_breaks_down_df = primeiros_breaks_down_df.loc[primeiros_breaks_down_df.groupby('x_rompimento')['fim_janela'].idxmin()]

primeiros_breaks_down_df.to_csv('dados_csv_produzidos/breaks_down.csv', index=True)

# ------------------------------------------------------------------------
# Encontrando breaks para cima nas retas de resistencia
# ------------------------------------------------------------------------

# Criando DataFrame para armazenar os breaks

breaks_up_df = pd.DataFrame(columns=['ponto', 'evento', 'reta' ,'x_rompimento', 'y_rompimento', 'inicio_janela', 'fim_janela'])

for i in range(pontos_para_tras, len(rsi_df)):
    # Criando a lista de pontos
    pontos = [(i - pontos_para_tras, rsi_df.iloc[i - pontos_para_tras]['RSI']), 
          (i, rsi_df.iloc[i]['RSI'])]
    
    # Percorrendo as linhas de tendência de resistência
    for idx, linha in eliminado_trendlines_resistencia_df.iterrows():
        # Extraindo os valores da reta e a fim_janela
        fim_janela = linha['fim_janela']
        inicio_janela = linha['inicio_janela']

        # Verificando se i é maior do que fim_janela + ordem
        if i > fim_janela + ordem:
            slope = linha['resist_slope_rounded']
            intercept = linha['resist_intercept']
            # Verificando se o cruzamento ocorreu e salvando o cruzamento
            cruzou, x_rompimento, y_rompimento = checar_cruzou_para_cima( pontos, slope, intercept, break_min, rsi_df)
            if cruzou:
                breaks_up_df = breaks_up_df._append({'ponto': int(i),
                                                'evento': 1,
                                                'reta': idx,
                                                'x_rompimento': x_rompimento,
                                                'y_rompimento': y_rompimento,
                                                'inicio_janela':inicio_janela,
                                                'fim_janela': fim_janela}, ignore_index=True)


breaks_up_df.to_csv('dados_csv_produzidos/breaks_up_sem_eliminacao.csv', index=True)

primeiros_breaks_up_df = breaks_up_df.loc[breaks_up_df.groupby('reta')['x_rompimento'].idxmin()]
primeiros_breaks_up_df = primeiros_breaks_up_df.loc[primeiros_breaks_up_df.groupby('x_rompimento')['fim_janela'].idxmin()]

primeiros_breaks_up_df.to_csv('dados_csv_produzidos/breaks_up.csv', index=True)

# Concatenando os dois DataFrames com os breaks para criar uma base única

breaks_df = pd.concat([primeiros_breaks_down_df, primeiros_breaks_up_df])

# Ordenando o DataFrame resultante pela coluna 'ponto'
breaks_df = breaks_df.sort_values(by='ponto')

# Resetando o índice se necessário
breaks_df = breaks_df.reset_index(drop=True)

# Salvando para inspeção
breaks_df.to_csv('dados_csv_produzidos/breaks.csv', index=True)

# ---------------------- Início do código para geração de gráfico auxiliar, comentado para performance ----------------------

plt.style.use('default')
fig, (ax1, ax3) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [2, 1]})

# ----------------------------------------------------------------   
# Plotando o preço de fechamento
# ----------------------------------------------------------------   

data['Close'].plot(ax=ax1, color='blue', label=ticker_clean + ' Close Price', linewidth = 0.3)

# ----------------------------------------------------------------   
# Plotando o RSI
# ----------------------------------------------------------------   

data['RSI'].plot(ax=ax3, color='purple', label='RSI', linewidth = 0.5)

# ----------------------------------------------------------------   
# Plotando o as linhas de sobrecompra (RSI = 70) e sobrevenda (RSI = 30)
# ----------------------------------------------------------------   
ax3.axhline(70, color='gray', linestyle='--', linewidth = 0.4)  # Linha de sobrecompra
ax3.axhline(30, color='gray', linestyle='--', linewidth = 0.4)  # Linha de sobrevenda

plt.legend()
ax1.set_title(ticker_clean + " and RSI", color='black', fontsize=8)
ax1.legend(loc='upper left', fontsize=6)
ax3.legend(loc='upper left', fontsize=6)
ax3.set_ylim([0, 100])  # O RSI varia de 0 a 100

# ----------------------------------------------------------------   
# Plotar os topos e fundos no gráfico
# ----------------------------------------------------------------   

idx = data.index

for top in tops_df.itertuples():
    # Plotar cada topo no gráfico RSI usando a data correspondente
    ax3.plot(idx[top.top_bottom_idx], data['RSI'][top.top_bottom_idx], marker='o', color='green', markersize=0.3)

for bottom in bottoms_df.itertuples():
    # Plotar cada fundo no gráfico RSI usando a data correspondente
    ax3.plot(idx[bottom.top_bottom_idx], data['RSI'][bottom.top_bottom_idx], marker='o', color='red', markersize=0.3)
    
# Obter as datas associadas aos valores do RSI
datas = data.index[len(data.index) - len(rsi_values):]

# ----------------------------------------------------------------   
# Plotando as retas de suporte do RSI
# ----------------------------------------------------------------   

for i in range(len(expurgado_trendlines_suporte_df)):
    row = expurgado_trendlines_suporte_df.iloc[i]

    x_start = int(row['inicio_janela'])
    y_start = row['support_slope'] * x_start + row['support_intercept']

    # Ajustar y_start se necessário
    if y_start < 0:
        x_start = max(0, min(len(datas) - 1, int(-row['support_intercept'] / row['support_slope'])))
        y_start = row['support_slope'] * x_start + row['support_intercept']

    x_end = min(len(datas)-1, int(row['x_max']))
    y_end = row['support_slope'] * x_end + row['support_intercept']

    # Ajustar y_end se necessário
    if y_end < 0:
        x_end = max(0, min(len(datas) - 1, int(-row['support_intercept'] / row['support_slope'])))
        y_end = row['support_slope'] * x_end + row['support_intercept']

    # Obter datas de início e fim
    data_start = datas[x_start]
    data_end = datas[x_end]

    # Desenhar o segmento de reta
    ax3.plot([data_start, data_end], [y_start, y_end], color='r', linewidth=0.2)

# ----------------------------------------------------------------   
# Plotando as retas de resistência do RSI
# ----------------------------------------------------------------

for i in range(len(expurgado_trendlines_resistencia_df)):
    row = expurgado_trendlines_resistencia_df.iloc[i]

    x_start = int(row['inicio_janela'])
    y_start = row['resist_slope'] * x_start + row['resist_intercept']

    # Ajustar y_start se necessário
    if y_start < 0:
        x_start = max(0, min(len(datas) - 1, int(-row['resist_intercept'] / row['resist_slope'])))
        y_start = row['resist_slope'] * x_start + row['resist_intercept']

    x_end = min(len(datas)-1, int(row['fim_janela']))
    y_end = row['resist_slope'] * x_end + row['resist_intercept']

    # Ajustar y_end se necessário
    if y_end < 0:
        x_end = max(0, min(len(datas) - 1, int(-row['resist_intercept'] / row['resist_slope'])))
        y_end = row['resist_slope'] * x_end + row['resist_intercept']

    # Obter datas de início e fim
    data_start = datas[x_start]
    data_end = datas[x_end]

    # Desenhar o segmento de reta
    ax3.plot([data_start, data_end], [y_start, y_end], color='green', linewidth=0.2)

# ----------------------------------------------------------------
# Desenhando as linhas indicativas de rompimento
# ----------------------------------------------------------------
for _, row in primeiros_breaks_down_df.iterrows():
    x_rompimento = row['x_rompimento']

    # Obter a data correspondente ao índice x_rompimento
    data_x_rompimento = data.index[int(x_rompimento)]

    # Adicionar linha vertical vermelha para os rompimentos das linhas de resistência
    ax1.axvline(x=data_x_rompimento, color='red', linestyle='--', linewidth=0.3)
    ax3.axvline(x=data_x_rompimento, color='red', linestyle='--', linewidth=0.3)

for _, row in primeiros_breaks_up_df.iterrows():
    x_rompimento = row['x_rompimento']

    # Obter a data correspondente ao índice x_rompimento
    data_x_rompimento = data.index[int(x_rompimento)]

    # Adicionar linha vertical azul para os rompimentos das linhas de suporte
    ax1.axvline(x=data_x_rompimento, color='blue', linestyle='--', linewidth=0.3)
    ax3.axvline(x=data_x_rompimento, color='blue', linestyle='--', linewidth=0.3)

# ----------------------------------------------------------------
# Ajustando o título e diminuir o tamanho da fonte
# ----------------------------------------------------------------
ax1.set_title(ticker_clean + " and RSI", color='black', fontsize=8)

# ----------------------------------------------------------------
# Reduzindo o tamanho da fonte dos valores da escala
# ----------------------------------------------------------------
ax1.tick_params(axis='both', which='major', labelsize=6)  # Tamanho da fonte dos ticks de ax1
ax3.tick_params(axis='both', which='major', labelsize=6)  # Tamanho da fonte dos ticks de ax3

# ----------------------------------------------------------------
# Salvando e plotando
# ----------------------------------------------------------------

file_name = f'graficos_gerados/rompimentos_{ticker_clean}.png'
fig.savefig(file_name, dpi=300)  # Salva a figura como um arquivo PNG com alta resolução
plt.show()

# ---------------------- Fim do código para geração de gráfico auxiliar, comentado para performance ----------------------



# ------------------------------------------------------------------------------------
# Criando a classe de estratégia a ser usada pela biblioteca Backtesting do Python
# ------------------------------------------------------------------------------------

class EstrategiaAdaptada(Strategy):
    # Adicione os parâmetros como variáveis de classe
    pt = pt_val  # Profit target padrão, será alterado por BT.run()
    sl = sl_val  # Stop loss padrão, será alterado por BT.run()

    def init(self):
        # Inicializando as variáveis de estado
        self.pos_ant = 0  # 0 = sem posição, -1 = vendido, 1 = comprado
        self.ini_posicao_ant = None  # Índice inicial da posição anterior
        self.valor_posicao_ant = None  # Valor inicial da posição anterior

    def next(self):
        # Preço atual e índice
        valor = self.data.Close[-1]  # Preço de fechamento da barra sendo inspecionada
        ind = len(self.data) - 1  # Índice atual no DataFrame
        
        # Evento da estratégia
        evento = self.data.df.loc[self.data.df.index[ind], 'Evento']

        # Lógica de abertura de uma posição a partir de uma posição neutra
        if self.pos_ant == 0:  # Sem posição
            if evento == 1:  # Sinal de compra
                self.buy()  # Abrir posição de compra
                self.pos_ant = 1  # Muda variável de estado para comprado
                with open("saida.txt", "a") as arquivo:
                    print("Mudei de zerado para comprado em ", ind, file=arquivo)
                    print("Valor da posição atual", valor, file=arquivo)
                    print("Profit taking considerado ", self.pt, file=arquivo)
                    print("Stop loss considerado ", self.sl, file=arquivo)               
                self.ini_posicao_ant = ind  # Marca a barra em que a posição foi comprada
                self.valor_posicao_ant = valor  # Assume que posição adquirida foi o preço de fechamento da barra sendo inspecionada
            elif evento == 2:  # Sinal de venda
                self.sell()  # Abrir posição de venda
                self.pos_ant = -1  # Muda variável de estado para vendido
                with open("saida.txt", "a") as arquivo:
                    print("Mudei de zerado para vendido em ", ind, file=arquivo)
                    print("Valor da posição atual", valor, file=arquivo)
                self.ini_posicao_ant = ind  # Marca a barra em que a posição foi vendida
                self.valor_posicao_ant = valor  # Assume que posição vendida foi o preço de fechamento da barra sendo inspecionada

        # Lógica de decisão caso a posição anterior fosse vendida
        elif self.pos_ant == -1:  # Posição vendida
            with open("saida.txt", "a") as arquivo:
                print("trade sendo considerado ", ind, file=arquivo)
                print("teste 1 > self.pt ou < -self.sl", -(valor / self.valor_posicao_ant - 1), file=arquivo)
                print("teste 2 ", evento == 1, file=arquivo)
            if -(valor / self.valor_posicao_ant-1) > self.pt or \
               -(valor / self.valor_posicao_ant - 1) < -self.sl or evento == 1:  # Testa stop loss ou profit taking ou sinal de compra
                with open("saida.txt", "a") as arquivo:
                    print("Fechei a posição vendida em ", ind, file=arquivo)
                    print("Valor da posição anterior", self.valor_posicao_ant, file=arquivo)
                    print("Valor da posição atual", valor, file=arquivo)
                if -(valor / self.valor_posicao_ant - 1) > self.pt:
                    with open("saida.txt", "a") as arquivo:
                        print("Valor da posição anterior", self.valor_posicao_ant, file=arquivo)
                        print("Valor da posição atual", valor, file=arquivo)
                        print("Profit taking em", ind, file=arquivo)
                        print("Profit taking a um ganho de ", (valor / self.valor_posicao_ant - 1), file=arquivo)
                        print("maior do que um pt de ", self.pt, file=arquivo)
                if -(valor / self.valor_posicao_ant - 1) < -self.sl:
                    with open("saida.txt", "a") as arquivo:
                        print("Stop loss em ", ind, file=arquivo)
                        print("Uma loss de ", (valor / self.valor_posicao_ant - 1), file=arquivo)
                        print("mais negativo do que um sl de ", -self.sl, file=arquivo)
                if evento == 1:
                    with open("saida.txt", "a") as arquivo:
                        print("Fechei a posição por um sinal em ", ind, file=arquivo)
                self.position.close()  # Fecha a posição
                self.pos_ant = 0  # Muda variável de estado para neutro

        # Lógica de decisão caso a posição anterior fosse comprada
        elif self.pos_ant == 1:  # Posição comprada
            with open("saida.txt", "a") as arquivo:
                print("trade sendoconsiderado ", ind, file=arquivo)
                print("teste 1", (valor / self.valor_posicao_ant-1), file=arquivo)
                print("teste 2 ", evento == 2, file=arquivo)
            if (valor - self.valor_posicao_ant) / self.valor_posicao_ant > self.pt or \
               (valor - self.valor_posicao_ant) / self.valor_posicao_ant < -self.sl or evento == 2:
                with open("saida.txt", "a") as arquivo:
                    print("Fechei a posição comprada em ", ind, file=arquivo)
                    print("Valor da posição anterior", self.valor_posicao_ant, file=arquivo)
                    print("Valor da posição atual", valor, file=arquivo)
                if (valor / self.valor_posicao_ant - 1) > self.pt:
                    with open("saida.txt", "a") as arquivo:
                        print("Profit taking em", ind, file=arquivo)
                        print("Profit taking com um ganho de ", (valor / self.valor_posicao_ant - 1), file=arquivo)
                        print("maior do que um pt de ", self.pt, file=arquivo)
                if (valor / self.valor_posicao_ant - 1) < -self.sl:
                    with open("saida.txt", "a") as arquivo:
                        print("Stop loss em ", ind, file=arquivo)
                        print("Uma loss de ", (valor / self.valor_posicao_ant - 1), file=arquivo)
                        print("mais negativo do que um sl de ", -self.sl, file=arquivo)
                if evento == 2 > self.pt:
                    with open("saida.txt", "a") as arquivo:
                        print("Fechei a posição por um sinal em ", ind, file=arquivo)
                self.position.close()  # Fecha a posição
                self.pos_ant = 0  # Muda variável de estado para neutro


# ------------------------------------------------------------------------------------
# Executanto o Backtesting do Python
# ------------------------------------------------------------------------------------

# Preparação do DataFrame a ser usado no Backtesting

# Inicializar a coluna 'Evento' no DataFrame Data com zeros

data['Evento'] = 0

# Salvar o DataFrame atualizado em um arquivo CSV para inspeção (opcional)
data.to_csv('Data_sem_Evento.csv', index=True)
breaks_df.to_csv('Break pre cruzamento.csv', index=True)

# Colocando os Eventos de break no DataFrame

for _, row in breaks_df.iterrows():
    x_rompimento = int(row['x_rompimento'])  # Certifique-se de que ponto é um inteiro
    evento = row['evento']
    if 0 <= x_rompimento-1 < len(data):  # Verifique se está dentro dos limites
        data.iloc[x_rompimento-1, data.columns.get_loc('Evento')] = evento

# Salvar o DataFrame atualizado em um arquivo CSV (opcional)


# Criar o DataFrame para backtesting com índice datetime
dados_backtesting = pd.DataFrame({
    'Open': data['Open'],    # Preço de abertura
    'High': data['High'],    # Preço mais alto
    'Low': data['Low'],      # Preço mais baixo
    'Close': data['Close'],  # Preço de fechamento
    'Volume': data['Volume'], # Volume negociado
    'Evento': data['Evento']  # Sinais de compra e venda
}, index=data.index)  # Define o índice como a coluna 'Date'

dados_backtesting.to_csv('Dados_para_backtesting_1.csv', index=True)

# Executar o backtesting
bt = Backtest(dados_backtesting, EstrategiaAdaptada, cash=10_000_000, commission=.002)
resultados =  bt.run(pt=pt_val, sl=sl_val)

# Exibir os resultados
print(resultados)

bt.plot(open_browser=True)