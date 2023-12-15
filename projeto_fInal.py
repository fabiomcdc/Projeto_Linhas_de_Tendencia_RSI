import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf
import warnings

from trendlines import fit_trendlines_single
from trendlines import mapear_retas_com_bottoms
from trendlines import mapear_retas_com_tops
from trendlines import identifica_retas_similares_resistencia
from tops_e_bottoms import checa_tops
from tops_e_bottoms import checa_bottoms
from calcula_RSI import compute_rsi

#---------------------------------------------------------------------

def simulacao(janela_rsi, ordem, lookback1, lookback2, lookback3, lookback4, distancia_maxima,num_pontos , break_min, pontos_para_tras, sl, pt, data, data_log):


    #---------------------------------------------------------------------
    # Cálculo do RSI
    #---------------------------------------------------------------------

    data['RSI'] = compute_rsi(data_log['Close'],janela_rsi)
    rsi_values = compute_rsi(data_log['Close'], janela_rsi)
    rsi_df = pd.DataFrame(data['RSI'])


    #---------------------------------------------------------------------
    # Encontrando Topos e Fundos do RSI
    #---------------------------------------------------------------------
    tops = []
    bottoms = []

    for i in range(len(data['RSI'])):
        if checa_tops(data['RSI'], i, ordem):
            # top[0] = confirmation index
            # top[1] = index of top
            # top[2] = price of top
            top = [i, i - ordem, data['RSI'][i - ordem]]
            tops.append(top)
        
        if checa_bottoms(data['RSI'], i, ordem):
            # bottom[0] = confirmation index
            # bottom[1] = index of bottom
            # bottom[2] = price of bottom
            bottom = [i, i - ordem, data['RSI'][i - ordem]]
            bottoms.append(bottom)

    tops_df = pd.DataFrame(tops, columns=['conf_idx', 'top_idx', 'top_price'])
    tops_df = tops_df.dropna(subset=['top_price'])

    bottoms_df = pd.DataFrame(bottoms, columns=['conf_idx', 'bottom_idx', 'bottom_price'])
    bottoms_df = bottoms_df.dropna(subset=['bottom_price'])

    #---------------------------------------------------------------------
    # Construção das retas de suporte para as janelas de observação
    #---------------------------------------------------------------------
    # Parâmetro
    contador_janela = 0
    borda_esquerda = bottoms_df['bottom_idx'].iloc[0]

    # Inicializar DataFrames
    support_slope = [np.nan] * len(rsi_values)
    colunas_suporte = ['indice', 'indice_original_lower_pivot', 'valor_rsi', 'support_slope', 'support_intercept', 'inicio_janela', 'fim_janela']
    trendlines_suporte_df = pd.DataFrame(columns=colunas_suporte)

    for x in [lookback1, lookback2, lookback3, lookback4]:
        lookback = x
        borda_esquerda = bottoms_df['bottom_idx'].iloc[0]
        while borda_esquerda + lookback < len(rsi_values):
            # Chamar a função fit_trendlines_single para a janela sendo avaliada
            lower_pivot, support_slope, upper_pivot, resist_slope = fit_trendlines_single(rsi_values[borda_esquerda:borda_esquerda+lookback - 1])
            lower_pivot = lower_pivot + borda_esquerda
            valor_rsi = data['RSI'].iloc[lower_pivot]
            suport_intercept = data['RSI'].iloc[lower_pivot] - lower_pivot * support_slope
            nova_linha_suporte = {
                'indice': contador_janela,
                'indice_original_lower_pivot': lower_pivot,
                'valor_rsi': valor_rsi,
                'support_slope': support_slope,
                'support_intercept':suport_intercept,
                'inicio_janela': borda_esquerda,
                'fim_janela':borda_esquerda + lookback - 1
            }
            trendlines_suporte_df = trendlines_suporte_df._append(nova_linha_suporte, ignore_index=True)

            try:
                proximo_esquerda = bottoms_df.loc[bottoms_df['bottom_idx'].gt(borda_esquerda), 'bottom_idx'].min()
                rolagem_1 = proximo_esquerda - borda_esquerda
            except IndexError:
                proximo_esquerda = None  # Ou qualquer valor padrão que você queira usar

            try:
                proximo_direita = bottoms_df.loc[bottoms_df['bottom_idx'].gt(borda_esquerda+lookback), 'bottom_idx'].min()
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
            contador_janela += 1
            borda_esquerda = borda_esquerda + rolagem

    #---------------------------------------------------------------------
    # Criando as linhas de resistência para as janelas de observação
    #---------------------------------------------------------------------
    contador_janela = 0
    borda_esquerda = tops_df['top_idx'].iloc[0]

    # Inicializar DataFrames

    resist_slope = [np.nan] * len(rsi_values)
    colunas_resistencia = ['indice', 'indice_original_upper_pivot','valor_rsi', 'resist_slope', 'resist_intercept', 'inicio_janela', 'fim_janela']
    trendlines_resistencia_df = pd.DataFrame(columns=colunas_resistencia)

    for x in [lookback1, lookback2, lookback3, lookback4]:
        lookback = x
        borda_esquerda = tops_df['top_idx'].iloc[0]
        while borda_esquerda + lookback < len(rsi_values):
            # Chamar a função fit_trendlines_single para a janela sendo avaliada
            lower_pivot, support_slope, upper_pivot, resist_slope = fit_trendlines_single(rsi_values[borda_esquerda:borda_esquerda+lookback - 1])
            upper_pivot = upper_pivot + borda_esquerda
            valor_rsi = data['RSI'].iloc[upper_pivot]
            resist_intercept = data['RSI'].iloc[upper_pivot] - upper_pivot * resist_slope
            nova_linha_resistencia = {
                'indice': contador_janela,
                'indice_original_upper_pivot': upper_pivot,
                'valor_rsi': valor_rsi,
                'resist_slope': resist_slope,
                'resist_intercept':resist_intercept,
                'inicio_janela': borda_esquerda,
                'fim_janela':borda_esquerda + lookback - 1
            }
            trendlines_resistencia_df = trendlines_resistencia_df._append(nova_linha_resistencia, ignore_index=True)

            try:
                proximo_esquerda = tops_df.loc[tops_df['top_idx'].gt(borda_esquerda), 'top_idx'].min()
                rolagem_1 = proximo_esquerda - borda_esquerda
            except IndexError:
                proximo_esquerda = None  # Ou qualquer valor padrão que você queira usar

            try:
                proximo_direita = tops_df.loc[tops_df['top_idx'].gt(borda_esquerda+lookback), 'top_idx'].min()
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
            contador_janela += 1
            borda_esquerda = borda_esquerda + rolagem
    #---------------------------------------------------------------------
    # Eliminando as retas pelo sinal Slope
    #---------------------------------------------------------------------
    slope_ok_trendlines_suporte_df = trendlines_suporte_df.loc[trendlines_suporte_df['support_slope'] > 0]
    slope_ok_trendlines_suporte_df = slope_ok_trendlines_suporte_df.reset_index(drop=True)

    slope_ok_trendlines_resistencia_df = trendlines_resistencia_df.loc[trendlines_resistencia_df['resist_slope'] < 0]
    slope_ok_trendlines_resistencia_df = slope_ok_trendlines_resistencia_df.reset_index(drop=True)
    #---------------------------------------------------------------------
    # Mapeando as retas suporte para encontrar as que passaram por três bottoms até o fim da janela que criou a reta
    #---------------------------------------------------------------------
    mapeados_trendlines_suporte_df = mapear_retas_com_bottoms(bottoms_df, slope_ok_trendlines_suporte_df, distancia_maxima, num_pontos)


    #---------------------------------------------------------------------
    # Selecionando as retas que passam por (num_pontos=3) pontos de máximo e mínimo até o fim da janela à direita
    #---------------------------------------------------------------------
    # Preparando o DataFrame para os resultados consolidados


    expurgado_trendlines_suporte_df = mapeados_trendlines_suporte_df[mapeados_trendlines_suporte_df['mapeado'] != 0]


    # Preparando o DataFrame para os resultados consolidados
    mapeados_trendlines_resistencia_df = mapear_retas_com_tops(tops_df, slope_ok_trendlines_resistencia_df, distancia_maxima, num_pontos)

    expurgado_trendlines_resistencia_df = mapeados_trendlines_resistencia_df[mapeados_trendlines_resistencia_df['mapeado'] != 0]

    #---------------------------------------------------------------------
    # Eliminando as linhas duplicadas
    #---------------------------------------------------------------------

    expurgado_trendlines_suporte_df['support_slope_rounded'] = expurgado_trendlines_suporte_df['support_slope'].round(3)

    eliminado_trendlines_suporte_df = expurgado_trendlines_suporte_df.groupby(['indice_original_lower_pivot', 'support_slope_rounded']).agg({
        'inicio_janela': 'min',
        'fim_janela': 'min',
        'support_intercept': 'first',
        'num_zeros': 'min'}).reset_index()


    eliminado_trendlines_resistencia_df = identifica_retas_similares_resistencia(expurgado_trendlines_resistencia_df)

    expurgado_trendlines_resistencia_df['resist_slope_rounded'] = expurgado_trendlines_resistencia_df['resist_slope'].round(3)
    eliminado_trendlines_resistencia_df = expurgado_trendlines_resistencia_df.groupby(['indice_original_upper_pivot', 'resist_slope_rounded']).agg({
        'inicio_janela': 'min',
        'fim_janela': 'min',
        'resist_intercept': 'first',
        'num_zeros': 'min'}).reset_index()

    #---------------------------------------------------------------------
    # Checando cruzamento das retas suporte
    #---------------------------------------------------------------------
    def cruzou_para_baixo(ind_pontos, slope_reta_suporte, intercept_reta_suporte, break_min, dados_rsi):
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

        if primeiro_acima and segundo_abaixo_distante:
            # Procurar por x3 entre x1 e x2
            for x in range(int(x1) + 1, int(x2)):
                y3 = dados_rsi.iloc[x]['RSI'] # Acessando o valor de RSI correspondente a x no DataFrame
                y_reta_3 = slope_reta_suporte * x + intercept_reta_suporte
                if y3 < y_reta_3:
                    return True, x, y3  # Retorna True e o primeiro x3 encontrado
            return True, x2, y2  # Caso nenhum x3 válido seja encontrado
        else:
            return False, None, None

    def cruzou_para_cima(ind_pontos, slope_reta_resistencia, intercept_reta_resistencia, break_min, dados_rsi):
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
            # Procurar por x3 entre x1 e x2
            for x in range(int(x1) + 1, int(x2)):
                y3 = dados_rsi.iloc[x]['RSI'] # Acessando o valor de RSI correspondente a x no DataFrame
                y_reta_3 = slope_reta_resistencia * x + intercept_reta_resistencia
                if y3 > y_reta_3:
                    return True, x, y3  # Retorna True e o primeiro x3 encontrado
            return True, x2, y2  # Caso nenhum x3 válido seja encontrado
        else:
            return False, None, None


    # --------------------------------------------------------
    # Encontrando breaks para baixo nas retas suporte
    # --------------------------------------------------------

    # DataFrame para armazenar os resultados
    breaks_down_df = pd.DataFrame(columns=['ponto', 'evento', 'reta' ,'x_rompimento', 'y_rompimento', 'inicio_janela', 'fim_janela'])

    # Processamento
    for i in range(pontos_para_tras, len(rsi_df)):
        # Criando a lista de pontos para a linha atual
        pontos = [(i - pontos_para_tras, rsi_df.iloc[i - pontos_para_tras]['RSI']), 
            (i, rsi_df.iloc[i]['RSI'])]


        for idx, linha in eliminado_trendlines_suporte_df.iterrows():
            # Extraindo os valores da reta e a fim_janela
            fim_janela = linha['fim_janela']
            inicio_janela = linha['inicio_janela']

            # Verificando se i é maior do que fim_janela + ordem
            if i > fim_janela + ordem*0:
                slope = linha['support_slope_rounded']
                intercept = linha['support_intercept']
                # Verificando cruzamento
                cruzou, x_rompimento, y_rompimento = cruzou_para_baixo( pontos, slope, intercept, break_min, rsi_df)
                if cruzou:
                        breaks_down_df = breaks_down_df._append({'ponto': i,
                                                        'evento': 1,
                                                        'reta': idx,
                                                        'x_rompimento': x_rompimento,
                                                        'y_rompimento': y_rompimento,
                                                        'inicio_janela':inicio_janela,
                                                        'fim_janela': fim_janela}, ignore_index=True)
                        

    primeiros_breaks_down_df = breaks_down_df.loc[breaks_down_df.groupby('reta')['x_rompimento'].idxmin()]
    primeiros_breaks_down_df = primeiros_breaks_down_df.loc[primeiros_breaks_down_df.groupby('x_rompimento')['fim_janela'].idxmin()]

    # --------------------------------------------------------
    # Encontrando breaks para cima nas retas de resistencia
    # --------------------------------------------------------

    # DataFrame para armazenar os resultados
    breaks_up_df = pd.DataFrame(columns=['ponto', 'evento', 'reta' ,'x_rompimento', 'y_rompimento', 'inicio_janela', 'fim_janela'])

    for i in range(pontos_para_tras, len(rsi_df)):
        # Criando a lista de pontos para a linha atual
        pontos = [(i - pontos_para_tras, rsi_df.iloc[i - pontos_para_tras]['RSI']), 
            (i, rsi_df.iloc[i]['RSI'])]

        for idx, linha in eliminado_trendlines_resistencia_df.iterrows():
            # Extraindo os valores da reta e a fim_janela
            fim_janela = linha['fim_janela']
            inicio_janela = linha['inicio_janela']

            # Verificando se i é maior do que fim_janela + ordem
            if i > fim_janela + ordem:
                slope = linha['resist_slope_rounded']
                intercept = linha['resist_intercept']
                # Verificando cruzamento
                cruzou, x_rompimento, y_rompimento = cruzou_para_cima( pontos, slope, intercept, break_min, rsi_df)
                if cruzou:
                    breaks_up_df = breaks_up_df._append({'ponto': i,
                                                    'evento': 2,
                                                    'reta': idx,
                                                    'x_rompimento': x_rompimento,
                                                    'y_rompimento': y_rompimento,
                                                    'inicio_janela':inicio_janela,
                                                    'fim_janela': fim_janela}, ignore_index=True)

    primeiros_breaks_up_df = breaks_up_df.loc[breaks_up_df.groupby('reta')['x_rompimento'].idxmin()]
    primeiros_breaks_up_df = primeiros_breaks_up_df.loc[primeiros_breaks_up_df.groupby('x_rompimento')['fim_janela'].idxmin()]

    #---------------------------------------------------------------------
    # Juntando os breaks
    #---------------------------------------------------------------------
    # Concatenar os dois DataFrames
    breaks_df = pd.concat([primeiros_breaks_down_df, primeiros_breaks_up_df])

    # Ordenar o DataFrame resultante pela coluna 'ponto'
    breaks_df = breaks_df.sort_values(by='ponto')

    # Resetar o índice se necessário
    breaks_df = breaks_df.reset_index(drop=True)

    #---------------------------------------------------------------------
    # Criando o Backtest
    #---------------------------------------------------------------------
    def estrategia(ind, valor, pos_ant, ini_posicao_ant, valor_posicao_ant, brs_df, sl, tp):
        
        # Verificar se existe uma linha em brs_df com 'ponto' igual a ind
        linha = brs_df[brs_df['ponto'] == ind]

        if pos_ant == 0:
            if not linha.empty:
                evento = linha.iloc[0]['evento']
                if evento == 1:
                    return -1, ind, valor
                elif evento == 2:
                        return 1, ind, valor
                else:
                    return 0, None, None

        elif pos_ant == -1:
            if not linha.empty:
                evento = linha.iloc[0]['evento']
                if evento == 1:
                    if valor/valor_posicao_ant-1 > tp:
                        return 0, None, valor
                    elif valor/valor_posicao_ant-1 < sl:
                        return 0, None, valor
                    else:
                        return -1, ini_posicao_ant, valor_posicao_ant
                elif evento == 2:
                    return 0, None, valor
            else:
                return -1, ini_posicao_ant, valor_posicao_ant

        elif pos_ant == 1:
            if not linha.empty:
                evento = linha.iloc[0]['evento']
                if evento == 2:
                    if valor - valor_posicao_ant > tp:
                        return 0, None, valor
                    elif valor - valor_posicao_ant < sl:
                        return 0, None, valor
                    else:
                        return 1, ini_posicao_ant, valor_posicao_ant
                elif evento == 1:
                    return 0, None, valor
            else:
                return 1, ini_posicao_ant, valor_posicao_ant

        # Para qualquer outro caso
        return pos_ant, ini_posicao_ant, valor_posicao_ant

    data = data.reset_index(drop=True)

    # Inicializar as colunas
    data['posicao'] = 0
    data['ini_posicao'] = None
    data['valor_posicao'] = None

    # Valores iniciais
    pos_ant = 0
    ini_posicao_ant = None
    valor_posicao_ant = None

    # Iterar sobre o DataFrame
    for ind in range(1, len(data)):  # Começa a partir da segunda linha
        valor = data.loc[ind, 'Close']
        pos_ant, ini_posicao_ant, valor_posicao_ant = estrategia(ind, valor, pos_ant, ini_posicao_ant, valor_posicao_ant, breaks_df, sl, pt)

        # Atualizar as colunas no DataFrame
        data.at[ind, 'posicao'] = pos_ant
        data.at[ind, 'ini_posicao'] = ini_posicao_ant
        data.at[ind, 'valor_posicao'] = valor_posicao_ant

    #---------------------------------------------------------------------
    # Calculando Quota da Estratégia
    #---------------------------------------------------------------------

    # Calcula 'retorno_ind' como antes
    data['retorno_ind'] = data['Close'].pct_change()
    data['retorno_ind'].iloc[0] = 0

    # Utiliza o 'retorno_ind' da linha seguinte e 'posicao' da linha atual
    data['retorno_estrategia'] = data['retorno_ind'].shift(-1) * data['posicao']

    # Para a última linha, como não há 'retorno_ind' seguinte, você pode definir 'retorno_estrategia' como 0 (ou outro valor conforme a necessidade)
    data['retorno_estrategia'].iloc[-1] = 0

    # Calcula 'Quota' como antes
    data['Quota'] = 100
    for i in range(1, len(data)):
        data['Quota'].iloc[i] = data['Quota'].iloc[i - 1] * (1 + data['retorno_estrategia'].iloc[i])

    data['retorno_max'] = data['Quota'].cummax()/100-1

    data['DD'] = (data['Quota']/100)/(data['retorno_max']+1)-1

    # Inicializa a coluna 'DDD' com zeros
    data['DDD'] = 0

    # Itera pelo DataFrame, aplicando a lógica desejada para a coluna 'DDD'
    for i in range(1, len(data)):
        
        if abs(data['DD'].iloc[i])<0.0000001:
            data['DDD'].iloc[i] = 0
        else:
            data['DDD'].iloc[i] = data['DDD'].iloc[i - 1] + 1

    return data['DD'].min(), data['DDD'].max(), data['Quota'].iloc[len(data)-1]-100
    #---------------------------------------------------------------------

