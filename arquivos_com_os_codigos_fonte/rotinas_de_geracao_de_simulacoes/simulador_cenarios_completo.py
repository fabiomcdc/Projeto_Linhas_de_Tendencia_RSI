# ------------------------------------------------------------------------
# A rotina simulador_cenario_individual_completo simula todas as fases
# em sequência: in_sample=>out_of_sample_validacao=>out_of_sample_final
# e salva os resultados em um único folder com o nome do ativo
# qualificado pela variáveis escolhidas na simulação.
# 
# Exemplo =>CSCO_np_1_rsi_14_21_28_35_42_49_56_63_ord_2_bm_3_lb_50
#
# Esses valores são escolhidos para a fase in_sample
#
# ------------------------------------------------------------------------
#
# Dentro do folder criado salvos 3 arquivos .csv na fase in_sample
# 1) nome_do_ativo_cenario_in_sample_1x_resultados.csv
# 2) nome_do_ativo_cenario_in_sample_1x_medias.csv
# 3) nome_do_ativo_cenario_in_sample_1x_melhores_resultados.csv
#
# ------------------------------------------------------------------------
#
# Dentro do folder criado salvos 3 arquivos .csv na fase
# out_of_sample_validacao:
# 1) nome_do_ativo_cenario_validacao_resultados.csv
# 2) nome_do_ativo_cenario_validacao_medias.csv.csv
# 3) nome_do_ativo_cenario_validacao_melhor_resultado.csv
#
# ------------------------------------------------------------------------
#
# Dentro do folder criado salvos 2 arquivos .csv na fase
# out_of_sample_final:
# 1) nome_do_ativo_cenario_final_resultados.csv
# 2) nome_do_ativo_cenario_final_resultados_media_por_ativo.csv
#
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

ativo_vals = range(1,2)

# ---------------------------------------------------------------------
#  Faz as simulações ativo a ativo
# ---------------------------------------------------------------------

folder_path_raiz = f'simulacoes_individuais/'

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

cenario_in_sample_1x = [ 1, 2, 3 ]
cenarios_validacao = [4, 5, 6, 7, 8]

# atribuição dos valores aos parâmetros que serão simulados

num_pontos_vals = [2] 
janela_rsi_vals = [14, 21, 28, 35, 42, 49, 56, 63]
break_min_vals = [3]
lookback_vals = [50]
ordem_vals = [1]
sl_vals = [0.02]
pt_vals = [0.05]


# construção do nome do folder em que os resultados da simulação
# escolhida serão armazenados

nome_simulacao = f''

nome_simulacao = f'{nome_simulacao}_np'
for np in num_pontos_vals:
    nome_simulacao = f'{nome_simulacao}_{np}'

nome_simulacao = f'{nome_simulacao}_rsi'
for j_rsi in janela_rsi_vals:
    nome_simulacao = f'{nome_simulacao}_{j_rsi}'

nome_simulacao = f'{nome_simulacao}_ord'
for ord in ordem_vals:
    nome_simulacao = f'{nome_simulacao}_{ord}'

nome_simulacao = f'{nome_simulacao}_bm'
for bm in break_min_vals:
    nome_simulacao = f'{nome_simulacao}_{bm}'

nome_simulacao = f'{nome_simulacao}_lb'
for lb in lookback_vals:
    nome_simulacao = f'{nome_simulacao}_{lb}'

