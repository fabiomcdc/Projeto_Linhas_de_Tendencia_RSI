# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
from backtesting import Backtest, Strategy
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

from gerador_de_um_cenario import simulacao

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

ind_indice = 2

indices = {
    1: "BTC-USD",    # Ticker para Bitcoin
    2: "^BVSP",      # Ticker para Ibovespa
    3: "^GSPC",      # Ticker para S&P 500
    4: "^FTSE",      # Ticker para FTSE All Share
    5: "^GDAXI",     # Ticker para DAX
    6: "^N225"       # Ticker para Nikkei 225
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
#  # Desativa todos os avisos
# ---------------------------------------------------------------------

warnings.filterwarnings('ignore')


#---------------------------------------------------------------------
# Setando variáveis para a simulação
#---------------------------------------------------------------------

# Variáveis fixas
num_pontos = 3
pontos_para_tras = 6
ind_indice = 5
distancia_maxima = 2
sl = -0.02
pt = 0.06
break_min = 4
aplicar_log = False

# Definindo as variáveis para a simulação
# lookbacks = [40, 70, 90, 100]
# janela_rsi_vals = [14, 21, 35, 42]
# ordem_vals = [3, 5, 7]

lookbacks = [40, 70]
janela_rsi_vals = [14, 21]
ordem_vals = [3, 4]

# ------------------------------------------------------------------------------------
# Criando a classe de estratégia a ser usada pela biblioteca Backtesting do Python
# ------------------------------------------------------------------------------------

class EstrategiaAdaptada(Strategy):

    pt = 0.05
    sl = 0.02
    
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

        # Lógica de abertura de uma posição a partida de uma posição neutra
        
        if self.pos_ant == 0:  # Sem posição
            if evento == 1:  # Sinal de compra
                self.buy()  # Abrir posição de compra
                self.pos_ant = 1 # Muda variável de estado para comprado
                self.ini_posicao_ant = ind # Marca a barra em que a posição foi comprada
                self.valor_posicao_ant = valor # Assume que posição adiquirida foi o preço de fechamento da barra sendo inspecionada
            elif evento == 2:  # Sinal de venda
                self.sell()  # Abrir posição de venda
                self.pos_ant = -1 # Muda variável de estado para vendido
                self.ini_posicao_ant = ind # Marca a barra em que a posição foi vendida
                self.valor_posicao_ant = valor # Assume que posição vendida foi o preço de fechamento da barra sendo inspecionada

        # Lógica de decisão caso a posição anterior fosse vendida

        elif self.pos_ant == -1:  # Posição vendida
            if (valor / self.valor_posicao_ant - 1) > self.pt or (valor / self.valor_posicao_ant - 1) < -self.sl or evento == 1: # Testa stop loss ou profit taking ou sinal de compra
                self.position.close()  # Fecha a posição
                self.pos_ant = 0 # Muda variável de estado para neutro

        # Lógica de decisão caso a posição anterior fosse comprada

        elif self.pos_ant == 1:  # Posição comprada
            if (valor - self.valor_posicao_ant) / self.valor_posicao_ant > self.pt or \
               (valor - self.valor_posicao_ant) / self.valor_posicao_ant < -self.sl or evento == 2:
                self.position.close()  # Fecha a posição
                self.pos_ant = 0 # Muda variável de estado para neutro


#---------------------------------------------------------------------
# Criando o DataFrame para armazenar os resultados
#---------------------------------------------------------------------

# DataFrame para armazenar os resultados
resultados = pd.DataFrame(columns=[
    'janela_rsi',
    'ordem',
    'lookback',
    'distancia_maxima',
    'num_pontos',
    'break_min',
    'pontos_para_tras',
    'sl',
    'pt',
    'ind_indice',
    'start_date',
    'end_date',
    'final_balance',
    'return_%',
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
# Loop para simular todos os cenários
#---------------------------------------------------------------------

for janela_rsi in janela_rsi_vals:
    for ordem in ordem_vals:
        for lookback1 in lookbacks:
            print(f"Simulando para: janela_rsi={janela_rsi}, ordem={ordem}, distancia_maxima={distancia_maxima}, "
                    f"break_min={break_min}, sl={sl}, pt={pt}, aplicar_log={aplicar_log}, ticker_clean={ticker_clean}")
            # Chama a função de simulação
            breaks_gerados = simulacao(janela_rsi,
                                       ordem,
                                       lookback1,
                                       distancia_maxima,
                                       num_pontos,
                                       break_min,
                                       pontos_para_tras,
                                       data,
                                       aplicar_log,
                                       ticker_clean)

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

            # Executar o backtesting
            bt = Backtest(dados_backtesting, EstrategiaAdaptada, cash=10000000, commission=.002)
            resultado_bt = bt.run()

            print(resultado_bt)

            nova_linha = {
                'janela_rsi': janela_rsi, 
                'ordem': ordem, 
                'lookback': lookback1,
                'distancia_maxima': distancia_maxima,
                'num_pontos': num_pontos,
                'break_min': break_min,
                'pontos_para_tras': pontos_para_tras,
                'sl': sl,
                'pt': pt,
                'ind_indice': ind_indice,
                'start_date': start_date,
                'end_date': end_date,
                'final_balance': resultado_bt['Equity Final [$]'],
                'return_%': resultado_bt['Return [%]'],
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

resultados.to_csv('dados_csv_produzidos/resultados.csv', index=True)

# Exibir os resultados
print(resultado_bt)
print(resultados)

bt.plot(open_browser=True)

