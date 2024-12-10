# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import yfinance as yf
import os
import matplotlib.pyplot as plt
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

from gerador_de_um_cenario import simulacao


# ------------------------------------------------------------------------------------
# Criando a classe de estratégia a ser usada pela biblioteca Backtesting do Python
# ------------------------------------------------------------------------------------

class EstrategiaAdaptada(Strategy):
    # Adicione os parâmetros como variáveis de classe
    pt = 0.05  # Profit target padrão, depois será sobrescrita
    sl = 0.02  # Stop loss padrão, depois será sobrescrita
    intervalos_valendo = None  # DataFrame com intervalos de datas permitidos

    def init(self):
        # Inicializando as variáveis de estado
        self.pos_ant = 0  # 0 = sem posição, -1 = vendido, 1 = comprado
        self.ini_posicao_ant = None  # Índice inicial da posição anterior
        self.valor_posicao_ant = None  # Valor inicial da posição anterior

        self.datas_validas = self._gerar_datas_validas()  # Lista de datas válidas para negociação


    def _gerar_datas_validas(self):
        # Gera um conjunto de datas válidas baseado no DataFrame intervalos_valendo.
        datas_validas = set()

        # Garante que as colunas do DataFrame estão no formato datetime
        self.intervalos_valendo['data_ini_periodo'] = pd.to_datetime(self.intervalos_valendo['data_ini_periodo'])
        self.intervalos_valendo['data_fim_periodo'] = pd.to_datetime(self.intervalos_valendo['data_fim_periodo'])

        # Percorre cada linha do DataFrame separadamente
        for i in range(len(self.intervalos_valendo)):
            data_ini = self.intervalos_valendo.iloc[i]['data_ini_periodo']
            data_fim = self.intervalos_valendo.iloc[i]['data_fim_periodo']

            # Gera o intervalo de datas para a linha atual
            intervalo_atual = pd.date_range(start=data_ini, end=data_fim)

            # Adiciona as datas ao conjunto de datas válidas
            datas_validas.update(intervalo_atual)
        
        return datas_validas


    def next(self):
        # Preço atual e índice
        valor = self.data.Close[-1]  # Preço de fechamento da barra sendo inspecionada
        ind = len(self.data) - 1  # Índice atual no DataFrame
        
        # Data atual
        data_atual = self.data.df.index[ind]

        # Verifica se a data atual não é válida
        if data_atual not in self.datas_validas:
            if self.pos_ant != 0:  # Se houver posição aberta
                self.position.close()  # Fecha a posição existente
                self.pos_ant = 0  # Atualiza estado para sem posição
            return  # Finaliza o processamento para a data atual

        # Evento da estratégia
        evento = self.data.df.loc[self.data.df.index[ind], 'Evento']

        # Lógica de abertura de uma posição a partir de uma posição neutra
        if self.pos_ant == 0:  # Sem posição
            if evento == 1:  # Sinal de compra
                self.buy()  # Abrir posição de compra
                self.pos_ant = 1  # Muda variável de estado para comprado
                self.ini_posicao_ant = ind  # Marca a barra em que a posição foi comprada
                self.valor_posicao_ant = valor  # Assume que posição adquirida foi o preço de fechamento da barra sendo inspecionada
            elif evento == 2:  # Sinal de venda
                self.sell()  # Abrir posição de venda
                self.pos_ant = -1  # Muda variável de estado para vendido
                self.ini_posicao_ant = ind  # Marca a barra em que a posição foi vendida
                self.valor_posicao_ant = valor  # Assume que posição vendida foi o preço de fechamento da barra sendo inspecionada

        # Lógica de decisão caso a posição anterior fosse vendida
        elif self.pos_ant == -1:  # Posição vendida
            if -(valor / self.valor_posicao_ant - 1) > self.pt or \
               -(valor / self.valor_posicao_ant - 1) < -self.sl or evento == 1:  # Testa stop loss ou profit taking ou sinal de compra
                self.position.close()  # Fecha a posição
                self.pos_ant = 0  # Muda variável de estado para neutro

        # Lógica de decisão caso a posição anterior fosse comprada
        elif self.pos_ant == 1:  # Posição comprada
            if (valor - self.valor_posicao_ant) / self.valor_posicao_ant > self.pt or \
               (valor - self.valor_posicao_ant) / self.valor_posicao_ant < -self.sl or evento == 2:
                self.position.close()  # Fecha a posição
                self.pos_ant = 0  # Muda variável de estado para neutro


# ----------------------------------------------------------------------------------------------------------------
# Rotina que processa uma simulação e devolve um resultado
# ----------------------------------------------------------------------------------------------------------------

