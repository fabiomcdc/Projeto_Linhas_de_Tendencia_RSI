import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Lista de datas no formato 'YYYY-MM-DD'
date_list = [
    '2000-01-03',
    '2005-08-19',
    '2005-08-22',
    '2008-01-14',
    '2008-01-15',
    '2013-10-29',
    '2013-10-30',
    '2016-04-28',
    '2016-04-29',
    '2019-09-18',
    '2019-09-19',
    '2022-05-17',
    '2022-05-18',
    '2024-11-01'
]

# Lista de tickers


indices = { 
    1: "^BVSP",     # Ticker para Ibovespa
    2: "^GSPC",     # Ticker para S&P 500
    3: "^FTSE",     # Ticker para FTSE 100
    4: "^IXIC",     # Ticker para NASDAQ
    5: "PETR4.SA",  # Ticker para Petrobras
    6: "VALE3.SA",  # Ticker para Vale
    7: "ITUB",      # Ticker para Itaú Unibanco
    8: "GOAU3.SA",     # Ticker para Americana
    9: "BRLUSD=X",  # Ticker para BRL
    10: "EURUSD=X",  # Ticker para Euro
    11: "JPYUSD=X",  # Ticker para BRL
    12: "CNYUSD=X",  # Ticker para YUAN
}

# DataFrame para consolidar todos os ativos
all_data = pd.DataFrame()

for ativo in indices:
    ticker = indices[ativo]
    ticker_clean = ticker.replace("^", "")  # Limpar ticker, se necessário
    print(f"Baixando dados para o ticker: {ticker}")

    data = []  # Lista para armazenar os dados temporariamente

    for date in date_list:
        try:
            # Converter a data para datetime e calcular o dia seguinte
            start_date = datetime.strptime(date, '%Y-%m-%d')
            end_date = start_date + timedelta(days=1)

            # Tentar buscar os dados para o intervalo
            df = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
            
            if not df.empty:
                df['Ticker'] = ticker_clean  # Adicionar a coluna com o ticker
                df['Data_Pregao'] = start_date.date()  # Renomear para Data_Pregao
                data.append(df)
            else:
                print(f"Sem dados para {ticker} no intervalo {start_date.date()} - {end_date.date()}.")
        except Exception as e:
            print(f"Erro ao buscar dados para {ticker} no intervalo {date}: {e}")

    # Verificar se há dados na lista
    if data:
        # Combinar os DataFrames do ticker atual
        ticker_data = pd.concat(data)
        # Acumular no DataFrame consolidado
        all_data = pd.concat([all_data, ticker_data])
    else:
        print(f"Nenhum dado disponível para o ticker {ticker} nas datas especificadas.")

# Resetar o índice do DataFrame consolidado, mas sem conflito com "Date"
all_data.reset_index(drop=True, inplace=True)

# Reorganizar as colunas: colocar 'Ticker' e 'Data_Pregao' no início
cols = ['Ticker', 'Data_Pregao'] + [col for col in all_data.columns if col not in ['Ticker', 'Data_Pregao']]
all_data = all_data[cols]

# Salvar os dados

all_data.to_csv("dados_para_calculo_buy_and_hold_outros_ativos.csv", sep=";", decimal=",", index=True, encoding="utf-8")