'''
#---------------------------------------------------------------------
# Setando variáveis para a simulação
#---------------------------------------------------------------------

# janela_rsi determina o número de períodos em que os parâmetros são calculados
janela_rsi = 21

# ordem determina quantos pontos à direita e à esquerda examinamos para determina pontos de máximo (tops) e mínimos (bottoms) locais
ordem = 10

# lookback determina quantos pontos para trás vamos olhar para desenharmos as primeiras tentativas de retas de suporte e resistência
lookback1 = 50
lookback2 = 100
lookback3 = 200
lookback4 = 300

# distancia_maxima determina a distancia máxima na vertical que uma linha deve passar para considerar que passou pelo ponto
distancia_maxima = 2

# num_pontos determina quantos pontos queremos na linha de tendência no mínimo
num_pontos = 3

# ind_indice determina quais variáveis vamos usar para fazer o estudo:
# 1 = bitcoin
# 2 = ibov
# 3 = S&P 500
# 4 = FTSE All Share
# 5  = DAX
# 6 = Nikkei 225

# break_min determina a distãncia mínima na veritia do ropomimento para uma reta ser considerada rompida
break_min = 4
# pontos_para_tras determina quantos pontos para trás eu checo o rompimento
pontos_para_tras = 6

# sl = stop loss e pt = profit taking
sl = -0.02
pt = 0.06

# Escolha do ativo
ind_indice = 2

# datas do intervalo sendo avaliado
start_date = "2018-01-01"
end_date = "2023-12-31"

DD_Min,DDD_max, retorno_acum = simulacao(janela_rsi, ordem, lookback1, lookback2, lookback3, lookback4, distancia_maxima,num_pontos , break_min, pontos_para_tras, sl, pt, ind_indice, start_date, end_date):

print("DD Mínimo :" + str(DD_Min))
print("DDD Máximo :" + str(DDD_max))
print("Retorno Acumulado Final: "+str(retorno_acum)+"%")
'''