def processa_simulacao(ticker,
                       tipo_intervalo,
                       start_date,
                       end_date,
                       break_min_vals,
                       janela_rsi_vals,
                       ordem_vals,
                       lookback_vals,
                       num_pontos,
                       ppt,
                       d_max,
                       aplicar_log,
                       imprime_grafico):
    
    ticker_clean = ticker.replace("^", "")
    folder_path = f'simulações_aplicadas_a_ativos/{ticker_clean}'
    file_name_tipo_intervalo = f'{tipo_intervalo}'

    intervalos_valendo = pd.DataFrame(columns=['data_ini_periodo', 'data_fim_periodo'])
    intervalos_valendo = intervalos_valendo._append({
        'data_ini_periodo': pd.Timestamp(start_date),
        'data_fim_periodo': pd.Timestamp(end_date)
    }, ignore_index=True)

    start_date_gráfico = f"{pd.Timestamp(start_date).year if pd.Timestamp(start_date).month >= 7 else pd.Timestamp(start_date).year - 1}-01-01"

    # Verifica se o diretório já existe; se não, cria
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Especifica os nomes de todos os arquivos de auditoria que serão salvos

    file_name_dados = f'{folder_path}/{ticker_clean}_{file_name_tipo_intervalo}_dados.csv'              
    file_name_resultado = f'{folder_path}/{ticker_clean}_{file_name_tipo_intervalo}_resultados.csv'
    file_name_trades = f'{folder_path}/{ticker_clean}_{file_name_tipo_intervalo}_trades.csv'
    file_name_equity_curve = f'{folder_path}/{ticker_clean}_{file_name_tipo_intervalo}_equity_curve.csv'
    file_name_dados_com_sinais = f'{folder_path}/{ticker_clean}_{file_name_tipo_intervalo}_dados_com_sinais.csv'
    file_name_backtesting = f'{folder_path}/{ticker_clean}_{file_name_tipo_intervalo}_gráfico_backtesting_html'

    # Cria o DataFrame para armazenar os resultados que serão retornados

    resultados = pd.DataFrame(columns=[
        'janela_rsi',
        'ordem',
        'lookback',
        'd_max',
        'num_pontos',
        'break_min',
        'ppt',
        'sl',
        'pt',
        'ativo',
        'start_date',
        'end_date',
        'final_balance',
        'return_acum',
        'return_ann',
        'sharpe_ratio',
        'sortino_ratio',
        'volatility',
        'max_drawdown',
        'trades',
        'win_rate',
        'profit_factor',
        'avg_trade_return',
        ])

    # baixa dos dados do yahoo finance para o ticker e as datas informadas informado
    if ticker:
        # Importa os dados do Yahoo Finace
        data = yf.download(ticker, start=start_date_gráfico, end=end_date)
        
        # Gera o nome do arquivo com base no índice escolhido
        data.to_csv(file_name_dados, sep=";", decimal=",", index=True, encoding="utf-8")
    else:
        print("Índice inválido")

    # Converte colunas numéricas (exceto 'Date', que é uma string)
    colunas_numericas = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    # Converte as colunas para tipo numérico (ignorar erros caso já esteja no formato correto)
    data[colunas_numericas] = data[colunas_numericas].apply(pd.to_numeric, errors='coerce')

    # Loop para simular todos os cenários

    for break_min in break_min_vals:
        for janela_rsi in janela_rsi_vals:
            for ordem in ordem_vals:
                for lookback in lookback_vals:
                    print(f"Simulando para: Ativo={ticker_clean}, janela_rsi={janela_rsi}, ordem={ordem}, lookback = {lookback}, d_max={d_max}, "
                            f"break_min={break_min}, aplicar_log={aplicar_log}")
                    
                    # Chama a função de simulação para gerar os sinais

                    breaks_gerados = simulacao(janela_rsi,
                                            ordem,
                                            lookback,
                                            d_max,
                                            num_pontos,
                                            break_min,
                                            ppt,
                                            data,
                                            aplicar_log,
                                            ticker_clean,
                                            imprime_grafico)

                    # Transfere os sinais para a base com os dados

                    data['Evento'] = 0 # Zera os valor de Evento em data para colocar os Eventos de break

                    for _, row in breaks_gerados.iterrows():
                        x_rompimento = int(row['x_rompimento'])  # Certifique-se de que ponto é um inteiro
                        evento = row['evento']
                        if 0 <= x_rompimento-1 < len(data):  # Verifique se está dentro dos limites
                            data.iloc[x_rompimento-1, data.columns.get_loc('Evento')] = evento

                    # Cria o DataFrame para backtesting com índice datetime

                    dados_backtesting = pd.DataFrame({
                        'Open': data['Open'],    # Preço de abertura
                        'High': data['High'],    # Preço mais alto
                        'Low': data['Low'],      # Preço mais baixo
                        'Close': data['Close'],  # Preço de fechamento
                        'Volume': data['Volume'], # Volume negociado
                        'Evento': data['Evento']  # Sinais de compra e venda
                    }, index=data.index)  # Define o índice como a coluna 'Date'

                    # Salva o DataFrame que vai ser usado no backtesting para efeito de auditoria

                    dados_backtesting.to_csv(file_name_dados_com_sinais, sep=";", decimal=",", encoding="utf-8")

                    # Executa o backtesting

                    bt = Backtest(dados_backtesting, EstrategiaAdaptada, cash=10_000_000, commission=.002)
                    for sl_val in sl_vals:
                        for pt_val in pt_vals:
                            print(f"Rodando o backtest para: sl={sl_val}, pt={pt_val}")
                            resultado_bt = bt.run(
                                pt=pt_val, 
                                sl=sl_val, 
                                intervalos_valendo=intervalos_valendo
                            )

                            nova_linha = {
                                'janela_rsi': janela_rsi, 
                                'ordem': ordem, 
                                'lookback': lookback,
                                'd_max': d_max,
                                'num_pontos': num_pontos,
                                'break_min': break_min,
                                'ppt': ppt,
                                'sl': sl_val,
                                'pt': pt_val,
                                'ativo': ticker,
                                'start_date': start_date,
                                'end_date': end_date,
                                'final_balance': resultado_bt['Equity Final [$]'],
                                'return_acum': resultado_bt['Return [%]'],
                                'return_ann': resultado_bt['Return (Ann.) [%]'],
                                'sharpe_ratio': resultado_bt['Sharpe Ratio'],
                                'sortino_ratio': resultado_bt['Sortino Ratio'],
                                'volatility': resultado_bt['Volatility (Ann.) [%]'],
                                'max_drawdown': resultado_bt['Max. Drawdown [%]'], 
                                'trades': resultado_bt['# Trades'],  
                                'win_rate': resultado_bt['Win Rate [%]'],
                                'profit_factor': resultado_bt['Profit Factor'],
                                'avg_trade_return': resultado_bt['Avg. Trade [%]'],
                            }

                            resultados = pd.concat([resultados, pd.DataFrame([nova_linha])], ignore_index=True)                        
                            
                            if imprime_grafico:
                                
                                # # Obtem os trades executados trades = stats._trades

                                trades = resultado_bt._trades
                                trades.to_csv(file_name_trades, sep=";", decimal=",", index=True, encoding="utf-8")

                                equity_values = resultado_bt._equity_curve
                                equity_values.to_csv(file_name_equity_curve, sep=";", decimal=",", index=True, encoding="utf-8")

                                bt.plot(open_browser=True, filename=file_name_backtesting)

    # Salva o arquivo com os resultados
    resultados.to_csv(file_name_resultado, sep=";", decimal=",", index=True, encoding="utf-8")
    
    # Retorna os resultados
    return resultados



