# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd

# ---------------------------------------------------------------------
#  Eliminando warnings indesejados 
# ---------------------------------------------------------------------

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

# ---------------------------------------------------------------------
#  Importando rotinas
# ---------------------------------------------------------------------

from rotinas_simulacao import processa_simulacao


#---------------------------------------------------------------------
# Setando localidade
#---------------------------------------------------------------------

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#---------------------------------------------------------------------
# Setando variáveis fixas
#---------------------------------------------------------------------

colunas_ordenacao = ['janela_rsi', 'ordem', 'lookback', 'break_min', 'sl', 'pt']

ppt = 6 # pontos para trás checados no rompimento
d_max = 2 # distância máxima que uma reta tem que passar de um ponto para dizer que "passa pelo ponto"
aplicar_log = False # flag se aplica ou não o log antes de calcular o RSI"
imprime_grafico = False # flag se gera ou não os gráficos, só é usado no cenário escolhido (único)
salva_dados = False # flag se gera ou não arquivos, só é usado no cenário escolhido (único)

peso_annual_return = 3
peso_sharpe_ratio = 2
peso_drawdown = 1
peso_trades = 1
num_pontos_vals = [2, 3]

folder_raiz = f'simulações_aplicadas_a_ativos_outros'

indices = { 
    1: "^BVSP",     # Ticker para Ibovespa
    2: "^GSPC",     # Ticker para S&P 500
    3: "^FTSE",     # Ticker para FTSE 100
    4: "^IXIC",     # Ticker para NASDAQ
    5: "PETR4.SA",  # Ticker para Petrobras
    6: "VALE3.SA",  # Ticker para Vale
    7: "ITUB",      # Ticker para Itaú Unibanco
    8: "KLBN3.SA",     # Ticker para Banco do Brasil
    9: "BRLUSD=X",  # Ticker para BRL
    10: "EURUSD=X",  # Ticker para Euro
    11: "JPYUSD=X",  # Ticker para BRL
    12: "CNYUSD=X",  # Ticker para YUAN
}

# ----------------------------------------------------------------------------
#  Faz as simulações primeiro, num_pontos a num_pontos, depois ativo a ativo
# ----------------------------------------------------------------------------

ativo_vals = range(8,9)


for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")

