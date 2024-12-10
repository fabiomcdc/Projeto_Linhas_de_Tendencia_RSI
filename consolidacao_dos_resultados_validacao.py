# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
#  Eliminando warnings indesejados 
# ---------------------------------------------------------------------

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)



#---------------------------------------------------------------------
# Setando localidade
#---------------------------------------------------------------------

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#---------------------------------------------------------------------
# Setando variáveis fixas
#---------------------------------------------------------------------

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

# ---------------------------------------------------------------------
#  Faz a consolidação ativo a ativo
# ---------------------------------------------------------------------

ativo_vals = range(1,51)

# Criação do DataFrame para armazenar os resultados do cenario_in_sample_1x do ativo sendo simulado
resultados_consolidados = pd.DataFrame(columns=[
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
    'trades',
])


for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")


    # simulações_aplicadas_a_ativos - RSI 21 e 28 ---------------------------------------------------------
    
    folder_path = f'simulações_aplicadas_a_ativos/{ticker_clean}'
    file_name = f'{folder_path}/{ticker_clean}_cenario_validacao_resultados.csv'

    print("Carregando  ,", file_name)

    resultados_do_ativo_df = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")

    for _, row in resultados_do_ativo_df.iterrows():

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
            'cenario': row['cenario'],
            'return_ann': row['return_ann'],
            'sharpe_ratio': row['sharpe_ratio'],
            'max_drawdown': row['max_drawdown'],
            'trades': row['trades'],
        }

        # Adicionando a nova linha ao DataFrame
        resultados_consolidados = pd.concat(
            [resultados_consolidados, pd.DataFrame([nova_linha])],
            ignore_index=True
        )

# Salva o arquivo com os resultados consolidados

folder_path = f'simulações_aplicadas_a_ativos/'
file_name_resultado_cenário = f'{folder_path}/resultados_consolidados_validacao.csv'
resultados_consolidados.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")


# Criação do DataFrame para armazenar os resultados do cenario_in_sample_1x do ativo sendo simulado
resultados_consolidados_melhores_media = pd.DataFrame(columns=[
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
    'media_pontos_ponderados',
])


for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")


    # simulações_aplicadas_a_ativos - RSI 21 e 28 ---------------------------------------------------------
    
    folder_path = f'simulações_aplicadas_a_ativos/{ticker_clean}'
    file_name = f'{folder_path}/{ticker_clean}_cenario_validacao_melhor_resultado.csv'

    print("Carregando  ,", file_name)

    resultados_do_ativo_df = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")

    for _, row in resultados_do_ativo_df.iterrows():

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
            'media_pontos_ponderados': row['media_pontos_ponderados'],
        }

        # Adicionando a nova linha ao DataFrame
        resultados_consolidados_melhores_media = pd.concat(
            [resultados_consolidados_melhores_media, pd.DataFrame([nova_linha])],
            ignore_index=True
        )

# Salva o arquivo com os resultados consolidados

folder_path = f'simulações_aplicadas_a_ativos/'
file_name_resultado_cenário = f'{folder_path}/resultados_consolidados_validacao_melhores_medias.csv'
resultados_consolidados_melhores_media.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")
