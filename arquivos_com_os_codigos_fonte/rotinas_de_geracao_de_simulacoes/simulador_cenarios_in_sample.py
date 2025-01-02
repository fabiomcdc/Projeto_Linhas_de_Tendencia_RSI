# ------------------------------------------------------------------------
# A rotina simula_cenario_in_sample simula a primeira fase: in_sample 
# e salva os resultados em um folder com o nome indicado pelas variá-
# veis escolhidas na simulação.
# Exemplo => fase_in_sample_np_1_rsi_14_21_28_ord_2_bm_3_4_lb_50_100
# Esses valores são escolhidos 
# 
# Um folder para cada ativo é criado dentro do folder da simulação
# Dentro de cada folder de cada ativo são salvos 3 arquivos .csv
# 1) nome_do_ativo_cenario_in_sample_1x_resultados.csv
# 2) nome_do_ativo_cenario_in_sample_1x_medias.csv
# 3) nome_do_ativo_cenario_in_sample_1x_melhores_resultados.csv
#
# O motivo pelo qual não consolidamos os resultados de todos os ativos
# ma medida em que os cenários são produzidos é porque as simulações
# podem ocorrer em paralelo por mais de um computador para diferentes
# sub-grupos de ativos.
#
# Por isso foi criada uma rotina que consolida todos os resultados
# in sample: consolidacao_de_resultados_in_sample.py
# 
# A consolidação só deve acontecer quando todos os ativos tiverem sido
# simulados
# ------------------------------------------------------------------------

# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import os
import sys
import warnings

# ---------------------------------------------------------------------
# Adiciona o caminho do projeto ao PYTHONPATH
# ---------------------------------------------------------------------

sys.path.append(os.path.abspath(r"C:\Users\User\Dropbox\FGV\Dissertação\Projeto\projeto_linhas_de_tendencia"))
sys.path.append(os.path.abspath(r"C:\Users\fabio\Dropbox\FGV\Dissertação\Projeto\projeto_linhas_de_tendencia"))

# ---------------------------------------------------------------------
#  Eliminando warnings indesejados 
# ---------------------------------------------------------------------

warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

# ---------------------------------------------------------------------
#  Importando rotinas
# ---------------------------------------------------------------------

# from arquivos_com_os_codigos_fonte.rotinas_da_metodologia.gerador_de_sinais_para_um_cenario import simulacao
# from arquivos_com_os_codigos_fonte.rotinas_da_metodologia.classe_estrategia import EstrategiaAdaptada
from arquivos_com_os_codigos_fonte.rotinas_da_metodologia.simulacao_cenario_individual import processa_simulacao


#---------------------------------------------------------------------
# Setando localidade
#---------------------------------------------------------------------

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#---------------------------------------------------------------------
# Setando variáveis fixas
#---------------------------------------------------------------------

colunas_ordenacao = ['janela_rsi', 'ordem', 'lookback', 'break_min', 'sl', 'pt']

# pontos para trás checados no rompimento
ppt = 6

# distância máxima que uma reta tem que passar de um ponto para dizer que "passa pelo ponto"
d_max = 2

# flag se aplica ou não o log antes de calcular o RSI"
aplicar_log = False 

# flag se gera ou não os gráficos, só é usado no cenário escolhido (único)
imprime_grafico = False

# flag se gera ou não arquivos, só é usado no cenário escolhido (único)
salva_dados = False 

# pesos utilizados na formação das notas de avaliação dos parâmetros com melhor performance
peso_annual_return = 3
peso_sharpe_ratio = 2
peso_drawdown = 1
peso_trades = 1

# ---------------------------------------------------------------------
#  Parâmetros setados da simulação desejada
# ---------------------------------------------------------------------

# dicionário de ativos
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
    51: "^BVSP",     # Ticker para Ibovespa
    52: "^GSPC",     # Ticker para S&P 500
    53: "PETR4.SA",  # Ticker para Petrobras
    54: "VALE3.SA",  # Ticker para Vale
    55: "ITUB",      # Ticker para Itaú/Unibanco
}

# escolha de quais ativos do dicionário serão simulados

ativo_vals = range(3,23)

# atribuição dos intervalos pré-definidos em sorteio

start_date_in_sample_1 = "2000-01-01"
end_date_in_sample_1 = "2005-08-19"

start_date_in_sample_2 = "2008-01-15"
end_date_in_sample_2 = "2013-10-29"

start_date_in_sample_3 = "2016-04-29"
end_date_in_sample_3 = "2019-09-18"

cenario_in_sample_1x = [ 1, 2, 3 ]

# atribuição dos valores aos parâmetros que serão simulados

num_pontos_vals = [2, 3] 
janela_rsi_vals = [14, 21, 28, 35, 42, 49, 56, 63]
break_min_vals = [3, 4]
lookback_vals = [50, 100]
ordem_vals = [1]
sl_vals = [0.02]
pt_vals = [0.05]

# construção do nome do folder em que os resultados da simulação
# escolhida serão armazenados

nome_simulação_in_sample = f'simulacoes_realizadas/fase_in_sample'

nome_simulação_in_sample = f'{nome_simulação_in_sample}_np'
for np in num_pontos_vals:
    nome_simulação_in_sample = f'{nome_simulação_in_sample}_{np}'

nome_simulação_in_sample = f'{nome_simulação_in_sample}_rsi'
for j_rsi in janela_rsi_vals:
    nome_simulação_in_sample = f'{nome_simulação_in_sample}_{j_rsi}'

nome_simulação_in_sample = f'{nome_simulação_in_sample}_ord'
for ord in ordem_vals:
    nome_simulação_in_sample = f'{nome_simulação_in_sample}_{ord}'

