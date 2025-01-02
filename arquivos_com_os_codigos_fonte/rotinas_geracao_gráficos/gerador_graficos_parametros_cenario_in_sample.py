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

# # ---------------------------------------------------------------------
# #  Faz a consolidação ativo a ativo
# # ---------------------------------------------------------------------

# ativo_vals = range(1,51)

# # Criação do DataFrame para armazenar os resultados do cenario_in_sample_1x do ativo sendo simulado
# resultados_consolidados = pd.DataFrame(columns=[
#     'num_pontos',
#     'janela_rsi',
#     'ordem',
#     'lookback',
#     'break_min',
#     'd_max',
#     'ppt',
#     'sl',
#     'pt',
#     'ativo',
#     'cenario',
#     'return_ann',
#     'sharpe_ratio',
#     'max_drawdown',
#     'trades'
# ])

# tipo_intervalo = "in_sample_1"

# for ativo in ativo_vals: # aqui começa o loop ativo a ativo

#     ticker = indices.get(ativo)
#     ticker_clean = ticker.replace("^", "")


#     # simulações_aplicadas_a_ativos_RSI de 28 35 42 49 ---------------------------------------------------------
    
#     folder_path = f'simulações_aplicadas_a_ativos_in_sample_parte_6/{ticker_clean}'
#     file_name = f'{folder_path}/{ticker_clean}_cenario_in_sample_1x_resultados.csv'

#     print("Carregando  ,", file_name)

#     resultados_do_ativo_df = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")

#     for _, row in resultados_do_ativo_df.iterrows():

#         # Criação de uma nova linha com os dados extraídos de cada linha do DataFrame
#         nova_linha = {
#             'num_pontos': row['num_pontos'],
#             'janela_rsi': row['janela_rsi'],
#             'ordem': row['ordem'],
#             'lookback': row['lookback'],
#             'break_min': row['break_min'],
#             'd_max': row['d_max'],
#             'ppt': row['ppt'],
#             'sl': row['sl'],
#             'pt': row['pt'],
#             'ativo': row['ativo'],
#             'cenario': row['cenario'],
#             'return_ann': row['return_ann'],
#             'sharpe_ratio': row['sharpe_ratio'],
#             'max_drawdown': row['max_drawdown'],
#             'trades': row['trades'],
#         }
#         # Adicionando a nova linha ao DataFrame
#         resultados_consolidados = pd.concat(
#             [resultados_consolidados, pd.DataFrame([nova_linha])],
#             ignore_index=True
#         )


# # simulações_aplicadas_a_ativos_RSI de 56 e 63  --------------------------------------------------

# folder_path = f'simulações_aplicadas_a_ativos_in_sample_resultados'
# file_name = f'{folder_path}/resultados_in_sample_final_parcial.csv'
# print("Carregando  ,", file_name)

# resultados_do_ativo_df = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")

# for _, row in resultados_do_ativo_df.iterrows():

#     # Criação de uma nova linha com os dados extraídos de cada linha do DataFrame
#     nova_linha = {
#         'num_pontos': row['num_pontos'],
#         'janela_rsi': row['janela_rsi'],
#         'ordem': row['ordem'],
#         'lookback': row['lookback'],
#         'break_min': row['break_min'],
#         'd_max': row['d_max'],
#         'ppt': row['ppt'],
#         'sl': row['sl'],
#         'pt': row['pt'],
#         'ativo': row['ativo'],
#         'cenario': row['cenario'],
#         'return_ann': row['return_ann'],
#         'sharpe_ratio': row['sharpe_ratio'],
#         'max_drawdown': row['max_drawdown'],
#         'trades': row['trades'],
#     }
#     # Adicionando a nova linha ao DataFrame
#     resultados_consolidados = pd.concat(
#         [resultados_consolidados, pd.DataFrame([nova_linha])],
#         ignore_index=True
#     )

# colunas_ordenacao = ['ativo', 'janela_rsi', 'ordem', 'lookback', 'break_min', 'sl', 'pt']
# resultados_consolidados = resultados_consolidados.sort_values(by=colunas_ordenacao)

# # cria a colunas adicionais para cálculo das notas

# resultados_consolidados['min_return_ann'] = resultados_consolidados.groupby(['ativo', 'cenario'])['return_ann'].transform('min')
# resultados_consolidados['min_sharpe_ratio'] = resultados_consolidados.groupby(['ativo', 'cenario'])['sharpe_ratio'].transform('min')
# resultados_consolidados['min_max_drawdown'] = resultados_consolidados.groupby(['ativo', 'cenario'])['max_drawdown'].transform('min')
# resultados_consolidados['min_trades'] = resultados_consolidados.groupby(['ativo', 'cenario'])['trades'].transform('min')

