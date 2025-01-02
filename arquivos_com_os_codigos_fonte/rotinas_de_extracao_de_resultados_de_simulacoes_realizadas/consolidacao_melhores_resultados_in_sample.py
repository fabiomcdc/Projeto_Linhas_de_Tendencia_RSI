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

# pesos utilizados na formação das notas de avaliação dos parâmetros com melhor performance

peso_annual_return = 3
peso_sharpe_ratio = 2
peso_drawdown = 1
peso_trades = 1

# definição das colunas para ordenação, agrupamento e média

colunas_ordenacao = ['janela_rsi', 'ordem', 'lookback', 'break_min', 'sl', 'pt']

colunas_agrupamento = [
        'janela_rsi', 'ordem', 'lookback', 'd_max', 'num_pontos',
        'break_min', 'ppt', 'sl', 'pt', 'ativo'
    ]

# Colunas para calcular a média
colunas_media = ['return_ann', 'sharpe_ratio', 'max_drawdown', 'trades']


# ---------------------------------------------------------------------
#  Faz a consolidação ativo a ativo
# ---------------------------------------------------------------------

ativo_vals = range(1,51)

# Criação do DataFrame para armazenar os melhores resultados do cenario_in_sample_1x do ativo sendo simulado
melhores_resultados_cenario_in_sample = pd.DataFrame(columns=[
    'ativo',
    'cenario',
    'variavel',
    'melhor_valor',
    'media_de_pontos',
])
    
folder_path = f'simulacoes_realizadas/simulacoes_in_sample'
file_name = f'{folder_path}/consolidação_todos_in_sample.csv'

print("Carregando  ,", file_name)

resultados_todos_in_sample = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")

# Ordenando o DataFrame pelos valores das colunas na sequência especificada

resultados_todos_in_sample = resultados_todos_in_sample.sort_values(by=colunas_ordenacao)