nome_simulação_in_sample = f'{nome_simulação_in_sample}_bm'
for bm in break_min_vals:
    nome_simulação_in_sample = f'{nome_simulação_in_sample}_{bm}'

nome_simulação_in_sample = f'{nome_simulação_in_sample}_lb'
for lb in lookback_vals:
    nome_simulação_in_sample = f'{nome_simulação_in_sample}_{lb}'

folder_path = f'{nome_simulação_in_sample}'


# ---------------------------------------------------------------------
#  Loop, ativo a ativo, simulando
# ---------------------------------------------------------------------


for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")

    cenarios_simulados = cenario_in_sample_1x

    # Criação do DataFrame para armazenar os resultados do cenario_in_sample_1x do ativo sendo simulado
    resultados_cenario_in_sample = pd.DataFrame(columns=[
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

    
    for cenario in cenarios_simulados:  # Roda os cenários previstos em cenario_in_sample_1x no caso, 1, 2 e 3

        match cenario:

            case 1: # ------------ Bloco in_sample_1_1x ----------------------------------

                start_date = start_date_in_sample_1
                end_date = end_date_in_sample_1
                tipo_intervalo = f'in_sample_1_1x'

            case 2: # ------------ Bloco in_sample_2_1x ----------------------------------

                start_date = start_date_in_sample_2
                end_date = end_date_in_sample_2
                tipo_intervalo =f'in_sample_2_1x'

            case 3: # ------------ Bloco in_sample_3_1x ----------------------------------

                start_date = start_date_in_sample_3
                end_date = end_date_in_sample_3
                tipo_intervalo =f'in_sample_3_1x'
        
        # executa a simulação e guarda no dataframe resultado_simulado
        print(f'Simulando cenario {tipo_intervalo}')

        resultado_simulado = processa_simulacao(ticker,  
            tipo_intervalo,
            start_date,
            end_date,
            break_min_vals,
            janela_rsi_vals,
            ordem_vals,
            lookback_vals,
            num_pontos_vals,
            ppt,
            d_max,
            sl_vals,
            pt_vals,
            aplicar_log,
            imprime_grafico,
            salva_dados,
            folder_path)

                
        # Itera pelos itens do resultado_simulado para salvar no dataframe
        # resultados_cenario_in_sample que junta todo os resultados dos cenarios
        # escolhidos para cada ativo.

        # Os resultados de cada ativo serão usados posteriormente para a atribuição
        # de notas e para a escolha dos valores de parâmetro que tiveram a melhor nota

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
            resultados_cenario_in_sample = pd.concat(
                [resultados_cenario_in_sample, pd.DataFrame([nova_linha])],
                ignore_index=True
            )
    
    # Concluídos todos os cenários (intervalos in_sample)
    # Antes de avançar e salvar os resultados, vamos garantir que a coluna trades tenha valores numéricos

    resultados_cenario_in_sample['trades'] = pd.to_numeric(resultados_cenario_in_sample['trades'], errors='coerce').astype(float)

    # Salva o arquivo com os resultados de resultados_cenario_in_sample para o ativo simulado

    file_name_resultado_cenário = f'{folder_path}/{ticker_clean}/{ticker_clean}_cenario_in_sample_1x_resultados.csv'
    resultados_cenario_in_sample.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")


    # -------------------------------------------------------------------------------------------------
    # Após se acumular no dataframe resultados_cenario_in_sample todos os cenários previstos
    # Vamos obter a média dos itens 'return_ann', 'sharpe_ratio', 'max_drawdown', 'trades'
    # -------------------------------------------------------------------------------------------------

    colunas_agrupamento = [
        'janela_rsi', 'ordem', 'lookback', 'd_max', 'num_pontos',
        'break_min', 'ppt', 'sl', 'pt', 'ativo'
    ]

    # Colunas para calcular a média
    colunas_media = ['return_ann', 'sharpe_ratio', 'max_drawdown', 'trades']

    # Com isso, o dataframe resultado_media_in_sample_1x tem, para os diferentes cenários, as médias obtidas

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
    
    # Ordenando o DataFrame pelos valores das colunas na sequência especificada
    resultado_media_in_sample_1x = resultado_media_in_sample_1x.sort_values(by=colunas_ordenacao)

    # Salvando o DataFrame em um arquivo CSV
    file_name_resultado_media_in_sample_1x = f'{folder_path}/{ticker_clean}/{ticker_clean}_cenario_in_sample_1x_medias.csv'
    resultado_media_in_sample_1x.to_csv(file_name_resultado_media_in_sample_1x, sep=";", decimal=",", index=True, encoding="utf-8")

    # -------------------------------------------------------------------------------------------------
    # Após calcular os pontos, vamos armazenar os melhores resultados do cenario_in_sample_1x
    # Os par6ametros com os melhores resultados sersão usados para pautar 
    # o próximo cenário (cenario_validacao)
    # -------------------------------------------------------------------------------------------------

    # Criação do DataFrame para armazenar os melhores resultados do cenario_in_sample_1x do ativo sendo simulado
    melhores_resultados_cenario_in_sample = pd.DataFrame(columns=[
        'ativo',
        'cenario',
        'variavel',
        'melhor_valor',
        'media_de_pontos',
    ])

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

    # Salvando os melhores valores dos parâmetros

    file_name_resultado_media_in_sample_1x = f'{folder_path}/{ticker_clean}/{ticker_clean}_cenario_in_sample_1x_melhores_resultados.csv'
    melhores_resultados_cenario_in_sample.to_csv(file_name_resultado_media_in_sample_1x, sep=";", decimal=",", index=True, encoding="utf-8")