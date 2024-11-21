import pandas as pd
import numpy as np
import math

def checar_acima_abaixo_da_linha(slope, pivot_x, pivot_y, df, acima: bool):

    # Verifica se algum ponto de df está acima ou abaixo da linha definida por (pivot_x, pivot_y) e slope.
    
    intercept = pivot_y - pivot_x * slope
    
    # Itera diretamente sobre as linhas do DataFrame
    for index, row in df.iterrows():
        x = row['top_bottom_idx']
        y = row['top_bottom_value']

        # Equação da reta: y = slope * (x - pivot_x) + pivot_y
        y_on_line = intercept + slope * x
        
        if int(x) != int(pivot_x):  # Evito compara com o próprio pivot
            if acima and y_on_line - math.trunc(y * 10000) / 10000 > 0.01:
                return False  # Se for linha de suporte e y estiver abaixo da linha, retorne False
            elif not acima and y - math.trunc(y_on_line * 10000) / 10000 > 0.01:
                return False  # Se for linha de resistência e y estiver acima da linha, retorne False
    
    return True  # Se nenhum ponto estiver acima ou abaixo da linha conforme necessário, retorne True


def rotacionar_ate_tocar(tops_bottoms_df, pivot_x, pivot_y, slope, direction, support: bool):

    inclinacoes = []

    # Percorrer todos os pontos do DataFrame e calcular as inclinações
    for index, row in tops_bottoms_df.iterrows():
        x = row['top_bottom_idx']
        y = row['top_bottom_value']

        # Calcular a inclinação da reta ligando o ponto pivot ao ponto atual
        # Verificar se o divisor não é zero antes de calcular a inclinação
        if x != pivot_x:
            inclinacao = (y - pivot_y) / (x - pivot_x)
        else:
            inclinacao = slope

        # Se estiver fazendo as retas de support (inferiores, support = True)...
        if support:
            # Se estiver procurando no sentido horário (direction = 1), preciso considerar
            # as retas entre o pivot e  os outros mínimos que possuam inclinação MENOR (ou MAIS NEGATIVA)
            # do que a inclinação da reta da regressão.
            # Se o sentido for anti-horário (direction = 1), preciso considerar
            # as retas entre o pivot e os outros mínimos que possuam inclinação MAIOR (ou MENOS NEGATIVA)
            # do que a inclinação da reta da regressão.
            if direction == 1:
                if inclinacao < slope:
                    inclinacoes.append(inclinacao)
            else:
                if inclinacao > slope:
                    inclinacoes.append(inclinacao)
        else:
        # Se estiver fazendo as retas de resistência (superiores, support = False)...
            # Se estiver procurando no sentido horário (direction = 1), preciso considerar
            # as retas entre o pivot e  os outros mínimos que possuam inclinação MAIOR (ou MENOS NEGATIVA)
            # do que a inclinação da reta da regressão.
            # Se o sentido for anti-horário (direction = 1), preciso considerar
            # as retas entre o pivot e os outros mínimos que possuam inclinação MENOR (ou MAIS NEGATIVA)
            # do que a inclinação da reta da regressão.
            if direction == 1:
                if inclinacao > slope:
                    inclinacoes.append(inclinacao)
            else:
                if inclinacao < slope:
                    inclinacoes.append(inclinacao)
    
    # Se estiver procurando no sentido horário (direction = 1), preciso considerar primeiro
    # as retas de MAIOR inclinação
    if direction == 1:
            inclinacoes.sort(reverse=True)
    else:
        # Se estiver procurando no sentido horário (direction = 1), preciso considerar primeiro
        # as retas de MENOR inclinação
            inclinacoes.sort(reverse=False)

    # Percorrer as inclinações da maior para a menor

    # Se estiver fazendo as retas de support (inferiores, support = True) ...
    # testo se os pontos de mínimo estão todos acima (parâmetro True)
    if support:
        for inclinacao in inclinacoes:
            if checar_acima_abaixo_da_linha(inclinacao, pivot_x, pivot_y, tops_bottoms_df, True):
                return inclinacao
    else:
        # Se estiver fazendo as retas de resistência (superiores, support = False)...
        # testo se os pontos de mínimo estão todos abaixo (parâmetro False)
        for inclinacao in inclinacoes:
            if checar_acima_abaixo_da_linha(inclinacao, pivot_x, pivot_y, tops_bottoms_df, False):
                return inclinacao

    return None
        
    # Se todas as inclinações passarem no teste, retornar a menor inclinação
    return inclinacao_anterior




def ajustar_linha_de_tendencia(data: np.array, borda_esquerda: int, tops_bottoms_df: pd.DataFrame, support: bool):

    # Cria os índices relevantes apenas para os valores de top_bottom_idx
    x_tops_bottoms = tops_bottoms_df['top_bottom_idx'].values

    # Trendline de melhor fit (por least squares) usando todos os pontos de 'data'
    x_full = np.arange(borda_esquerda, borda_esquerda + len(data))  # Índices para todos os dados
    coefs = np.polyfit(x_full, data, 1)

    # Pontos da linha de tendência (y) correspondentes aos valores de top_bottom_idx em tops_df e bottoms_df
    line_points_tops_bottoms = coefs[0] * x_tops_bottoms + coefs[1]

    # Calcular as diferenças entre line_points e top_bottom_value para os máximos

    tops_bottoms_df = tops_bottoms_df.copy()

    if support:
        tops_bottoms_df.loc[:, 'diferenca'] = line_points_tops_bottoms - tops_bottoms_df['top_bottom_value']
    else:
        tops_bottoms_df.loc[:, 'diferenca'] = tops_bottoms_df['top_bottom_value'] - line_points_tops_bottoms


    # Acha o máximo mais distante verticalmente da reta
    pivot = tops_bottoms_df.loc[tops_bottoms_df['diferenca'].idxmax()]
    pivot_y = tops_bottoms_df.loc[tops_bottoms_df['top_bottom_idx'] == pivot['top_bottom_idx'], 'top_bottom_value'].values[0]

    # Agora, otimizando a inclinação para as linhas de tendência usando a rotação sentido horário e depois sentido anti horário
    

    slope_1 = rotacionar_ate_tocar(tops_bottoms_df, pivot['top_bottom_idx'], pivot_y, coefs[0], -1, support)

    slope_2 = rotacionar_ate_tocar(tops_bottoms_df, pivot['top_bottom_idx'], pivot_y, coefs[0], 1, support)
    
    # retorna as duas retas criadas
    return (pivot['top_bottom_idx'], pivot_y, slope_1, slope_2)



def mapear_retas_com_bottoms(bottoms, retas, dist_min, num_pontos):
    mapeamento_suporte = pd.DataFrame(index=bottoms['top_bottom_idx'], columns=retas['indice'])

    # Preencher o DataFrame mapeamento
    for bottom in bottoms.itertuples():
        for reta in retas.itertuples():
            valor_na_reta = bottom.top_bottom_idx * reta.support_slope + reta.support_intercept
            distancia = bottom.top_bottom_value - valor_na_reta

            if abs(distancia) < dist_min:
                mapeamento_suporte.at[bottom.top_bottom_idx, reta.indice] = 0
            elif distancia < 0:
                mapeamento_suporte.at[bottom.top_bottom_idx, reta.indice] = -1
            else:
                mapeamento_suporte.at[bottom.top_bottom_idx, reta.indice] = 1
    
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
    mapeamento_resistencia = pd.DataFrame(index=tops['top_bottom_idx'], columns=retas['indice'])

    # Preencher o DataFrame mapeamento
    for top in tops.itertuples():
        for reta in retas.itertuples():
            valor_na_reta = top.top_bottom_idx * reta.resist_slope + reta.resist_intercept
            distancia = top.top_bottom_value - valor_na_reta

            if abs(distancia) < dist_min:
                mapeamento_resistencia.at[top.top_bottom_idx, reta.indice] = 0
            elif distancia < 0:
                mapeamento_resistencia.at[top.top_bottom_idx, reta.indice] = -1
            else:
                mapeamento_resistencia.at[top.top_bottom_idx, reta.indice] = 1

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


def identificar_retas_similares_suporte(df):
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



def identificar_retas_similares_resistencia(df):
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


# -------------------------------------------------------------------------
# Rotinas que identificam cruzamento de uma linha de tendência
# -------------------------------------------------------------------------

#  Cruzamento para baixo

def checar_cruzou_para_baixo(ind_pontos, slope_reta_suporte, intercept_reta_suporte, break_min, dados_rsi):
    if len(ind_pontos) != 2:
        raise ValueError("A lista ind_pontos deve conter exatamente dois pontos.")

    x1, y1 = ind_pontos[0]
    x2, y2 = ind_pontos[1]

    # Calculando y na reta para os pontos x1 e x2
    y_reta_1 = slope_reta_suporte * x1 + intercept_reta_suporte
    y_reta_2 = slope_reta_suporte * x2 + intercept_reta_suporte

    # Verificando se o primeiro ponto está acima da reta e o segundo abaixo
    primeiro_acima = y1 > y_reta_1
    segundo_abaixo_distante = y2 < y_reta_2 and abs(y2 - y_reta_2) > break_min

    if primeiro_acima and segundo_abaixo_distante: # Ocorreu um cruzamento de x1 para x2, agora temos que achar primeiro ponto em que esse cruzamento ocorreu (x3)
        # Procurar por x3 entre x1 e x2, começando do primeiro x maior do que x1, indo até x2
        for x in range(int(x1) + 1, int(x2)):
            y3 = dados_rsi.iloc[x]['RSI'] # Obtendo o valor de RSI correspondente ao x3 sendo testado => y3
            y_reta_3 = slope_reta_suporte * x + intercept_reta_suporte # Obtendo o valor na reta correspondente ao x3 sendo testado => y_reta_3
            if y3 < y_reta_3: # Se y3 < y_reta_3, é sinal que houve rompimento no ponto x3 sendo testado, interrompo o teste e retorno x e y3, caso contrário, continuo
                return True, x, y3  # Retorna True e o primeiro x3 encontrado
        return True, x2, y2  # Retorno criado para evitar mensagem de erro pois loop for deveria encontrar x3 válido, nem que seja igual a x2
    else:
        return False, None, None


#  Cruzamento para cima

def checar_cruzou_para_cima(ind_pontos, slope_reta_resistencia, intercept_reta_resistencia, break_min, dados_rsi):
    if len(ind_pontos) != 2:
        raise ValueError("A lista ind_pontos deve conter exatamente dois pontos.")

    x1, y1 = ind_pontos[0]
    x2, y2 = ind_pontos[1]

    # Calculando y na reta para os pontos x1 e x2
    y_reta_1 = slope_reta_resistencia * x1 + intercept_reta_resistencia
    y_reta_2 = slope_reta_resistencia * x2 + intercept_reta_resistencia

    # Verificando se o primeiro ponto está acima da reta e o segundo abaixo
    
    primeiro_abaixo = y1 < y_reta_1
    segundo_acima_distante = y2 > y_reta_2 and abs(y2 - y_reta_2) > break_min

    if primeiro_abaixo and segundo_acima_distante:
        # Procurar por x3 entre x1 e x2, começando do primeiro x maior do que x1, indo até x2
        for x in range(int(x1) + 1, int(x2)):
            y3 = dados_rsi.iloc[x]['RSI'] # Obtendo o valor de RSI correspondente ao x3 sendo testado => y3
            y_reta_3 = slope_reta_resistencia * x + intercept_reta_resistencia # Obtendo o valor na reta correspondente ao x3 sendo testado => y_reta_3
            if y3 > y_reta_3: # Se y3 < y_reta_3, é sinal que houve rompimento no ponto x3 sendo testado, interrompo o teste e retorno x e y3, caso contrário, continuo
                return True, x, y3  # Retorna True e o primeiro x3 encontrado
        return True, x2, y2  # Retorno criado para evitar mensagem de erro pois loop for deveria encontrar x3 válido, nem que seja igual a x2
    else:
        return False, None, None