for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")

    folder_path = f'{folder_path_raiz}/{ticker_clean}{nome_simulacao}'

    # Verifica se o diretório já existe; se não, cria
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # ---------------------------------------------------------------------
    #  Simulação do cenario_in_sample_1x
    # ---------------------------------------------------------------------


    cenarios_simulados = cenario_in_sample_1x

    # Criação do DataFrame para armazenar os resultados do cenario_in_sample_1x do ativo sendo simulado
    resultados_cenario_in_sample_1x = pd.DataFrame(columns=[
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

                
        # Iterando pelos itens do resultado_simulado para salvar no dataframe que junta todo
        # os resultados do cenário in_sample_1

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
            resultados_cenario_in_sample_1x = pd.concat(
                [resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
                ignore_index=True
            )
    
    # Antes de avançar e salvar os resultados, vamos garantir que a coluna trades tenha valores numéricos

    resultados_cenario_in_sample_1x['trades'] = pd.to_numeric(resultados_cenario_in_sample_1x['trades'], errors='coerce').astype(float)

    # Salva o arquivo com os resultados de resultados_cenario_in_sample_1x

    file_name_resultado_cenário = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_resultados.csv'
    resultados_cenario_in_sample_1x.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")


    # -------------------------------------------------------------------------------------------------
    # Após se acumular no dataframe resultados_cenario_in_sample_1x todos os cenários previstos
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
        resultados_cenario_in_sample_1x.groupby(colunas_agrupamento, as_index=False)[colunas_media]
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
    file_name_resultado_media_in_sample_1x = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_medias.csv'
    resultado_media_in_sample_1x.to_csv(file_name_resultado_media_in_sample_1x, sep=";", decimal=",", index=True, encoding="utf-8")

    # -------------------------------------------------------------------------------------------------
    # Após calcular os pontos,  armazenar os melhores resultados do cenario_in_sample_1x
    # Os melhores resão usados para pautar o próximo cenário (cenario_validacao)
    # -------------------------------------------------------------------------------------------------

    # Criação do DataFrame para armazenar os melhores resultados do cenario_in_sample_1x do ativo sendo simulado
    melhores_resultados_cenario_in_sample_1x = pd.DataFrame(columns=[
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

    melhores_resultados_cenario_in_sample_1x = pd.concat(
        [melhores_resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
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

    melhores_resultados_cenario_in_sample_1x = pd.concat(
        [melhores_resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
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

    melhores_resultados_cenario_in_sample_1x = pd.concat(
        [melhores_resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
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

    melhores_resultados_cenario_in_sample_1x = pd.concat(
        [melhores_resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
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

    melhores_resultados_cenario_in_sample_1x = pd.concat(
        [melhores_resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
        ignore_index=True
    )

    # Salvando os melhores valores dos parâmetros
    file_name_resultado_media_in_sample_1x = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_melhores_resultados.csv'
    melhores_resultados_cenario_in_sample_1x.to_csv(file_name_resultado_media_in_sample_1x, sep=";", decimal=",", index=True, encoding="utf-8")





    # --------------------------------------------------------------------------------------------------
    #  Aqui começa a simulação de validação
    # --------------------------------------------------------------------------------------------------


    melhor_janela_rsi_in_sample_1 = melhores_resultados_cenario_in_sample_1x.loc[
        (melhores_resultados_cenario_in_sample_1x['ativo'] == ticker_clean) & (melhores_resultados_cenario_in_sample_1x['variavel'] == 'janela_rsi'),
        'melhor_valor'
    ].values[0]


    melhor_ordem_in_sample_1 = melhores_resultados_cenario_in_sample_1x.loc[
        (melhores_resultados_cenario_in_sample_1x['ativo'] == ticker_clean) & (melhores_resultados_cenario_in_sample_1x['variavel'] == 'ordem'),
        'melhor_valor'
    ].values[0]


    melhor_lookback_in_sample_1 = melhores_resultados_cenario_in_sample_1x.loc[
        (melhores_resultados_cenario_in_sample_1x['ativo'] == ticker_clean) & (melhores_resultados_cenario_in_sample_1x['variavel'] == 'lookback'),
        'melhor_valor'
    ].values[0]


    melhor_break_min_in_sample_1 = melhores_resultados_cenario_in_sample_1x.loc[
        (melhores_resultados_cenario_in_sample_1x['ativo'] == ticker_clean) & (melhores_resultados_cenario_in_sample_1x['variavel'] == 'break_min'),
        'melhor_valor'
        ].values[0]


    melhor_num_pontos_in_sample_1 = melhores_resultados_cenario_in_sample_1x.loc[
        (melhores_resultados_cenario_in_sample_1x['ativo'] == ticker_clean) & (melhores_resultados_cenario_in_sample_1x['variavel'] == 'num_pontos'),
        'melhor_valor'
    ].values[0]



    #  Com os resultados do cenario_in_sample_1x, vamos especificar os parâmetros do cenario_validacao

    break_min_vals = [melhor_break_min_in_sample_1]
    janela_rsi_vals = [melhor_janela_rsi_in_sample_1]
    ordem_vals = [melhor_ordem_in_sample_1]
    lookback_vals = [50, 60, 70]
    sl_vals = [0.01, 0.02, 0.03]
    pt_vals = [0.05, 0.06, 0.07]

    cenarios_simulados = cenarios_validacao

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

                start_date = start_date_in_sample_1
                end_date = end_date_in_sample_1
                tipo_intervalo = f'in_sample_1_2x'


            case 5: # ------------ Bloco in_sample_2_2x ----------------------------------

                start_date = start_date_in_sample_2
                end_date = end_date_in_sample_2
                tipo_intervalo = f'in_sample_2_2x'

            case 6: # ------------ Bloco in_sample_3_2x ----------------------------------

                start_date = start_date_in_sample_3
                end_date = end_date_in_sample_3
                tipo_intervalo = f'in_sample_3_2x'


            case 7: # ------------ Bloco out_of_sample_val_1 ----------------------------------

                start_date = start_date_out_of_sample_validacao_1
                end_date = end_date_out_of_sample_validacao_1
                tipo_intervalo = f'out_of_sample_val_1'


            case 8: # ------------ Bloco out_of_sample_val_2 ----------------------------------

                start_date = start_date_out_of_sample_validacao_2
                end_date = end_date_out_of_sample_validacao_2
                tipo_intervalo = f'out_of_sample_val_2'

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

    # Salvando o melhor resultado do cenario_validacao para  ativo sendo simulado
    file_name_resultado_media_validacao = f'{folder_path}/{ticker_clean}_cenario_validacao_melhor_resultado.csv'
    melhor_resultado_cenario_validacao.to_csv(file_name_resultado_media_validacao, sep=";", decimal=",", index=True, encoding="utf-8")



    # --------------------------------------------------------------------------------------------------
    #  Aqui começa a simulação final
    # --------------------------------------------------------------------------------------------------

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



    
    # Salva o arquivo com os resultados para esse ativo
    file_name_resultado_cenário = f'{folder_path}/{ticker_clean}_cenario_final_resultados.csv'
    resultados_cenario_final.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")

    # # Colunas para agrupamento
    
    colunas_agrupamento = [
        'janela_rsi', 'ordem', 'lookback', 'd_max', 'num_pontos',
        'break_min', 'ppt', 'sl', 'pt', 'ativo'
    ]

    # Colunas para calcular a média
    colunas_media = ['return_ann', 'sharpe_ratio', 'max_drawdown', 'trades']

    # Adiciona os novos resultados já com as médias
    resultados_atualizados = resultados_cenario_final.groupby(colunas_agrupamento, as_index=False)[colunas_media].mean()
    resultados_atualizados['cenario'] = 'Media dos resultados por ativo'

    # Salva o DataFrame atualizado no mesmo arquivo
    file_name_medias_resultado_final = f'{folder_path}/{ticker_clean}_cenario_final_resultados_media_por_ativo.csv'
    resultados_atualizados.to_csv(file_name_medias_resultado_final, sep=";", decimal=",", index=True, encoding="utf-8")