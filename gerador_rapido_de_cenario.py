# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter

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

def simulacao(janela_rsi, 
              ordem, 
              lookback1, 
              distancia_maxima, 
              num_pontos, 
              break_min, 
              pontos_para_tras, 
              data, aplicar_log, 
              ticker_clean, 
              imprime_grafico, 
              salva_dados):



    # ---------------------------------------------------------------------
    # Calculando o RSI
    # ---------------------------------------------------------------------

    # Preparando base para o RSI, dependendo se vai usar log ou não

    ordem_str =  str(int(ordem))
    lookback_str = str(int(lookback1))
    break_min_str = str(int(break_min))

    if aplicar_log:
        colunas_numericas_para_log = ['Open', 'High', 'Low', 'Close', 'Adj Close']
        data_log = np.log(data[colunas_numericas_para_log]) # Aplicando logaritmo nas colunas numéricas exceto volume
        data['RSI'] = compute_rsi(data_log['Close'],janela_rsi)
        rsi_values = compute_rsi(data_log['Close'], janela_rsi)
    else:
        data['RSI'] = compute_rsi(data['Close'],janela_rsi)
        rsi_values = compute_rsi(data['Close'], janela_rsi)

    rsi_df = pd.DataFrame(data['RSI'])


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

    bottoms_df = pd.DataFrame(bottoms, columns=['top_bottom_idx', 'top_bottom_value'])
    bottoms_df = bottoms_df.dropna(subset=['top_bottom_value'])

    idx = data.index

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


    # --------------------------------------------------------------------------------------------
    # Eliminando as retas de suporte e resistência que não passam por pelo menos três pontos 
    # --------------------------------------------------------------------------------------------

    # Mapeando as retas suporte para encontrar por quantos pontos elas passaram. Marcam mapeado = 1 se maior ou igual a pontos_min
    # e marca mapeado = 0 se menor que pontos_min

    mapeados_trendlines_suporte_df = mapear_retas_com_bottoms(bottoms_df, trendlines_suporte_df, distancia_maxima, num_pontos)

    # Eliminando as retas suporte que não foram mapeadas, exclui mapeado = 0

    expurgado_trendlines_suporte_df = mapeados_trendlines_suporte_df[mapeados_trendlines_suporte_df['mapeado'] != 0]

    # Mapeando as retas resistencia para encontrar por quantos pontos elas passaram. Marcam mapeado = 1 se maior ou igual a pontos_min
    # e marca mapeado = 0 se menor que pontos_min

    mapeados_trendlines_resistencia_df = mapear_retas_com_tops(tops_df, trendlines_resistencia_df, distancia_maxima, num_pontos)

    # Eliminando as retas resistência que não foram mapeadas

    expurgado_trendlines_resistencia_df = mapeados_trendlines_resistencia_df[mapeados_trendlines_resistencia_df['mapeado'] != 0]


    # ----------------------------------------------------------------
    # Eliminando as retas similares de suporte e resistência
    # ----------------------------------------------------------------

    # Eliminando as retasde suporte

    eliminado_trendlines_suporte_df = identificar_retas_similares_suporte(expurgado_trendlines_suporte_df)

    eliminado_trendlines_suporte_df['support_slope_rounded'] = eliminado_trendlines_suporte_df['support_slope'].round(5)

    

    # Eliminando as retas de resistência

    eliminado_trendlines_resistencia_df = identificar_retas_similares_resistencia(expurgado_trendlines_resistencia_df)

    eliminado_trendlines_resistencia_df['resist_slope_rounded'] = eliminado_trendlines_resistencia_df['resist_slope'].round(5)

    # eliminado_trendlines_resistencia_df = eliminado_trendlines_resistencia_df.groupby(['indice_original_upper_pivot', 'resist_slope_rounded']).agg({
    #     'inicio_janela': 'min',
    #     'fim_janela': 'min',
    #     'x_min': 'min',
    #     'x_max' : 'max',
    #     'resist_intercept': 'first',
    #     'num_zeros': 'min'}).reset_index()
    
    # ------------------------------------------------------------------------
    # Encontrando breaks para baixo nas retas suporte
    # ------------------------------------------------------------------------

    # Criando DataFrame para armazenar os breaks para baixo

    breaks_down_df = pd.DataFrame(columns=['ponto', 'evento', 'reta' ,'x_rompimento', 'y_rompimento', 'inicio_janela', 'fim_janela'])

    # Percorrendo o gráfico para encontrar os breaks
    # Passea por todos os valores de x de ppt até o fim

    for i in range(pontos_para_tras, len(rsi_df)):

        # Examino o ponto atual até o ppt pontos anteriores
        pontos = [(i - pontos_para_tras, rsi_df.iloc[i - pontos_para_tras]['RSI']), 
            (i, rsi_df.iloc[i]['RSI'])]
        
        # Percorrendo todas as linhas de tendência de suporte não eliminadas
        for idx, linha in eliminado_trendlines_suporte_df.iterrows():
            # Extraindo os valores da reta e a fim_janela para armazenar
            inicio_janela = linha['inicio_janela']
            fim_janela = inicio_janela + lookback1

            # Verifica se i é maior do que fim_janela + ordem
            # Só posso testar retas que já tenham sido criadas no momento i-1, caso eu tivesse percorrido todos os pontos anteriores
            # Para isso na consolidação das retas em um mesmo pivot point, tenho que armazenar a menor fim_janela
            # ou tenho que pega a menor inicio_janela e somar o lookback1

            if i > fim_janela + ordem:
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
                            

    primeiros_breaks_down_df = breaks_down_df.loc[breaks_down_df.groupby('reta')['x_rompimento'].idxmin()]
    primeiros_breaks_down_df = primeiros_breaks_down_df.loc[primeiros_breaks_down_df.groupby('x_rompimento')['fim_janela'].idxmin()]


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
            inicio_janela = linha['inicio_janela']
            fim_janela = inicio_janela + lookback1

            # Verifica se i é maior do que fim_janela + ordem
            # Só posso testar retas que já tenham sido criadas no momento i-1, caso eu tivesse percorrido todos os pontos anteriores
            # Para isso na consolidação das retas em um mesmo pivot point, tenho que armazenar a menor fim_janela
            # ou tenho que pega a menor inicio_janela e somar o lookback1            

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

    primeiros_breaks_up_df = breaks_up_df.loc[breaks_up_df.groupby('reta')['x_rompimento'].idxmin()]
    primeiros_breaks_up_df = primeiros_breaks_up_df.loc[primeiros_breaks_up_df.groupby('x_rompimento')['fim_janela'].idxmin()]


    # Concatenando os dois DataFrames com os breaks para criar uma base única

    breaks_df = pd.concat([primeiros_breaks_down_df, primeiros_breaks_up_df])

    # Ordenando o DataFrame resultante pela coluna 'ponto'
    breaks_df = breaks_df.sort_values(by='ponto')

    # Resetando o índice se necessário
    breaks_df = breaks_df.reset_index(drop=True)

    # # Salvando para inspeção

    return breaks_df

