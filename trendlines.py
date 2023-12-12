import pandas as pd
import numpy as np

def check_trend_line(support: bool, pivot: int, slope: float, y: np.array):
    # compute sum of differences between line and prices, 
    # return negative val if invalid 
    
    # Find the intercept of the line going through pivot point with given slope
    intercept = -slope * pivot + y.iloc[pivot]
    line_vals = slope * np.arange(len(y)) + intercept
     
    diffs = line_vals - y
    
    # Check to see if the line is valid, return -1 if it is not valid.
    if support and diffs.max() > 1e-5:
        return -1.0
    elif not support and diffs.min() < -1e-5:
        return -1.0

    # Squared sum of diffs between data and line 
    err = (diffs ** 2.0).sum()
    return err


def optimize_slope(support: bool, pivot:int , init_slope: float, y: np.array):
    
    # Amount to change slope by. Multiplyed by opt_step
    slope_unit = (y.max() - y.min()) / len(y) 
    
    # Optmization variables
    opt_step = 1.0
    min_step = 0.0001
    curr_step = opt_step # current step
    
    # Initiate at the slope of the line of best fit
    best_slope = init_slope
    best_err = check_trend_line(support, pivot, init_slope, y)
    assert(best_err >= 0.0) # Shouldn't ever fail with initial slope

    get_derivative = True
    derivative = None
    while curr_step > min_step:

        if get_derivative:
            # Numerical differentiation, increase slope by very small amount
            # to see if error increases/decreases. 
            # Gives us the direction to change slope.
            slope_change = best_slope + slope_unit * min_step
            test_err = check_trend_line(support, pivot, slope_change, y)
            derivative = test_err - best_err;
            
            # If increasing by a small amount fails, 
            # try decreasing by a small amount
            if test_err < 0.0:
                slope_change = best_slope - slope_unit * min_step
                test_err = check_trend_line(support, pivot, slope_change, y)
                derivative = best_err - test_err

            if test_err < 0.0: # Derivative failed, give up
                raise Exception("Derivative failed. Check your data. ")

            get_derivative = False

        if derivative > 0.0: # Increasing slope increased error
            test_slope = best_slope - slope_unit * curr_step
        else: # Increasing slope decreased error
            test_slope = best_slope + slope_unit * curr_step
        

        test_err = check_trend_line(support, pivot, test_slope, y)
        if test_err < 0 or test_err >= best_err: 
            # slope failed/didn't reduce error
            curr_step *= 0.5 # Reduce step size
        else: # test slope reduced error
            best_err = test_err 
            best_slope = test_slope
            get_derivative = True # Recompute derivative
    
    # Optimize done, return best slope and intercept
    return (best_slope)

def fit_trendlines_single(data: np.array):
    # Trendline de melhor fit (por least squared) 
    # coefs[0] = slope,  coefs[1] = intercept
    x = np.arange(len(data))
    coefs = np.polyfit(x, data, 1)
    
    # Pontos do eixo y correspondentes a trendline fittada
    line_points = coefs[0] * x + coefs[1]

    # acha os índices do pontos chaves de máximo e de mínimo
    upper_pivot = (data - line_points).argmax() 
    lower_pivot = (data - line_points).argmin() 

    # Optimando a inclinação para as linhas de tendência
    support_slope = optimize_slope(True, lower_pivot, coefs[0], data)
    resist_slope = optimize_slope(False, upper_pivot, coefs[0], data)

    return (lower_pivot, support_slope, upper_pivot, resist_slope) 




