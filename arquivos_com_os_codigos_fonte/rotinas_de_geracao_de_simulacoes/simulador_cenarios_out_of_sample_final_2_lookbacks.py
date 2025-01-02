# ------------------------------------------------------------------------
# A rotina simula_cenarios_out_of_sample_validacao simula a segunda fase 
# e salva os resultados em um folder com o nome indicado pelas variá-
# veis escolhidas na simulação.
#
# A rotina assume que dois passos anteriores foram tomados:
#   1) os cenários in_sample para os ativos escolhidos
#   foram gerados anteriormente pela rotina simula_cenarios_in_sample
#   e 
#   2) os resultados foram consolidados a partir da rotina
#   consolidacao_de_resultados_in_sample aplicados ao 
#   folder criado pelo passo 1 
# 
# Com os dois passos acima, um arquivo chamado melhores_resultados.csv terá sido
# criado no folder simulacoes_realizadas/simulacoes_in_sample
# 
# É a partir desse arquivo que os parâmetros serão escolhidos para a segunda fase
#
# Para salvar os resultados da validacao, um folder chamado
# simulacoes_realizadas/simulacoes_out_of_sample_validacao é criado
# 
# Dentro desse folder, para cada ativo, é criado um folder com o nome do ativo.
# Dentro de cada folder de cada ativo são salvos 3 arquivos .csv:
#   1) nome_do_ativo_cenario_validacao_resultados.csv
#   2) nome_do_ativo_cenario_validacao_medias.csv.csv
#   3) nome_do_ativo_cenario_validacao_melhor_resultado.csv
#
# ------------------------------------------------------------------------
#
# Em seguida, dentro do loop de cada ativo, faz-se a simulação final
# utilizando-se o parâmetros com os melhores resultados da fase validacao
# para os intervalos out_of_sample_final_1 e out_of_sample_final_2
#
# Para salvar os resultados finais, um folder chamado
# simulacoes_realizadas/simulacoes_out_of_sample_final é criado
#
# Dentro desse folder, para cada ativo, é criado um folder com o nome do ativo.
# Dentro do folder de cada ativo, são salvos 2 arquivos .csv:
#   1) nome_do_ativo_cenario_final_resultados.csv
#   2) nome_do_ativo_cenario_final_resultados_media_por_ativo.csv
#
# ------------------------------------------------------------------------
# Ao final de cada uma das fases, deve-se consolidar os resultados
#
# O motivo pelo qual não consolidamos os resultados de todos os ativos
# ma medida em que os cenários são produzidos é porque as simulações
# podem ocorrer em paralelo por mais de um computador para diferentes
# sub-grupos de ativos.
#
# Por isso foi criada uma rotina que consolida todos os resultados
# out_of_sample_validacao: consolidacao_de_resultados_validacao.py
# e outra para os resultados out_of_sample_finais:
# consolidacao_de_resultados_validacao.py
#
# A consolidação só deve acontecer quando todos os ativos tiverem sido
# simulados#
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

from arquivos_com_os_codigos_fonte.rotinas_da_metodologia.simulacao_cenario_individual_2_lookbacks import processa_simulacao_dois_lookbacks
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

#---------------------------------------------------------------------
# Setando as variáveis da simulação desejada
#---------------------------------------------------------------------

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
    55: "ITUB",      # Ticker para Vale
}

ativo_vals = range(1,51)

# atribuição dos intervalos pré-definidos em sorteio

start_date_in_sample_1 = "2000-01-01"
end_date_in_sample_1 = "2005-08-19"

start_date_in_sample_2 = "2008-01-15"
end_date_in_sample_2 = "2013-10-29"

start_date_in_sample_3 = "2016-04-29"
end_date_in_sample_3 = "2019-09-18"

start_date_out_of_sample_validacao_1 = "2005-10-26"
end_date_out_of_sample_validacao_1 = "2007-03-02"

start_date_out_of_sample_validacao_2 = "2019-03-06"
end_date_out_of_sample_validacao_2 = "2021-09-17"