# resultados_consolidados['max_return_ann'] = resultados_consolidados.groupby(['ativo', 'cenario'])['return_ann'].transform('max')
# resultados_consolidados['max_sharpe_ratio'] = resultados_consolidados.groupby(['ativo', 'cenario'])['sharpe_ratio'].transform('max')
# resultados_consolidados['max_max_drawdown'] = resultados_consolidados.groupby(['ativo', 'cenario'])['max_drawdown'].transform('max')
# resultados_consolidados['max_trades'] = resultados_consolidados.groupby(['ativo', 'cenario'])['trades'].transform('max')


# # Agora criamos as notas obtidas entre 0 e 10, conforme o valor pro-rata entre a menor média e a maior média

# resultados_consolidados['Pontos_return_ann'] = \
#     10 * (resultados_consolidados['return_ann'] - resultados_consolidados['min_return_ann'])\
#             / (resultados_consolidados['max_return_ann'] - resultados_consolidados['min_return_ann'])

# resultados_consolidados['Pontos_sharpe_ratio'] = \
#     10 * (resultados_consolidados['sharpe_ratio'] - resultados_consolidados['min_sharpe_ratio'])\
#             / (resultados_consolidados['max_sharpe_ratio'] - resultados_consolidados['min_sharpe_ratio'])

# resultados_consolidados['Pontos_max_drawdown'] = \
#     10 * (resultados_consolidados['max_drawdown'] - resultados_consolidados['min_max_drawdown'])\
#             / (resultados_consolidados['max_max_drawdown'] - resultados_consolidados['min_max_drawdown'])

# resultados_consolidados['Pontos_trades'] = \
#     10 * (resultados_consolidados['trades'].astype(float) - resultados_consolidados['min_trades'].astype(float))\
#             / (resultados_consolidados['max_trades'].astype(float) - resultados_consolidados['min_trades'].astype(float))

# # Para concluir, vamos obter os pontos ponderados usando os pesos definidos anteriormente

# peso_annual_return = 3
# peso_sharpe_ratio = 2
# peso_drawdown = 1
# peso_trades = 1

# resultados_consolidados['Pontos_ponderados'] = \
# (\
#     peso_annual_return * resultados_consolidados['Pontos_return_ann'] + \
#     peso_sharpe_ratio* resultados_consolidados['Pontos_sharpe_ratio'] + \
#     peso_drawdown* resultados_consolidados['Pontos_max_drawdown'] + \
#     peso_trades*resultados_consolidados['Pontos_trades']\
# )/ (peso_annual_return+peso_sharpe_ratio+peso_drawdown+peso_trades)

# resultados_consolidados = resultados_consolidados.sort_values(
#     by=['num_pontos', 'ativo', 'janela_rsi', 'ordem', 'lookback', 'break_min', 'cenario', 'sl', 'pt'], 
#     ignore_index=True
# )

# file_name_resultados = f'simulações_aplicadas_a_ativos_in_sample_resultados/resultados_in_sample_final.csv'
# resultados_consolidados.to_csv(file_name_resultados, sep=";", decimal=",", index=True, encoding="utf-8")


# # # Criação do DataFrame para armazenar a média dos 3 cenários simulados para cada conjunto único de parâmetros para cada ativo

# media_pontos_ponderados = resultados_consolidados.groupby(
#     ['janela_rsi', 'ordem', 'lookback', 'd_max', 'num_pontos', 
#      'break_min', 'ppt', 'sl', 'pt', 'ativo']
# )['Pontos_ponderados'].mean().reset_index().rename(columns={'Pontos_ponderados': 'media_pontos_ponderados'})

# file_name_melhor_resultado_cenário = f'simulações_aplicadas_a_ativos_in_sample_resultados/media_pontos_ponderados.csv'
# media_pontos_ponderados.to_csv(file_name_melhor_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")

# melhores_resultados_por_ativo_in_sample_1 = media_pontos_ponderados.loc[
#     media_pontos_ponderados.groupby('ativo')['media_pontos_ponderados'].idxmax()
# ].reset_index(drop=True)


# file_name_melhor_resultado_cenário = f'simulações_aplicadas_a_ativos_in_sample_resultados/melhores_resultados_consolidados.csv'
# melhores_resultados_por_ativo_in_sample_1.to_csv(file_name_melhor_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")


# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------
# # Box plot com  janela_rsi ---------------------------------------------------
# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------