def mapear_retas_com_bottoms(bottoms, retas, dist_min, num_pontos):
    mapeamento_suporte = pd.DataFrame(index=bottoms['bottom_idx'], columns=retas['indice'])

    # Preencher o DataFrame mapeamento
    for bottom in bottoms.itertuples():
        for reta in retas.itertuples():
            valor_na_reta = bottom.bottom_idx * reta.support_slope + reta.support_intercept
            distancia = bottom.bottom_price - valor_na_reta

            if abs(distancia) < dist_min:
                mapeamento_suporte.at[bottom.bottom_idx, reta.indice] = 0
            elif distancia < 0:
                mapeamento_suporte.at[bottom.bottom_idx, reta.indice] = -1
            else:
                mapeamento_suporte.at[bottom.bottom_idx, reta.indice] = 1
    
    mapeamento_suporte.to_csv('dados_csv_produzidos/maepamento_suporte.csv', index=True)
    
    # Avaliar cada reta
    num_reta = 0
    for coluna in mapeamento_suporte.columns:
        coluna_valores = mapeamento_suporte[coluna]
        zeros_consecutivos = 0
        x_min = None
        x_max = None
        x_min_final = 0
        x_max_final = 0
        sucesso = False
        maior_zeros = 0
        inicio_janela = retas['inicio_janela'].iloc[num_reta]
        fim_janela = retas['fim_janela'].iloc[num_reta]
        num_reta += 1
        for i, valor in enumerate(coluna_valores):
            if mapeamento_suporte.index[i] <=  fim_janela and mapeamento_suporte.index[i] >=  inicio_janela:
                if valor == 0:
                    if x_min is None: # primeiro 0 da sequencia
                        x_min = mapeamento_suporte.index[i]
                    x_max = mapeamento_suporte.index[i]
                    zeros_consecutivos += 1
                elif valor == 1:
                    x_max = mapeamento_suporte.index[i]
                elif valor == -1: # sequencia interrompida
                    if zeros_consecutivos>= num_pontos: # sequencia bem sucedida
                        sucesso = True
                        if zeros_consecutivos > maior_zeros: # nova sequencia tem mais zeros
                            maior_zeros = zeros_consecutivos
                            x_min_final = x_min
                            x_max_final = x_max
                    # reseta os valores para continuar a busca
                    x_min = None 
                    x_max = None
                    zeros_consecutivos = 0
        #verifica a última sequencia depois do loop"
        if zeros_consecutivos >= num_pontos: #verifica a última sequencia depois do loop"
            sucesso = True
            if zeros_consecutivos > maior_zeros: # nova sequencia tem mais zeros
                maior_zeros = zeros_consecutivos
                x_min_final = x_min
                x_max_final = x_max
        
        if sucesso:
            retas.loc[retas['indice'] == coluna, 'mapeado'] = 1
        else:
            retas.loc[retas['indice'] == coluna, 'mapeado'] = 0
       
        retas.loc[retas['indice'] == coluna, 'x_min'] = x_min_final
        retas.loc[retas['indice'] == coluna, 'x_max'] = x_max_final
        retas.loc[retas['indice'] == coluna, 'num_zeros'] = maior_zeros

    retas.to_csv('dados_csv_produzidos/retas_suporte.csv', index=True)
    return retas



def mapear_retas_com_tops(tops, retas, dist_min, num_pontos):
    mapeamento_resistencia = pd.DataFrame(index=tops['top_idx'], columns=retas['indice'])

    # Preencher o DataFrame mapeamento
    for top in tops.itertuples():
        for reta in retas.itertuples():
            valor_na_reta = top.top_idx * reta.resist_slope + reta.resist_intercept
            distancia = top.top_price - valor_na_reta

            if abs(distancia) < dist_min:
                mapeamento_resistencia.at[top.top_idx, reta.indice] = 0
            elif distancia < 0:
                mapeamento_resistencia.at[top.top_idx, reta.indice] = -1
            else:
                mapeamento_resistencia.at[top.top_idx, reta.indice] = 1

    mapeamento_resistencia.to_csv('dados_csv_produzidos/maepamento_resistencia.csv', index=True)

    # Avaliar cada reta
    num_reta = 0
    for coluna in mapeamento_resistencia.columns:
        coluna_valores = mapeamento_resistencia[coluna]
        zeros_consecutivos = 0
        x_min = None
        x_max = None
        x_min_final = 0
        x_max_final = 0
        sucesso = False
        maior_zeros = 0
        inicio_janela = retas['inicio_janela'].iloc[num_reta]
        fim_janela = retas['fim_janela'].iloc[num_reta]
        num_reta += 1
        for i, valor in enumerate(coluna_valores):
            if mapeamento_resistencia.index[i] <=  fim_janela and mapeamento_resistencia.index[i] >=  inicio_janela:
                if valor == 0:
                    if x_min is None: # primeiro 0 da sequencia
                        x_min = mapeamento_resistencia.index[i]
                    x_max = mapeamento_resistencia.index[i]
                    zeros_consecutivos += 1
                elif valor == -1:
                    x_max = mapeamento_resistencia.index[i]
                elif valor == 1: # sequencia interrompida
                    if zeros_consecutivos>= num_pontos: # sequencia bem sucedida
                        sucesso = True
                        if zeros_consecutivos > maior_zeros: # nova sequencia tem mais zeros
                            maior_zeros = zeros_consecutivos
                            x_min_final = x_min
                            x_max_final = x_max
                    # reseta os valores para continuar a busca
                    x_min = None 
                    x_max = None
                    zeros_consecutivos = 0
        #verifica a última sequencia depois do loop"
        if zeros_consecutivos >= num_pontos: #verifica a última sequencia depois do loop"
            sucesso = True
            if zeros_consecutivos > maior_zeros: # nova sequencia tem mais zeros
                maior_zeros = zeros_consecutivos
                x_min_final = x_min
                x_max_final = x_max
        
        if sucesso:
            retas.loc[retas['indice'] == coluna, 'mapeado'] = 1
        else:
            retas.loc[retas['indice'] == coluna, 'mapeado'] = 0
       
        retas.loc[retas['indice'] == coluna, 'x_min'] = x_min_final
        retas.loc[retas['indice'] == coluna, 'x_max'] = x_max_final
        retas.loc[retas['indice'] == coluna, 'num_zeros'] = maior_zeros

    retas.to_csv('dados_csv_produzidos/retas_resistencia.csv', index=True)
    return retas