start_date_out_of_sample_final_1 = "2002-03-05"
end_date_out_of_sample_final_1 = "2005-10-26"

start_date_out_of_sample_final_2 = "2021-09-18" 	
end_date_out_of_sample_final_2 = "2024-11-01"

cenarios_validacao = [4, 5, 6, 7, 8]

cenarios_simulados = cenarios_validacao


# ----------------------------------------------------------------------------
#  Importando as variáveis com os melhores resultados out_of_sample_validacao
# ----------------------------------------------------------------------------

folder_path_melhores_resultados = f'simulacoes_realizadas/simulacoes_out_of_sample_validacao'
file_name_melhores_resultados = f'{folder_path_melhores_resultados}/resultados_consolidados_validacao_melhores_medias.csv'
melhores_resultados = pd.read_csv(file_name_melhores_resultados, sep=";", decimal=",", index_col=0, encoding="utf-8")

# --------------------------------------------------------------------------------------------------
#  Aqui começa a loop para cada ativo
# --------------------------------------------------------------------------------------------------

for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")

    folder_path = f'simulacoes_realizadas/simulacoes_out_of_sample_final_2_lookbacks/{ticker_clean}'

    # Verifica se o diretório já existe; se não, cria
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # --------------------------------------------------------------------------------------------------
    #  Aqui começa a simulação final
    # --------------------------------------------------------------------------------------------------

    # Usando valores obtidos no cenário validacao

    melhor_janela_rsi = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'janela_rsi'].iloc[0]
    melhor_ordem = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'ordem'].iloc[0]
    melhor_lookback = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'lookback'].iloc[0]
    melhor_break_min = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'break_min'].iloc[0]
    melhor_num_pontos = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'num_pontos'].iloc[0]
    melhor_sl = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'sl'].iloc[0]
    melhor_pt = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'pt'].iloc[0]


    #  Com os resultados do cenario_validação, vamos especificar os parâmetros do cenario_validacao

    janela_rsi_vals = [melhor_janela_rsi]
    ordem_vals = [melhor_ordem]
    lookback_vals = [melhor_lookback, melhor_lookback + 40]
    break_min_vals = [melhor_break_min]
    num_pontos_vals = [melhor_num_pontos]
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


    for cenario in cenarios_simulados:  # Roda os cenários previstos em cenario_out_of_sample_validacao

        match cenario:
            
            case 9: # ------------ Bloco out_of_sample_final_1 ----------------------------------

                start_date = start_date_out_of_sample_final_1
                end_date = end_date_out_of_sample_final_1
                tipo_intervalo = f'out_of_sample_final_1'

            case 10: # ------------ Bloco out_of_sample_final_2 ----------------------------------

                start_date = start_date_out_of_sample_final_2
                end_date = end_date_out_of_sample_final_2
                tipo_intervalo = f'out_of_sample_final_2'

        resultado_simulado = processa_simulacao_dois_lookbacks(ticker,
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

    file_name_resultado_cenário = f'{folder_path}/{ticker_clean}_cenario_final_resultados.csv'
    resultados_cenario_final.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")

    # Colunas para agrupamento
    
    colunas_agrupamento = [
        'janela_rsi', 'ordem', 'lookback', 'd_max', 'num_pontos',
        'break_min', 'ppt', 'sl', 'pt', 'ativo'
    ]

    # Colunas para calcular a média
    colunas_media = ['return_ann', 'sharpe_ratio', 'max_drawdown', 'trades']

    # Adiciona os novos resultados já com as médias
    resultados_final_medias = resultados_cenario_final.groupby(colunas_agrupamento, as_index=False)[colunas_media].mean()
    resultados_final_medias['cenario'] = 'Media_dos_resultados_por_ativo'

    # Salva o DataFrame atualizado no mesmo arquivo
    file_name_medias_resultado_final = f'{folder_path}/{ticker_clean}_cenario_final_resultados_media_por_ativo.csv'
    resultados_final_medias.to_csv(file_name_medias_resultado_final, sep=";", decimal=",", index=True, encoding="utf-8")