#---------------------------------------------------------------------
# Setando localidade
#---------------------------------------------------------------------

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#---------------------------------------------------------------------
# Setando variáveis fixas
#---------------------------------------------------------------------

colunas_ordenacao = ['break_min', 'janela_rsi', 'ordem', 'lookback', 'sl', 'pt']
num_pontos = 3 # pontos mínimos que uma reta tem que passar para ser relevante
ppt = 6 # pontos para trás checados no rompimento
d_max = 2 # distância máxima que uma reta tem que passar de um ponto para dizer que "passa pelo ponto"
aplicar_log = False # flag se aplica ou não o log antes de calcular o RSI"
imprime_grafico = False # flag se gera ou não os gráficos, só é usado no cenário escolhido (único)
peso_annual_return = 3
peso_sharpe_ratio = 2
peso_drawdown = 1
peso_trades = 1

indices = { 
    1: "CSCO",       # Ticker para Cisco Systems
    2: "MSFT",       # Ticker para Microsoft
    3: "PHM",        # Ticker para PulteGroup
    4: "MAR",        # Ticker para Marriott International
    5: "YUM",        # Ticker para Yum! Brands
    6: "COST",       # Ticker para Costco
    7: "HSY",        # Ticker para Hershey Company (The)
    8: "K",          # Ticker para Kellanova
    9: "HES",        # Ticker para Hess Corporation
    10: "BSX",       # Ticker para Boston Scientific
    11: "CI",        # Ticker para Cigna
    12: "CVS",       # Ticker para CVS Health
    13: "BA",        # Ticker para Boeing
    14: "GE",        # Ticker para GE Aerospace
    15: "WM",        # Ticker para Waste Management
    16: "ADBE",      # Ticker para Adobe Inc.
    17: "AAPL",      # Ticker para Apple Inc.
    18: "HPQ",       # Ticker para HP Inc.
    19: "VMC",       # Ticker para Vulcan Materials Company
    20: "NEM",       # Ticker para Newmont
    21: "AEP",       # Ticker para American Electric Power
    22: "NEE",       # Ticker para NextEra Energy
    23: "CMI",       # Ticker para Cummins Inc.
    24: "AFL",       # Ticker para Aflac
    25: "JNJ",       # Ticker para Johnson & Johnson
    26: "AIG",       # Ticker para American International Group
    27: "LLY",       # Ticker para Eli Lilly and Company
    28: "NOC",       # Ticker para Northrop Grumman
    29: "AES",       # Ticker para AES Corporation
    30: "BEN",       # Ticker para Franklin Resources
    31: "BAC",       # Ticker para Bank of America
    32: "CL",        # Ticker para Colgate-Palmolive
    33: "COF",       # Ticker para Capital One
    34: "MMC",       # Ticker para Marsh & McLennan
    35: "DHR",       # Ticker para Danaher Corporation
    36: "HAS",       # Ticker para Hasbro
    37: "PFE",       # Ticker para Pfizer
    38: "MMM",       # Ticker para 3M
    39: "ED",        # Ticker para Consolidated Edison
    40: "ORCL",      # Ticker para Oracle Corporation
    41: "PNC",       # Ticker para PNC Financial Services
    42: "MU",        # Ticker para Micron Technology
    43: "MCO",       # Ticker para Moody's Corporation
    44: "FDX",       # Ticker para FedEx
    45: "WY",        # Ticker para Weyerhaeuser
    46: "CINF",      # Ticker para Cincinnati Financial
    47: "AEE",       # Ticker para Ameren
    48: "TJX",       # Ticker para TJX Companies
    49: "SO",        # Ticker para Southern Company
    50: "ITW",       # Ticker para Illinois Tool Works
}



# indices = {
#     1: "BTC-USD",    # Ticker para Bitcoin
#     2: "^BVSP",      # Ticker para Ibovespa
#     3: "^GSPC",      # Ticker para S&P 500
# }

# ---------------------------------------------------------------------
#  Faz as simulações ativo a ativo
# ---------------------------------------------------------------------

ativo_vals = range(34,51)

folder_path = f'simulações_aplicadas_a_ativos/'
file_name_melhor_resultado_cenário = f'{folder_path}/melhores_resultados_consolidados.csv'
melhores_resultados = pd.read_csv(file_name_melhor_resultado_cenário, sep=";", decimal=",", index_col=0, encoding="utf-8")

for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")

#     # ---------------------------------------------------------------------
#     #  Primeiro o cenario_in_sample_1x 
#     # ---------------------------------------------------------------------

#     cenario_in_sample_1x = [ 1, 2, 3 ]
#     cenarios_simulados = cenario_in_sample_1x

#     # Criação do DataFrame para armazenar os resultados do cenario_in_sample_1x do ativo sendo simulado
#     resultados_cenario_in_sample_1x = pd.DataFrame(columns=[
#         'janela_rsi',
#         'ordem',
#         'lookback',
#         'd_max',
#         'num_pontos',
#         'break_min',
#         'ppt',
#         'sl',
#         'pt',
#         'ativo',
#         'cenario',
#         'return_ann',
#         'sharpe_ratio',
#         'max_drawdown',
#         'trades'
#     ])

#     for cenario in cenarios_simulados:  # Roda os cenários previstos em cenario_in_sample_1x no caso, 1, 2 e 3

#         match cenario:

#             case 1: # ------------ Bloco in_sample_1_1x ----------------------------------

#                 start_date = "2000-01-01"
#                 end_date = "2005-08-19"
#                 break_min_vals = [3, 4]
#                 lookback_vals = [50, 100]
#                 janela_rsi_vals = [14, 42, 49]
#                 ordem_vals = [3, 4, 5]
#                 sl_vals = [0.02, 0.05]
#                 pt_vals = [0.05, 0.10]
#                 tipo_intervalo = f'in_sample_1_1x'