for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")

    # selecionando apenas os dados do ativo sendo calculado

    resultados_cenario_in_sample = resultados_todos_in_sample[resultados_todos_in_sample['ativo'] == ticker_clean]

    # obtendo a média dos itens 'return_ann', 'sharpe_ratio', 'max_drawdown', 'trades' e 
    # salvando no dataframe resultado_media_in_sample_1x tem, para os diferentes cenários

    resultado_media_in_sample_1x = (
        resultados_cenario_in_sample.groupby(colunas_agrupamento, as_index=False)[colunas_media]
        .mean()
    )
    # Agora criamos as notas obtidas entre 0 e 10, conforme o valor pro-rata entre a menor média e a maior média

    resultado_media_in_sample_1x['Pontos_return_ann'] = \
        10 * (resultado_media_in_sample_1x['return_ann'] - resultado_media_in_sample_1x['return_ann'].min())\
              / (resultado_media_in_sample_1x['return_ann'].max() - resultado_media_in_sample_1x['return_ann'].min())
    
    resultado_media_in_sample_1x['Pontos_sharpe_ratio'] = \
        10 * (resultado_media_in_sample_1x['sharpe_ratio'] - resultado_media_in_sample_1x['sharpe_ratio'].min())\
              / (resultado_media_in_sample_1x['sharpe_ratio'].max() - resultado_media_in_sample_1x['sharpe_ratio'].min())
    
    resultado_media_in_sample_1x['Pontos_max_drawdown'] = \
        10 * (resultado_media_in_sample_1x['max_drawdown'] - resultado_media_in_sample_1x['max_drawdown'].min())\
              / (resultado_media_in_sample_1x['max_drawdown'].max() - resultado_media_in_sample_1x['max_drawdown'].min())
    
    resultado_media_in_sample_1x['Pontos_trades'] = \
        10 * (resultado_media_in_sample_1x['trades'].astype(float) - resultado_media_in_sample_1x['trades'].astype(float).min())\
              / (resultado_media_in_sample_1x['trades'].astype(float).max() - resultado_media_in_sample_1x['trades'].astype(float).min())
   
    # Para concluir, vamos obter os pontos ponderados usando os pesos definidos anteriormente

    resultado_media_in_sample_1x['Pontos_ponderados'] = \
    (\
        peso_annual_return * resultado_media_in_sample_1x['Pontos_return_ann'] + \
        peso_sharpe_ratio* resultado_media_in_sample_1x['Pontos_sharpe_ratio'] + \
        peso_drawdown* resultado_media_in_sample_1x['Pontos_max_drawdown'] + \
        peso_trades*resultado_media_in_sample_1x['Pontos_trades']\
    )/ (peso_annual_return+peso_sharpe_ratio+peso_drawdown+peso_trades)


    # Após calcular os pontos, armazenar os melhores resultados do cenario_in_sample_1x

    # Valor de janela_rsi que produziu a melhor média e pontuação obtida

    df_melhor_janela_rsi_in_sample_1 = resultado_media_in_sample_1x.groupby('janela_rsi')['Pontos_ponderados'].mean()
    melhor_janela_rsi_in_sample_1 = df_melhor_janela_rsi_in_sample_1.idxmax()
    media_melhor_janela_rsi_in_sample_1 = df_melhor_janela_rsi_in_sample_1.max()
    nova_linha = {
        'ativo': ticker_clean,
        'cenario': 'cenario_in_sample_1x',
        'variavel': 'janela_rsi',
        'melhor_valor': melhor_janela_rsi_in_sample_1,
        'media_de_pontos': media_melhor_janela_rsi_in_sample_1,
    }

    melhores_resultados_cenario_in_sample = pd.concat(
        [melhores_resultados_cenario_in_sample, pd.DataFrame([nova_linha])],
        ignore_index=True
    )

    # Valor de ordem que produziu a melhor média e pontuação obtida

    df_melhor_ordem_in_sample_1 = resultado_media_in_sample_1x.groupby('ordem')['Pontos_ponderados'].mean()
    melhor_ordem_in_sample_1 = df_melhor_ordem_in_sample_1.idxmax()
    media_melhor_ordem_in_sample_1 = df_melhor_ordem_in_sample_1.max()
    nova_linha = {
        'ativo': ticker_clean,
        'cenario': 'cenario_in_sample_1x',
        'variavel': 'ordem',
        'melhor_valor': melhor_ordem_in_sample_1,
        'media_de_pontos': media_melhor_ordem_in_sample_1,
    }

    melhores_resultados_cenario_in_sample = pd.concat(
        [melhores_resultados_cenario_in_sample, pd.DataFrame([nova_linha])],
        ignore_index=True
    )

    # Valor de lookback que produziu a melhor média e pontuação obtida

    df_melhor_lookback_in_sample_1 = resultado_media_in_sample_1x.groupby('lookback')['Pontos_ponderados'].mean()
    melhor_lookback_in_sample_1 = df_melhor_lookback_in_sample_1.idxmax()
    media_melhor_lookback_in_sample_1 = df_melhor_lookback_in_sample_1.max()
    nova_linha = {
        'ativo': ticker_clean,
        'cenario': 'cenario_in_sample_1x',
        'variavel': 'lookback',
        'melhor_valor': melhor_lookback_in_sample_1,
        'media_de_pontos': media_melhor_lookback_in_sample_1,
    }

    melhores_resultados_cenario_in_sample = pd.concat(
        [melhores_resultados_cenario_in_sample, pd.DataFrame([nova_linha])],
        ignore_index=True
    )

    # Valor de break_min que produziu a melhor média e pontuação obtida

    df_melhor_break_min_in_sample_1 = resultado_media_in_sample_1x.groupby('break_min')['Pontos_ponderados'].mean()
    melhor_break_min_in_sample_1 = df_melhor_break_min_in_sample_1.idxmax()
    media_melhor_break_min_in_sample_1 = df_melhor_break_min_in_sample_1.max()
    nova_linha = {
        'ativo': ticker_clean,
        'cenario': 'cenario_in_sample_1x',
        'variavel': 'break_min',
        'melhor_valor': melhor_break_min_in_sample_1,
        'media_de_pontos': media_melhor_break_min_in_sample_1,
    }

    melhores_resultados_cenario_in_sample = pd.concat(
        [melhores_resultados_cenario_in_sample, pd.DataFrame([nova_linha])],
        ignore_index=True
    )

    # Valor de num_pontos que produziu a melhor média e pontuação obtida

    df_melhor_num_pontos_in_sample_1 = resultado_media_in_sample_1x.groupby('num_pontos')['Pontos_ponderados'].mean()
    melhor_num_pontos_in_sample_1 = df_melhor_num_pontos_in_sample_1.idxmax()
    media_melhor_num_pontos_in_sample_1 = df_melhor_num_pontos_in_sample_1.max()
    nova_linha = {
        'ativo': ticker_clean,
        'cenario': 'cenario_in_sample_1x',
        'variavel': 'num_pontos',
        'melhor_valor': melhor_num_pontos_in_sample_1,
        'media_de_pontos': media_melhor_num_pontos_in_sample_1,
    }

    melhores_resultados_cenario_in_sample = pd.concat(
        [melhores_resultados_cenario_in_sample, pd.DataFrame([nova_linha])],
        ignore_index=True
    )

# Salvando os melhores valores dos parâmetros
file_name_resultado_media_in_sample_1x = f'{folder_path}/melhores_resultados.csv'
melhores_resultados_cenario_in_sample.to_csv(file_name_resultado_media_in_sample_1x, sep=";", decimal=",", index=True, encoding="utf-8")