#---------------------------------------------------------------------
# Setando variáveis para a simulação
#---------------------------------------------------------------------

# Desativa todos os avisos
warnings.filterwarnings('ignore')

# Variáveis fixas
lookback1 = 50
lookback2 = 100
lookback3 = 200
lookback4 = 300
num_pontos = 3
pontos_para_tras = 6
ind_indice = 5
distancia_maxima = 2
sl = -0.02
pt = 0.06
start_date = "2018-01-01"
end_date = "2023-12-31"
break_min = 4

# Definindo as variáveis para a simulação
janela_rsi_vals = [14, 21, 35, 42]
ordem_vals = [5, 7, 9, 11]

#---------------------------------------------------------------------
# Carregando dados
#---------------------------------------------------------------------

indices = {
    1: "BTC-USD",    # Ticker para Bitcoin
    2: "^BVSP",      # Ticker para Ibovespa
    3: "^GSPC",      # Ticker para S&P 500
    4: "^FTSE",      # Ticker para FTSE All Share
    5: "^GDAXI",     # Ticker para DAX
    6: "^N225"       # Ticker para Nikkei 225
}

ticker = indices.get(ind_indice)
if ticker:
    data = yf.download(ticker, start=start_date, end=end_date)
else:
    print("Índice inválido")

# Take natural log of data to resolve price scaling issues
data_log = np.log(data)