def identifica_retas_similares_suporte(df):
    # Adiciona uma nova coluna para a reta similar
    df['reta_similar'] = np.nan

    # Intervalo de x
    x_vals = np.arange(20, 81)

    # Iterar sobre cada reta no DataFrame
    for i, reta_i in df.iterrows():
        indice_similar = reta_i['indice_original_lower_pivot']
        distancia_minima = float('inf')

        # Calcular os valores y para a reta atual
        y_i = reta_i['support_slope'] * x_vals + reta_i['support_intercept']

        # Comparar com todas as outras retas
        for j, reta_j in df.iterrows():
            if i != j:
                # Calcular os valores y para a reta de comparação
                y_j = reta_j['support_slope'] * x_vals + reta_j['support_intercept']

                # Calcular a distância máxima entre as retas
                distancia_max = np.max(np.abs(y_i - y_j))

                # Verificar se as retas são similares e atualizar a reta similar se necessário
                if distancia_max <= 4 and reta_j['indice_original_lower_pivot'] < indice_similar:
                    indice_similar = reta_j['indice_original_lower_pivot']
                    distancia_minima = distancia_max

        # Registrar a reta similar
        df.at[i, 'reta_similar'] = indice_similar

    grupos = df.groupby('reta_similar')

    # Lista para armazenar os resultados consolidados
    retas_consolidadas = []

    for nome_grupo, grupo in grupos:
        reta_consolidada = {

            'indice_original_lower_pivot': grupo['indice_original_lower_pivot'].min(),
            'valor_rsi': grupo['valor_rsi'].min(),
            'support_slope': grupo['support_slope'].mean(),
            'support_intercept': grupo['support_intercept'].mean(),
            'inicio_janela': grupo['inicio_janela'].min(),
            'fim_janela': grupo['fim_janela'].min(),
            'x_min': grupo['x_min'].min(),
            'x_max': grupo['x_max'].max(),
            'num_zeros': grupo['num_zeros'].min()
        }
        retas_consolidadas.append(reta_consolidada)

    # Criar novo dataframe com as retas consolidadas
    df_consolidado = pd.DataFrame(retas_consolidadas)

    return df_consolidado



def identifica_retas_similares_resistencia(df):
    # Adiciona uma nova coluna para a reta similar
    df['reta_similar'] = np.nan

    # Intervalo de x
    x_vals = np.arange(20, 81)

    # Iterar sobre cada reta no DataFrame
    for i, reta_i in df.iterrows():
        indice_similar = reta_i['indice_original_upper_pivot']
        distancia_minima = float('inf')

        # Calcular os valores y para a reta atual
        y_i = reta_i['resist_slope'] * x_vals + reta_i['resist_intercept']

        # Comparar com todas as outras retas
        for j, reta_j in df.iterrows():
            if i != j and reta_j['indice_original_upper_pivot'] == reta_i['indice_original_upper_pivot']:
                # Calcular os valores y para a reta de comparação
                y_j = reta_j['resist_slope'] * x_vals + reta_j['resist_intercept']

                # Calcular a distância máxima entre as retas
                distancia_max = np.max(np.abs(y_i - y_j))

                # Verificar se as retas são similares e atualizar a reta similar se necessário
                if distancia_max <= 4 and reta_j['indice_original_upper_pivot'] < indice_similar:
                    indice_similar = reta_j['indice_original_upper_pivot']
                    distancia_minima = distancia_max

        # Registrar a reta similar
        df.at[i, 'reta_similar'] = indice_similar

    grupos = df.groupby('reta_similar')

    # Lista para armazenar os resultados consolidados
    retas_consolidadas = []

    for nome_grupo, grupo in grupos:
        reta_consolidada = {
            'indice_original_upper_pivot': grupo['indice_original_upper_pivot'].min(),
            'valor_rsi': grupo['valor_rsi'].min(),
            'resist_slope': grupo['resist_slope'].mean(),
            'resist_intercept': grupo['resist_intercept'].mean(),
            'inicio_janela': grupo['inicio_janela'].min(),
            'fim_janela': grupo['fim_janela'].min(),
            'x_min': grupo['x_min'].min(),
            'x_max': grupo['x_max'].max(),
            'num_zeros': grupo['num_zeros'].min()
        }
        retas_consolidadas.append(reta_consolidada)

    # Criar novo dataframe com as retas consolidadas
    df_consolidado = pd.DataFrame(retas_consolidadas)

    return df_consolidado