#     # ---------------------------------------------------------------------
#     #  Primeiro o cenario_in_sample_1x 
#     # ---------------------------------------------------------------------

    cenario_in_sample_1x = [ 1, 2, 3]
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

                start_date = "2000-03-01"
                end_date = "2005-08-19"
                break_min_vals = [2, 3]
                lookback_vals = [50, 100]
                janela_rsi_vals = [21, 28, 35, 42, 49]
                ordem_vals = [2, 3]
                sl_vals = [0.02]
                pt_vals = [0.05]
                tipo_intervalo = f'in_sample_1_1x'

            case 2: # ------------ Bloco in_sample_2_1x ----------------------------------

                start_date = "2008-01-1"
                end_date = "2013-10-29"
                break_min_vals = [2, 3]
                lookback_vals = [50, 100]
                janela_rsi_vals = [21, 28, 35, 42, 49]
                ordem_vals = [2, 3]
                sl_vals = [0.02]
                pt_vals = [0.05]
                tipo_intervalo =f'in_sample_2_1x'

            case 3: # ------------ Bloco in_sample_3_1x ----------------------------------

                start_date = "2016-04-29"
                end_date = "2019-09-18"
                break_min_vals = [2, 3]
                lookback_vals = [50, 100]
                janela_rsi_vals = [21, 28, 35, 42, 49]
                ordem_vals = [2, 3]
                sl_vals = [0.02]
                pt_vals = [0.05]
                tipo_intervalo =f'in_sample_3_1x'

        print(f'Começando os testes no intervalo {tipo_intervalo} ---------------------------------------------------------')

        resultado_simulado = processa_simulacao(ticker,  # executa a simulação e guarda no dataframe
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
            folder_raiz)
                
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

    folder_path = f'{folder_raiz}/{ticker_clean}'
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
    # Os melhores serão usados para pautar o próximo cenário (cenario_validacao)
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

    # Valor de sl que produziu a melhor média e pontuação obtida

    df_melhor_sl_in_sample_1 = resultado_media_in_sample_1x.groupby('sl')['Pontos_ponderados'].mean()
    melhor_sl_in_sample_1 = df_melhor_sl_in_sample_1.idxmax()
    media_melhor_sl_in_sample_1 = df_melhor_sl_in_sample_1.max()
    nova_linha = {
        'ativo': ticker_clean,
        'cenario': 'cenario_in_sample_1x',
        'variavel': 'sl',
        'melhor_valor': melhor_sl_in_sample_1,
        'media_de_pontos': media_melhor_sl_in_sample_1,
    }

    melhores_resultados_cenario_in_sample_1x = pd.concat(
        [melhores_resultados_cenario_in_sample_1x, pd.DataFrame([nova_linha])],
        ignore_index=True
    )

    # Valor de pt que produziu a melhor média e pontuação obtida

    df_melhor_pt_in_sample_1 = resultado_media_in_sample_1x.groupby('pt')['Pontos_ponderados'].mean()
    melhor_pt_in_sample_1 = df_melhor_pt_in_sample_1.idxmax()
    media_melhor_pt_in_sample_1 = df_melhor_pt_in_sample_1.max()
    nova_linha = {
        'ativo': ticker_clean,
        'cenario': 'cenario_in_sample_1x',
        'variavel': 'pt',
        'melhor_valor': melhor_pt_in_sample_1,
        'media_de_pontos': media_melhor_pt_in_sample_1,
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

    # Se carregar os dados do arquivo ---------------------------------------------

    # folder_path_melhores_resultados = f'{folder_raiz}_in_sample_resultados'
    # file_name_melhores_resultados = f'{folder_path_melhores_resultados}/melhores_resultados_consolidados.csv'
    # melhores_resultados = pd.read_csv(file_name_melhores_resultados, sep=";", decimal=",", index_col=0, encoding="utf-8")

    # melhor_break_min_in_sample_1 =  melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'break_min'].values[0]
    # melhor_janela_rsi_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'janela_rsi'].values[0]
    # melhor_ordem_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'ordem'].values[0]
    # melhor_num_pontos_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'num_pontos'].values[0]
    # melhor_lookback_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'lookback'].values[0]
    # melhor_sl_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'sl'].values[0]
    # melhor_pt_in_sample_1 = melhores_resultados.loc[melhores_resultados['ativo'] == ticker_clean, 'pt'].values[0]


    #  Com os resultados do cenario_in_sample_1x, vamos especificar os parâmetros do cenario_validacao

    break_min_vals = [melhor_break_min_in_sample_1]
    janela_rsi_vals = [melhor_janela_rsi_in_sample_1]
    ordem_vals = [melhor_ordem_in_sample_1]
    num_pontos_vals = [melhor_num_pontos_in_sample_1]

    if melhor_lookback_in_sample_1 == 50:
        lookback_vals = [50, 60, 70]
    else:
        lookback_vals = [80, 90, 100]


    if melhor_sl_in_sample_1 == 0.02:
        sl_vals = [0.01, 0.02, 0.03]
    else:
        sl_vals = [0.04, 0.05, 0.06]

    if melhor_pt_in_sample_1 == 0.05:
        pt_vals = [0.05, 0.06, 0.07]
    else:
        pt_vals = [0.08, 0.10, 0.12]
    

    cenario_validacao = [4, 5, 6, 7, 8]
    cenarios_simulados = cenario_validacao

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

                start_date = "2000-01-01"
                end_date = "2005-08-19"
                tipo_intervalo = f'in_sample_1_2x'


            case 5: # ------------ Bloco in_sample_2_2x ----------------------------------

                start_date = "2008-01-15"
                end_date = "2013-10-29"
                tipo_intervalo = f'in_sample_2_2x'

            case 6: # ------------ Bloco in_sample_3_2x ----------------------------------

                start_date = "2016-04-29"
                end_date = "2019-09-18"
                tipo_intervalo = f'in_sample_3_2x'


            case 7: # ------------ Bloco out_of_sample_val_1 ----------------------------------

                start_date = "2005-10-26"
                end_date = "2007-03-02"
                tipo_intervalo = f'out_of_sample_val_1'


            case 8: # ------------ Bloco out_of_sample_val_2 ----------------------------------

                start_date = "2019-03-06"
                end_date = "2021-09-17"
                tipo_intervalo = f'out_of_sample_val_2'


        print(f'Começando os testes no intervalo {tipo_intervalo} ---------------------------------------------------------')

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
            folder_raiz)
                
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

    folder_path = f'{folder_raiz}/{ticker_clean}'

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

    # # Salvando o melhor resultado do cenario_validacao para  ativo sendo simulado
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
    melhor_num_pontos = melhor_resultado_cenario_validacao.iloc[0]['num_pontos']
    melhor_sl = melhor_resultado_cenario_validacao.iloc[0]['sl']
    melhor_pt = melhor_resultado_cenario_validacao.iloc[0]['pt']


    #  Com os resultados do cenario_validação, vamos especificar os parâmetros do cenario_validacao

    janela_rsi_vals = [melhor_janela_rsi]
    ordem_vals = [melhor_ordem]
    lookback_vals = [melhor_lookback]
    break_min_vals = [melhor_break_min]
    num_pontos = [melhor_num_pontos]
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


    for cenario in cenarios_simulados:  # Roda os cenários previstos em cenario_in_sample_1x

        match cenario:
            
            case 9: # ------------ Bloco out_of_sample_final_1 ----------------------------------

                start_date = "2002-03-05"
                end_date = "2005-10-26"
                tipo_intervalo = f'out_of_sample_final_1'

            case 10: # ------------ Bloco out_of_sample_final_2 ----------------------------------

                start_date = "2021-09-18" 	
                end_date = "2024-11-01"
                tipo_intervalo = f'out_of_sample_final_2'
        
        print(f'Começando os testes no intervalo {tipo_intervalo} ---------------------------------------------------------')

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
            folder_raiz)
                
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

    folder_path = f'{folder_raiz}/{ticker_clean}'
    file_name_resultado_cenário = f'{folder_path}/{ticker_clean}_{cenarios_simulados}_cenario_final_resultados.csv'
    resultados_cenario_final.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")

    # Carrega o arquivo com os resultados acumulados existente por ativo e intervalo

    file_name_resultados = f'{folder_raiz}/resultados_finais_acumulados_por_ativo_intervalo.csv' 
    resultados_existentes = pd.read_csv(file_name_resultados, sep=";", decimal=",", index_col=0, encoding="utf-8")

    # Se certifica de que o pandas interpreta as colunas relevantes como float antes de concatenar

    resultados_existentes['return_ann'] = pd.to_numeric(resultados_existentes['return_ann'], errors='coerce').astype(float)
    resultados_existentes['sharpe_ratio'] = pd.to_numeric(resultados_existentes['sharpe_ratio'], errors='coerce').astype(float)
    resultados_existentes['max_drawdown'] = pd.to_numeric(resultados_existentes['max_drawdown'], errors='coerce').astype(float)
    resultados_existentes['trades'] = pd.to_numeric(resultados_existentes['trades'], errors='coerce').astype(float)

    # Adiciona os novos resultados
    resultados_atualizados = pd.concat([resultados_existentes, resultados_cenario_final])

    # Salva o DataFrame atualizado no mesmo arquivo
    resultados_atualizados.to_csv(file_name_resultados, sep=";", decimal=",", index=True, encoding="utf-8")

    # -------------------------------------------------------------------------------------------------
    # Após calcular os pontos, armazena os melhores resultados do cenario_validacao
    # O melhores cenario será usado para pautar o cenário_final
    # -------------------------------------------------------------------------------------------------

    # Carrega o arquivo com os resultados acumulados existente por ativo e intervalo

    file_name_resultados = f'{folder_raiz}/resultados_finais_acumulados_por_ativo.csv' 
    resultados_existentes = pd.read_csv(file_name_resultados, sep=";", decimal=",", index_col=0, encoding="utf-8")

    # Se certifica de que o pandas interpreta as colunas relevantes como float antes de concatenar

    resultados_existentes['return_ann'] = pd.to_numeric(resultados_existentes['return_ann'], errors='coerce').astype(float)
    resultados_existentes['sharpe_ratio'] = pd.to_numeric(resultados_existentes['sharpe_ratio'], errors='coerce').astype(float)
    resultados_existentes['max_drawdown'] = pd.to_numeric(resultados_existentes['max_drawdown'], errors='coerce').astype(float)
    resultados_existentes['trades'] = pd.to_numeric(resultados_existentes['trades'], errors='coerce').astype(float)

    # # Colunas para agrupamento
    
    colunas_agrupamento = [
        'janela_rsi', 'ordem', 'lookback', 'd_max', 'num_pontos',
        'break_min', 'ppt', 'sl', 'pt', 'ativo'
    ]

    # Colunas para calcular a média
    colunas_media = ['return_ann', 'sharpe_ratio', 'max_drawdown', 'trades']

    # Adiciona os novos resultados já com as médias
    resultados_atualizados = pd.concat([resultados_existentes, resultados_cenario_final.groupby(colunas_agrupamento, as_index=False)[colunas_media].mean()])
    resultados_atualizados['cenario'] = 'Media dos resultados por ativo'

    # Salva o DataFrame atualizado no mesmo arquivo
    resultados_atualizados.to_csv(file_name_resultados, sep=";", decimal=",", index=True, encoding="utf-8")