# # -------------------------------------------------------------------------
# # Cria o box plot com o retorno anual por janela_rsi ----------------------
# # -------------------------------------------------------------------------

# plt.figure(figsize=(10, 6))

# resultados_consolidados.boxplot(column='return_ann', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Retorno Anual por janela_rsi')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi')
# plt.ylabel('Retorno Anual %')

# # # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/retorno_anual_por_rsi.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI


# # ----------------------------------------------------------------------------
# # Cria o box plot com o número de trades por janela_rsi ----------------------
# # ----------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='trades', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Número de Trades por janela_rsi')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi')
# plt.ylabel('Número de trades')

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/num_trades_por_rsi.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ------------------------------------------------------------------------
# # Cria o box plot com o sharpe_ratio por janela_rsi ----------------------
# # ------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='sharpe_ratio', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Sharpe Ratio por janela_rsi')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi')
# plt.ylabel('Sharpe Ratio')

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/sharpe_ratio_por_rsi.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por janela_rsi ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por janela_rsi')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi')
# plt.ylabel('Percentual de Drawdown Máximo')

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_rsi.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por janela_rsi ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por janela_rsi')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi')
# plt.ylabel('Percentual de Drawdown Máximo')

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_rsi.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI





# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------
# # Box plot com  lookback ---------------------------------------------------
# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------



# # -------------------------------------------------------------------------
# # Cria o box plot com o retorno anual por lookback ----------------------
# # -------------------------------------------------------------------------

# plt.figure(figsize=(10, 6))

# resultados_consolidados.boxplot(column='return_ann', by='lookback', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Retorno Anual por lookback')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('lookback')
# plt.ylabel('Retorno Anual %')

# # # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/retorno_anual_por_lookback.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI


# # ----------------------------------------------------------------------------
# # Cria o box plot com o número de trades por lookback ----------------------
# # ----------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='trades', by='lookback', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Número de Trades por lookback')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('lookback')
# plt.ylabel('Número de trades')

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/num_trades_por_lookback.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ------------------------------------------------------------------------
# # Cria o box plot com o sharpe_ratio por lookback ----------------------
# # ------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='sharpe_ratio', by='lookback', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Sharpe Ratio por lookback')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('lookback')
# plt.ylabel('Sharpe Ratio')

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/sharpe_ratio_por_lookback.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por lookback ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='lookback', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por lookback')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('lookback')
# plt.ylabel('Percentual de Drawdown Máximo')

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_lookback.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por lookback ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='lookback', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por lookback')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('lookback')
# plt.ylabel('Percentual de Drawdown Máximo')

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_lookback.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI








# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------
# # Box plot com  break_min ---------------------------------------------------
# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------



# # -------------------------------------------------------------------------
# # Cria o box plot com o retorno anual por break_min ----------------------
# # -------------------------------------------------------------------------

# plt.figure(figsize=(10, 6))

# resultados_consolidados.boxplot(column='return_ann', by='break_min', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Retorno Anual por break_min')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('break_min')
# plt.ylabel('Retorno Anual %')

# # # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/retorno_anual_por_break_min.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI


# # ----------------------------------------------------------------------------
# # Cria o box plot com o número de trades por break_min ----------------------
# # ----------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='trades', by='break_min', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Número de Trades por break_min')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('break_min')
# plt.ylabel('Número de trades')

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/num_trades_por_break_min.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ------------------------------------------------------------------------
# # Cria o box plot com o sharpe_ratio por break_min ----------------------
# # ------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='sharpe_ratio', by='break_min', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Sharpe Ratio por break_min')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('break_min')
# plt.ylabel('Sharpe Ratio')

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/sharpe_ratio_por_break_min.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por break_min ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='break_min', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por break_min')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('break_min')
# plt.ylabel('Percentual de Drawdown Máximo')

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_break_min.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI


# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por break_min ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='break_min', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por break_min')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('break_min')
# plt.ylabel('Percentual de Drawdown Máximo')

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_break_min.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# ----------------------------------------------------------------------
# Cria o scattered para o in_sample ----------------------
# ----------------------------------------------------------------------

file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/resultados_in_sample_final.csv'
resultados_consolidados = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")

# Definindo as cores com base nas condições
cores = [
    'blue' if (row['sharpe_ratio'] > 0.75 and row['return_ann'] > 10) else
    'gray' if (row['sharpe_ratio'] > 0 and row['return_ann'] > 0) else
    'red'
    for _, row in resultados_consolidados.iterrows()
]

# Configuração do gráfico
plt.figure(figsize=(12, 8))

