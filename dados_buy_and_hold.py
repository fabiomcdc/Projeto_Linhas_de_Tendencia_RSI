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

all_data.to_csv("dados_para_calculo_buy_and_hold.csv", sep=";", decimal=",", index=True, encoding="utf-8")