#             case 2: # ------------ Bloco in_sample_2_1x ----------------------------------

#                 start_date = "2008-01-15"
#                 end_date = "2013-10-29"
#                 break_min_vals = [3, 4]
#                 lookback_vals = [50, 100]
#                 janela_rsi_vals = [14, 42, 49]
#                 ordem_vals = [3, 4, 5]
#                 sl_vals = [0.02, 0.05]
#                 pt_vals = [0.05, 0.10]
#                 tipo_intervalo =f'in_sample_2_1x'

#             case 3: # ------------ Bloco in_sample_3_1x ----------------------------------

#                 start_date = "2016-04-29"
#                 end_date = "2019-09-18"
#                 break_min_vals = [3, 4]
#                 lookback_vals = [50, 100]
#                 janela_rsi_vals = [14, 42, 49]
#                 ordem_vals = [3, 4, 5]
#                 sl_vals = [0.02, 0.05]
#                 pt_vals = [0.05, 0.10]
#                 tipo_intervalo =f'in_sample_3_1x'

#         resultado_simulado = processa_simulacao(ticker,  # executa a simulação e guarda no dataframe
#             tipo_intervalo,
#             start_date,
#             end_date,
#             break_min_vals,
#             janela_rsi_vals,
#             ordem_vals,
#             lookback_vals,
#             num_pontos,
#             ppt,
#             d_max,
#             aplicar_log,
#             imprime_grafico)
                
#         # Iterando pelos itens do resultado_simulado para salvar no dataframe que junta todo
#         # os resultados do cenário in_sample_1

#         for _, row in resultado_simulado.iterrows():
#             # Criação de uma nova linha com os dados extraídos de cada linha do DataFrame
#             nova_linha = {
#                 'janela_rsi': row['janela_rsi'],
#                 'ordem': row['ordem'],
#                 'lookback': row['lookback'],
#                 'd_max': row['d_max'],
#                 'num_pontos': row['num_pontos'],
#                 'break_min': row['break_min'],
#                 'ppt': row['ppt'],
#                 'sl': row['sl'],
#                 'pt': row['pt'],
#                 'ativo': row['ativo'],
#                 'cenario': tipo_intervalo,
#                 'return_ann': row['return_ann'],
#                 'sharpe_ratio': row['sharpe_ratio'],
#                 'max_drawdown': row['max_drawdown'],
#                 'trades': row['trades'],
#             }
#             # Adicionando a nova linha ao DataFrame
#             resultados_cenario_in_sample_1x = pd.concat(
#                 [resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
#                 ignore_index=True
#             )
    
#     # Antes de avançar e salvar os resultados, vamos garantir que a coluna trades tenha valores numéricos

#     resultados_cenario_in_sample_1x['trades'] = pd.to_numeric(resultados_cenario_in_sample_1x['trades'], errors='coerce').astype(float)

#     # Salva o arquivo com os resultados de resultados_cenario_in_sample_1x

#     folder_path = f'simulações_aplicadas_a_ativos/{ticker_clean}'
#     file_name_resultado_cenário = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_resultados.csv'
#     resultados_cenario_in_sample_1x.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")


#     # -------------------------------------------------------------------------------------------------
#     # Após se acumular no dataframe resultados_cenario_in_sample_1x todos os cenários previstos
#     # Vamos obter a média dos itens 'return_ann', 'sharpe_ratio', 'max_drawdown', 'trades'
#     # -------------------------------------------------------------------------------------------------

#     colunas_agrupamento = [
#         'janela_rsi', 'ordem', 'lookback', 'd_max', 'num_pontos',
#         'break_min', 'ppt', 'sl', 'pt', 'ativo'
#     ]

#     # Colunas para calcular a média
#     colunas_media = ['return_ann', 'sharpe_ratio', 'max_drawdown', 'trades']

#     # Com isso, o dataframe resultado_media_in_sample_1x tem, para os diferentes cenários, as médias obtidas

#     resultado_media_in_sample_1x = (
#         resultados_cenario_in_sample_1x.groupby(colunas_agrupamento, as_index=False)[colunas_media]
#         .mean()
#     )
#     # Agora criamos as notas obtidas entre 0 e 10, conforme o valor pro-rata entre a menor média e a maior média

#     resultado_media_in_sample_1x['Pontos_return_ann'] = \
#         10 * (resultado_media_in_sample_1x['return_ann'] - resultado_media_in_sample_1x['return_ann'].min())\
#               / (resultado_media_in_sample_1x['return_ann'].max() - resultado_media_in_sample_1x['return_ann'].min())
    
#     resultado_media_in_sample_1x['Pontos_sharpe_ratio'] = \
#         10 * (resultado_media_in_sample_1x['sharpe_ratio'] - resultado_media_in_sample_1x['sharpe_ratio'].min())\
#               / (resultado_media_in_sample_1x['sharpe_ratio'].max() - resultado_media_in_sample_1x['sharpe_ratio'].min())
    
#     resultado_media_in_sample_1x['Pontos_max_drawdown'] = \
#         10 * (resultado_media_in_sample_1x['max_drawdown'] - resultado_media_in_sample_1x['max_drawdown'].min())\
#               / (resultado_media_in_sample_1x['max_drawdown'].max() - resultado_media_in_sample_1x['max_drawdown'].min())
    
#     resultado_media_in_sample_1x['Pontos_trades'] = \
#         10 * (resultado_media_in_sample_1x['trades'].astype(float) - resultado_media_in_sample_1x['trades'].astype(float).min())\
#               / (resultado_media_in_sample_1x['trades'].astype(float).max() - resultado_media_in_sample_1x['trades'].astype(float).min())
   
#     # Para concluir, vamos obter os pontos ponderados usando os pesos definidos anteriormente

