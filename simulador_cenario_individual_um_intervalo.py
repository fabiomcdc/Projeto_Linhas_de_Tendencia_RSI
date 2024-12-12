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

#---------------------------------------------------------------------
# Setando localidade
#---------------------------------------------------------------------

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#---------------------------------------------------------------------
# Setando variáveis fixas
#---------------------------------------------------------------------

num_pontos = 3
ppt = 6 # pontos para trás checados no rompimento
d_max = 2
aplicar_log = False
imprime_grafico = False
salva_dados = False

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


ind = 1

ticker = indices.get(ind)
ticker_clean = ticker.replace("^", "")


# ---------------------------------------------------------------------
#  Fazendo a simulacao
# ---------------------------------------------------------------------

intervalo_simulado_vals = [ 0 ]

for intervalo_simulado in intervalo_simulado_vals:

    # Preaparando dataframe para guardar os intervalos válidos

    intervalos_valendo = pd.DataFrame(columns=['data_ini_periodo', 'data_fim_periodo'])

    match intervalo_simulado:
        
        case 0: # ------------ Teste Unitári com gráfico ----------------------------------

            start_date = "2008-01-15"
            end_date = "2013-10-29"

            start_date_gráfico = f"{pd.Timestamp(start_date).year if pd.Timestamp(start_date).month >= 1 else pd.Timestamp(start_date).year - 1}-01-01"
            # start_date_gráfico = start_date

            intervalos_valendo = intervalos_valendo._append({
                'data_ini_periodo': pd.Timestamp(start_date),
                'data_fim_periodo': pd.Timestamp(end_date)
            }, ignore_index=True)

            break_min_vals = [3]
            lookback_vals = [100]
            janela_rsi_vals = [14]
            ordem_vals = [5]
            sl_vals = [0.02]
            pt_vals = [0.05]
            imprime_grafico = True
            salva_dados = True

    #---------------------------------------------------------------------
    # Criando o DataFrame para armazenar os resultados
    #---------------------------------------------------------------------

    # DataFrame para armazenar os resultados
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
        'ind',
        'start_date',
        'end_date',
        'final_balance',
        'return_%',
        'return_ann_%',
        'sharpe_ratio',
        'sortino_ratio',
        'volatility',
        'max_drawdown_%',
        'trades',
        'win_rate_%',
        'profit_factor',
        'avg_trade_return',
        ])

    #---------------------------------------------------------------------
    # Carregando os dados
    #---------------------------------------------------------------------

    if ticker:
        # Importa os dados do Yahoo Finace
        data = yf.download(ticker, start=start_date_gráfico, end=end_date)
        
        # Salva arquivo com os dados do índice escolhido
        if salva_dados:
            folder_path = f'simulações_individuais/{ticker_clean}'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_name = f'{folder_path}/dados_de {start_date_gráfico} até {end_date}.csv'

            data.to_csv(file_name, sep=";", decimal=",", index=True, encoding="utf-8")

    else:
        print("Índice inválido")

    # Convertendo colunas numéricas (exceto 'Date', que é uma string)
    
    colunas_numericas = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    # Converter as colunas para tipo numérico (ignorar erros caso já esteja no formato correto)
    data[colunas_numericas] = data[colunas_numericas].apply(pd.to_numeric, errors='coerce')

    for break_min in break_min_vals:
        for janela_rsi in janela_rsi_vals:
            for ordem in ordem_vals:
                for lookback in lookback_vals:
                    
                    simulacao_name = f'janela_rsi_{janela_rsi} ordem_{ordem}, lookback_{lookback}, break_min_{break_min}'

                    folder_path = f'simulações_Individuais/{ticker_clean}/{simulacao_name}'
                    # Verifica se o diretório já existe; se não, cria
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    print(f"Simulando para: janela_rsi={janela_rsi}, ordem={ordem}, lookback = {lookback}, d_max={d_max}, "
                            f"break_min={break_min}, aplicar_log={aplicar_log}, ticker_clean={ticker_clean}")
                    # Chama a função de simulação
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
                                            imprime_grafico,
                                            salva_dados)

                    # Imprime as variáveis do cenário


                    data['Evento'] = 0 # Zera os valor de Evento em data para colocar os Eventos de break

                    for _, row in breaks_gerados.iterrows():
                        x_rompimento = int(row['x_rompimento'])  # Certifique-se de que ponto é um inteiro
                        evento = row['evento']
                        if 0 <= x_rompimento-1 < len(data):  # Verifique se está dentro dos limites
                            data.iloc[x_rompimento-1, data.columns.get_loc('Evento')] = evento

                    # Criar o DataFrame para backtesting com índice datetime
                    dados_backtesting = pd.DataFrame({
                        'Open': data['Open'],    # Preço de abertura
                        'High': data['High'],    # Preço mais alto
                        'Low': data['Low'],      # Preço mais baixo
                        'Close': data['Close'],  # Preço de fechamento
                        'Volume': data['Volume'], # Volume negociado
                        'Evento': data['Evento']  # Sinais de compra e venda
                    }, index=data.index)  # Define o índice como a coluna 'Date'


                    file_name = f'simulações_individuais/{ticker_clean}/{simulacao_name}/dados_com_sinais.csv'
                    dados_backtesting.reset_index().to_csv(file_name, sep=";", decimal=",", index=True, encoding="utf-8")

                    # Executar o backtesting
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
                                'ind': ind,
                                'start_date': start_date,
                                'end_date': end_date,
                                'final_balance': resultado_bt['Equity Final [$]'],
                                'return_%': resultado_bt['Return [%]'],
                                'return_ann_%': resultado_bt['Return (Ann.) [%]'],
                                'sharpe_ratio': resultado_bt['Sharpe Ratio'],
                                'sortino_ratio': resultado_bt['Sortino Ratio'],
                                'volatility': resultado_bt['Volatility (Ann.) [%]'],
                                'max_drawdown_%': resultado_bt['Max. Drawdown [%]'], 
                                'trades': resultado_bt['# Trades'],  
                                'win_rate_%': resultado_bt['Win Rate [%]'],
                                'profit_factor': resultado_bt['Profit Factor'],
                                'avg_trade_return': resultado_bt['Avg. Trade [%]'],
                            }

                            resultados = pd.concat([resultados, pd.DataFrame([nova_linha])], ignore_index=True)                        
                            
                            if imprime_grafico:
                                
                                # # Obtendo os trades executados trades = stats._trades
                                trades = resultado_bt._trades

                                file_name = f'simulações_individuais/{ticker_clean}/{simulacao_name}/trades.csv'
                                trades.to_csv(file_name, sep=";", decimal=",", index=True, encoding="utf-8")

                                equity_values = resultado_bt._equity_curve

                                file_name = f'simulações_individuais/{ticker_clean}/{simulacao_name}/equity_values.csv'
                                equity_values.reset_index().to_csv(file_name, sep=";", decimal=",", index=True, encoding="utf-8")

                                file_name_backtesting = f'simulações_individuais/{ticker_clean}/{simulacao_name}/gráfico_backtesting_html'
                                bt.plot(open_browser=True, filename=file_name_backtesting)


    file_name = f'simulações_individuais/{ticker_clean}/{simulacao_name}/resultados.csv'
    resultados.to_csv(file_name, sep=";", decimal=",", index=True, encoding="utf-8")





