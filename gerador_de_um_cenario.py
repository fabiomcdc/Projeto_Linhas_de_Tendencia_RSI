# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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



#---------------------------------------------------------------------

def simulacao(janela_rsi, ordem, lookback1, distancia_maxima, num_pontos, break_min, pontos_para_tras, data, aplicar_log, ticker_clean, imprime_grafico):



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


    # file_name = f'dados_csv_produzidos/dados_rsi/rsi_values_{ticker_clean}.csv'
    # rsi_df.to_csv(file_name, index=True)



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
    # file_name = f'dados_csv_produzidos/minimos_maximos_locais/maximos_locais_{ticker_clean}.csv'
    # tops_df.to_csv(file_name, index=True)

    bottoms_df = pd.DataFrame(bottoms, columns=['top_bottom_idx', 'top_bottom_value'])
    bottoms_df = bottoms_df.dropna(subset=['top_bottom_value'])
    # file_name = f'dados_csv_produzidos/minimos_maximos_locais/minimos_locais_{ticker_clean}.csv'
    # bottoms_df.to_csv(file_name, index=True)

    idx = data.index



    # ---------------------- Início de código para geração de gráfico auxiliar, comentado para performance ----------------------

    if imprime_grafico:
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

        file_name = f'simulações_aplicadas_a_ativos/{ticker_clean}/{ticker_clean}_cenário_escolhido_mínimos_máximos.png'
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

    # for x in [lookback1, lookback2, lookback3, lookback4]:
    for x in [lookback1]:
        lookback = x
        borda_esquerda = bottoms_df['top_bottom_idx'].iloc[0]-ordem
        while borda_esquerda + lookback < len(rsi_values):
            subset_tops_df = bottoms_df[(bottoms_df['top_bottom_idx'] >= borda_esquerda) & (bottoms_df['top_bottom_idx'] <= borda_esquerda+lookback-ordem)]
            
            # Chamar a função ajustar_linha_de_tendencia para a janela sendo avaliada
            if not subset_tops_df.empty:
                
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

        # trendlines_suporte_df.to_csv('dados_csv_produzidos/trendlines_iniciais/trendlines_suporte.csv', index=True)


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

    # for x in [lookback1, lookback2, lookback3, lookback4]:
    for x in [lookback1]:
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

            # Rola a janela a maior distância possível até pegar o próximo máximo

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
        
    # trendlines_resistencia_df.to_csv('dados_csv_produzidos/trendlines_iniciais/trendlines_resistencia.csv', index=True)



    # ---------------------- Início de código para geração de gráfico auxiliar, comentado para performance ----------------------

    if imprime_grafico:
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

        file_name = f'simulações_aplicadas_a_ativos/{ticker_clean}/{ticker_clean}_cenário_escolhido_primeiras_retas.png'
        fig.savefig(file_name, dpi=300)  # Salva a figura como um arquivo PNG com alta resolução

        plt.show()

    # ---------------------- Fim de código para geração de gráfico auxiliar, comentado para performance ----------------------



    # --------------------------------------------------------------------------------------------
    # Eliminando as retas de suporte e resistência que não passam por pelo menos três pontos 
    # --------------------------------------------------------------------------------------------

    # Mapeando as retas suporte para encontrar as que passaram por três bottoms até o fim da janela que criou a reta

    mapeados_trendlines_suporte_df = mapear_retas_com_bottoms(bottoms_df, trendlines_suporte_df, distancia_maxima, num_pontos)

    # mapeados_trendlines_suporte_df.to_csv('dados_csv_produzidos/mapeados_trendlines_suporte.csv', index=True)

    # Eliminando as retas suporte que não foram mapeadas

    expurgado_trendlines_suporte_df = mapeados_trendlines_suporte_df[mapeados_trendlines_suporte_df['mapeado'] != 0]

    # expurgado_trendlines_suporte_df.to_csv('dados_csv_produzidos/expurgado_trendlines_suporte.csv', index=True)


    # Mapeando as retas resistência para encontrar as que passaram por três tops até o fim da janela que criou a reta

    mapeados_trendlines_resistencia_df = mapear_retas_com_tops(tops_df, trendlines_resistencia_df, distancia_maxima, num_pontos)

    # mapeados_trendlines_resistencia_df.to_csv('dados_csv_produzidos/mapeados_trendlines_suporte.csv', index=True)

    # Eliminando as retas resistência que não foram mapeadas

    expurgado_trendlines_resistencia_df = mapeados_trendlines_resistencia_df[mapeados_trendlines_resistencia_df['mapeado'] != 0]

    # expurgado_trendlines_resistencia_df.to_csv('dados_csv_produzidos/expurgado_trendlines_resistencia.csv', index=True)



    # ---------------------- Início de código para geração de gráfico auxiliar, comentado para performance ----------------------


    if imprime_grafico:

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

        file_name = f'simulações_aplicadas_a_ativos/{ticker_clean}/{ticker_clean}_cenário_escolhido_retas_com_expurgo.png'
        fig.savefig(file_name, dpi=300)  # Salva a figura como um arquivo PNG com alta resolução

        plt.show()

    # ---------------------- Fim de código para geração de gráfico auxiliar, comentado para performance ----------------------



    # ----------------------------------------------------------------
    # Eliminando as retas similares de suporte e resistência
    # ----------------------------------------------------------------

    # Eliminando as retasde suporte

    eliminado_trendlines_suporte_df =   identificar_retas_similares_suporte(expurgado_trendlines_suporte_df)

    expurgado_trendlines_suporte_df['support_slope_rounded'] = expurgado_trendlines_suporte_df['support_slope'].round(3)

    eliminado_trendlines_suporte_df = expurgado_trendlines_suporte_df.groupby(['indice_original_lower_pivot', 'support_slope_rounded']).agg({
        'inicio_janela': 'min',
        'fim_janela': 'min',
        'support_intercept': 'first',
        'num_zeros': 'min'}).reset_index()
    # eliminado_trendlines_suporte_df.to_csv('dados_csv_produzidos/eliminado_trendlines_suporte.csv', index=True)

    # Eliminando as retas de resistência

    eliminado_trendlines_resistencia_df = identificar_retas_similares_resistencia(expurgado_trendlines_resistencia_df)


    # eliminado_trendlines_resistencia_df.to_csv('dados_csv_produzidos/eliminado_trendlines_resistencia.csv', index=True)

    expurgado_trendlines_resistencia_df['resist_slope_rounded'] = expurgado_trendlines_resistencia_df['resist_slope'].round(3)
    eliminado_trendlines_resistencia_df = expurgado_trendlines_resistencia_df.groupby(['indice_original_upper_pivot', 'resist_slope_rounded']).agg({
        'inicio_janela': 'min',
        'fim_janela': 'min',
        'resist_intercept': 'first',
        'num_zeros': 'min'}).reset_index()
    # eliminado_trendlines_resistencia_df.to_csv('dados_csv_produzidos/eliminado_trendlines_resistencia.csv', index=True)



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
                        
    # breaks_down_df.to_csv('dados_csv_produzidos/breaks_down_sem_eliminacao.csv', index=True)

    primeiros_breaks_down_df = breaks_down_df.loc[breaks_down_df.groupby('reta')['x_rompimento'].idxmin()]
    primeiros_breaks_down_df = primeiros_breaks_down_df.loc[primeiros_breaks_down_df.groupby('x_rompimento')['fim_janela'].idxmin()]

    # primeiros_breaks_down_df.to_csv('dados_csv_produzidos/breaks_down.csv', index=True)

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


    # breaks_up_df.to_csv('dados_csv_produzidos/breaks_up_sem_eliminacao.csv', index=True)

    primeiros_breaks_up_df = breaks_up_df.loc[breaks_up_df.groupby('reta')['x_rompimento'].idxmin()]
    primeiros_breaks_up_df = primeiros_breaks_up_df.loc[primeiros_breaks_up_df.groupby('x_rompimento')['fim_janela'].idxmin()]

    # primeiros_breaks_up_df.to_csv('dados_csv_produzidos/breaks_up.csv', index=True)

    # Concatenando os dois DataFrames com os breaks para criar uma base única

    breaks_df = pd.concat([primeiros_breaks_down_df, primeiros_breaks_up_df])

    # Ordenando o DataFrame resultante pela coluna 'ponto'
    breaks_df = breaks_df.sort_values(by='ponto')

    # Resetando o índice se necessário
    breaks_df = breaks_df.reset_index(drop=True)

    # # Salvando para inspeção
    # breaks_df.to_csv('dados_csv_produzidos/breaks.csv', index=True)

    # ---------------------- Início do código para geração de gráfico auxiliar, comentado para performance ----------------------

    if imprime_grafico:
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

        file_name = f'simulações_aplicadas_a_ativos/{ticker_clean}/{ticker_clean}_cenário_escolhido_rompimentos.png'
        fig.savefig(file_name, dpi=300)  # Salva a figura como um arquivo PNG com alta resolução
        plt.show()

    # ---------------------- Fim do código para geração de gráfico auxiliar, comentado para performance ----------------------

    return breaks_df