#     resultado_media_in_sample_1x['Pontos_ponderados'] = \
#     (\
#         peso_annual_return * resultado_media_in_sample_1x['Pontos_return_ann'] + \
#         peso_sharpe_ratio* resultado_media_in_sample_1x['Pontos_sharpe_ratio'] + \
#         peso_drawdown* resultado_media_in_sample_1x['Pontos_max_drawdown'] + \
#         peso_trades*resultado_media_in_sample_1x['Pontos_trades']\
#     )/ (peso_annual_return+peso_sharpe_ratio+peso_drawdown+peso_trades)
    
#     # Ordenando o DataFrame pelos valores das colunas na sequência especificada
#     resultado_media_in_sample_1x = resultado_media_in_sample_1x.sort_values(by=colunas_ordenacao)

#     # Salvando o DataFrame em um arquivo CSV
#     file_name_resultado_media_in_sample_1x = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_medias.csv'
#     resultado_media_in_sample_1x.to_csv(file_name_resultado_media_in_sample_1x, sep=";", decimal=",", index=True, encoding="utf-8")

#     # -------------------------------------------------------------------------------------------------
#     # Após calcular os pontos,  armazenar os melhores resultados do cenario_in_sample_1x
#     # Os melhores resão usados para pautar o próximo cenário (cenario_validacao)
#     # -------------------------------------------------------------------------------------------------

#     # Criação do DataFrame para armazenar os melhores resultados do cenario_in_sample_1x do ativo sendo simulado
#     melhores_resultados_cenario_in_sample_1x = pd.DataFrame(columns=[
#         'ativo',
#         'cenario',
#         'variavel',
#         'melhor_valor',
#         'media_de_pontos',
#     ])

#     # Valor de janela_rsi que produziu a melhor média e pontuação obtida

#     df_melhor_janela_rsi_in_sample_1 = resultado_media_in_sample_1x.groupby('janela_rsi')['Pontos_ponderados'].mean()
#     melhor_janela_rsi_in_sample_1 = df_melhor_janela_rsi_in_sample_1.idxmax()
#     media_melhor_janela_rsi_in_sample_1 = df_melhor_janela_rsi_in_sample_1.max()
#     nova_linha = {
#         'ativo': ticker_clean,
#         'cenario': 'cenario_in_sample_1x',
#         'variavel': 'janela_rsi',
#         'melhor_valor': melhor_janela_rsi_in_sample_1,
#         'media_de_pontos': media_melhor_janela_rsi_in_sample_1,
#     }

#     melhores_resultados_cenario_in_sample_1x = pd.concat(
#         [melhores_resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
#         ignore_index=True
#     )

#     # Valor de ordem que produziu a melhor média e pontuação obtida

#     df_melhor_ordem_in_sample_1 = resultado_media_in_sample_1x.groupby('ordem')['Pontos_ponderados'].mean()
#     melhor_ordem_in_sample_1 = df_melhor_ordem_in_sample_1.idxmax()
#     media_melhor_ordem_in_sample_1 = df_melhor_ordem_in_sample_1.max()
#     nova_linha = {
#         'ativo': ticker_clean,
#         'cenario': 'cenario_in_sample_1x',
#         'variavel': 'ordem',
#         'melhor_valor': melhor_ordem_in_sample_1,
#         'media_de_pontos': media_melhor_ordem_in_sample_1,
#     }

#     melhores_resultados_cenario_in_sample_1x = pd.concat(
#         [melhores_resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
#         ignore_index=True
#     )

#     # Valor de lookback que produziu a melhor média e pontuação obtida

#     df_melhor_lookback_in_sample_1 = resultado_media_in_sample_1x.groupby('lookback')['Pontos_ponderados'].mean()
#     melhor_lookback_in_sample_1 = df_melhor_lookback_in_sample_1.idxmax()
#     media_melhor_lookback_in_sample_1 = df_melhor_lookback_in_sample_1.max()
#     nova_linha = {
#         'ativo': ticker_clean,
#         'cenario': 'cenario_in_sample_1x',
#         'variavel': 'lookback',
#         'melhor_valor': melhor_lookback_in_sample_1,
#         'media_de_pontos': media_melhor_lookback_in_sample_1,
#     }

#     melhores_resultados_cenario_in_sample_1x = pd.concat(
#         [melhores_resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
#         ignore_index=True
#     )

#     # Valor de break_min que produziu a melhor média e pontuação obtida

#     df_melhor_break_min_in_sample_1 = resultado_media_in_sample_1x.groupby('break_min')['Pontos_ponderados'].mean()
#     melhor_break_min_in_sample_1 = df_melhor_break_min_in_sample_1.idxmax()
#     media_melhor_break_min_in_sample_1 = df_melhor_break_min_in_sample_1.max()
#     nova_linha = {
#         'ativo': ticker_clean,
#         'cenario': 'cenario_in_sample_1x',
#         'variavel': 'break_min',
#         'melhor_valor': melhor_break_min_in_sample_1,
#         'media_de_pontos': media_melhor_break_min_in_sample_1,
#     }

#     melhores_resultados_cenario_in_sample_1x = pd.concat(
#         [melhores_resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
#         ignore_index=True
#     )

#     # Salvando os melhores valores dos parâmetros
#     file_name_resultado_media_in_sample_1x = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_melhores_resultados.csv'
#     melhores_resultados_cenario_in_sample_1x.to_csv(file_name_resultado_media_in_sample_1x, sep=";", decimal=",", index=True, encoding="utf-8")




    
    # --------------------------------------------------------------------------------------------------
    #  Aqui começa a simulação de validação
    # --------------------------------------------------------------------------------------------------

    # # Caso queria overide a primeira etapa



    melhor_break_min_in_sample_1 =  melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'break_min'].values[0]
    melhor_janela_rsi_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'janela_rsi'].values[0]
    melhor_ordem_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'ordem'].values[0]
    melhor_lookback_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'lookback'].values[0]
    melhor_sl_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'sl'].values[0]
    melhor_pt_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'pt'].values[0]

    #  Com os resultados do cenario_in_sample_1x, vamos especificar os parâmetros do cenario_validacao

    break_min_vals = [melhor_break_min_in_sample_1]
    janela_rsi_vals = [melhor_janela_rsi_in_sample_1]
    ordem_vals = [melhor_ordem_in_sample_1]

    if melhor_lookback_in_sample_1 == 50:
        lookback_vals = [50, 60, 70]
    else:
        lookback_vals = [80, 90, 100]


    if melhor_sl_in_sample_1 == 0.02:
        sl_vals = [0.01, 0.02, 0.03]
    else:
        sl_vals = [0.04, 0.05, 0.06]

    if melhor_pt_in_sample_1 == 0.05:
        pt_vals = [0.05, 0.06, 0.07]
    else:
        pt_vals = [0.08, 0.10, 0.12]
    

    cenario_validacao = [4, 5, 6, 7, 8]
    cenarios_simulados = cenario_validacao

    # Criação do DataFrame para armazenar os resultados do cenario_in_sample_1x do ativo sendo simulado

    resultados_cenario_validacao = pd.DataFrame(columns=[
        'janela_rsi',
        'ordem',
        'lookback',
        'd_max',
        'num_pontos',
        'break_min',
        'ppt',
        'sl',
        'pt',
        'ativo',
        'cenario',
        'return_ann',
        'sharpe_ratio',
        'max_drawdown',
        'trades'
    ])


    for cenario in cenarios_simulados:  # Roda os cenários previstos em cenario_in_sample_1x

        match cenario:
            
            case 4: # ------------ Bloco in_sample_1_2x  ----------------------------------

                start_date = "2000-01-01"
                end_date = "2005-08-19"
                tipo_intervalo = f'in_sample_1_2x'


            case 5: # ------------ Bloco in_sample_2_2x ----------------------------------

                start_date = "2008-01-15"
                end_date = "2013-10-29"
                tipo_intervalo = f'in_sample_2_2x'

            case 6: # ------------ Bloco in_sample_3_2x ----------------------------------

                start_date = "2016-04-29"
                end_date = "2019-09-18"
                tipo_intervalo = f'in_sample_3_2x'


            case 7: # ------------ Bloco out_of_sample_val_1 ----------------------------------

                start_date = "2005-10-26"
                end_date = "2007-03-02"
                tipo_intervalo = f'out_of_sample_val_1'


            case 8: # ------------ Bloco out_of_sample_val_2 ----------------------------------

                start_date = "2019-03-06"
                end_date = "2021-09-17"
                tipo_intervalo = f'out_of_sample_val_2'

        resultado_simulado = processa_simulacao(ticker,
            tipo_intervalo,
            start_date,
            end_date,
            break_min_vals,
            janela_rsi_vals,
            ordem_vals,
            lookback_vals,
            num_pontos,
            ppt,
            d_max,
            aplicar_log,
            imprime_grafico)
                
        # Iterando pelos itens do resultado_simulado
        for _, row in resultado_simulado.iterrows():
            # Criação de uma nova linha com os dados extraídos de cada linha do DataFrame
            nova_linha = {
                'janela_rsi': row['janela_rsi'],
                'ordem': row['ordem'],
                'lookback': row['lookback'],
                'd_max': row['d_max'],
                'num_pontos': row['num_pontos'],
                'break_min': row['break_min'],
                'ppt': row['ppt'],
                'sl': row['sl'],
                'pt': row['pt'],
                'ativo': row['ativo'],
                'cenario': tipo_intervalo,
                'return_ann': row['return_ann'],
                'sharpe_ratio': row['sharpe_ratio'],
                'max_drawdown': row['max_drawdown'],
                'trades': row['trades'],
            }
            # Adicionando a nova linha ao DataFrame
            resultados_cenario_validacao = pd.concat(
                [resultados_cenario_validacao, pd.DataFrame([nova_linha])],
                ignore_index=True
            )
        
    # Se certifica de que o pandas interpreta as colunas relevantes como float antes de concatenar

    resultados_cenario_validacao['return_ann'] = pd.to_numeric(resultados_cenario_validacao['return_ann'], errors='coerce').astype(float)
    resultados_cenario_validacao['sharpe_ratio'] = pd.to_numeric(resultados_cenario_validacao['sharpe_ratio'], errors='coerce').astype(float)
    resultados_cenario_validacao['max_drawdown'] = pd.to_numeric(resultados_cenario_validacao['max_drawdown'], errors='coerce').astype(float)
    resultados_cenario_validacao['trades'] = pd.to_numeric(resultados_cenario_validacao['trades'], errors='coerce').astype(float)
    resultados_cenario_validacao['sl'] = pd.to_numeric(resultados_cenario_validacao['sl'], errors='coerce').astype(float)
    resultados_cenario_validacao['pt'] = pd.to_numeric(resultados_cenario_validacao['pt'], errors='coerce').astype(float)

    # Salva o arquivo com os resultados

    folder_path = f'simulações_aplicadas_a_ativos/{ticker_clean}'

    resultados_cenario_validacao['min_return_ann'] = resultados_cenario_validacao.groupby(['ativo', 'cenario'])['return_ann'].transform('min')
    resultados_cenario_validacao['min_sharpe_ratio'] = resultados_cenario_validacao.groupby(['ativo', 'cenario'])['sharpe_ratio'].transform('min')
    resultados_cenario_validacao['min_max_drawdown'] = resultados_cenario_validacao.groupby(['ativo', 'cenario'])['max_drawdown'].transform('min')
    resultados_cenario_validacao['min_trades'] = resultados_cenario_validacao.groupby(['ativo', 'cenario'])['trades'].transform('min')

    resultados_cenario_validacao['max_return_ann'] = resultados_cenario_validacao.groupby(['ativo', 'cenario'])['return_ann'].transform('max')
    resultados_cenario_validacao['max_sharpe_ratio'] = resultados_cenario_validacao.groupby(['ativo', 'cenario'])['sharpe_ratio'].transform('max')
    resultados_cenario_validacao['max_max_drawdown'] = resultados_cenario_validacao.groupby(['ativo', 'cenario'])['max_drawdown'].transform('max')
    resultados_cenario_validacao['max_trades'] = resultados_cenario_validacao.groupby(['ativo', 'cenario'])['trades'].transform('max')


    # Agora criamos as notas obtidas entre 0 e 10, conforme o valor pro-rata entre a menor média e a maior média

    resultados_cenario_validacao['Pontos_return_ann'] = \
        10 * (resultados_cenario_validacao['return_ann'] - resultados_cenario_validacao['min_return_ann'])\
                / (resultados_cenario_validacao['max_return_ann'] - resultados_cenario_validacao['min_return_ann'])

    resultados_cenario_validacao['Pontos_sharpe_ratio'] = \
        10 * (resultados_cenario_validacao['sharpe_ratio'] - resultados_cenario_validacao['min_sharpe_ratio'])\
                / (resultados_cenario_validacao['max_sharpe_ratio'] - resultados_cenario_validacao['min_sharpe_ratio'])

    resultados_cenario_validacao['Pontos_max_drawdown'] = \
        10 * (resultados_cenario_validacao['max_drawdown'] - resultados_cenario_validacao['min_max_drawdown'])\
                / (resultados_cenario_validacao['max_max_drawdown'] - resultados_cenario_validacao['min_max_drawdown'])

    resultados_cenario_validacao['Pontos_trades'] = \
        10 * (resultados_cenario_validacao['trades'].astype(float) - resultados_cenario_validacao['min_trades'].astype(float))\
                / (resultados_cenario_validacao['max_trades'].astype(float) - resultados_cenario_validacao['min_trades'].astype(float))

    # Para concluir, vamos obter os pontos ponderados usando os pesos definidos anteriormente

    peso_annual_return = 3
    peso_sharpe_ratio = 2
    peso_drawdown = 1
    peso_trades = 1

    resultados_cenario_validacao['Pontos_ponderados'] = \
    (\
        peso_annual_return * resultados_cenario_validacao['Pontos_return_ann'] + \
        peso_sharpe_ratio* resultados_cenario_validacao['Pontos_sharpe_ratio'] + \
        peso_drawdown* resultados_cenario_validacao['Pontos_max_drawdown'] + \
        peso_trades*resultados_cenario_validacao['Pontos_trades']\
    )/ (peso_annual_return+peso_sharpe_ratio+peso_drawdown+peso_trades)


    # Ordenando o DataFrame pelos valores das colunas na sequência especificada
    resultados_cenario_validacao = resultados_cenario_validacao.sort_values(by=colunas_ordenacao)

    # Salvando os resultados do cenario_validacao em um arquivo CSV
    file_name_resultados_cenario_validacao = f'{folder_path}/{ticker_clean}_cenario_validacao_resultados.csv'
    resultados_cenario_validacao.to_csv(file_name_resultados_cenario_validacao, sep=";", decimal=",", index=True, encoding="utf-8")

 
     # Calculando e salvando as médias somadas dos intervalos do cenario_validacao para ativo sendo simulado

    resultado_cenario_validacao_medias = resultados_cenario_validacao.groupby(
        ['janela_rsi', 'ordem', 'lookback', 'd_max', 'num_pontos', 
        'break_min', 'ppt', 'sl', 'pt', 'ativo']
    )['Pontos_ponderados'].mean().reset_index().rename(columns={'Pontos_ponderados': 'media_pontos_ponderados'})


    file_name_resultado_media_validacao = f'{folder_path}/{ticker_clean}_cenario_validacao_medias.csv'
    resultado_cenario_validacao_medias.to_csv(file_name_resultado_media_validacao, sep=";", decimal=",", index=True, encoding="utf-8")

    melhor_resultado_cenario_validacao = resultado_cenario_validacao_medias.loc[
        resultado_cenario_validacao_medias.groupby('ativo')['media_pontos_ponderados'].idxmax()
    ].reset_index(drop=True)

     # # Salvando o melhor resultado do cenario_validacao para  ativo sendo simulado
    file_name_resultado_media_validacao = f'{folder_path}/{ticker_clean}_cenario_validacao_melhor_resultado.csv'
    melhor_resultado_cenario_validacao.to_csv(file_name_resultado_media_validacao, sep=";", decimal=",", index=True, encoding="utf-8")


    # --------------------------------------------------------------------------------------------------
    #  Aqui começa a simulação final
    # --------------------------------------------------------------------------------------------------

    # Valores sobre escritos para pular a primeira etapa
 
    # melhor_break_min = 4
    # melhor_janela_rsi = 28
    # melhor_ordem = 3
    # melhor_lookback = 80
    # melhor_sl = 0.03
    # melhor_pt = 0.05

    # Usando valores obtidos no cenário validacao

    melhor_janela_rsi = melhor_resultado_cenario_validacao.iloc[0]['janela_rsi']
    melhor_ordem = melhor_resultado_cenario_validacao.iloc[0]['ordem']
    melhor_lookback = melhor_resultado_cenario_validacao.iloc[0]['lookback']
    melhor_break_min = melhor_resultado_cenario_validacao.iloc[0]['break_min']
    melhor_sl = melhor_resultado_cenario_validacao.iloc[0]['sl']
    melhor_pt = melhor_resultado_cenario_validacao.iloc[0]['pt']


    #  Com os resultados do cenario_validação, vamos especificar os parâmetros do cenario_validacao

    janela_rsi_vals = [melhor_janela_rsi]
    ordem_vals = [melhor_ordem]
    lookback_vals = [melhor_lookback]
    break_min_vals = [melhor_break_min]
    sl_vals = [melhor_sl]
    pt_vals = [melhor_pt]

    cenario_final = [9, 10]
    cenarios_simulados = cenario_final

    # Criação do DataFrame para armazenar os resultados do cenario_in_sample_1x do ativo sendo simulado

    resultados_cenario_final = pd.DataFrame(columns=[
        'janela_rsi',
        'ordem',
        'lookback',
        'd_max',
        'num_pontos',
        'break_min',
        'ppt',
        'sl',
        'pt',
        'ativo',
        'cenario',
        'return_ann',
        'sharpe_ratio',
        'max_drawdown',
        'trades'
    ])


    for cenario in cenarios_simulados:  # Roda os cenários previstos em cenario_in_sample_1x

        match cenario:
            
            case 9: # ------------ Bloco out_of_sample_final_1 ----------------------------------

                start_date = "2002-03-05"
                end_date = "2005-10-26"
                tipo_intervalo = f'out_of_sample_final_1'

            case 10: # ------------ Bloco out_of_sample_final_2 ----------------------------------

                start_date = "2021-09-18" 	
                end_date = "2024-11-01"
                tipo_intervalo = f'out_of_sample_final_2'

        resultado_simulado = processa_simulacao(ticker,
            tipo_intervalo,
            start_date,
            end_date,
            break_min_vals,
            janela_rsi_vals,
            ordem_vals,
            lookback_vals,
            num_pontos,
            ppt,
            d_max,
            aplicar_log,
            imprime_grafico)
                
        # Iterando pelos itens do resultado_simulado
        for _, row in resultado_simulado.iterrows():
            # Criação de uma nova linha com os dados extraídos de cada linha do DataFrame
            nova_linha = {
                'janela_rsi': row['janela_rsi'],
                'ordem': row['ordem'],
                'lookback': row['lookback'],
                'd_max': row['d_max'],
                'num_pontos': row['num_pontos'],
                'break_min': row['break_min'],
                'ppt': row['ppt'],
                'sl': row['sl'],
                'pt': row['pt'],
                'ativo': row['ativo'],
                'cenario': tipo_intervalo,
                'return_ann': row['return_ann'],
                'sharpe_ratio': row['sharpe_ratio'],
                'max_drawdown': row['max_drawdown'],
                'trades': row['trades'],
            }
            # Adicionando a nova linha ao DataFrame
            resultados_cenario_final = pd.concat(
                [resultados_cenario_final, pd.DataFrame([nova_linha])],
                ignore_index=True
            )
        
    # Antes de avançar, vamos garantir que a coluna trades tenha valores numéricos

    resultados_cenario_final['trades'] = pd.to_numeric(resultados_cenario_final['trades'], errors='coerce').astype(float)   
   


    # Salva o arquivo com os resultados para esse ativo

    folder_path = f'simulações_aplicadas_a_ativos/{ticker_clean}'
    file_name_resultado_cenário = f'{folder_path}/{ticker_clean}_{cenarios_simulados}_cenario_final_resultados.csv'
    resultados_cenario_final.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")

    # Carrega o arquivo com os resultados acumulados existente por ativo e intervalo

    file_name_resultados = "simulações_aplicadas_a_ativos/resultados_finais_acumulados_por_ativo_intervalo_notebook.csv" 
    resultados_existentes = pd.read_csv(file_name_resultados, sep=";", decimal=",", index_col=0, encoding="utf-8")

    # Se certifica de que o pandas interpreta as colunas relevantes como float antes de concatenar

    resultados_existentes['return_ann'] = pd.to_numeric(resultados_existentes['return_ann'], errors='coerce').astype(float)
    resultados_existentes['sharpe_ratio'] = pd.to_numeric(resultados_existentes['sharpe_ratio'], errors='coerce').astype(float)
    resultados_existentes['max_drawdown'] = pd.to_numeric(resultados_existentes['max_drawdown'], errors='coerce').astype(float)
    resultados_existentes['trades'] = pd.to_numeric(resultados_existentes['trades'], errors='coerce').astype(float)

    # Adiciona os novos resultados
    resultados_atualizados = pd.concat([resultados_existentes, resultados_cenario_final])

    # Salva o DataFrame atualizado no mesmo arquivo
    resultados_atualizados.to_csv(file_name_resultados, sep=";", decimal=",", index=True, encoding="utf-8")

    # -------------------------------------------------------------------------------------------------
    # Após calcular os pontos, armazena os melhores resultados do cenario_validacao
    # O melhores cenario será usado para pautar o cenário_final
    # -------------------------------------------------------------------------------------------------

    # Carrega o arquivo com os resultados acumulados existente por ativo e intervalo

    file_name_resultados = "simulações_aplicadas_a_ativos/resultados_finais_acumulados_por_ativo_notebook.csv" 
    resultados_existentes = pd.read_csv(file_name_resultados, sep=";", decimal=",", index_col=0, encoding="utf-8")

    # Se certifica de que o pandas interpreta as colunas relevantes como float antes de concatenar

    resultados_existentes['return_ann'] = pd.to_numeric(resultados_existentes['return_ann'], errors='coerce').astype(float)
    resultados_existentes['sharpe_ratio'] = pd.to_numeric(resultados_existentes['sharpe_ratio'], errors='coerce').astype(float)
    resultados_existentes['max_drawdown'] = pd.to_numeric(resultados_existentes['max_drawdown'], errors='coerce').astype(float)
    resultados_existentes['trades'] = pd.to_numeric(resultados_existentes['trades'], errors='coerce').astype(float)

    # # Colunas para agrupamento
    
    colunas_agrupamento = [
        'janela_rsi', 'ordem', 'lookback', 'd_max', 'num_pontos',
        'break_min', 'ppt', 'sl', 'pt', 'ativo'
    ]

    # Colunas para calcular a média
    colunas_media = ['return_ann', 'sharpe_ratio', 'max_drawdown', 'trades']

    # Adiciona os novos resultados já com as médias
    resultados_atualizados = pd.concat([resultados_existentes, resultados_cenario_final.groupby(colunas_agrupamento, as_index=False)[colunas_media].mean()])
    resultados_atualizados['cenario'] = 'Media dos resultados por ativo'

    # Salva o DataFrame atualizado no mesmo arquivo
    resultados_atualizados.to_csv(file_name_resultados, sep=";", decimal=",", index=True, encoding="utf-8")