cenarios = ['in_sample_1_1x', 'in_sample_2_1x', 'in_sample_3_1x']
cenarios_buy_and_hold = ['in_sample_1_1x', 'in_sample_2_1x', 'in_sample_3_1x']
títulos = ['in_sample_1', 'in_sample_2', 'in_sample_3']
marcadores = ['x', 'o', '*']
cores_legenda = ['black', 'black', 'black']

file_name = f'base_dados_ativos_simulados/resultados.csv'
df_buy_and_hold= pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")


# Loop para criar gráficos por cenário
for i, cenario in enumerate(cenarios):
    # Filtra apenas os dados do cenário atual
    df_cenario = resultados_consolidados[resultados_consolidados['cenario'] == cenario]

    # Cria uma nova figura para cada cenário
    plt.figure(figsize=(12, 8))
    plt.scatter(
        df_cenario['return_ann'], df_cenario['sharpe_ratio'],
        c=[cores[idx] for idx in df_cenario.index], marker=marcadores[i], label=f'{títulos[i]}'
    )

    # Linhas horizontais e verticais
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
    plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
    plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

        # Filtra os dados de buy and hold para o mesmo cenário do loop
    df_buy_and_hold_cenario = df_buy_and_hold[df_buy_and_hold['Cenario'] == cenarios_buy_and_hold[i]]

    # Adiciona os pontos de buy and hold ao mesmo gráfico
    plt.scatter(
        df_buy_and_hold_cenario['Retorno_Anual_Medio'], df_buy_and_hold_cenario['Sharpe_Ratio'],
        c='black', marker='x', label='Buy and Hold'
    )

    # Configuração de títulos e eixos
    plt.title(f'Dispersão dos Resultados: {títulos[i]}', fontsize=16)
    plt.xlabel('Retorno Anual (%)', fontsize=12)
    plt.ylabel('Sharpe Ratio', fontsize=12)

    # Grade e legenda
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title='Cenário', fontsize=12, frameon=False)

    # Salvar gráfico como imagem
    file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/dispersao_cenario_{cenario}.png'
    plt.savefig(file_name, dpi=300)
    plt.close()  # Fecha a figura atual para evitar sobreposição



# Resultados para out_of_sample_final_1 (marcados com "x")
df1 = resultados_consolidados[resultados_consolidados['cenario'] == 'in_sample_1_1x']
plt.scatter(
    df1['return_ann'], df1['sharpe_ratio'],
    c=[cores[i] for i in df1.index], marker='x', label='_nolegend_'  # Evita adicionar as cores na legenda
)

# Resultados para out_of_sample_final_1 (marcados com "x")
df1 = resultados_consolidados[resultados_consolidados['cenario'] == 'in_sample_2_1x']
plt.scatter(
    df1['return_ann'], df1['sharpe_ratio'],
    c=[cores[i] for i in df1.index], marker='o', label='_nolegend_'  # Evita adicionar as cores na legenda
)

# Resultados para out_of_sample_final_1 (marcados com "x")
df1 = resultados_consolidados[resultados_consolidados['cenario'] == 'in_sample_3_1x']
plt.scatter(
    df1['return_ann'], df1['sharpe_ratio'],
    c=[cores[i] for i in df1.index], marker='*', label='_nolegend_'  # Evita adicionar as cores na legenda
)

# Adiciona os pontos de buy and hold ao mesmo gráfico
plt.scatter(
    df_buy_and_hold['Retorno_Anual_Medio'], df_buy_and_hold['Sharpe_Ratio'],
    c='black', marker='x', label='Buy and Hold'
)

# Adicionando manualmente os itens na legenda
plt.scatter([], [], color='black', marker='x', label='in_sample_1_1x')
plt.scatter([], [], color='black', marker='o', label='in_sample_2_1x')
plt.scatter([], [], color='black', marker='*', label='in_sample_3_1x')

# Adicionando linhas horizontais e verticais sem incluir na legenda:
# Linhas para Sharpe Ratio e Retorno iguais a zero
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)

# Linhas para Sharpe Ratio = 0.75 e Retorno = 10
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configuração de títulos e eixos
plt.title('Dispersão dos Resultados: Retorno Anual vs Sharpe Ratio', fontsize=16)
plt.xlabel('Retorno Anual (%)', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)

# Adiciona uma grade
plt.grid(True, linestyle='--', alpha=0.5)

# Adiciona a legenda com marcadores em preto
plt.legend(title='Cenário', fontsize=12, frameon=False)

file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/dispersão_cenario_todos_cenarios.png'
plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI
