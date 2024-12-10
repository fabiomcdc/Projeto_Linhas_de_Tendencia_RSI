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
    'trades'
])

tipo_intervalo = "in_sample_1"

for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")


    # simulações_aplicadas_a_ativos - RSI 21 e 28 ---------------------------------------------------------
    
    folder_path = f'simulações_aplicadas_a_ativos - RSI 21 e 28/{ticker_clean}'
    file_name = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_resultados.csv'

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
    
    # simulações_aplicadas_a_ativos - RSI 28 e 35, pulando os de 28 ---------------------------------------------------

    folder_path = f'simulações_aplicadas_a_ativos - RSI 28 e 35/{ticker_clean}'
    file_name = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_resultados.csv'

    print("Carregando ,", file_name)

    resultados_do_ativo_df = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")


    for _, row in resultados_do_ativo_df.iterrows():

        if row['janela_rsi'] != 28 :

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

    # simulações_aplicadas_a_ativos - RSI 14 42 e 49 ---------------------------------------------------------
    
    folder_path = f'simulações_aplicadas_a_ativos - RSI 14 42 e 49/{ticker_clean}'
    file_name = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_resultados.csv'

    print("Carregando ,", file_name)

    resultados_do_ativo_df = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")


    for _, row in resultados_do_ativo_df.iterrows():

        if row['janela_rsi'] != 28 :

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

resultados_consolidados['min_return_ann'] = resultados_consolidados.groupby(['ativo', 'cenario'])['return_ann'].transform('min')
resultados_consolidados['min_sharpe_ratio'] = resultados_consolidados.groupby(['ativo', 'cenario'])['sharpe_ratio'].transform('min')
resultados_consolidados['min_max_drawdown'] = resultados_consolidados.groupby(['ativo', 'cenario'])['max_drawdown'].transform('min')
resultados_consolidados['min_trades'] = resultados_consolidados.groupby(['ativo', 'cenario'])['trades'].transform('min')

resultados_consolidados['max_return_ann'] = resultados_consolidados.groupby(['ativo', 'cenario'])['return_ann'].transform('max')
resultados_consolidados['max_sharpe_ratio'] = resultados_consolidados.groupby(['ativo', 'cenario'])['sharpe_ratio'].transform('max')
resultados_consolidados['max_max_drawdown'] = resultados_consolidados.groupby(['ativo', 'cenario'])['max_drawdown'].transform('max')
resultados_consolidados['max_trades'] = resultados_consolidados.groupby(['ativo', 'cenario'])['trades'].transform('max')


# Agora criamos as notas obtidas entre 0 e 10, conforme o valor pro-rata entre a menor média e a maior média

resultados_consolidados['Pontos_return_ann'] = \
    10 * (resultados_consolidados['return_ann'] - resultados_consolidados['min_return_ann'])\
            / (resultados_consolidados['max_return_ann'] - resultados_consolidados['min_return_ann'])

resultados_consolidados['Pontos_sharpe_ratio'] = \
    10 * (resultados_consolidados['sharpe_ratio'] - resultados_consolidados['min_sharpe_ratio'])\
            / (resultados_consolidados['max_sharpe_ratio'] - resultados_consolidados['min_sharpe_ratio'])

resultados_consolidados['Pontos_max_drawdown'] = \
    10 * (resultados_consolidados['max_drawdown'] - resultados_consolidados['min_max_drawdown'])\
            / (resultados_consolidados['max_max_drawdown'] - resultados_consolidados['min_max_drawdown'])

resultados_consolidados['Pontos_trades'] = \
    10 * (resultados_consolidados['trades'].astype(float) - resultados_consolidados['min_trades'].astype(float))\
            / (resultados_consolidados['max_trades'].astype(float) - resultados_consolidados['min_trades'].astype(float))

# Para concluir, vamos obter os pontos ponderados usando os pesos definidos anteriormente

peso_annual_return = 3
peso_sharpe_ratio = 2
peso_drawdown = 1
peso_trades = 1

resultados_consolidados['Pontos_ponderados'] = \
(\
    peso_annual_return * resultados_consolidados['Pontos_return_ann'] + \
    peso_sharpe_ratio* resultados_consolidados['Pontos_sharpe_ratio'] + \
    peso_drawdown* resultados_consolidados['Pontos_max_drawdown'] + \
    peso_trades*resultados_consolidados['Pontos_trades']\
)/ (peso_annual_return+peso_sharpe_ratio+peso_drawdown+peso_trades)

folder_path = f'simulações_aplicadas_a_ativos/'
# file_name_resultado_cenário = f'{folder_path}/resultados_consolidados.csv'
# resultados_consolidados.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")


# # Ordenando o DataFrame pelos valores das colunas na sequência especificada
# resultados_consolidados = resultados_consolidados.sort_values(by=colunas_ordenacao)

# # Salvando o DataFrame em um arquivo CSV
# file_name_resultados_consolidados = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_medias.csv'
# resultados_consolidados.to_csv(file_name_resultados_consolidados, sep=";", decimal=",", index=True, encoding="utf-8")

# -------------------------------------------------------------------------------------------------
# Após calcular os pontos,  armazenar os melhores resultados do cenario_in_sample_1x
# Os melhores resão usados para pautar o próximo cenário (cenario_validacao)
# -------------------------------------------------------------------------------------------------

# Criação do DataFrame para armazenar a média dos 3 cenários simulados para cada conjunto único de parâmetros para cada ativo

media_pontos_ponderados = resultados_consolidados.groupby(
    ['janela_rsi', 'ordem', 'lookback', 'd_max', 'num_pontos', 
     'break_min', 'ppt', 'sl', 'pt', 'ativo']
)['Pontos_ponderados'].mean().reset_index().rename(columns={'Pontos_ponderados': 'media_pontos_ponderados'})

file_name_melhor_resultado_cenário = f'{folder_path}/media_pontos_ponderados.csv'
media_pontos_ponderados.to_csv(file_name_melhor_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")

melhores_resultados_por_ativo_in_sample_1 = media_pontos_ponderados.loc[
    media_pontos_ponderados.groupby('ativo')['media_pontos_ponderados'].idxmax()
].reset_index(drop=True)


file_name_melhor_resultado_cenário = f'{folder_path}/melhores_resultados_consolidados.csv'
melhores_resultados_por_ativo_in_sample_1.to_csv(file_name_melhor_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")

# # Cria o box plot
# plt.figure(figsize=(10, 6))
# resultados_consolidados.boxplot(column='return_ann', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de return_ann por janela_rsi')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi')
# plt.ylabel('return_ann %')

# # Exibir o gráfico
# plt.show()


# # Cria o box plot
# plt.figure(figsize=(10, 6))
# resultados_consolidados.boxplot(column='trades', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de trades por janela_rsi')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi')
# plt.ylabel('número de trades')

# # Exibir o gráfico
# plt.show()


# # Cria o box plot
# plt.figure(figsize=(10, 6))
# resultados_consolidados.boxplot(column='sharpe_ratio', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de sharpe_ratio por janela_rsi')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi')
# plt.ylabel('número de sharpe_ratio')

# # Exibir o gráfico
# plt.show()


# # Cria o box plot
# plt.figure(figsize=(10, 6))
# resultados_consolidados.boxplot(column='max_drawdown', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de max_drawdown por janela_rsi')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi')
# plt.ylabel('número de max_drawdown')

# # Exibir o gráfico
# plt.show()