# DataFrame para armazenar os resultados
resultados = pd.DataFrame(columns=['janela_rsi', 'ordem', 'lookback1', 'lookback2', 'lookback3', 'lookback4', 
                                   'distancia_maxima', 'num_pontos', 'break_min', 'pontos_para_tras', 
                                   'sl', 'pt', 'ind_indice', 'start_date', 'end_date', 
                                   'DD_Min', 'DDD_max', 'retorno_acum'])

# Loop para simular todos os cenários
for janela_rsi in janela_rsi_vals:
    for ordem in ordem_vals:
        # Chama a função de simulação
        DD_Min, DDD_max, retorno_acum = simulacao(janela_rsi, ordem, lookback1, lookback2, lookback3, lookback4, 
                                                    distancia_maxima, num_pontos, break_min, pontos_para_tras, 
                                                    sl, pt, data, data_log)
        
        # Imprime as variáveis do cenário
        print(f"Simulando para: janela_rsi={janela_rsi}, ordem={ordem}, distancia_maxima={distancia_maxima}, "
                f"break_min={break_min}, sl={sl}, pt={pt}")
        print(f"Resultados: DD Mínimo: {DD_Min}, DDD Máximo: {DDD_max}, Retorno Acumulado: {retorno_acum}%")

        # Adiciona os resultados ao DataFrame
        resultados = resultados._append({'janela_rsi': janela_rsi, 'ordem': ordem, 'lookback1': lookback1, 
                                        'lookback2': lookback2, 'lookback3': lookback3, 'lookback4': lookback4,
                                        'distancia_maxima': distancia_maxima, 'num_pontos': num_pontos, 
                                        'break_min': break_min, 'pontos_para_tras': pontos_para_tras, 
                                        'sl': sl, 'pt': pt, 'ind_indice': ind_indice, 
                                        'start_date': start_date, 'end_date': end_date, 
                                        'DD_Min': DD_Min, 'DDD_max': DDD_max, 'retorno_acum': retorno_acum}, 
                                        ignore_index=True)

resultados.to_csv('dados_csv_produzidos/resultados.csv', index=True)

# Reativa os avisos
warnings.filterwarnings('default')
